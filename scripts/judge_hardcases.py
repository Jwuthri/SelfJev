"""Blind re-labelling of data/hardcases/raw/*.jsonl by GPT-6 Astra through the OpenAI Batch API (half price, 24 h window).

  zsh -ic 'uv run python scripts/judge_hardcases.py --prefixes gf gk df lu'        # submit new sources, wait, write answers
  zsh -ic 'uv run python scripts/judge_hardcases.py --prefixes gf gk df lu --jev'  # + Jev as a cheap second opinion

- The judge sees state + instruction + candidates only (never the target, notes or tags): the same prompt, JSON
  schema and reasoning effort (low) as the GPT-6 Astra test run (compare_external.llm_request).
- Each source is submitted once: <review>/batches.json remembers every batch and its source ids, the downloaded output
  files are kept in <review>/batch_results/<id>.jsonl, and answers_astra.jsonl is rebuilt from all of them on every run.
- Needs OPENAI_API_KEY (the judge) and OPENROUTER_API_KEY (Jev): run through `zsh -ic`, never print either.
  OpenRouter's own batch endpoint refused this account's key ("Batch requests require a concrete user identity").
- Answer rows {"id": "<source_id>-q<i>", "answer": bool | id | [ids], "confidence": p, "note": ...} are what
  build_hardcases.py compares with the authored target. Agreement tables go to <review>/JUDGE.md.
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import sys
import threading
import time
import os
import urllib.error
import urllib.request
import uuid
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
from compare_external import call_cost, http, jev_request, llm_request  # noqa: E402
from personal_jev.data import expand_source, read_jsonl, write_jsonl  # noqa: E402

RAW = ROOT / "data/hardcases/raw"
lock_sync = threading.Lock()
TERMINAL = {"completed", "failed", "expired", "cancelled"}
OPENAI = "https://api.openai.com"
PRICE = {"gpt-6-astra": (5.0, 25.0)}  # batch USD per M tokens (input, output incl. reasoning) = 50% of list


def oa(method, path, body=None, raw=None, ctype="application/json", timeout=600):
    data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
    headers = {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"} | ({"Content-Type": ctype} if data is not None else {})
    try:
        with urllib.request.urlopen(urllib.request.Request(OPENAI + path, data, method=method, headers=headers), timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path}: HTTP {e.code} {e.read()[:400].decode(errors='replace')}") from None


def upload_jsonl(lines):
    b = "----pjev" + uuid.uuid4().hex
    payload = (f"--{b}\r\nContent-Disposition: form-data; name=\"purpose\"\r\n\r\nbatch\r\n--{b}\r\n"
               f"Content-Disposition: form-data; name=\"file\"; filename=\"batch.jsonl\"\r\nContent-Type: application/jsonl\r\n\r\n").encode()
    payload += "\n".join(lines).encode() + f"\r\n--{b}--\r\n".encode()
    return json.loads(oa("POST", "/v1/files", raw=payload, ctype=f"multipart/form-data; boundary={b}"))["id"]


def to_openai(body, model, effort):
    """OpenRouter chat body (compare_external.llm_request) -> OpenAI chat body."""
    b = {k: v for k, v in body.items() if k not in ("model", "usage", "reasoning", "max_tokens")}
    return b | {"model": model, "reasoning_effort": effort, "max_completion_tokens": body.get("max_tokens", 6000)}


def sources(prefixes, limit=None, raw=RAW):
    out = {}
    for f in sorted(raw.glob("*.jsonl")):
        for src in read_jsonl(f):
            sid = src["source_id"]
            if prefixes and sid.split("-")[0] not in prefixes:
                continue
            if sid in out:
                raise ValueError(f"duplicate source_id {sid} in {f}")
            out[sid] = (src, expand_source(src))
    return dict(list(out.items())[:limit]) if limit else out


def decide(ex, ans):
    """Judge probabilities -> (answer, confidence) in the authored target's type."""
    q = ex["question"]
    if q["type"] == "binary":
        p = float(ans["p_yes"])
        return p >= 0.5, max(p, 1 - p)
    ids = [c["id"] for c in q["candidates"]]
    ps = {c: max(float(ans.get(c, 0.0)), 0.0) for c in ids}
    if q["type"] == "multiclass":
        best = max(ids, key=lambda c: (ps[c], -ids.index(c)))
        return best, ps[best] / (sum(ps.values()) or 1.0)
    return [c for c in ids if ps[c] >= 0.5], min(max(p, 1 - p) for p in ps.values())


