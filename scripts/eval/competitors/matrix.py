"""Accuracy matrix of the 2026-09-30 competitor run, from the files under reports/competitors/ (never typed by hand).

Rows: every model that has any result. Columns: our frozen sets through the same Jev-shaped request (accuracy counting
failed requests as wrong; answered share in brackets when < 100 %), typed-decisions test, JevBench public-231 (+ hard-111),
Nimble 13-subset macro. DecisionBench was stopped unfinished (README).
usage: uv run python scripts/eval/competitors/matrix.py > reports/competitors/matrix.md
       uv run python scripts/eval/competitors/matrix.py --public > reports/competitors/public_table.md  (website, docs, HF cards)
"""

import json
import re
from pathlib import Path

R = Path(__file__).resolve().parents[3] / "reports/competitors"


def ours_set(name, f):
    p = R / f / name / "report.json"
    if not p.exists():
        return ""
    m = json.loads(p.read_text())["meta"]
    cov = m["n"] / m["n_total"]
    return f"{100 * m['accuracy_all']:.1f}" + (f" ({100 * cov:.0f}% answered)" if cov < 1 else "")


HELD_OUT = {"img_hurricane", "img_indoor", "img_painting", "img_snacks"}  # image datasets selfjev never trained on


def image_split(name):
    """image test as 'held-out / trained-on' accuracy (families selfjev-4b-vision did not / did fine-tune on)."""
    p = R / "eval_images_v1" / name / "report.json"
    if not p.exists():
        return ""
    rep = json.loads(p.read_text())
    ids = {r["id"]: r["correct"] for r in rep["predictions"]}
    fam = {r["id"]: r["family"] for r in json.loads((R / "eval_images_v1/selfjev-4b-vision-api/report.json").read_text())["predictions"]}
    acc = lambda held: (
        100 * sum(ids.get(i, False) for i, f in fam.items() if (f in HELD_OUT) == held) / sum((f in HELD_OUT) == held for f in fam.values())
    )
    return f"{acc(True):.1f} / {acc(False):.1f}"


def typed(name):
    p = R / "typed_decisions" / name / "result.json"
    return f"{json.loads(p.read_text())['accuracy']:.1f}" if p.exists() else ""


def jevbench(name):
    p = R / "jevbench" / name / "tiers.txt"
    if not p.exists():
        return ""
    t = p.read_text()
    # tiers.txt has 4-decimal accuracies: back to correct counts (n attempted = n planned here) for exact 1-decimal rounding
    acc = {k: round(float(v) * int(n)) / int(n) for k, n, v in re.findall(r"^(\w+)\s+n=(\d+)/\d+ acc=([\d.]+)", t, re.M)}
    return f"{100 * acc['ALL231']:.1f} / {100 * acc['hard']:.1f}" if "ALL231" in acc and "hard" in acc else "failed"


def s1(name):
    p = R / "s1bench" / f"{name}.json"
    return f"{100 * json.loads(p.read_text())['macro']:.1f}" if p.exists() else ""


CARD = {  # size / base / licence, from each model card (2026-09-30 survey)
    "selfjev-4b-vision": "4B, Qwen3.5-4B + LoRA r64, text + images, Apache-2.0 code; Jev soft targets in training",
    "decider-4b": "4.2B, Qwen3.5-4B-Base full FT, text, Apache-2.0",
    "imajev-4b": "4B, Qwen3.5-4B + LoRA r64, text + images, Apache-2.0",
    "jpt-4b": "4.5B, Qwen3.5-4B merged LoRA, text + images, CC-BY-NC-4.0",
    "kev-4b": "4B, Qwen3.5-4B-Base + LoRA r16 + head, text, Apache-2.0",
    "laya": "0.4B, ModernBERT-large encoder, text, Apache-2.0",
    "laya-long": "same, max_len 8192 / head 2048",
    "mica-4b": "4.2B, Qwen3.5-4B merged LoRA (llama.cpp BF16), text, Apache-2.0",
    "plumb-4b": "4.2B, JevK5 (Qwen3.5-4B), text, Apache-2.0",
    "openjev-27b-fp8": "27B, Qwen3.8-27B FP8, text + images, CC-BY-NC-4.0",
}


def wall(name):
    p = R / "eval2" / ("selfjev-4b-vision-api-w4" if name == "selfjev-4b-vision" else name) / "report.json"
    return f"{json.loads(p.read_text())['meta']['wall_s']:.0f}" if p.exists() else ""


