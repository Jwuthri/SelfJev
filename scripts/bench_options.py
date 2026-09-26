"""Latency of the two option formats through vLLM, in-process (model resident, no network), as options grow:
  ova  every option listed in the question, each leaf repeats its full description (data/ova/, --options-in-question)
  ptr  options numbered once in the question, each leaf says only "option k"      (data/ptr/, --option-pointers)
Every request has a fresh random text, so no prefix-cache hit can come from an earlier request. p50 / p95 of classify().

usage (vLLM venv): python scripts/bench_options.py --model-dir runs/X/merged --model-id Qwen/Qwen3-4B-Instruct-2507 \
    --mode ptr --out reports/X/bench_options_ptr.json
"""
import argparse
import json
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from personal_jev.benchmark import FILLER  # noqa: E402
from personal_jev.classify import classify  # noqa: E402
from personal_jev.options import with_options  # noqa: E402
from personal_jev.vllm_tree import VllmTreeScorer  # noqa: E402


def request(tok, n_tokens, n_q, n_opt, nonce, mode):
    text = f"Ticket {nonce:06d}. " + FILLER * (n_tokens // 60 + 2)
    state = tok.decode(tok(text, add_special_tokens=False)["input_ids"][:n_tokens])
    qs = [{"id": f"q{i}", "type": "multiclass", "instruction": f"Which team should handle issue number {i + 1} in this message?",
           "candidates": [{"id": f"t{j}", "description": f"Team {j + 1}: handles category {j + 1} problems such as outages, billing "
                                                         f"errors or integration failures"} for j in range(n_opt)]} for i in range(n_q)]
    return {"state": state, "questions": [with_options(q, q["id"], pointers=mode == "ptr") for q in qs]}


ap = argparse.ArgumentParser()
ap.add_argument("--model-dir", required=True)
ap.add_argument("--model-id", required=True)
ap.add_argument("--mode", choices=["ova", "ptr"], required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--reps", type=int, default=10)
a = ap.parse_args()
sc = VllmTreeScorer(a.model_dir, model_id=a.model_id, max_length=16384)
rng, rows = random.Random(0), []
for n_tokens in (512, 2048):
    for n_q in (1, 16):
        for n_opt in (3, 8, 32, 64):
            ms, meta = [], None
            for rep in range(a.reps + 1):  # rep 0 = warm-up
                meta = classify(sc, request(sc.tokenizer, n_tokens, n_q, n_opt, rng.randrange(10 ** 6), a.mode))["meta"]
                if rep:
                    ms.append(meta["total_ms"])
            ms.sort()
            rows.append({"mode": a.mode, "text_tokens": n_tokens, "questions": n_q, "options": n_opt, "p50_ms": statistics.median(ms),
                         "p95_ms": ms[min(len(ms) - 1, round(0.95 * (len(ms) - 1)))], "input_tokens": meta["input_tokens"],
                         "leaf_tokens_submitted": meta["padded_tokens"]})
            print(json.dumps(rows[-1]), flush=True)
Path(a.out).parent.mkdir(parents=True, exist_ok=True)
Path(a.out).write_text(json.dumps({"meta": sc.meta | {"created": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, "rows": rows}, indent=1))
