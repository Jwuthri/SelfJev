# Experiment ledger

Every session (Claude Code, Codex, human) reads this before starting work and appends to it when a run finishes.
The table is generated from `reports/*/test/report.json` by `uv run python scripts/ledger.py`; the text sections
are hand-written. All numbers are on the shared test split: 3,471 questions = `hf.jsonl` test + `eval.jsonl` test,
identical ids for every model. Never train or tune on it.

## Results (old test split, 3,471 questions, sorted by its question accuracy; eval2 column where scored; the report links are the old-test `test/report.md` files)

<!-- ledger:start -->
| run | base | architecture | trained on | **eval2 acc %** (target task, 1,991 q) | old-test question acc % | binary acc % | binary AUROC | multiclass acc % | multilabel EM % | authored eval_* acc % (n=171) | report | weights |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| external | openai/gpt-6-astra | external API | — | — | 85.8 | 93.8 | 0.971 | 87.0 | 55.8 | 100.0 | [report](../reports/external/test/report.md) | — |
| external | ~typesafe/jev-latest | external API | — | 97.2 | 82.7 | 93.5 | 0.981 | 84.6 | 40.1 | 94.7 | [report](../reports/external/test/report.md) | — |
| tree_4b_instruct_r2x64 | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | 18,681 q / 218 steps | 92.7 | 82.7 | 90.9 | 0.965 | 83.7 | 52.9 | 81.9 | [report](../reports/tree_4b_instruct_r2x64/test/report.md) | runs/tree_4b_instruct_r2x64/adapter |
| tree_4b_ova | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,372 q / 241 steps | 91.6 | 82.6 | 89.2 | 0.962 | 83.6 | 57.8 | 84.2 | [report](../reports/tree_4b_ova/test/report.md) | runs/tree_4b_ova/adapter |
| tree_4b_ova_kd | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,372 q / 241 steps | 91.0 | 82.5 | 88.1 | 0.959 | 83.8 | 58.4 | 84.8 | [report](../reports/tree_4b_ova_kd/test/report.md) | runs/tree_4b_ova_kd/adapter |
| curve/tree_4b_r2b_r64_mlp | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,375 q / 208 steps | 91.3 | 82.4 | 89.0 | 0.962 | 83.5 | 57.0 | 84.2 | [report](../reports/curve/tree_4b_r2b_r64_mlp/test/report.md) | runs/curve/tree_4b_r2b_r64_mlp/adapter |
| tree_4b | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 10,112 q / 84 steps | 85.1 | 81.6 | 87.1 | 0.953 | 83.9 | 51.7 | 78.4 | [report](../reports/tree_4b/test/report.md) | runs/tree_4b/adapter |
| curve/tree_4b_mlp | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 10,080 q / 84 steps | 86.3 | 81.6 | 87.9 | 0.955 | 83.4 | 51.7 | 78.9 | [report](../reports/curve/tree_4b_mlp/test/report.md) | runs/curve/tree_4b_mlp/adapter |
| curve/tree_4b_r64 | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 10,080 q / 84 steps | 87.2 | 81.5 | 88.5 | 0.956 | 83.0 | 52.3 | 77.8 | [report](../reports/curve/tree_4b_r64/test/report.md) | runs/curve/tree_4b_r64/adapter |
| tree_4b_instruct_r3_step300 | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | — | 90.8 | 81.5 | 89.4 | 0.954 | 82.5 | 52.6 | 81.3 | [report](../reports/tree_4b_instruct_r3_step300/test/report.md) | — |
| tree_4b_r2b | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,375 q / 225 steps | 90.6 | 81.2 | 88.1 | 0.955 | 82.8 | 51.7 | 83.0 | [report](../reports/tree_4b_r2b/test/report.md) | runs/tree_4b_r2b/adapter |
| curve/tree_4b_r2b_r64 | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,375 q / 208 steps | 90.3 | 81.2 | 87.8 | 0.962 | 82.5 | 54.4 | 82.5 | [report](../reports/curve/tree_4b_r2b_r64/test/report.md) | runs/curve/tree_4b_r2b_r64/adapter |
| curve/boolq_300 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,412 q / 218 steps | — | 80.9 | 88.0 | 0.940 | 82.5 | 50.9 | 71.9 | [report](../reports/curve/boolq_300/test/report.md) | runs/curve/boolq_300/adapter |
| curve/boolq_1000 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 11,112 q / 224 steps | — | 80.9 | 88.8 | 0.954 | 82.5 | 48.8 | 73.7 | [report](../reports/curve/boolq_1000/test/report.md) | runs/curve/boolq_1000/adapter |
| curve/boolq_3000 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 13,112 q / 240 steps | — | 80.9 | 88.9 | 0.954 | 82.5 | 47.7 | 73.1 | [report](../reports/curve/boolq_3000/test/report.md) | runs/curve/boolq_3000/adapter |
| lora_8b | Qwen3-Reranker-8B | stock pairs (task-v1) | 10,112 q / 185 steps | — | 80.7 | 87.3 | 0.945 | 82.9 | 48.0 | 74.9 | [report](../reports/lora_8b/test/report.md) | runs/lora_8b/adapter |
| tree_4b_r2 | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,357 q / 224 steps | 90.4 | 80.6 | 87.6 | 0.956 | 82.2 | 50.9 | 81.9 | [report](../reports/tree_4b_r2/test/report.md) | runs/tree_4b_r2/adapter |
| curve/instruct_lora | Qwen3-4B-Instruct-2507 | stock pairs (answer-v1) | 10,112 q / 216 steps | — | 80.6 | 87.4 | 0.944 | 82.6 | 48.3 | 75.4 | [report](../reports/curve/instruct_lora/test/report.md) | runs/curve/instruct_lora/adapter |
| tree_4b_instruct | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | 10,112 q / 78 steps | 88.1 | 80.4 | 87.8 | 0.958 | 82.3 | 46.8 | 79.5 | [report](../reports/tree_4b_instruct/test/report.md) | runs/tree_4b_instruct/adapter |
| lora_4b | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,112 q / 216 steps | 86.5 | 80.3 | 87.5 | 0.945 | 82.3 | 47.7 | 70.8 | [report](../reports/lora_4b/test/report.md) | runs/lora_4b/adapter |
| curve/boolq_100 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,212 q / 217 steps | — | 80.0 | 86.9 | 0.945 | 82.0 | 48.3 | 70.8 | [report](../reports/curve/boolq_100/test/report.md) | runs/curve/boolq_100/adapter |
| curve/vol100_e2 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,112 q / 431 steps | — | 79.8 | 87.0 | 0.951 | 81.9 | 46.2 | 69.6 | [report](../reports/curve/vol100_e2/test/report.md) | runs/curve/vol100_e2/adapter |
| curve/vol50_e2 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 5,056 q / 214 steps | — | 79.1 | 84.8 | 0.940 | 81.7 | 46.8 | 72.5 | [report](../reports/curve/vol50_e2/test/report.md) | runs/curve/vol50_e2/adapter |
| curve/vol25_e2 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 2,528 q / 107 steps | — | 79.1 | 85.7 | 0.935 | 81.4 | 45.6 | 73.7 | [report](../reports/curve/vol25_e2/test/report.md) | runs/curve/vol25_e2/adapter |
| curve/vol50_e1 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 5,056 q / 107 steps | — | 78.9 | 84.5 | 0.934 | 81.9 | 44.5 | 70.2 | [report](../reports/curve/vol50_e1/test/report.md) | runs/curve/vol50_e1/adapter |
| curve/vol25_e1 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 2,528 q / 53 steps | — | 77.0 | 83.8 | 0.930 | 80.8 | 33.4 | 71.9 | [report](../reports/curve/vol25_e1/test/report.md) | runs/curve/vol25_e1/adapter |
| jina_r2b | jinaai/jina-reranker-v3.5 | jina listwise (jina-v1) | 16,301 q / 345 steps | 73.3 | 76.6 | 81.4 | 0.888 | 79.4 | 45.1 | 60.2 | [report](../reports/jina_r2b/test/report.md) | runs/jina_r2b/adapter |
| t5_round2b_2026-09-24/t5_r1 | google/t5gemma-2-1b-1b | pretrained T5Gemma encoder/decoder; shared document cross-KV views | 10,080 q / 823 steps | 73.0 | 75.4 | 83.0 | 0.887 | 76.6 | 45.6 | 62.0 | [report](../reports/t5_round2b_2026-09-24/t5_r1/test/report.md) | runs/t5gemma2_r1_reference/adapter |
| t5_round2b_2026-09-24/decoder_only_audit/t5_r2b | google/t5gemma-2-1b-1b | pretrained T5Gemma encoder/decoder; shared document cross-KV views | 16,375 q / 228 steps | 76.8 | 73.8 | 82.7 | 0.893 | 75.1 | 40.4 | 62.6 | [report](../reports/t5_round2b_2026-09-24/decoder_only_audit/t5_r2b/test/report.md) | runs/t5gemma2_r2b/adapter |
| lora_pilot | Qwen3-Reranker-0.6B | stock pairs (task-v1) | 10,112 q / 183 steps | 68.8 | 73.5 | 77.8 | 0.863 | 78.3 | 31.1 | 55.0 | [report](../reports/lora_pilot/test/report.md) | runs/lora_pilot/adapter |
| curve/instruct_zero | Qwen3-4B-Instruct-2507 | stock pairs (answer-v1) | — | — | 71.3 | 84.2 | 0.911 | 73.5 | 20.1 | 63.2 | [report](../reports/curve/instruct_zero/test/report.md) | — |
| baseline_8b | Qwen3-Reranker-8B | stock pairs (task-v1) | — | — | 66.2 | 56.1 | 0.658 | 79.8 | 10.2 | 50.3 | [report](../reports/baseline_8b/test/report.md) | — |
| baseline_4b | Qwen3-Reranker-4B | stock pairs (answer-v1) | — | — | 62.8 | 55.0 | 0.604 | 76.2 | 2.0 | 44.4 | [report](../reports/baseline_4b/test/report.md) | — |
| baseline | Qwen3-Reranker-0.6B | stock pairs (task-v1) | — | — | 61.0 | 55.3 | 0.605 | 73.3 | 1.2 | 39.2 | [report](../reports/baseline/test/report.md) | — |
| custom_sim_lora | Qwen3-Reranker-0.6B | shared-state cross-attention (custom-v1) | 10,112 q / 1176 steps | — | 58.2 | 51.7 | 0.514 | 70.2 | 1.7 | 42.1 | [report](../reports/custom_sim_lora/test/report.md) | runs/custom_sim_lora/checkpoint |
| custom_sim_frozen | Qwen3-Reranker-0.6B | shared-state cross-attention (custom-v1) | 10,112 q / 1176 steps | — | 48.0 | 51.4 | 0.524 | 53.9 | 1.5 | 38.0 | [report](../reports/custom_sim_frozen/test/report.md) | runs/custom_sim_frozen/checkpoint |
| custom_distill_lora | Qwen3-Reranker-0.6B | shared-state cross-attention (custom-v1) | 16,671 q / 2028 steps | — | 39.7 | 51.3 | 0.451 | 40.6 | 0.9 | 35.1 | [report](../reports/custom_distill_lora/test/report.md) | runs/custom_distill_lora/checkpoint |
| custom_frozen | Qwen3-Reranker-0.6B | shared-state cross-attention (custom-v1) | 10,112 q / 1764 steps | — | 39.0 | 51.9 | 0.536 | 39.1 | 1.2 | 36.3 | [report](../reports/custom_frozen/test/report.md) | runs/custom_frozen/checkpoint |
| custom_distill_frozen | Qwen3-Reranker-0.6B | shared-state cross-attention (custom-v1) | 16,671 q / 2028 steps | — | 37.7 | 52.8 | 0.507 | 36.7 | 0.6 | 36.8 | [report](../reports/custom_distill_frozen/test/report.md) | runs/custom_distill_frozen/checkpoint |
<!-- ledger:end -->

