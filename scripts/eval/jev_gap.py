"""Where the default loses to Jev on eval2, at the category level only (tier, type, trap, length; confident mistakes;
accuracy at matched coverage). A test-set diagnosis: label any change it motivates as such (AGENTS.md).

usage: uv run python scripts/eval/jev_gap.py [reports/<run>/eval2/report.json]  -> reports/audit_2026-09-30/jev_gap.md
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

from selfjev.evaluation.stats import mcnemar

ours_path = Path(sys.argv[1] if len(sys.argv) > 1 else "reports/images_v1/eval2/report.json")
OURS = {p["id"]: p for p in json.loads(ours_path.read_text())["predictions"]}
JEV = {p["id"]: p for p in json.loads(Path("reports/external/eval2/typesafe_jev-latest/report.json").read_text())["predictions"]}
rows = {r["id"]: r for r in map(json.loads, Path("data/eval2.jsonl").read_text().splitlines())}
ids = sorted(set(OURS) & set(JEV))


def conf(p):  # the model's probability of what it selected (binary: of its yes/no)
    if p["type"] == "binary":
        return max(p["p_yes"], 1 - p["p_yes"])
    if p["type"] == "multiclass":
        return max(p["probabilities"])
    return min(max(x, 1 - x) for x in p["probabilities"])  # multilabel: its least sure option


def line(name, sel):
    if not sel:
        return None
    o, j = sum(OURS[i]["correct"] for i in sel), sum(JEV[i]["correct"] for i in sel)
    a, b, p = mcnemar({i: OURS[i]["correct"] for i in sel}, {i: JEV[i]["correct"] for i in sel})
    return (b - a, f"| {name} | {len(sel)} | {100 * o / len(sel):.1f} | {100 * j / len(sel):.1f} | {a} / {b} | {p:.2g} |")


slices = defaultdict(list)
for i in ids:
    r = rows[i]
    slices[f"type: {r['question']['type']}"].append(i)
    slices[f"tier: {r['family'][3:]}"].append(i)
    for h in r.get("hard_cases", []):
        slices[f"trap: {h}"].append(i)
    if not r.get("hard_cases"):
        slices["trap: none"].append(i)
out = ["# Where selfjev loses to Jev on eval2 (category level)", "",
       f"Ours: `{ours_path}`; Jev: `reports/external/eval2/typesafe_jev-latest`. A test-set diagnosis: never train on items.", "",
       "| slice | n | ours | Jev | only ours / only Jev | p |", "|---|---|---|---|---|---|"]  # fmt: skip
out.append(line("all", ids)[1])
for _, s in sorted(filter(None, (line(k, v) for k, v in slices.items())), key=lambda x: -x[0]):
    out.append(s)
n = len(ids)
cw = {m: sum(P[i]["correct"] is False and conf(P[i]) >= 0.9 for i in ids) for m, P in (("ours", OURS), ("Jev", JEV))}
out += ["", f"Confident mistakes (wrong at >= 0.9): ours {cw['ours']}, Jev {cw['Jev']}.", "",
        "Accuracy on the questions each model is most sure about (same coverage):", "",
        "| coverage | ours | Jev |", "|---|---|---|"]  # fmt: skip
for cov in (0.5, 0.8, 0.9, 0.95, 1.0):
    k = int(cov * n)
    acc = {m: 100 * sum(P[i]["correct"] for i in sorted(ids, key=lambda i: -conf(P[i]))[:k]) / k for m, P in (("ours", OURS), ("Jev", JEV))}
    out.append(f"| {cov:.0%} | {acc['ours']:.2f} | {acc['Jev']:.2f} |")
Path("reports/audit_2026-09-30").mkdir(parents=True, exist_ok=True)
Path("reports/audit_2026-09-30/jev_gap.md").write_text("\n".join(out) + "\n")
print("\n".join(out))
