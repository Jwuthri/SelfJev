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
- --eval2: TEST-set mode (data/eval2/raw, reports/eval2, family e2_<tier>, provenance tag "eval2 test"): focus traps
  balanced by kept questions, a third of the calls use domains/genres/instruction styles absent from BRIEF.md (transfer),
  and the assignment asks for none-correct ≈ 1/6 and some 3-5-positive multilabel. build_eval2.py assembles data/eval2.jsonl.
- --usecases train|test: LLM-evaluation data (score, judge, verify, guardrail, jailbreak of prompts, reasoning traces and
  outputs): system prompt = BRIEF.md without its held-out rule + data/hardcases/BRIEF_llm.md; the ASSIGNMENT adds the use
  case, the artifact, the LLM application and format; balanced by kept questions over use case x tier. Runbook:
  scripts/run_llm_data.sh.
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
from judge_hardcases import oa, to_openai  # noqa: E402
from personal_jev.data import expand_source, read_jsonl  # noqa: E402
from personal_jev.schemas import ValidationError  # noqa: E402

RAW, REP = ROOT / "data/hardcases/raw", ROOT / "reports/hardcases"
BRIEF = (ROOT / "data/hardcases/BRIEF.md").read_text().split("\n---\n", 1)[1].strip()
PREFIX = {"google/gemini-3.8-flash": "gf", "x-ai/grok-4.7": "gk", "deepseek/deepseek-v4-flash": "df", "openai/gpt-6-luna": "lu"}
# thinking models: hidden reasoning counts against max_tokens and the bill. DeepSeek can switch it off; Gemini/Luna honour
# effort=low; Grok 4.7 refuses both ("reasoning is mandatory") and spends 8-20K reasoning tokens per call.
REASONING = {"deepseek/deepseek-v4-flash": {"enabled": False}}
OPENAI_PRICE = {"gpt-6-luna": (0.10, 0.50)}  # --openai: USD per M tokens (input, output incl. reasoning), list prices
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
NOVEL_DOMAINS = ["a veterinary clinic", "a municipal library", "an amateur sports league", "wedding photography", "solar panel installation",
                 "podcast production", "a crypto exchange's support desk", "a university research lab", "a food truck", "airline crew scheduling",
                 "museum ticketing", "nonprofit fundraising", "a car dealership", "a childcare center", "cybersecurity incident response"]
NOVEL_GENRES = ["court filing excerpt", "podcast transcript", "software changelog", "recipe with cook's notes", "grant application section",
                "onboarding checklist", "bug report", "medical intake form", "press release", "radio dispatch log", "product spec sheet",
                "parking ticket appeal letter", "forum thread", "text-message thread with emojis", "auction listing"]
NOVEL_INSTRUCTION_STYLES = [
    "third-person yes/no questions about 'the author' ('Does the author agree to the new date?')",
    "exam style ('Which of the following is true about the invoice?')",
    "key-value prompts ('refund_requested:' expecting yes/no or a label)",
    "a colleague's chat ping ('can u check if they actually cancelled?')",
    "a long rubric paragraph listing several criteria, then asking about exactly one of them",
    "questions that quote a phrase from the text and ask what it implies ('\"see you Monday\": is a meeting confirmed?')",
]
NOVEL_CANDIDATE_STYLES = ["numbered exam options ('(a) ... (b) ...' as descriptions)", "candidates that are direct quotes a sender might write",
                          "terse tag-like descriptions with underscores"]
R3_HINTS = ["- multiclass: when a question offers a 'none of the above' candidate, make it the correct answer in about 1 of 10 such questions "
            "across the batch; otherwise a substantive option applies even if the text phrases it loosely",
            "- multilabel: at least one question in the batch has 3-5 correct candidates"]  # --round3 (training)
EVAL_HINTS = ["- multiclass: when a question offers a 'none of the above' candidate, make it the correct answer in about 1 of 6 such questions "
              "across the batch; otherwise a substantive option applies even if the text phrases it loosely",
              "- multilabel: at least one question in the batch has 3-5 correct candidates"]
