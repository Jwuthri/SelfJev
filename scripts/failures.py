"""Where our LoRA model fails, next to Jev and GPT-6 Astra (full test set).

Writes reports/external/failures.jsonl (every test question LoRA gets wrong, worst first) and
reports/external/failures.md (failure rates by family / hard-case tag and the biggest gaps).

These are TEST questions: use them to understand errors and to steer NEW training data. Training on them would
turn the test set into training data and invalidate every number measured on it.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "reports/external"


def preds(path):
    return {r["id"]: r for r in json.loads(Path(path).read_text())["predictions"]}


lora, base = preds(EXT / "full/ours-LoRA/report.json"), preds(EXT / "full/ours-base/report.json")
jev = preds(EXT / "full/typesafe_jev-latest/report.json")
astra = preds(EXT / "full/openai_gpt-6-astra/report.json")
examples = {json.loads(line)["id"]: json.loads(line) for line in open(EXT / "full/subset.jsonl")}


def answer(r):
    if r is None:
        return None
    if r["type"] == "binary":
        return {"selected": r["selected"], "p_yes": round(r["p_yes"], 4), "correct": r["correct"]}
    return {"selected": r["selected"], "correct": r["correct"],
            "probabilities": {c: round(p, 4) for c, p in zip(r["candidate_ids"], r["probabilities"])}}


def wrong_confidence(r):
    """How confident LoRA was in its wrong answer: prob. of the chosen wrong option (binary: of the wrong side)."""
    if r["type"] == "binary":
        return r["p_yes"] if r["selected"] else 1 - r["p_yes"]
    if r["type"] == "multiclass":
        return max(r["probabilities"])
    ps = dict(zip(r["candidate_ids"], r["probabilities"]))  # multilabel: worst single label error
    return max(ps[c] if c not in r["target"] else 1 - ps[c] for c in r["candidate_ids"])


rows = []
for i, r in lora.items():
    if r["correct"]:
        continue
    ex = examples[i]
    rows.append({"id": i, "family": r["family"], "type": r["type"], "hard_cases": r["hard_cases"],
                 "gap": "jev_right" if jev[i]["correct"] else "jev_also_wrong", "lora_wrong_confidence": round(wrong_confidence(r), 4),
                 "question": ex["question"], "target": ex["target"], "state": ex["state"],
                 "lora": answer(r), "base": answer(base[i]), "jev": answer(jev[i]), "gpt6_astra": answer(astra.get(i))})
rows.sort(key=lambda x: (x["gap"] != "jev_right", -x["lora_wrong_confidence"]))
with open(EXT / "failures.jsonl", "w") as f:
    for x in rows:
        f.write(json.dumps(x, ensure_ascii=False) + "\n")


def table(key, title, min_n=10):
    g = defaultdict(lambda: [0, 0, 0, 0])  # n, lora wrong, jev wrong, lora wrong & jev right
    for i, r in lora.items():
        for k in key(r):
            g[k][0] += 1
            g[k][1] += not r["correct"]
            g[k][2] += not jev[i]["correct"]
            g[k][3] += (not r["correct"]) and jev[i]["correct"]
    out = [f"## {title}", "", "| slice | n | LoRA error % | Jev error % | gap (pp) | LoRA wrong & Jev right |", "|---|---|---|---|---|---|"]
    for k, (n, lw, jw, lj) in sorted(g.items(), key=lambda kv: -(kv[1][1] - kv[1][2]) / kv[1][0]):
        if n >= min_n:
            out.append(f"| {k} | {n} | {100 * lw / n:.1f} | {100 * jw / n:.1f} | {100 * (lw - jw) / n:+.1f} | {lj} |")
    return out


both = sum(1 for x in rows if x["gap"] == "jev_also_wrong")
ours_only = sum(1 for i, r in lora.items() if r["correct"] and not jev[i]["correct"])
lines = ["# Where LoRA fails (full test set, n = %d)" % len(lora), "",
         "TEST questions: use for analysis and to steer new training data only; never train on them.", "",
         f"- LoRA wrong: {len(rows)} ({len(rows) - both} where Jev is right, {both} where Jev is also wrong)",
         f"- LoRA right and Jev wrong: {ours_only}",
         f"- Full list, worst first (Jev-right cases, then by LoRA's confidence in its wrong answer): `reports/external/failures.jsonl`", ""]
lines += table(lambda r: [r["family"]], "Error rate by family (sorted by LoRA - Jev gap)", 1) + [""]
lines += table(lambda r: r["hard_cases"] or ["(none)"], "Error rate by hard-case tag (n >= 10)") + [""]
lines += table(lambda r: [r["type"]], "Error rate by question type", 1) + [""]
(EXT / "failures.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
