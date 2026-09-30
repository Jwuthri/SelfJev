"""Frozen held-out image test: kinds of images and questions that NO training mix may use (images v1, v2, ...), to
measure generalization (docs/image_datasets.md, JOURNAL 2026-09-30). Human labels only. Photos and documents both.

Per dataset, 150 questions at random (seed 0; an image can carry two), images at most 1,024 px on the long side (documents need it):
- open-answer sets (TextVQA, VizWiz, DocVQA, ChartQA): a yes/no answer becomes a binary question; any other answer a
  multiclass among the answer + 3 distractors, shown as annotators wrote them. Text distractors are other questions'
  answers of the same shape (digits or not, about as many words) that no annotator gave for this question; number
  distractors are the answer x0.5 / x0.75 / x1.25 / x1.5 (never over 100 for a percentage; years +-1..3), all outside
  ChartQA's 5% tolerance. TextVQA / VizWiz need >= 3 of 10 annotators on the answer (the VQA-accuracy bar).
- multiple-choice sets (RealWorldQA, AI2D, CV-Bench without COCO images): their own options.
- the 4 held-out classification sets of images v1 (hurricane damage, snacks, indoor scenes, painting style) are in
  data/eval_images_v1.jsonl; score both files for the full held-out picture.

Image sources overlap nothing a v2 mix plans to use (COCO / Visual Genome: VQAv2, A-OKVQA, GQA, COCO labels).
Writes data/eval_images_heldout.jsonl and data/ova/eval_images_heldout.jsonl (gitignored, base64 images).
usage: uv run --group data python scripts/data/build_eval_images_heldout.py
"""

import json
import os
import random
import re
import sys
from collections import Counter
from pathlib import Path

from datasets import load_dataset

sys.path.insert(0, str(Path(__file__).parent))
from hf_images_to_rows import data_url

from selfjev.core.options import with_options

N, SIDE = 150, 1024
ARTICLES = re.compile(r"\b(a|an|the)\b")


def norm(a):
    a = ARTICLES.sub(" ", str(a).lower().strip())
    return " ".join(re.sub(r"[^\w\s.%-]", " ", a).split()).rstrip(".")


def number(a):
    try:
        return float(norm(a).replace(",", "").rstrip("%"))
    except ValueError:
        return None


def num_distractors(gold, question=""):
    g = number(gold)
    if g is None:
        return None
    if g.is_integer() and 1900 <= g <= 2100:  # a year: other years
        return [str(int(g + d)) for d in (-3, -2, -1, 1, 2, 3)]
    fmt = (lambda x: str(round(x))) if g.is_integer() else (lambda x: f"{x:.{len(norm(gold).split('.')[-1])}f}")
    pct = "%" in str(gold) or (re.search(r"%|percent|share", question.lower()) and 0 <= g <= 100)
    if not g:
        return ["1", "2", "5"]
    out = [fmt(g * f) for f in (0.5, 0.75, 1.25, 1.5, 0.25, 0.9, 2)]  # the first ones first: the most plausible
    return [x for x in dict.fromkeys(out) if abs(number(x) - g) > 0.05 * abs(g) and not (pct and number(x) > 100)]


def shape(a):
    return any(c.isdigit() for c in str(a)), min(len(str(a).split()), 4)


def open_rows(name, items, rnd):
    """items: [(image, question, gold, all_answers)] -> rows (binary for yes/no, else multiclass with 3 distractors)."""
    pool = {True: [], False: []}
    for *_, gold, _ in items:
        if norm(gold) not in ("yes", "no"):
            pool[number(gold) is not None].append(gold)
    out = []
    for i, (img, q, gold, answers) in enumerate(items):
        src = f"{name}-{i}"
        base = {"source_id": src, "family": f"held_{name}", "provenance": f"held-out {name}", "state": data_url(img, SIDE), "split": "test"}
        if norm(gold) in ("yes", "no"):
            out.append(base | {"id": src, "question": {"type": "binary", "instruction": q}, "target": norm(gold) == "yes"})
            continue
        taken = {norm(a) for a in answers}
        same = [a for a in pool[False] if shape(a) == shape(gold)] or pool[False]
        cands = (num_distractors(gold, q) if number(gold) is not None else None) or rnd.sample(same, min(40, len(same)))
        dis = [c for c in dict.fromkeys(cands) if norm(c) not in taken][:3]
        if len(dis) < 3:
            continue
        opts = [gold, *dis]
        rnd.shuffle(opts)
        cand = [{"id": f"o{k}", "description": str(o)} for k, o in enumerate(opts)]
        out.append(
            base | {"id": src, "question": {"type": "multiclass", "instruction": q, "candidates": cand}, "target": f"o{opts.index(gold)}"}
        )
    return out


