# Datasets and labels

The three authored evaluation suites are published as **[SelfJev Decision Bench](https://huggingface.co/datasets/Jwuthrich/selfjev-decision-bench)**: Text Decisions (`eval2`), AI Response Review (`eval_llm`), and Record Reasoning (`compact_challenge_v1`). The release contains 3,657 unchanged questions, expected answers, provenance, Parquet/JSONL files and a strict prediction scorer. See its data card for construction, prior development use, and evaluation limitations.

All data is one JSONL line per (text, question, target), with `id`, `source_id`, `family`, `split`, `provenance`,
`state`, `question` (`type`, `instruction`, `candidates`), `target`, `hard_cases` and optional `paraphrase_group` and
`notes`. Authored files use a compact form (one text, several questions) that `selfjev.data.load` expands. Check any
file with `uv run python -m selfjev.data check FILE`.

**`data/all.jsonl.gz` is the dataset**: every original question in one file (93,237 questions from 12 datasets on
2026-09-27), tagged by `dataset`, with Jev's prediction in `jev` (`uv run python scripts/data/build_all.py`). Catalog
with per-dataset counts, usage snippet and the growth procedure: [data/README.md](../data/README.md), generated from
[src/selfjev/data/catalog.py](../src/selfjev/data/catalog.py). Always start from it, and add new training data as a
**batch** (`gen_hardcases.py --batch <name>`, then `scripts/data/grow_batch.sh`), never as a new stand-alone file. The
files below are its sources.

## Labeling policy (all sources)

- Binary `true` means **the text supports answering yes**. Contradicted and simply-not-stated are both `false`:
  `false` is "not supported by the text", not "known false".
- Instructions inside the text are data, not instructions.
- Negations, hypotheticals and future conditionals are not the thing itself.
- Multilabel targets are complete over the listed candidates: candidates with unknown labels are left out rather than
  labeled negative.
- LLM labels are not ground truth. Training labels come from authored targets checked by a blind judge; Jev answers
  never decide a training label.

## Files

| file | what | size | provenance |
|---|---|---|---|
| `data/hf.jsonl` | public human-labeled datasets in our schema | 16,800 questions: train 12,000; validation, calibration 750 each; test 1,500 in-distribution + 1,800 held-out | 11 pinned HF revisions, licenses per row ([scripts/data/build_hf.py](../scripts/data/build_hf.py)); label descriptions written by Claude Sonnet |
| `data/eval.jsonl` | authored evaluation set over 7 families, hard cases tagged | 155 texts / 398 questions: validation 118, calibration 109, test 171 | 7 Claude Opus agents from [data/eval/BRIEF.md](../data/eval/BRIEF.md); a blind Opus relabelling agreed 398/398; not human-reviewed |
| `data/synthetic.jsonl` | hard, long, trap-heavy training data, 6 families | 923 texts / 2,405 questions | 12 Claude Sonnet agents from [data/synthetic/BRIEF.md](../data/synthetic/BRIEF.md); an Opus review dropped 43 questions |
| `data/hardcases.jsonl` | **round 2**: verified hard-case training data | 10,142 kept of 10,627 (train 8,999 / validation 1,143) | 4 OpenRouter models + 8 Claude Sonnet agents, blind GPT-6 Astra judge ([round-2 write-up](hardcases_round2.md)) |
| `data/hardcases_r3.jsonl` | **round 3**: verified hard-case training data | 38,628 questions (train 34,868 / validation 3,760) | GPT-6 Luna, Gemini 3.8 Flash, Grok 4.7; blind Astra judge |
| `data/eval2.jsonl` | **eval2**: frozen target-task test set | 1,991 questions / 647 texts, all `test` | Claude Opus 5.5, Kimi K3, GLM 5.3; two blind judges |
| `data/hardcases_llm.jsonl` | **LLM-evaluation** training data: score, judge, verify, guardrail, jailbreak ([llm_eval_data.md](llm_eval_data.md)) | 9,443 questions (train 8,497 / validation 946) | GPT-6 Luna, Gemini 3.8 Flash, Grok 4.7, DeepSeek V4 Flash; blind Astra judge; strict build + moderation review |
| `data/eval_llm.jsonl` | **eval_llm**: frozen LLM-evaluation test set | 946 questions / 317 texts, all `test` | Claude Opus 5.5, Kimi K3, GLM 5.3; blind Astra + Claude Sonnet 5; strict build |
| `data/compact_challenge_v1.jsonl` | **compact_challenge_v1**: frozen programmatic challenge, explicit-record reasoning with evidence/absence contrasts | 720 questions / 120 texts, all `test` | generated and labeled by code ([scripts/data/build_compact_challenge.py](../scripts/data/build_compact_challenge.py), a Codex session) |
| `data/batches/<name>.jsonl` | **batches**, training data grown since 2026-09-26: `llm_multilabel_v1` (LLM-evaluation multilabel, near-miss negatives), `numdate_neg_v1` (double negation, numbers, dates), `mpos_distr_num_v1` (several correct answers, distractors, numbers) | 7,570 + 549 + 3,645 = 11,764 questions (train and validation) | GPT-6 Luna (+ Gemini 3.8 Flash and Grok 4.7 for `llm_multilabel_v1`); blind Astra judge; strict build + moderation screen; one README per batch |

- **Splits** hash `source_id`, so every question about one text shares a split. `build_data.py` drops any synthetic
  text whose word-8-gram containment with an eval text is ≥ 0.3; round 2, round 3, eval2 and the LLM-evaluation data
  apply the same guard (none was dropped), and every batch runs it against every test set (`grow_batch.sh build`).
- **Held-out families** never appear in training: CLINC150 intents (with an out-of-scope `none` option), DBpedia-14,
  TREC question types, dair-ai emotion, BoolQ and SST-2. The authored `eval_agent_output` family (grading AI replies; no longer held out once a model trains on `hardcases_llm.jsonl`)
  is also excluded from all training data.
- **Known leaks in the dev benchmark** (review of 2026-09-23): MNLI rows share premises across splits (22 test
  questions), and some authored policy texts have near-duplicate variants across splits. The effect on results is
  small (MNLI without those rows: 57.6% untrained vs 88.8% LoRA), but it is one more reason to call it a development
  benchmark.
- **Contamination:** public sets such as Banking77, AG News and TweetEval may be in the base model's pretraining data.

## The training mixes

`selfjev-4b`, the default model, trains on every non-test question of `data/all.jsonl.gz`. The mix is built by
[scripts/train/jev_soft_targets.py](../scripts/train/jev_soft_targets.py); the recipe that trains on it is
[scripts/train/selfjev_4b.sh](../scripts/train/selfjev_4b.sh) (`selfjev-4b` itself ran through its predecessor,
`scripts/jev_soft_box.sh scratch` at the archive tag):

| mix | used by | questions |
|---|---|---|
| the train and validation rows of every training dataset (`hf`, `synthetic`, `hardcases`, `hardcases_r3`, `hardcases_llm`, batches `llm_multilabel_v1` and `numdate_neg_v1`) minus the 1,200-question validation sample (`data/val_sample_1200.txt`); no family cap, no `none` rebalance, texts ≤ 16K tokens; every option listed in the question; target 0.5 × label + 0.5 × Jev's probabilities | **`selfjev-4b`** (the default) | 79,943 |

Batch `mpos_distr_num_v1` came after it and is not in `selfjev-4b`.

The older mixes below are history. They were built at tag `archive/pre-cleanup-2026-09-27` with its scripts and
configs: the 1,600-per-family cap (`max_train_per_family` in the configs), round 2b's `data/hardcases_nb.jsonl` (round
2 with `none`-correct training questions capped at 10%: 9,982 questions, by `scripts/rebalance_nota.py`) and the
`data/ova/` training copies (`scripts/options_in_question.py`). Master keeps only the `data/ova/` evaluation copies.
Training logs: `reports/train_meta/<run>.json`.

