"""Print the README result tables straight from report files (no hand-copied numbers).

usage: uv run python scripts/summarize.py > reports/summary.md
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = {"base": "baseline/test", "base+cal": "baseline/test_calibrated", "LoRA": "lora_pilot/test", "LoRA+cal": "lora_pilot/test_calibrated",
        # custom shared-state model (spec version, frozen) and the similarity variant with joint LoRA, once their reports exist
        "custom": "custom_frozen/test", "custom-sim-LoRA": "custom_sim_lora/test", "custom-sim-LoRA+cal": "custom_sim_lora/test_calibrated"}
R = {k: json.loads((ROOT / "reports" / v / "report.json").read_text()) for k, v in RUNS.items()
     if (ROOT / "reports" / v / "report.json").exists()}


def g(m, *path):
    for k in path:
        m = m.get(k) if isinstance(m, dict) else None
    return m


def f(x, pct):
    return "—" if x is None else f"{100 * x:.1f}" if pct else f"{x:.3f}"


def table(title, rows, cols, source):
    out = [f"**{title}**", "", "| | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    for label, path, pct in rows:
        out.append(f"| {label} | " + " | ".join(f(g(source(c), *path), pct) for c in cols) + " |")
    return "\n".join(out) + "\n"


QUALITY = [("question accuracy %", ("question_accuracy",), True), ("binary accuracy %", ("binary", "accuracy"), True),
           ("binary F1 %", ("binary", "f1"), True), ("binary AUROC", ("binary", "auroc"), False),
           ("multiclass accuracy %", ("multiclass", "accuracy"), True), ("multiclass macro-F1 %", ("multiclass", "macro_f1"), True),
           ("multilabel exact match %", ("multilabel", "exact_match"), True), ("multilabel micro-F1 %", ("multilabel", "micro_f1"), True),
           ("multilabel label AUROC", ("multilabel", "label_auroc"), False)]
CALIB = [(f"{t} {k}", (t, k), False) for t in ("binary", "multiclass", "multilabel")
         for k in (("ece_top_label" if t == "multiclass" else "ece"), "brier", "log_loss")]

print(table(f"Test split, n = {R['base']['meta']['n']} questions (hf.jsonl test + eval.jsonl test)", QUALITY, list(R), lambda c: R[c]["metrics"]))
print(table("Calibration on the test split (lower is better)", CALIB, list(R), lambda c: R[c]["metrics"]))

fams = sorted(R["base"]["by_family"])
lines = ["**Question accuracy % by family (test)**", "", "| family | n | " + " | ".join(R) + " |", "|---|---|" + "---|" * len(R)]
for fam in fams:
    n = sum(g(R["base"]["by_family"][fam], t, "n") or 0 for t in ("binary", "multiclass", "multilabel"))
    lines.append(f"| {fam} | {n} | " + " | ".join(f(g(R[c]['by_family'].get(fam, {}), 'question_accuracy'), True) for c in R) + " |")
print("\n".join(lines) + "\n")

tags = [t for t, v in sorted(R["base"]["by_hard_case"].items()) if v["n"] >= 10]
lines = ["**Question accuracy % by hard-case tag (test, tags with n >= 10)**", "", "| tag | n | " + " | ".join(R) + " |", "|---|---|" + "---|" * len(R)]
for t in tags:
    lines.append(f"| {t} | {R['base']['by_hard_case'][t]['n']} | " + " | ".join(f(R[c]['by_hard_case'].get(t, {}).get('question_accuracy'), True) for c in R) + " |")
print("\n".join(lines) + "\n")

pg = {c: R[c]["paraphrase_groups"] for c in R}
print(f"**Paraphrase groups** ({pg['base']['groups']} groups, same state with reworded question or candidates): "
      + "; ".join(f"{c}: same prediction {f(v['same_prediction'], True)}%, all correct {f(v['all_correct'], True)}%" for c, v in pg.items()) + "\n")


def mcnemar(a, b):
    """Exact two-sided McNemar p-value on paired question-level correctness (a, b: {id: correct})."""
    ids = a.keys() & b.keys()
    only_a, only_b = sum(a[i] and not b[i] for i in ids), sum(b[i] and not a[i] for i in ids)
    n, k = only_a + only_b, min(only_a, only_b)
    p = min(1.0, 2 * sum(math.comb(n, j) for j in range(k + 1)) / 2 ** n) if n else 1.0
    return only_a, only_b, p


correct = {c: {r["id"]: r["correct"] for r in R[c]["predictions"]} for c in R}
fam_of = {r["id"]: r["family"] for r in R["base"]["predictions"]}
for x, y in [("base", "LoRA"), ("LoRA", "custom-sim-LoRA"), ("custom", "custom-sim-LoRA")]:
    if x not in R or y not in R:
        continue
    lines = [f"**Paired test, {x} vs {y} (uncalibrated): questions only one of them gets right; exact McNemar p**", "",
             f"| slice | n | {x} only | {y} only | p |", "|---|---|---|---|---|"]
    for name, keep in [("all test questions", lambda i: True)] + [(f, (lambda f: lambda i: fam_of[i] == f)(f)) for f in fams]:
        a = {i: v for i, v in correct[x].items() if keep(i)}
        b = {i: v for i, v in correct[y].items() if keep(i)}
        oa, ob, p = mcnemar(a, b)
        lines.append(f"| {name} | {len(a)} | {oa} | {ob} | {p:.2g} |")
    print("\n".join(lines) + "\n")
