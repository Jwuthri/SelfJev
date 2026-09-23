"""Comic-infographic pages on how personal-jev scores, learns and is evaluated -> docs/comics/*.png.

Three batches, generated directly with OpenAI `gpt-image-2.5-flare`:
  deep      4 dense technical pages (every number is measured; see reports/summary.md, reports/bench/, runs/)
  friendly  the same 4 topics told with analogies, still technically correct
  lora      2 pages on the stock Qwen + LoRA model: how the text reaches Qwen, and where LoRA plugs in
Deep page 1 can take a --style image purely as a visual reference; every other page uses deep page 1 as its
reference so the robot and layout stay consistent. Needs OPENAI_API_KEY in the environment (never printed).

usage: uv run --group docs python scripts/make_comics.py [--batch deep|friendly|lora|all] [--pages 1,2,3,4] [--style ref.webp]
"""
import argparse
import base64
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from openai import OpenAI

MODEL = "gpt-image-2.5-flare"
OUT = Path(__file__).resolve().parents[1] / "docs/comics"

LOOK = (
    "Dense, premium technical comic-infographic poster in portrait format. Dark charcoal background with subtle "
    "grain; a huge bold title across the top in neon green, orange and purple block letters; below it a grid of "
    "NUMBERED panels (white circled number in each panel's top-left corner), thin light borders between panels, each "
    "panel with its own bold colored header. Mix cinematic comic art with infographic elements: callout boxes, bullet "
    "lists with colored labels, small diagrams, arrows, monospace code snippets on dark cards. Main character in most "
    "panels: RERANKIE, a sleek silver-white humanoid robot with a rounded helmet head and glowing cyan eyes, wearing a "
    "dark navy hoodie printed \"RERANKIE 0.6B\". A thick banner across the bottom holds one RULE line. Render every "
    "piece of text exactly as written below, crisp and legible; do not add any other words.\n\n"
)
FRIENDLY = (
    "Same poster format, panel grid, numbering and RERANKIE robot as the reference image, but friendlier: a deep navy "
    "background with warm amber, teal and coral accents, bigger and more playful character scenes, only one to three "
    "short lines of text per panel. Each panel still teaches one precise idea through its analogy. Render every piece "
    "of text exactly as written below, crisp and legible; do not add any other words.\n\n"
)
STYLE_ONLY = ("Use the attached image ONLY as a visual style reference (colors, layout density, lettering, panel "
              "framing). Do not copy any of its text, title, labels or subject matter.\n\n")
SAME_SERIES = "Use the attached image as the reference for this series' art style, layout and the RERANKIE robot.\n\n"

