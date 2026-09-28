# Open questions

What we would do next, in priority order. To work on one, claim it in the *Open ideas* table of the
[experiment ledger](experiments.md#open-ideas-claim-before-starting-edit-the-status-cell) first; paid runs need the
user's OK with a price.

## 1. Close the quality gap (1.4 points on eval2)

The default model, `selfjev-4b`, scores 95.8 against Jev's 97.2 on eval2 (and is level on eval_llm, 93.1 vs 92.5). The
largest slice gaps are multi-positive questions (91.0 vs 96.0), numeric reasoning (87.5 vs 92.0), multi-turn (92.6 vs
96.0), distractors (93.9 vs 97.0) and multilabel exact match (91.4 vs 94.2)
([eval2 summary](../reports/eval2/summary.md)).

| idea | why | cost |
|---|---|---|
| ~~Several correct answers, distractors, numbers~~: **tried, worse.** Batch `mpos_distr_num_v1` (3,645 verified questions) in the retrain `selfjev_4b_v2`: eval2 95.4 vs 95.8 (p = 0.42), eval_llm 90.5 vs 93.1 (p = 0.0002); not promoted. More data of this kind is not the lever; a different readout (below) may be | wrong questions on eval2 vs Jev: multi-positive 29 vs 13, distractor 29 vs 14, numeric 28 vs 18 (a test diagnosis) | spent: $19.81 data + ≈ $21.46 GPU |
| **Dates and grading** with verified answers | temporal 88.2 vs 89.2 on eval2, Jev's weakest slice too; numbers are partly covered by `numdate_neg_v1` (in `selfjev-4b`) and the batch above | generation + blind judge |
| **Parallel-readout branch** (one branch per question, a yes/no readout per option + `none`, listwise loss) | the shape Jev's disclosures imply; multilabel and `none` decided jointly ([memo](../reports/jev_hypothesis_2026-09-25.md)) | code + one retrain (≈ $21 at `selfjev-4b`'s size) |

## 2. Time the default model, then close the speed gap

Jev answers in a flat ~100–135 ms server side. On one H100 the Qwen3 tree on vLLM is faster than that in every cell
but 4,096 tokens × 16 questions (22–82 ms for one question, 58–189 ms for 16; 2026-09-26), so for that model speed is a
deployment question (GPU class and placement), not a model question. The default `selfjev-4b` (Qwen3.5) is served by
`TreeServer`, which does the same work as the Qwen3 tree (the text once), but **it has not been timed on a GPU**; on
vLLM the same architecture is fast for one question and slow for many ([speed](speed.md)).

| idea | why | cost |
|---|---|---|
| **Time `TreeServer` on a GPU**: `selfjev bench`, then against Jev and vLLM on the same requests; on an L40S, on the L4 that `selfjev deploy aws` uses by default (g6.xlarge), then an H100 | no GPU latency exists for the served model; the Jev side-by-side script (`scripts/latency_sweep.py`) is at tag `archive/pre-cleanup-2026-09-27` | ≈ 1 h L40S ≈ $2.50; L4 $0.805/h |
| **Route by question count**: vLLM for 1–2 questions, `TreeServer` for more | vLLM answers one question in 87 ms at 512 tokens on an L40S (the old forked-cache engine: 156 ms), but takes 454–1,138 ms for 16 questions | half a day, after the timing |
| **Patch vLLM** to checkpoint the recurrent state where prompts stop sharing tokens | the root cause of the slow multi-question case; 0.30 does it only for speculative decoding | code |
| **Smaller tree student** (Qwen3.5-0.8B or 2B) distilled from `selfjev-4b` | the 0.6B Qwen3 reranker trained directly is 17 points behind; `selfjev` trains Qwen3.5-4B only, so this needs code | code + 1 GPU-day |

## 3. Trust the numbers

| idea | why | cost |
|---|---|---|
| **Fresh final test set** (new authors, templates, documents) | eval2 and the dev benchmark have informed decisions, and eval_llm now informs promotions | ≈ $40 API |
| **Second seeds** for the best runs | measured once: rerunning `selfjev-4b`'s exact recipe moved eval2 by −0.7 and eval_llm by −1.2 (not significant; [findings 5b](findings.md)), so wins of about a point need two or more runs per arm | ≈ $20 each (one L40S, ≈ 9 h) |
| **Public JevBench items** for our best model; Laya, open-jev-deberta and kev-4b on eval2 | the only shared yardstick across open Jev-like models | no API cost; GPU time (never on the laptop) |
| **Calibration policy**: temperatures separate from thresholds, thresholds for accuracy on a separate split | the F1 thresholds fitted for `tree_4b` cost accuracy (81.6 → 79.3); Jev's soft targets moved calibration, RLCD did not | code |

## Done since the last version of this page

- Round 3 (38.6K verified questions) and options in the question: 94.5 each way, and they stack.
- Qwen3.5-4B with a forked cache (94.5), then trained with its own tree (**95.6**).
- The vLLM path scored on eval2: the same accuracy as transformers for both best models of the time.
- The H100 sweep (2026-09-26): the Qwen3 tree on vLLM beats Jev's server time in every cell but 4,096 tokens × 16
  questions, and the rest of the gap is network ([speed](speed.md#the-same-model-on-an-h100-2026-09-26)).
- `selfjev finetune` and `selfjev rlcd`, and the best weights in the repo ([weights/](../weights/README.md)).
- Jev's probabilities as soft targets, and RLCD with a confident-mistake cost: confident mistakes on eval2 30 → 14 and 8,
  accuracy flat. Retrained from scratch on everything with them, with the LLM-evaluation data and texts up to 16K
  (150 questions dropped instead of 2,548 at 8K; long-text errors on eval2 8 → 3): **`selfjev-4b`**, the default
  (eval2 95.8, eval_llm 93.1).
- The 2026-09-27 cleanup: one model (`selfjev-4b`), the `selfjev` package with Jev's HTTP API ([API](api.md)), an SDK,
  fine-tuning over HTTP and `selfjev deploy aws` ([deploy](deploy.md)). Everything else is at tag
  `archive/pre-cleanup-2026-09-27`.
- Closed or parked at the cleanup:
  - distilling the 27B teacher further (weight 0.5 gave nothing); its code is at the tag;
  - the serving ensemble: the fixed 50/50 average of `qwen35_4b_tree` and `tree_4b_combo` scored 95.9 on eval2, 96.5
    with the 27B teacher ([ensembles](../reports/eval2/ensembles.md)), but both adapters, the teacher's code and
    `scripts/ensemble_eval2.py` are only at the tag now, and `selfjev-4b` alone scores 95.8.
