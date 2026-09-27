"""Training data with Jev's probabilities as soft targets, from data/all.jsonl.gz (user request 2026-09-26: train on all
of it, distilling Jev's hedging).

  uv run python scripts/train/jev_soft_targets.py   # free, local: writes runs/jev_all/{train,val}.jsonl.gz

- Train: every non-test row of the training datasets (train + validation splits), minus the validation sample. Out:
  test rows, the frozen / benchmark datasets (eval, eval2, eval_llm, compact_challenge_v1:
  selfjev.data.catalog.TEST_DATASETS) and the calibration splits (kept for temperature fitting). No family cap, no `none` rebalance.
- Val: the same 1,200 validation questions as every Qwen3.5 run, so validation numbers compare across runs.
- Each training row gains "soft" from its `jev` field: P(yes) (binary) or {candidate id: p} (multiclass: Jev's
  distribution; multilabel: P(yes) per option). The target stays the verified one; `selfjev finetune / rlcd --soft-weight`
  (default 0.5) mixes the two, so Jev never decides a label. Questions stay as in all.jsonl.gz: selfjev adds the option
  list (options_in_question, seeded by id, as data/ova was built).
"""

import gzip
import json
from collections import Counter
from pathlib import Path

from selfjev.data.catalog import TEST_DATASETS

OUT = Path("runs/jev_all")


def val_ids():
    """The 1,200-question validation sample of every Qwen3.5 run (drawn with seed 13 by run_qwen35.py, at tag
    archive/pre-cleanup-2026-09-27), frozen in data/val_sample_1200.txt."""
    return set(Path("data/val_sample_1200.txt").read_text().split())


def label_prob(r, s):
    """Jev's probability of the verified answer; multilabel: its least-agreeing option."""
    t, q = r["target"], r["question"]["type"]
    if q == "binary":
        return s if t else 1 - s
    if q == "multiclass":
        return s[t]
    return min(p if c in t else 1 - p for c, p in s.items())


def main():
    with gzip.open("data/all.jsonl.gz", "rt") as f:
        rows = [json.loads(line) for line in f]
    vids = val_ids()
    val = [r for r in rows if r["id"] in vids and r["split"] != "test"]
    train = [
        r | {"soft": r["jev"]["p_yes"] if r["question"]["type"] == "binary" else r["jev"]["probs"]}
        for r in rows
        if r["dataset"] not in TEST_DATASETS and r["split"] in ("train", "validation") and r["id"] not in vids
    ]
    assert len(val) == len(vids), (len(val), len(vids))
    assert not any(r["split"] == "test" or r["dataset"] in TEST_DATASETS for r in train)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, part in (("train", train), ("val", val)):
        with gzip.open(OUT / f"{name}.jsonl.gz", "wt") as f:
            f.writelines(json.dumps({k: v for k, v in r.items() if k != "jev"}) + "\n" for r in part)
    print(f"train {len(train)} questions, val {len(val)} -> {OUT}/")
    for (d, s), n in sorted(Counter((r["dataset"], r["split"]) for r in train).items()):
        print(f"  {d:16s} {s:11s} {n:6d}")
    pl = [label_prob(r, r["soft"]) for r in train]
    print(
        f"Jev's probability of the verified answer: >= 0.9 on {sum(p >= 0.9 for p in pl) / len(pl):.1%} (soft target ~ label), "
        f"0.5-0.9 on {sum(0.5 <= p < 0.9 for p in pl) / len(pl):.1%} (hedges), "
        f"< 0.5 on {sum(p < 0.5 for p in pl) / len(pl):.1%} (disagrees)"
    )


if __name__ == "__main__":
    main()
