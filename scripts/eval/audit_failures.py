"""Audit the test questions our best model or Jev gets wrong: blind relabel by Claude Opus 5.5, then sort each failure
into "label right, model wrong", "label probably wrong" or "ambiguous", and look for patterns in the real errors.

  zsh -ic 'uv run python scripts/eval/audit_failures.py relabel --limit 40'   # PAID (user OK): pilot, then without --limit
  uv run python scripts/eval/audit_failures.py report                         # free: reports/audit_2026-09-26/AUDIT.md

- Failures: eval2 and the dev benchmark (hf + eval test) where `qwen35_4b_tree` or Jev is wrong; eval_llm where Jev is wrong
  (our models are not scored on it yet). Ours from reports/qwen35_4b_tree/{eval2,test}/report.json, Jev from the `jev`
  field of data/all.jsonl.gz.
- Opus sees the text, the question and the candidates only (never the target nor any model answer): the protocol and
  policy of our blind judges (selfjev.data.providers: run_sync, llm_request), reasoning effort medium, one call
  per text with its failed questions. Cached, so reruns never pay twice.
- Opus 5.5 wrote a third of eval2 and eval_llm: on those rows it may side with its own label. Label errors are only
  proposed (errata list for a human), never written into the frozen test sets.
"""

import argparse
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path

from selfjev.data.providers import run_sync

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports/audit_2026-09-26"
MODEL = "anthropic/claude-opus-5.5"
OURS = {"eval2": "reports/qwen35_4b_tree/eval2/report.json", "dev": "reports/qwen35_4b_tree/test/report.json"}
norm = lambda t: sorted(t) if isinstance(t, list) else t


def failures():
    with gzip.open(ROOT / "data/all.jsonl.gz", "rt") as f:
        rows = [json.loads(line) for line in f]
    ours = {}
    for p in OURS.values():
        ours |= {r["id"]: r["selected"] for r in json.loads((ROOT / p).read_text())["predictions"]}
    out = []
    for r in rows:
        test = (
            "eval2"
            if r["dataset"] == "eval2"
            else "dev"
            if r["dataset"] in ("hf", "eval") and r["split"] == "test"
            else "eval_llm"
            if r["dataset"] == "eval_llm"
            else None
        )
        if not test:
            continue
        o, j = ours.get(r["id"]), (r.get("jev") or {}).get("answer")
        ow = o is not None and norm(o) != norm(r["target"])
        jw = "jev" in r and not r["jev"]["correct"]
        if ow or jw:
            out.append(r | {"test": test, "ours": o, "jev_answer": j, "ours_wrong": ow, "jev_wrong": jw})
    return out


def relabel(a):
    fails = failures()
    groups = defaultdict(list)
    for r in fails:
        groups[(r["dataset"], r["source_id"])].append(r)
    keys = list(groups)[: a.limit] if a.limit else list(groups)
    g = {f"{d}:{s}": ({"state": groups[(d, s)][0]["state"]}, groups[(d, s)]) for d, s in keys}
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "failures.jsonl", "w") as f:
        for r in fails:
            f.write(
                json.dumps(
                    {k: r[k] for k in ("id", "test", "dataset", "family", "target", "ours", "jev_answer", "ours_wrong", "jev_wrong")}
                )
                + "\n"
            )
    print(f"{len(fails)} failed questions in {len(groups)} texts; relabelling {len(g)} texts", flush=True)
    run_sync(g, OUT, MODEL, effort="medium", workers=8)


def report(a):
    fails = {r["id"]: r for r in failures()}
    with open(OUT / "answers_claude-opus-5.5.jsonl") as f:
        opus = {r["id"]: r for r in map(json.loads, f)}
    verdict = {}
    for i, r in fails.items():
        if i not in opus:
            continue
        o = norm(opus[i]["answer"])
        wrong_answers = [norm(x) for x, w in ((r["ours"], r["ours_wrong"]), (r["jev_answer"], r["jev_wrong"])) if w and x is not None]
        verdict[i] = (
            "label right, model wrong"
            if o == norm(r["target"])
            else "label probably wrong (Opus = a model)"
            if o in wrong_answers
            else "ambiguous (Opus gives a third answer)"
        )
    lines = [
        "# Test-set failure audit (2026-09-26)",
        "",
        f"Blind relabel by {MODEL} (effort medium) of every test question our best model (`qwen35_4b_tree`) or Jev gets wrong "
        "(eval_llm: Jev only). Opus never saw the target or any model answer. Opus wrote a third of eval2 and eval_llm, so on those "
        "rows it may side with its own label. Proposed label errors are for human review; the frozen files are unchanged.",
        "",
    ]
    for test in ("eval2", "dev", "eval_llm"):
        ids = [i for i in verdict if fails[i]["test"] == test]
        if not ids:
            continue
        lines += [
            f"## {test}: {len(ids)} failed questions relabelled",
            "",
            "| who is wrong | label right, model wrong | label probably wrong | ambiguous |",
            "|---|---|---|---|",
        ]
        for who, sel in (
            ("ours only", lambda r: r["ours_wrong"] and not r["jev_wrong"]),
            ("Jev only", lambda r: r["jev_wrong"] and not r["ours_wrong"]),
            ("both", lambda r: r["ours_wrong"] and r["jev_wrong"]),
            ("all", lambda r: True),
        ):
            c = Counter(verdict[i] for i in ids if sel(fails[i]))
            lines.append(
                f"| {who} | {c['label right, model wrong']} | {c['label probably wrong (Opus = a model)']} | "
                f"{c['ambiguous (Opus gives a third answer)']} |"
            )
        real = [fails[i] for i in ids if verdict[i] == "label right, model wrong"]
        for key, name in ((lambda r: r["question"]["type"], "type"), (lambda r: r["family"], "family"), (lambda r: None, "trap")):
            c = Counter()
            for r in real:
                for k in (r.get("hard_cases") or ["(none)"]) if name == "trap" else [key(r)]:
                    c[(k, "ours" if r["ours_wrong"] else "", "jev" if r["jev_wrong"] else "")] += 1
            agg = defaultdict(lambda: [0, 0])
            for (k, o, j), n in c.items():
                agg[k][0] += n if o else 0
                agg[k][1] += n if j else 0
            top = sorted(agg.items(), key=lambda kv: -max(kv[1]))[:12]
            lines += ["", f"Real errors (label confirmed) by {name}: " + ", ".join(f"{k} ours {v[0]} / Jev {v[1]}" for k, v in top)]
        lines.append("")
    errata = [i for i in verdict if verdict[i].startswith("label probably wrong")]
    lines += [f"## Proposed errata ({len(errata)} questions): `errata_candidates.jsonl`", ""]
    with open(OUT / "errata_candidates.jsonl", "w") as f:
        for i in errata:
            r = fails[i]
            f.write(
                json.dumps(
                    {
                        "id": i,
                        "test": r["test"],
                        "target": r["target"],
                        "opus": opus[i]["answer"],
                        "opus_confidence": opus[i]["confidence"],
                        "ours": r["ours"],
                        "jev": r["jev_answer"],
                        "instruction": r["question"]["instruction"],
                        "candidates": r["question"].get("candidates"),
                        "state": r["state"][:3000],
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
    with open(OUT / "verdicts.jsonl", "w") as f:
        for i, v in verdict.items():
            f.write(json.dumps({"id": i, "test": fails[i]["test"], "verdict": v, "opus": opus[i]["answer"]}) + "\n")
    (OUT / "AUDIT.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["relabel", "report"])
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    (relabel if a.action == "relabel" else report)(a)
