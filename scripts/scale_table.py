"""Model-size comparison on the identical test questions: Qwen3-Reranker 0.6B / 4B / 8B (unmodified and LoRA
fine-tuned) next to Jev and GPT-6 Astra. Every number comes from a report file.

usage: uv run python scripts/scale_table.py > reports/scale_comparison.md
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLS = {  # label -> test report (all on hf.jsonl + eval.jsonl test, 3,471 questions)
    "0.6B": "baseline/test", "0.6B + LoRA": "lora_pilot/test",
    "4B": "baseline_4b/test", "4B + LoRA": "lora_4b/test",
    "8B": "baseline_8b/test", "8B + LoRA": "lora_8b/test",
    "Jev": "external/full/typesafe_jev-latest", "GPT-6 Astra": "external/full/openai_gpt-6-astra",
}
R = {k: json.loads((ROOT / "reports" / v / "report.json").read_text()) for k, v in COLS.items() if (ROOT / "reports" / v / "report.json").exists()}
ids = set.intersection(*({p["id"] for p in r["predictions"]} for r in R.values()))
assert all(len(r["predictions"]) == len(ids) for r in R.values()), "reports cover different questions"
LOWER = ("ece", "brier", "log_loss")
ROWS = [("question accuracy %", ("question_accuracy",), True), ("binary accuracy %", ("binary", "accuracy"), True),
        ("binary F1 %", ("binary", "f1"), True), ("binary AUROC", ("binary", "auroc"), False),
        ("multiclass accuracy %", ("multiclass", "accuracy"), True), ("multiclass macro-F1 %", ("multiclass", "macro_f1"), True),
        ("multilabel exact match %", ("multilabel", "exact_match"), True), ("multilabel micro-F1 %", ("multilabel", "micro_f1"), True),
        ("multilabel label AUROC", ("multilabel", "label_auroc"), False), ("binary ECE", ("binary", "ece"), False),
        ("binary Brier", ("binary", "brier"), False), ("multiclass ECE (top-label)", ("multiclass", "ece_top_label"), False)]


def get(m, path):
    for k in path:
        m = m.get(k) if isinstance(m, dict) else None
    return m


def fmt(v, pct):
    return "—" if v is None else f"{100 * v:.1f}" if pct else f"{v:.3f}"


def mcnemar(a, b):
    oa, ob = sum(a[i] and not b[i] for i in a), sum(b[i] and not a[i] for i in a)
    n, k = oa + ob, min(oa, ob)
    return oa, ob, (min(1.0, 2 * sum(math.comb(n, j) for j in range(k + 1)) / 2 ** n) if n else 1.0)


cols = list(R)
out = [f"**Test split: {len(ids)} identical questions** (`hf.jsonl` test + `eval.jsonl` test). Qwen rows are "
       "Qwen3-Reranker checkpoints; \"+ LoRA\" = the same frozen checkpoint plus our rank-16 adapter on q/k/v/o.", "",
       "| | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
for label, path, pct in ROWS:
    vals = [get(R[c]["metrics"], path) for c in cols]
    real = [v for v in vals if v is not None]
    best = (min if path[-1].startswith(LOWER) else max)(real) if real else None
    out.append(f"| {label} | " + " | ".join(f"**{fmt(v, pct)}**" if v is not None and v == best else fmt(v, pct) for v in vals) + " |")
out.append("| dtype / prompt | " + " | ".join(
    f"{R[c]['meta'].get('dtype', '-')} / {R[c]['meta'].get('prompt', '-')}" if not c.startswith(("Jev", "GPT")) else "API" for c in cols) + " |")
print("\n".join(out) + "\n")

correct = {c: {p["id"]: p["correct"] for p in R[c]["predictions"]} for c in cols}
lines = ["**Paired exact McNemar** (questions only one side gets right)", "", "| comparison | left only | right only | p |", "|---|---|---|---|"]
pairs = [(a, b) for a, b in (("0.6B", "0.6B + LoRA"), ("4B", "4B + LoRA"), ("8B", "8B + LoRA"), ("0.6B + LoRA", "4B + LoRA"),
                             ("4B + LoRA", "8B + LoRA"), ("8B + LoRA", "Jev"), ("8B + LoRA", "GPT-6 Astra")) if a in R and b in R]
for a, b in pairs:
    oa, ob, p = mcnemar(correct[a], correct[b])
    lines.append(f"| {a} vs {b} | {oa} | {ob} | {p:.2g} |")
print("\n".join(lines) + "\n")

fams = sorted(R[cols[0]]["by_family"])
lines = ["**Question accuracy % by family**", "", "| family | n | " + " | ".join(cols) + " |", "|---|---|" + "---|" * len(cols)]
for f in fams:
    n = sum(get(R[cols[0]]["by_family"][f], (t, "n")) or 0 for t in ("binary", "multiclass", "multilabel"))
    lines.append(f"| {f} | {n} | " + " | ".join(fmt(get(R[c]["by_family"].get(f, {}), ("question_accuracy",)), True) for c in cols) + " |")
print("\n".join(lines) + "\n")

tags = [t for t, v in sorted(R[cols[0]]["by_hard_case"].items()) if v["n"] >= 10]
lines = ["**Question accuracy % by hard-case tag (n >= 10)**", "", "| tag | n | " + " | ".join(cols) + " |", "|---|---|" + "---|" * len(cols)]
for t in tags:
    lines.append(f"| {t} | {R[cols[0]]['by_hard_case'][t]['n']} | "
                 + " | ".join(fmt(R[c]["by_hard_case"].get(t, {}).get("question_accuracy"), True) for c in cols) + " |")
print("\n".join(lines))
