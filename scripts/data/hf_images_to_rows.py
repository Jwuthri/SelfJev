"""A Hugging Face image-classification dataset (an image column and a ClassLabel) -> questions in the eval schema, for
`selfjev finetune --data` and `selfjev eval` (or a fine-tuning upload after `selfjev.types.TrainingRow` conversion).

Per photo, on the same state (the photo, a base64 JPEG data URL, longest side <= side):
  - multiclass: the true class among up to `options` classes (the rest random), listed in the question by the trainer;
  - binary "<question> Is it <class>?": the true class (yes) or a random other one (no), alternating per class
    (skipped for 2-class datasets, where the multiclass question already is binary).
per_class caps the photos per class; the dataset streams, so nothing is downloaded whole. For a dataset with a single
split, holdout=(k, part) keeps every k-th row for part="test" and the others for part="train".

usage: uv run --group data python scripts/data/hf_images_to_rows.py timm/oxford-iiit-pet --split train --out data/pets_train.jsonl \
           --question "What breed is the pet in this photo?" --per-class 60
       (datasets: docs/image_datasets.md; the v1 mix: scripts/data/build_images_v1.py)
"""

import argparse
import base64
import io
import json
import os
import random
import re
from collections import Counter

from datasets import load_dataset


def data_url(img, side=512):
    img = img.convert("RGB")
    img.thumbnail((side, side))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def readable(name):
    """'AnnualCrop' -> 'Annual Crop', 'angular_leaf_spot' -> 'angular leaf spot'."""
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name).replace("_", " ").strip()


def rows_from(dataset, split, question, *, short=None, label_col="label", image_col="image", per_class=50, options=12,
              side=512, seed=0, holdout=None, revision=None, split_name=None):  # fmt: skip
    rnd, short = random.Random(seed), short or dataset.split("/")[-1]
    ds = load_dataset(dataset, split=split, streaming=True, revision=revision)
    names = [readable(n) for n in ds.features[label_col].names]
    cand = lambda i: {"id": str(i), "description": names[i]}
    seen, out, part = Counter(), [], split_name or split
    for n, ex in enumerate(ds):
        if holdout and (n % holdout[0] == 0) != (holdout[1] == "test"):
            continue
        y = ex[label_col]
        if seen[y] >= per_class:
            if len(seen) == len(names) and min(seen.values()) >= per_class:
                break
            continue
        seen[y] += 1
        src = f"{short}-{part}-{n}"
        state = data_url(ex[image_col], side)
        base = {"source_id": src, "family": f"img_{short}", "provenance": f"hf {dataset} {split}", "state": state, "split": part}
        others = [i for i in range(len(names)) if i != y]
        opts = [y, *rnd.sample(others, min(options, len(names)) - 1)]
        rnd.shuffle(opts)
        mc = {"type": "multiclass", "instruction": question, "candidates": [cand(i) for i in opts]}
        out.append(base | {"id": f"{src}-mc", "question": mc, "target": str(y)})
        if len(names) > 2:
            yes = seen[y] % 2 == 1
            asked = y if yes else rnd.choice(others)
            yn = {"type": "binary", "instruction": f"{question} Is it {names[asked]}?"}
            out.append(base | {"id": f"{src}-yn", "question": yn, "target": yes})
    print(f"  {dataset} {part}: {sum(seen.values())} photos, {len(seen)}/{len(names)} classes, {len(out)} questions", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("--split", default="train")
    ap.add_argument("--out", required=True)
    ap.add_argument("--question", default="What is in this photo?")
    ap.add_argument("--image-col", default="image")
    ap.add_argument("--label-col", default="label")
    ap.add_argument("--per-class", type=int, default=50)
    ap.add_argument("--options", type=int, default=12)
    ap.add_argument("--side", type=int, default=512)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--revision", help="e.g. refs/convert/parquet for datasets that need a loading script")
    a = ap.parse_args()
    rows = rows_from(a.dataset, a.split, a.question, label_col=a.label_col, image_col=a.image_col, per_class=a.per_class,
                     options=a.options, side=a.side, seed=a.seed, revision=a.revision)  # fmt: skip
    random.Random(a.seed).shuffle(rows)
    with open(a.out, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in rows)
    print(f"{len(rows)} questions -> {a.out}")


if __name__ == "__main__":
    main()
    os._exit(0)  # ponytail: the streaming reader's threads can keep the interpreter from exiting