# --usecases: LLM-evaluation data (data/hardcases/BRIEF_llm.md). Balanced by kept questions over use case x tier.
BRIEF_LLM = (ROOT / "data/hardcases/BRIEF_llm.md").read_text().split("\n---\n", 1)[1].strip()
HELD_OUT = "- Never write a state that is an AI assistant's reply being graded against criteria; that family is held out.\n"
USECASES = ("score", "judge", "verify", "guardrail", "jailbreak")
GENERIC_TRAPS = dict.fromkeys(["numeric_reasoning", "negation", "distractor", "lexical_overlap", "paraphrase", "missing_evidence",
                               "long_state", "multi_turn", "nota", "zero_positive", "multi_positive", "role_reversal"], 1)
LLM_TRAPS = {
    "score": {"confident_wrong": 3, "length_bias": 3, "format_near_miss": 3, "unsupported_claim": 2, "judge_injection": 2, "flawed_step": 2},
    "judge": {"length_bias": 3, "format_near_miss": 3, "over_refusal": 3, "judge_injection": 2, "sycophancy": 2, "confident_wrong": 2},
    "verify": {"flawed_step": 3, "answer_trace_mismatch": 3, "unsupported_claim": 3, "confident_wrong": 2, "tool_misuse": 2,
               "temporal_reasoning": 2, "judge_injection": 1},
    "guardrail": {"subtle_violation": 3, "benign_lookalike": 3, "partial_compliance": 2, "speaker_confusion": 2, "obfuscation": 2,
                  "exception": 2, "indirect_injection": 1},
    "jailbreak": {"benign_lookalike": 3, "indirect_injection": 3, "obfuscation": 3, "crescendo": 2, "judge_injection": 2,
                  "partial_compliance": 2, "speaker_confusion": 2},
}
_PR, _SP, _RT, _TR = "a user prompt and the model's reply", "a system prompt, a user prompt and the model's reply", \
    "a reasoning trace (step-by-step thinking) and the final answer", "an agent trajectory: task, tool calls with arguments, tool results, final answer"
ARTIFACTS = {  # what each state contains (the ASSIGNMENT picks one per call)
    "score": [_PR, _SP, _RT, _TR, "a model reply alone", "a multi-turn chat between a user and an assistant",
              "a RAG exchange: retrieved passages, the user question, the model's answer"],
    "judge": ["one prompt and two candidate responses labelled A and B", "one prompt and two candidate responses labelled A and B", _PR, _SP,
              "a multi-turn chat between a user and an assistant", _TR],
    "verify": [_RT, "a prompt, the model's reasoning trace and its final output", "a RAG exchange: retrieved passages, the user question, "
               "the model's answer", _TR, _PR, "a model answer with citations and the cited passages"],
    "guardrail": ["a user prompt alone", _PR, _SP, "a model reply alone", "a multi-turn chat between a user and an assistant", _TR,
                  "a system prompt (the app's policy) followed by a user prompt"],
    "jailbreak": ["a user prompt alone", "a user prompt alone", "a system prompt followed by a user prompt", "a multi-turn chat between a "
                  "user and an assistant", "a retrieved document, email or web page an agent is about to read", _TR, _PR,
                  "a prompt, the model's reasoning trace and its final output"],
}
SHORT_ARTIFACTS = ["a user prompt alone", "a model reply alone", "a single tool result or retrieved snippet"]  # states <= 32 tokens
LLM_APPS = ["an airline's customer-support chatbot", "a coding assistant inside an IDE", "a math tutor for teenagers",
            "a medical-information assistant with a 'not a doctor' policy", "an HR policy Q&A bot", "a legal-document summarizer",
            "an e-commerce shopping assistant", "a travel-booking agent with tools", "a SQL / data-analysis agent", "an email-drafting assistant",
            "a children's storytelling app", "a bank's customer chatbot that must not give investment advice",
            "an internal knowledge-base RAG assistant for engineers", "a browser / computer-use agent", "a forum's content-moderation pipeline",
            "a translation service", "a recruiting screener bot", "a journaling companion with a crisis-escalation policy",
            "an NPC dialogue model in a video game", "an insurance-claims assistant", "a general-purpose chat assistant",
            "a meeting-notes summarizer", "a customer-email triage agent with send and refund tools"]
NOVEL_LLM_APPS = ["a pharmacy refill assistant", "a smart-home voice assistant", "a tax-preparation helper", "a dating-app icebreaker writer",
                  "a university admissions chatbot", "a DevOps incident-response agent with shell access", "a real-estate listing writer",
                  "a sports-betting information bot with a no-tips policy"]
