"""A random slice of selfjev-4b's own text training rows (runs/jev_all/train.jsonl.gz, Jev soft targets), keeping a share
of the texts over 4K tokens (they are 64% of the tokens; JOURNAL 2026-09-30 15:45). For quick paired experiments.

usage: uv run python scripts/train/sample_text_mix.py N LONG_FRAC OUT   e.g. 15000 0.333 runs/chain_pilot/train.jsonl.gz
"""

import gzip
import json
import random
import sys
from pathlib import Path

n, long_frac, out = int(sys.argv[1]), float(sys.argv[2]), Path(sys.argv[3])
rnd = random.Random(0)
with gzip.open("runs/jev_all/train.jsonl.gz", "rt") as f:
    rows = [r for line in f if len((r := json.loads(line))["state"]) <= 4096 * 3.6 or rnd.random() < long_frac]
out.parent.mkdir(parents=True, exist_ok=True)
with gzip.open(out, "wt") as f:
    f.writelines(json.dumps(r) + "\n" for r in rnd.sample(rows, n))
print(f"{n} of {len(rows)} rows -> {out}")
