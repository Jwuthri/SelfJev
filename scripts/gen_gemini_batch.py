"""Write a data batch with Gemini through Google's Batch API (50% of the interactive price, results within 24 h).

  zsh -ic 'uv run python scripts/gen_gemini_batch.py submit --batch <name> --calls 400 [--usecases train] [--multilabel] [--round3]'
  zsh -ic 'uv run python scripts/gen_gemini_batch.py collect --batch <name>'      # poll, download, write data/batches/<name>/raw/<prefix>.jsonl

Then the usual steps: bash scripts/grow_batch.sh <name> judge|build|finish (data/README.md "Grow it"). PAID: the user
OKs a price first (≈ $0.02 per call at batch prices for gemini-3.8-flash; see the estimate printed by submit).

- Same prompts as gen_hardcases.py: system prompt = its BRIEF (+ BRIEF_llm.md for --usecases), user = one ASSIGNMENT per call.
- No live feedback in a batch, so the plan is balanced up front: every (use case x tier) cell gets the same number of
  calls at every text length, and long lengths get more calls because each call writes fewer texts there (the sync
  generator balances kept texts per length the same way).
- Key GOOGLE_GEMINI_API_KEY from ~/.zshrc (run through zsh -ic; never printed). State and raw responses:
  reports/batches/<name>/gemini_batch/.
"""
import argparse
import hashlib
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
import gen_hardcases as g  # noqa: E402
from selfjev.data import read_jsonl  # noqa: E402

API = "https://generativelanguage.googleapis.com"
PRICE = {"gemini-3.8-flash": (0.375, 1.875)}  # USD per M tokens at batch prices (50% of 0.75 / 3.75); thinking = output
EST_CALL = 0.02  # USD per call at batch prices (sync calls averaged ≈ $0.04 on llm/multilabel batches)


def req(method, path, body=None, raw=None, headers=None, timeout=300):
    data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
    h = {"x-goog-api-key": os.environ["GOOGLE_GEMINI_API_KEY"]} | ({"Content-Type": "application/json"} if body is not None else {}) | (headers or {})
    r = urllib.request.Request(path if path.startswith("http") else API + path, data, method=method, headers=h)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path.split('?')[0]}: HTTP {e.code} {e.read()[:400].decode(errors='replace')}") from None


