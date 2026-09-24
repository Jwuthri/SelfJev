# Experiment ledger

The cross-session state of the project. Every session (Claude Code, Codex, human) reads this before starting work and
updates it when something finishes; the dated log is in [JOURNAL.md](JOURNAL.md). The formatted version of these results
is the docs site: [key findings](findings.md) and [leaderboard](leaderboard.md).

- **eval2** (`data/eval2.jsonl`, 1,991 questions) is the primary benchmark since 2026-09-24. Never train, select prompts
  or fit calibration on it.
- **Dev benchmark** (the "old test"): 3,471 questions = `hf.jsonl` test + `eval.jsonl` test, identical ids for every
  model. It has been reused for many decisions, so report it as a development benchmark. Never train or tune on it.

## Results (generated)

The table is generated from `reports/*/test/report.json` and `reports/*/eval2/report.json` by
`uv run python scripts/ledger.py`: never hand-edit it. Sorted by eval2, then by the dev benchmark. The report links are
the dev-benchmark `test/report.md` files; weights are in `runs/` (not in git).

<!-- --8<-- [start:ledger] -->
<!-- ledger:start -->
| run | base | architecture | trained on | **eval2 acc %** (target task, 1,991 q) | dev benchmark acc % (old test, 3,471 q) | binary acc % | binary AUROC | multiclass acc % | multilabel EM % | authored eval_* acc % (n=171) | report | weights |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| external | ~typesafe/jev-latest | external API | — | 97.2 | 82.7 | 93.5 | 0.981 | 84.6 | 40.1 | 94.7 | [report](../reports/external/full/typesafe_jev-latest/report.md) | — |
| tree_4b_instruct_r2x64 | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | 18,681 q / 218 steps | 92.7 | 82.7 | 90.9 | 0.965 | 83.7 | 52.9 | 81.9 | [report](../reports/tree_4b_instruct_r2x64/test/report.md) | runs/tree_4b_instruct_r2x64/adapter |
| tree_4b_ova | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,372 q / 241 steps | 91.6 | 82.6 | 89.2 | 0.962 | 83.6 | 57.8 | 84.2 | [report](../reports/tree_4b_ova/test/report.md) | runs/tree_4b_ova/adapter |
| curve/tree_4b_r2b_r64_mlp | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,375 q / 208 steps | 91.3 | 82.4 | 89.0 | 0.962 | 83.5 | 57.0 | 84.2 | [report](../reports/curve/tree_4b_r2b_r64_mlp/test/report.md) | runs/curve/tree_4b_r2b_r64_mlp/adapter |
| tree_4b_ova_kd | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,372 q / 241 steps | 91.0 | 82.5 | 88.1 | 0.959 | 83.8 | 58.4 | 84.8 | [report](../reports/tree_4b_ova_kd/test/report.md) | runs/tree_4b_ova_kd/adapter |
| tree_4b_instruct_r3_step300 | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | — | 90.8 | 81.5 | 89.4 | 0.954 | 82.5 | 52.6 | 81.3 | [report](../reports/tree_4b_instruct_r3_step300/test/report.md) | — |
| tree_4b_r2b | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,375 q / 225 steps | 90.6 | 81.2 | 88.1 | 0.955 | 82.8 | 51.7 | 83.0 | [report](../reports/tree_4b_r2b/test/report.md) | runs/tree_4b_r2b/adapter |
| tree_4b_r2 | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,357 q / 224 steps | 90.4 | 80.6 | 87.6 | 0.956 | 82.2 | 50.9 | 81.9 | [report](../reports/tree_4b_r2/test/report.md) | runs/tree_4b_r2/adapter |
| curve/tree_4b_r2b_r64 | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,375 q / 208 steps | 90.3 | 81.2 | 87.8 | 0.962 | 82.5 | 54.4 | 82.5 | [report](../reports/curve/tree_4b_r2b_r64/test/report.md) | runs/curve/tree_4b_r2b_r64/adapter |
| tree_4b_instruct | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | 10,112 q / 78 steps | 88.1 | 80.4 | 87.8 | 0.958 | 82.3 | 46.8 | 79.5 | [report](../reports/tree_4b_instruct/test/report.md) | runs/tree_4b_instruct/adapter |
| curve/tree_4b_r64 | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 10,080 q / 84 steps | 87.2 | 81.5 | 88.5 | 0.956 | 83.0 | 52.3 | 77.8 | [report](../reports/curve/tree_4b_r64/test/report.md) | runs/curve/tree_4b_r64/adapter |
| lora_4b | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,112 q / 216 steps | 86.5 | 80.3 | 87.5 | 0.945 | 82.3 | 47.7 | 70.8 | [report](../reports/lora_4b/test/report.md) | runs/lora_4b/adapter |
| curve/tree_4b_mlp | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 10,080 q / 84 steps | 86.3 | 81.6 | 87.9 | 0.955 | 83.4 | 51.7 | 78.9 | [report](../reports/curve/tree_4b_mlp/test/report.md) | runs/curve/tree_4b_mlp/adapter |
| tree_4b | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 10,112 q / 84 steps | 85.1 | 81.6 | 87.1 | 0.953 | 83.9 | 51.7 | 78.4 | [report](../reports/tree_4b/test/report.md) | runs/tree_4b/adapter |
| t5_round2b_2026-09-24/decoder_only_audit/t5_r2b | google/t5gemma-2-1b-1b | pretrained T5Gemma encoder/decoder; shared document cross-KV views | 16,375 q / 228 steps | 76.8 | 73.8 | 82.7 | 0.893 | 75.1 | 40.4 | 62.6 | [report](../reports/t5_round2b_2026-09-24/decoder_only_audit/t5_r2b/test/report.md) | runs/t5gemma2_r2b/adapter |
| jina_r2b | jinaai/jina-reranker-v3.5 | jina listwise (jina-v1) | 16,301 q / 345 steps | 73.3 | 76.6 | 81.4 | 0.888 | 79.4 | 45.1 | 60.2 | [report](../reports/jina_r2b/test/report.md) | runs/jina_r2b/adapter |
| t5_round2b_2026-09-24/t5_r1 | google/t5gemma-2-1b-1b | pretrained T5Gemma encoder/decoder; shared document cross-KV views | 10,080 q / 823 steps | 73.0 | 75.4 | 83.0 | 0.887 | 76.6 | 45.6 | 62.0 | [report](../reports/t5_round2b_2026-09-24/t5_r1/test/report.md) | runs/t5gemma2_r1_reference/adapter |
| lora_pilot | Qwen3-Reranker-0.6B | stock pairs (task-v1) | 10,112 q / 183 steps | 68.8 | 73.5 | 77.8 | 0.863 | 78.3 | 31.1 | 55.0 | [report](../reports/lora_pilot/test/report.md) | runs/lora_pilot/adapter |
| external | openai/gpt-6-astra | external API | — | — | 85.8 | 93.8 | 0.971 | 87.0 | 55.8 | 100.0 | [report](../reports/external/full/openai_gpt-6-astra/report.md) | — |
| curve/boolq_300 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,412 q / 218 steps | — | 80.9 | 88.0 | 0.940 | 82.5 | 50.9 | 71.9 | [report](../reports/curve/boolq_300/test/report.md) | runs/curve/boolq_300/adapter |
| curve/boolq_1000 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 11,112 q / 224 steps | — | 80.9 | 88.8 | 0.954 | 82.5 | 48.8 | 73.7 | [report](../reports/curve/boolq_1000/test/report.md) | runs/curve/boolq_1000/adapter |
| curve/boolq_3000 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 13,112 q / 240 steps | — | 80.9 | 88.9 | 0.954 | 82.5 | 47.7 | 73.1 | [report](../reports/curve/boolq_3000/test/report.md) | runs/curve/boolq_3000/adapter |
| lora_8b | Qwen3-Reranker-8B | stock pairs (task-v1) | 10,112 q / 185 steps | — | 80.7 | 87.3 | 0.945 | 82.9 | 48.0 | 74.9 | [report](../reports/lora_8b/test/report.md) | runs/lora_8b/adapter |
| curve/instruct_lora | Qwen3-4B-Instruct-2507 | stock pairs (answer-v1) | 10,112 q / 216 steps | — | 80.6 | 87.4 | 0.944 | 82.6 | 48.3 | 75.4 | [report](../reports/curve/instruct_lora/test/report.md) | runs/curve/instruct_lora/adapter |
| curve/boolq_100 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,212 q / 217 steps | — | 80.0 | 86.9 | 0.945 | 82.0 | 48.3 | 70.8 | [report](../reports/curve/boolq_100/test/report.md) | runs/curve/boolq_100/adapter |
| curve/vol100_e2 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,112 q / 431 steps | — | 79.8 | 87.0 | 0.951 | 81.9 | 46.2 | 69.6 | [report](../reports/curve/vol100_e2/test/report.md) | runs/curve/vol100_e2/adapter |
| curve/vol50_e2 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 5,056 q / 214 steps | — | 79.1 | 84.8 | 0.940 | 81.7 | 46.8 | 72.5 | [report](../reports/curve/vol50_e2/test/report.md) | runs/curve/vol50_e2/adapter |
| curve/vol25_e2 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 2,528 q / 107 steps | — | 79.1 | 85.7 | 0.935 | 81.4 | 45.6 | 73.7 | [report](../reports/curve/vol25_e2/test/report.md) | runs/curve/vol25_e2/adapter |
| curve/vol50_e1 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 5,056 q / 107 steps | — | 78.9 | 84.5 | 0.934 | 81.9 | 44.5 | 70.2 | [report](../reports/curve/vol50_e1/test/report.md) | runs/curve/vol50_e1/adapter |
| curve/vol25_e1 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 2,528 q / 53 steps | — | 77.0 | 83.8 | 0.930 | 80.8 | 33.4 | 71.9 | [report](../reports/curve/vol25_e1/test/report.md) | runs/curve/vol25_e1/adapter |
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
<!-- --8<-- [end:ledger] -->