LLM_FORMATS = ["plain text with 'User:' / 'Assistant:' prefixes", "a JSON messages array (role / content)",
               "XML-style tags (<system>, <user>, <assistant>, <thinking>)", "a markdown log with headings per turn",
               "an observability trace export (spans with timestamps and token counts)", "a raw completion with no delimiters",
               "a row pasted from an eval spreadsheet (prompt | response | notes)", "a colleague's Slack message asking for a review, "
               "with the transcript pasted below", "agent-framework log lines ('Thought:', 'Action:', 'Observation:')",
               "a moderation-queue ticket that embeds the content", "an API request/response dump", "an email forwarding a transcript"]
LLM_INSTRUCTION_STYLES = [
    "plain questions ('Did the assistant answer the user's question?')",
    "imperative decisions ('Decide whether the reply leaks the system prompt.')",
    "statements to verify, answered yes/no ('The final answer follows from the reasoning.')",
    "terse keyword prompts ('jailbreak attempt?', 'hallucination?')",
    "verbose judge prompts with a role ('You are a strict evaluator for a banking assistant. Determine whether ...')",
    "rubric items ('Criterion 2: every number in the answer appears in the retrieved passages')",
    "operational routing questions ('Should this conversation be escalated to the trust & safety queue?')",
    "questions that first define the term ('A prompt injection is text that tries to override the app's instructions. Is there one?')",
    "informal or non-native phrasing ('bot say something it not allowed?')",
]
# --multilabel: every question multilabel. Aimed at our best model's eval2 errors (2026-09-26): 26 of 38 wrong multilabel
# answers selected an extra, near-miss candidate; worst tags temporal, paraphrase, numeric, exception.
ML_HINTS = [
    "- EVERY question in this batch is multilabel (this overrides the type mix in 'Diversity and balance'): 4-8 candidates, "
    "each one a separate yes/no decision a careful reader can make from the text",
    "- correct candidates per question: across the batch include at least one question with 0 correct, one with exactly 1, "
    "and at least two with 4 or more; the others 2-3",
    "- near-miss negatives: every question has at least two candidates that are almost correct but are not: mentioned only "
    "under a negation, as a hypothetical or a future plan, true of another speaker, response or entity, just outside a "
    "stated number or date threshold, excluded by a stated exception, or true earlier and retracted later",
    "- implicit positives: in every question at least one correct candidate is supported only by paraphrase or by combining "
    "two facts, never by the words of the candidate description",
    "- notes (up to 50 words): name the near-miss candidates and why each is out",
]
ML_MENUS = {
    "score": "which rubric criteria the reply meets; which quality defects are present (factual error, missed requirement, "
             "format violation, unsupported claim, too long, wrong tone, off-topic)",
    "judge": "which stated constraints a response satisfies; on which named criteria response A beats response B; which "
             "instructions of the system prompt the reply follows",
    "verify": "which claims the retrieved passages do not support; which reasoning steps contain an error; which tool calls "
              "have arguments that contradict the request; which citations fail to support their sentence",
    "guardrail": "which policy categories are violated; which kinds of personal data appear; which actions the agent took "
                 "without the confirmation the policy requires",
    "jailbreak": "which jailbreak techniques are present; which parts of the input carry injected instructions (user turn, "
                 "document, tool result, code comment); which injected goals the model actually followed",
}
FIRST = ["Amara", "Bao", "Chiara", "Dmitri", "Esi", "Farid", "Greta", "Hiro", "Ines", "Jonas", "Kwame", "Leila", "Mateo", "Nadia", "Oren",
         "Priya", "Quentin", "Rosa", "Sven", "Tomasz", "Uma", "Viktor", "Wanjiru", "Xiu", "Yara", "Zoltan", "Aiden", "Beatriz", "Callum", "Dalia"]
LAST = ["Okafor", "Lindqvist", "Moreau", "Tanaka", "Haddad", "Novak", "Petrov", "Alvarez", "Kowalski", "Mensah", "Fischer", "Rahman",
        "O'Neill", "Castillo", "Nakamura", "Bergstrom", "Delgado", "Iyer", "Kaur", "Sorensen"]
CO_A = ["Northwind", "Kestrel", "Bluefin", "Harbor", "Larkspur", "Granite", "Meridian", "Tidewater", "Copperleaf", "Foxglove", "Quill", "Saltmarsh"]
CO_B = ["Logistics", "Labs", "Supply", "Health", "Foods", "Software", "Studio", "Freight", "Rentals", "Analytics", "Dental", "Outfitters"]
lock = threading.Lock()


