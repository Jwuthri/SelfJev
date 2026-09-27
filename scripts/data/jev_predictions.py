"""Jev's prediction for every question of our datasets -> data/jev/predictions.jsonl (tracked), joined into
data/all.jsonl.gz as the `jev` field by scripts/data/build_all.py.

  uv run python scripts/data/jev_predictions.py                                  # free: reuse cached Jev responses, estimate the rest
  zsh -ic 'uv run python scripts/data/jev_predictions.py --call --budget 3'     # PAID (user OK first): call Jev for what is missing
  uv run python scripts/data/build_all.py                                        # then rebuild all.jsonl.gz with the jev field

- One request per text with all its questions, the mapping of every Jev comparison (selfjev.data.providers.jev_request):
  binary -> noul = P(yes); multiclass -> choice probabilities; multilabel -> one noul per candidate.
- Free reuse: the caches of earlier runs (dev benchmark, round-2 judge, eval2, eval_llm) are keyed by the exact request,
  so each text is tried with its kept questions and with its full raw question list (how the judge runs grouped them).
  New responses go to data/jev/cache.jsonl, so nothing is ever paid twice.
- Row: {id, dataset, request, model, type, p_yes | probs, answer, confidence, correct}. `request` is a hash of the text
  and question: build_all.py drops a prediction whose text or question changed since. `model` is the Jev version that
  answered. `correct` compares with the authored `target`.
- These are Jev's outputs, not labels: they never replace `target`, and test rows are for reporting only.
"""

import argparse
import concurrent.futures as cf
import hashlib
import json
import threading
import time
from collections import Counter, defaultdict
from pathlib import Path

from selfjev.data import expand_source, load, read_jsonl
from selfjev.data.catalog import datasets, request_sha
from selfjev.data.providers import call_cost, http, jev_request

ROOT = Path(__file__).resolve().parents[2]
MODEL = "~typesafe/jev-latest"
OUT = ROOT / "data/jev"
CACHES = [
    "reports/external/cache/typesafe_jev-latest.jsonl",
    "data/hardcases/review/jev_cache.jsonl",
    "data/eval2/review/jev_cache.jsonl",
    "data/eval_llm/review/jev_cache.jsonl",
    "data/jev/cache.jsonl",
]
RAW = ["data/hardcases/raw", "data/eval2/raw", "data/eval_llm/raw"]  # sources the judge runs sent to Jev whole
norm = lambda t: sorted(t) if isinstance(t, list) else t


def key_of(body):
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]