## eval2: the primary benchmark

Full slices (type, tier, author, length, trap) and paired tests: [reports/eval2/summary.md](../reports/eval2/summary.md),
generated by `python3 scripts/eval2_summary.py`. Score new models with `scripts/run_eval2.sh`, then re-run the summary.

| model | eval2 acc % | binary | multiclass | multilabel EM | dev benchmark |
|---|---|---|---|---|---|
| Jev | **97.2** | 97.8 | 98.1 | 94.2 | 82.7 |
| **tree_4b_instruct_r2x64** (Instruct base, round-2 data uncapped, r64) | **92.7** | 94.6 | 95.4 | 83.5 | 82.7 |
| tree_4b_ova (reranker, round-2b data, all options listed in the question) | 91.6 | 93.8 | 94.9 | 80.4 | 82.6 |
| curve/tree_4b_r2b_r64_mlp (reranker, round-2b data, r64 + MLP) | 91.3 | 93.7 | 94.3 | 80.4 | 82.4 |
| tree_4b_r2b (reranker, round-2 data, `none` capped) | 90.6 | 92.9 | 94.1 | 78.8 | 81.2 |
| tree_4b_r2 (reranker, round-2 data) | 90.4 | 92.8 | 95.8 | 75.4 | 80.6 |
| curve/tree_4b_r2b_r64 (reranker, round-2b data, r64) | 90.3 | 92.9 | 94.9 | 75.9 | 81.2 |
| tree_4b_instruct (Instruct base, round-1 data) | 88.1 | 91.4 | 92.7 | 72.3 | 80.4 |
| curve/tree_4b_r64 (reranker, r64, round-1 data) | 87.2 | 90.5 | 92.7 | 69.9 | 81.5 |
| lora_4b (stock pairs, round-1 data) | 86.5 | 89.7 | 91.6 | 70.4 | 80.3 |
| curve/tree_4b_mlp (reranker, r16 + MLP, round-1 data) | 86.3 | 90.0 | 91.9 | 68.1 | 81.6 |
| tree_4b (reranker, r16, round-1 data) | 85.1 | 89.4 | 91.6 | 63.9 | 81.6 |
| lora_pilot (0.6B stock, round-1 data) | 68.8 | 75.7 | 75.7 | 39.8 | 73.5 |

