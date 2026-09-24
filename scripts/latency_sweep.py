"""Latency and cost: the same decisions requests to Jev (OpenRouter) and to our tree scorer, text of 8..4096 tokens.

  sweep       (this machine) one request at a time, alternating endpoints in random order so both see the same
              network. Jev: POST openrouter.ai/api/alpha/decisions. Ours: `pjev serve --tree` on a GPU box, reached
              through an SSH tunnel, same body (our server accepts the decisions shape). Records the client wall
              time, plus each side's server time: ours = meta.total_ms (parse + tokenize + GPU), Jev = OpenRouter's
              Server-Timing cfWorker (OpenRouter + its call to Jev). Network round trip = TCP connect time.
  throughput  (GPU box) requests/s with batching (classify_many), which is what sets our cost per request.
  report      markdown tables from both.

Requests: a support-ticket text cut to N Qwen tokens, starting with a fresh random ticket number (no cache can
answer it), x {1, 16} choice questions with 3 options. Data sent to Jev: this synthetic text only.

usage:
  zsh -ic 'uv run python scripts/latency_sweep.py sweep --ours ours=http://127.0.0.1:8765 --ours merged=http://127.0.0.1:8766'
  uv run python scripts/latency_sweep.py throughput --adapter runs/tree_4b/adapter --merge   # on the box
  ~/vllm-env/bin/python scripts/latency_sweep.py throughput --vllm runs/tree_4b/merged       # on the box, vLLM venv
  uv run python scripts/latency_sweep.py report
"""
import argparse
import http.client
import json
import os
import random
import socket
import statistics
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from personal_jev.benchmark import FILLER  # noqa: E402

OUT = ROOT / "reports/latency"
JEV = "~typesafe/jev-latest"
LENGTHS = [2 ** k for k in range(3, 13)]  # 8 .. 4096 text tokens
SHAPES = (1, 16)  # choice questions per request, 3 options each


def body(tok, n_tokens, n_q, nonce):
    text = f"Ticket {nonce:06d}. " + FILLER * (n_tokens // 60 + 2)
    state = tok.decode(tok(text, add_special_tokens=False)["input_ids"][:n_tokens])
    crit = {f"team_{j + 1}": f"handles category {j + 1} problems such as outages, billing errors or integration failures" for j in range(3)}
    return {"model": JEV, "state": state, "questions": {
        f"q{i}": {"type": "choice", "instructions": f"Which team should handle issue number {i + 1} in this message?", "criteria": crit}
        for i in range(n_q)}}


class Endpoint:
    """Keep-alive HTTP(S) connection; connecting (and reconnecting) happens outside the timed part."""

    def __init__(self, url, headers):
        u = urlparse(url)
        self.cls = http.client.HTTPSConnection if u.scheme == "https" else http.client.HTTPConnection
        self.host, self.port, self.path, self.headers, self.conn = u.hostname, u.port, u.path, headers, None

    def post(self, obj):
        data = json.dumps(obj).encode()
        for attempt in range(2):
            try:
                if self.conn is None:
                    self.conn = self.cls(self.host, self.port, timeout=600)
                    self.conn.connect()
                t = time.perf_counter()
                self.conn.request("POST", self.path, data, self.headers)
                r = self.conn.getresponse()
                raw = r.read()
                ms = 1e3 * (time.perf_counter() - t)
                if (r.getheader("Connection") or "").lower() == "close":
                    self.conn.close()
                    self.conn = None
                return r.status, raw, ms, r.getheader("Server-Timing") or ""
            except (http.client.HTTPException, OSError):
                self.conn = None
                if attempt:
                    raise


def rtt_ms(host, port, n=7):
    addr = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)[0][4]
    ts = []
    for _ in range(n):
        t = time.perf_counter()
        socket.create_connection(addr[:2], timeout=10).close()
        ts.append(1e3 * (time.perf_counter() - t))
    return statistics.median(ts)


