"""The mix for continuing selfjev-4b-vision on the 2026-10-01 batches (planted wrong verdicts, JSON records, typed-decisions train).

- New: every train-split row of the NEW batches in runs/jev_all/train.jsonl.gz (verified targets + Jev's soft targets).
- Text replay: as many rows again, drawn (seed 0) from the other training datasets of runs/jev_all, keeping a third of the
  texts over 4K tokens (they are ~95 % of a step's compute; JOURNAL 2026-09-30 10:40), so old skills are not forgotten.
- Image replay: IMAGES rows from data/images_v1/train.jsonl (the images v1 training photos), so vision is not forgotten.
- Val: the usual 1,200 text questions (runs/jev_all/val), the images v1 validation photos, the new batches' validation split.

usage (after grow_batch.sh <name> finish for both batches):
  uv run python scripts/train/jev_soft_targets.py && uv run python scripts/data/build_verdict_mix.py
writes runs/verdict_json_v1/{train,val}.jsonl.gz for `selfjev finetune --init weights/selfjev_4b_vision`.
Other mixes: `build_verdict_mix.py OUT_NAME BATCH...`, e.g. `verdict_json_only_v1 verdict_json_v1` (no typed-decisions import).
"""

import gzip
import json
import random
import sys
from pathlib import Path

NEW = set(sys.argv[2:]) or {"verdict_json_v1", "typed_decisions_train_v1"}
IMAGES = 3000
OUT = Path("runs") / (sys.argv[1] if len(sys.argv) > 1 else "verdict_json_v1")


def read(path):
    with (gzip.open if str(path).endswith(".gz") else open)(path, "rt") as f:
        return [json.loads(line) for line in f]


def write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def main():
    rnd = random.Random(0)
    text = read("runs/jev_all/train.jsonl.gz")
    new = [r for r in text if r.get("dataset") in NEW and r.get("split") == "train"]
    new_val = [r for r in text if r.get("dataset") in NEW and r.get("split") == "validation"]
    old = [r for r in text if r.get("dataset") not in NEW and (len(r["state"]) <= 4096 * 3.6 or rnd.random() < 1 / 3)]
    replay = rnd.sample(old, len(new))
    images = rnd.sample(read("data/images_v1/train.jsonl"), IMAGES)
    mix = new + replay + images
    rnd.shuffle(mix)
    write(OUT / "train.jsonl.gz", mix)
    write(OUT / "val.jsonl.gz", read("runs/jev_all/val.jsonl.gz") + read("data/images_v1/val.jsonl") + new_val)
    by = {d: sum(r.get("dataset") == d for r in new) for d in sorted(NEW)}
    print(f"train {len(mix)}: new {len(new)} {by} + text replay {len(replay)} + images {len(images)}; new val {len(new_val)}")


if __name__ == "__main__":
    main()