def submit(model, effort, groups, registry, chunk, reg_path=None):
    """Submits new sources in chunks; the registry is saved after EVERY chunk so a failure mid-way (e.g. OpenAI's enqueued-token
    limit) never leads to paying twice: rerun and the remaining sources are submitted."""
    known = {sid for b in registry["batches"] for sid in b["source_ids"]}
    todo = [sid for sid in groups if sid not in known]
    for i in range(0, len(todo), chunk):
        sids = todo[i:i + chunk]
        lines = []
        for sid in sids:
            state, exs = groups[sid][0]["state"], groups[sid][1]
            body, _ = llm_request(model, state, exs, effort)
            lines.append(json.dumps({"custom_id": sid, "method": "POST", "url": "/v1/chat/completions", "body": to_openai(body, model, effort)}))
        try:
            fid = upload_jsonl(lines)
            b = json.loads(oa("POST", "/v1/batches", {"input_file_id": fid, "endpoint": "/v1/chat/completions", "completion_window": "24h",
                                                        "metadata": {"project": "personal-jev hardcases"}}))
        except RuntimeError as e:  # e.g. "Enqueued token limit reached": stop here, rerun later for the rest
            print(f"submission stopped after {i} sources: {str(e)[:300]}", flush=True)
            return i
        registry["batches"].append({"id": b["id"], "input_file_id": fid, "model": model, "effort": effort, "source_ids": sids,
                                    "submitted": time.time(), "status": b.get("status")})
        if reg_path:
            reg_path.write_text(json.dumps(registry, indent=1))
        print(f"submitted batch {b['id']}: {len(sids)} sources, status {b.get('status')}", flush=True)
    return len(todo)


def wait(registry, results_dir, poll):
    pending = [b for b in registry["batches"] if not (results_dir / f"{b['id']}.jsonl").exists()]
    while pending:
        for b in list(pending):
            r = json.loads(oa("GET", f"/v1/batches/{b['id']}"))
            b["status"] = r.get("status")
            c = r.get("request_counts") or {}
            print(f"  {b['id']}: {r.get('status')} {c.get('completed', '?')}/{c.get('total', '?')} done, {c.get('failed', 0)} failed", flush=True)
            if r.get("status") in TERMINAL:
                out = oa("GET", f"/v1/files/{r['output_file_id']}/content").decode() if r.get("output_file_id") else ""
                if r.get("error_file_id"):
                    (results_dir / f"{b['id']}.errors.jsonl").write_bytes(oa("GET", f"/v1/files/{r['error_file_id']}/content"))
                if r.get("status") != "completed":
                    print(f"  batch {b['id']} ended {r.get('status')}: {str(r.get('errors'))[:300]}", flush=True)
                (results_dir / f"{b['id']}.jsonl").write_text(out)
                pending.remove(b)
        if pending:
            if poll <= 0:
                return False
            time.sleep(poll)
    return True


def collect(groups, results_dir, out, model):
    rows, cost, errs = [], 0.0, Counter()
    keys_by_sid = {sid: [(ex["id"], f"q{i}") for i, ex in enumerate(exs)] for sid, (src, exs) in groups.items()}
    pin, pout = PRICE.get(model, (0.0, 0.0))
    for f in sorted(results_dir.glob("*.jsonl")):
        if f.name.endswith(".errors.jsonl"):
            continue
        for item in map(json.loads, filter(str.strip, f.read_text().splitlines())):
            sid = item.get("custom_id")
            if sid not in groups:
                continue
            resp = (item.get("response") or {}).get("body") or {}
            if item.get("error") or (item.get("response") or {}).get("status_code") != 200:
                errs["item error"] += 1
                continue
            u = resp.get("usage") or {}
            cost += (u.get("prompt_tokens", 0) * pin + u.get("completion_tokens", 0) * pout) / 1e6
            try:
                answers = json.loads(resp["choices"][0]["message"]["content"])
                for (eid, k), ex in zip(keys_by_sid[sid], groups[sid][1]):
                    a, conf = decide(ex, answers[k])
                    rows.append({"id": eid, "answer": a, "confidence": round(conf, 4), "note": f"{resp.get('model', model)} effort=low batch {f.stem}"})
            except Exception as e:  # unparsable content
                errs[f"parse: {type(e).__name__}"] += 1
    write_jsonl(out, rows)
    print(f"{out}: {len(rows)} answers, batch cost ${cost:.2f}, errors {dict(errs)}", flush=True)
    return {row["id"]: row for row in rows}, cost


