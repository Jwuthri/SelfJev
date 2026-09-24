# Round-2 hard-case data: generation, judging, and what it did to the model

Written 2026-09-24. Everything below is measured; paths point at the evidence. The cross-session ledger is
[experiments.md](experiments.md).

## TL;DR

- 4,103 states / 10,627 questions were written by five models, judged blind by GPT-6 Astra, and 10,142 kept
  (95.4% author = judge). Cost: $22.86 generation + $36.24 judge + $0.30 Jev. Build: `data/hardcases.jsonl`.
- Retraining the shared-prefix tree 4B on it (`runs/tree_4b_r2`) **helps the target task and hurts the aggregate
  test number**: authored eval families 78.4 → 81.9%, every reasoning trap up (numeric +25, exception +29,
  paraphrase +14, role reversal +13, injection +10, distractor +9, temporal +7, long state +6), but overall
  81.6 → 80.6% (McNemar p = 0.01) because CLINC intents fell 94.7 → 83.3%.
- The CLINC loss has one cause: **all 50 CLINC errors are "none of the above" picks when a real intent applied**
  (95 "none" predictions vs 45 true). The hard data offers a none candidate in 50% of hard/very-hard multiclass
  questions and it is correct 28% of the time when offered, vs 8% in round-1 synthetic data and never in public
  data. Fix the mix, not the idea.
- The public-set-heavy test split (3,300 of 3,471 questions) cannot see trap improvements; per-trap n is 6–107.
  A larger frozen target-task test set is the prerequisite for the next decisions ([experiments.md](experiments.md), open ideas).

## Generation ([scripts/gen_hardcases.py](../scripts/gen_hardcases.py), prompt [data/hardcases/BRIEF.md](../data/hardcases/BRIEF.md))

One OpenRouter call = one random ASSIGNMENT drawn by the script: difficulty tier (simple / hard / very_hard, balanced
1/3 each by kept questions), 1–2 focus traps weighted by the gap to Jev, domain (20), three genres (of 20), tone (8),
instruction style (9), instruction length (3), candidate-description style (7), invented names. State length is a
separate axis balanced over a token ladder 8, 32, 64, 128, 256, 512, 1K, 2K, 4K, 8K (models undershoot long targets by
~30%; targets ≥ 2K are asked at 0.95 words/token). Each row's `provenance` records model, tier and length bucket.

| author | states / questions | cost | author = judge | notes |
|---|---|---|---|---|
| google/gemini-3.8-flash | 950 / 2,462 | $12.87 (Google key, BYOK) | 97.6% | reasoning capped at `effort: low` |
| x-ai/grok-4.7 | 319 / 1,022 | $8.19 (OpenRouter credit) | 98.9% | reasoning is mandatory: 8–20K hidden tokens per call, 4× Gemini per state; adds extra keys inside candidates |
| openai/gpt-6-luna | 1,676 / 3,988 | $1.62 (OpenAI key) | 96.0% | cheapest good generator |
| deepseek/deepseek-v4-flash | 458 / 1,264 | $0.17 (credit) | 82.1% | `reasoning.enabled=false` needed (else 32K tokens); slow provider, stopped early |
| claude-sonnet agents (other session, 8 trap families, prefixes h*) | 700 / 1,891 | Claude Code usage | 98.3% | brief: `data/hardcases/BRIEF_sonnet_agents.md` |

Diversity check on the OpenRouter part: 45/30/25% binary/multiclass/multilabel per model, instruction length p10–p90 =
3–60 words, 41–64% distinct first-two-words, binary targets 35–47% true (false = "not supported" is the more common
label), multilabel positives 0/1/2/3+ = 114/253/479/228. Tags: distractor 978, role reversal 561, sarcasm 548,
negation 540, numeric 532, injection 478, temporal 419.

## Judging ([scripts/judge_hardcases.py](../scripts/judge_hardcases.py))

GPT-6 Astra, reasoning low, blind (state + instruction + candidates only), same prompt and JSON schema as the test
comparison, through **OpenAI's Batch API** (OpenRouter's batch endpoint answers 401 "Batch requests require a concrete
user identity" for this key). 5 batches, 0 failed requests, ≈ $3.40 per 1K questions with long states included.
Results: [data/hardcases/review/JUDGE.md](../data/hardcases/review/JUDGE.md); build:
[data/hardcases/review/REVIEW.md](../data/hardcases/review/REVIEW.md).

- Agreement by tier: simple 97.3, hard 93.8, very hard 93.3. Weakest tags: exception 88.4, long state 91.2, temporal
  91.3, sarcasm 92.7. Four sampled temporal disagreements: two author errors (one note says "Wait: 4 is < 5"), two
  genuinely ambiguous. Dropping disagreements is the right rule.
- Jev as annotator: agrees with authors 93.0%; worst on temporal (82.7% on the Sonnet set), numeric, injection and
  multilabel. 432 questions are author = Astra but Jev wrong: the slice that can beat Jev. Cheap second opinion, not a
  gate.

## Retrain result (`runs/tree_4b_r2`, other session; test split 3,471 questions)

| slice | n | tree_4b (round-1 data) | tree_4b_r2 (+ hard cases) |
|---|---|---|---|
| all | 3,471 | 81.6 | 80.6 (p = 0.01) |
| authored eval_* | 171 | 78.4 | 81.9 |
| public hf_/heldout_ | 3,300 | 81.8 | 80.5 |
| heldout_intent_clinc | 300 | 94.7 | **83.3** |
| every other public family | 300 each | | within ±2.7 |
| numeric_reasoning | 16 | 43.8 | 68.8 |
| exception | 7 | 28.6 | 57.1 |
| paraphrase | 22 | 77.3 | 90.9 |
| role_reversal | 15 | 73.3 | 86.7 |
| injection | 10 | 80.0 | 90.0 |
| distractor | 33 | 69.7 | 78.8 |
| long_state | 50 | 76.0 | 82.0 |
| temporal_reasoning | 29 | 51.7 | 58.6 |
| multi_positive | 81 | 44.4 | 44.4 |

Newly wrong CLINC questions: 34, all predicted `none`, mean max probability 0.61 (so a none-prior correction or an
`abstain_below`-style penalty recovers most of them even before retraining).

## What to do with this

1. **Rebalance "none" in the hard data**: cap none-correct at ≈ 10% of multiclass questions and add none-offered-but-
   wrong cases on intent-like states; or drop `nota` from the focus traps and let it occur naturally. Then retrain.
2. **Mix weight**: hard cases are now ≈ 50% of training questions; try 25–30% (subsample per tier) against the same
   test to separate "too much none" from "too much hard data".
3. **Measure on the target distribution**: build the frozen test set ([experiments.md](experiments.md), open ideas) before more
   retraining decisions. The current test cannot distinguish +3.5 on 171 authored questions from noise.
4. **multi_positive (44.4%, unchanged)** is the largest untouched slice: 3+ positives are only 21% of new multilabel
   questions; generate more with 3–5 positives.

## Rerunning

```bash
zsh -ic 'uv run python scripts/gen_hardcases.py --model openai/gpt-6-luna --budget 2 --max-questions 3000'  # resumes counters
zsh -ic 'uv run python scripts/judge_hardcases.py --jev'          # judges every raw source not yet submitted; never run two at once
uv run python scripts/build_hardcases.py                         # other session's build: keeps author = judge, leakage guard
```

Raw responses and per-call logs: `reports/hardcases/` (gen_cache, gen_log.jsonl, run_*.log, judge_run*.log).