What each lever is worth on eval2 against `tree_4b` at 85.1 (paired exact McNemar, only-row / only-ref):

| lever | gain | evidence |
|---|---|---|
| round-2 verified hard cases | **+5.5** (142 / 34, p = 7e-17) | tree_4b_r2b |
| Instruct base (Qwen3-4B-Instruct-2507) instead of the reranker | **+3.0** (129 / 69, p = 2e-5) | tree_4b_instruct |
| LoRA rank 64 instead of 16 | **+2.1** (77 / 36, p = 1e-4) | curve/tree_4b_r64 |
| MLP targets added | +1.2 (62 / 38, p = 0.02) | curve/tree_4b_mlp |
| stock pairs instead of tree | +1.4 (129 / 101, p = 0.08): the tree's speed costs no significant quality | lora_4b |
| 0.6B instead of 4B (stock) | **−17.7** vs stock 4B | lora_pilot |

The levers overlap. Round-2b data + r64 → 90.3 (no gain over 90.6, p = 0.61); + MLP → 91.3 (p = 0.17). The Instruct
base stacks with the data: `tree_4b_instruct_r2x64` 92.7 vs r2b 90.6 (90 / 47, p = 0.0003).

## Current conclusions (2026-09-24)

Each has a formatted box with its evidence in [findings.md](findings.md).

