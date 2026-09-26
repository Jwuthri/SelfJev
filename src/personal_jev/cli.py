"""pjev: classify | eval | calibrate | compare | bench | serve | train | train-custom | train-tree | finetune | rlcd"""
import argparse
import json
import sys
from pathlib import Path

from .formatting import DEFAULT_PROMPT, PROMPTS
from .model import MODEL_ID, MODEL_REVISION


def _scorer(a):
    if a.jina:
        from .jina import JINA, JinaScorer
        model, rev = (a.model, a.revision) if a.model.startswith("jinaai/") else JINA
        return JinaScorer(model, rev, adapter=a.adapter, device=a.device, dtype=a.dtype, max_length=a.max_length, max_batch_tokens=a.max_batch_tokens)
    if a.tree:
        from .tree import TreeScorer
        return TreeScorer(a.model, a.revision, adapter=a.adapter, device=a.device, dtype=a.dtype, max_length=a.max_length,
                          max_batch_tokens=a.max_batch_tokens, merge=a.merge)
    if a.checkpoint:
        from .custom import CustomScorer
        return CustomScorer(a.checkpoint, device=a.device, dtype=a.dtype, max_length=a.max_length,
                            max_candidate_length=a.max_candidate_length, max_batch_tokens=a.max_batch_tokens)
    from .model import Scorer
    return Scorer(adapter=a.adapter, device=a.device, dtype=a.dtype, max_length=a.max_length, max_batch_tokens=a.max_batch_tokens,
                  model_id=a.model, revision=a.revision)