def run_sync(groups, review, model, effort="low", workers=6):
    """Second judge through OpenRouter chat completions (no batch): answers_<slug>.jsonl, cached, blind like the batch judge."""
    slug = model.split("/")[-1]
    cache_path = review / f"sync_cache_{slug}.jsonl"
    cache = {c["key"]: c["response"] for c in map(json.loads, open(cache_path))} if cache_path.exists() else {}
    rows, cost, errs = {}, [0.0], Counter()

    def one(sid):
        src, exs = groups[sid]
        body, keys = llm_request(model, src["state"], exs, effort)
        key = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
        if key not in cache:
            for attempt in range(3):
                try:
                    resp = http("POST", "/v1/chat/completions", body, timeout=600)
                    break
                except Exception as e:  # rate limit, network
                    resp, err = None, repr(e)[:120]
                    time.sleep(5 * (attempt + 1))
            if resp is None:
                errs[err] += 1
                return
            cost[0] += call_cost(resp)
            cache[key] = resp
            with lock_sync:
                with open(cache_path, "a") as f:
                    f.write(json.dumps({"key": key, "sid": sid, "response": resp}) + "\n")
        try:
            answers = json.loads(cache[key]["choices"][0]["message"]["content"])
            for (eid, ks), ex in zip(keys, exs):
                a, conf = decide(ex, answers[ks[0]])
                rows[eid] = {"id": eid, "answer": a, "confidence": round(conf, 4), "note": f"{model} effort={effort} sync"}
        except Exception as e:
            errs[f"parse: {type(e).__name__}"] += 1

    with cf.ThreadPoolExecutor(workers) as pool:
        list(pool.map(one, list(groups)))
    out = review / f"answers_{slug}.jsonl"
    write_jsonl(out, list(rows.values()))
    print(f"{out}: {len(rows)} answers, ${cost[0]:.2f}, errors {dict(errs)}", flush=True)
    return rows


def run_jev(groups, review, model="~typesafe/jev-latest", workers=6):
    cache_path = review / "jev_cache.jsonl"
    cache = {c["key"]: c["response"] for c in map(json.loads, open(cache_path))} if cache_path.exists() else {}
    rows, cost = {}, [0.0]

    def one(sid):
        src, exs = groups[sid]
        body, keys = jev_request(model, src["state"], exs)
        key = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
        if key not in cache:
            try:
                resp = http("POST", "/alpha/decisions", body)
            except (urllib.error.HTTPError, Exception) as e:
                return
            cost[0] += call_cost(resp)
            cache[key] = resp
            with open(cache_path, "a") as f:
                f.write(json.dumps({"key": key, "sid": sid, "response": resp}) + "\n")
        ans = cache[key]["answers"]
        for (eid, ks), ex in zip(keys, exs):
            q = ex["question"]
            if q["type"] == "binary":
                p = float(ans[ks[0]]["noul"])
                rows[eid] = {"id": eid, "answer": p >= 0.5, "confidence": max(p, 1 - p), "note": "jev"}
            elif q["type"] == "multiclass":
                pr = ans[ks[0]]["probabilities"]
                ids = [c["id"] for c in q["candidates"]]
                best = max(ids, key=lambda c: float(pr.get(c, 0)))
                rows[eid] = {"id": eid, "answer": best, "confidence": float(pr.get(best, 0)), "note": "jev"}
            else:
                ps = [float(ans[k]["noul"]) for k in ks]
                rows[eid] = {"id": eid, "answer": [c["id"] for c, p in zip(q["candidates"], ps) if p >= 0.5],
                             "confidence": min(max(p, 1 - p) for p in ps), "note": "jev"}

    with cf.ThreadPoolExecutor(workers) as pool:
        list(pool.map(one, list(groups)))
    write_jsonl(review / "jev_answers.jsonl", list(rows.values()))
    print(f"jev: {len(rows)} answers, ${cost[0]:.3f}", flush=True)
    return rows


def norm(t):
    return sorted(t) if isinstance(t, list) else t