1. **Best model: `tree_4b_instruct_r2x64`**: Qwen3-4B-Instruct-2507, shared-prefix tree, LoRA r64, round-2 data
   uncapped. eval2 92.7 (Jev 97.2, 25 / 115, p = 5e-15); dev benchmark 82.7, tied with Jev (213 / 214). It is the
   control for round 3.
2. **The dev benchmark cannot rank models.** Public-label noise caps every model at 80–86%. It called data, base model
   and capacity ties; eval2 shows +5.5, +3.0 and +2.1. Re-check any "no gain" measured on it before treating it as dead.
3. **Verified target-task data is the biggest lever** (+5.5 on eval2). Mix details matter: round 2's `none`-heavy
   multiclass data cost CLINC 94.7 → 83.3; capping `none`-correct at 10% (r2b) restored 92.0 (a test diagnosis).
4. **More of the same data buys ~1.5 points per doubling; a second epoch never helps; a new task type needs thousands
   of examples** (BoolQ +3,000 → BoolQ 86.7, overall unchanged). [reports/curve/summary.md](../reports/curve/summary.md).
5. **Model choice:** 4B ≈ 8B (80.3 vs 80.7, p = 0.52); sub-1B is 17 points behind on eval2 (0.6B Qwen 68.8, jina 73.3);
   the Instruct base beats the reranker once the data is good.
6. **Capacity overlaps with data:** r64 +2.1 on round-1 data, +0 on round-2b data; r64 + MLP +0.7 (n.s.).
7. **Listing every option in the question helps** (`tree_4b_ova`): dev benchmark 82.6 vs 81.2 (p = 0.001), eval2 91.6
   vs 90.6 (p = 0.07). One run each.
8. **The 27B teacher is complementary but does not distil** at weight 0.5: teacher zero-shot 91.4 on eval2, 50/50
   ensemble with `tree_4b_ova` 94.5, distilled student 91.0 vs 91.6 (p = 0.21).
9. **The tree scorer is the architecture:** same quality as stock pairs, 32–37× faster at 16 × 3 on 8K–16K tokens.
   The custom cross-attention model (39.0 / 58.2), T5Gemma 2 (73.0 eval2), jina 0.6B (73.3) and Qwen3.5-2B (79.9 dev
   benchmark) all fall short.
10. **Calibration:** temperatures fit near 1 after LoRA; the F1-maximizing thresholds in `calib/tree_4b.json` lower
    accuracy (81.6 → 79.3): serve without them. SST-2 (held out) is a bias: AUROC 0.973 but 34.7% predicted positive.
