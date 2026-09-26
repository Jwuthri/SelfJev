# Open questions

What we would do next, in priority order. To work on one, claim it in the *Open ideas* table of the
[experiment ledger](experiments.md#open-ideas-claim-before-starting-edit-the-status-cell) first; paid runs need the
user's OK with a price.

## 1. Close the quality gap (1.6 points on eval2)

The best model, `qwen35_4b_tree`, scores 95.6 against Jev's 97.2. Multilabel is still about half of the gap
(exact match 90.1 vs 94.2), then numbers and dates.

| idea | why | cost |
|---|---|---|
| **RLCD with a reward that carries more than the label**: soft targets (the two judges' agreement, a teacher's probabilities) or a cost that punishes confident mistakes | the first RLCD test on hard labels gave nothing (accuracy 95.63 vs 95.58, ECE 0.010 vs 0.005); Jev's edge is hedged mistakes (7 of 57 at ≥ 0.9, ours 30 of 99) | ≈ $6 per test on an L40S |
| **Multilabel with many positives**: more verified questions with 3+ correct labels and zero-positive ones | the largest remaining slice gap (90.1 vs 94.2 exact match) | generation + blind judge |
| **Numbers, dates and grading** with verified answers | numeric 88.4 vs 92.0, temporal 85.7 vs 89.2 on eval2 | generation + blind judge |
| **Question-level sharing in the Qwen3.5 tree for longer questions**, and texts beyond 8K in training | the tree made 8K training possible; 2,013 questions (3.7%) are still dropped | GPU time only |
| **Parallel-readout branch** (one branch per question, a yes/no readout per option + `none`, listwise loss) | the shape Jev's disclosures imply; multilabel and `none` decided jointly ([memo](../reports/jev_hypothesis_2026-09-25.md)) | code + ≈ $12 |
| **Serving cascade / ensemble**: the 50/50 average of `qwen35_4b_tree` and `tree_4b_combo` scores 95.9 on eval2, with the 27B teacher 96.5 (nothing fitted) | two models' errors overlap little (either is right on 97.6%) | $0 to decide; 2× serving compute |
| **Use the 27B teacher better**: multiclass-only distillation, a lower weight | distillation at weight 0.5 gave nothing | ≈ $3 GPU each |

## 2. Close the speed gap

Jev answers in a flat ~100–130 ms server side. The Qwen3 tree on vLLM matches that for one question up to ~1K tokens
and is cheaper per request; the Qwen3.5 model is slow with many questions on vLLM.

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
- `pjev finetune` and `pjev rlcd`, and the best weights in the repo ([weights/](../weights/README.md)).