## Results on eval2: the frozen target-task test set, primary benchmark from 2026-09-24

1,991 authored questions (`data/eval2.jsonl`, sha `2fa95459…`), with labels agreed by the author and two blind judges.
Full slices (type, tier, author, length, trap) and paired tests: [reports/eval2/summary.md](../reports/eval2/summary.md),
generated by `python3 scripts/eval2_summary.py`. Score new models with `scripts/run_eval2.sh`, then re-run the summary.
Never train, select prompts or fit calibration on eval2.

| model | eval2 acc % | binary | multiclass | multilabel EM | old test (3,471) |
|---|---|---|---|---|---|
| Jev | **97.2** | 97.8 | 98.1 | 94.2 | 82.7 |
| **tree_4b_instruct_r2x64** (**Instruct base**, round-2 data uncapped, **rank 64**) | **92.7** | 94.6 | 95.4 | 83.5 | 82.7 |
| tree_4b_ova (reranker, round-2b data, all options listed in the question) | 91.6 | 93.8 | 94.9 | 80.4 | 82.6 |
| curve/tree_4b_r2b_r64_mlp (reranker, round-2b data, **rank 64 + MLP**) | **91.3** | 93.7 | 94.3 | 80.4 | 82.4 |
| tree_4b_r2b (reranker, round-2 data, none capped) | **90.6** | 92.9 | 94.1 | 78.8 | 81.2 |
| curve/tree_4b_r2b_r64 (reranker, round-2b data, rank 64) | 90.3 | 92.9 | 94.9 | 75.9 | 81.2 |
| tree_4b_r2 (reranker, round-2 data) | 90.4 | 92.8 | 95.8 | 75.4 | 80.6 |
| tree_4b_instruct (**Instruct base**, round-1 data) | 88.1 | 91.4 | 92.7 | 72.3 | 80.4 |
| curve/tree_4b_r64 (reranker, **rank 64**, round-1 data) | 87.2 | 90.5 | 92.7 | 69.9 | 81.5 |
| lora_4b (stock pairs, round-1 data) | 86.5 | 89.7 | 91.6 | 70.4 | 80.3 |
| curve/tree_4b_mlp (reranker, r16 + MLP, round-1 data) | 86.3 | 90.0 | 91.9 | 68.1 | 81.6 |
| tree_4b (reranker, r16, round-1 data) | 85.1 | 89.4 | 91.6 | 63.9 | 81.6 |
| t5_round2b **decoder-only audit** (not intended full adaptation) | 76.8 | 82.6 | 83.6 | 50.8 | — |
| lora_pilot (0.6B stock, round-1 data) | 68.8 | 75.7 | 75.7 | 39.8 | 73.5 |