11. **Speed vs Jev** ([reports/latency/summary.md](../reports/latency/summary.md)): Jev is flat at ~150 ms p50 from 8 to
    4,096 tokens and 1 or 16 questions. Tree 4B + vLLM on one A10G matches it up to ~128 tokens with 1 question and is
    5× slower at 4,096 tokens, 2–7× slower with 16 questions. Fully busy, the A10G is 1.3–3× cheaper per request.
12. **Serving:** vLLM + merged weights is the general option (967 → 700 ms at 2K × 16 × 3, dev benchmark 81.53 vs
    81.50). The compact tree format failed its 15% speed gate (7.4%) and adds CLINC over-rejection: experimental only
    ([conclusions](../reports/latency_optimization_2026-09-24/conclusions.md)).
13. **Remaining gap to Jev on eval2** (best model): multilabel EM 83.5 vs 94.2, sarcasm 86.6 vs 97.3, numeric 82.1 vs
    92.0, multi-positive 86.3 vs 96.0, injection 88.7 vs 97.4. Text length is not a weakness.

## Dead ends: do not redo

Measured where noted. eval2 revives anything measured only on the dev benchmark until eval2 re-scores it.

| tried | result | evidence |
|---|---|---|
| Stock LoRA, 2 epochs instead of 1 | dev benchmark 79.8 vs 80.3; best validation checkpoint inside epoch 1 | `reports/curve/vol100_e2` |
| Stock LoRA on 8B instead of 4B | dev benchmark 80.7 vs 80.3, p = 0.52; 1.7× slower | `reports/lora_8b`, `reports/scale_comparison.md` |
| More of the same training mix | ~1.5 points per doubling; matching Jev this way would take several × the data | `reports/curve/summary.md` |
| Custom model: frozen backbone, Stage A only | 39.0 | `reports/custom_frozen` |
| Custom model: joint LoRA without the similarity term | 39.7, p = 0.32 vs frozen | `reports/custom_diagnostics/logs/` |
| Custom model: distillation from the stock 0.6B teacher (`data/distill.jsonl`) | no gain over direct training | `reports/custom_distill_frozen`, `reports/custom_distill_lora` |
| Explicit attention mask in the custom encoder | identical outputs, 1.7–2.2× slower on MPS, loses the flash kernel on CUDA | `reports/custom_diagnostics/shapes.py` |
| jina-reranker-v3.5 (0.6B) as a smaller backbone, tree-r2b recipe | eval2 73.3 vs 90.6 (tree 4B r2b); non-commercial license | `reports/jina_r2b`, [jina_model.md](jina_model.md) |
| Applying the fitted calibration file to the tree model | dev benchmark accuracy 81.6 → 79.3 | `reports/tree_4b/test_calibrated` |
| Distilling Qwen3.8-27B-FP8 zero-shot probabilities into the tree 4B (weight 0.5 on target-task rows) | eval2 91.0 vs 91.6 (p = 0.21). Untried: multiclass-only, lower weight, r64 student | `reports/tree_4b_ova_kd` |
| Astra's verbalized probabilities as soft labels | 98.8% of questions have every probability ≤ 0.05 or ≥ 0.95: they equal the hard labels | `data/hardcases/review/batch_results/` |
| Compact tree format (shorter branches) | 7.4% faster on vLLM (gate: 15%), CLINC 94.7 → 91.7 | `reports/latency_optimization_2026-09-24/` |

Revived by eval2 (dead on the dev benchmark only): the Instruct base (+3.0), LoRA r64 (+2.1) and MLP targets (+1.2).

## Known issues and gotchas

- `benchmark.py` runs the stock scorer with prompt `task-v1` while quality reports use `answer-v1`
  (`src/personal_jev/benchmark.py` takes no prompt): latency ratios are valid, exact same-format claims are not.
- **Fixed 2026-09-24:** `TreeModel.cached` builds only the branch mask instead of the full T×T document mask; GPU score
  parity in `reports/latency_optimization_2026-09-24/parity_a10g.json`. The latency gain alone was small.
