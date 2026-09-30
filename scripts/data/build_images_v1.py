"""The images v1 mix: does image skill generalize across tasks while text stays as good? (docs/image_datasets.md)

- Train (licence-safe only, so the weights can ship): 6 datasets, ~1,000 photos each, a multiclass + a yes/no question
  per photo (scripts/data/hf_images_to_rows.py); 5% of the photos (by photo) held out for validation.
- Text replay: as many text questions as image ones, drawn at random (seed 0) from selfjev-4b's own training rows with
  Jev's soft targets (runs/jev_all/train.jsonl.gz, scripts/train/jev_soft_targets.py), so text is not forgotten.
- Test (frozen): ~100 photos from the test part of each training dataset (disjoint photos) + 4 HELD-OUT datasets never
  trained on (new tasks: satellite damage, snacks, indoor scenes, painting style), for transfer.

Writes data/images_v1/{train,val}.jsonl (images only), runs/images_v1/{train,val}.jsonl.gz (the mix `selfjev finetune`
reads) and data/eval_images_v1.jsonl + data/ova/eval_images_v1.jsonl (the test set). All gitignored (base64 images).
usage: uv run python scripts/train/jev_soft_targets.py && uv run --group data python scripts/data/build_images_v1.py
"""

import gzip
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hf_images_to_rows import rows_from

from selfjev.core.options import with_options

P = "refs/convert/parquet"  # Hugging Face's parquet copy: loads datasets whose repo has a loading script
# id, short, question, label col, train split, test split (None: every 10th row of the train split), train / test photos per class, revision
TRAIN = [
    ("timm/oxford-iiit-pet", "pets", "What breed is the pet in this photo?", "label", "train", "test", 30, 3, None),
    ("zalando-datasets/fashion_mnist", "fashion", "What type of clothing item is this?", "label", "train", "test", 100, 10, None),
    ("AI-Lab-Makerere/beans", "beans", "What is the condition of this bean leaf?", "labels", "train", "test", 300, 34, None),
    ("nateraw/rice-image-dataset", "rice", "Which rice variety are these grains?", "label", "train", None, 200, 20, P),
    ("timm/eurosat-rgb", "eurosat", "What land use does this satellite image show?", "label", "train", "test", 100, 10, None),
    ("garythung/trashnet", "trash", "What material is this waste item?", "label", "train", None, 160, 17, P),
]
HELD_OUT = [  # test only: never in training
    (
        "jonathan-roberts1/Satellite-Images-of-Hurricane-Damage",
        "hurricane",
        "What does this satellite image show?",
        "label",
        "train",
        None,
        0,
        50,
        None,
    ),
    ("Matthijs/snacks", "snacks", "What snack is in this photo?", "label", None, "test", 0, 5, P),
    ("keremberke/indoor-scene-classification", "indoor", "What kind of room or place is this?", "labels", None, "test", 0, 2, P),
    ("keremberke/painting-style-classification", "painting", "What painting style is this?", "labels", None, "test", 0, 4, P),
]


def write(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    op = gzip.open if str(path).endswith(".gz") else open
    with op(path, "wt") as f:
        f.writelines(json.dumps(r) + "\n" for r in rows)


def main():
    rnd, train, test = random.Random(0), [], []
    for ds, short, q, lab, tr, te, n_tr, n_te, rev in TRAIN + HELD_OUT:
        kw = {"short": short, "label_col": lab, "revision": rev}
        if n_tr:
            train += rows_from(ds, tr, q, per_class=n_tr, holdout=None if te else (10, "train"), **kw)
        test += rows_from(ds, te or tr, q, per_class=n_te, holdout=None if te else (10, "test"), split_name="test", **kw)
    photos = sorted({r["source_id"] for r in train})
    val_photos = set(rnd.sample(photos, len(photos) // 20))
    img_val = [r | {"split": "validation"} for r in train if r["source_id"] in val_photos]
    img_train = [r for r in train if r["source_id"] not in val_photos]
    write("data/images_v1/train.jsonl", img_train)
    write("data/images_v1/val.jsonl", img_val)
    write("data/eval_images_v1.jsonl", test)
    write("data/ova/eval_images_v1.jsonl", [r | {"question": with_options(r["question"], r["id"])} for r in test])

    with gzip.open("runs/jev_all/train.jsonl.gz", "rt") as f:
        text = [json.loads(line) for line in f]
    with gzip.open("runs/jev_all/val.jsonl.gz", "rt") as f:
        text_val = [json.loads(line) for line in f]
    replay = rnd.sample(text, len(img_train))
    mix = img_train + replay
    rnd.shuffle(mix)
    write("runs/images_v1/train.jsonl.gz", mix)
    write("runs/images_v1/val.jsonl.gz", img_val + text_val)
    print(f"train: {len(img_train)} image + {len(replay)} text questions; val: {len(img_val)} image + {len(text_val)} text; "
          f"test: {len(test)} questions over {len({r['source_id'] for r in test})} photos", flush=True)  # fmt: skip


if __name__ == "__main__":
    main()
    os._exit(0)  # the streaming reader's threads can keep the interpreter from exiting