def sweep(a):
    from transformers import AutoTokenizer

    from personal_jev.model import MODEL_ID, MODEL_REVISION
    tok = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)  # same tokenizer as the 4B
    eps = {"jev": Endpoint("https://openrouter.ai/api/alpha/decisions", {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}", "Content-Type": "application/json", "X-OpenRouter-Title": "personal-jev latency"})}
    eps |= {name: Endpoint(url.rstrip("/") + "/api/alpha/decisions", {"Content-Type": "application/json"})
            for name, url in (o.split("=", 1) for o in a.ours)}
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {"created": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "reps": a.reps, "warmup": 1, "lengths": LENGTHS, "shapes": SHAPES,
            "rtt_ms": {"openrouter.ai:443": rtt_ms("openrouter.ai", 443)} | ({f"{a.box}:22": rtt_ms(a.box, 22)} if a.box else {})}
    print(json.dumps(meta), flush=True)
    rng, spent, n = random.Random(a.seed), 0.0, 0
    with open(OUT / f"{a.name}.jsonl", "w") as f:
        for rep in range(a.reps + 1):  # rep 0 = warm-up, not reported
            for n_tokens in LENGTHS:
                for n_q in SHAPES:
                    b = body(tok, n_tokens, n_q, rng.randrange(10 ** 6))
                    for name in rng.sample(list(eps), len(eps)):
                        status, raw, ms, timing = eps[name].post(b)
                        resp = json.loads(raw)
                        row = {"endpoint": name, "rep": rep, "text_tokens": n_tokens, "questions": n_q, "status": status, "wall_ms": ms}
                        if status != 200:
                            row["error"] = str(resp)[:300]
                        elif name == "jev":
                            u = resp.get("usage") or {}
                            spent += float(u.get("cost") or 0)
                            row |= {"server_ms": next((float(t.split("dur=")[1]) for t in timing.split(",") if t.startswith("cfWorker")), None),
                                    "input_tokens": u.get("input_tokens"), "cost": u.get("cost"), "model": resp.get("model")}
                        else:
                            m = resp["meta"]
                            row |= {"server_ms": m["total_ms"], "model_ms": m["model_ms"], "input_tokens": m["input_tokens"]}
                        f.write(json.dumps(row) + "\n")
                        n += 1
                    if spent > a.budget:
                        sys.exit(f"Jev spend ${spent:.4f} passed --budget {a.budget}")
            f.flush()
            print(f"rep {rep}/{a.reps}: {n} requests, Jev spend ${spent:.4f}", flush=True)
    (OUT / f"{a.name}_meta.json").write_text(json.dumps(meta | {"jev_spend_usd": spent}, indent=1))


def throughput(a):
    """Batched requests/s per text length on this GPU (the number that sets cost per request)."""
    import torch

    from personal_jev.classify import classify_many
    from personal_jev.server import compat_to_request
    from personal_jev.tree import RERANKER_4B, TreeScorer
    if a.vllm:
        from personal_jev.vllm_tree import VllmTreeScorer
        sc = VllmTreeScorer(a.vllm)
    else:
        sc = TreeScorer(*RERANKER_4B, adapter=a.adapter, dtype="bfloat16", max_batch_tokens=a.max_batch_tokens, merge=a.merge)
    rng, rows = random.Random(a.seed), []
    for n_tokens in LENGTHS:
        for n_q in SHAPES:
            reqs = [compat_to_request(body(sc.tokenizer, n_tokens, n_q, rng.randrange(10 ** 6)))[0] for _ in range(a.batch)]
            classify_many(sc, reqs[:8])  # warm-up
            torch.cuda.synchronize()
            t = time.perf_counter()
            _, stats = classify_many(sc, reqs)
            torch.cuda.synchronize()
            s = time.perf_counter() - t
            rows.append({"text_tokens": n_tokens, "questions": n_q, "requests": a.batch, "seconds": s, "requests_per_s": a.batch / s,
                         "input_tokens": stats["input_tokens"], "padded_tokens": stats["padded_tokens"]})
            print(json.dumps(rows[-1]), flush=True)
    out = {"meta": sc.meta | {"gpu": torch.cuda.get_device_name(), "max_batch_tokens": a.max_batch_tokens, "torch": torch.__version__,
                             "created": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, "rows": rows}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"throughput{'_vllm' if a.vllm else '_merged' if a.merge else ''}.json").write_text(json.dumps(out, indent=1))


def report(a):
    rows = [r for f in sorted(OUT.glob("requests*.jsonl")) for r in map(json.loads, open(f)) if r["rep"] > 0]  # Jev rows of all runs pool
    metas = [json.loads(f.read_text()) for f in sorted(OUT.glob("requests*_meta.json"))]
    meta = metas[0] | {"jev_spend_usd": sum(m["jev_spend_usd"] for m in metas), "reps": sum(m["reps"] for m in metas)}
    names = sorted({r["endpoint"] for r in rows}, key=lambda n: (n != "jev", n))
    bad = [r for r in rows if r["status"] != 200]
    ok = [r for r in rows if r["status"] == 200]

    def cell(n_tokens, n_q, name, key, q=0.5):
        xs = sorted(r[key] for r in ok if (r["text_tokens"], r["questions"], r["endpoint"]) == (n_tokens, n_q, name) and r.get(key) is not None)
        return xs[min(len(xs) - 1, round(q * (len(xs) - 1)))] if xs else None

    fmt = lambda x: "—" if x is None else f"{x:,.0f}"  # noqa: E731
    lines = ["# Latency sweep: Jev vs our tree scorer", "",
             f"- {meta['created']}; {len(metas)} sweep run(s) of 10 timed rounds each (after 1 warm-up round), one request at a time, "
             f"endpoints in random order; Jev is in every run, so it has {meta['reps']} samples per cell, each of ours 10.",
             f"- network round trip (TCP connect, median): " + ", ".join(f"{k} {v:.0f} ms" for k, v in meta["rtt_ms"].items()),
             f"- Jev spend for the whole sweep: ${meta['jev_spend_usd']:.4f}; failed requests: {len(bad)}", ""]
    for n_q in SHAPES:
        lines += [f"## {n_q} question{'s' if n_q > 1 else ''} × 3 options", "",
                  "Wall = at the client (this machine), p50 / p95 ms. Server = ours: parse + tokenize + GPU; Jev: time inside OpenRouter incl. Jev.", "",
                  "| text tokens | " + " | ".join(f"{n} wall p50 | {n} wall p95 | {n} server p50" for n in names) + " |",
                  "|---|" + "---|---|---|" * len(names)]
        for n_tokens in LENGTHS:
            lines.append(f"| {n_tokens:,} | " + " | ".join(f"{fmt(cell(n_tokens, n_q, n, 'wall_ms'))} | {fmt(cell(n_tokens, n_q, n, 'wall_ms', 0.95))} | "
                                                        f"{fmt(cell(n_tokens, n_q, n, 'server_ms'))}" for n in names) + " |")
        lines.append("")
    jev_tok = [(r["input_tokens"], r["cost"]) for r in ok if r["endpoint"] == "jev" and r.get("cost")]
    if jev_tok:
        per_m = 1e6 * sum(c for _, c in jev_tok) / sum(t for t, _ in jev_tok)
        lines += [f"Jev price: ${per_m:.4f} per million input tokens (reported cost / reported input tokens).", ""]
    for f in sorted(OUT.glob("throughput*.json")):
        t = json.loads(f.read_text())
        lines += [f"## Batched throughput, ours ({f.stem}): {t['meta']['gpu']}, {t['meta']['architecture']}{', merged LoRA' if t['meta'].get('merged') else ''}", "",
                  f"Cost per 1,000 requests at ${a.gpu_price}/h, GPU fully busy; Jev = its reported cost for the same requests (median).", "",
                  "| text tokens | questions | requests/s | ours $ / 1K requests | Jev $ / 1K requests |", "|---|---|---|---|---|"]
        for r in t["rows"]:
            jev = cell(r["text_tokens"], r["questions"], "jev", "cost")
            lines.append(f"| {r['text_tokens']:,} | {r['questions']} | {r['requests_per_s']:.1f} | {1e3 * a.gpu_price / 3600 / r['requests_per_s']:.4f} | "
                         f"{'—' if jev is None else f'{1e3 * jev:.4f}'} |")
        lines.append("")
    (OUT / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sweep")
    p.add_argument("--ours", action="append", default=[], metavar="NAME=URL", help="our server(s), e.g. ours=http://127.0.0.1:8765")
    p.add_argument("--box", help="GPU box host, for the round-trip measurement")
    p.add_argument("--reps", type=int, default=10)
    p.add_argument("--budget", type=float, default=0.25, help="stop if Jev spend passes this many USD")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--name", default="requests", help="output reports/latency/<name>.jsonl (report pools every requests*.jsonl)")
    p = sub.add_parser("throughput")
    p.add_argument("--adapter", default="runs/tree_4b/adapter")
    p.add_argument("--merge", action="store_true")
    p.add_argument("--vllm", metavar="MERGED_DIR", help="vLLM backend on a merged checkpoint (vllm_tree.py) instead of transformers")
    p.add_argument("--batch", type=int, default=64, help="requests per timed batch")
    p.add_argument("--max-batch-tokens", type=int, default=32768)
    p.add_argument("--seed", type=int, default=1)
    p = sub.add_parser("report")
    p.add_argument("--gpu-price", type=float, default=1.006, help="$/h of the GPU box (g5.xlarge on-demand)")
    a = ap.parse_args()
    {"sweep": sweep, "throughput": throughput, "report": report}[a.cmd](a)
