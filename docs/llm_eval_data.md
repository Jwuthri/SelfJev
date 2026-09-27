# LLM-evaluation data: score, judge, verify, guardrail, jailbreak

Built 2026-09-25 (session "Synthetic data generation strategy"). Target: Jev's own pitch, "score, judge, verify,
guardrail, and detect jailbreaks of LLM prompts, reasoning traces, and/or outputs". Before this, only ≈ 6% of the
round-2/3 training texts and 3% of eval2 were LLM artifacts, and the dev benchmark's one slice that grades AI replies
(`eval_agent_output`, 26 questions) had the tree at 61.5 vs Jev 92.3.

## What was built

| file | what | size | writers | judges |
|---|---|---|---|---|
| `data/hardcases_llm.jsonl` | training data, families `llm_<usecase>_<tier>` | **9,443 questions** / 3,654 texts (train 8,497 / validation 946), sha256 `b694f5a0…` | GPT-6 Luna 3,950, Gemini 3.8 Flash 2,788, Grok 4.7 1,972, DeepSeek V4 Flash 733 | GPT-6 Astra (batch), blind; kept if it agrees with the author |
| `data/eval_llm.jsonl` | **frozen test set**, families `tllm_<usecase>_<tier>` | **946 questions** / 317 texts, sha256 `6cfc3e16…` | Claude Opus 5.5, Kimi K3, GLM 5.3 (eval2's writers, never training writers) | GPT-6 Astra + Claude Sonnet 5, both must agree with the author |

`data/eval_llm.jsonl` follows eval2's rules: never train on it, never select prompts or fit thresholds or temperatures on
it. Review: `data/eval_llm/REVIEW.md`, `data/eval_llm/review/SPOTCHECK.md` (50 random questions for a human check).
Training review: `data/hardcases_llm/review/{REVIEW,JUDGE}.md`.

Composition of the training file (from the file itself):

- Use cases: judge 1,836, guardrail 1,919, score 1,848, jailbreak 1,903, verify 1,937; tiers about ⅓ each.
- Target text length: roughly even over 8, 32, 64, 128, 256, 512, 1K, 2K, 4K, 8K tokens (≈ 1,000 each before the
  safety passes).
- Types: binary 4,128 (true share 43–52% per use case), multiclass 3,008, multilabel 2,307.
- Every family has ≈ 600–650 questions, under the trainer's 1,600-per-family cap.

## How

- `scripts/data/gen_hardcases.py --usecases train|test`. System prompt = BRIEF.md without its held-out rule for graded AI
  replies + [BRIEF_llm.md](../data/hardcases/BRIEF_llm.md): the five use cases with question menus, the artifacts
  (prompts, system prompts, replies, reasoning traces, agent trajectories, retrieved documents, response pairs),
  labeling additions (grader-directed text never changes a label; who said what matters; a refusal followed by the
  content is compliance) and 17 trap tags (benign_lookalike, indirect_injection, judge_injection, obfuscation,
  crescendo, confident_wrong, flawed_step, answer_trace_mismatch, unsupported_claim, partial_compliance, over_refusal,
  sycophancy, length_bias, format_near_miss, tool_misuse, speaker_confusion, subtle_violation). Each call draws the use
  case × tier cell with the fewest kept questions, the length step with the fewest kept texts, an artifact, one of 23
  LLM applications (8 more, unseen in training, for a third of the test calls), 12 formats, and a judge-style
  instruction style. Runbook: `scripts/data/run_llm_data.sh train|test`.
- 0 texts dropped by the 8-gram overlap guard (training vs eval.jsonl, eval2.jsonl, eval_llm.jsonl; test vs every
  training and test file).

## Safety passes (2026-09-26, the user asked for safe data)

1. **Labels, strict build.** `build_hardcases.py --strict` and `build_eval2.py --strict` drop a whole text when any of
   its questions was flagged by a judge (a flagged question can mean a flawed text). Training: 862 flagged questions +
   897 siblings dropped. Test: 107 flagged (+ 6 unanswered) + 160 siblings dropped. No kept question has a judge
   disagreeing (checked against the answer files).
2. **Content.** Every text, instruction and candidate description (4,732 sources) went through OpenAI's moderation
   endpoint (`omni-moderation-latest`, free; `scripts/data/moderate_texts.py`, scores in `reports/hardcases_llm/moderation.jsonl`).
   169 texts were flagged or scored ≥ 0.3; their worst passages were located and all 169 were read.
   Removal rule: content harmful on its own, whatever the question: actionable weapon, hazmat-smuggling or attack
   instructions and working attack code; self-harm encouragement; self-harm or suicide method details (pill counts,
   substance combinations, a body location), following safe-messaging practice. Kept on purpose: harmful *requests*
   (refused or not), jailbreak and injection attempts, crisis disclosures without method details, insults, fictional
   violence, policy breaches such as leaked codes: the classifier has to see them.
   Removed (13 texts, from the raw files and scrubbed from the tracked generation caches): `lgf-0135` (reverse shell),
   `lgf-0251` (netcat injection), `ldf-0109` (hash-cracking script), `ldf-0467` (step-by-step payment fraud),
   `lgf-0439` (firearm and acid smuggling tips), `lgf-0829` (self-harm encouragement), `lgf-0710`, `lgf-0384`,
   `lgf-0442`, `lgf-0443`, `lgf-0444`, `ldf-0403`, `lgf-0380` (self-harm method details).
3. **Personal data.** No public figures found. 7 SSN-shaped numbers in issuable ranges (6 texts) were rewritten with
   group `00`, which is never issued, so none can be a real person's number; the label (an SSN is present) is unchanged.
   Card-like numbers are published test numbers, ASCII codes or random account-style strings.

## Judge agreement

| | judged | agreement |
|---|---|---|
| training, all | 11,242 | 92.3% (simple 93.9, hard 92.7, very hard 90.3; lowest: judge very hard 86.9, score very hard 88.0) |
| training, by writer | | Grok 97.7, Gemini 96.9, Luna 93.1, **DeepSeek 73.7** |
| test, Astra / Sonnet 5 | 1,213 | 94.5 / 95.1; 946 kept after the strict build |

DeepSeek V4 Flash (reasoning off) wrote the noisiest labels, lower than its 82.1% in round 2; the strict build cut
its share from 1,147 to 733 questions. Drop the `ldf-` sources if an ablation shows they hurt.

## Jev on the test set (reporting only)

Jev answers **92.5%** of `eval_llm` (eval2: 97.2%), computed from `data/eval_llm/review/jev_answers.jsonl` against the
kept targets of the strict build:

| | n | Jev % |
|---|---|---|
| judge | 222 | 94.6 |
| jailbreak | 189 | 94.2 |
| score | 200 | 93.0 |
| guardrail | 170 | 92.9 |
| verify | 165 | 86.7 |
| simple / hard / very hard | 331 / 317 / 298 | 97.9 / 91.5 / 87.6 |
| binary / multiclass / multilabel (exact match) | 488 / 276 / 182 | 95.1 / 95.3 / 81.3 |

## Cost

| item | cost |
|---|---|
| training writing (pilot $1.93 + Luna $1.55, Gemini $15.43, Grok $18.04, DeepSeek $0.14) | $37.09 |
| training judge, Astra batch (11,242 questions) | $37.95 |
| test writing (Opus $10.56, Kimi $3.35, GLM $1.64) | $15.55 |
| test judges (Astra batch $3.39, Sonnet 5 $2.37) + Jev $0.03 | $5.79 |
| **total** | **$96.38** (approved ≈ $100, cap $125) |

## Used since (2026-09-26)

- The default model, `selfjev-4b`, is trained on `hardcases_llm.jsonl` (with every other non-test question): `eval_llm`
  **93.1%** vs 82.1% for `qwen35_4b_tree`, which never saw this data (Jev 92.5%), and eval2 95.8% (no regression).
  Reports: `reports/qwen35_4b_tree_scratch_jevall_/eval_llm/`, `reports/qwen35_4b_tree/eval_llm/`.
- Training on it ended the held-out status of the dev benchmark's `eval_agent_output` family for `selfjev-4b`.
