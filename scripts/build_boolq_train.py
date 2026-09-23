"""data/curve/boolq_{100,300,1000,3000}.jsonl: BoolQ TRAIN-split questions in our schema, for the per-task data curve.

Same conversion as scripts/build_hf.py (passage = state, capitalized question + "?", binary target) and the same pinned
dataset revision. The held-out test questions come from BoolQ's validation split; any train row whose passage also
appears in our test/eval data is dropped. The four files are nested prefixes of one seeded shuffle, and the family
name is `boolq_train` so it never mixes with the held-out `heldout_boolq` reports.

usage: uv run --group data python scripts/build_boolq_train.py
"""
import random
from pathlib import Path

import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download

from personal_jev.data import load, validate_example, write_jsonl

REV = "35b264d03638db9f4ce671b711558bf7ff0f80d5"
SIZES = (100, 300, 1000, 3000)
path = hf_hub_download("google/boolq", "data/train-00000-of-00001.parquet", repo_type="dataset", revision=REV)
rows = pq.read_table(path).to_pylist()
seen = {e["state"] for e in load(["data/hf.jsonl", "data/eval.jsonl", "data/synthetic.jsonl"])}
out = []
for i, r in enumerate(rows):
    if r["passage"] in seen:
        continue
    q = r["question"].strip()
    out.append({"id": f"boolq-train-{i}", "source_id": f"boolq-train-{i}", "family": "boolq_train", "split": "train",
                "provenance": f"hf:google/boolq@{REV[:10]}:data/train-00000-of-00001.parquet#{i} (CC-BY-SA-3.0)",
                "state": r["passage"], "question": {"type": "binary", "instruction": q[0].upper() + q[1:] + "?"},
                "target": bool(r["answer"]), "hard_cases": []})
random.Random(7).shuffle(out)
for ex in out[:max(SIZES)]:
    validate_example(ex)
for n in SIZES:
    write_jsonl(f"data/curve/boolq_{n}.jsonl", out[:n])
print(f"{len(rows)} train rows, {len(rows) - len(out)} dropped for passage overlap; wrote {SIZES} to data/curve/; "
      f"positives in the 3000: {sum(e['target'] for e in out[:3000])}")
