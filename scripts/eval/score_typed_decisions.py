"""Score a Jev-compatible server on LocalLLaMA/typed-decisions (test: 400 cases x 5 questions, Apache-2.0).

Each case goes as one request (the dataset's `state` + `questions` are a /v1/systemone body; its README asks for the
whole case in one request). Metric as on the dataset's leaderboard: argmax of the answer's probabilities vs the gold
`label` (the argmax of a 4B-class teacher's 3-sample mean; teacher self-agreement 0.735 is the ceiling). A failed
request counts as wrong. Zero-shot for selfjev: none of the 400 test states is in data/all.jsonl.gz (2026-09-30 check).

usage (server running): uv run python scripts/eval/score_typed_decisions.py --url http://127.0.0.1:8000 --name selfjev-4b-vision \
    --parquet td_test.parquet --out reports/competitors/typed_decisions
"""

import argparse
import concurrent.futures as cf
import json
from collections import defaultdict
from pathlib import Path

import pyarrow.parquet as pq
from score_systemone import post


def pred_label(a: dict, qtype: str) -> str:
    probs = a.get("probabilities")
    if qtype == "noul" and not probs:
        return "true" if float(a["noul"]) > 0.5 else "false"
    return max(probs, key=lambda k: float(probs[k]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--path", default="/v1/systemone")
    ap.add_argument("--name", required=True)
    ap.add_argument("--model", default="default")
    ap.add_argument("--parquet", required=True, help="test/0.parquet of LocalLLaMA/typed-decisions (config all)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--extra", default="{}", help="JSON merged into every request body")
    a = ap.parse_args()
    cases = pq.read_table(a.parquet).to_pylist()

    def one(c):
        qs, gold = json.loads(c["questions"]), json.loads(c["gold"])
        try:
            ans = post(a.url + a.path, {"model": a.model, "state": json.loads(c["state"]), "questions": qs} | json.loads(a.extra), 600)[
                "answers"
            ]
        except Exception as e:
            ans, err = {}, repr(e)[:200]
        else:
            err = None
        out = []
        for k, q in qs.items():
            try:
                p = pred_label(ans[k], q["type"])
            except Exception:
                p = None
            out.append(
                {
                    "id": c["id"],
                    "workflow": c["workflow"],
                    "q": k,
                    "type": q["type"],
                    "gold": gold[k]["label"],
                    "pred": p,
                    "correct": p == gold[k]["label"],
                    "error": err,
                }
            )
        return out

    with cf.ThreadPoolExecutor(a.workers) as pool:
        rows = [r for rs in pool.map(one, cases) for r in rs]
    acc = lambda rs: round(100 * sum(r["correct"] for r in rs) / len(rs), 1)
    by = defaultdict(list)
    for r in rows:
        by["type:" + r["type"]].append(r)
        by["workflow:" + r["workflow"]].append(r)
    res = {
        "name": a.name,
        "n": len(rows),
        "accuracy": acc(rows),
        "failed": sum(r["pred"] is None for r in rows),
        "slices": {k: acc(v) for k, v in sorted(by.items())},
    }
    d = Path(a.out) / a.name
    d.mkdir(parents=True, exist_ok=True)
    (d / "result.json").write_text(json.dumps(res, indent=1))
    (d / "predictions.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    print("TYPED", json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
