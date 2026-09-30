"""Frozen image test set from the Oxford-IIIT Pet test split (timm/oxford-iiit-pet, CC BY-SA 4.0; human labels): each
state is one photo as a base64 JPEG data URL (longest side <= 512 px), questions in eval2's schema.

- pets_cat_breed: every cat photo, "which breed", 12 options (multiclass)
- pets_breed37: 10 photos per breed, 37 options, cats and dogs (multiclass)
- pets_is_cat: 150 cats + 150 dogs, "is it a cat" (binary)

Writes data/eval_pets.jsonl and its option-list copy data/ova/eval_pets.jsonl (what `selfjev eval` reads).
usage: uv run --group data python scripts/data/build_eval_pets.py
"""

import base64
import io
import json
import random
from pathlib import Path

import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download
from PIL import Image

from selfjev.core.options import with_options

REPO, REV = "timm/oxford-iiit-pet", "089695c834a7deb60505b7cc506672db1c31a6aa"
PROVENANCE = f"{REPO}@{REV[:7]} test split, human label (CC BY-SA 4.0)"


def data_url(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img.thumbnail((512, 512))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    t = pq.read_table(hf_hub_download(REPO, "data/test-00000-of-00001.parquet", repo_type="dataset", revision=REV))
    names = json.loads(t.schema.metadata[b"huggingface"])["info"]["features"]["label"]["names"]
    rows = t.to_pylist()
    species = {r["label"]: ("cat", "dog")[r["label_cat_dog"]] for r in rows}
    desc = {i: f"{'an' if n[0] in 'aeiou' else 'a'} {n.replace('_', ' ').title()} {species[i]}" for i, n in enumerate(names)}
    cand = lambda labels: [{"id": names[i], "description": desc[i]} for i in sorted(labels)]
    cats = sorted(i for i in species if species[i] == "cat")
    rnd = random.Random(0)
    by_label = {i: [r for r in rows if r["label"] == i] for i in species}
    picks = {
        "pets_cat_breed": [r for r in rows if species[r["label"]] == "cat"],
        "pets_breed37": [r for i in sorted(by_label) for r in rnd.sample(by_label[i], 10)],
        "pets_is_cat": rnd.sample([r for r in rows if species[r["label"]] == "cat"], 150)
        + rnd.sample([r for r in rows if species[r["label"]] == "dog"], 150),
    }
    out = []
    for family, rs in picks.items():
        for r in rs:
            q = {
                "pets_cat_breed": {"type": "multiclass", "instruction": "What breed is the cat in this photo?", "candidates": cand(cats)},
                "pets_breed37": {"type": "multiclass", "instruction": "What breed is the pet in this photo?", "candidates": cand(species)},
                "pets_is_cat": {"type": "binary", "instruction": "Is the animal in this photo a cat?"},
            }[family]
            target = species[r["label"]] == "cat" if family == "pets_is_cat" else names[r["label"]]
            sid = r["image_id"]
            out.append(
                {"source_id": sid, "family": family, "provenance": PROVENANCE, "state": data_url(r["image"]["bytes"]),
                 "id": f"{family}-{sid}", "question": q, "target": target, "hard_cases": [], "split": "test"}
            )  # fmt: skip
    Path("data/ova").mkdir(parents=True, exist_ok=True)
    Path("data/eval_pets.jsonl").write_text("".join(json.dumps(r) + "\n" for r in out))
    ova = [r | {"question": with_options(r["question"], r["id"])} for r in out]
    Path("data/ova/eval_pets.jsonl").write_text("".join(json.dumps(r) + "\n" for r in ova))
    print({f: len(rs) for f, rs in picks.items()}, len(out), "rows")


if __name__ == "__main__":
    main()
