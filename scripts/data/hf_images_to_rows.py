"""A Hugging Face image-classification dataset (an `image` column and a ClassLabel `label`) -> fine-tuning rows, one file
for `selfjev finetune --data` (or a fine-tuning upload after `selfjev.types.TrainingRow` conversion).

Per photo, two questions on the same state (the photo, a base64 JPEG data URL, longest side <= --side):
  - multiclass: the true class + (--options - 1) random distractors, listed in the question by the trainer;
  - binary: "is it <class>?", the true class (yes) or a random other class (no), alternating.
--per-class caps the photos per class; big datasets stream, so nothing is downloaded whole.

usage: uv run --group data python scripts/data/hf_images_to_rows.py timm/oxford-iiit-pet --split train --out data/pets_train.jsonl \
           --question "What breed is the pet in this photo?" --per-class 60
       (other datasets: docs/image_datasets.md)
"""

import argparse
import base64
import io
import json
import os
import random
from collections import Counter

from datasets import load_dataset


def data_url(img, side):
    img = img.convert("RGB")
    img.thumbnail((side, side))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("--split", default="train")
    ap.add_argument("--out", required=True)
    ap.add_argument("--question", default="What is in this photo?", help="the multiclass question; the binary one is 'Is it <class>?'")
    ap.add_argument("--image-col", default="image")
    ap.add_argument("--label-col", default="label")
    ap.add_argument("--per-class", type=int, default=50)
    ap.add_argument("--options", type=int, default=12)
    ap.add_argument("--side", type=int, default=512)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    rnd = random.Random(a.seed)
    ds = load_dataset(a.dataset, split=a.split, streaming=True)
    names = [n.replace("_", " ") for n in ds.features[a.label_col].names]
    cand = lambda i: {"id": str(i), "description": names[i]}
    seen, rows = Counter(), []
    for ex in ds:
        y = ex[a.label_col]
        if seen[y] >= a.per_class:
            if len(seen) == len(names) and min(seen.values()) >= a.per_class:
                break
            continue
        seen[y] += 1
        state, src = data_url(ex[a.image_col], a.side), f"{a.dataset.split('/')[-1]}-{a.split}-{sum(seen.values())}"
        others = [i for i in range(len(names)) if i != y]
        opts = [y, *rnd.sample(others, min(a.options, len(names)) - 1)]
        rnd.shuffle(opts)
        yes = seen[y] % 2 == 1  # alternate yes / no per class
        asked = y if yes else rnd.choice(others)
        base = {"source_id": src, "family": "images", "provenance": f"{a.dataset} {a.split}", "state": state}
        mc = {"type": "multiclass", "instruction": a.question, "candidates": [cand(i) for i in opts]}
        rows.append(base | {"id": f"{src}-mc", "question": mc, "target": str(y)})
        rows.append(base | {"id": f"{src}-yn", "question": {"type": "binary", "instruction": f"Is it {names[asked]}?"}, "target": yes})
    rnd.shuffle(rows)
    with open(a.out, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in rows)
    print(f"{len(rows)} questions over {sum(seen.values())} photos, {len(seen)}/{len(names)} classes -> {a.out}")


if __name__ == "__main__":
    main()
    os._exit(0)  # ponytail: the streaming reader's threads can keep the interpreter from exiting
