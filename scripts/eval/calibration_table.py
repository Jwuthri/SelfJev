"""Accuracy and calibration of eval reports on eval2 and the dev benchmark (test): Brier, 10-bin ECE over every decision,
wrong decisions, how many were >= 0.9 sure, mean confidence when wrong, and a paired exact McNemar against the first run.

  uv run python scripts/eval/calibration_table.py qwen35_4b_tree_scratch_jevall_ jev     # selfjev-4b vs Jev

A name is a report directory under reports/ (with eval2/report.json and test/report.json), or "jev" (reports/external/).
"""

import json
import sys
from pathlib import Path

from selfjev.evaluation.stats import mcnemar


def path(run, split):
    if run == "jev":
        return Path(f"reports/external/{'eval2' if split == 'eval2' else 'full'}/typesafe_jev-latest/report.json")
    return Path(f"reports/{run}/{split}/report.json")


def decisions(p):
    """-> [(confidence of each decision, decision right)], the question's Brier score."""
    t, probs, cids = p["type"], p["probabilities"], p["candidate_ids"]
    if t == "multiclass":
        y = [float(c == p["target"]) for c in cids]
        k = max(range(len(probs)), key=probs.__getitem__)
        return [(probs[k], y[k] == 1.0)], sum((a - b) ** 2 for a, b in zip(probs, y))
    ys = [float(p["target"])] if t == "binary" else [float(c in p["target"]) for c in cids]
    return [(max(q, 1 - q), (q >= 0.5) == (y == 1.0)) for q, y in zip(probs, ys)], sum(2 * (q - y) ** 2 for q, y in zip(probs, ys)) / len(
        ys
    )


def stats(run, split):
    preds = {x["id"]: x for x in json.loads(path(run, split).read_text())["predictions"]}
    conf, brier = [], 0.0
    for p in preds.values():
        d, b = decisions(p)
        conf += d
        brier += b
    bins = [min(int(10 * c), 9) for c, _ in conf]
    ece = sum(abs(sum(c - h for (c, h), b in zip(conf, bins) if b == k)) for k in range(10)) / len(conf)
    wrong = [c for c, h in conf if not h]
    return {i: p["correct"] for i, p in preds.items()}, {
        "acc": 100 * sum(p["correct"] for p in preds.values()) / len(preds),
        "brier": brier / len(preds),
        "ece": ece,
        "wrong": len(wrong),
        "sure": sum(c >= 0.9 for c in wrong),
        "mean": sum(wrong) / max(1, len(wrong)),
    }


if __name__ == "__main__":
    runs = sys.argv[1:]
    for split in ("eval2", "test"):
        base, _ = stats(runs[0], split)
        print(
            f"\n{split} ({len(base)} q) | accuracy | vs {runs[0]}: only this right / only it right, p | Brier | ECE | "
            "wrong decisions | >= 0.9 sure | mean confidence when wrong"
        )
        print("|---|---|---|---|---|---|---|---|")
        for run in runs:
            ok, s = stats(run, split)
            assert set(ok) == set(base), (run, split, len(set(ok) ^ set(base)))
            oa, ob, pv = mcnemar(ok, base)
            vs = "" if run == runs[0] else f"{oa} / {ob}, p = {pv:.2g}"
            print(f"| {run} | {s['acc']:.2f} | {vs} | {s['brier']:.4f} | {s['ece']:.4f} | {s['wrong']} | {s['sure']} | {s['mean']:.3f} |")