What each lever is worth on eval2, vs tree_4b at 85.1 (paired exact McNemar, only-row / only-ref):

| lever | gain | evidence |
|---|---|---|
| round-2 verified hard cases | **+5.5** (142 / 34, p = 7e-17) | tree_4b_r2b |
| Instruct base (Qwen3-4B-Instruct-2507) instead of the reranker | **+3.0** (129 / 69, p = 2e-5) | tree_4b_instruct |
| LoRA rank 64 instead of 16 | **+2.1** (77 / 36, p = 1e-4) | curve/tree_4b_r64 |
| MLP targets added | +1.2 (62 / 38, p = 0.02) | curve/tree_4b_mlp |
| stock pairs instead of tree | +1.4 (129 / 101, p = 0.08): the tree's speed costs no significant quality | lora_4b |
| 0.6B instead of 4B (stock) | **−17.7** vs stock 4B | lora_pilot |

- The old test called every one of these a tie or a loss. Its public-label noise capped every model at 80–86%.
- Data and capacity combined (fork 2, 03:10): round-2b + r64 → 90.3 (no gain, p = 0.61); round-2b + r64 + MLP → **91.3**
  (+0.7, p = 0.17). The levers overlap: capacity adds ≤ 1 point once the data is good.
- **Instruct base + round-2 data + r64** (`tree_4b_instruct_r2x64`, 03:35) is the best so far at **92.7**, and the base
  stacks with the data:
  - vs r2b: 90 / 47, p = 0.0003;
  - vs the Instruct base on round-1 data: 123 / 32, p = 9e-14;
  - vs tree_4b_ova: 78 / 55, p = 0.06;
  - vs Jev: 25 / 115, p = 5e-15, so Jev still leads by 4.5 points.
  - Old test: 82.7, identical to Jev (213 / 214).
  - Multilabel exact match: 83.5 (r2b 78.8, Jev 94.2).
  - Its recipe differs from r2b in three ways: base, r64, and the r2_* families left uncapped (7.2K vs 4.6K questions).
    Given r2b + r64 = 90.3, most of the gain is the base.
  - It is the control for round 3: same recipe plus `data/hardcases_r3.jsonl`.
