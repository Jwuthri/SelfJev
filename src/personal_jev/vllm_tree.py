"""The tree format served by vLLM (CUDA graphs, fused kernels, paged KV cache) instead of plain transformers.

Each leaf becomes one prompt: the exact standalone sequence the tree scores (root + question + leaf tokens).
vLLM's prefix cache computes the shared root and question once and reuses their KV blocks for the other leaves,
so the text is still read once per request. Readout: vLLM's Qwen3-reranker conversion, a 1-logit head
lm_head[yes] - lm_head[no], i.e. s = z_yes - z_no, then classify.decide as for every backend.
Needs the LoRA merged into a checkpoint (`merge`), and a separate venv with vllm (its own torch pin).

  python -m personal_jev.vllm_tree merge --adapter runs/tree_4b/adapter --out runs/tree_4b/merged   # project venv
  python -m personal_jev.vllm_tree serve --model-dir runs/tree_4b/merged --port 8002                 # vllm venv
"""
import argparse
import time

from .tree import FORMAT, RERANKER_4B, Encoder, TreeScorer, format_config, leaf_paths


def merge(adapter, out, model_id=RERANKER_4B[0], revision=RERANKER_4B[1]):
    """Merged weights + the ORIGINAL config/tokenizer files (vLLM's transformers may not read a re-saved 5.x config)."""
    import shutil
    from pathlib import Path

    import torch
    from huggingface_hub import snapshot_download
    from peft import PeftModel
    from transformers import AutoModelForCausalLM
    lm = AutoModelForCausalLM.from_pretrained(model_id, revision=revision, dtype=torch.bfloat16)
    PeftModel.from_pretrained(lm, adapter).merge_and_unload().save_pretrained(out)
    src = Path(snapshot_download(model_id, revision=revision, allow_patterns=["*.json", "*.txt", "*.jinja"]))
    for f in [f for pat in ("*.json", "*.txt", "*.jinja") for f in src.glob(pat)]:  # the snapshot also holds the original shards
        if f.name not in ("model.safetensors.index.json", "modules.json", "sentence_bert_config.json", "config_sentence_transformers.json"):
            # skip: the original shard index, and sentence-transformers files whose 1_LogitScore module we don't copy
            shutil.copy(f, Path(out) / f.name)


class VllmTreeScorer:
    trees, check_lengths = TreeScorer.trees, TreeScorer.check_lengths  # same tree building and length checks

    def __init__(self, model_dir, model_id=RERANKER_4B[0], max_length=8192, gpu_memory_utilization=0.85):
        from transformers import AutoTokenizer
        from vllm import LLM, PoolingParams
        self.max_length, self.tokenizer = max_length, AutoTokenizer.from_pretrained(model_dir)
        self.enc = Encoder(self.tokenizer, model_id)
        self.llm = LLM(model=model_dir, runner="pooling", dtype="bfloat16", max_model_len=max_length, enable_prefix_caching=True,
                       gpu_memory_utilization=gpu_memory_utilization,
                       hf_overrides={"architectures": ["Qwen3ForSequenceClassification"], "classifier_from_token": ["no", "yes"],
                                     "is_original_qwen3_reranker": True})
        fields = getattr(PoolingParams, "__struct_fields__", ())  # raw logit, no sigmoid (the flag was renamed across versions)
        self.params = PoolingParams(**{"use_activation" if "use_activation" in fields else "activation": False})
        self.meta = {"model": model_id, "revision": RERANKER_4B[1], "architecture": f"shared-prefix tree ({FORMAT}) on vLLM prefix cache",
                     "adapter": f"merged into {model_dir}", "adapter_sha256": None, "prompt": FORMAT, "prompt_sha": format_config(model_id)["sha"],
                     "device": "cuda", "dtype": "bfloat16", "max_length": max_length, "truncation": "none (overlength input raises InputTooLong)"}

    def score_requests(self, reqs):
        t0 = time.perf_counter()
        trees, owners = self.trees(reqs)
        self.check_lengths(trees, owners)
        prompts = [{"prompt_token_ids": [t["ids"][i] for i in p]} for t in trees for p in leaf_paths(t)]
        t1 = time.perf_counter()
        scores = iter([o.outputs.probs[0] for o in self.llm.classify(prompts, pooling_params=self.params, use_tqdm=False)])
        t2 = time.perf_counter()
        by_q = {}
        for own in owners:
            for ri, qid, _ in own:
                by_q.setdefault((ri, qid), []).append(next(scores))
        state_tokens = sum(t["root"] for t in trees)
        return [[by_q[ri, q.id] for q in r.questions] for ri, r in enumerate(reqs)], {
            "pairs": len(prompts), "batches": 1, "input_tokens": sum(len(t["ids"]) for t in trees),
            "padded_tokens": sum(len(p["prompt_token_ids"]) for p in prompts),  # tokens submitted before prefix-cache hits
            "state_sequences": len(trees), "state_tokens": state_tokens, "tokenize_ms": 1e3 * (t1 - t0), "model_ms": 1e3 * (t2 - t1)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("merge")
    p.add_argument("--adapter", required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("serve")
    p.add_argument("--model-dir", required=True)
    p.add_argument("--port", type=int, default=8002)
    a = ap.parse_args()
    if a.cmd == "merge":
        merge(a.adapter, a.out)
    else:
        from .server import serve
        serve(VllmTreeScorer(a.model_dir), port=a.port)