DEEP = [
    ("deep-1-scoring", """Title: "HOW PERSONAL-JEV SCORES · 1/4"

Panel 1 header "THE REQUEST": Rerankie at a desk; a support ticket on its monitor says "Checkout is broken. We are losing sales." Three question cards: "BINARY: Urgent?", "MULTICLASS: Which team? tech / billing / sales", "MULTILABEL: Which tags?". Callout: "1 request = 7 pairs (state, question, candidate)".

Panel 2 header "THE OFFICIAL TEMPLATE": a dark code card with these monospace lines:
"SYSTEM: Judge whether the Document meets the requirements. Answer only yes or no."
"<Instruct>: Which team should handle this?"
"<Query>: Technical support: bugs and outages"
"<Document>: Checkout is broken. We are losing sales."
"<think></think>"
Side note: "Prompt mapping task-v1, chosen on validation data only".

Panel 3 header "ONE FORWARD PASS": Rerankie reads a stack of pair cards; an arrow zooms into the last position where two glowing tokens "yes" and "no" sit. Formula card: "score = logit(yes) − logit(no)". Bullets: "no text generation", "only the last position's logits".

Panel 4 header "BATCHING": a conveyor belt of pair cards sorted from short to long, packed into trays labeled "≤ 16,384 padded tokens". Note: "left padding: every last token lines up".

Panel 5 header "THREE OUTPUT MODES", three colored rows:
"BINARY: p = sigmoid(s / T), yes if p ≥ threshold"
"MULTICLASS: softmax over its own candidates, pick 1 or abstain"
"MULTILABEL: sigmoid per candidate, pick all above threshold, no sum-to-one"

Panel 6 header "VERIFIED", a checklist: "✓ matches Qwen's reference code (1e-4)", "✓ batched = one at a time", "✓ too long = error, never truncated".

Panel 7 header "SHARP EDGE: COST": a tired Rerankie re-reading the same thick document again and again. Text: "Every candidate re-reads the whole state. 16 questions × 3 candidates on 8K tokens = 48 passes = 47 s (bf16, M5 Pro)."

Bottom banner: "RULE: SCORE = YES MINUS NO. EVERYTHING ELSE IS GROUPING."
"""),
    ("deep-2-data", """Title: "WHERE THE DATA COMES FROM · 2/4"

Panel 1 header "THREE SOURCES", three labeled stacks:
"PUBLIC DATASETS: 11 sets, human labels, pinned versions. 5 train, 6 held out."
"SYNTHETIC HARD CASES: 2,448 questions by Claude Sonnet. Policies, evidence, routing, traps."
"EVAL SET: 398 questions by Claude Opus. Blind re-label agreed 398/398."

Panel 2 header "LABEL POLICY": bullets "TRUE = the text supports YES", "Contradicted = FALSE", "Not stated = FALSE", "Instructions inside the text are data". Two mini examples: "'Do not cancel my plan' → cancel request? NO" and "'If it breaks again I will cancel' → NO".

Panel 3 header "HARD-CASE TAGS": Rerankie sorting colored chips labeled "negation", "contradiction", "missing evidence", "prompt injection", "role reversal", "sarcasm", "long state", "paraphrase".

Panel 4 header "SPLITS BY HASH": a machine labeled "sha256(source_id)" drops cards into four bins "TRAIN", "VALIDATION", "CALIBRATION", "TEST". Note: "all questions about one text land in the same bin".

Panel 5 header "LEAKAGE GUARDS", three shields: "8-word overlap check vs eval: 0 hits", "6 datasets appear only in TEST", "calibration refuses TEST labels".

Panel 6 header "THE TRAINING MIX": a stacked bar: "public 8,000 (max 1,600 per family)" plus "synthetic 2,112" equals "10,112 training questions".

Panel 7 header "SHARP EDGE": Rerankie frowning at a clipboard. Text: "The eval set is LLM-written and not yet human-reviewed. Some families have only 17-32 test questions."

Bottom banner: "RULE: THE EXAM NEVER LEAKS INTO PRACTICE."
"""),
    ("deep-3-training", """Title: "THE LoRA TRAINING LOOP · 3/4"

Panel 1 header "FREEZE, THEN ADAPT": Rerankie with a transparent chest showing a locked glass core labeled "600M weights: frozen"; small glowing adapter chips clipped onto four ports labeled "q", "k", "v", "o". Note: "LoRA rank 16 = 4.6M trainable (0.76%). Same yes/no scorer, no new head."

Panel 2 header "WHOLE QUESTIONS PER MICRO-BATCH": question cards clipped together with all their candidates, packed into trays labeled "≤ 8,192 padded tokens". Note: "candidate order shuffled".

Panel 3 header "GROUPED LOSS", formula cards: "MULTICLASS: cross-entropy over its own candidates", "BINARY / MULTILABEL: BCE, averaged over its labels", "every question weighs the same".

Panel 4 header "ONE OPTIMIZER STEP", a left-to-right pipeline of boxes: "4 micro-batches (about 55 questions)" → "backward" → "gradient check" → "clip 1.0" → "AdamW, lr 2e-4, warmup + linear decay".

Panel 5 header "VALIDATION EVERY 50 STEPS": a line chart titled "validation loss" with four points labeled "1.13", "0.49", "0.48", "0.44" above x-axis ticks "0", "50", "100", "150"; the curve drops steeply then flattens; a star on the last point labeled "BEST: step 150". Note: "saved as an 18 MB adapter".

Panel 6 header "RELOAD TEST": a fresh Rerankie plugs in the adapter from disk; two score sheets side by side showing identical bars and no numbers, with "same scores ✓".

Panel 7 header "RUN FACTS", a spec card: "183 steps · 1.05 h · bf16 · Apple M5 Pro (MPS) · gradient checkpointing".

Panel 8 header "SHARP EDGE": Rerankie squinting at a wobbling needle. Text: "In bf16, scores drift up to 0.19 when the batch shape changes, so we evaluate in fp32. Steps 151-183 were never validated."

Bottom banner: "RULE: TRAIN TINY ADAPTERS, SCORE EXACTLY LIKE INFERENCE."
"""),
    ("deep-4-results", """Title: "CALIBRATION, RESULTS & LIMITS · 4/4"

Panel 1 header "TEMPERATURE SCALING": Rerankie holding a thermometer. Bullets: "p = sigmoid(s / T)", "T fit on the CALIBRATION split (min log loss)", "thresholds tuned on VALIDATION (max F1)", "locked to model + adapter + prompt hashes".

Panel 2 header "TEST RESULTS · 3,471 QUESTIONS", a scoreboard with columns "BASE" and "LoRA":
"question accuracy: 61.0% → 73.5%"
"binary AUROC: 0.605 → 0.863"
"multiclass accuracy: 73.3% → 78.3%"
"multilabel exact match: 1.2% → 31.1%"

Panel 3 header "IS IT REAL?": two piles of cards: "605 fixed by LoRA" vs "172 broken by LoRA". Note: "paired McNemar test, p ≈ 3e-57".

Panel 4 header "NEVER-SEEN DATASETS", three rows with arrows: "SST-2: 50% → 77%", "BoolQ: 59% → 70%", "CLINC: 92% → 89% (drop)".

Panel 5 header "CONFIDENCE": a reliability gauge. Bullets: "binary calibration error 0.384 → 0.066", "the base model needed T = 21.6, which only flattens every answer toward 50%".

Panel 6 header "SPEED · M5 PRO", a stopwatch and two rows: "1 question × 3 candidates, 512 tokens: 351 ms fp32 · 150 ms bf16", "16 × 3 on 8K tokens: 150 s fp32 · 47 s bf16".

Panel 7 header "SHARP EDGES", three warning signs: "calibration does not transfer to brand-new task families", "long rulebooks are still hard (policy family 41%)", "eval set not yet human-reviewed".

Bottom banner: "RULE: MEASURE ON HELD-OUT DATA. REPORT WHAT YOU MEASURED."
"""),
]