- **Round 3 is still unmeasured.** Its run was stopped by someone at step ≈ 500 of 915 (JOURNAL 10:17). The best
  checkpoint saved before that (step 300, peak learning rate, about 1/3 of the data) scores 90.8 on eval2 and 81.5 on
  the old test (`tree_4b_instruct_r3_step300`). That is not a verdict on the data; a full run is needed.
- Scoring of the round-1 variants ran on AWS g5.xlarge, ≈ $1.12 (JOURNAL 2026-09-24 01:00).

## Conclusions so far (2026-09-23)

0. **(2026-09-24) Read the eval2 section above first.**
   - Conclusions 2–4 below and the dead-end rows were measured on the noisy old test. That test hid a +5.5-point data
     effect, so re-check any "no gain" there on eval2 before treating it as dead.

1. **Best model: shared-prefix tree scorer on Qwen3-Reranker-4B + LoRA r=16, round-1 data** (`runs/tree_4b`):
   81.6% vs 80.3% for the stock pair scorer on the same data (exact McNemar p = 0.016) and 32–37× faster for
   16 questions × 3 candidates on 8K–16K-token texts. The gap to Jev (82.7%) is not significant (p = 0.08;
   document-bootstrap 95% interval for tree − Jev: −2.4 to +0.1 points). Write-up: [tree_model.md](tree_model.md),
   audit: [reports/tree_review_2026-09-23/review.md](../reports/tree_review_2026-09-23/review.md). For scale: GPT-6
   Astra (reasoning low) scores 85.8% and 100% on the authored eval_* families (`reports/external/full/openai_gpt-6-astra`);
   the authored families are where Jev (94.7%) is furthest ahead of the tree (78.4%).
2. **The stock recipe saturates at 80–81% whatever you feed it.** Nested data subsets (25/50/100%) give
   77.0/78.9/80.3; 2 epochs 79.1/79.1/79.8; 8B 80.7 (= 4B, p = 0.52); Qwen3-4B-Instruct base 80.6 after LoRA
   (p = 0.68 vs reranker) although it is far better zero-shot (71.3 vs 62.8). Each doubling of the data buys
   about 1.5 points. [reports/curve/summary.md](../reports/curve/summary.md).
   **Adapter capacity: flat on the old test, real on eval2 (corrected 2026-09-24).** The tree scorer with LoRA r=64
   (4× the trainable parameters) scores 81.5% on the old test and r=16 on attention + MLP matrices (2.8×) 81.6%, vs 81.6%
   for r=16 (p = 0.94 / 1.0). On eval2 the same adapters score **87.2%** (77 / 36 questions vs r=16, p = 0.00014) and
   **86.3%** (62 / 38, p = 0.021) vs 85.1%. Validation had predicted it (80.2 → 81.8 / 81.4); the old test's public
   held-out families hid it. **Combined with the round-2b data (2026-09-24 03:10):** r=64 alone adds nothing (90.3 vs 90.6,
   p = 0.61); r=64 + MLP gives 91.3 (p = 0.17 vs r2b), 82.4 on the old test (p = 0.0065) and the best validation (87.0).
   The levers do not add up: +2.1 for r=64 on round-1 data becomes 0 on round-2b data; the MLP adapter keeps a small,
   consistent edge (+1 to +4 points on every trap tag, all three eval2 authors within noise of each other).
3. **A new task type costs thousands of examples for a few points.** +100/+300/+1,000/+3,000 BoolQ training
   questions: BoolQ test 84.3/83.3/84.3/86.7 (from 83.3; Jev 90.7); overall accuracy unchanged (p ≥ 0.09).
4. **Round-2 data (verified hard cases, 16,357 questions, 8K training length) did not raise the tree's test
   score**: 80.6 vs 81.6. The whole net loss is CLINC over-rejection: 34 questions flipped to `none` (`none`
   picked 95× vs 45 gold); authored eval cases improved 78.4 → 81.9. Details in the tree review, section
   "round two's regression". Keep `runs/tree_4b` as the reference. Data-side cause and the generation/judging
   pipeline (6 authors, 10,627 questions, 95.4% author = Astra, $59 total): [hardcases_round2.md](hardcases_round2.md).
   In the hard/very-hard tiers a `none` candidate is offered in 50% of multiclass questions and is correct 28% of the
   time when offered, vs 8% in round-1 synthetic data and never in the public sets; CLINC gold is 15%.
   **Round 2b** (`runs/tree_4b_r2b`) caps the none-answers at 10% and reaches **81.2%**: vs 81.6 p = 0.39, vs round 2
   p = 0.08, vs Jev p = 0.02.
   - CLINC is back to 92.0% (in-scope sent to `none`: 24, round 1: 16, round 2: 50).
   - Authored cases are the best of any of our runs: 83.0% (round 1: 78.4, Jev: 94.7).
   - Traps vs round 1: temporal 52 → 69, numeric 44 → 69, multi-positive 44 → 51, long state 76 → 84, exception 29 → 57.
   - New drop: TREC 88.7 → 84.7, mostly questions sent to `entities`.
   - Outside CLINC, rounds 1, 2 and 2b are within 0.1 point of each other (80.2–80.4%).
   - So the round-2 data only helps the slices this test barely contains: eval2 decides between `tree_4b` and
     `tree_4b_r2b`.
   - The CLINC fix came from a test diagnosis.
