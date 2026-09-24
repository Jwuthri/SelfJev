"""Learning-curve tables from reports/curve/*/test/report.json (+ runs/lora_4b as the 100% / +0 reference).

usage: uv run python scripts/summarize_curve.py > reports/curve/summary.md
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "reports/lora_4b/test/report.json"  # Qwen3-Reranker-4B + LoRA, 10,112 questions, 1 epoch


def report(name):
    p = ROOT / "reports/curve" / name / "test/report.json"
    return json.loads(p.read_text()) if p.exists() else None


def pct(x):
    return "—" if x is None else f"{100 * x:.1f}"


def row(r, fam=None):
    if r is None:
        return ["—"] * 5
    m = r["metrics"] if fam is None else r["by_family"].get(fam, {})
    if fam:
        return [pct(m.get("question_accuracy"))]
    return [pct(m["question_accuracy"]), pct(m["binary"]["accuracy"]), f"{m['binary']['auroc']:.3f}",
            pct(m["multiclass"]["accuracy"]), pct(m["multilabel"]["exact_match"])]


def mcnemar(a, b):
    ids = a.keys() & b.keys()
    oa, ob = sum(a[i] and not b[i] for i in ids), sum(b[i] and not a[i] for i in ids)
    n, k = oa + ob, min(oa, ob)
    return oa, ob, (min(1.0, 2 * sum(math.comb(n, j) for j in range(k + 1)) / 2 ** n) if n else 1.0)


def correct(r):
    return {p["id"]: p["correct"] for p in r["predictions"]}


ref = json.loads(REF.read_text()) if REF.exists() else None
H = "| run | train questions | epochs | question acc % | binary acc % | binary AUROC | multiclass acc % | multilabel EM % |\n|---|---|---|---|---|---|---|---|"
print("# Learning curves on Qwen3-Reranker-4B (test split, 3,471 questions)\n")
print("Same recipe as `runs/lora_4b` (LoRA r=16 on q/k/v/o, lr 2e-4, bf16, prompt answer-v1); one A10G per run.\n")
print("## Volume: nested subsets of the same 10,112-question mix\n")
print(H)
for name, n, ep in [("vol25_e1", 2528, 1), ("vol50_e1", 5056, 1), ("lora_4b (reference)", 10112, 1),
                    ("vol25_e2", 2528, 2), ("vol50_e2", 5056, 2), ("vol100_e2", 10112, 2)]:
    r = ref if name.startswith("lora_4b") else report(name)
    print(f"| {name} | {n:,} | {ep} | " + " | ".join(row(r)) + " |")
print("\n## Per-task: BoolQ training questions added to the mix (BoolQ test is otherwise never trained on)\n")
print("| run | BoolQ train questions added | BoolQ test acc % | overall question acc % | binary acc % | binary AUROC | Jev on BoolQ |\n|---|---|---|---|---|---|---|")
jev = json.loads((ROOT / "reports/external/full/typesafe_jev-latest/report.json").read_text())
jev_boolq = pct(jev["by_family"]["heldout_boolq"]["question_accuracy"])
for name, n in [("lora_4b (reference)", 0), ("boolq_100", 100), ("boolq_300", 300), ("boolq_1000", 1000), ("boolq_3000", 3000)]:
    r = ref if name.startswith("lora_4b") else report(name)
    cells = ["—"] * 4 if r is None else [pct(r["by_family"]["heldout_boolq"]["question_accuracy"]), *row(r)[:3]]
    print(f"| {name} | {n:,} | " + " | ".join(cells) + f" | {jev_boolq} |")
print("\n## Base model: Qwen3-4B-Instruct-2507 vs Qwen3-Reranker-4B, same pair format and LoRA recipe\n")
print(H)
for name, label, n, ep in [("baseline_4b", "Reranker-4B zero-shot", 0, 0), ("instruct_zero", "Instruct-4B zero-shot", 0, 0),
                           ("lora_4b (reference)", "Reranker-4B + LoRA", 10112, 1), ("instruct_lora", "Instruct-4B + LoRA", 10112, 1)]:
    if name == "baseline_4b":
        p = ROOT / "reports/baseline_4b/test/report.json"
        r = json.loads(p.read_text()) if p.exists() else None
    else:
        r = ref if name.startswith("lora_4b") else report(name)
    print(f"| {label} | {n:,} | {ep} | " + " | ".join(row(r)) + " |")
sel = ROOT / "reports/curve/instruct_prompt_selection/selected.json"
if sel.exists():
    s = json.loads(sel.read_text())
    print(f"\nInstruct prompt selected on validation: `{s['selected']}` ({', '.join(f'{k} {v:.3f}' for k, v in s['scores'].items())}).")
TREF = ROOT / "reports/tree_4b/test/report.json"
tref = json.loads(TREF.read_text()) if TREF.exists() else None
print("\n## Tree scorer: LoRA capacity (same data and recipe as `runs/tree_4b`, 84 steps)\n")
E2REF = ROOT / "reports/tree_4b/eval2/report.json"
e2ref = json.loads(E2REF.read_text()) if E2REF.exists() else None
print("| run | LoRA | trainable params | validation acc % | old test acc % | binary acc % | binary AUROC | multiclass acc % | multilabel EM % | vs tree_4b on old test: run only / ref only / p | eval2 acc % | vs tree_4b on eval2: run only / ref only / p |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
for name, label, rdir, tdir in [("tree_4b (reference)", "r=16 on q/k/v/o", "reports/tree_4b", "runs/tree_4b"),
                                ("tree_4b_r64", "r=64 on q/k/v/o", "reports/curve/tree_4b_r64", "runs/curve/tree_4b_r64"),
                                ("tree_4b_mlp", "r=16 on q/k/v/o + gate/up/down", "reports/curve/tree_4b_mlp", "runs/curve/tree_4b_mlp")]:
    rp, tp = ROOT / rdir / "test/report.json", ROOT / tdir / "train_meta.json"
    if not (rp.exists() and tp.exists()):
        continue
    r, t = json.loads(rp.read_text()), json.loads(tp.read_text())
    ob, oa, p = mcnemar(correct(r), correct(tref)) if tref else (0, 0, 1.0)
    e2p = ROOT / rdir / "eval2/report.json"
    e2 = "— | — |"
    if e2p.exists() and e2ref:
        r2 = json.loads(e2p.read_text()); ob2, oa2, p2 = mcnemar(correct(r2), correct(e2ref))
        e2 = f"{pct(r2['metrics']['question_accuracy'])} | {ob2} / {oa2} / {p2:.2g} |"
    print(f"| {name} | {label} | {t['lora']['trainable_params']:,} | {pct(t['best']['question_accuracy'])} | " + " | ".join(row(r)) + f" | {ob} / {oa} / {p:.2g} | " + e2)
print("\nValidation = the trainer's own validation mix (in-distribution + authored families); the old test adds the six held-out public families;"
      " eval2 = the frozen 1,991-question target-task set (`data/eval2.jsonl`, `reports/eval2/summary.md`). The old test shows no capacity effect,"
      " eval2 does, in the direction validation predicted.")
R2B = ROOT / "reports/tree_4b_r2b"
if (R2B / "eval2/report.json").exists():
    r2b_e2, r2b_t = json.loads((R2B / "eval2/report.json").read_text()), json.loads((R2B / "test/report.json").read_text())
    jev_e2 = json.loads((ROOT / "reports/external/eval2/typesafe_jev-latest/report.json").read_text())
    print("\n## Tree scorer: round-2b data combined with more LoRA capacity (recipe of `runs/tree_4b_r2b`: + verified hard cases, 8K training length)\n")
    print("| run | LoRA | trainable params | validation acc % | eval2 acc % | eval2 binary | eval2 multiclass | eval2 multilabel EM | vs tree_4b_r2b on eval2: run only / ref only / p | vs Jev on eval2 | old test acc % | vs tree_4b_r2b on old test |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for name, label, rdir, tdir in [("tree_4b_r2b (reference)", "r=16 on q/k/v/o", "reports/tree_4b_r2b", "runs/tree_4b_r2b"),
                                    ("tree_4b_r2b_r64", "r=64 on q/k/v/o", "reports/curve/tree_4b_r2b_r64", "runs/curve/tree_4b_r2b_r64"),
                                    ("tree_4b_r2b_r64_mlp", "r=64 on q/k/v/o + gate/up/down", "reports/curve/tree_4b_r2b_r64_mlp", "runs/curve/tree_4b_r2b_r64_mlp")]:
        e2p, tp, mp = ROOT / rdir / "eval2/report.json", ROOT / rdir / "test/report.json", ROOT / tdir / "train_meta.json"
        if not (e2p.exists() and tp.exists() and mp.exists()):
            continue
        e2, te, t = json.loads(e2p.read_text()), json.loads(tp.read_text()), json.loads(mp.read_text())
        m = e2["metrics"]; a = mcnemar(correct(e2), correct(r2b_e2)); j = mcnemar(correct(e2), correct(jev_e2)); o = mcnemar(correct(te), correct(r2b_t))
        print(f"| {name} | {label} | {t['lora']['trainable_params']:,} | {pct(t['best']['question_accuracy'])} | {pct(m['question_accuracy'])} | {pct(m['binary']['accuracy'])} | {pct(m['multiclass']['accuracy'])} | {pct(m['multilabel']['exact_match'])} | {a[0]} / {a[1]} / {a[2]:.2g} | {j[0]} / {j[1]} / {j[2]:.2g} | {pct(te['metrics']['question_accuracy'])} | {o[0]} / {o[1]} / {o[2]:.2g} |")
    print("\nJev on eval2: " + pct(jev_e2["metrics"]["question_accuracy"]) + "%. The two combined runs trained on A10Gs with max_batch_tokens 8192 × grad_accum 4 (same 32K-token effective batch as the reference's 16384 × 2).")
print("\n## Paired McNemar vs the reference (questions only one of the two gets right)\n")
if ref:
    rc = correct(ref)
    print("| run | run only | reference only | p |\n|---|---|---|---|")
    for name in ["vol25_e1", "vol50_e1", "vol25_e2", "vol50_e2", "vol100_e2", "boolq_100", "boolq_300", "boolq_1000", "boolq_3000", "instruct_lora"]:
        r = report(name)
        if r:
            ob, oa, p = mcnemar(correct(r), rc)
            print(f"| {name} | {ob} | {oa} | {p:.2g} |")
