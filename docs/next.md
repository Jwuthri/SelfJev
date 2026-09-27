# Open questions

What we would do next, in priority order. To work on one, claim it in the *Open ideas* table of the
[experiment ledger](experiments.md#open-ideas-claim-before-starting-edit-the-status-cell) first; paid runs need the
user's OK with a price.

## 1. Close the quality gap (1.4 points on eval2)

The default model, `selfjev-4b`, scores 95.8 against Jev's 97.2. The largest slice gaps are multi-positive questions
(91.0 vs 96.0), numeric reasoning (87.5 vs 92.0), distractors (93.9 vs 97.0) and multilabel exact match (91.4 vs 94.2)
([eval2 summary](../reports/eval2/summary.md)).

| idea | why | cost |
|---|---|---|
| **Multilabel with many positives**: more verified questions with 3+ correct labels and zero-positive ones | multi-positive 91.0 vs 96.0, multilabel exact match 91.4 vs 94.2 | generation + blind judge |
| **Numbers, dates and grading** with verified answers | numeric 87.5 vs 92.0, temporal 88.2 vs 89.2 on eval2 | generation + blind judge |
| **Question-level sharing in the Qwen3.5 tree for longer questions**, and texts beyond 8K in training | the tree made 8K training possible; 2,013 questions (3.7%) are still dropped | GPU time only |
| **Parallel-readout branch** (one branch per question, a yes/no readout per option + `none`, listwise loss) | the shape Jev's disclosures imply; multilabel and `none` decided jointly ([memo](../reports/jev_hypothesis_2026-09-25.md)) | code + ≈ $12 |
| **Serving cascade / ensemble**: the 50/50 average of `qwen35_4b_tree` and `tree_4b_combo` scores 95.9 on eval2, with the 27B teacher 96.5 (nothing fitted) | two models' errors overlap little (either is right on 97.6%) | $0 to decide; 2× serving compute |

## 2. Close the speed gap

Jev answers in a flat ~100–130 ms server side. On one H100 the Qwen3 tree on vLLM is faster than that at every size
(22–82 ms for one question, 58–189 ms for 16; 2026-09-26), so the remaining end-to-end gap is network distance and
speed is a deployment question (GPU class and placement), not a model question. On an A10G or L40S it matches Jev
only for one question up to ~1K tokens; the Qwen3.5 model is slow with many questions on vLLM.

| idea | why | cost |
|---|---|---|
| **Time `qwen35_tree.TreeServer` on a GPU** against Jev and the Qwen3 tree, same requests | it does the same work as the Qwen3 tree (text once), where vLLM recomputes up to 527 text tokens per candidate; exact in the CPU test | ≈ 1 h L40S ≈ $2.50 |
| **Route by question count**: vLLM for 1–2 questions, the tree server for more | vLLM wins on one question (87 vs 156 ms at 512 tokens), the tree path on many | half a day |
| **Patch vLLM** to checkpoint the recurrent state where prompts stop sharing tokens | the root cause of the slow multi-question case; 0.30 does it only for speculative decoding | code |
| **An H100 sweep** (vLLM, bf16 and FP8) | per-token speed is the limit once the text is shared; never obtained on AWS | ≈ $5 (capacity permitting) |
| **Smaller tree student** (0.6B / 1.7B) distilled from the best model | the 0.6B trained directly is 17 points behind | 1 GPU-day |

## 3. Trust the numbers

| idea | why | cost |
|---|---|---|
| **Fresh final test set** (new authors, templates, documents) | both current test sets have informed decisions | ≈ $40 API |
| **Second seeds** for the best runs | every result is one run; several wins are p ≈ 0.03–0.07 | ≈ $10 each on an L40S |
| **Public JevBench items** for our best model; Laya, open-jev-deberta and kev-4b on eval2 | the only shared yardstick across open Jev-like models | $0 |
| **Calibration policy**: temperatures separate from thresholds, thresholds for accuracy on a separate split | the current fitted file costs accuracy; RLCD on hard labels did not change calibration | code |

## Done since the last version of this page

- Round 3 (38.6K verified questions) and options in the question: 94.5 each way, and they stack.
- Qwen3.5-4B with a forked cache (94.5), then trained with its own tree (**95.6**).
- The vLLM path scored on eval2: the same accuracy as transformers for both best models.
- `selfjev finetune` and `selfjev rlcd`, and the best weights in the repo ([weights/](../weights/README.md)).
- Jev's probabilities as soft targets, and RLCD with a confident-mistake cost: confident mistakes on eval2 30 → 14 and 8,
  accuracy flat. Retrained from scratch on everything with them: **`selfjev-4b`**, the default (eval2 95.8, eval_llm 93.1).
- Distilling the 27B teacher further was dropped (weight 0.5 gave nothing); its code is at tag
  `archive/pre-cleanup-2026-09-27`.