5. **Where the remaining gap to Jev is:** binary judgments (tree 87.1% vs Jev 93.5%, 63 answers), agent-output
   grading (61.5% vs 92.3% on 26 questions), BoolQ and SST-2. Multilabel exact match is already ahead of Jev.
6. **The custom cross-attention model (v1 spec) is not competitive:** 39.0% as specified, 58.2% with a
   similarity term and joint LoRA, although 38–43× faster than stock pairs at 16 × 3 on long texts. Causes:
   label memorization, unlearned binary head, features that already match unseen labels (MaxSim 75–77% vs
   trained heads 23–28%). Diagnostics in `reports/custom_diagnostics/`, write-up [custom_model.md](custom_model.md).
7. **Calibration:** temperatures fit near 1; the F1-maximizing thresholds in `calib/tree_4b.json` *lower* test
   accuracy (81.6 → 79.3 in `reports/tree_4b/test_calibrated`). Tree binary ECE 0.077 vs stock 0.056 vs Jev 0.045.
8. **Speed vs Jev, end to end** (2026-09-23, [reports/latency/summary.md](../reports/latency/summary.md)): Jev answers in a
   flat ~150 ms (p50, from California) at every size, 8 → 4,096 tokens and 1 or 16 questions. Our tree 4B on one A10G
   with vLLM:
   - matches or beats it up to ~128 tokens with 1 question (120 ms, including 71 ms of network);
   - is 5× slower at 4,096 tokens and 2–7× slower with 16 questions, because the A10G is compute-bound (6.5–10K
     tokens/s).
   - Fully busy, the A10G is 1.3–3× cheaper per request than Jev ($0.042 per million input tokens). An idle GPU is not.
9. **Listing every option in the question helps** (2026-09-24, `tree_4b_ova`, `scripts/options_in_question.py`).
   - Each leaf judges one candidate while seeing all the alternatives; the recipe is r2b's.
   - Old test: 82.6 vs 81.2 (p = 0.001), tied with Jev (82.7).
   - eval2: 91.6 vs 90.6 (p = 0.07).
   - Multilabel on the old test: 57.8 vs 51.7.
   - One run each: confirm with a second seed or in round 3.



## Completed latency/compact experiment (2026-09-24)

The direct branch-mask optimization, vLLM quality/cache checks, and compact-format continuation training are complete;
[results and decision](../reports/latency_optimization_2026-09-24/conclusions.md). Compact failed its predeclared cold-prefix
vLLM speed-improvement gate and introduced CLINC over-rejection, so it stays experimental. Measurements use R1;
they do not compare against round 2b or the new eval2 benchmark. Faster GPU launches were authorized in this Codex
session but failed due to AWS capacity/quota, so their latency benefit is still unmeasured. All code and artifacts
are now in the original `master` checkout; no new branches or worktrees should be created.

8. **jina-reranker-v3.5 (0.6B listwise) is not a shortcut to the 4B's quality** (2026-09-24, `docs/jina_model.md`): trained
   with the r2b recipe it scores 76.6 on the old test and 73.3 on eval2 vs 81.2 / 90.6 for the tree 4B r2b; multilabel
   exact match 40.1 vs 78.8. Same size class as the 0.6B Qwen reranker (73.5 old test), same result. Non-commercial license.

## Dead ends: do not redo

Measured on the old test only. eval2 revives any of them that it hasn't re-scored yet (see the eval2 section).
- **Distilling Qwen3.8-27B-FP8 zero-shot probabilities into the tree 4B**: teacher_weight 0.5 on target-task rows, gold on
  hf rows (`tree_4b_ova_kd`, 2026-09-24).
  - Old test 82.5 vs 82.6, eval2 91.0 vs 91.6 (p = 0.21): no gain, although a 50/50 ensemble of the two scores 94.5 on
    eval2.
  - Not yet tried: multiclass-only distillation, a lower weight, an r64 student.

| tried | result | evidence |
|---|---|---|
| Stock LoRA, 2 epochs instead of 1 | no gain (79.8 vs 80.3; best validation checkpoint inside epoch 1) | `reports/curve/vol100_e2` |
| Stock LoRA on 8B instead of 4B | 80.7 vs 80.3, p = 0.52; 1.7× slower | `reports/lora_8b`, `reports/scale_comparison.md` |
| Instruct base (Qwen3-4B-Instruct-2507) instead of the reranker, pairs or tree | 80.6 / 80.4 after LoRA, same as reranker | `reports/curve/instruct_lora`, `reports/tree_4b_instruct` |
| Custom model: frozen backbone, Stage A only | 39.0 | `reports/custom_frozen` |
| Custom model: joint LoRA without similarity term | 39.7, p = 0.32 vs frozen | `reports/custom_diagnostics/logs/` |
| Custom model: distillation from the stock 0.6B teacher (`data/distill.jsonl`) | no gain over direct training | `reports/custom_distill_frozen`, `reports/custom_distill_lora` |
| Explicit attention mask in the custom encoder | identical outputs, 1.7–2.2× slower on MPS, loses the flash kernel on CUDA | `reports/custom_diagnostics/shapes.py` |
| More of the same training mix | ~1.5 points per doubling; matching Jev this way would take several × the data | `reports/curve/summary.md` |
| ~~Tree scorer with more LoRA capacity (r=64; r=16 + MLP targets)~~ **not dead**: flat on the old test (81.5 / 81.6 vs 81.6) but +2.1 / +1.2 points on eval2 (p = 0.00014 / 0.021) | the old test cannot see capacity effects; keep it as the example of why eval2 decides | `reports/curve/tree_4b_r64`, `reports/curve/tree_4b_mlp`, `reports/curve/summary.md` |
| jina-reranker-v3.5 (0.6B) as a drop-in smaller backbone, tree-r2b recipe | 73.3 on eval2 vs 90.6 (tree 4B r2b); one pass per text but 17 points behind | `reports/jina_r2b`, `docs/jina_model.md` |
| Applying the fitted calibration file to the tree model | test accuracy drops 81.6 → 79.3 | `reports/tree_4b/test_calibrated` |

