"""Lower how often "none of the above" is the right answer in hard-case TRAINING questions.

Round 2 (tree_4b_r2) over-selected "none" on held-out CLINC (in-scope requests routed to none: 16 -> 50 of 255):
in data/hardcases.jsonl, multiclass training questions that offer a none-candidate have "none" as the answer 23% of
the time, vs 8% in round 1's synthetic data. This drops a seeded random subset of those none-answer TRAIN questions
until the rate is --rate (default 0.10). Validation and all other questions are untouched.
Caveat: this fix was motivated by a test-set diagnosis, so the retrained model's CLINC score is no longer a clean
held-out number.

usage: uv run python scripts/rebalance_nota.py [--rate 0.10] -> data/hardcases_nb.jsonl
"""
import argparse
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from personal_jev.data import read_jsonl, write_jsonl  # noqa: E402


def none_ids(ex):
    q = ex["question"]
    return [c["id"] for c in q.get("candidates", []) if c["id"] == "none" or c["id"].startswith("none")] if q["type"] == "multiclass" else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rate", type=float, default=0.10)
    ap.add_argument("--seed", type=int, default=13)
    a = ap.parse_args()
    ex = read_jsonl(ROOT / "data/hardcases.jsonl")
    offer = [e for e in ex if e["split"] == "train" and none_ids(e)]
    none_ans = [e for e in offer if e["target"] in none_ids(e)]
    keep_n = round(a.rate * (len(offer) - len(none_ans)) / (1 - a.rate))
    drop = {e["id"] for e in random.Random(a.seed).sample(none_ans, max(0, len(none_ans) - keep_n))}
    out = [e for e in ex if e["id"] not in drop]
    write_jsonl(ROOT / "data/hardcases_nb.jsonl", out)
    print(f"train questions offering none: {len(offer)}; answer none: {len(none_ans)} ({100 * len(none_ans) / len(offer):.0f}%) "
          f"-> kept {keep_n} ({100 * keep_n / (len(offer) - len(drop)):.0f}%); dropped {len(drop)}; wrote {len(out)} questions")


if __name__ == "__main__":
    main()
