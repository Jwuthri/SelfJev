"""Head-to-head on the SAME test questions: our models vs Jev (OpenRouter decisions API) vs a big LLM (chat).

- Subset: every eval.jsonl test question + N sampled per hf.jsonl test family (seeded).
- Budget: spend = max(OpenRouter account usage delta, summed per-call cost incl. BYOK upstream cost), re-checked
  while running; the run stops before the spend passes --budget. Raw responses are cached in reports/external/cache/, so reruns never
  pay twice. The API key comes from OPENROUTER_API_KEY and is never printed.
- Metrics use the same evaluator as our own reports, on the questions every model answered.
- Data sent: synthetic eval texts and public-dataset texts only (no private data).

usage: zsh -ic 'uv run python scripts/eval/compare_external.py --budget 20'
       zsh -ic 'uv run python scripts/eval/compare_external.py --data data/eval2.jsonl --ours tree_4b/eval2 --only jev \
         --tag eval2 --budget 2'
"""

import argparse
import concurrent.futures as cf
import hashlib
import json
import math
import random
import threading
import time
import urllib.error
from collections import defaultdict
from pathlib import Path

from selfjev.data import load, sha256_file, write_jsonl
from selfjev.data.providers import account_usage, call_cost, http, jev_request, llm_request
from selfjev.evaluation.evaluate import breakdowns, compare, evaluate_predictions, markdown
from selfjev.evaluation.stats import mcnemar

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports/external"
lock = threading.Lock()


# ---------------------------------------------------------------------------------------------- answers -> our rows


def to_row(ex, ours, kind, ans):
    """ours: our own prediction row for this id (gives state_tokens and field layout)."""
    q = ex["question"]
    row = {k: ours[k] for k in ("id", "source_id", "family", "split", "target", "paraphrase_group", "hard_cases", "state_tokens")}
    row |= {"type": q["type"], "calibration": "external", "candidate_ids": [c["id"] for c in q.get("candidates", [])]}
    if q["type"] == "binary":
        p = float(ans[0]["noul"] if kind == "jev" else ans[0]["p_yes"])
        row |= {"p_yes": p, "probabilities": [p], "selected": p >= 0.5}
    elif q["type"] == "multiclass":
        raw = ans[0]["probabilities"] if kind == "jev" else ans[0]
        ps = [max(float(raw.get(c, 0.0)), 0.0) for c in row["candidate_ids"]]
        z = sum(ps) or 1.0
        ps = [p / z for p in ps]
        row |= {"probabilities": ps, "selected": row["candidate_ids"][max(range(len(ps)), key=ps.__getitem__)]}
    else:
        ps = [float(a["noul"]) for a in ans] if kind == "jev" else [float(ans[0][c]) for c in row["candidate_ids"]]
        row |= {"probabilities": ps, "selected": [c for c, p in zip(row["candidate_ids"], ps) if p >= 0.5]}
    row["scores"] = [math.log(max(p, 1e-9) / max(1 - p, 1e-9)) for p in row["probabilities"]]
    row["correct"] = set(row["selected"]) == set(row["target"]) if q["type"] == "multilabel" else row["selected"] == row["target"]
    return row


def run_provider(name, kind, model, groups, ours, budget_left, workers, effort):
    cache_path = OUT / "cache" / f"{name}.jsonl"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache = {}
    if cache_path.exists():
        with open(cache_path) as f:
            cache = {c["key"]: c for c in map(json.loads, f)}
    rows, errors, start = {}, [], account_usage()
    stop, paid = threading.Event(), [0.0]  # paid: real cost of the calls made in this run (incl. BYOK upstream)

    def one(sid):
        state, exs = groups[sid]
        body, keys = jev_request(model, state, exs) if kind == "jev" else llm_request(model, state, exs, effort)
        key = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
        if key in cache:
            resp = cache[key]["response"]
        else:
            if stop.is_set():
                return
            try:
                resp = http("POST", "/alpha/decisions" if kind == "jev" else "/v1/chat/completions", body)
            except urllib.error.HTTPError as e:
                errors.append((sid, e.code, e.read()[:300].decode(errors="replace")))
                return
            except Exception as e:  # network, timeout
                errors.append((sid, None, repr(e)[:300]))
                return
            with lock:
                paid[0] += call_cost(resp)
                cache[key] = {"key": key, "sid": sid, "response": resp, "t": time.time()}
                with open(cache_path, "a") as f:
                    f.write(json.dumps(cache[key]) + "\n")
        try:
            answers = resp["answers"] if kind == "jev" else json.loads(resp["choices"][0]["message"]["content"])
            for (eid, ks), ex in zip(keys, exs):
                rows[eid] = to_row(ex, ours[eid], kind, [answers[k] for k in ks])
        except Exception as e:
            errors.append((sid, "parse", repr(e)[:300]))

    sids = list(groups)
    with cf.ThreadPoolExecutor(workers) as pool:
        futs = []
        for i, sid in enumerate(sids):
            futs.append(pool.submit(one, sid))
            if i % 25 == 24:  # re-check real spend as we go
                cf.wait(futs)
                spent = max(account_usage() - start, paid[0])
                print(f"  {name}: {i + 1}/{len(sids)} states, spent ${spent:.2f}, errors {len(errors)}", flush=True)
                if spent >= budget_left:
                    stop.set()
                    print(f"  {name}: budget reached, stopping", flush=True)
                    break
    return rows, errors, max(account_usage() - start, paid[0])