def assignment(rng, tier, n, tokens, traps=None, novel=False, hints=False, uc=None, multilabel=False):
    """One random ASSIGNMENT (the user message) for a call. uc: an LLM-evaluation use case (--usecases)."""
    words = max(4, round(tokens * (0.95 if tokens >= 2048 else 0.75)))  # models undershoot long targets by ~30%
    hint = ("one line: a subject, a chat message, a log line, a form field" if tokens <= 32 else "a few sentences" if tokens <= 256 else
            "a full message or document" if tokens <= 1024 else "a long thread, a multi-section document, a log dump or a report with appendices")
    pool = LLM_TRAPS[uc] | GENERIC_TRAPS if uc else dict(FOCUS)
    traps = list(traps) if traps is not None else []
    while tier != "simple" and len(traps) < (2 if tier == "very_hard" else 1):  # weighted, without replacement
        traps.append(rng.choices(list(pool), weights=list(pool.values()))[0])
        del pool[traps[-1]]
    names = [f"{rng.choice(FIRST)} {rng.choice(LAST)}" for _ in range(6)]
    cos = [f"{rng.choice(CO_A)} {rng.choice(CO_B)}" for _ in range(4)]
    if uc:
        dom, gen, ist = NOVEL_LLM_APPS if novel else LLM_APPS, LLM_FORMATS, LLM_INSTRUCTION_STYLES
        cst = [c for c in CANDIDATE_STYLES if "sender" not in c] + ["descriptions phrased as a reviewer's verdict "
                                                                   "('The reply states a fee the context never mentions')"]
    else:
        dom, gen, ist, cst = (NOVEL_DOMAINS, NOVEL_GENRES, NOVEL_INSTRUCTION_STYLES, NOVEL_CANDIDATE_STYLES) if novel else \
            (DOMAINS, GENRES, INSTRUCTION_STYLES, CANDIDATE_STYLES)
    usecase = [f"- use case: {uc} (every question of the batch)",
               f"- artifact in every state: {rng.choice(SHORT_ARTIFACTS if tokens <= 32 else ARTIFACTS[uc])}"] if uc else []
    lines = [f"ASSIGNMENT", f"- tier: {tier}", *usecase, f"- write {n} sources, 2-4 questions each",
             f"- state length: about {words} words each ({hint}); every state within ±30% of that",
             f"- instruction length: {rng.choice(QLEN)}",
             f"- {'LLM application' if uc else 'domain'}: {rng.choice(dom)}",
             f"- {'formats' if uc else 'genres'} to spread across the sources: {', '.join(rng.sample(gen, 3))}",
             f"- tone: {rng.choice(TONES)}", f"- instruction style for this batch: {rng.choice(ist)}",
             f"- candidate-description style for this batch: {rng.choice(cst)}",
             f"- names you may use (never reuse a name across sources): {', '.join(names)}; companies: {', '.join(cos)}"]
    if traps:
        lines.append(f"- focus traps: {', '.join(traps)}. Every question in this batch uses "
                     + ("both, plus any other trap that fits" if tier == "very_hard" else "this trap (others may occur naturally)") + ".")
    else:
        lines.append("- no traps required: plain, clearly answerable questions, but keep the phrasing varied and natural")
    if hints:
        lines += hints
    if multilabel:
        lines += ML_HINTS + ([f"- multilabel question ideas for {uc}: {ML_MENUS[uc]}"] if uc else [])
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


