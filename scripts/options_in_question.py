""""All options at once" for the tree scorer, as a data transform: every candidate is listed in the question text,
so each leaf still judges one candidate but now sees all the alternatives (one vs all, in context). The tree
code, format and readout are unchanged, and every row keeps its id, split and target.

Options are listed in a fixed random order per question (seeded by id), so list position carries no signal.
Binary questions are unchanged. Apply the same transform at inference time (transform()).

usage: uv run python scripts/options_in_question.py data/hf.jsonl data/eval2.jsonl ...   -> data/ova/<name>.jsonl
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from personal_jev.options import with_options  # noqa: E402


def transform(row):
    return row | {"question": with_options(row["question"], row["id"])}


if __name__ == "__main__":
    out = Path("data/ova")
    out.mkdir(exist_ok=True)
    for f in sys.argv[1:]:
        rows = [transform(json.loads(line)) for line in open(f)]
        (out / Path(f).name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        print(f"{f} -> {out / Path(f).name}: {len(rows)} rows")