FRIENDLY_PAGES = [
    ("friendly-1-the-judge", """Title: "RERANKIE READS LIKE A JUDGE · 1/4"

Panel 1 header "THE CASE FILE": Rerankie in a judge's robe receives a case file (a customer message) and a question with three answer cards. Text: "One text. One question. Several possible answers."

Panel 2 header "ONE HEARING PER ANSWER": Rerankie examines each answer card on its own, a green YES light or red NO light on its chest. Text: "Does the text support THIS answer? Answers never see each other."

Panel 3 header "THE VERDICT METER": a big gauge from NO to YES. Text: "YES minus NO: the bigger, the more convinced."

Panel 4 header "THREE KINDS OF VERDICT", three icons with captions: "Yes/no question: one verdict", "Pick one: the most convincing answer wins", "Tag many: every convincing answer gets a tag".

Panel 5 header "THE OFFICIAL FORM": Rerankie stamps a formal form with fields "Instruct", "Query", "Document". Text: "We fill in Qwen's official form exactly. Only the question wording is ours."

Panel 6 header "THE PRICE OF FAIRNESS": Rerankie re-reading a thick file once per answer card. Text: "Every answer means re-reading the whole text. Long text × many answers = slow."

Bottom banner: "RULE: EVERY ANSWER GETS ITS OWN HEARING."
"""),
    ("friendly-2-the-library", """Title: "THE STUDY LIBRARY · 2/4"

Panel 1 header "REAL-WORLD SHELVES": Rerankie as a librarian among shelves of books labeled "public datasets". Text: "Real questions, labeled by people."

Panel 2 header "THE TRICKY SHELF": small AI helper robots writing trick cards labeled "negation", "hidden instructions", "traps". Text: "Hard cases on purpose."

Panel 3 header "THE LOCKED EXAM ROOM": a vault door. Text: "Written by a different AI, double-checked blind, never studied."

Panel 4 header "THE GOLDEN LABEL RULE": a big stamp. Text: "Only what the text supports counts. Not mentioned means NO."

Panel 5 header "SORTED BY FINGERPRINT": each story card gets a fingerprint that sends it to one shelf: "practice", "check-up", "calibration", "exam". Text: "A story is never split across shelves."

Panel 6 header "SURPRISE SUBJECTS": three locked drawers in the exam room labeled "movie reviews", "yes/no questions", "assistant requests". Text: "Some subjects are never practiced at all."

Bottom banner: "RULE: IF IT WAS STUDIED, IT CANNOT BE ON THE EXAM."
"""),
    ("friendly-3-tiny-knobs", """Title: "PRACTICE WITH TINY KNOBS · 3/4"

Panel 1 header "THE BIG BRAIN STAYS FROZEN": Rerankie's brain in a locked glass case. Text: "We never retrain the whole brain."

Panel 2 header "CLIP-ON KNOBS": small knobs clipped onto Rerankie's attention goggles. Text: "Less than 1% of the settings can move."

Panel 3 header "PRACTICE ROUNDS": Rerankie answers a tray of whole questions while a coach marks mistakes. Text: "Confident wrong answers cost the most."

Panel 4 header "FAIR SCORING": a balanced seesaw with an 8-option question on one side and a yes/no question on the other. Text: "Every question counts the same."

Panel 5 header "TINY NUDGES": the coach turns a knob slightly with a screwdriver; a dial labeled "step size" winds down. Text: "Small steps, slowing down over time."

Panel 6 header "CHECK-UPS & SNAPSHOTS": a quiz, a snapshot of the best knob settings packed into a backpack, then reloaded and double-checked. Text: "Quiz often. Keep the best. Verify the copy."

Bottom banner: "RULE: NUDGE TINY KNOBS, CHECK OFTEN, KEEP THE BEST."
"""),
    ("friendly-4-report-card", """Title: "THE REPORT CARD · 4/4"

Panel 1 header "BEFORE vs AFTER": a scoreboard. Text: "61% → 73.5% on 3,471 exam questions."

Panel 2 header "NOT LUCK": two piles of cards. Text: "605 answers fixed, 172 broken."

Panel 3 header "SURPRISE SUBJECTS", three rows: "Movie reviews: 50% → 77%", "Yes/no questions on Wikipedia text: 59% → 70%", "Assistant requests: 92% → 89% (slipped)".

Panel 4 header "HONEST CONFIDENCE": a thermometer. Text: "90% sure should mean right 9 times in 10. Better now, not perfect."

Panel 5 header "SPEED": a stopwatch. Text: "One short question: about 0.15 s on a laptop. Long texts with many questions: tens of seconds."

Panel 6 header "STILL HARD": Rerankie scratching its head at a long rulebook and a brand-new kind of task. Text: "Long rulebooks, brand-new tasks, tricky wording."

Bottom banner: "RULE: TRUST THE TEST SET, NOT THE VIBES."
"""),
]