def extract(resp, keys, exs, want, dataset):
    """One prediction row per question id in `want`."""
    out, ans = [], resp["answers"]
    for (eid, ks), ex in zip(keys, exs):
        if eid not in want:
            continue
        q = ex["question"]
        row = {"id": eid, "dataset": dataset, "request": request_sha(ex), "model": resp.get("model"), "type": q["type"]}
        if q["type"] == "binary":
            p = float(ans[ks[0]]["noul"])
            row |= {"p_yes": p, "answer": p >= 0.5, "confidence": max(p, 1 - p)}
        elif q["type"] == "multiclass":
            pr = ans[ks[0]]["probabilities"]
            probs = {c["id"]: float(pr.get(c["id"], 0)) for c in q["candidates"]}
            best = max(probs, key=probs.get)
            row |= {"probs": probs, "answer": best, "confidence": probs[best]}
        else:
            probs = {c["id"]: float(ans[k]["noul"]) for c, k in zip(q["candidates"], ks)}
            row |= {
                "probs": probs,
                "answer": [c for c, p in probs.items() if p >= 0.5],
                "confidence": min(max(p, 1 - p) for p in probs.values()),
            }
        row["correct"] = norm(row["answer"]) == norm(ex["target"])
        out.append(row)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--call", action="store_true", help="PAID: call Jev for texts with no cached response")
    ap.add_argument("--budget", type=float, default=0.0, help="max USD for --call")
    ap.add_argument("--workers", type=int, default=12)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    cache = {}
    for p in CACHES:
        if (ROOT / p).exists():
            for c in read_jsonl(ROOT / p):
                cache.setdefault(c["key"], c["response"])
    raw = {}
    for d in RAW:
        for f in sorted((ROOT / d).glob("*.jsonl")):
            for src in read_jsonl(f):
                raw[src["source_id"]] = src
    print(f"{len(cache)} cached Jev responses, {len(raw)} raw sources", flush=True)

    preds, pending, hit_cost, hit_chars = {}, [], 0.0, 0
    for name, path, *_ in datasets(ROOT):
        groups = defaultdict(list)
        for ex in load([ROOT / path]):
            groups[ex["source_id"]].append(ex)
        for sid, exs in groups.items():
            want, state = {e["id"] for e in exs}, exs[0]["state"]
            tries = [exs]
            if sid in raw and raw[sid]["state"] == state:
                tries.append(expand_source(raw[sid]))
            for t in tries:
                body, keys = jev_request(MODEL, state, t)
                resp = cache.get(key_of(body))
                if resp:
                    try:
                        for r in extract(resp, keys, t, want, name):
                            preds[r["id"]] = r
                        hit_cost += call_cost(resp)
                        hit_chars += len(json.dumps(body))
                        break
                    except (KeyError, TypeError, ValueError):
                        continue
            else:
                pending.append((name, sid, exs))
    rate = hit_cost / max(hit_chars, 1)
    est = sum(len(json.dumps(jev_request(MODEL, exs[0]["state"], exs)[0])) for _, _, exs in pending) * rate
    todo = Counter(n for n, _, exs in pending for _ in exs)
    print(
        f"from cache: {len(preds)} questions; missing: {sum(todo.values())} questions in {len(pending)} texts "
        f"{dict(todo)}; estimated cost ${est:.2f} (at the cached calls' cost per character)",
        flush=True,
    )

    if a.call and pending:
        lock, spent, errors, stop = threading.Lock(), [0.0], [], threading.Event()

        def one(item):
            name, sid, exs = item
            if stop.is_set():
                return
            body, keys = jev_request(MODEL, exs[0]["state"], exs)
            for attempt in range(3):
                try:
                    resp = http("POST", "/alpha/decisions", body)
                    break
                except Exception as e:  # HTTP or network: retry, then record
                    err = repr(e)[:200]
                    time.sleep(3 * (attempt + 1))
            else:
                with lock:
                    errors.append((sid, err))
                return
            with lock:
                spent[0] += call_cost(resp)
                new_cache.write(json.dumps({"key": key_of(body), "sid": sid, "response": resp, "t": time.time()}) + "\n")
                new_cache.flush()
                try:
                    for r in extract(resp, keys, exs, {e["id"] for e in exs}, name):
                        preds[r["id"]] = r
                except (KeyError, TypeError, ValueError) as e:
                    errors.append((sid, f"parse {e!r}"[:200]))
                if spent[0] >= a.budget:
                    stop.set()

        with open(OUT / "cache.jsonl", "a") as new_cache, cf.ThreadPoolExecutor(a.workers) as pool:
            for i, _ in enumerate(pool.map(one, pending)):
                if i % 2000 == 1999:
                    print(f"  {i + 1}/{len(pending)} texts, spent ${spent[0]:.2f}, errors {len(errors)}", flush=True)
        print(f"called Jev: spent ${spent[0]:.2f}, errors {len(errors)} {errors[:3]}", flush=True)

    order = {n: i for i, (n, *_) in enumerate(datasets(ROOT))}
    rows = sorted(preds.values(), key=lambda r: (order.get(r["dataset"], 99), r["id"]))
    with open(OUT / "predictions.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {OUT / 'predictions.jsonl'}: {len(rows)} questions", flush=True)


if __name__ == "__main__":
    main()
