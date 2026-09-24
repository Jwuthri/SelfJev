# Open questions

What we would do next, in priority order. To work on one, claim it in the *Open ideas* table of the
[experiment ledger](experiments.md#open-ideas-claim-before-starting-edit-the-status-cell) first; paid runs need the
user's OK with a price.

## 1. Close the quality gap (4.5 points on eval2)

| idea | why | cost |
|---|---|---|
| **Round 3, full run**: best recipe + 38.6K new verified questions | data was the biggest lever (+5.5); the first run was stopped at step ≈ 500 of 915, and its step-300 checkpoint (90.8) is not a verdict | ~10 h A10G ≈ $10 |
| **Multilabel with many positives** | multilabel exact match is the largest gap (83.5 vs 94.2); round 3 has 54% of multilabel questions with 3+ positives, round 2 had 21% | covered by round 3 |
| **Numbers, dates and grading** with verified answers | numeric 82.1 vs 92.0, temporal 82.8 vs 89.2; the agent-output grading family is still excluded from training on purpose | generation + blind judge |
| **Use the 27B teacher better**: multiclass-only distillation, a lower weight, an r64 student, or serve the ensemble | the 50/50 ensemble scores 94.5, distillation at weight 0.5 gave nothing | ≈ $3 GPU each |
| **Rejection as its own decision**: a permutation-invariant `none` rule; balanced in/out-of-scope pairs | the round-2 regression was entirely over-rejection | data + small code |
| **Tree full fine-tune** | the upper bound on capacity | needs ≥ 48 GB GPU and code |

## 2. Close the speed gap (5× at 4K tokens)

| idea | why | cost |
|---|---|---|
| **The same sweep on an H100** (vLLM, bf16 and FP8) | Jev's flat ~150 ms at 4K tokens × 16 questions needs ≥ 10× an A10G's compute; tells whether our model can match it on better hardware | ≈ $5 (capacity permitting) |
| **Qwen3.5-4B with a forked native cache**, best recipe | Qwen3.5-2B reached 79.9 on round-1 data and was 1.4–2× faster at 8K tokens | ≈ $5, claimed, awaiting OK |
| **Smaller tree student** (0.6B / 1.7B) distilled from the 4B | the 0.6B trained directly is 17 points behind | 1 GPU-day |
| **Structured attention kernel** for the tree | the direct branch mask is done; matmuls and attention dominate | code |
| **vLLM path on eval2** | serving quality was only checked on the dev benchmark | ≈ 15 min GPU |

## 3. Trust the numbers

| idea | why | cost |
|---|---|---|
| **Fresh final test set** (new authors, templates, documents) | both current test sets have informed decisions | ≈ $40 API |
| **Second seeds** for `tree_4b_ova` and `tree_4b_instruct_r2x64` | every result is one run; several wins are p ≈ 0.06–0.07 | ≈ $3 each |
| **Public JevBench items** for our best tree; Laya, open-jev-deberta and kev-4b on eval2 | the only shared yardstick across open Jev-like models | $0 |
| **Calibration policy**: temperatures separate from thresholds, thresholds for accuracy on a separate split | the current file costs 2.3 points | code |
| **Label-free binary bias fix** (e.g. contextual calibration) chosen on validation | SST-2 ranks well (AUROC 0.973) but predicts positive 34.7% of the time | ≈ 1 h GPU |
| **Stock 4B on round-2 data** | the stock-vs-tree control for round 2 was never finished | ~1 h A10G |

## Smaller follow-ups

- jina 0.6B: 2 epochs, r64 + MLP, pairwise layout (configs ready in `configs/jina_r2b_*.json`).
- Round-2 mix: add `none`-offered-but-wrong intent-like texts; subsample hard cases to ≈ 30% of training.
- Prompt-template robustness: a random prompt mapping per training example, averaged at eval.
- T5Gemma 2 with the encoder adapted too (in progress in another session).