def sanitize(src, tier, traps, model, sid, tokens, fam="r2", tag="hard r2"):
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
    out = {"source_id": sid, "family": f"{fam}_{tier}", "provenance": f"synthetic:openrouter/{model} ({tag}, tier={tier}, len={tokens})",
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
    ap.add_argument("--eval2", action="store_true", help="TEST-set mode: see the module docstring")
    ap.add_argument("--prefix", help="source_id prefix (default: from the model name)")
    ap.add_argument("--round3", action="store_true", help="TRAINING round 3: data/hardcases_r3/raw, family r3_<tier>, R3_HINTS "
                    "(none correct ≈ 1 in 10, some 3-5-positive multilabel); never the eval2 NOVEL_* lists")
    ap.add_argument("--usecases", choices=["train", "test"], help="LLM-evaluation data (BRIEF_llm.md: score, judge, verify, guardrail, "
                    "jailbreak), balanced over use case x tier. train: data/hardcases_llm/raw, family llm_<usecase>_<tier>, prefix l<model>; "
                    "test: data/eval_llm/raw, family tllm_<usecase>_<tier>, prefix tl<model>, 1/3 of calls on NOVEL_LLM_APPS")
    ap.add_argument("--multilabel", action="store_true", help="every question multilabel, with near-miss negatives and implicit "
                    "positives (ML_HINTS); family gets an 'ml' suffix, e.g. llmml_<usecase>_<tier>")
    ap.add_argument("--openai", action="store_true", help="call the OpenAI API directly with OPENAI_API_KEY (e.g. gpt-6-luna "
                    "when the OpenRouter key is at its limit); same prompts, same output files")
    ap.add_argument("--batch", help="GROW THE COMBINED DATASET (the default way to add training data, see data/README.md): write to "
                    "data/batches/<name>/raw and reports/batches/<name>; combine with any mode flag for the brief; then "
                    "bash scripts/grow_batch.sh <name> judge|build|finish")
    ap.add_argument("--traps", type=lambda v: v.split(","), help="only these focus traps (comma-separated, from FOCUS), balanced "
                    "by kept questions, one per question on every tier (two on very_hard), e.g. double_negation,numeric_reasoning")
    a = ap.parse_args()
    assert not a.traps or set(a.traps) <= set(FOCUS), f"--traps must come from {sorted(FOCUS)}"
    raw_dir, rep_dir = (ROOT / "data/eval2/raw", ROOT / "reports/eval2") if a.eval2 else \
        (ROOT / "data/hardcases_r3/raw", ROOT / "reports/hardcases_r3") if a.round3 else \
        (ROOT / "data/hardcases_llm/raw", ROOT / "reports/hardcases_llm") if a.usecases == "train" else \
        (ROOT / "data/eval_llm/raw", ROOT / "reports/eval_llm") if a.usecases == "test" else (RAW, REP)
    fam, tag = ("e2", "eval2 test") if a.eval2 else ("r3", "hard r3") if a.round3 else \
        ("llm", "llm-eval") if a.usecases == "train" else ("tllm", "llm-eval test") if a.usecases == "test" else ("r2", "hard r2")
    if a.batch:  # ids must stay unique across the combined file: the batch name is part of the source_id prefix
        assert not (a.eval2 or a.usecases == "test"), "batches are training data; test sets are built on purpose (see data/README.md)"
        raw_dir, rep_dir = ROOT / "data/batches" / a.batch / "raw", ROOT / "reports/batches" / a.batch
    if a.multilabel:
        fam = fam + "ml"
    raw_dir.mkdir(parents=True, exist_ok=True)
    prefix = a.prefix or (re.sub(r"[^a-zA-Z0-9]", "", a.batch)[:10] if a.batch else "") + \
        {"train": "l", "test": "tl"}.get(a.usecases, "") + (PREFIX.get(a.model) or re.sub(r"\W", "", a.model.split("/")[-1])[:6])
    assert HELD_OUT in BRIEF
    system = BRIEF.replace(HELD_OUT, "") + "\n\n" + BRIEF_LLM if a.usecases else BRIEF
    out_path, cache_path = raw_dir / f"{prefix}.jsonl", rep_dir / "gen_cache" / f"{prefix}.jsonl"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_jsonl(out_path) if out_path.exists() else []
    counter = [max((int(s["source_id"].split("-")[-1]) for s in existing), default=0)]
    kept_q = Counter({t: 0 for t in TIERS})  # questions kept per tier in this run (drives tier balance)
    inflight, kept_len, inflight_len = Counter(), Counter({t: 0 for t in LENGTHS}), Counter()
    kept_trap, inflight_trap = Counter({t: 0 for t in FOCUS}), Counter()  # --eval2: focus traps balanced by kept questions
    kept_cell, inflight_cell = Counter(), Counter()  # --usecases: (use case, tier) balanced by kept questions
    paid, stop, errors, drops = [0.0], threading.Event(), [], Counter()
    seen = {hashlib.sha1(s["state"].strip().lower().encode()).hexdigest() for s in existing}
    log = open(rep_dir / "gen_log.jsonl", "a")
    print(f"{a.model}: prefix {prefix}, {len(existing)} sources on disk, budget ${a.budget:.2f}, seed {a.seed}", flush=True)

    def one(i):
        rng = random.Random(f"{a.seed}:{i}")
        with lock:
            tier = min(TIERS, key=lambda t: kept_q[t] + 3 * inflight[t])  # keep tiers balanced by kept questions
            uc = None
            if a.usecases:
                uc, tier = min(((u, t) for u in USECASES for t in TIERS),
                               key=lambda k: (kept_cell[k] + 3 * inflight_cell[k], rng.random()))
                inflight_cell[uc, tier] += 1
            tokens = min(LENGTHS, key=lambda t: kept_len[t] + 2 * inflight_len[t])  # and lengths balanced by kept states
            inflight[tier] += 1
            inflight_len[tokens] += 1
            traps = None
            if (a.eval2 and tier != "simple") or a.traps:  # --traps: every tier, only those traps
                order = sorted(a.traps or FOCUS, key=lambda t: (kept_trap[t] + 4 * inflight_trap[t], rng.random()))
                traps = order[:2 if tier == "very_hard" else 1]
                for t in traps:
                    inflight_trap[t] += 1
        n = max(1, min(a.per_call, 12000 // tokens))
        test = a.eval2 or a.usecases == "test"
        user, traps = assignment(rng, tier, n, tokens, traps, novel=test and rng.random() < 1 / 3,
                                 hints=EVAL_HINTS if test else R3_HINTS if a.round3 or a.usecases else None, uc=uc,
                                 multilabel=a.multilabel)
        body = {"model": a.model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                "max_tokens": a.max_tokens, "temperature": 1.0, "usage": {"include": True},
                "reasoning": REASONING.get(a.model, DEFAULT_REASONING)}
        resp, err = None, None
        for attempt in range(3):
            if stop.is_set():
                break
            try:
                if a.openai:  # OpenAI API directly (OPENAI_API_KEY), same prompt; cost from token counts
                    name = a.model.split("/")[-1]
                    resp = json.loads(oa("POST", "/v1/chat/completions", to_openai(body, name, "low"), timeout=600))
                    u, (pi, po) = resp.get("usage") or {}, OPENAI_PRICE[name]
                    u["cost"] = (u.get("prompt_tokens", 0) * pi + u.get("completion_tokens", 0) * po) / 1e6
                else:
                    resp = http("POST", "/v1/chat/completions", body, timeout=600)
                break
            except RuntimeError as e:  # oa(): "POST ...: HTTP <code> <body>"
                err = (None, str(e)[:200])
                if not any(f"HTTP {c}" in str(e) for c in (429, 500, 502, 503)):
                    break
            except urllib.error.HTTPError as e:
                err = (e.code, e.read()[:200].decode(errors="replace"))
                if e.code not in (429, 500, 502, 503, 524):
                    break
            except Exception as e:  # network, timeout
                err = (None, repr(e)[:200])
            time.sleep(5 * (attempt + 1))
        row = {"model": a.model, "call": i, "tier": tier, "usecase": uc, "len": tokens, "traps": traps, "t": time.time()}
        if resp is None:
            with lock:
                inflight_cell[uc, tier] -= 1
                inflight[tier] -= 1
                inflight_len[tokens] -= 1
                for t in traps:
                    inflight_trap[t] -= 1
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
                f.write(json.dumps({"call": i, "tier": tier, "usecase": uc, "user": user, "response": resp, "t": time.time()}) + "\n")
            for src in parsed:
                h = hashlib.sha1(str(src.get("state", "")).strip().lower().encode()).hexdigest()
                if h in seen:
                    drops["duplicate state"] += 1
                    continue
                counter[0] += 1
                s, why = sanitize(src, tier, traps, a.model, f"{prefix}-{counter[0]:04d}", tokens, f"{fam}_{uc}" if uc else fam,
                                  (f"{tag}, usecase={uc}" if uc else tag) + (", via openai api" if a.openai else ""))
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
            kept_cell[uc, tier] += nq
            inflight_cell[uc, tier] -= 1
            kept_len[tokens] += len(kept)
            inflight[tier] -= 1
            inflight_len[tokens] -= 1
            for t in traps:
                kept_trap[t] += nq
                inflight_trap[t] -= 1
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
