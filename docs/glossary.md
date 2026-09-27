---
hide:
  - navigation
---

# Glossary

Every piece of shorthand used on this site, in plain words. On any page you can also hover a dotted-underlined term
to see a one-line definition.

## The test sets

eval2
:   The **main benchmark** since 2026-09-24: 1,991 questions about 647 texts, written to look like the real task
    (hard, trap-heavy, texts from 8 to 8K tokens). Written by three LLMs that never wrote training data, and a question
    is kept only when two other LLMs, judging blind, give the same answer. Nothing is ever trained or tuned on it.
    Jev scores 97.2%, our best model (`selfjev-4b`) 95.8%. Details: [data](data.md#eval2-the-frozen-target-task-test-set).

eval_llm
:   The frozen **LLM-evaluation** test set: 946 questions about 317 texts on scoring, judging, verifying, guardrail and
    jailbreak checks of LLM prompts and outputs. Same writers as eval2; a question is kept only when two blind judges
    (GPT-6 Astra and Claude Sonnet 5) both agree with the author. Jev scores 92.5%, `selfjev-4b` 93.1%.
    Details: [LLM-evaluation data](llm_eval_data.md).

dev benchmark (also "old test")
:   The **original test split**: 3,471 questions, 3,300 of them from public datasets (Banking77, AG News, CLINC,
    BoolQ…) and 171 authored ones. It was reused for many decisions, so we call it a development benchmark. Label
    noise in the public sets caps every good model at 80–86%, so it cannot tell good models apart.

held-out family
:   A dataset never used in training (CLINC, DBpedia, TREC, dair-ai emotion, BoolQ, SST-2), so it measures
    generalization to new tasks and label sets.

validation / calibration split
:   Slices of the training data kept aside to pick checkpoints and prompts (validation) and to fit temperatures
    (calibration). Never the test sets.

## Training data

round 1 (R1)
:   The first training mix: 10,112 questions from public datasets (at most 1,600 per dataset) plus LLM-written
    synthetic questions.

round 2
:   Round 1 plus about 10K **hard cases**: tricky questions written by five LLMs and kept only when a blind GPT-6
    Astra judge gave the same answer as the author.

round 2b
:   Round 2 with one fix: questions whose right answer is "none of the above" capped at 10%, because too many of them
    made the model reject valid answers.

round 3
:   38,628 more verified hard cases (GPT-6 Luna, Gemini 3.8 Flash, Grok 4.7; blind Astra judge), built with round 2's
    lessons. Its first training run was stopped halfway; the rerun (`tree_4b_instruct_r3`) and every best model since
    (`tree_4b_combo`, `qwen35_4b_tree`, `selfjev-4b`) train on it.

batch
:   How new training data is added now: a named set of new verified questions (for example `llm_multilabel_v1`) that
    joins `data/all.jsonl.gz`, never a stand-alone dataset ([data/README.md](../data/README.md)).

hard case / trap
:   A question designed to fool a shallow reader. The trap tags on eval2:

    | tag | the question tests |
    |---|---|
    | negation, double negation | "not", "never", "not unlike" |
    | numeric / temporal reasoning | arithmetic, limits, dates and durations |
    | role reversal | who did what to whom |
    | injection | instructions planted in the text, which must be ignored |
    | sarcasm | the literal words say the opposite |
    | distractor, lexical overlap | a wrong option that shares words with the text |
    | paraphrase | the answer is stated in different words |
    | exception, hypothetical, contradiction | "unless…", "if…", statements that cancel each other |
    | missing evidence | the text does not say, so the answer is "no" |
    | multi-positive / zero-positive | multilabel questions with several or no correct labels |
    | `nota` | "none of the above" is offered |
    | long state, evidence start/middle/end | long texts, and where the key sentence sits |
    | multi-turn | a conversation rather than a document |

tier
:   Difficulty level of an authored question: simple, hard or very hard.

blind judge
:   An LLM that answers the question without seeing the author's answer. A question is kept only if they agree.

## Question types

binary
:   Yes/no: "does the text support this?" Jev calls it `noul`.

multiclass
:   Pick exactly one candidate. Jev calls it `choice`.

multilabel
:   Pick every candidate that applies (zero, one or several).

state
:   Jev's word for the input text that the questions are about.

## Models and how they are built

selfjev-4b
:   The default model: Qwen3.5-4B with a rank-64 LoRA adapter, trained with the tree on all 80K non-test questions,
    Jev's probabilities as half-weight soft targets and every option listed in the question (`weights/selfjev_4b`).
    Its reports are named `qwen35_4b_tree_scratch_jevall_`.

archived
:   Kept only at git tag `archive/pre-cleanup-2026-09-27`: every model but `selfjev-4b`, with its code, scripts and
    configs (there the package is `personal_jev` and the CLI `pjev`). Reports stay in `reports/`.

stock pairs
:   The standard way to use a reranker: one sequence per (text, question, candidate). Accurate, but the text is re-read
    for every candidate. The first models used it (archived).

shared-prefix tree (tree)
:   Our architecture: the text is read once, and every question and candidate branches off it, still attending to the
    text in every layer. Same quality as stock pairs, up to 37× faster. [Details](tree_model.md).

reranker / Instruct base
:   The two Qwen3 4B starting models: Qwen3-Reranker-4B (built to judge relevance) and Qwen3-4B-Instruct-2507 (a
    general chat model). The Instruct base does better once the data is good. Both archived: `selfjev-4b` starts from
    Qwen3.5-4B, a hybrid of Gated DeltaNet (recurrent) and attention layers.

LoRA
:   A small set of trainable weights added to a frozen model: 1.4% of Qwen3.5-4B for `selfjev-4b`'s rank-64 adapter on
    the attention and DeltaNet layers, 0.3% for the first rank-16 Qwen3 adapters. The only thing we train.

r16 / r64 (rank)
:   The size of the LoRA adapter: rank 64 has 4× the trainable weights of rank 16.

MLP targets
:   LoRA also on the feed-forward layers, not only on attention: more trainable capacity.

all options in the question (OVA)
:   Every candidate is listed in the question text, so each judgment sees the alternatives. Helped by about one point.

teacher / KD
:   Qwen3.8-27B, a larger model used zero-shot as a *teacher*; knowledge distillation (KD) trains our model on its
    probabilities. It did not help (archived).

soft targets (Jev targets)
:   Training toward a mix of the verified label and a teacher's probabilities: 0.5 × label + 0.5 × Jev's stored
    probabilities for `selfjev-4b` (`--soft-weight`). The label still decides; Jev only says how sure to be.

RLCD
:   Jev's name for training on calibration scores (proper scoring rules such as log, Brier and spherical), here
    `selfjev rlcd`. Despite the name, no reinforcement learning is involved. [Details](finetune.md).

custom model
:   A first attempt at "read the text once": new cross-attention layers on top of a frozen encoder. Fast but inaccurate
    (archived). [Details](custom_model.md).

merged / vLLM
:   Serving tricks: *merged* folds the LoRA into the base weights; *vLLM* is a fast inference server whose prefix
    cache shares the text between questions.

compact format
:   A shorter tree layout tested for speed; it did not pay off (archived).

### Reading a run name

Run names are built from these pieces:

| piece | meaning |
|---|---|
| `tree_` / `lora_` | shared-prefix tree / stock pairs |
| `4b`, `8b`, `pilot` | model size (`pilot` = the first 0.6B run) |
| `instruct` | Qwen3-4B-Instruct base instead of the reranker |
| `r1`, `r2`, `r2b`, `r3`, `r2x64` | training data round 1, 2, 2b or 3 (none = round 1); `r2x64` = round 2 × rank 64 |
| `r64`, `mlp` | LoRA rank 64, MLP targets (none = rank 16 on attention) |
| `ova`, `kd` | all options in the question, distillation from the 27B teacher |
| `combo` | the combined levers: rank 64, every option in the question, round-2b + round-3 data (`combo_r2`: round 2b only), and for Qwen3 the Instruct base |
| `qwen35_` | Qwen3.5-4B base; there `tree` means trained with the tree (the earlier Qwen3.5 runs trained on full sequences) |
| `scratch`, `sft`, `rlcd`, `cost` | a new adapter / a fine-tune of `qwen35_4b_tree` / RLCD from it / RLCD with a confident-mistake cost from the `sft` result |
| `jevall`, `fresh` | all non-test data with Jev's probabilities as soft targets / 4,412 questions `qwen35_4b_tree` never trained on |
| trailing `_`, `__last` | the report of the best-by-validation / of the last checkpoint |
| `baseline` | untrained model |
| `curve/` | one of the learning-curve / ablation runs |

So `tree_4b_instruct_r2x64` = tree scorer, 4B, Instruct base, round-2(b) data × rank 64 (the best model on 2026-09-24),
and `qwen35_4b_tree_scratch_jevall_` = Qwen3.5-4B trained with the tree, a new adapter on all the data with Jev's
probabilities, best checkpoint: `selfjev-4b`.

## Metrics

accuracy (question accuracy)
:   Share of questions answered fully right. For multilabel, every label must be right.

multilabel EM (exact match)
:   Share of multilabel questions where the chosen set of labels is exactly right.

AUROC
:   How well scores rank yes-answers above no-answers, ignoring the threshold: 0.5 is chance, 1.0 is perfect.

ECE / Brier
:   Calibration: whether "80% sure" is right 80% of the time. Lower is better.

temperature / threshold
:   Calibration knobs: a temperature softens or sharpens probabilities; a threshold is the probability above which the
    answer is "yes".

McNemar test, p, "142 / 34"
:   Compares two models on the same questions. "142 / 34" means 142 questions only the first gets right and 34 only
    the second; p is the chance of a gap that large if the two were equally good. p < 0.05 is the usual bar.

p50 / p95
:   Median and 95th-percentile latency.

## Services, hardware and datasets

Jev
:   TypeSafe's hosted typed-decision model, the one we are reproducing. [More](landscape.md).

GPT-6 Astra, GPT-6 Luna, Gemini, Grok, Kimi, GLM, Claude Opus / Sonnet
:   LLMs used as reference models, data writers or blind judges.

OpenRouter / BYOK
:   The API gateway used to call Jev and other models; BYOK ("bring your own key") means the bill goes to our own
    OpenAI or Google key.

L4, A10G, L40S, H100
:   NVIDIA GPUs, roughly from slowest to fastest, rented on AWS (g6, g5, g6e, p5 instances). `selfjev deploy aws`
    defaults to an L4 (g6.xlarge).

CLINC, Banking77, AG News, DBpedia, TREC, BoolQ, SST-2, MNLI, GoEmotions, TweetEval
:   Public classification datasets in the dev benchmark (intents, topics, question types, yes/no reading, sentiment,
    entailment, emotions).