- **T5Gemma PEFT targets:** the native encoder path is `model.encoder.text_model.layers`. A filter on
  `model.encoder.layers` silently trains the decoder only. Check adapter tensor counts per stack.
- **eval2 ids:** join on the expanded row ids (`<source_id>-q<i>`). The first export renumbered ids after drops;
  `data/eval2/review/id_map_sourceformat_to_real.json` remaps reports scored on it.
- Apple MPS caches one graph per tensor shape: the custom trainer buckets shapes (25% ladder) to keep memory flat
  (2.7 GB → 0.9 GB for +6.7% time).
- No evals or training on the laptop (see [AGENTS.md](../AGENTS.md)). A g5.xlarge (A10G, $1.006/h) trains one 4B LoRA
  on 10K questions in ~40 min and runs the dev benchmark in ~4 min (`scripts/setup_gpu_box.sh`, `scripts/run_curve.sh`,
  `scripts/run_tree_gpu.sh`). AWS GPU capacity is often short: g6e, L40S and H100 launches failed repeatedly.
- `reports/external/failures.jsonl` lists **test** failures: use it to design data families, never as training data.
- Paid generation and judging ([hardcases_round2.md](hardcases_round2.md)):
  - OpenRouter's batch API refuses this account's key, so half-price judging goes through OpenAI's Batch API
    (`scripts/judge_hardcases.py`; it saves progress after every chunk, so reruns submit only what is left).
  - Cap hidden reasoning per model: Gemini `effort: low`, DeepSeek `enabled: false`; Grok's cannot be disabled and
    costs 4× Gemini per state.
  - Gemini and OpenAI are BYOK on this OpenRouter account: budget checks must use per-call cost, not the account-usage
    delta.
  - One judge process per review dir and one generator per prefix; check the `none`-correct rate after each build.
- Jev as an annotator agrees with authors on 93.0% (worst: temporal, numeric, injection, multilabel): a second opinion,
  not the gate. 432 round-2 questions are author = Astra but Jev wrong (`data/hardcases/review/JUDGE.md`).

## Open ideas: claim before starting (edit the status cell)