def report(name, rows, meta_extra, tag):
    rows = list(rows)
    rep = {
        "meta": {
            "model": name,
            "revision": "-",
            "adapter": None,
            "adapter_sha256": None,
            "prompt": name,
            "prompt_sha": "-",
            "calibration": None,
            "device": "-",
            "dtype": "-",
            "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "wall_s": 0.0,
            "n": len(rows),
            "splits": ["test"],
            **meta_extra,
        },
        "metrics": evaluate_predictions(rows),
        **breakdowns(rows),
        "predictions": rows,
    }
    d = OUT / tag / name.replace("/", "_").replace("~", "")
    d.mkdir(parents=True, exist_ok=True)
    (d / "report.json").write_text(json.dumps(rep, indent=1))
    (d / "report.md").write_text(markdown(rep))
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=float, default=20.0, help="max USD for the whole run (all providers)")
    ap.add_argument("--jev", default="~typesafe/jev-latest")
    ap.add_argument("--llm", default="openai/gpt-6-astra")
    ap.add_argument("--effort", default="low", help="LLM reasoning effort")
    ap.add_argument("--per-hf-family", type=int, default=20)
    ap.add_argument("--limit-states", type=int, help="smoke test: only the first N states")
    ap.add_argument("--only", choices=["jev", "llm"])
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--tag", default="subset", help="output folder under reports/external/")
    ap.add_argument("--data", help="score every test question of this file instead of the default subset (e.g. data/eval2.jsonl)")
    ap.add_argument("--ours", help="with --data: our report dir under reports/ on the same file (row layout + paired test)")
    a = ap.parse_args()

    if a.data:
        ours = {"LoRA": {r["id"]: r for r in json.loads((ROOT / f"reports/{a.ours}/report.json").read_text())["predictions"]}}
        subset = load(ROOT / a.data, {"test"})
    else:
        ours = {
            n: {r["id"]: r for r in json.loads((ROOT / f"reports/{p}/report.json").read_text())["predictions"]}
            for n, p in (("base", "baseline/test"), ("LoRA", "lora_pilot/test"))
        }
        rng = random.Random(7)
        ev = load(ROOT / "data/eval.jsonl", {"test"})
        hf_by_fam = defaultdict(list)
        for ex in load(ROOT / "data/hf.jsonl", {"test"}):
            hf_by_fam[ex["family"]].append(ex)
        subset = ev + [ex for f in sorted(hf_by_fam) for ex in rng.sample(hf_by_fam[f], min(a.per_hf_family, len(hf_by_fam[f])))]
    groups = {}
    for ex in subset:
        groups.setdefault(ex["source_id"], (ex["state"], []))[1].append(ex)
    if a.limit_states:
        groups = dict(list(groups.items())[: a.limit_states])
    subset = [ex for _, exs in groups.values() for ex in exs]
    (OUT / a.tag).mkdir(parents=True, exist_ok=True)
    write_jsonl(OUT / a.tag / "subset.jsonl", subset)
    print(f"subset: {len(subset)} questions in {len(groups)} states", flush=True)

    total_start, results = account_usage(), {}
    for kind, model in (("jev", a.jev), ("llm", a.llm)):
        if a.only and a.only != kind:
            continue
        left = a.budget - (account_usage() - total_start)
        print(f"{model}: budget left ${left:.2f}", flush=True)
        rows, errors, spent = run_provider(
            model.replace("/", "_").replace("~", ""), kind, model, groups, ours["LoRA"], left, a.workers, a.effort
        )
        results[model] = (rows, errors, spent)
        print(f"{model}: answered {len(rows)}/{len(subset)} questions, errors {len(errors)}, spent ${spent:.2f}", flush=True)
        for e in errors[:5]:
            print("   error:", e, flush=True)

    answered = set.intersection(*[set(r[0]) for r in results.values()]) if results else set(ours["LoRA"])
    ids = [ex["id"] for ex in subset if ex["id"] in answered]
    data_meta = {
        "data": [{"path": f"reports/external/{a.tag}/subset.jsonl", "sha256": sha256_file(OUT / a.tag / "subset.jsonl")}],
        "note": f"{len(ids)} questions answered by every model",
    }
    reps = {n: report(f"ours-{n}", [ours[n][i] for i in ids], data_meta, a.tag) for n in ours}
    for model, (rows, errors, spent) in results.items():
        reps[model] = report(model, [rows[i] for i in ids], data_meta | {"spent_usd": spent, "errors": len(errors)}, a.tag)
    names = list(reps)
    md = compare([reps[n] for n in names], names)
    lines = [
        "",
        "## Paired tests vs our LoRA model (exact McNemar on the same questions)",
        "",
        "| other | n | LoRA only right | other only right | p |",
        "|---|---|---|---|---|",
    ]
    lora = {r["id"]: r["correct"] for r in reps["LoRA"]["predictions"]}
    for n in names:
        if n != "LoRA":
            other = {r["id"]: r["correct"] for r in reps[n]["predictions"]}
            oa, ob, p = mcnemar(lora, other)
            lines.append(f"| {n} | {len(lora)} | {oa} | {ob} | {p:.2g} |")
    spend = {m: round(r[2], 4) for m, r in results.items()}
    (OUT / a.tag / "comparison.md").write_text(
        md + "\n".join(lines) + f"\n\nSpend (USD, from OpenRouter account usage): {spend}; total ${account_usage() - total_start:.2f}\n"
    )
    print((OUT / a.tag / "comparison.md").read_text())


if __name__ == "__main__":
    main()
