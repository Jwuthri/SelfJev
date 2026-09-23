"""Pick the default prompt mapping using VALIDATION splits only; writes reports/prompt_selection.md.

Criterion (threshold- and temperature-free, since both are fitted later): per family, the mean over its
question types of binary AUROC / multiclass accuracy / multilabel label-AUROC; then the macro mean over families.
usage: uv run python scripts/select_prompt.py [--model M --revision R --dtype D --out reports/prompt_selection] data/hf.jsonl data/eval.jsonl
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from personal_jev.evaluate import run  # noqa: E402
from personal_jev.formatting import PROMPTS, prompt_sha  # noqa: E402
from personal_jev.model import MODEL_ID, MODEL_REVISION, Scorer  # noqa: E402

PRIMARY = {"binary": "auroc", "multiclass": "accuracy", "multilabel": "label_auroc"}


def family_score(m):
    vals = [m[t][k] for t, k in PRIMARY.items() if t in m and m[t][k] is not None]
    return sum(vals) / len(vals) if vals else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--model", default=MODEL_ID)
    ap.add_argument("--revision", default=MODEL_REVISION)
    ap.add_argument("--dtype", default="float32")
    ap.add_argument("--out", default="reports/prompt_selection", help="per-prompt reports go here; summary to <out>.md")
    a = ap.parse_args()
    files, out = a.files, ROOT / a.out
    scorer = Scorer(model_id=a.model, revision=a.revision, dtype=a.dtype)
    rows = {}
    for p in PROMPTS:
        rep = run(scorer, files, ["validation"], out_dir=out / p, prompt=p)
        fams = {f: family_score(m) for f, m in rep["by_family"].items()}
        rows[p] = (sum(fams.values()) / len(fams), fams, rep["metrics"]["question_accuracy"], rep["meta"]["n"])
        print(p, round(rows[p][0], 4), flush=True)
    best = max(rows, key=lambda p: rows[p][0])
    fams = sorted(next(iter(rows.values()))[1])
    lines = [f"# Prompt selection (validation splits only): `{a.model}`", "", f"data: {', '.join(map(str, files))}; n={rows[best][3]} questions; "
             "criterion: macro over families of (binary AUROC | multiclass accuracy | multilabel label-AUROC)", "",
             f"**Selected: `{best}`** ({prompt_sha(best)})", "", "| prompt | sha | macro score | question acc (t=0.5) | " + " | ".join(fams) + " |",
             "|---|---|---|---|" + "---|" * len(fams)]
    for p, (score, fs, qa, _) in sorted(rows.items(), key=lambda kv: -kv[1][0]):
        lines.append(f"| {p} | {prompt_sha(p)} | {score:.3f} | {100 * qa:.1f} | " + " | ".join(f"{fs[f]:.3f}" for f in fams) + " |")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".md").write_text("\n".join(lines) + "\n")
    (out / "selected.json").write_text(json.dumps({"model": a.model, "revision": a.revision, "selected": best,
                                                    "scores": {k: v[0] for k, v in rows.items()}}, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
