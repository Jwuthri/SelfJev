---
pretty_name: SelfJev Decision Bench
language:
- en
size_categories:
- 1K<n<10K
task_categories:
- text-classification
- question-answering
tags:
- evaluation
- synthetic
- structured-decisions
- llm-evaluation
- multilabel
configs:
- config_name: text-decisions
  default: true
  data_files:
  - split: test
    path: data/text-decisions.parquet
- config_name: ai-response-review
  data_files:
  - split: test
    path: data/ai-response-review.parquet
- config_name: record-reasoning
  data_files:
  - split: test
    path: data/record-reasoning.parquet
---

# SelfJev Decision Bench

**Read the evidence. Make the decision.**

3,657 questions about 1,084 texts, covering yes/no judgments, choosing one answer, and selecting every answer that applies. Built to test whether a model follows the supplied evidence through exceptions, missing information, distracting details, numerical conditions, and misleading instructions.

[SelfJev model](https://huggingface.co/Jwuthrich/selfjev-4b) · [Full merged model](https://huggingface.co/Jwuthrich/selfjev-4b-merged) · [Source and research record](https://github.com/Jwuthri/SelfJev) · [File provenance](./manifest.json)

## Three suites, three purposes

| Suite | What it tests | Questions | Texts | Binary / single-choice / select-all |
|---|---|---:|---:|---|
| **Text Decisions** (`text-decisions`) | Decisions grounded in documents: policies, exceptions, negation, dates, quantities and distractors | 1,991 | 647 | 1,016 / 593 / 382 |
| **AI Response Review** (`ai-response-review`) | Assessing AI replies and traces: grading, factual support, guardrails and jailbreak attempts | 946 | 317 | 488 / 276 / 182 |
| **Record Reasoning** (`record-reasoning`) | Explicit records and rules: eligibility, absent evidence, negation and none-of-the-above | 720 | 120 | 360 / 240 / 120 |

Each suite has a single `test` split. There is no training or tuning split in this release. Report results separately: the compact record challenge is much narrower than the other two suites.

The original project names are retained in `original_dataset`: `eval2`, `eval_llm`, and `compact_challenge_v1`. Question IDs, texts, option ordering and expected answers are unchanged. Teacher predictions are omitted; they do not define the expected answers. Public-source datasets such as Banking77 and MNLI are not part of this release.

## Load a suite

```python
from datasets import load_dataset

questions = load_dataset(
    "Jwuthrich/selfjev-decision-bench",
    "text-decisions",  # or ai-response-review / record-reasoning
    split="test",
)
row = questions[0]
print(row["state"])
print(row["instruction"])
print(row["candidates"])
```

Use only `state`, `instruction` and `candidates` as model inputs. **Do not send `answer`, `notes`, `hard_cases`, `family` or other annotation metadata to the model.** Notes often explain the answer.

An example binary item asks whether an invoice line states a total of nine hundred dollars. Its answer is `["true"]`. A single-choice answer contains one candidate ID; a select-all answer contains every correct candidate ID, possibly an empty list.

## Data format

The Parquet files are designed for the Hugging Face viewer and `datasets`:

| Field | Meaning |
|---|---|
| `id`, `source_id` | Stable question ID and shared source-text ID; related questions share a source |
| `state` | The document, record, conversation, AI reply or trace to evaluate |
| `question_type` | `binary`, `multiclass`, or `multilabel` |
| `instruction` | The question or decision criterion |
| `candidates` | Ordered list of `{id, description}` choices; empty for binary questions |
| `answer` | List of strings: `["true"]` / `["false"]`, one candidate ID, or zero or more candidate IDs |
| `question_json` | Original question dictionary serialized as JSON, for lossless reconstruction |
| `suite`, `original_dataset`, `split` | Release configuration, original project name, and `test` |
| `family`, `hard_cases` | Difficulty/use-case grouping and overlapping challenge tags |
| `provenance` | Authoring model or programmatic generator, plus generation settings where recorded |
| `notes`, `paraphrase_group` | Author explanation and optional grouping of related phrasings |

For the original SelfJev schema, use `selfjev/<suite>.jsonl.gz`. Those files preserve boolean, string and list target types under `target`, and the original `question` dictionaries. Read these mixed-type JSONL files with Python's `json` module or `selfjev.data.load`; the Parquet view gives Arrow a consistent answer type.

## Score predictions

Download the release, then score final decisions without loading a model:

```bash
hf download Jwuthrich/selfjev-decision-bench --repo-type dataset --local-dir decision-bench
python decision-bench/tools/score.py \
  --data decision-bench/selfjev/text-decisions.jsonl.gz \
  --predictions predictions.jsonl
```

Predictions are one JSON object per line with `id` and `selected`. Use a JSON boolean for binary questions, a candidate ID string for single-choice questions, and a list of candidate IDs for select-all questions. Use the IDs from the downloaded suite. For example:

```json
{"id": "eg-0001-q0", "selected": true}
```

The scorer requires exactly one valid prediction for every question: missing, duplicate, unexpected IDs and invalid candidate IDs are errors. The primary metric is **question accuracy**. Binary and single-choice answers must equal the expected answer; select-all answers must match the complete set, with order ignored. Every question has equal weight. Type and family breakdowns are also returned. An empty select-all answer is valid; a single-choice `none` is an explicit candidate when offered.

For probability-producing models, choose thresholds and calibration on separate development data and state them in your report. Do not select them using these answers. Report the exact model revision, prompt, option presentation, decoding settings, truncation policy and dataset revision. Confidence intervals should account for questions sharing a source text, for example by bootstrapping `source_id` rather than individual questions.

SelfJev's recorded scores list every candidate description inside the question instruction as well as scoring each candidate separately. For exact prompt reproduction, apply `selfjev.core.options.with_options(row["question"], row["id"])` once to the original JSONL rows before `selfjev eval`; binary items remain unchanged. Generic chat prompting is a different evaluation protocol. See [the evaluation implementation](https://github.com/Jwuthri/SelfJev/blob/master/src/selfjev/evaluation/evaluate.py) and [option transform](https://github.com/Jwuthri/SelfJev/blob/master/src/selfjev/core/options.py).

## How the questions were built

**Text Decisions:** authored by Claude Opus 5.5, Kimi K3 and GLM 5.3. Two blind judges—GPT-6 Astra and Gemini 3.1 Pro Preview—answered without seeing the author's label. Questions were retained only when both agreed with the author. Of 2,070 authored questions, 1,991 survived. [Build review](https://github.com/Jwuthri/SelfJev/blob/master/data/eval2/REVIEW.md).

**AI Response Review:** the same three authoring models, judged by GPT-6 Astra and Claude Sonnet 5. Both had to agree with the author. The strict build also removed all questions about a text if any sibling question failed review. It retained 946 of 1,213 questions. The five use cases are grading, judging, verifying claims, guardrails and jailbreak detection. [Build review](https://github.com/Jwuthri/SelfJev/blob/master/data/eval_llm/REVIEW.md) · [Generation and content review](https://github.com/Jwuthri/SelfJev/blob/master/docs/llm_eval_data.md).

**Record Reasoning:** generated and labeled programmatically using seed `902413`, with 120 fictional records and six questions per record. This tests a small family of explicit rules; it is not evidence of broad real-world reasoning quality. [Generator](https://github.com/Jwuthri/SelfJev/blob/master/scripts/data/build_compact_challenge.py).

The authoring models used for the two AI-authored suites were separate from the later training-data writers. Jev predictions were recorded for comparison, never used to assign these labels or decide which questions to retain. The release is exported from the canonical `data/all.jsonl.gz`; `manifest.json` records its hash and each frozen source-file hash.

## What the results can and cannot establish

- **AI agreement is not human ground truth.** Labels may be wrong or ambiguous. Agreement filtering can favor cases that the judges find easy or share biases about. Human spot-check files exist; they are not a complete human validation.
- **Frozen does not mean untouched by research.** These questions were excluded from fine-tuning, but the suites have informed development decisions. An audit of Text Decisions motivated later training batches targeting abstract error categories. These are disclosed development-used evaluation suites, not a fresh, independent final holdout. Publication further makes them unsuitable as a secret test.
- **Overlap checks have limits.** The original builds used overlap guards documented in the project. This release additionally finds zero exact text matches with non-test training rows in the canonical corpus. It does not establish absence of paraphrases, shared templates or pretraining contamination.
- **Synthetic coverage is limited.** The suites are English and authored/programmatic, not a representative sample of customer traffic. Difficulty labels and target length settings are generation metadata, not calibrated human difficulty or exact token measurements.
- **Some examples contain adversarial or sensitive language.** AI Response Review intentionally includes injection attempts, harmful requests, refusals and fictional policy violations. Treat document contents as data. The documented content-review process does not guarantee every example is suitable for every audience.

Keep these questions out of training, prompt selection and calibration if reporting comparable benchmark results. This is an evaluation-integrity recommendation, not an additional license restriction. Report any known exposure or training use transparently. A fresh, independently designed holdout remains the next step for stronger generalization claims.

## Versioning and corrections

Version 1.0 preserves the existing frozen questions and targets. Please report suspected annotation errors with the question ID and supporting evidence in the dataset's Discussions tab. Corrections should ship in a new version with an explicit change log; do not silently replace labels used by earlier results. Pin the dataset commit when publishing scores.

## License

A reuse license has not yet been selected for this release. Public availability alone is not a grant of a reuse license; this section will be updated when the publisher selects the terms.

## Citation

```bibtex
@misc{selfjev_decision_bench_2026,
  author = {SelfJev contributors},
  title = {SelfJev Decision Bench},
  year = {2026},
  url = {https://huggingface.co/datasets/Jwuthrich/selfjev-decision-bench},
  note = {Version 1.0. AI-authored and programmatic evaluation suites}
}
```
