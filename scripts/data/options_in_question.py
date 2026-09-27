""" "All options at once" for the tree scorer, as a data transform: every candidate is listed in the question text,
so each leaf still judges one candidate but now sees all the alternatives (one vs all, in context). The tree
code, format and readout are unchanged, and every row keeps its id, split and target.

Options are listed in a fixed random order per question (seeded by id), so list position carries no signal.
Binary questions are unchanged. `selfjev finetune` and `selfjev serve` apply the same transform themselves; this script
builds the evaluation copies that `selfjev eval` reads (data/ova/eval2, eval_llm, hf, eval).

usage: uv run python scripts/data/options_in_question.py data/eval2.jsonl ...   -> data/ova/<name>.jsonl
"""

import json
import sys
from pathlib import Path

from selfjev.core.options import with_options


def transform(row):
    return row | {"question": with_options(row["question"], row["id"])}


if __name__ == "__main__":
    out = Path("data/ova")
    out.mkdir(exist_ok=True)
    for f in sys.argv[1:]:
        with open(f) as fh:
            rows = [transform(json.loads(line)) for line in fh]
        (out / Path(f).name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        print(f"{f} -> {out / Path(f).name}: {len(rows)} rows")
