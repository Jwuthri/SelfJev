---
hide:
  - navigation
---

# Glossary

Every piece of shorthand used on this site, in plain words. On any page you can also hover a dotted-underlined term
to see a one-line definition.

## The two test sets

eval2
:   The **main benchmark** since 2026-09-24: 1,991 questions about 647 texts, written to look like the real task
    (hard, trap-heavy, texts from 8 to 8K tokens). Written by three LLMs that never wrote training data, and a question
    is kept only when two other LLMs, judging blind, give the same answer. Nothing is ever trained or tuned on it.
    Jev scores 97.2%, our best model 92.7%. Details: [data](data.md#eval2-the-frozen-target-task-test-set).

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
:   38,628 more verified hard cases, built with round 2's lessons. Its training run was stopped halfway, so it is not
    measured yet.

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

stock pairs
:   The standard way to use a reranker: one sequence per (text, question, candidate). Accurate, but the text is re-read
    for every candidate.

shared-prefix tree (tree)
:   Our architecture: the text is read once, and every question and candidate branches off it, still attending to the
    text in every layer. Same quality as stock pairs, up to 37× faster. [Details](tree_model.md).

reranker / Instruct base
:   The two Qwen3 4B starting models: Qwen3-Reranker-4B (built to judge relevance) and Qwen3-4B-Instruct-2507 (a
    general chat model). The Instruct base does better once the data is good.

LoRA
:   A small set of trainable weights added to a frozen model (0.3% of a 4B model). The only thing we train.

r16 / r64 (rank)
:   The size of the LoRA adapter: rank 64 has 4× the trainable weights of rank 16.

MLP targets
:   LoRA also on the feed-forward layers, not only on attention: more trainable capacity.

all options in the question (OVA)
:   Every candidate is listed in the question text, so each judgment sees the alternatives. Helped by about one point.

teacher / KD
:   Qwen3.8-27B, a larger model used zero-shot as a *teacher*; knowledge distillation (KD) trains our model on its
    probabilities. It did not help.

custom model
:   A first attempt at "read the text once": new cross-attention layers on top of a frozen encoder. Fast but inaccurate.
    [Details](custom_model.md).

merged / vLLM
:   Serving tricks: *merged* folds the LoRA into the base weights; *vLLM* is a fast inference server whose prefix
    cache shares the text between questions.

compact format
:   A shorter tree layout tested for speed; it did not pay off.

### Reading a run name

Run names are built from these pieces:

| piece | meaning |
|---|---|
| `tree_` / `lora_` | shared-prefix tree / stock pairs |
| `4b`, `8b`, `pilot` | model size (`pilot` = the first 0.6B run) |
| `instruct` | Qwen3-4B-Instruct base instead of the reranker |
| `r2`, `r2b`, `r3`, `r2x64` | training data round 2, 2b or 3 (none = round 1); `r2x64` = round 2 × rank 64 |
| `r64`, `mlp` | LoRA rank 64, MLP targets (none = rank 16 on attention) |
| `ova`, `kd` | all options in the question, distillation from the 27B teacher |
| `baseline` | untrained model |
| `curve/` | one of the learning-curve / ablation runs |

So `tree_4b_instruct_r2x64` = tree scorer, 4B, Instruct base, round-2(b) data × rank 64: the best model.

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

A10G, L40S, H100
:   NVIDIA GPUs, from slowest to fastest, rented on AWS (g5, g6e, p5 instances).

CLINC, Banking77, AG News, DBpedia, TREC, BoolQ, SST-2, MNLI, GoEmotions, TweetEval
:   Public classification datasets in the dev benchmark (intents, topics, question types, yes/no reading, sentiment,
    entailment, emotions).
