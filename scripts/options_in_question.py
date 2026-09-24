""""All options at once" for the tree scorer, as a data transform: every candidate is listed in the question text,
so each leaf still judges one candidate but now sees all the alternatives (one vs all, in context). The tree
code, format and readout are unchanged, and every row keeps its id, split and target.

Options are listed in a fixed random order per question (seeded by id), so list position carries no signal.
Binary questions are unchanged. Apply the same transform at inference time (transform()).

usage: uv run python scripts/options_in_question.py data/hf.jsonl data/eval2.jsonl ...   -> data/ova/<name>.jsonl
"""
import hashlib
import json
import random
import sys
from pathlib import Path

HEAD = {"multiclass": "Options (exactly one is correct):", "multilabel": "Options (any number can be correct, possibly none):"}


def transform(row):
    q = row["question"]
    if q["type"] == "binary":
        return row
    opts = list(q["candidates"])
    random.Random(int(hashlib.sha256(row["id"].encode()).hexdigest()[:8], 16)).shuffle(opts)
    listing = "\n".join(f"- {c['description']}" for c in opts)
    return row | {"question": q | {"instruction": f"{q['instruction']}\n{HEAD[q['type']]}\n{listing}"}}


if __name__ == "__main__":
    out = Path("data/ova")
    out.mkdir(exist_ok=True)
    for f in sys.argv[1:]:
        rows = [transform(json.loads(line)) for line in open(f)]
        (out / Path(f).name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        print(f"{f} -> {out / Path(f).name}: {len(rows)} rows")