def _calibration(a, scorer):
    if not a.calibration:
        return None
    from . import calibration
    from .formatting import prompt_sha
    return calibration.load(a.calibration, scorer.meta, scorer.meta.get("prompt_sha") or prompt_sha(a.prompt))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pjev", description="Instruction-conditioned classification on Qwen3-Reranker-0.6B: "
                                 "custom shared-state model (--checkpoint) or the stock reranker backend")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def model_args(p):
        p.add_argument("--tree", action="store_true", help="shared-prefix tree scorer (tree.py) on --model/--revision; "
                                                                "--adapter from `pjev train-tree`")
        p.add_argument("--jina", action="store_true", help="jina-reranker-v3.5 listwise scorer (jina.py); --adapter from `pjev train-jina`")
        p.add_argument("--checkpoint", help="custom shared-state model checkpoint (from `pjev train-custom`); "
                                            "default: the stock reranker backend")
        p.add_argument("--model", default=MODEL_ID, help="stock backend: Qwen3-Reranker checkpoint (0.6B / 4B / 8B)")
        p.add_argument("--revision", default=MODEL_REVISION, help="stock backend: pinned HF commit for --model")
        p.add_argument("--merge", action="store_true", help="--tree: merge the LoRA adapter into the weights (inference speed)")
        p.add_argument("--adapter", help="stock backend only: LoRA adapter directory (default: unmodified base model)")
        p.add_argument("--device", help="cuda | mps | cpu (default: best available)")
        p.add_argument("--dtype", default="float32", choices=["float32", "bfloat16", "float16"])
        p.add_argument("--max-length", type=int, default=8192, help="max tokens per pair (custom: per state) incl. template; "
                                                                        "longer input is an error")
        p.add_argument("--max-candidate-length", type=int, default=512, help="custom model: max tokens per question+candidate text")
        p.add_argument("--max-batch-tokens", type=int, default=16384, help="padded tokens per forward pass")
        p.add_argument("--calibration", help="calibration JSON from `pjev calibrate` (must match model/adapter/prompt)")
        p.add_argument("--prompt", default=DEFAULT_PROMPT, choices=sorted(PROMPTS), help="question-to-pair mapping (see formatting.py)")

    p = sub.add_parser("classify", help="classify one request JSON (file path or - for stdin)")
    p.add_argument("request")
    model_args(p)
    p = sub.add_parser("eval", help="evaluate JSONL examples; writes report.json and report.md")
    p.add_argument("--data", nargs="+", required=True)
    p.add_argument("--split", nargs="*", help="only these splits (e.g. validation); default all")
    p.add_argument("--out", required=True)
    p.add_argument("--limit", type=int)
    model_args(p)
    p = sub.add_parser("calibrate", help="fit temperatures on a calibration-split report; thresholds on a validation-split report")
    p.add_argument("--fit", required=True, help="report.json from `pjev eval --split calibration`")
    p.add_argument("--thresholds", help="report.json from `pjev eval --split validation`")
    p.add_argument("--out", required=True)
    p = sub.add_parser("compare", help="side-by-side markdown of two or more eval reports")
    p.add_argument("reports", nargs="+")
    p.add_argument("--names", nargs="*")
    p.add_argument("--out")
    p = sub.add_parser("bench", help="latency / throughput / memory benchmark")
    model_args(p)
    p.add_argument("--lengths", default="512,2048,8192")
    p.add_argument("--questions", default="1,4,16")
    p.add_argument("--repeats", type=int, default=20, help="max samples per row (at least 3; ~60 s budget per row)")
    p.add_argument("--out", required=True)
    p = sub.add_parser("serve", help="local HTTP server: POST /classify and POST /api/alpha/decisions (shape-compatible)")
    model_args(p)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--options-in-question", action="store_true", help="list every option in the question text "
                   "(required for adapters trained on data/ova/)")
    p.add_argument("--option-pointers", action="store_true", help="numbered options in the question, "
                   "'option k' leaves (adapters trained on data/ptr/)")
    p = sub.add_parser("train", help="stock backend: LoRA training from a JSON config")
    p.add_argument("config")
    p.add_argument("--set", nargs="*", default=[], metavar="KEY=JSON", help="override config keys, e.g. max_steps=20")
    p = sub.add_parser("train-custom", help="custom model: new-module warm-up, then LoRA/full backbone adaptation")
    p.add_argument("config")
    p.add_argument("--set", nargs="*", default=[], metavar="KEY=JSON", help="override config keys, e.g. max_steps=20")
    p = sub.add_parser("train-tree", help="shared-prefix tree scorer: LoRA on any Qwen3-architecture causal LM")
    p.add_argument("config")
    p.add_argument("--set", nargs="*", default=[], metavar="KEY=JSON", help="override config keys, e.g. max_steps=20")
    p = sub.add_parser("train-jina", help="jina-reranker-v3.5 listwise scorer: LoRA + projector + head scalars")
    p.add_argument("config")
    p.add_argument("--set", nargs="*", default=[], metavar="KEY=JSON", help="override config keys, e.g. max_steps=20")
    def finetune_args(p, rlcd=False):  # personal_jev.finetune: the Qwen3.5 tree recipe on your JSONL data, one CUDA GPU
        p.add_argument("--data", required=True, help="training JSONL (state, question, target per line)")
        p.add_argument("--val", help="validation JSONL (default: 5%% of --data, at most 1,000 questions)")
        p.add_argument("--out", required=True, help="run directory: adapter/, adapter_last/, train_meta.json")
        p.add_argument("--init", required=rlcd, help="adapter to start from, e.g. weights/qwen35_4b_tree" + (" or a finetune run" if rlcd else ""))
        p.add_argument("--base", default="qwen35_4b", choices=["qwen35_4b", "qwen35"], help="Qwen3.5-4B, or Qwen3.5-2B for quick runs")
        p.add_argument("--no-options-in-question", action="store_true", help="do not list every option in the question text")
        p.add_argument("--epochs", type=int, default=1)
        p.add_argument("--lr", type=float, help="default 2e-4 (finetune), 5e-5 (rlcd)")
        p.add_argument("--lora-r", type=int, default=64, help="LoRA rank when starting without --init")
        p.add_argument("--max-length", type=int, default=8192, help="longer questions are dropped and counted, never truncated")
        p.add_argument("--batch-tokens", type=int, default=8192, help="packed tree tokens per micro-batch")
        p.add_argument("--grad-accum", type=int, default=4)
        p.add_argument("--eval-every", type=int, default=150)
        p.add_argument("--seed", type=int, default=13)
        p.add_argument("--soft-weight", type=float, default=0.5, help="rows with \"soft\" (a teacher's probabilities, e.g. "
                       "scripts/jev_soft_targets.py) train on (1 - w) x label + w x soft")
        if rlcd:
            p.add_argument("--reward", default="log=1,brier=1,spherical=1", help="weighted rewards: log, brier, spherical "
                           "(proper scoring rules), accuracy (not proper), confident_miss (a cost per decision >= 0.9 sure and wrong)")
            p.add_argument("--samples", type=int, default=8, help="sampled reports per question")
            p.add_argument("--sigma", type=float, default=0.3, help="sd of the Gaussian around the logits")
            p.add_argument("--beta", type=float, default=0.05, help="KL penalty to the --init model")

    finetune_args(sub.add_parser("finetune", help="LoRA fine-tune the best recipe (Qwen3.5 + shared-prefix tree) on your data"))
    finetune_args(sub.add_parser("rlcd", help="calibration training with proper scoring rules (Jev's \"RLCD\"), from a fine-tuned adapter"), rlcd=True)
    a = ap.parse_args(argv)

    if a.cmd == "classify":
        from .classify import classify
        scorer = _scorer(a)
        req = json.load(sys.stdin if a.request == "-" else open(a.request))
        print(json.dumps(classify(scorer, req, _calibration(a, scorer), a.prompt), indent=2))
    elif a.cmd == "eval":
        from .evaluate import run
        scorer = _scorer(a)
        rep = run(scorer, a.data, a.split, _calibration(a, scorer), a.out, a.limit, a.prompt)
        print((Path(a.out) / "report.md").read_text())
        print(f"n={rep['meta']['n']} -> {a.out}/report.json")
    elif a.cmd == "calibrate":
        from .calibration import fit
        print(json.dumps(fit(a.fit, a.thresholds, a.out), indent=2))
    elif a.cmd == "compare":
        from .evaluate import compare
        md = compare([json.loads(Path(r).read_text()) for r in a.reports], a.names or [Path(r).parent.name for r in a.reports])
        if a.out:
            Path(a.out).write_text(md)
        print(md)
    elif a.cmd == "bench":
        from .benchmark import default_grid, run
        grid = default_grid(tuple(map(int, a.lengths.split(","))), tuple(map(int, a.questions.split(","))))
        rep = run(a.adapter, a.device, a.dtype, grid, a.repeats, max_batch_tokens=a.max_batch_tokens, out_dir=a.out,
                  checkpoint=a.checkpoint, model_id=a.model, revision=a.revision, tree=a.tree)
        print((Path(a.out) / "bench.md").read_text())
    elif a.cmd == "serve":
        from .server import serve
        scorer = _scorer(a)
        serve(scorer, a.host, a.port, _calibration(a, scorer), a.prompt, a.options_in_question, a.option_pointers)
    elif a.cmd == "train":
        from .train import train
        train(a.config, **{k: json.loads(v) for k, v in (s.split("=", 1) for s in a.set)})
    elif a.cmd == "train-custom":
        from .train_custom import train
        train(a.config, **{k: json.loads(v) for k, v in (s.split("=", 1) for s in a.set)})
    elif a.cmd == "train-tree":
        from .train_tree import train
        train(a.config, **{k: json.loads(v) for k, v in (s.split("=", 1) for s in a.set)})
    elif a.cmd == "train-jina":
        from .train_jina import train
        train(a.config, **{k: json.loads(v) for k, v in (s.split("=", 1) for s in a.set)})
    elif a.cmd in ("finetune", "rlcd"):
        from .finetune import train
        extra = {"reward_weights": {k: float(v) for k, v in (x.split("=") for x in a.reward.split(","))}, "samples": a.samples,
                 "sigma": a.sigma, "beta": a.beta} if a.cmd == "rlcd" else {}
        train(a.cmd, a.data, a.out, a.val, a.init, a.base, not a.no_options_in_question, a.epochs, a.lr, a.lora_r, a.max_length,
              a.batch_tokens, a.grad_accum, a.eval_every, a.seed, soft_weight=a.soft_weight, **extra)


if __name__ == "__main__":
    main()