| idea | why | cost | status |
|---|---|---|---|
| **Round 3, full run**: `tree_4b_instruct_r2x64` recipe + `data/hardcases_r3.jsonl` (38.6K verified questions) | the first run was stopped at step ≈ 500 of 915; its step-300 checkpoint (90.8 eval2) is not a verdict | ~10 h A10G ≈ $10 | open; owner was "Jev classifier with Qwen reranker" |
| T5Gemma 2 corrected full encoder + decoder adaptation on round-2b data | the pilot trained the decoder only (76.8 eval2) | L40S $3.00424/h | **in progress** (Codex tree latency/compact), `reports/t5_round2b_2026-09-24/`; no corrected result yet |
| **Qwen3.5-4B shared-document model**: port `run_challenger.py` + forked native cache from the Codex worktree; `tree_4b_instruct_r2x64` recipe; score dev benchmark + eval2; also Eikos-4B and the Qwen3.5-2B adapter zero-shot on eval2 | Qwen3.5-2B reached 79.9 on round-1 data; linear attention is 2× faster at 8K tokens | g5.xlarge ≈ 4–5 h ≈ $5, cap $7 | **claimed, awaiting the user's OK on the spend** (session "SelfJev state of play") |
| Distillation variants: 27B teacher on multiclass only, lower weight, r64 student; or a 50/50 ensemble served as is | 50/50 ensemble scores 94.5 on eval2; weight 0.5 on all rows gave nothing | ≈ $3 GPU each | unclaimed |
| Multilabel with 3–5 positives | multilabel EM is the largest gap to Jev (83.5 vs 94.2); round 3 has 54% of multilabel questions with 3+ positives | ≈ $3 generation + judge | partly covered by round 3 |
| Binary-judgment data with verified answers (numeric, temporal, agent-output grading) | numeric 82.1 vs 92.0, temporal 82.8 vs 89.2 on eval2; grading family still excluded from training on purpose | generation + blind judge | unclaimed |
| Rejection (`none`) as its own decision: permutation-invariant rule over candidate scores; balanced in/out-of-scope training pairs | the round-2 regression was all CLINC over-rejection; the "all options in the question" part is done (`tree_4b_ova`) | data + small code | unclaimed |
| Round-2 mix, remaining parts: `none`-offered-but-wrong intent-like states; subsample hard cases to ≈ 30% of training | the `none` cap (r2b) is done | ≈ $3 GPU + $2 generation | unclaimed |
| Label-free binary bias fix, e.g. contextual calibration (subtract each question's score on an empty text), chosen on validation | SST-2 + BoolQ explain ≈ 60 of the 63 binary answers behind Jev on the dev benchmark (a test diagnosis: confirm on a fresh holdout) | code + ≈ 1 h GPU | unclaimed |
| Calibration policy: temperature separate from thresholds; thresholds for accuracy, validated on a split not used for fitting | the current file costs 2.3 points | code only | unclaimed |
| Prompt-template robustness: random `formatting.PROMPTS` mapping per training example; average over 2–4 mappings at eval | learn the task, not the template | code + ≈ $2 GPU | unclaimed |
| Tree full fine-tune (no adapter) | upper bound for capacity; r64 gave +2.1 on round-1 data | needs code (train_tree always wraps PEFT) + ≥ 48 GB GPU | unclaimed |
| Smaller tree student (0.6B / 1.7B) distilled from the tree 4B | speed; the 0.6B stock reaches only 68.8 on eval2 | 1 GPU-day | unclaimed |
| Latency on a fast GPU: vLLM tree on an H100 (bf16 and FP8), same sweep (`scripts/latency_sweep.py`) | Jev's flat ~150 ms at 4K tokens × 16 questions needs ≥ 10× an A10G's compute | ≈ $5 (p5.4xlarge $6.88/h) | proposed, awaiting OK; H100 capacity was unavailable in Ohio on 2026-09-24 |
| Tree execution: structured attention kernel | the direct branch mask is done; kernel work remains | code only | unclaimed |
| vLLM path on eval2 (R1 and compact were checked on the dev benchmark only) | confirm serving quality on the target task | ≈ 15 min GPU | unclaimed |
| Stock 4B on round-2 data (`scripts/run_4b_r2.sh`) | control for the tree's round-2 number; the first run was stopped unfinished | ~1 h A10G | unclaimed |
| jina 0.6B follow-ups: 2 epochs (`configs/jina_r2b_e2.json`), r64 + MLP (`configs/jina_r2b_r64.json`), pairwise layout (`scripts/run_jina_followups.sh`) | adapter- or data-limited? | ~1 h A10G each | unclaimed |
| Score Laya (`pip install laya`, Apache 2.0) zero-shot on eval2 and the dev benchmark, `max_len=8192`, via its Jev-shaped API | the only open competitor with the same interface | Mac only, ≈ 1 h, $0 | unclaimed |
| Score our best tree on the public JevBench items; score 2–3 open models (Laya, open-jev-deberta, kev-4b) on eval2 | the only shared yardstick across open Jev-like models | $0 (model downloads) | unclaimed |
| Fresh final test set (new authors, templates and documents) | both current test sets have informed decisions | ≈ $40 API | unclaimed |
| GLiClass-Instruct / hybrid backbones | alternatives from the strategy memo | research | deferred |

## Done ideas

| idea | result | where |
|---|---|---|
| Frozen target-task test set (eval2) | 1,991 q / 647 states, 3 authors, 2 blind judges (96.2% kept), Jev 97.2%, $32.72 | `data/eval2/REVIEW.md` |
| Tree + higher LoRA capacity (r64; r16 + MLP) | dev benchmark flat; eval2 +2.1 / +1.2 | `reports/curve/summary.md` |
| Combine round-2b data with r64 / r64 + MLP | 90.3 / 91.3 vs 90.6 | `reports/curve/tree_4b_r2b_r64*` |
| Instruct base + round-2 data + r64 | **92.7**, best so far | `reports/tree_4b_instruct_r2x64` |
| Full candidate bank in the question ("all options") | eval2 91.6 vs 90.6, dev benchmark 82.6 vs 81.2 | `reports/tree_4b_ova` |
| Round-2 `none` cap at 10% | CLINC back to 92.0, dev benchmark 81.2, eval2 90.6 | `reports/tree_4b_r2b`, `scripts/rebalance_nota.py` |
| Round-3 training data | 38,628 verified questions, ≈ $280 | `data/hardcases_r3/review/REVIEW.md` |
| 27B teacher: validation, eval2, training-split scores, distillation | complementary, but no gain from KD at 0.5 | `reports/teacher/`, `reports/tree_4b_ova_kd` |
| Direct branch-mask construction, vLLM path, `--merge` | scores unchanged; vLLM 1.3–2× faster on an A10G; merge 15–35% faster | `reports/latency_optimization_2026-09-24/`, JOURNAL 2026-09-23 21:10 |
| vLLM quality check on the dev benchmark | R1 vLLM 81.53 vs merged HF 81.50 | `reports/latency_optimization_2026-09-24/` |
| Compact tree format | failed the 15% speed gate | `reports/latency_optimization_2026-09-24/conclusions.md` |
| Architecture review after latency and eval2 | proposed T5Gemma 2; superseded when the earlier T5Gemma run was found | `reports/architecture_next_2026-09-24.md` |
| Integrate the latency/compact experiment into `master` | code, reports and weights moved; 16 tests pass | `reports/latency_optimization_2026-09-24/integration.json` |
| Docs site and cleanup | Zensical site from `docs/`, README rewritten, this file restructured | [JOURNAL 2026-09-24](JOURNAL.md) |

## Where things are

| what | where |
|---|---|
| formatted findings, leaderboard, models, data, speed | the docs site: `docs/*.md`, built with Zensical (see [README](../README.md)) |
| tree scorer: design, results, speed, reproduce | [tree_model.md](tree_model.md), `src/personal_jev/tree.py`, `train_tree.py`, `vllm_tree.py`, `configs/tree_4b*.json`, `scripts/run_tree_gpu.sh`, `run_tree_r2.sh` |
| custom cross-attention model | [custom_model.md](custom_model.md), `src/personal_jev/custom.py`, `train_custom.py`, `configs/custom_*.json`, `reports/custom_diagnostics/` |
| jina and T5Gemma challengers | [jina_model.md](jina_model.md), [challengers.md](challengers.md), `reports/t5_round2b_2026-09-24/` |
| learning curves (data volume, epochs, per-task, base model, capacity) | [reports/curve/summary.md](../reports/curve/summary.md), `configs/curve/`, `scripts/run_curve.sh`, `scripts/summarize_curve.py` |
| eval2 | `data/eval2.jsonl`, `data/eval2/REVIEW.md`, [reports/eval2/summary.md](../reports/eval2/summary.md), `scripts/run_eval2.sh`, `scripts/eval2_summary.py` |
| reviews and strategy | `reports/review_2026-09-23.md`, `reports/deep_review_2026-09-23/`, `reports/strategy_2026-09-23/`, `reports/tree_review_2026-09-23/review.md`, `reports/architecture_next_2026-09-24.md` |
| Jev comparison (cached API answers) | `reports/external/`, `scripts/compare_external.py`, failures in `reports/external/failures.md` |
| latency | `reports/bench/`, `reports/latency/`, `reports/latency_optimization_2026-09-24/`, `scripts/latency_sweep.py` |
| data: sources, splits, labeling policy | [data.md](data.md); briefs `data/eval/BRIEF.md`, `data/synthetic/BRIEF.md`, `data/hardcases/BRIEF.md`; builders `scripts/build_*.py` |
| round-2 and round-3 hard cases | [hardcases_round2.md](hardcases_round2.md), `scripts/gen_hardcases.py`, `scripts/judge_hardcases.py`, `data/hardcases*/review/` |
| trained weights and training metadata | `runs/<name>/adapter` or `checkpoint`, `runs/<name>/train_meta.json` (not in git) |
| comics explaining the pipeline | `docs/comics/`, `scripts/make_comics.py` |