## Known issues and gotchas

- `benchmark.py` runs the stock scorer with prompt `task-v1` while quality reports use `answer-v1`
  (`src/personal_jev/benchmark.py:79` takes no prompt); latency ratios are still valid, exact same-format claims are not.
- **Fixed 2026-09-24:** `TreeModel.cached` now constructs only the branch mask, avoiding the full document T×T CPU mask. GPU score parity is recorded in `reports/latency_optimization_2026-09-24/parity_a10g.json`; measured latency improvement alone was small.
- Apple MPS caches one graph per tensor shape: the custom trainer buckets shapes (25% ladder) to keep memory flat
  (2.7 GB → 0.9 GB for +6.7% time); training on MPS without bucketing grows ~17 MB per new shape.
- Long stock evals on the 0.6B on MPS take hours; every 4B/8B number in this repo was produced on AWS
  (`scripts/setup_gpu_box.sh`, `scripts/run_curve.sh`, `scripts/run_tree_gpu.sh`). A g5.xlarge (A10G, $1.006/h)
  trains one 4B LoRA (10K questions) in ~40 min and runs the test split in ~4 min; the ten curve runs cost ~$23.
- `reports/external/failures.jsonl` lists **test** failures: use it to design data families, never as training data.
- The eval labels are LLM-written, family slices are small (17–32 authored questions per family), and this test set
  has been used for many development decisions; a fresh, task-balanced test set is overdue (see open ideas).

- Paid generation/judging gotchas (details in [hardcases_round2.md](hardcases_round2.md)): OpenRouter's batch API refuses this
  account's key, so half-price judging goes through OpenAI's Batch API (`scripts/judge_hardcases.py`, 24 h window, ~3 min
  for small batches); hidden reasoning tokens must be capped per model (Gemini `effort: low`, DeepSeek `enabled: false`,
  Grok cannot be disabled and costs 4× Gemini per state); Gemini and OpenAI are BYOK on this OpenRouter account, so
  budget checks must use per-call cost, not the account-usage delta (two generators running at once share it).
- Jev as an annotator agrees with authors on 93.0% (worst: temporal 82.7%, numeric, injection, multilabel); use it as a
  second opinion, not the gate. 432 round-2 questions are author = Astra but Jev wrong (`data/hardcases/review/JUDGE.md`).

## Open ideas: claim before starting (edit the status cell)

