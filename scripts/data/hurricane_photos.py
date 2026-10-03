"""A folder of labelled photos for the image fine-tuning demo: satellite images of hurricane damage, a task selfjev-4b-vision
does poorly zero-shot (62% on its frozen test; data/eval_images_v1.jsonl, family img_hurricane).

The test photos are every 10th row of the dataset's train split (scripts/data/build_images_v1.py); these come from the
other rows, and any photo whose bytes equal a test photo's is dropped. Writes runs/hurricane_demo/photos/<label>/<n>.jpg
(512 px JPEGs, as the test), the layout a user's labelled photos would have.
usage: uv run --group data python scripts/data/hurricane_photos.py [PER_CLASS=150]
"""

import base64
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hf_images_to_rows import rows_from

DS, Q = "jonathan-roberts1/Satellite-Images-of-Hurricane-Damage", "What does this satellite image show?"


def main():
    per_class = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    with open("data/eval_images_v1.jsonl") as f:
        test = {r["state"] for r in map(json.loads, f) if r["family"] == "img_hurricane"}
    rows = rows_from(DS, "train", Q, short="hurricane", per_class=per_class, holdout=(10, "train"))
    out, kept = Path("runs/hurricane_demo/photos"), 0
    for r in rows:
        if r["state"] in test:
            continue
        label = next(c["description"] for c in r["question"]["candidates"] if c["id"] == r["target"])
        path = out / label / f"{r['source_id'].rsplit('-', 1)[1]}.jpg"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(base64.b64decode(r["state"].split(",", 1)[1]))
        kept += 1
    print(f"{kept} photos ({len(rows) - kept} equal to a test photo, dropped) -> {out}/<label>/", flush=True)


if __name__ == "__main__":
    main()
    os._exit(0)  # the streaming reader's threads can keep the interpreter from exiting