| mix | used by | questions |
|---|---|---|
| round 1: public sets (≤ 1,600 per family) + synthetic | every model until 2026-09-23 | 10,112 |
| round 2: round 1 + `hardcases.jsonl`, 8K-token training length | `tree_4b_r2` | 16,357 |
| round 2b: round 1 + `hardcases_nb.jsonl` | `tree_4b_r2b`, `tree_4b_ova`, the capacity runs | 16,375 |
| round 2b with the hard-case families exempt from the 1,600-per-family cap | `tree_4b_instruct_r2x64` | 18,681 |
| round 3: the above + `hardcases_r3.jsonl` (r3 families exempt too) | `tree_4b_instruct_r3` | 51.9K |
| round 3 with every option listed in the question (`data/ova/`) | `tree_4b_combo`, `qwen35_4b_combo` (texts ≤ 2K: 43.8K), `qwen35_4b_tree` (texts ≤ 8K) | 51.8K |

## Generating and judging hard cases

The pipeline behind rounds 2 and 3, eval2, the LLM-evaluation data and every batch (for a batch,
`scripts/data/grow_batch.sh` runs the judge and the build):

1. **Write** ([scripts/data/gen_hardcases.py](../scripts/data/gen_hardcases.py), system prompt
   [data/hardcases/BRIEF.md](../data/hardcases/BRIEF.md)). Each call draws a random assignment: difficulty tier
   (simple / hard / very hard, balanced), 1–2 focus traps weighted by the gap to Jev, domain, three genres, tone,
   instruction style and length, candidate-description style, invented names, and a text length from a ladder of 8,
   32, 64 … 8K tokens.
