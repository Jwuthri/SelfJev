"""data/eval2.jsonl: the frozen TEST-ONLY target-task set, from data/eval2/raw/*.jsonl and two blind judges.

  uv run python scripts/build_eval2.py

- Keeps a question only if the authored target equals BOTH judges' answers (data/eval2/review/answers_astra.jsonl and
  answers_<second>.jsonl). Jev answers (jev_answers.jsonl) are reported, never used to keep or drop.
- Drops any state whose word 8-gram containment with a state of hf.jsonl, synthetic.jsonl, eval.jsonl or
  hardcases.jsonl is >= 0.3 (any split: eval2 must be new text).
- Writes EXPANDED rows (one question per line, split=test) so ids stay the raw "<source_id>-q<i>" and join the judge
  files in data/eval2/review/ (source-format lines would renumber ids after a drop). Also data/eval2/REVIEW.md
  (agreement, composition, Jev accuracy, sha256 of the frozen file) and data/eval2/review/SPOTCHECK.md (50 random
  questions for a human check).
"""
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from personal_jev.data import expand_source, read_jsonl, sha256_file, write_jsonl  # noqa: E402

RAW, REVIEW, OUT = ROOT / "data/eval2/raw", ROOT / "data/eval2/review", ROOT / "data/eval2.jsonl"
TRAIN_FILES = ["data/hf.jsonl", "data/synthetic.jsonl", "data/eval.jsonl", "data/hardcases.jsonl"]


def shingles(text, n=8):
    w = re.findall(r"\w+", text.lower())
    return {" ".join(w[i:i + n]) for i in range(max(1, len(w) - n + 1))}


def norm(t):
    return sorted(t) if isinstance(t, list) else t


def pct(a, b):
    return f"{100 * a / b:.1f}" if b else "—"


def table(title, rows, cols):
    lines = [f"### {title}", "", "| " + " | ".join([title] + cols) + " |", "|" + "---|" * (len(cols) + 1)]
    lines += [f"| {k} | " + " | ".join(str(v) for v in vals) + " |" for k, vals in rows]
    return lines + [""]


