"""Expand authored sources into example JSONL with hash-assigned splits, and check train/eval overlap.

  data/eval/raw/*.jsonl      -> data/eval.jsonl       (validation 0.3 / calibration 0.2 / test 0.5 by source_id)
  data/synthetic/raw/*.jsonl -> data/synthetic.jsonl  (train 0.85 / validation 0.05 / calibration 0.05 / test 0.05)

Splits are assigned per source_id, so every question (and paraphrase) about one state lands in one split.
Synthetic sources whose state overlaps an eval state (word 8-gram containment >= 0.3) are dropped, not moved.
Eval review overrides (data/eval/review/overrides.json: {example_id: new_target | null to drop}) are applied last.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from personal_jev.data import expand_source, read_jsonl, split_for, validate_example, write_jsonl  # noqa: E402

EVAL_SPLITS = {"validation": 0.3, "calibration": 0.2, "test": 0.5}
SYN_SPLITS = {"train": 0.85, "validation": 0.05, "calibration": 0.05, "test": 0.05}


def shingles(text, n=8):
    w = re.findall(r"\w+", text.lower())
    return {" ".join(w[i:i + n]) for i in range(max(1, len(w) - n + 1))}


def build(raw_dir, weights, salt):
    out, seen = [], set()
    for f in sorted(Path(raw_dir).glob("*.jsonl")):
        for src in read_jsonl(f):
            if src["source_id"] in seen:
                raise ValueError(f"duplicate source_id {src['source_id']} in {f}")
            seen.add(src["source_id"])
            out += expand_source(src | {"split": split_for(src["source_id"], weights, salt)})
    return out


def main():
    ev = build(ROOT / "data/eval/raw", EVAL_SPLITS, "eval-v1")
    overrides_path = ROOT / "data/eval/review/overrides.json"
    if overrides_path.exists():
        ov = json.loads(overrides_path.read_text())
        ev = [e | {"target": ov[e["id"]]["target"], "notes": ov[e["id"]].get("note", e.get("notes", ""))} if e["id"] in ov else e
              for e in ev if not (e["id"] in ov and ov[e["id"]].get("drop"))]
        for e in ev:
            validate_example(e)
        print(f"applied {len(ov)} review overrides")
    write_jsonl(ROOT / "data/eval.jsonl", ev)
    print("eval:", dict(Counter(e["split"] for e in ev)), dict(Counter(e["question"]["type"] for e in ev)))

    eval_sh = [shingles(s) for s in {e["state"] for e in ev}]
    syn, dropped = build(ROOT / "data/synthetic/raw", SYN_SPLITS, "syn-v1"), set()
    for s in {e["state"] for e in syn}:
        sh = shingles(s)
        if any(len(sh & e) / min(len(sh), len(e)) >= 0.3 for e in eval_sh if e):
            dropped.add(s)
    syn = [e for e in syn if e["state"] not in dropped]
    write_jsonl(ROOT / "data/synthetic.jsonl", syn)
    print("synthetic:", dict(Counter(e["split"] for e in syn)), dict(Counter(e["question"]["type"] for e in syn)),
          f"dropped {len(dropped)} states overlapping eval")

    hf = read_jsonl(ROOT / "data/hf.jsonl") if (ROOT / "data/hf.jsonl").exists() else []
    hits = sum(1 for s in {e["state"] for e in hf if e["split"] == "train"} if (sh := shingles(s)) and
               any(len(sh & e) / min(len(sh), len(e)) >= 0.3 for e in eval_sh if e))
    print(f"hf train states overlapping eval: {hits}")


if __name__ == "__main__":
    main()
