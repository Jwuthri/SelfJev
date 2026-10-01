"""The images v2 mix: diverse human-labelled questions about photos, for transfer to unseen image tasks (images v1 learnt
its 6 fixed-label tasks but moved unseen ones only 83.5 -> 84.3). Continues from the vision release (images v1).

- VQAv2 (validation, CC BY 4.0; COCO photos): >= 4 of 10 annotators agree; yes/no -> binary; counts -> a choice among the
  count and +-1 / +-2; other answers -> a choice among 3 wrong answers to questions of the same type ("what color is the")
  that no annotator gave. At most 2 questions per photo, at most 40% yes/no.
- A-OKVQA (train, Apache-2.0): its 4 human-written options (commonsense and world knowledge about the photo).
- COCO 2017 objects (train, CC BY 4.0): "which of these can be seen?", multilabel over 6 options: 0-3 of the objects
  annotated in the photo and look-alikes that are not (other objects seen with them elsewhere); 15% have none.
- replay: 3,000 image questions of images v1 (its 6 tasks) and text questions from selfjev-4b's own training rows with
  Jev's soft targets, keeping a third of the texts over 4K tokens (JOURNAL 2026-09-30 15:45: ~1.7x faster).

None of these sources is in data/ova/eval_images_heldout.jsonl (no COCO or Visual Genome photos there).
Writes runs/images_v2/{train,val}.jsonl.gz (gitignored). usage: uv run --group data python scripts/data/build_images_v2.py
"""

import gzip
import itertools
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from datasets import load_dataset

sys.path.insert(0, str(Path(__file__).parent))
from build_eval_images_heldout import norm, shape
from hf_images_to_rows import data_url

N_VQA, N_AOK, N_COCO, N_V1, N_TEXT, LONG_FRAC = 8000, 5000, 3000, 3000, 12000, 1 / 3
rnd, ids = random.Random(0), itertools.count()


def stream(ds, split, n, cfg=None):
    d = load_dataset(ds, cfg, split=split, streaming=True) if cfg else load_dataset(ds, split=split, streaming=True)
    return (ex for _, ex in zip(range(n), d))


def row(src, family, img, q, target):
    return {"source_id": src, "family": family, "provenance": f"images v2 {family}", "state": img, "split": "train",
            "id": f"{src}-{next(ids)}", "question": q, "target": target}  # fmt: skip


def choice(q, gold, wrong):
    opts = [gold, *wrong]
    rnd.shuffle(opts)
    return {
        "type": "multiclass",
        "instruction": q,
        "candidates": [{"id": f"o{k}", "description": o} for k, o in enumerate(opts)],
    }, f"o{opts.index(gold)}"


def vqav2():
    items = []  # (image, question, gold, human answers, answer_type, question_type)
    for ex in stream("lmms-lab/VQAv2", "validation", N_VQA * 4):
        answers = [a["answer"] for a in ex["answers"]]
        (a, c), *_ = Counter(norm(x) for x in answers).most_common(1)
        if c >= 4 and a:
            gold = Counter(x.strip() for x in answers if norm(x) == a).most_common(1)[0][0]
            items.append((ex["image"], ex["question"], gold, answers, ex["answer_type"], ex["question_type"], ex["image_id"]))
    pool = defaultdict(dict)  # question type -> {normalized answer: as written}
    for _, _, gold, _, at, qt, _ in items:
        if at == "other":
            pool[qt].setdefault(norm(gold), gold)
    rnd.shuffle(items)
    out, per_image, urls, yn = [], Counter(), {}, 0
    for img, q, gold, answers, at, qt, iid in items:
        if len(out) >= N_VQA or per_image[iid] >= 2 or (at == "yes/no" and yn >= 0.4 * N_VQA):
            continue
        taken = {norm(x) for x in answers}
        if at == "yes/no" and norm(gold) in ("yes", "no"):
            question, target = {"type": "binary", "instruction": q}, norm(gold) == "yes"
            yn += 1
        elif at == "number" and norm(gold).isdigit():
            g = int(norm(gold))
            wrong = [str(x) for x in (g - 1, g + 1, g + 2, g - 2, g + 3) if x >= 0 and str(x) not in taken][:3]
            if len(wrong) < 3:
                continue
            question, target = choice(q, gold, wrong)
        elif at == "other":
            same = [x for n, x in pool[qt].items() if n not in taken and shape(x) == shape(gold)]
            if len(same) < 3:
                continue
            question, target = choice(q, gold, rnd.sample(same, 3))
        else:
            continue
        urls[iid] = urls.get(iid) or data_url(img)
        per_image[iid] += 1
        out.append(row(f"vqav2-{iid}", "img2_vqav2", urls[iid], question, target))
    return out