def full_matrix():
    from selfjev.evaluation.stats import mcnemar

    names = sorted(
        {p.parent.name for p in R.glob("*/*/report.json")}
        | {p.parent.name for p in R.glob("*/*/result.json")}
        | {p.parent.name for p in R.glob("jevbench/*/tiers.txt")}
        | {p.stem for p in R.glob("s1bench/*.json")}
    )
    COLS = [
        "model",
        "size, base, licence",
        "eval2 s (1 L40S)",
        "eval2",
        "eval_llm",
        "image test: held-out / trained-on datasets",
        "typed-decisions",
        "JevBench public-231 / hard-111",
        "Nimble 13 macro",
    ]
    print("| " + " | ".join(COLS) + " |\n" + "|---" * len(COLS) + "|")
    for n in names:
        alias = "selfjev-4b-vision-api" if n == "selfjev-4b-vision" else n
        cells = [ours_set(alias, "eval2"), ours_set(alias, "eval_llm"), image_split(alias), typed(n), jevbench(n), s1(n)]
        if n.startswith("selfjev-4b-vision-api"):
            continue
        print(f"| {n} | {CARD.get(n, '')} | {wall(n) or '—'} | " + " | ".join(c or "—" for c in cells) + " |")

    # paired exact McNemar vs our run through the same requests (failed requests count as wrong)

    print("\n| model | set | ours only right | model only right | p |\n|---|---|---|---|---|")
    for f in ("eval2", "eval_llm", "eval_images_v1"):
        base = R / f / "selfjev-4b-vision-api" / "report.json"
        if not base.exists():
            continue
        ours = {r["id"]: r["correct"] for r in json.loads(base.read_text())["predictions"]}
        for p in sorted((R / f).glob("*/report.json")):
            if p.parent.name.startswith("selfjev-4b-vision-api"):
                continue
            got = {r["id"]: r["correct"] for r in json.loads(p.read_text())["predictions"]}
            oa, ob, pv = mcnemar(ours, {i: got.get(i, False) for i in ours})
            print(f"| {p.parent.name} | {f} | {oa} | {ob} | {pv:.2g} |")


def public_table():
    """The table for the website, the docs and the Hugging Face cards: one row per model, sorted by eval2, Jev as reference."""
    jev_eval2 = json.loads((R.parent / "external/eval2/typesafe_jev-latest/report.json").read_text())["metrics"]["question_accuracy"]
    # Jev's other cells are published numbers: eval_llm docs/llm_eval_data.md (from data/eval_llm/review/jev_answers.jsonl),
    # typed-decisions the dataset's own leaderboard, JevBench the Benchmark Heaven board (v1.4.2.2 public accuracy, hard tier).
    rows = [
        ("Jev 1.13 (TypeSafe API, reference)", "?", "no", "paid API", f"{100 * jev_eval2:.1f}", "92.5", "—", "72.7", "86.6 / 73.0", "—")
    ]
    meta = {  # size, images, licence (model cards, 2026-09-30)
        "selfjev-4b-vision": ("4B", "yes", "Apache-2.0 code"),
        "openjev-27b-fp8": ("27B", "yes", "CC-BY-NC-4.0"),
        "plumb-4b": ("4.2B", "no", "Apache-2.0"),
        "jpt-4b": ("4.5B", "yes", "CC-BY-NC-4.0"),
        "imajev-4b": ("4B", "yes", "Apache-2.0"),
        "decider-4b": ("4.2B", "no", "Apache-2.0"),
        "mica-4b": ("4.2B", "no", "Apache-2.0"),
        "kev-4b": ("4B", "no", "Apache-2.0"),
        "laya": ("0.4B", "no", "Apache-2.0"),
    }
    links = {
        "selfjev-4b-vision": "[**SelfJev-4B Vision**](https://huggingface.co/Jwuthrich/selfjev-4b-vision)",
        "openjev-27b-fp8": "[openjev](https://huggingface.co/openjev/openjev)",
        "plumb-4b": "[Plumb-4B](https://huggingface.co/crh225/plumb-4b)",
        "jpt-4b": "[jpt-4b](https://huggingface.co/kirp/jpt-4b)",
        "imajev-4b": "[imajev-4b](https://huggingface.co/mohit67890/imajev-4b)",
        "decider-4b": "[decider-4b](https://huggingface.co/Mapika/decider-4b)",
        "mica-4b": "[Mica-v0.1-4B](https://huggingface.co/sky7350/Mica-v0.1-4B)",
        "kev-4b": "[kev-4b](https://huggingface.co/jaredpalmer/kev-4b)",
        "laya": "[Laya](https://huggingface.co/convaiinnovations/laya)",
    }
    acc = lambda n, f: ours_set("selfjev-4b-vision-api" if n == "selfjev-4b-vision" else n, f).split(" (")[0]
    for n in meta:
        held = image_split("selfjev-4b-vision-api" if n == "selfjev-4b-vision" else n).split(" / ")[0]
        td = typed(n) + (" ¹" if n == "jpt-4b" else "")
        e2, el = acc(n, "eval2"), acc(n, "eval_llm")
        if n == "mica-4b":
            e2, el = e2 + " ²", el + " ²"
        rows.append((links[n], *meta[n], e2, el, held or "—", td, jevbench(n) or "—", wall(n)))
    rows[1:] = sorted(rows[1:], key=lambda r: -float(r[4].split()[0]))
    head = [
        "model",
        "size",
        "images",
        "licence",
        "Text Decisions",
        "AI Response Review",
        "held-out images",
        "typed-decisions",
        "JevBench public / hard",
        "Text Decisions time (s)",
    ]
    out = ["| " + " | ".join(head) + " |", "|---" * len(head) + "|"] + ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(public_table()) if "--public" in sys.argv else full_matrix()