def mc_rows(name, items):
    """items: [(image, question, [options], index of the right one)] -> multiclass rows with the dataset's own options."""
    out = []
    for i, (img, q, opts, gold) in enumerate(items):
        src = f"{name}-{i}"
        cand = [{"id": f"o{k}", "description": str(o)} for k, o in enumerate(opts)]
        base = {"source_id": src, "family": f"held_{name}", "provenance": f"held-out {name}", "state": data_url(img, SIDE), "split": "test"}
        out.append(base | {"id": src, "question": {"type": "multiclass", "instruction": q, "candidates": cand}, "target": f"o{gold}"})
    return out


def realworldqa(e):
    """'stem\n\nA. x\nB. y\n...\nPlease answer ...', answer 'B' -> (stem, [x, y], 1); None if not multiple choice."""
    lines = e["question"].split("\n")
    opts = [(m[1], m[2].strip()) for ln in lines if (m := re.match(r"^([A-F])[.)]\s*(.+)$", ln.strip()))]
    letters = [x for x, _ in opts]
    if len(opts) < 2 or e["answer"].strip() not in letters or len({o for _, o in opts}) < len(opts):
        return None
    stem = " ".join(
        ln.strip() for ln in lines[: next(i for i, ln in enumerate(lines) if re.match(r"^[A-F][.)]", ln.strip()))] if ln.strip()
    )
    return stem, [o for _, o in opts], letters.index(e["answer"].strip())


def majority(answers, need):
    """The answer >= need annotators gave (after norm), as most of them wrote it; else None."""
    (a, c), *_ = Counter(norm(x) for x in answers).most_common(1)
    return Counter(x.strip() for x in answers if norm(x) == a).most_common(1)[0][0] if c >= need else None


def take(ds, cfg, split, n=N * 3):
    d = load_dataset(ds, cfg, split=split, streaming=True) if cfg else load_dataset(ds, split=split, streaming=True)
    return [ex for _, ex in zip(range(n), d)]


def main():
    rnd, rows = random.Random(0), []

    def keep(name, items):  # N items at random, then converted
        items = rnd.sample(items, min(N + 30, len(items)))  # a margin for items the conversion drops
        got = open_rows(name, items, rnd)[:N]
        print(f"  {name}: {len(got)} questions ({Counter(r['question']['type'] for r in got)})", flush=True)
        rows.extend(got)

    tv = take("lmms-lab/textvqa", None, "validation")  # N * 3 streamed, then N at random
    keep("textvqa", [(e["image"], e["question"].capitalize() + "?" * (not e["question"].endswith("?")), g, e["answers"])
                     for e in tv if (g := majority(e["answers"], 3))])  # fmt: skip
    vz = take("lmms-lab/VizWiz-VQA", None, "val")
    keep(
        "vizwiz",
        [(e["image"], e["question"], g, e["answers"]) for e in vz if (g := majority(e["answers"], 3)) and norm(g) != "unanswerable"],
    )
    dv = take("lmms-lab/DocVQA", "DocVQA", "validation")
    keep("docvqa", [(e["image"], e["question"], e["answers"][0], e["answers"]) for e in dv])
    cq = take("lmms-lab/ChartQA", None, "test")
    keep("chartqa", [(e["image"], e["question"], e["answer"], [e["answer"]]) for e in cq if e["type"] == "human_test"])

    def keep_mc(name, items):
        items = rnd.sample(items, min(N, len(items)))
        got = mc_rows(name, items)
        print(f"  {name}: {len(got)} questions (multiclass)", flush=True)
        rows.extend(got)

    rw = take("lmms-lab/RealWorldQA", None, "test", 800)
    keep_mc("realworldqa", [(e["image"], *x) for e in rw if (x := realworldqa(e))])
    ai = take("lmms-lab/ai2d", None, "test")
    keep_mc(
        "ai2d",
        [
            (e["image"], e["question"], e["options"], int(e["answer"]))
            for e in ai
            if len({o.lower() for o in e["options"]}) == len(e["options"])
        ],
    )
    cv = take("nyu-visionx/CV-Bench", None, "test", 2700)
    keep_mc(
        "cvbench",
        [(e["image"], e["question"], e["choices"], "ABCDEF".index(e["answer"].strip("() "))) for e in cv if e["source"] != "COCO"],
    )

    Path("data/ova").mkdir(parents=True, exist_ok=True)
    with open("data/eval_images_heldout.jsonl", "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in rows)
    with open("data/ova/eval_images_heldout.jsonl", "w") as f:
        f.writelines(json.dumps(r | {"question": with_options(r["question"], r["id"])}) + "\n" for r in rows)
    print(f"{len(rows)} questions -> data/eval_images_heldout.jsonl, data/ova/eval_images_heldout.jsonl", flush=True)


if __name__ == "__main__":
    main()
    os._exit(0)  # the streaming reader's threads can keep the interpreter from exiting