def main():
    judges = {f.stem.replace("answers_", ""): {r["id"]: r for r in read_jsonl(f)} for f in sorted(REVIEW.glob("answers_*.jsonl"))}
    if len(judges) < 2:
        sys.exit(f"need two judges in {REVIEW}, found {list(judges)}")
    jev = {r["id"]: r for r in read_jsonl(REVIEW / "jev_answers.jsonl")} if (REVIEW / "jev_answers.jsonl").exists() else {}
    print("judges:", {k: len(v) for k, v in judges.items()}, "jev:", len(jev))

    # leakage index: every 8-gram of every state in the training/eval files
    index = defaultdict(set)
    for f in TRAIN_FILES:
        for k, st in enumerate({e["state"] for e in read_jsonl(ROOT / f)}):
            for sh in shingles(st):
                index[sh].add((f, k))
    leak_sizes = {}
    for f in TRAIN_FILES:
        for k, st in enumerate({e["state"] for e in read_jsonl(ROOT / f)}):
            leak_sizes[(f, k)] = len(shingles(st))

    srcs, stats, leaked, kept_srcs, kept, spot = [], defaultdict(Counter), [], [], [], []
    seen = set()
    for f in sorted(RAW.glob("*.jsonl")):
        for src in read_jsonl(f):
            if src["source_id"] in seen:
                raise ValueError(f"duplicate source_id {src['source_id']}")
            seen.add(src["source_id"])
            srcs.append(src)
    for src in srcs:
        sh = shingles(src["state"])
        hits = Counter(ref for g in sh for ref in index.get(g, ()))
        if any(n / min(len(sh), leak_sizes[ref]) >= 0.3 for ref, n in hits.items()):
            leaked.append(src["source_id"])
            continue
        exs, keep_q = expand_source(src), []
        for i, ex in enumerate(exs):
            answers = [j.get(ex["id"]) for j in judges.values()]
            key = ex["family"]
            if any(a is None for a in answers):
                stats[key]["unanswered"] += 1
                continue
            agree = [norm(a["answer"]) == norm(ex["target"]) for a in answers]
            stats[key]["judged"] += 1
            for name, ok in zip(judges, agree):
                stats[key][f"agree_{name}"] += ok
            if all(agree):
                stats[key]["kept"] += 1
                keep_q.append(ex | {"split": "test"})
                spot.append((src, ex, [a["answer"] for a in answers]))
            else:
                stats[key]["dropped"] += 1
        if keep_q:
            kept_srcs.append(src)
            kept.extend(keep_q)
    write_jsonl(OUT, kept)
    digest = sha256_file(OUT)
    # ids a source-format export would have given (position among kept questions) -> real ids, for older reports
    pos = Counter()
    id_map = {}
    for e in kept:
        id_map[f"{e['source_id']}-q{pos[e['source_id']]}"] = e["id"]
        pos[e["source_id"]] += 1
    (REVIEW / "id_map_sourceformat_to_real.json").write_text(json.dumps(id_map, indent=0))

    # composition + Jev accuracy on the kept set
    def bucket(e):
        m = re.search(r"len=(\d+)", e["provenance"])
        return int(m.group(1)) if m else 0
    def comp(keyf):
        c = defaultdict(Counter)
        for e in kept:
            for k in keyf(e):
                c[k]["n"] += 1
                if e["id"] in jev:
                    c[k]["jev_n"] += 1
                    c[k]["jev_ok"] += norm(jev[e["id"]]["answer"]) == norm(e["target"])
        return [(k, [v["n"], pct(v["jev_ok"], v["jev_n"])]) for k, v in sorted(c.items(), key=lambda kv: str(kv[0]))]
    author = lambda e: e["provenance"].split(" (")[0].replace("synthetic:openrouter/", "")
    lines = ["# eval2: frozen target-task test set", "",
             f"`data/eval2.jsonl` sha256 `{digest}` — {len(kept)} questions / {len(kept_srcs)} states, every row split=test. "
             "**Frozen: never train, select prompts, fit thresholds or temperatures on it.** Authors: "
             + ", ".join(sorted({author(e) for e in kept})) + f". Judges (blind, both must agree with the author): {', '.join(judges)}. "
             "Jev is reported, never used to keep or drop. LLM-verified; human spot-check list in review/SPOTCHECK.md. "
             "Rows are expanded (one question per line) so ids are the raw `<source_id>-q<i>` and join `review/answers_*.jsonl`; "
             "a first export on 2026-09-24 used source-format lines whose ids were renumbered after drops (sha `f18549eb…`): "
             "`review/id_map_sourceformat_to_real.json` maps those ids to the real ones, and the 95.2% Jev figure computed on "
             "that misalignment was wrong.", "",
             f"States dropped for 8-gram overlap ≥ 0.3 with training/eval files: {len(leaked)} {leaked[:10]}", "",
             "## Agreement (before the keep rule)", "", "| family | judged | " + " | ".join(f"author = {j} %" for j in judges) + " | kept (unanimous) | dropped | unanswered |",
             "|---|---|" + "---|" * len(judges) + "---|---|---|"]
    tot = Counter()
    for fam, c in sorted(stats.items()):
        tot.update(c)
        lines.append(f"| {fam} | {c['judged']} | " + " | ".join(pct(c[f'agree_{j}'], c['judged']) for j in judges) + f" | {c['kept']} | {c['dropped']} | {c['unanswered']} |")
    lines.append(f"| **all** | {tot['judged']} | " + " | ".join(pct(tot[f'agree_{j}'], tot['judged']) for j in judges) + f" | {tot['kept']} | {tot['dropped']} | {tot['unanswered']} |")
    lines += ["", "## Composition of the kept set, with Jev accuracy on it", ""]
    lines += table("tier (family)", comp(lambda e: [e["family"]]), ["n", "Jev acc %"])
    lines += table("author", comp(lambda e: [author(e)]), ["n", "Jev acc %"])
    lines += table("type", comp(lambda e: [e["question"]["type"]]), ["n", "Jev acc %"])
    lines += table("length bucket (tokens)", comp(lambda e: [bucket(e)]), ["n", "Jev acc %"])
    lines += table("hard case (all tags)", comp(lambda e: e["hard_cases"] or ["(none)"]), ["n", "Jev acc %"])
    ml = Counter(len(e["target"]) for e in kept if e["question"]["type"] == "multilabel")
    none_q = [e for e in kept if e["question"]["type"] == "multiclass" and any(c["id"] == "none" or c["description"].lower().startswith("none") for c in e["question"]["candidates"])]
    none_ok = sum(e["target"] == "none" or any(c["id"] == e["target"] and c["description"].lower().startswith("none") for c in e["question"]["candidates"]) for e in none_q)
    lines += [f"Multilabel positives: {dict(sorted(ml.items()))}. Multiclass questions offering a none candidate: {len(none_q)}, none correct in {none_ok} ({pct(none_ok, len(none_q))}%).", ""]
    (ROOT / "data/eval2/REVIEW.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:4 + len(stats) + 8]))

    rng = random.Random(2)
    rows = ["# eval2 spot-check: 50 random kept questions (human review)", "",
            "Mark each as OK / wrong / ambiguous. The model never sees notes, tags or ids.", ""]
    for src, ex, answers in rng.sample(spot, min(50, len(spot))):
        q = ex["question"]
        st = src["state"] if len(src["state"]) <= 2500 else src["state"][:2500] + " […truncated for display]"
        rows += [f"## {ex['id']} — {ex['family']}, {author(ex)}, tags {ex['hard_cases']}", "", "```text", st, "```", "",
                 f"**{q['type']}**: {q['instruction']}", ""]
        rows += [f"- `{c['id']}`: {c['description']}" for c in q.get("candidates", [])]
        rows += ["", f"**Target** `{json.dumps(ex['target'])}` (judges: {', '.join(json.dumps(a) for a in answers)}). Author's note: {ex.get('notes', '')}", "", "Verdict: ☐ OK ☐ wrong ☐ ambiguous", ""]
    (REVIEW / "SPOTCHECK.md").write_text("\n".join(rows) + "\n")
    print(f"wrote {OUT} ({len(kept)} questions, sha256 {digest[:12]}…), data/eval2/REVIEW.md, {REVIEW / 'SPOTCHECK.md'}")


if __name__ == "__main__":
    main()
