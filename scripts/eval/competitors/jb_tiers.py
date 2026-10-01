"""Per-tier accuracy / macro / ECE from a JevBench results.jsonl (run from the jevbench checkout, PYTHONPATH=.).
usage: python jb_tiers.py RESULTS.jsonl"""

import json
import sys
from pathlib import Path

from jevbench.summarize import summarize
from jevbench.tasks import load_jsonl

recs = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
tiers = {t: load_jsonl(f"datasets/public/{t}.jsonl") for t in ("easy", "original", "hard")}
for name, tasks in [*tiers.items(), ("ALL231", [t for ts in tiers.values() for t in ts])]:
    ids = {t.id for t in tasks}
    s = summarize(tasks, [r for r in recs if r["task_id"] in ids])
    print(f"{name:9} n={s['n_attempted']}/{s['n_planned']} acc={s['accuracy']:.4f} macro_family_acc={s['macro_accuracy']:.4f} "
          f"ece={s['ece']['ece']:.4f} brier={s['brier_mean']:.4f}")  # fmt: skip
