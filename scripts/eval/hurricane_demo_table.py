"""The image fine-tuning demo's table, from its report files: the release vs the hurricane fine-tunes, per image test family
and on eval2, paired (McNemar). usage: uv run python scripts/eval/hurricane_demo_table.py > reports/hurricane_demo/README.md"""

import json
from collections import defaultdict
from pathlib import Path

from selfjev.evaluation.stats import mcnemar

R = Path(__file__).resolve().parents[2] / "reports"
RUNS = {
    "release": R / "engine_0.4.1",
    "1 epoch (2 steps)": R / "hurricane_demo/1_epoch",
    "5 epochs (10 steps)": R / "hurricane_demo/5_epochs",
}


def preds(run, name):
    rep = json.loads((run / name / "report.json").read_text())
    return {p["id"]: bool(p["correct"]) for p in rep["predictions"]}, {p["id"]: p.get("family", "") for p in rep["predictions"]}


def cell(base, new, ids):
    acc = 100 * sum(new[k] for k in ids) / len(ids)
    if base is new:
        return f"{acc:.1f}"
    broken, fixed, p = mcnemar({k: base[k] for k in ids}, {k: new[k] for k in ids})
    return f"{acc:.1f} ({fixed} fixed / {broken} broken, p = {p:.2g})"


def main():
    imgs = {k: preds(v, "eval_images_v1")[0] for k, v in RUNS.items()}
    fam = preds(RUNS["release"], "eval_images_v1")[1]
    by = defaultdict(list)
    for k in imgs["release"]:
        by[fam[k].removeprefix("img_")].append(k)
    base = imgs["release"]
    print("# Image fine-tuning on 300 photos of a new task (hurricane damage), through the API\n")
    print("`scripts/data/hurricane_photos.py` (150 photos per class from rows the frozen test does not use) ->")
    print("`scripts/eval/image_finetune_demo.py` (rows from a folder, `upload_file`, a job, `wait_fine_tuning_job`) on")
    print("`selfjev serve --fine-tuning` 0.4.1, L40S; each model then scored by `selfjev eval` on the frozen image test")
    print("(`data/ova/eval_images_v1.jsonl`) and eval2. Paired against the release on the same engine. JOURNAL 2026-10-02.\n")
    print("| test | " + " | ".join(RUNS) + " |")
    print("|---" * (len(RUNS) + 1) + "|")
    for f in sorted(by, key=lambda f: (f != "hurricane", f)):
        print(f"| {f} ({len(by[f])} q) | " + " | ".join(cell(base, imgs[r], by[f]) for r in RUNS) + " |")
    print("| **all images** (2,002 q) | " + " | ".join(cell(base, imgs[r], list(base)) for r in RUNS) + " |")
    text = {k: preds(v, "eval2")[0] for k, v in RUNS.items()}
    print("| **eval2 (text)** | " + " | ".join(cell(text["release"], text[r], list(text["release"])) for r in RUNS) + " |")


if __name__ == "__main__":
    main()
