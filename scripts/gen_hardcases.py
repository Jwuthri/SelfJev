"""Round-2 hard-case TRAINING data through OpenRouter -> data/hardcases/raw/<prefix>.jsonl (one file per model).

  zsh -ic 'uv run python scripts/gen_hardcases.py --model google/gemini-3.8-flash --budget 10'
  zsh -ic 'uv run python scripts/gen_hardcases.py --model x-ai/grok-4.7 --budget 10 --max-questions 5000'

- System prompt = data/hardcases/BRIEF.md (after its '---'). Each call also gets a random ASSIGNMENT: difficulty
  tier, focus traps, domain, genres, tone, instruction style, candidate-description style, invented names. The
  tier is chosen to keep kept questions at 1/3 simple, 1/3 hard, 1/3 very_hard.
- Every row's provenance names the model: "synthetic:openrouter/<model> (hard r2, tier=<tier>)"; family = r2_<tier>.
- Stops at --budget USD (OpenRouter charge + BYOK upstream cost, re-checked against the account after every wave)
  or --max-questions. Resumable: source_id counters continue from the files on disk.
- Raw responses: reports/hardcases/gen_cache/<prefix>.jsonl. Per-call log: reports/hardcases/gen_log.jsonl.
- Labels are LLM-intended. judge_hardcases.py re-labels blind; build_hardcases.py keeps only agreements.
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import random
import re
import sys
import threading
import time
import urllib.error
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
from compare_external import call_cost, http  # noqa: E402
from personal_jev.data import expand_source, read_jsonl  # noqa: E402
from personal_jev.schemas import ValidationError  # noqa: E402

RAW, REP = ROOT / "data/hardcases/raw", ROOT / "reports/hardcases"
BRIEF = (ROOT / "data/hardcases/BRIEF.md").read_text().split("\n---\n", 1)[1].strip()
PREFIX = {"google/gemini-3.8-flash": "gf", "x-ai/grok-4.7": "gk", "deepseek/deepseek-v4-flash": "df", "openai/gpt-6-luna": "lu"}
# thinking models: hidden reasoning counts against max_tokens and the bill. DeepSeek can switch it off; Gemini/Luna honour
# effort=low; Grok 4.7 refuses both ("reasoning is mandatory") and spends 8-20K reasoning tokens per call.
REASONING = {"deepseek/deepseek-v4-flash": {"enabled": False}}
DEFAULT_REASONING = {"effort": "low", "exclude": True}
TIERS = ("simple", "hard", "very_hard")
LENGTHS = (8, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192)  # target state tokens, balanced by kept states
QLEN = ("very short (3-8 words)", "medium (10-25 words)", "long (30-80 words, with a sentence of context or a definition)")
# focus traps, weighted by the gap to Jev on the test set (reports/external/failures.md)
FOCUS = {"sarcasm": 3, "numeric_reasoning": 3, "role_reversal": 3, "injection": 2, "paraphrase": 2, "distractor": 2,
         "lexical_overlap": 2, "long_state": 2, "negation": 2, "temporal_reasoning": 2, "double_negation": 1, "hypothetical": 1,
         "exception": 1, "missing_evidence": 1, "contradiction": 1, "multi_turn": 1, "nota": 1, "zero_positive": 1, "multi_positive": 1}
DOMAINS = ["e-commerce customer support", "SaaS operations and incidents", "HR and internal policy", "contracts and legal notices",
           "clinic and appointment administration", "logistics and shipping", "invoicing and accounts payable", "school and course admin",
           "property management and leases", "travel bookings", "an online gaming community", "developer tooling and CI logs",
           "public-sector permits and benefits", "hotels and restaurants", "insurance claims", "field service and repairs",
           "recruiting and job applications", "banking and card disputes", "event planning", "a small manufacturing shop"]
GENRES = ["customer chat transcript", "email thread with quoted replies", "support ticket with internal comments", "server or app log excerpt",
          "contract clause with amendments", "policy page", "invoice with line items", "meeting notes", "product review", "web form submission",
          "forwarded email with a one-line cover note", "Slack/Teams thread", "SMS exchange", "voicemail transcript", "incident postmortem",
          "spreadsheet pasted as text", "FAQ excerpt", "handwritten-style note typed up", "status update to a manager", "terms-of-service excerpt"]
TONES = ["formal", "terse with typos", "non-native English", "chatty and rambling", "angry", "overly polite", "bureaucratic", "sarcastic and dry"]
INSTRUCTION_STYLES = [
    "plain questions ('Did the customer ask for a refund?')",
    "imperative decisions ('Decide whether the customer asked for a refund.')",
    "statements to verify, answered yes/no ('The customer asked for a refund.')",
    "terse keyword prompts ('refund requested?')",
    "verbose instructions with a role and context ('You are triaging tickets for a payments team. Determine whether ...')",
    "checklist or rubric items ('Criterion 3: the message contains an explicit refund request')",
    "operational routing questions ('Should this go to the billing queue?')",
    "questions that first define the term ('A refund request means the sender explicitly asks for money back. Is there one here?')",
    "informal or non-native phrasing ('customer want refund or no?')",
]
CANDIDATE_STYLES = ["one or two words per candidate", "short noun phrases", "full sentences with a definition", "a definition plus a short example",
                    "a mix of very short and very long descriptions within the same question",
                    "descriptions phrased from the sender's point of view ('I want my money back')",
                    "descriptions that avoid the words used in the text (paraphrased)"]
FIRST = ["Amara", "Bao", "Chiara", "Dmitri", "Esi", "Farid", "Greta", "Hiro", "Ines", "Jonas", "Kwame", "Leila", "Mateo", "Nadia", "Oren",
         "Priya", "Quentin", "Rosa", "Sven", "Tomasz", "Uma", "Viktor", "Wanjiru", "Xiu", "Yara", "Zoltan", "Aiden", "Beatriz", "Callum", "Dalia"]
LAST = ["Okafor", "Lindqvist", "Moreau", "Tanaka", "Haddad", "Novak", "Petrov", "Alvarez", "Kowalski", "Mensah", "Fischer", "Rahman",
        "O'Neill", "Castillo", "Nakamura", "Bergstrom", "Delgado", "Iyer", "Kaur", "Sorensen"]
CO_A = ["Northwind", "Kestrel", "Bluefin", "Harbor", "Larkspur", "Granite", "Meridian", "Tidewater", "Copperleaf", "Foxglove", "Quill", "Saltmarsh"]
CO_B = ["Logistics", "Labs", "Supply", "Health", "Foods", "Software", "Studio", "Freight", "Rentals", "Analytics", "Dental", "Outfitters"]
lock = threading.Lock()


def assignment(rng, tier, n, tokens):
    """One random ASSIGNMENT (the user message) for a call."""
    words = max(4, round(tokens * (0.95 if tokens >= 2048 else 0.75)))  # models undershoot long targets by ~30%
    hint = ("one line: a subject, a chat message, a log line, a form field" if tokens <= 32 else "a few sentences" if tokens <= 256 else
            "a full message or document" if tokens <= 1024 else "a long thread, a multi-section document, a log dump or a report with appendices")
    traps, pool = [], dict(FOCUS)
    while tier != "simple" and len(traps) < (2 if tier == "very_hard" else 1):  # weighted, without replacement
        traps.append(rng.choices(list(pool), weights=list(pool.values()))[0])
        del pool[traps[-1]]
    names = [f"{rng.choice(FIRST)} {rng.choice(LAST)}" for _ in range(6)]
    cos = [f"{rng.choice(CO_A)} {rng.choice(CO_B)}" for _ in range(4)]
    lines = [f"ASSIGNMENT", f"- tier: {tier}", f"- write {n} sources, 2-4 questions each",
             f"- state length: about {words} words each ({hint}); every state within ±30% of that",
             f"- instruction length: {rng.choice(QLEN)}",
             f"- domain: {rng.choice(DOMAINS)}", f"- genres to spread across the sources: {', '.join(rng.sample(GENRES, 3))}",
             f"- tone: {rng.choice(TONES)}", f"- instruction style for this batch: {rng.choice(INSTRUCTION_STYLES)}",
             f"- candidate-description style for this batch: {rng.choice(CANDIDATE_STYLES)}",
             f"- names you may use (never reuse a name across sources): {', '.join(names)}; companies: {', '.join(cos)}"]
    if traps:
        lines.append(f"- focus traps: {', '.join(traps)}. Every question in this batch uses "
                     + ("both, plus any other trap that fits" if tier == "very_hard" else "this trap (others may occur naturally)") + ".")
    else:
        lines.append("- no traps required: plain, clearly answerable questions, but keep the phrasing varied and natural")
    return "\n".join(lines), traps


def parse_sources(text):
    """JSON array -> list of dicts; a truncated array yields its complete elements ('truncated')."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1].rsplit("```", 1)[0]
    i = t.find("[")
    if i < 0:
        return [], "no array"
    try:
        v = json.loads(t[i:t.rfind("]") + 1])
        return (v if isinstance(v, list) else []), None
    except json.JSONDecodeError:
        pass
    dec, out, pos = json.JSONDecoder(), [], i + 1
    while True:
        while pos < len(t) and t[pos] in " \n\r\t,":
            pos += 1
        try:
            obj, pos = dec.raw_decode(t, pos)
            out.append(obj)
        except json.JSONDecodeError:
            return out, "truncated"


QKEYS = {"type", "instruction", "candidates", "target", "hard_cases", "notes", "paraphrase_group"}


def sanitize(src, tier, traps, model, sid, tokens):
    """Keep only known fields, fill ours, validate. Returns (source, None) or (None, reason)."""
    if not isinstance(src, dict) or not isinstance(src.get("state"), str) or not isinstance(src.get("questions"), list):
        return None, "shape"
    if len(re.findall(r"\w+", src["state"])) < 3:
        return None, "state too short"
    qs = []
    for q in src["questions"]:
        if not isinstance(q, dict):
            return None, "question shape"
        q = {k: v for k, v in q.items() if k in QKEYS}
        if q.get("type") == "binary":
            q.pop("candidates", None)
            if isinstance(q.get("target"), str) and q["target"].lower() in ("true", "false"):
                q["target"] = q["target"].lower() == "true"
        if isinstance(q.get("candidates"), list):  # some models add extra keys per candidate; keep the schema's two
            q["candidates"] = [{"id": c.get("id"), "description": c.get("description")} if isinstance(c, dict) else c for c in q["candidates"]]
        q["hard_cases"] = [h for h in (q.get("hard_cases") or []) if isinstance(h, str) and h]
        if tier != "simple" and not q["hard_cases"]:
            q["hard_cases"] = list(traps)  # the assignment said every question uses the focus trap(s)
        q["notes"] = str(q.get("notes", ""))[:300]
        qs.append(q)
    out = {"source_id": sid, "family": f"r2_{tier}", "provenance": f"synthetic:openrouter/{model} (hard r2, tier={tier}, len={tokens})",
           "state": src["state"], "questions": qs}
    try:
        expand_source(out)
    except ValidationError as e:
        return None, re.sub(r"'[^']*'", "'…'", str(e))[:80]
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--budget", type=float, required=True, help="max USD for this run")
    ap.add_argument("--max-questions", type=int, default=10 ** 9, help="stop once this many questions were kept in this run")
    ap.add_argument("--per-call", type=int, default=5, help="sources per call (fewer for long states)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-tokens", type=int, default=32000)
    ap.add_argument("--seed", type=int, default=int(time.time()))
    a = ap.parse_args()
    prefix = PREFIX.get(a.model) or re.sub(r"\W", "", a.model.split("/")[-1])[:6]
    out_path, cache_path = RAW / f"{prefix}.jsonl", REP / "gen_cache" / f"{prefix}.jsonl"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_jsonl(out_path) if out_path.exists() else []
    counter = [max((int(s["source_id"].split("-")[-1]) for s in existing), default=0)]
    kept_q = Counter({t: 0 for t in TIERS})  # questions kept per tier in this run (drives tier balance)
    inflight, kept_len, inflight_len = Counter(), Counter({t: 0 for t in LENGTHS}), Counter()
    paid, stop, errors, drops = [0.0], threading.Event(), [], Counter()
    seen = {hashlib.sha1(s["state"].strip().lower().encode()).hexdigest() for s in existing}
    log = open(REP / "gen_log.jsonl", "a")
    print(f"{a.model}: prefix {prefix}, {len(existing)} sources on disk, budget ${a.budget:.2f}, seed {a.seed}", flush=True)

    def one(i):
        rng = random.Random(f"{a.seed}:{i}")
        with lock:
            tier = min(TIERS, key=lambda t: kept_q[t] + 3 * inflight[t])  # keep tiers balanced by kept questions
            tokens = min(LENGTHS, key=lambda t: kept_len[t] + 2 * inflight_len[t])  # and lengths balanced by kept states
            inflight[tier] += 1
            inflight_len[tokens] += 1
        n = max(1, min(a.per_call, 12000 // tokens))
        user, traps = assignment(rng, tier, n, tokens)
        body = {"model": a.model, "messages": [{"role": "system", "content": BRIEF}, {"role": "user", "content": user}],
                "max_tokens": a.max_tokens, "temperature": 1.0, "usage": {"include": True},
                "reasoning": REASONING.get(a.model, DEFAULT_REASONING)}
        resp, err = None, None
        for attempt in range(3):
            if stop.is_set():
                break
            try:
                resp = http("POST", "/v1/chat/completions", body, timeout=600)
                break
            except urllib.error.HTTPError as e:
                err = (e.code, e.read()[:200].decode(errors="replace"))
                if e.code not in (429, 500, 502, 503, 524):
                    break
            except Exception as e:  # network, timeout
                err = (None, repr(e)[:200])
            time.sleep(5 * (attempt + 1))
        row = {"model": a.model, "call": i, "tier": tier, "len": tokens, "traps": traps, "t": time.time()}
        if resp is None:
            with lock:
                inflight[tier] -= 1
                inflight_len[tokens] -= 1
                errors.append(err)
                log.write(json.dumps(row | {"error": err}) + "\n"); log.flush()
            return
        cost = call_cost(resp)
        choice = (resp.get("choices") or [{}])[0]
        text = (choice.get("message") or {}).get("content") or ""
        parsed, note = parse_sources(text)
        kept = []
        with lock:
            paid[0] += cost
            with open(cache_path, "a") as f:
                f.write(json.dumps({"call": i, "tier": tier, "user": user, "response": resp, "t": time.time()}) + "\n")
            for src in parsed:
                h = hashlib.sha1(str(src.get("state", "")).strip().lower().encode()).hexdigest()
                if h in seen:
                    drops["duplicate state"] += 1
                    continue
                counter[0] += 1
                s, why = sanitize(src, tier, traps, a.model, f"{prefix}-{counter[0]:04d}", tokens)
                if s is None:
                    counter[0] -= 1
                    drops[why] += 1
                    continue
                seen.add(h)
                kept.append(s)
            with open(out_path, "a") as f:
                for s in kept:
                    f.write(json.dumps(s, ensure_ascii=False) + "\n")
            nq = sum(len(s["questions"]) for s in kept)
            kept_q[tier] += nq
            kept_len[tokens] += len(kept)
            inflight[tier] -= 1
            inflight_len[tokens] -= 1
            u = resp.get("usage") or {}
            log.write(json.dumps(row | {"cost": cost, "prompt_tokens": u.get("prompt_tokens"), "completion_tokens": u.get("completion_tokens"),
                                        "finish": choice.get("finish_reason"), "parsed": len(parsed), "kept": len(kept), "questions": nq,
                                        "note": note}) + "\n")
            log.flush()

    i, total_states = 0, 0
    with cf.ThreadPoolExecutor(a.workers) as pool:
        while not stop.is_set():
            cf.wait([pool.submit(one, j) for j in range(i, i + a.workers)])
            i += a.workers
            spent = paid[0]  # per-call cost only: the account-usage delta also counts other generators running concurrently
            nq = sum(kept_q.values())
            total_states = sum(1 for _ in open(out_path)) - len(existing) if out_path.exists() else 0
            print(f"  {a.model}: {i} calls, {total_states} states / {nq} questions kept {dict(kept_q)}, by length {dict(kept_len)}, "
                  f"spent ${spent:.2f}, errors {len(errors)}, drops {dict(drops)}", flush=True)
            if spent >= a.budget or nq >= a.max_questions or len(errors) >= 3 * a.workers:
                stop.set()
    print(f"done: {total_states} states, {sum(kept_q.values())} questions, ${paid[0]:.2f}; "
          f"errors: {errors[:3]}")


if __name__ == "__main__":
    main()