2. **Judge blind** ([scripts/data/judge_hardcases.py](../scripts/data/judge_hardcases.py)): GPT-6 Astra sees only the text,
   instruction and candidates, through OpenAI's Batch API. eval2 adds Gemini 3.1 Pro as a second judge, eval_llm
   Claude Sonnet 5.
3. **Keep only agreement** ([scripts/data/build_hardcases.py](../scripts/data/build_hardcases.py)): a question survives only
   when every judge gives the author's answer. Disagreements are mostly author errors or genuinely ambiguous.
4. **Check the mix** after the build: the `none`-correct rate, positives per multilabel question, types, tiers.

| set | written | kept | author = judge | cost |
|---|---|---|---|---|
| round 2 | 10,627 questions, 5 authoring models | 10,142 | 95.4% (DeepSeek V4 Flash 82.1 … Grok 4.7 98.9) | $22.86 writing + $36.24 judging |
| round 3 | 39,833 questions, 3 authors | 38,628 | 97.0% (simple 98.8, hard 96.5, very hard 95.6) | ≈ $280 |
| eval2 | 2,070 questions, 3 authors | 1,991 | 96.2% unanimous (Astra 97.5, Gemini 97.0) | $32.72 |
| eval_llm ([details](llm_eval_data.md)) | 1,213 questions, 3 authors | 946 (strict build) | Astra 94.5, Sonnet 5 95.1 | $15.55 writing + $5.76 judging |
| LLM evaluation, training ([details](llm_eval_data.md)) | 11,242 questions, 4 authors | 9,443 (strict build, safety passes) | 92.3% | $37.09 writing + $37.95 judging |
| batch `llm_multilabel_v1` | 9,286 questions, 3 authors | 7,570 | 89.7% | $26.60 writing + $42.36 judging |
| batch `numdate_neg_v1` | 643 questions, GPT-6 Luna | 549 | 93.0% | $0.28 writing + $2.78 judging |
| batch `mpos_distr_num_v1` | 4,041 questions, GPT-6 Luna | 3,645 | 95.6% | $1.87 writing + $17.80 judging |

**Round 3's changes, from round 2's lessons:** `none` is correct in 7.0% of the multiclass questions that offer it
(round 2: 28% in the hard tiers), and 54% of multilabel questions have 3+ positives (round 2: 21%). Types: binary
16,770, multiclass 12,402, multilabel 9,456.

## eval2: the frozen target-task test set

Built because the dev benchmark could not see trap improvements (per-trap n was 6–107). Review:
[data/eval2/REVIEW.md](../data/eval2/REVIEW.md); human spot-check list `data/eval2/review/SPOTCHECK.md`.

- **Authors never used for training data:** Claude Opus 5.5 (560 questions), Kimi K3 (649), GLM 5.3 (782). A third of
  the calls used domains, genres and instruction styles absent from the training brief.
- **Judges:** GPT-6 Astra and Gemini 3.1 Pro, blind; a question is kept only when both give the author's answer.
- **Composition:** tiers 673 hard / 664 simple / 654 very hard; 1,016 binary / 593 multiclass / 382 multilabel; 177–222
  questions per length bucket; n ≥ 57 for every main trap tag (`evidence_start` 17); 245 of 382 multilabel questions have
  3+ positives; `none` is offered in 391 multiclass questions and correct in 58 (14.8%).
- **Jev: 97.2%.** Weakest on temporal (89.2) and numeric (92.0) reasoning. Never used to keep or drop a question.
  Two Jev runs agree on 1,981 of 1,991 decisions; the rest is Jev's own run-to-run noise.
- **sha256** `2fa954592d0a3124…`. Join predictions on the expanded ids (`<source_id>-q<i>`): an early export renumbered
  ids after drops and made Jev look like 95.2%.
- **Rules:** never train, select prompts or fit calibration on it. It has informed the research direction, so a fresh
  final set is still needed. Batches `numdate_neg_v1` and `mpos_distr_num_v1` were motivated by an eval2 failure audit
  (`reports/audit_2026-09-26/AUDIT.md`; their writer saw only abstract trap names), so eval2 gains from them are
  labeled as test-diagnosis-motivated.