def plan(n, seed, usecases, per_call):
    """n call specs {i, uc, tier, tokens}, balanced over cells x lengths, weighted to equal texts per length."""
    rng = random.Random(seed)
    cells = [(u, t) for u in g.USECASES for t in g.TIERS] if usecases else [(None, t) for t in g.TIERS]
    texts_per_call = {L: max(1, min(per_call, 12000 // L)) for L in g.LENGTHS}
    w = {L: 1 / texts_per_call[L] for L in g.LENGTHS}
    calls = {L: round(n * w[L] / sum(w.values())) for L in g.LENGTHS}
    specs = []
    for L, k in calls.items():
        order = cells[:]
        rng.shuffle(order)
        specs += [{"uc": order[j % len(order)][0], "tier": order[j % len(order)][1], "tokens": L} for j in range(k)]
    rng.shuffle(specs)
    return [s | {"i": i} for i, s in enumerate(specs)]


def mode(a):
    fam, tag = ("llm", "llm-eval") if a.usecases == "train" else ("r3", "hard r3") if a.round3 else ("r2", "hard r2")
    fam += "ml" if a.multilabel else ""
    system = g.BRIEF.replace(g.HELD_OUT, "") + "\n\n" + g.BRIEF_LLM if a.usecases else g.BRIEF
    prefix = a.prefix or "".join(ch for ch in a.batch if ch.isalnum())[:10] + ("l" if a.usecases else "") + "gb"
    return fam, tag, system, prefix


def submit(a):
    fam, tag, system, prefix = mode(a)
    specs = plan(a.calls, a.seed, a.usecases, a.per_call)
    lines = []
    for s in specs:
        rng = random.Random(f"{a.seed}:{s['i']}")
        n = max(1, min(a.per_call, 12000 // s["tokens"]))
        user, traps = g.assignment(rng, s["tier"], n, s["tokens"], None, False, g.R3_HINTS if a.round3 or a.usecases else None,
                                   uc=s["uc"], multilabel=a.multilabel)
        s |= {"traps": traps, "user": user}
        lines.append(json.dumps({"key": f"c{s['i']}", "request": {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"temperature": 1.0, "maxOutputTokens": a.max_tokens, "thinkingConfig": {"thinkingLevel": "low"}}}}))
    payload = ("\n".join(lines) + "\n").encode()
    print(f"{len(specs)} calls, {len(payload) / 1e6:.1f} MB; estimated ≈ ${len(specs) * EST_CALL:.2f} at batch prices", flush=True)
    if a.dry_run:
        print(lines[0][:600])
        return
    _, h = req("POST", "/upload/v1beta/files", body={"file": {"display_name": f"{a.batch}-{a.seed}"}}, headers={
        "X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start",
        "X-Goog-Upload-Header-Content-Length": str(len(payload)), "X-Goog-Upload-Header-Content-Type": "application/jsonl"})
    url = next(v for k, v in h.items() if k.lower() == "x-goog-upload-url")
    body, _ = req("POST", url, raw=payload, headers={"X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"})
    file_name = json.loads(body)["file"]["name"]
    body, _ = req("POST", f"/v1beta/models/{a.model}:batchGenerateContent",
                  body={"batch": {"display_name": f"{a.batch}-{a.seed}", "input_config": {"file_name": file_name}}})
    job = json.loads(body)["name"]
    state = STATE(a)
    jobs = json.loads(state.read_text()) if state.exists() else []
    jobs.append({"job": job, "file": file_name, "model": a.model, "seed": a.seed, "fam": fam, "tag": tag, "prefix": prefix,
                 "specs": specs, "collected": False, "t": time.time()})
    state.write_text(json.dumps(jobs))
    print(f"submitted {job} ({len(specs)} calls); collect with: gen_gemini_batch.py collect --batch {a.batch}", flush=True)


def STATE(a):
    d = ROOT / "reports/batches" / a.batch / "gemini_batch"
    d.mkdir(parents=True, exist_ok=True)
    return d / "jobs.json"


def text_of(resp):
    parts = ((resp.get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
    return "".join(p.get("text", "") for p in parts if not p.get("thought"))


def collect(a):
    state = STATE(a)
    jobs = json.loads(state.read_text()) if state.exists() else []
    raw_dir = ROOT / "data/batches" / a.batch / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    seen = {hashlib.sha1(s["state"].strip().lower().encode()).hexdigest() for f in raw_dir.glob("*.jsonl") for s in read_jsonl(f)}
    for jb in jobs:
        if jb["collected"]:
            continue
        while True:
            info = json.loads(req("GET", f"/v1beta/{jb['job']}")[0])
            st = info.get("state") or info.get("metadata", {}).get("state", "")
            print(f"{jb['job']}: {st}", flush=True)
            if st.endswith(("SUCCEEDED", "FAILED", "CANCELLED", "EXPIRED")) or not a.wait:
                break
            time.sleep(a.poll)
        if not st.endswith("SUCCEEDED"):
            continue
        dest = info.get("dest") or info.get("response", {}).get("dest") or info.get("metadata", {}).get("output") or {}
        out_file = dest.get("fileName") or dest.get("responsesFile")
        data = req("GET", f"{API}/download/v1beta/{out_file}:download?alt=media", timeout=600)[0].decode()
        (state.parent / f"{jb['job'].split('/')[-1]}.jsonl").write_text(data)
        specs = {f"c{s['i']}": s for s in jb["specs"]}
        pin, pout = PRICE.get(jb["model"], (0.0, 0.0))
        out_path = raw_dir / f"{jb['prefix']}.jsonl"
        counter = max((int(s["source_id"].split("-")[-1]) for s in read_jsonl(out_path)), default=0) if out_path.exists() else 0
        kept, drops, cost, qs = [], Counter(), 0.0, Counter()
        for line in data.splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            s, resp = specs.get(r.get("key")), r.get("response")
            if not s or not resp:
                drops["error " + str((r.get("error") or r.get("status") or {}).get("code", "?"))] += 1
                continue
            u = resp.get("usageMetadata") or {}
            cost += (u.get("promptTokenCount", 0) * pin + (u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)) * pout) / 1e6
            parsed, _ = g.parse_sources(text_of(resp))
            for src in parsed:
                if not isinstance(src, dict):  # a model sometimes emits a bare string in the array
                    drops["shape"] += 1
                    continue
                h = hashlib.sha1(str(src.get("state", "")).strip().lower().encode()).hexdigest()
                if h in seen:
                    drops["duplicate state"] += 1
                    continue
                counter += 1
                fam = f"{jb['fam']}_{s['uc']}" if s["uc"] else jb["fam"]
                tag = f"{jb['tag']}, usecase={s['uc']}, gemini batch" if s["uc"] else f"{jb['tag']}, gemini batch"
                out, why = g.sanitize(src, s["tier"], s["traps"], jb["model"], f"{jb['prefix']}-{counter:04d}", s["tokens"], fam, tag)
                if out is None:
                    counter -= 1
                    drops[why] += 1
                    continue
                out["provenance"] = out["provenance"].replace("synthetic:openrouter/", "synthetic:google-batch/", 1)  # not OpenRouter
                seen.add(h)
                kept.append(out)
                qs[(s["uc"], s["tier"])] += len(out["questions"])
        with open(out_path, "a") as f:
            for src in kept:
                f.write(json.dumps(src, ensure_ascii=False) + "\n")
        jb |= {"collected": True, "cost": cost, "kept_texts": len(kept), "kept_questions": sum(qs.values())}
        state.write_text(json.dumps(jobs))
        print(f"collected {jb['job']}: {len(kept)} texts / {sum(qs.values())} questions, cost ${cost:.2f} (batch prices), "
              f"drops {dict(drops)}; by cell {dict(qs)}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["submit", "collect"])
    ap.add_argument("--batch", required=True)
    ap.add_argument("--calls", type=int, default=100)
    ap.add_argument("--model", default="gemini-3.8-flash")
    ap.add_argument("--usecases", choices=["train"])
    ap.add_argument("--multilabel", action="store_true")
    ap.add_argument("--round3", action="store_true")
    ap.add_argument("--per-call", type=int, default=5)
    ap.add_argument("--max-tokens", type=int, default=32000)
    ap.add_argument("--seed", type=int, default=int(time.time()))
    ap.add_argument("--prefix")
    ap.add_argument("--dry-run", action="store_true", help="submit: build the requests and print one, no API call")
    ap.add_argument("--wait", action="store_true", help="collect: poll until every job is done")
    ap.add_argument("--poll", type=int, default=300)
    a = ap.parse_args()
    (submit if a.action == "submit" else collect)(a)


if __name__ == "__main__":
    main()