def report(groups, judge, jev, path):
    def agree_table(title, keyf):
        c = defaultdict(Counter)
        for sid, (src, exs) in groups.items():
            for ex in exs:
                k = keyf(src, ex)
                if ex["id"] in judge:
                    c[k]["judged"] += 1
                    c[k]["agree"] += norm(judge[ex["id"]]["answer"]) == norm(ex["target"])
                if jev and ex["id"] in jev:
                    c[k]["jev"] += 1
                    c[k]["jev_agree"] += norm(jev[ex["id"]]["answer"]) == norm(ex["target"])
                    if ex["id"] in judge:
                        c[k]["both"] += norm(judge[ex["id"]]["answer"]) == norm(ex["target"]) != norm(jev[ex["id"]]["answer"])
        lines = [f"### {title}", "", "| " + title + " | judged | author = judge % | jev | author = jev % | judge right, jev wrong |", "|---|---|---|---|---|---|"]
        for k, v in sorted(c.items(), key=lambda kv: str(kv[0])):
            pct = lambda a, b: f"{100 * v[a] / v[b]:.1f}" if v[b] else "—"
            lines.append(f"| {k} | {v['judged']} | {pct('agree', 'judged')} | {v['jev']} | {pct('jev_agree', 'jev')} | {v['both']} |")
        tot = Counter()
        for v in c.values():
            tot.update(v)
        pct = lambda a, b: f"{100 * tot[a] / tot[b]:.1f}" if tot[b] else "—"
        lines.append(f"| **all** | {tot['judged']} | {pct('agree', 'judged')} | {tot['jev']} | {pct('jev_agree', 'jev')} | {tot['both']} |")
        return lines + [""]

    def bucket(src):
        m = [p for p in src["provenance"].split() if p.startswith("len=")]
        return int(m[0][4:].rstrip(")")) if m else "?"

    lines = ["# Blind judge review (round 2)", "", "Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; "
             "Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.", ""]
    lines += agree_table("family", lambda s, e: s["family"])
    lines += agree_table("author", lambda s, e: s["provenance"].split(" (")[0].replace("synthetic:", ""))
    lines += agree_table("type", lambda s, e: e["question"]["type"])
    lines += agree_table("length bucket (tokens)", lambda s, e: bucket(s))
    lines += agree_table("hard case", lambda s, e: ", ".join(e["hard_cases"][:1]) or "(none)")
    path.write_text("\n".join(lines))
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefixes", nargs="*", help="source_id prefixes to judge (default: every raw file)")
    ap.add_argument("--model", default="gpt-6-astra")
    ap.add_argument("--effort", default="low")
    ap.add_argument("--chunk", type=int, default=1000, help="requests per batch")
    ap.add_argument("--poll", type=int, default=60, help="seconds between status checks; 0 = submit and return")
    ap.add_argument("--limit", type=int, help="smoke test: first N sources")
    ap.add_argument("--review", default=str(ROOT / "data/hardcases/review"))
    ap.add_argument("--jev", action="store_true", help="also run Jev synchronously as a second opinion")
    ap.add_argument("--raw", default=str(RAW), help="directory of source files to judge")
    ap.add_argument("--sync-model", help="run this OpenRouter model synchronously as the judge instead of the Astra batch")
    a = ap.parse_args()
    review = Path(a.review)
    results_dir = review / "batch_results"
    results_dir.mkdir(parents=True, exist_ok=True)
    reg_path = review / "batches.json"
    registry = json.loads(reg_path.read_text()) if reg_path.exists() else {"batches": []}
    groups = sources(a.prefixes, a.limit, Path(a.raw))
    print(f"{len(groups)} sources, {sum(len(g[1]) for g in groups.values())} questions from prefixes {a.prefixes or 'all'}", flush=True)
    if a.sync_model:
        judge = run_sync(groups, review, a.sync_model, a.effort)
        report(groups, judge, run_jev(groups, review) if a.jev else None, review / f"JUDGE_{a.sync_model.split('/')[-1]}.md")
        return
    n = submit(a.model, a.effort, groups, registry, a.chunk, reg_path)
    reg_path.write_text(json.dumps(registry, indent=1))
    print(f"{n} new sources submitted; {len(registry['batches'])} batches on record", flush=True)
    done = wait(registry, results_dir, a.poll)
    reg_path.write_text(json.dumps(registry, indent=1))
    judge, _ = collect(groups, results_dir, review / "answers_astra.jsonl", a.model)
    jev = run_jev(groups, review) if a.jev else None
    report(groups, judge, jev, review / "JUDGE.md")
    if not done:
        print("some batches are still running: rerun to collect them")


if __name__ == "__main__":
    main()
