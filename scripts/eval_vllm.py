"""Score a merged tree checkpoint through vLLM (the serving path) -> report.json / report.md like `pjev eval`, to check
that serving keeps the accuracy measured with transformers. Data files are used as given (data/ova/ for adapters
trained with every option in the question).

usage (vLLM venv, on a GPU box):
  python scripts/eval_vllm.py --model-dir runs/X/merged --model-id Qwen/Qwen3-4B-Instruct-2507 \
      --data data/ova/eval2.jsonl --split test --out reports/X/eval2_vllm
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from personal_jev.data import load, sha256_file  # noqa: E402
from personal_jev.evaluate import breakdowns, evaluate_predictions, markdown, predict  # noqa: E402
from personal_jev.vllm_qwen35 import VllmQwen35Scorer  # noqa: E402
from personal_jev.vllm_tree import VllmTreeScorer  # noqa: E402

if __name__ == "__main__":  # vLLM may spawn its engine process, which re-imports this module
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--model-id", help="the tree checkpoint's base model (not needed with --qwen35)")
    ap.add_argument("--qwen35", action="store_true", help="a merged Qwen3.5 shared-document model (personal_jev.vllm_qwen35)")
    ap.add_argument("--data", nargs="+", required=True)
    ap.add_argument("--split", nargs="+", default=["test"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-length", type=int, default=16384)
    ap.add_argument("--quantization", help="vLLM quantization for a bf16 checkpoint, e.g. fp8 (tree path only)")
    a = ap.parse_args()
    sc = VllmQwen35Scorer(a.model_dir, max_length=a.max_length) if a.qwen35 else VllmTreeScorer(a.model_dir, model_id=a.model_id, max_length=a.max_length, quantization=a.quantization)
    examples = load(a.data, set(a.split))
    t0, preds = time.perf_counter(), []
    for k in range(0, len(examples), 128):
        preds += predict(sc, examples[k:k + 128])[0]
    rep = {"meta": sc.meta | {"calibration": None, "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "wall_s": time.perf_counter() - t0,
                              "n": len(preds), "splits": a.split, "data": [{"path": p, "sha256": sha256_file(p)} for p in a.data]},
           "metrics": evaluate_predictions(preds), **breakdowns(preds), "predictions": preds}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(rep, indent=1))
    (out / "report.md").write_text(markdown(rep))
    print(f"{a.out}: question accuracy {100 * rep['metrics']['question_accuracy']:.2f}% over {len(preds)} questions in {rep['meta']['wall_s']:.0f}s")
