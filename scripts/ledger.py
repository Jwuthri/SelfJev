"""Results ledger: every test-split report under reports/ (+ Jev) in one table, sorted by eval2 then by the dev
benchmark, written into docs/experiments.md between the ledger markers. Run after every eval:  uv run python scripts/ledger.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/experiments.md"
START, END = "<!-- ledger:start -->", "<!-- ledger:end -->"


def pct(x):
    return "—" if x is None else f"{100 * x:.1f}"


def rows():
    paths = sorted(ROOT.glob("reports/**/test/report.json")) \
        + [q for q in sorted(ROOT.glob("reports/external/full/*/report.json")) if not q.parent.name.startswith("ours-")]
    for p in paths:  # ours-* under external/ are the 0.6B baseline/lora_pilot again; eval2 column from reports/<run>/eval2 when scored
        r = json.loads(p.read_text())
        m, meta = r["metrics"], r["meta"]
        if int(meta.get("n", len(r["predictions"]))) != 3471:
            continue  # not the shared 3,471-question test set
        run = str(p.parent.parent.relative_to(ROOT / "reports")).replace("external/full", "external")
        auth = [q["correct"] for q in r["predictions"] if q["family"].startswith("eval_")]
        adapter = meta.get("adapter") or ""
        tm = None
        if adapter and adapter != "None":
            cand = ROOT / re.sub(r"/(adapter|checkpoint)$", "", adapter) / "train_meta.json"
            tm = json.loads(cand.read_text()) if cand.exists() else None
        train_n = (tm.get("data", {}).get("train_questions", tm.get("train_questions"))) if tm else None
        trained = "—" if train_n is None else f"{train_n:,} q / {tm.get('steps', '?')} steps"
        base = meta.get("model", "?").replace("Qwen/", "")
        arch = meta.get("architecture") or ("external API" if run.startswith("external") else f"stock pairs ({meta.get('prompt')})")
        e2p = p.parent.parent / "eval2/report.json" if not run.startswith("external") else ROOT / "reports/external/eval2" / p.parent.name / "report.json"
        e2_acc = json.loads(e2p.read_text())["metrics"]["question_accuracy"] if e2p.exists() else None
        e2 = pct(e2_acc)
        yield ((-1.0 if e2_acc is None else e2_acc, m["question_accuracy"]), run, base, arch, trained, e2, pct(m["question_accuracy"]), pct(m["binary"]["accuracy"]),
               f"{m['binary']['auroc']:.3f}", pct(m["multiclass"]["accuracy"]), pct(m["multilabel"]["exact_match"]),
               pct(sum(auth) / len(auth)), f"[report](../{p.with_suffix('.md').relative_to(ROOT)})", adapter if tm else "—")


table = ["| run | base | architecture | trained on | **eval2 acc %** (target task, 1,991 q) | dev benchmark acc % (old test, 3,471 q) | binary acc % | binary AUROC | multiclass acc % | multilabel EM % | authored eval_* acc % (n=171) | report | weights |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
table += ["| " + " | ".join(r[1:]) + " |" for r in sorted(rows(), reverse=True)]
body = "\n".join(table)
doc = DOC.read_text()
DOC.write_text(doc[:doc.index(START) + len(START)] + "\n" + body + "\n" + doc[doc.index(END):])
print(f"{len(table) - 2} rows written to {DOC.relative_to(ROOT)}")
