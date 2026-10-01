"""Write the open-model comparison (2026-09-30 head-to-head) everywhere it is shown, from the generated table only.

Targets: reports/competitors/card_section.md (the {{COMPARISON}} of scripts/docs/model_card.template.md), docs/comparison.md (docs site),
website/content/comparison.md (website docs page), README.md and the local model cards (between markers), and with
--push-hf the README of every Hugging Face repo of the project (download, replace or insert the marked block, upload).
Re-running replaces the block; nothing outside the markers changes.

usage: uv run python scripts/docs/publish_comparison.py [--push-hf]
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/eval/competitors"))
from matrix import public_table  # noqa: E402

GH = "https://github.com/Jwuthri/SelfJev/blob/master/"
START, END = "<!-- selfjev:comparison:start -->", "<!-- selfjev:comparison:end -->"

BODY = """*Measured 2026-09-30.* Eight open "Jev-like" decision models from Hugging Face and SelfJev were each served with
their card's recommended setup on the same GPU (one NVIDIA L40S) and asked exactly the requests TypeSafe's Jev receives.
A request a model cannot answer counts as wrong. Jev is shown for reference.

**SelfJev's test suites.** Text Decisions (1,991 questions) and AI Response Review (946), published as
[selfjev-decision-bench](https://huggingface.co/datasets/Jwuthrich/selfjev-decision-bench), and photos:

{table1}

- Every model gets the same Jev-shaped questions; select-all questions become one yes/no per option, which costs SelfJev
  1.4–1.8 points against its native evaluation (96.1 and 92.5). **Held-out images**: the 4 image datasets of the SelfJev
  image test that none of these models trained on (772 questions). **Time**: Text Decisions end to end, 4 requests in
  flight. ² Refuses inputs over 8,192 tokens (2 % and 1 % of the questions), counted wrong.
- No other model trained on these suites, but they come from the same authors and judges as SelfJev's training data,
  so they favour SelfJev.
- SelfJev is the most accurate open model at 4.5B parameters or less on both suites (paired tests, p ≤ 0.023) and ties
  imajev-4b on held-out images; the 27B openjev is higher on Text Decisions. It is slower than most 4B models here.


Protocol, per-model setups, paired tests and raw reports: [reports/competitors]({gh}reports/competitors/README.md)."""


def block(title="## Compared with open Jev-like models", note=""):
    text = BODY.format(table1=public_table()[0], gh=GH)
    return "\n".join(x for x in (START, title, "", note + "\n" if note else "", text, END) if x is not None).replace("\n\n\n", "\n\n")


def s1_macro():
    return 100 * json.loads((ROOT / "reports/competitors/s1bench/selfjev-4b-vision.json").read_text())["macro"]


def fix_stale(text):
    """Sentences of the text cards that the 2026-09-30 measurements made stale (no-op where absent)."""
    return text.replace(
        "There is **no SelfJev S1Bench result yet**. Lev's published S1Bench scores cannot be compared with our authored-test scores. "
        "Comparing SelfJev, Lev, Reflex and other decision models requires the same dataset revision, item IDs, candidate sets, "
        "scoring rules and coverage.",
        f"**S1Bench** (the 13 public subsets pinned by Nimble, 3,880 items, run through lev's harness on 2026-09-30): SelfJev-4B "
        f"Vision **{s1_macro():.1f}** macro accuracy; lev's card reports 68.9 for lev and 76.1 for Jev through the same harness. "
        "The other shared benchmarks: [Compared with open Jev-like models](#compared-with-open-jev-like-models).",
    ).replace("We make no S1Bench or general state-of-the-art claim.", "We make no general state-of-the-art claim.")


def put(text, new, before):
    """Replace the marked block, else insert it before the first line starting with `before` (else append)."""
    if START in text:
        i, j = text.index(START), text.index(END) + len(END)
        return text[:i] + new + text[j:]
    k = text.find("\n" + before) if before else -1
    return text.rstrip("\n") + "\n\n" + new + "\n" if k < 0 else text[: k + 1] + new + "\n\n" + text[k + 1 :]


TEXT_NOTE = (
    "Measured with [SelfJev-4B Vision](https://huggingface.co/Jwuthrich/selfjev-4b-vision), the default release, which "
    "continues this adapter; on text the two score within half a point of each other (Text Decisions 96.1 vs 95.7)."
)
HF = {  # repo -> (anchor heading to insert before, note)
    "Jwuthrich/selfjev-4b": ("## Public datasets", TEXT_NOTE),
    "Jwuthrich/selfjev-4b-merged": ("## Public datasets", TEXT_NOTE),
    "Jwuthrich/selfjev-4b-vision": ("## Training", ""),
    "Jwuthrich/selfjev-4b-vision-merged": ("", ""),
    "datasets/Jwuthrich/selfjev-decision-bench": ("## How the questions were built", ""),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--push-hf", action="store_true", help="update the README of every Hugging Face repo in HF")
    a = ap.parse_args()
    (ROOT / "reports/competitors/card_section.md").write_text(block(note=TEXT_NOTE) + "\n")  # {{COMPARISON}} of the text card
    (ROOT / "docs/comparison.md").write_text(block("# Compared with open Jev-like models") + "\n")
    (ROOT / "website/content/comparison.md").write_text(BODY.format(table1=public_table()[0], gh=GH) + "\n")  # no HTML markers
    for path, before in (("README.md", "## Get the weights"), ("weights/selfjev_4b_vision/README.md", "## Training")):
        p = ROOT / path
        p.write_text(put(p.read_text(), block(), before))
    p = ROOT / "weights/selfjev_4b/README.md"
    p.write_text(fix_stale(put(p.read_text(), block(note=TEXT_NOTE), "## Public datasets")))
    p = ROOT / "scripts/docs/model_card.template.md"
    p.write_text(fix_stale(p.read_text()))
    print("local files written")
    if not a.push_hf:
        return
    from huggingface_hub import HfApi, hf_hub_download

    api = HfApi()
    for repo, (before, note) in HF.items():
        kind, rid = ("dataset", repo.split("/", 1)[1]) if repo.startswith("datasets/") else ("model", repo)
        old = Path(hf_hub_download(rid, "README.md", repo_type=kind, force_download=True)).read_text()
        new = fix_stale(put(old, block(note=note), before))
        if new == old:
            print(f"{repo}: unchanged")
            continue
        info = api.upload_file(path_or_fileobj=new.encode(), path_in_repo="README.md", repo_id=rid, repo_type=kind,
                               commit_message="Card: comparison with open Jev-like models (2026-09-30)")  # fmt: skip
        print(f"{repo}: {info.oid if hasattr(info, 'oid') else info}")


if __name__ == "__main__":
    main()
