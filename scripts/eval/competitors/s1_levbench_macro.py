"""Run the 13 Nimble public subsets ("S1Bench", lev's export) through levbench against any /v1/systemone server;
print per-subset accuracy and the macro. usage: python s1_levbench_macro.py BASE_URL MODEL TASKS_DIR [CONCURRENCY] [OUT_JSON]"""

import json
import sys
from pathlib import Path

from levbench import runner
from levbench.tasks import load_task_file

base, model, tasks = sys.argv[1], sys.argv[2], Path(sys.argv[3])
conc = int(sys.argv[4]) if len(sys.argv) > 4 else 8
out = sys.argv[5] if len(sys.argv) > 5 else "s1bench_results.json"
client, _ = runner.build_client("lev", model, base, 600.0)  # 'lev' backend = local server, no key, 600 s timeout
res = {}
for f in sorted(tasks.glob("*.json")):
    if f.name == "index.json":
        continue
    items, qs = load_task_file(f)
    rep = runner.run_eval(client, "lev", model, items, qs, concurrency=conc)
    c = rep.per_question["decision"]
    res[f.stem] = {"n": c.n, "correct": c.n_correct, "acc": round(c.accuracy, 4), "ece": round(c.ece, 4), "brier": round(c.mean_brier, 4),
                   "p50_s": round(rep.pct(0.5), 3), "served_by": sorted(rep.served_by)}  # fmt: skip
    print(f"{f.stem:22} n={c.n:4} acc={c.accuracy:.4f} ece={c.ece:.3f}", flush=True)
macro = sum(r["acc"] for r in res.values()) / len(res)
micro = sum(r["correct"] for r in res.values()) / sum(r["n"] for r in res.values())
print(f"MACRO({len(res)}) = {macro:.4f}   MICRO = {micro:.4f}")
Path(out).write_text(json.dumps({"subsets": res, "macro": macro, "micro": micro}, indent=1))
