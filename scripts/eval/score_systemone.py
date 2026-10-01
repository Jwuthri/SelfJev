"""Score any Jev-compatible server (POST /v1/systemone) on one of our frozen test files, with our own evaluator.

Questions are mapped exactly as for Jev (compare_external.py): binary -> noul, multiclass -> choice over the candidate
descriptions, multilabel -> one noul per candidate. One request per state (split into chunks of --max-questions).
Answers are normalised to Jev's fields, so servers that name them slightly differently still score. A question the
server fails to answer (HTTP error, missing key) counts as wrong in `accuracy_all`; `question_accuracy` is on answered
questions only. Our own report on the same file gives the row layout and the paired McNemar test.

usage (on the GPU box, with the competitor's server running):
  uv run python scripts/eval/score_systemone.py --url http://127.0.0.1:8010 --name laya \
      --data data/eval2.jsonl --ours images_v1/eval2 --out reports/competitors/eval2
"""

import argparse
import concurrent.futures as cf
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from compare_external import to_row

from selfjev.data import load, sha256_file
from selfjev.data.providers import jev_request
from selfjev.evaluation.evaluate import breakdowns, evaluate_predictions, markdown
from selfjev.evaluation.stats import mcnemar

ROOT = Path(__file__).resolve().parents[2]


def norm(a: dict) -> dict:
    """-> Jev's answer fields: {"noul": p} or {"probabilities": {key: p}}."""
    if "noul" in a and not isinstance(a["noul"], bool):
        return {"noul": float(a["noul"])}
    probs = a.get("probabilities") or a.get("probs") or a.get("distribution")
    if isinstance(probs, dict) and probs:
        low = {str(k).lower(): float(v) for k, v in probs.items()}
        if set(low) <= {"true", "false", "yes", "no"} and ("true" in low or "yes" in low):
            p = low.get("true", low.get("yes", 0.0))
            return {"noul": p, "probabilities": probs}
        return {"probabilities": {k: float(v) for k, v in probs.items()}}
    for k in ("probability", "p_yes", "p", "yes"):
        if k in a:
            return {"noul": float(a[k])}
    if "choice" in a:  # label only: one-hot
        return {"probabilities": {a["choice"]: 1.0}}
    raise KeyError(f"no probabilities in answer {str(a)[:200]}")