| idea | why | cost | status |
|---|---|---|---|
| T5Gemma 2 matched round-2b follow-up | prior shared-encoder/cross-KV run already exists: 75.37% old benchmark, 203 ms 2K×16×3 L40S; test stronger training mix | user authorized AWS; dedicated L40S target $3.00424/h | **corrected rerun in progress** Codex tree latency/compact: initial pilot accidentally decoder-only; full encoder+decoder targets now verified. `reports/t5_round2b_2026-09-24/` |
| Architecture recommendation after latency/eval2: shared pretrained encoder-decoder versus smaller tree | choose the next experiment using current evidence | no new GPU/API spend | **review complete 2026-09-24**: [architecture memo](../reports/architecture_next_2026-09-24.md); proposed T5Gemma 2 pretrained shared reader pilot, smaller-tree control, GLiClass short-input screening. No new training/results. |
| Integrate the completed latency/compact experiment into original `master` | user requires all work in the original branch; preserve concurrent changes and model artifacts | local only | **done 2026-09-24**: code, reports and trained artifacts in original `master`; extra branch/worktree removed; 16 focused integration tests pass. `reports/latency_optimization_2026-09-24/integration.json` |
| Tree + higher LoRA capacity: r=64, or r=16 + MLP targets (`configs/curve/tree_4b_r64.json`, `tree_4b_mlp.json`; `scripts/run_curve.sh tree_4b_r64 tree_4b_mlp`) | 4B = 8B and data curves flat suggest the adapter, not the model, is the ceiling | ~1 h A10G each (~$1) | **done 2026-09-23 22:00, fork 2**: old test 81.5 / 81.6 vs 81.6 (p ≈ 1); **eval2 87.2 / 86.3 vs 85.1 (p = 0.00014 / 0.021)**. Capacity helps on the target task. `reports/curve/tree_4b_r64`, `tree_4b_mlp` |
| **Combine the two levers**: round-2b data (`data/hardcases_nb.jsonl`, r2b recipe) + LoRA r=64, and r=64 + MLP targets; score on validation, old test and eval2 | +5.5 (data) and +2.1 (capacity) on eval2 were measured separately, both at the other setting's default | ~2 h A10G (~$3) each | **done 2026-09-24 03:10, fork 2**: r2b + r=64 → eval2 **90.3** (vs 90.6, p = 0.61); r2b + r=64 + MLP → eval2 **91.3** (59 / 44, p = 0.17), old test 82.4 (p = 0.0065 vs r2b), validation 87.0. Gains are uniform across authors, types and traps but small: once the data is good, capacity adds ≤ 1 point. `reports/curve/tree_4b_r2b_r64*`, `reports/curve/summary.md` |
| Tree full fine-tune (no adapter) | same question, upper bound | needs code (train_tree always wraps PEFT) + ≥48 GB GPU | unclaimed; worth it again since r=64 gave +2.1 on eval2 |
| Rejection (`none`) as its own decision: permutation-invariant rule over candidate scores, or the full candidate bank in the question prefix; balanced in/out-of-scope training pairs | round-2 regression is 100% CLINC over-rejection | data + small code | full candidate bank in the question: **done, wins** (fork, 2026-09-24): old test 82.6 vs r2b 81.2 (p = 0.001), eval2 91.6 vs 90.6 (p = 0.07), `tree_4b_ova`; see JOURNAL 02:45. The other parts are unclaimed |
| Binary-judgment data with verified answers (numeric, temporal, agent-output grading) | 63 of the answers behind Jev are binary; grading is 61.5 vs 92.3 | generation + blind judge | round-2 hard cases exist (`data/hardcases.jsonl`); grading family still excluded from training on purpose |
| Tree execution: direct branch-mask construction, structured attention kernel | 1 GB masks | code only | **direct branch mask done 2026-09-24** (Codex tree latency/compact); structured-kernel work remains open. `--merge` (15–35% faster) and a vLLM path (`vllm_tree.py`, 1.3–2× faster on an A10G) are done: JOURNAL 2026-09-23 21:10 |
| Latency on a fast GPU: vLLM tree on an H100 (bf16 and FP8), same sweep (`scripts/latency_sweep.py`) | Jev's flat ~150 ms at 4K tokens × 16 questions needs ≥ 10× an A10G's compute; tells whether our model can match it | ≈ $5 (p5.4xlarge $6.88/h) | proposed to the user 2026-09-23, awaiting OK |
| vLLM path accuracy check: `pjev eval` equivalent through `VllmTreeScorer` on test | merged bf16 + vLLM kernels move scores ~0.06 logit; confirm 81.6% holds | ≈ 15 min GPU | **done 2026-09-24** (Codex tree latency/compact): R1 vLLM quality and compact vLLM quality measured on the development benchmark; raw predictions and backend comparisons in `reports/latency_optimization_2026-09-24/`. Eval2 remains open for these backends. |
| Calibration policy: temperature separate from thresholds; thresholds for accuracy, validated on a split not used for fitting | current file costs 2.3 points | code only | unclaimed |
| jina 0.6B follow-ups: 2 epochs (`configs/jina_r2b_e2.json`), r=64 + MLP LoRA (`configs/jina_r2b_r64.json`), pairwise layout; runner `scripts/run_jina_followups.sh` | tests whether the 0.6B is adapter- or data-limited; ~$1 each | ~1 h A10G each | unclaimed |
| Smaller tree student (0.6B / 1.7B) distilled from tree 4B | speed; the 0.6B stock reaches only 73.5 | 1 GPU-day | unclaimed |
| Fresh frozen target-task test set (`data/eval2.jsonl`, test only): ~1,500 questions balanced by trap and by the 8 → 8K length ladder, written by models not used for training data (e.g. claude-opus-5.5 + gemini-3.1-pro), two blind judges (Astra + one more), keep unanimous only, human spot-checks; score Jev and Astra on it too. Reuse `scripts/gen_hardcases.py` (new prefix) + `judge_hardcases.py` | current test reused for many decisions and 95% public sets: trap gains (numeric +25, exception +29 in round 2) are invisible in the aggregate | ≈ $40 API | **done 2026-09-24** (Synthetic data generation strategy): `data/eval2.jsonl` 1,991 q / 647 states, authors Opus 5.5 + Kimi K3 + GLM 5.3, judges Astra + Gemini 3.1 Pro unanimous (96.2% kept), Jev 97.2% on it, $32.72; details `data/eval2/REVIEW.md`, `docs/JOURNAL.md` 2026-09-24. Scoring our models on it: unclaimed |
| Stock 4B round 2 (`scripts/run_4b_r2.sh`) | control for the tree round-2 number | ~1 h A10G | stopped unfinished at 20:15 on 2026-09-23 to free the GPU for tree r2b (Jev classifier with Qwen reranker). No report: the control is still open |
| Score Laya (`pip install laya`, Apache 2.0; ModernBERT/mmBERT encoder + listwise [MASK] head, 3 routed checkpoints) zero-shot on eval2 and the old test, `max_len=8192`, via its Jev-shaped API | only open competitor with the same interface; its claims vs Jev are third-party and not comparable (JOURNAL 2026-09-24 Laya review). Needs a small adapter from our schema (multilabel = one noul per candidate, as for Jev) | Mac only, ≈ 1 h, $0 | unclaimed |
| Score our best tree on the public JevBench items (reported by kev, decider, others) and score 2–3 open models (Laya, open-jev-deberta, kev-4b) on eval2 | the only shared yardstick across the open Jev-like models; their own benchmarks are not comparable (JOURNAL 2026-09-24 HF survey) | Mac, $0 (model downloads) | unclaimed |
| **Qwen3.5-4B shared-document model**: port `run_challenger.py` + forked native cache from the Codex worktree; train with the `tree_4b_instruct_r2x64` recipe (round-2 uncapped, r64, 1 epoch) so it is a clean control; score old test + eval2; also score Eikos-4B and the existing Qwen3.5-2B adapter zero-shot on eval2 | Qwen3.5-2B with round-1 data already reached 79.9 on the old test; linear attention is 2× faster at 8K tokens; Eikos-4B shows the base works for typed decisions (JOURNAL 2026-09-24 Qwen3.5 entry) | g5.xlarge ≈ 4–5 h ≈ $5, cap $7 | **claimed, awaiting the user's OK on the spend** (session "SelfJev state of play") |
| GLiClass-Instruct / T5Gemma / hybrid backbones | alternatives from [reports/strategy_2026-09-23/strategy.md](../reports/strategy_2026-09-23/strategy.md) | research | deferred by the tree review |
| Round-2 mix fix + retrain tree 4B: cap none-correct at ≈ 10% of multiclass, add none-offered-but-wrong intent-like states, subsample hard cases to ≈ 30% of training questions (currently ≈ 50%); compare on both test sets | round-2 data lifts authored eval 78.4 → 81.9 and every trap, loses only on CLINC `none` | ≈ $3 GPU + $2 generation | **first step done** (Jev classifier with Qwen reranker): `tree_4b_r2b` = cap only, via `scripts/rebalance_nota.py` (160 none-answer train questions dropped). 81.2%, CLINC back to 92.0, authored 83.0 (conclusion 4). Still open: none-offered-but-wrong intent-like states, subsampling hard cases to ≈ 30% |
| Label-free binary bias fix, e.g. contextual calibration (subtract each question's score on an empty text), chosen on validation | SST-2 (held out) ranks well (AUROC 0.973) but predicts positive 34.7% vs 50% true: 84.0% vs 91.7% at the best threshold. SST-2 + BoolQ explain ≈ 60 of the 63 binary answers behind Jev (JOURNAL 2026-09-23 20:40; a test diagnosis, so confirm on a fresh holdout) | code + ≈ 1 h GPU | proposed, unclaimed |
| Multilabel with 3–5 positives (multi_positive exact match 44.4%, unchanged by round 2; only 21% of new multilabel questions have 3+ positives) | largest untouched slice; multilabel is where we already beat Jev | ≈ $3 generation (Luna/Gemini) + judge | unclaimed |
| Prompt-template robustness: random `formatting.PROMPTS` mapping per training example; average scores over 2–4 mappings at eval (TTA) | learn the task, not the template; cheap +1–2 points expected | code + ≈ $2 GPU | unclaimed |
| Soft labels: Astra's per-candidate probabilities for all 10.6K round-2 questions are in `data/hardcases/review/batch_results/` | distil calibration, not only argmax | code only | **not useful as is** (fork, 2026-09-23): 98.8% of questions have every probability ≤ 0.05 or ≥ 0.95 (86.7% exactly 0/1), so they equal the hard labels. Real soft targets need a teacher whose logits we can read. `train_tree.py` now has `teacher_weight` / `teacher_file` (added by another session) |
| More generation is cheap: Luna ≈ $0.002 per 5 states, Gemini ≈ $0.014 per state, judge ≈ $3.40 per 1K questions; scripts resume | if the eval2 curve is still rising | per run | — |

## Where things are

| what | where |
|---|---|
| overview and headline tables | [README.md](../README.md) |
| tree scorer: design, results, speed, reproduce | [docs/tree_model.md](tree_model.md), `src/personal_jev/tree.py`, `train_tree.py`, `configs/tree_4b*.json`, `scripts/run_tree_gpu.sh`, `run_tree_r2.sh` |
| custom cross-attention model | [docs/custom_model.md](custom_model.md), `src/personal_jev/custom.py`, `train_custom.py`, `configs/custom_*.json`, `reports/custom_diagnostics/` |
| learning curves (data volume, epochs, per-task, base model) | [reports/curve/summary.md](../reports/curve/summary.md), `configs/curve/`, `scripts/run_curve.sh`, `scripts/summarize_curve.py` |
| reviews and strategy | `reports/review_2026-09-23.md`, `reports/deep_review_2026-09-23/review.md`, `reports/strategy_2026-09-23/strategy.md`, `reports/tree_review_2026-09-23/review.md` |
| Jev comparison (cached API answers) | `reports/external/`, `scripts/compare_external.py`, failures in `reports/external/failures.md` |
| latency | `reports/bench/`, `reports/latency/`, `scripts/latency_sweep.py` |
| data: sources, splits, labeling policy | README "Data"; `data/eval/BRIEF.md`, `data/synthetic/BRIEF.md`, `data/hardcases/BRIEF.md`; builders `scripts/build_*.py` |
| round-2 hard cases: generation, blind judging, agreement tables, retrain diagnosis | [docs/hardcases_round2.md](hardcases_round2.md), `scripts/gen_hardcases.py`, `scripts/judge_hardcases.py`, `data/hardcases/review/{JUDGE,REVIEW}.md`, `reports/hardcases/` |
| trained weights and training metadata | `runs/<name>/adapter` or `checkpoint`, `runs/<name>/train_meta.json` (config, data hashes, log, reload check) |
| comics explaining the pipeline | `docs/comics/`, `scripts/make_comics.py` |
