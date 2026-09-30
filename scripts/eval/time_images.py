"""Latency of one request on this GPU: text only vs an image (cold = loads the vision tower, then warm), with the time split
into tokenize + image preprocessing (CPU) and the model. Photos come from data/ova/eval_pets.jsonl.

usage: uv run python scripts/eval/time_images.py [--adapter weights/selfjev_4b] [--n 20]
"""

import argparse
import json
import statistics as st
import time

from selfjev.core.schemas import parse_request
from selfjev.engine.tree import TreeServer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", default="weights/selfjev_4b")
    ap.add_argument("--n", type=int, default=20)
    a = ap.parse_args()
    with open("data/ova/eval_pets.jsonl") as f:
        rows = [json.loads(line) for _, line in zip(range(400), f)]
    photos = list(dict.fromkeys(r["state"] for r in rows))[: a.n + 1]
    cats = next(r["question"] for r in rows if r["family"] == "pets_cat_breed")  # 12 options
    yn = {"type": "binary", "instruction": "Is the animal in this photo a cat?"}
    srv = TreeServer(a.adapter)

    def one(state, qs):
        t = time.perf_counter()
        _, stats = srv.score_requests([parse_request({"state": state, "questions": [{"id": f"q{i}", **q} for i, q in enumerate(qs)]})])
        return {
            "ms": 1e3 * (time.perf_counter() - t),
            "prep_ms": stats["tokenize_ms"],
            "model_ms": stats["model_ms"],
            "tokens": stats["input_tokens"],
        }

    text = "Ticket 4411: the invoice was charged twice and the customer wants the second charge back. " * 3
    one(text, [yn])  # warm the text path
    out = {"text, 1 question": [one(text, [yn]) for _ in range(a.n)]}
    cold = one(photos[0], [yn])
    out["image, 1 yes/no"] = [one(p, [yn]) for p in photos[1:]]
    out["image, 12-way choice"] = [one(p, [cats]) for p in photos[1:]]
    out["image, 1 yes/no + 12-way + 3 more"] = [one(p, [yn, cats, yn, yn, yn]) for p in photos[1:]]
    print(f"first image request (loads the vision tower): {cold['ms']:.0f} ms")
    print(f"{'request':40s} {'median ms':>10s} {'p90 ms':>8s} {'cpu prep':>9s} {'model':>7s} {'tokens':>7s}")
    for k, v in out.items():
        ms = sorted(x["ms"] for x in v)
        print(f"{k:40s} {st.median(ms):10.0f} {ms[int(0.9 * len(ms))]:8.0f} {st.median(x['prep_ms'] for x in v):9.0f} "
              f"{st.median(x['model_ms'] for x in v):7.0f} {int(st.median(x['tokens'] for x in v)):7d}")  # fmt: skip
    with open("timing.json", "w") as f:
        json.dump({"first_image_ms": cold["ms"], "runs": out, "meta": srv.meta}, f, indent=1)


if __name__ == "__main__":
    main()