def post(url, body, timeout):
    req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="server base URL, e.g. http://127.0.0.1:8010")
    ap.add_argument("--path", default="/v1/systemone")
    ap.add_argument("--name", required=True)
    ap.add_argument("--model", default="default", help="`model` field of each request")
    ap.add_argument("--data", required=True)
    ap.add_argument("--ours", required=True, help="our report dir under reports/ on the same file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--extra", default="{}", help="JSON merged into every request body, e.g. '{\"max_len\": 8192}'")
    ap.add_argument(
        "--image-style",
        choices=["raw", "dict", "messages"],
        default="raw",
        help='image state as sent: raw data URL (Jev/ours/imajev), {"image": url} (openjev shim), chat messages (llm2jev)',
    )
    ap.add_argument("--max-questions", type=int, default=64)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--limit-states", type=int)
    a = ap.parse_args()

    ours = {r["id"]: r for r in json.loads((ROOT / "reports" / a.ours / "report.json").read_text())["predictions"]}
    groups = {}
    for ex in load(ROOT / a.data, {"test"}):
        groups.setdefault(ex["source_id"], (ex["state"], []))[1].append(ex)
    if a.limit_states:
        groups = dict(list(groups.items())[: a.limit_states])
    total = sum(len(exs) for _, exs in groups.values())
    chunks = []  # (state, [examples]) with at most max_questions Jev questions each
    for state, exs in groups.values():
        cur, n = [], 0
        for ex in exs:
            k = len(ex["question"]["candidates"]) if ex["question"]["type"] == "multilabel" else 1
            if cur and n + k > a.max_questions:
                chunks.append((state, cur))
                cur, n = [], 0
            cur.append(ex)
            n += k
        chunks.append((state, cur))

    rows, errors, t0 = {}, [], time.time()

    def one(chunk):
        state, exs = chunk
        body, keys = jev_request(a.model, state, exs)
        body |= json.loads(a.extra)
        if isinstance(state, str) and state.startswith("data:image") and a.image_style != "raw":
            img = {"type": "image", "image": state}
            body["state"] = {"image": state} if a.image_style == "dict" else [{"role": "user", "content": [img]}]
        try:
            answers = post(a.url + a.path, body, a.timeout)["answers"]
        except urllib.error.HTTPError as e:
            return [], [(exs[0]["source_id"], e.code, e.read()[:300].decode(errors="replace"))]
        except Exception as e:
            return [], [(exs[0]["source_id"], None, repr(e)[:300])]
        out, errs = [], []
        for (eid, ks), ex in zip(keys, exs):
            try:
                out.append(to_row(ex, ours[eid], "jev", [norm(answers[k]) for k in ks]))
            except Exception as e:
                errs.append((eid, "parse", repr(e)[:300]))
        return out, errs

    with cf.ThreadPoolExecutor(a.workers) as pool:
        for i, (out, errs) in enumerate(pool.map(one, chunks)):
            rows.update((r["id"], r) for r in out)
            errors += errs
            if i % 50 == 49:
                print(
                    f"  {a.name}: {i + 1}/{len(chunks)} requests, {len(rows)} answered, {len(errors)} errors, {time.time() - t0:.0f}s",
                    flush=True,
                )
    wall = time.time() - t0
    preds = list(rows.values())
    if not preds:
        raise SystemExit(f"EVAL {a.name} {a.data}: nothing answered, {len(errors)} errors, first: {errors[:3]}")
    rep = {
        "meta": {
            "model": a.name,
            "revision": "-",
            "adapter": None,
            "adapter_sha256": None,
            "prompt": "jev-request",
            "prompt_sha": "-",
            "calibration": None,
            "device": "cuda",
            "dtype": "-",
            "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "wall_s": wall,
            "n": len(preds),
            "n_total": total,
            "splits": ["test"],
            "architecture": "external open model via /v1/systemone",
            "extra_body": json.loads(a.extra),
            "image_style": a.image_style,
            "data": [{"path": a.data, "sha256": sha256_file(ROOT / a.data)}],
            "errors": len(errors),
            "error_examples": errors[:10],
            "accuracy_all": sum(r["correct"] for r in preds) / total,
        },
        "metrics": evaluate_predictions(preds),
        **breakdowns(preds),
        "predictions": preds,
    }
    d = ROOT / a.out / a.name
    d.mkdir(parents=True, exist_ok=True)
    (d / "report.json").write_text(json.dumps(rep, indent=1))
    ids = {ex["id"] for _, exs in groups.values() for ex in exs}
    ours_c = {i: ours[i]["correct"] for i in ids}
    theirs = {i: rows[i]["correct"] if i in rows else False for i in ours_c}
    oa, ob, p = mcnemar(ours_c, theirs)
    (d / "report.md").write_text(
        markdown(rep) + f"\n\nAnswered {len(preds)}/{total}; errors {len(errors)}; accuracy counting failures as wrong "
        f"{100 * rep['meta']['accuracy_all']:.1f}%.\n"
        f"Paired vs ours ({a.ours}): ours only right {oa}, {a.name} only right {ob}, p = {p:.2g}\n"
    )
    print(
        f"EVAL {a.name} {a.data}: answered {len(preds)}/{total}, acc(answered) {100 * rep['metrics']['question_accuracy']:.1f}, "
        f"acc(all) {100 * rep['meta']['accuracy_all']:.1f}, errors {len(errors)}, wall {wall:.0f}s, vs ours {oa}/{ob} p={p:.2g}",
        flush=True,
    )
    for e in errors[:5]:
        print("   error:", e, flush=True)


if __name__ == "__main__":
    main()