def aokvqa():
    out = []
    for i, ex in enumerate(stream("HuggingFaceM4/A-OKVQA", "train", N_AOK)):
        opts, k = ex["choices"], int(ex["correct_choice_idx"])
        if not all(o.strip() for o in opts) or len({norm(o) for o in opts}) < len(opts):  # 2 of 5,000 have an empty option
            continue
        question = {
            "type": "multiclass",
            "instruction": ex["question"],
            "candidates": [{"id": f"o{j}", "description": o} for j, o in enumerate(opts)],
        }
        out.append(row(f"aokvqa-{i}", "img2_aokvqa", data_url(ex["image"]), question, f"o{k}"))
    return out


def coco():
    ds = load_dataset("detection-datasets/coco", split="train", streaming=True)
    names = ds.features["objects"]["category"].feature.names
    photos = [(ex["image"], sorted(set(ex["objects"]["category"]))) for _, ex in zip(range(N_COCO), ds) if ex["objects"]["category"]]
    seen_with = defaultdict(Counter)  # look-alikes: objects that appear with these ones in other photos
    for _, cats in photos:
        for a in cats:
            seen_with[a].update(b for b in cats if b != a)
    out = []
    for i, (img, cats) in enumerate(photos):
        k = 0 if rnd.random() < 0.15 else rnd.randint(1, min(3, len(cats)))
        present = rnd.sample(cats, k)
        near = [b for a in cats for b, _ in seen_with[a].most_common(8) if b not in cats]
        absent = list(dict.fromkeys(near))[: 6 - k] or []
        absent += rnd.sample([c for c in range(len(names)) if c not in cats and c not in absent], 6 - k - len(absent))
        opts = present + absent
        rnd.shuffle(opts)
        cand = [{"id": re.sub(r"\W+", "_", names[c]), "description": names[c]} for c in opts]
        question = {"type": "multilabel", "instruction": "Which of these can be seen in the photo?", "candidates": cand}
        out.append(row(f"coco-{i}", "img2_coco", data_url(img), question, [re.sub(r"\W+", "_", names[c]) for c in present]))
    return out


def write(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt") as f:
        f.writelines(json.dumps(r) + "\n" for r in rows)


def main():
    img = []
    for name, fn in (("vqav2", vqav2), ("aokvqa", aokvqa), ("coco", coco)):
        got = fn()
        print(f"  {name}: {len(got)} questions {dict(Counter(r['question']['type'] for r in got))}", flush=True)
        img += got
    with open("data/images_v1/train.jsonl") as f:
        v1 = rnd.sample([json.loads(line) for line in f], N_V1)
    photos = sorted({r["source_id"] for r in img})
    val_photos = set(rnd.sample(photos, len(photos) // 20))
    img_val = [r | {"split": "validation"} for r in img if r["source_id"] in val_photos]
    img_train = [r for r in img if r["source_id"] not in val_photos] + v1
    with gzip.open("runs/jev_all/train.jsonl.gz", "rt") as f:
        text = [r for line in f if len((r := json.loads(line))["state"]) <= 4096 * 3.6 or rnd.random() < LONG_FRAC]
    with gzip.open("runs/jev_all/val.jsonl.gz", "rt") as f:
        text_val = [json.loads(line) for line in f]
    mix = img_train + rnd.sample(text, N_TEXT)
    rnd.shuffle(mix)
    write("runs/images_v2/train.jsonl.gz", mix)
    write("runs/images_v2/val.jsonl.gz", img_val + text_val)
    print(
        f"train: {len(img_train)} image ({N_V1} of them images v1) + {N_TEXT} text; val: {len(img_val)} image + {len(text_val)} text",
        flush=True,
    )


if __name__ == "__main__":
    main()
    os._exit(0)  # the streaming reader's threads can keep the interpreter from exiting
