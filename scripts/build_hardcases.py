"""Round-2 hard-case TRAINING data: data/hardcases/raw/*.jsonl -> data/hardcases.jsonl.

  uv run python scripts/build_hardcases.py --blind   # write target-free files for the blind verifiers
  uv run python scripts/build_hardcases.py           # build, keeping only questions the blind verifier agrees with

- Splits by source_id hash: train 0.9 / validation 0.1. There is no test split: the test set stays hf.jsonl +
  eval.jsonl test, untouched.
- Leakage guard: drops any state whose word 8-gram containment with an eval.jsonl state is >= 0.3.
- Verification: data/hardcases/review/answers_*.jsonl hold blind re-labels. A question is kept only if the blind
  answer equals the authored target. Without answers the build refuses (use --unverified to override).
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from personal_jev.data import expand_source, read_jsonl, split_for, write_jsonl  # noqa: E402

RAW, REVIEW = ROOT / "data/hardcases/raw", ROOT / "data/hardcases/review"
GROUPS = {"v1": ["hnum", "htmp"], "v2": ["hrol", "hinj"], "v3": ["hlng", "hmul"], "v4": ["hpol", "hpar"]}


def shingles(text, n=8):
    w = re.findall(r"\w+", text.lower())
    return {" ".join(w[i:i + n]) for i in range(max(1, len(w) - n + 1))}


def sources():
    out, seen = [], set()
    for f in sorted(RAW.glob("*.jsonl")):
        for src in read_jsonl(f):
            if src["source_id"] in seen:
                raise ValueError(f"duplicate source_id {src['source_id']} in {f}")
            seen.add(src["source_id"])
            out.append(src)
    return out


def write_blind(srcs):
    REVIEW.mkdir(parents=True, exist_ok=True)
    for g, prefixes in GROUPS.items():
        rows = [{"source_id": s["source_id"], "state": s["state"],
                 "questions": [{"id": e["id"], "type": e["question"]["type"], "instruction": e["question"]["instruction"],
                                **({"candidates": e["question"]["candidates"]} if "candidates" in e["question"] else {})}
                               for e in expand_source(s)]}
                for s in srcs if s["source_id"].split("-")[0] in prefixes]
        write_jsonl(REVIEW / f"blind_{g}.jsonl", rows)
        print(f"blind_{g}.jsonl: {len(rows)} states, {sum(len(r['questions']) for r in rows)} questions")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blind", action="store_true")
    ap.add_argument("--unverified", action="store_true", help="build without blind answers (not recommended)")
    a = ap.parse_args()
    srcs = sources()
    if a.blind:
        return write_blind(srcs)

    answers = {x["id"]: x for f in sorted(REVIEW.glob("answers_*.jsonl")) for x in read_jsonl(f)}
    if not answers and not a.unverified:
        sys.exit("no blind answers in data/hardcases/review/; run the verification pass or pass --unverified")
    eval_sh = [shingles(s) for s in {e["state"] for e in read_jsonl(ROOT / "data/eval.jsonl")}]
    norm = lambda t: sorted(t) if isinstance(t, list) else t
    kept, stats, leak = [], defaultdict(Counter), 0
    for s in srcs:
        sh = shingles(s["state"])
        if any(len(sh & e) / min(len(sh), len(e)) >= 0.3 for e in eval_sh if e):
            leak += 1
            continue
        for ex in expand_source(s | {"split": split_for(s["source_id"], {"train": 0.9, "validation": 0.1}, "hard-r2")}):
            fam = ex["family"]
            if answers:
                if ex["id"] not in answers:
                    stats[fam]["unanswered"] += 1
                    continue
                if norm(answers[ex["id"]]["answer"]) != norm(ex["target"]):
                    stats[fam]["disagreed"] += 1
                    continue
            stats[fam]["kept"] += 1
            kept.append(ex)
    write_jsonl(ROOT / "data/hardcases.jsonl", kept)
    total = Counter()
    lines = ["# Hard-case data review (round 2)", "",
             "Authored by Claude Sonnet ([BRIEF.md](../BRIEF.md)). Every question was re-labelled blind by Claude Opus, and only "
             "questions where both agree are kept. LLM-verified, not human-reviewed.", "",
             f"States dropped for overlap with eval.jsonl: {leak}", "",
             "| family | kept | disagreed (dropped) | unanswered (dropped) | agreement % |", "|---|---|---|---|---|"]
    for fam, c in sorted(stats.items()):
        total.update(c)
        judged = c["kept"] + c["disagreed"]
        lines.append(f"| {fam} | {c['kept']} | {c['disagreed']} | {c['unanswered']} | {100 * c['kept'] / judged:.1f} |" if judged else f"| {fam} | 0 | 0 | {c['unanswered']} | — |")
    judged = total["kept"] + total["disagreed"]
    lines.append(f"| **total** | {total['kept']} | {total['disagreed']} | {total['unanswered']} | {100 * total['kept'] / max(judged, 1):.1f} |")
    REVIEW.mkdir(parents=True, exist_ok=True)
    (REVIEW / "REVIEW.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("splits:", dict(Counter(e["split"] for e in kept)), "types:", dict(Counter(e["question"]["type"] for e in kept)))


if __name__ == "__main__":
    main()