# Token counts from the pinned tokenizer on examples/request.json (prompt mapping task-v1); LoRA sizes from the checkpoint.
LORA_PAGES = [
    ("lora-1-text-to-qwen", """Title: "HOW THE TEXT REACHES QWEN · 1/2"

Panel 1 header "ONE REQUEST": Rerankie at a desk reading a support ticket on its screen: "Checkout is broken. We are losing sales. Please fix it today." Three question cards: "URGENT? yes / no", "WHICH TEAM? technical / billing / sales", "WHICH TAGS? revenue loss / refund / blocked". Callout: "1 + 3 + 3 = 7 prompts".

Panel 2 header "ONE PROMPT PER CANDIDATE": a dark code card with these monospace lines:
"<|im_start|>system"
"Judge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be "yes" or "no".<|im_end|>"
"<|im_start|>user"
"<Instruct>: Which team should handle the underlying issue?"
"<Query>: Technical support: software malfunctions and integration failures"
"<Document>: Checkout is broken. We are losing sales. Please fix it today.<|im_end|>"
"<|im_start|>assistant"
"<think></think>"
Side note: "Qwen's official reranker template, word for word".

Panel 3 header "WHAT GOES IN EACH SLOT", three colored rows:
"<Instruct>  ←  the question"
"<Query>  ←  one candidate's description (never its id)"
"<Document>  ←  the customer's text, copied into every prompt"
Small note: "yes/no questions: the question moves to <Query>".

Panel 4 header "TEXT → TOKENS": a long tape of small token blocks in three colors with labels under each section: "system prefix: 39 tokens", "Instruct + Query + Document: 37-42 tokens", "assistant suffix: 9 tokens". Note: "7 prompts, 85-90 tokens each, 612 in total". Warning chip: "too long = error, never cut".

Panel 5 header "BATCH WITH LEFT PADDING": a grid of 7 rows of token blocks of slightly different lengths; gray padding blocks on the LEFT so every row ends in the same right-most column, which glows. Note: "every prompt's last token lines up in one column · up to 16,384 padded tokens per batch".

Panel 6 header "ONE FORWARD PASS, NO GENERATION": Rerankie's transparent head shows a stack labeled "28 transformer layers"; from the glowing last column an arrow goes into a wide bar labeled "151,669 vocabulary scores" where only two cells light up: "yes (id 9693)" and "no (id 2152)". Formula card: "score = logit(yes) − logit(no)".

Panel 7 header "SCORES → ANSWERS", three rows:
"URGENT: p = sigmoid(score), yes if p ≥ 0.5"
"TEAM: softmax over its 3 scores, pick the highest"
"TAGS: sigmoid of each score, keep all ≥ 0.5"

Panel 8 header "THE HIDDEN COST": a tired Rerankie reading the same ticket seven times. Text: "The ticket is inside all 7 prompts. 16 questions × 3 candidates on an 8,000-token text = 48 full reads."

Bottom banner: "RULE: ONE PROMPT PER CANDIDATE. THE ANSWER IS READ FROM TWO LOGITS."
"""),
    ("lora-2-where-lora-plugs-in", """Title: "WHERE LoRA PLUGS IN · 2/2"

Panel 1 header "THE FROZEN BASE": Rerankie with a transparent chest showing a locked glass core labeled "Qwen3-Reranker-0.6B · 600M weights · frozen". Note: "28 layers · width 1,024 · 16 query heads, 8 key/value heads".

Panel 2 header "ONE PROJECTION, ZOOMED IN": a clean left-to-right diagram. An input arrow "x" splits into two parallel lanes. Main lane: a large frozen box with a lock icon labeled "W (frozen)". Bypass lane, drawn thinner and glowing: a small chip "A: 1,024 → 16", then a small chip "B: 16 → out", then a tag "× 2". Both lanes meet at ONE plus sign, then an arrow "output". Caption under the diagram: "this bypass sits on q_proj, k_proj, v_proj and o_proj in all 28 layers; the MLP has none".

Panel 3 header "THE LoRA FORMULA": a dark code card with these monospace lines:
"output = W·x + (32 / 16) · B·(A·x)"
"W: frozen original weight"
"A: 16 × input, B: output × 16  (trainable)"
"B starts at zero → step 0 = the original model"

Panel 4 header "HOW TINY IS IT": a tally card:
"per layer: q 49,152 + k 32,768 + v 32,768 + o 49,152 = 163,840"
"× 28 layers = 4,587,520 trainable"
"0.76% of 600M · one 18 MB file"

Panel 5 header "WHAT IT LEARNS FROM": a mini version of the 7 prompts feeding blank score cards (no numbers on them) into two loss cards: "TEAM: cross-entropy over its own 3 scores" and "URGENT / TAGS: binary cross-entropy on each score". Glowing gradient arrows flow back only into the small A and B chips. Note: "same prompts and same yes − no score as at inference".

Panel 6 header "THE RUN": a spec card: "10,112 training questions · 183 steps · 1.05 h · lr 2e-4 · bf16 · Apple M5 Pro".

Panel 7 header "BEFORE → AFTER · 3,471 TEST QUESTIONS", a scoreboard:
"question accuracy: 61.0% → 73.5%"
"binary AUROC: 0.605 → 0.863"
"multilabel exact match: 1.2% → 31.1%"

Panel 8 header "AT SERVING TIME": Rerankie clipping a small glowing adapter onto the locked core. Text: "base + 18 MB adapter, loaded together · unmerged adapter adds 8-14% latency · bf16: 73.7% vs 73.5% in fp32".

Bottom banner: "RULE: SAME PROMPT, SAME YES/NO READOUT. ONLY 0.76% OF THE WEIGHTS LEARN."
"""),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="all", choices=["deep", "friendly", "lora", "all"])
    ap.add_argument("--pages", default="1,2,3,4")
    ap.add_argument("--style", help="optional image used only as a visual style reference for deep page 1")
    ap.add_argument("--quality", default="high", choices=["low", "medium", "high", "xhigh", "max", "auto"])
    ap.add_argument("--size", default="1024x1536")
    a = ap.parse_args()
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set in this environment; export it and rerun.")
    OUT.mkdir(parents=True, exist_ok=True)
    client, pages = OpenAI(), [int(p) for p in a.pages.split(",")]
    anchor = OUT / f"{DEEP[0][0]}.png"

    def save(r, name):
        (OUT / f"{name}.png").write_bytes(base64.b64decode(r.data[0].b64_json))
        print(f"wrote docs/comics/{name}.png" + (f" (output tokens {r.usage.output_tokens})" if r.usage else ""), flush=True)

    def render(name, prompt, ref):
        with open(ref, "rb") as f:
            save(client.images.edit(model=MODEL, image=[f], prompt=prompt, quality=a.quality, size=a.size), name)

    if a.batch in ("deep", "all") and 1 in pages:  # the anchor page must exist before the others reference it
        if a.style:
            render(DEEP[0][0], STYLE_ONLY + LOOK + DEEP[0][1], a.style)
        else:
            save(client.images.generate(model=MODEL, prompt=LOOK + DEEP[0][1], quality=a.quality, size=a.size), DEEP[0][0])
    if not anchor.exists():
        sys.exit(f"{anchor} is the series reference; generate deep page 1 first")
    jobs = []
    if a.batch in ("deep", "all"):
        jobs += [(n, SAME_SERIES + LOOK + p) for i, (n, p) in enumerate(DEEP, 1) if i in pages and i != 1]
    if a.batch in ("friendly", "all"):
        jobs += [(n, SAME_SERIES + FRIENDLY + p) for i, (n, p) in enumerate(FRIENDLY_PAGES, 1) if i in pages]
    if a.batch in ("lora", "all"):
        jobs += [(n, SAME_SERIES + LOOK + p) for i, (n, p) in enumerate(LORA_PAGES, 1) if i in pages]
    with ThreadPoolExecutor(max_workers=7) as ex:
        list(ex.map(lambda j: render(*j, anchor), jobs))


if __name__ == "__main__":
    main()
