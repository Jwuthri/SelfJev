# Experiment ledger

The cross-session state of the project. Every session (Claude Code, Codex, human) reads this before starting work and
updates it when something finishes; the dated log is in [JOURNAL.md](JOURNAL.md). The formatted version of these results
is the docs site: [key findings](findings.md) and [leaderboard](leaderboard.md).

- **eval2** (`data/eval2.jsonl`, 1,991 questions) is the primary benchmark since 2026-09-24. Never train, select prompts
  or fit calibration on it.
- **eval_llm** (`data/eval_llm.jsonl`, 946 questions on LLM prompts, traces and outputs) is a frozen test set since
  2026-09-26, under the same rules ([llm_eval_data.md](llm_eval_data.md)).
- **Dev benchmark** (the "old test"): 3,471 questions = `data/hf.jsonl` test + `data/eval.jsonl` test, identical ids for
  every model. It has been reused for many decisions, so report it as a development benchmark. Never train or tune on it.

## Results (generated)

The table is generated from `reports/*/test/report.json` and `reports/*/eval2/report.json` by
`uv run python scripts/eval/ledger.py`: never hand-edit it. Sorted by eval2, then by the dev benchmark. The report links are
the dev-benchmark `test/report.md` files. The weights column names the adapter kept in `weights/` (only `selfjev-4b`
on master; `qwen35_4b_tree` and `tree_4b_combo` are at tag `archive/pre-cleanup-2026-09-27`, the other adapters were
never in git); "trained on" comes from each run's training log in `reports/train_meta/`. The architecture column is the
engine that scored the report: every Qwen3.5 row was scored by the forked-cache engine that `TreeServer` replaced on
2026-09-27.

<!-- --8<-- [start:ledger] -->
<!-- ledger:start -->
| run | base | architecture | trained on | **eval2 acc %** (target task, 1,991 q) | dev benchmark acc % (old test, 3,471 q) | binary acc % | binary AUROC | multiclass acc % | multilabel EM % | authored eval_* acc % (n=171) | report | weights |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| external | ~typesafe/jev-latest | external API | — | 97.2 | 82.7 | 93.5 | 0.981 | 84.6 | 40.1 | 94.7 | [report](../reports/external/full/typesafe_jev-latest/report.md) | — |
| images_v1 | Qwen3.5-4B | shared-prefix tree, forward only: text once per request, each question once, then each candidate | 22,668 q / 622 steps | 96.1 | 84.1 | 91.9 | 0.973 | 85.4 | 53.5 | 91.2 | [report](../reports/images_v1/test/report.md) | weights/selfjev_4b_vision |
| qwen35_4b_tree_scratch_jevall_ | Qwen3.5-4B | shared document / forked native cache branches | 79,943 q / 1803 steps | 95.8 | 83.8 | 91.5 | 0.974 | 85.3 | 52.3 | 91.2 | [report](../reports/qwen35_4b_tree_scratch_jevall_/test/report.md) | weights/selfjev_4b |
| qwen35_4b_tree_sft_jevall__last | Qwen3.5-4B | shared document / forked native cache branches | 69,528 q / 1230 steps | 95.7 | 84.4 | 90.5 | 0.976 | 85.7 | 59.0 | 92.4 | [report](../reports/qwen35_4b_tree_sft_jevall__last/test/report.md) | — |
| qwen35_4b_tree_cost_jevall__last | Qwen3.5-4B | shared document / forked native cache branches | 69,528 q / 1230 steps | 95.7 | 84.4 | 90.7 | 0.975 | 85.6 | 59.3 | 92.4 | [report](../reports/qwen35_4b_tree_cost_jevall__last/test/report.md) | — |
| selfjev_4b_treeserver | Qwen3.5-4B | shared-prefix tree, forward only: text once per request, each question once, then each candidate | — | 95.7 | 83.8 | 91.6 | 0.974 | 85.2 | 52.6 | 91.2 | [report](../reports/selfjev_4b_treeserver/test/report.md) | — |
| qwen35_4b_tree_rlcd_fresh_ | Qwen3.5-4B | shared document / forked native cache branches | 4,412 q / 97 steps | 95.6 | 84.4 | 90.2 | 0.972 | 85.6 | 59.9 | 90.1 | [report](../reports/qwen35_4b_tree_rlcd_fresh_/test/report.md) | — |
| qwen35_4b_tree_scratch_jevall__last | Qwen3.5-4B | shared document / forked native cache branches | 79,943 q / 1803 steps | 95.6 | 83.8 | 91.7 | 0.974 | 85.3 | 52.0 | 91.2 | [report](../reports/qwen35_4b_tree_scratch_jevall__last/test/report.md) | — |
| qwen35_4b_tree | Qwen3.5-4B | shared document / forked native cache branches | 51,774 q / 941 steps | 95.6 | 84.4 | 90.5 | 0.972 | 85.7 | 59.3 | 90.1 | [report](../reports/qwen35_4b_tree/test/report.md) | — |
| qwen35_4b_tree_sft_fresh_ | Qwen3.5-4B | shared document / forked native cache branches | 4,412 q / 97 steps | 95.4 | 84.5 | 90.2 | 0.971 | 85.8 | 59.9 | 90.1 | [report](../reports/qwen35_4b_tree_sft_fresh_/test/report.md) | — |
| qwen35_4b_tree_rlcd_jevall__last | Qwen3.5-4B | shared document / forked native cache branches | 69,528 q / 1230 steps | 95.4 | 84.5 | 90.7 | 0.975 | 85.5 | 60.8 | 92.4 | [report](../reports/qwen35_4b_tree_rlcd_jevall__last/test/report.md) | — |
| selfjev_4b_v2 | Qwen3.5-4B | shared-prefix tree, forward only: text once per request, each question once, then each candidate | 83,581 q / 1912 steps | 95.4 | 83.5 | 91.2 | 0.973 | 85.2 | 51.7 | 88.9 | [report](../reports/selfjev_4b_v2/test/report.md) | — |
| images_v2 | Qwen3.5-4B | shared-prefix tree, forward only: text once per request, each question once, then each candidate | 30,173 q / 575 steps | 95.2 | 83.5 | 91.4 | 0.973 | 85.3 | 50.6 | 91.8 | [report](../reports/images_v2/test/report.md) | — |
| selfjev_4b_repro | Qwen3.5-4B | shared-prefix tree, forward only: text once per request, each question once, then each candidate | 79,943 q / 1803 steps | 95.1 | 83.8 | 91.8 | 0.973 | 85.2 | 52.3 | 91.8 | [report](../reports/selfjev_4b_repro/test/report.md) | — |
| qwen35_4b_combo | Qwen3.5-4B | shared document / forked native cache branches | 43,827 q / 2474 steps | 94.5 | 84.3 | 90.0 | 0.963 | 85.3 | 62.2 | 84.2 | [report](../reports/qwen35_4b_combo/test/report.md) | — |
| tree_4b_combo | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | 51,826 q / 967 steps | 94.5 | 82.7 | 89.1 | 0.959 | 83.8 | 57.6 | 86.0 | [report](../reports/tree_4b_combo/test/report.md) | — |
| qwen35_4b_r2x64 | Qwen3.5-4B | shared document / forked native cache branches | 17,435 q / 769 steps | 93.7 | 83.4 | 90.9 | 0.971 | 84.0 | 58.4 | 87.7 | [report](../reports/qwen35_4b_r2x64/test/report.md) | — |
| tree_4b_instruct_r3 | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | 51,853 q / 910 steps | 93.3 | 82.8 | 89.8 | 0.966 | 83.9 | 56.1 | 85.4 | [report](../reports/tree_4b_instruct_r3/test/report.md) | — |
| tree_4b_combo_r2 | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | 18,676 q / 239 steps | 92.9 | 83.5 | 90.0 | 0.966 | 84.4 | 59.0 | 84.8 | [report](../reports/tree_4b_combo_r2/test/report.md) | — |
| tree_4b_instruct_r2x64 | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | 18,681 q / 218 steps | 92.7 | 82.7 | 90.9 | 0.965 | 83.7 | 52.9 | 81.9 | [report](../reports/tree_4b_instruct_r2x64/test/report.md) | — |
| tree_4b_combo_ptr | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | 18,676 q / 232 steps | 92.0 | 82.7 | 89.6 | 0.965 | 83.6 | 57.0 | 81.3 | [report](../reports/tree_4b_combo_ptr/test/report.md) | — |
| tree_4b_ova | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,372 q / 241 steps | 91.6 | 82.6 | 89.2 | 0.962 | 83.6 | 57.8 | 84.2 | [report](../reports/tree_4b_ova/test/report.md) | — |
| curve/tree_4b_r2b_r64_mlp | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,375 q / 208 steps | 91.3 | 82.4 | 89.0 | 0.962 | 83.5 | 57.0 | 84.2 | [report](../reports/curve/tree_4b_r2b_r64_mlp/test/report.md) | — |
| tree_4b_ova_kd | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,372 q / 241 steps | 91.0 | 82.5 | 88.1 | 0.959 | 83.8 | 58.4 | 84.8 | [report](../reports/tree_4b_ova_kd/test/report.md) | — |
| tree_4b_instruct_r3_step300 | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | — | 90.8 | 81.5 | 89.4 | 0.954 | 82.5 | 52.6 | 81.3 | [report](../reports/tree_4b_instruct_r3_step300/test/report.md) | — |
| tree_4b_r2b | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,375 q / 225 steps | 90.6 | 81.2 | 88.1 | 0.955 | 82.8 | 51.7 | 83.0 | [report](../reports/tree_4b_r2b/test/report.md) | — |
| tree_4b_r2 | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,357 q / 224 steps | 90.4 | 80.6 | 87.6 | 0.956 | 82.2 | 50.9 | 81.9 | [report](../reports/tree_4b_r2/test/report.md) | — |
| curve/tree_4b_r2b_r64 | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 16,375 q / 208 steps | 90.3 | 81.2 | 87.8 | 0.962 | 82.5 | 54.4 | 82.5 | [report](../reports/curve/tree_4b_r2b_r64/test/report.md) | — |
| tree_4b_instruct | Qwen3-4B-Instruct-2507 | shared-prefix tree (tree-v1) | 10,112 q / 78 steps | 88.1 | 80.4 | 87.8 | 0.958 | 82.3 | 46.8 | 79.5 | [report](../reports/tree_4b_instruct/test/report.md) | — |
| curve/tree_4b_r64 | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 10,080 q / 84 steps | 87.2 | 81.5 | 88.5 | 0.956 | 83.0 | 52.3 | 77.8 | [report](../reports/curve/tree_4b_r64/test/report.md) | — |
| lora_4b | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,112 q / 216 steps | 86.5 | 80.3 | 87.5 | 0.945 | 82.3 | 47.7 | 70.8 | [report](../reports/lora_4b/test/report.md) | — |
| curve/tree_4b_mlp | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 10,080 q / 84 steps | 86.3 | 81.6 | 87.9 | 0.955 | 83.4 | 51.7 | 78.9 | [report](../reports/curve/tree_4b_mlp/test/report.md) | — |
| tree_4b | Qwen3-Reranker-4B | shared-prefix tree (tree-v1) | 10,112 q / 84 steps | 85.1 | 81.6 | 87.1 | 0.953 | 83.9 | 51.7 | 78.4 | [report](../reports/tree_4b/test/report.md) | — |
| t5_round2b_2026-09-24/decoder_only_audit/t5_r2b | google/t5gemma-2-1b-1b | pretrained T5Gemma encoder/decoder; shared document cross-KV views | 16,375 q / 228 steps | 76.8 | 73.8 | 82.7 | 0.893 | 75.1 | 40.4 | 62.6 | [report](../reports/t5_round2b_2026-09-24/decoder_only_audit/t5_r2b/test/report.md) | — |
| jina_r2b | jinaai/jina-reranker-v3.5 | jina listwise (jina-v1) | 16,301 q / 345 steps | 73.3 | 76.6 | 81.4 | 0.888 | 79.4 | 45.1 | 60.2 | [report](../reports/jina_r2b/test/report.md) | — |
| t5_round2b_2026-09-24/t5_r1 | google/t5gemma-2-1b-1b | pretrained T5Gemma encoder/decoder; shared document cross-KV views | 10,080 q / 823 steps | 73.0 | 75.4 | 83.0 | 0.887 | 76.6 | 45.6 | 62.0 | [report](../reports/t5_round2b_2026-09-24/t5_r1/test/report.md) | — |
| lora_pilot | Qwen3-Reranker-0.6B | stock pairs (task-v1) | 10,112 q / 183 steps | 68.8 | 73.5 | 77.8 | 0.863 | 78.3 | 31.1 | 55.0 | [report](../reports/lora_pilot/test/report.md) | — |
| external | openai/gpt-6-astra | external API | — | — | 85.8 | 93.8 | 0.971 | 87.0 | 55.8 | 100.0 | [report](../reports/external/full/openai_gpt-6-astra/report.md) | — |
| curve/boolq_300 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,412 q / 218 steps | — | 80.9 | 88.0 | 0.940 | 82.5 | 50.9 | 71.9 | [report](../reports/curve/boolq_300/test/report.md) | — |
| curve/boolq_1000 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 11,112 q / 224 steps | — | 80.9 | 88.8 | 0.954 | 82.5 | 48.8 | 73.7 | [report](../reports/curve/boolq_1000/test/report.md) | — |
| curve/boolq_3000 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 13,112 q / 240 steps | — | 80.9 | 88.9 | 0.954 | 82.5 | 47.7 | 73.1 | [report](../reports/curve/boolq_3000/test/report.md) | — |
| lora_8b | Qwen3-Reranker-8B | stock pairs (task-v1) | 10,112 q / 185 steps | — | 80.7 | 87.3 | 0.945 | 82.9 | 48.0 | 74.9 | [report](../reports/lora_8b/test/report.md) | — |
| curve/instruct_lora | Qwen3-4B-Instruct-2507 | stock pairs (answer-v1) | 10,112 q / 216 steps | — | 80.6 | 87.4 | 0.944 | 82.6 | 48.3 | 75.4 | [report](../reports/curve/instruct_lora/test/report.md) | — |
| curve/boolq_100 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,212 q / 217 steps | — | 80.0 | 86.9 | 0.945 | 82.0 | 48.3 | 70.8 | [report](../reports/curve/boolq_100/test/report.md) | — |
| curve/vol100_e2 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 10,112 q / 431 steps | — | 79.8 | 87.0 | 0.951 | 81.9 | 46.2 | 69.6 | [report](../reports/curve/vol100_e2/test/report.md) | — |
| curve/vol50_e2 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 5,056 q / 214 steps | — | 79.1 | 84.8 | 0.940 | 81.7 | 46.8 | 72.5 | [report](../reports/curve/vol50_e2/test/report.md) | — |
| curve/vol25_e2 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 2,528 q / 107 steps | — | 79.1 | 85.7 | 0.935 | 81.4 | 45.6 | 73.7 | [report](../reports/curve/vol25_e2/test/report.md) | — |
| curve/vol50_e1 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 5,056 q / 107 steps | — | 78.9 | 84.5 | 0.934 | 81.9 | 44.5 | 70.2 | [report](../reports/curve/vol50_e1/test/report.md) | — |
| curve/vol25_e1 | Qwen3-Reranker-4B | stock pairs (answer-v1) | 2,528 q / 53 steps | — | 77.0 | 83.8 | 0.930 | 80.8 | 33.4 | 71.9 | [report](../reports/curve/vol25_e1/test/report.md) | — |
| curve/instruct_zero | Qwen3-4B-Instruct-2507 | stock pairs (answer-v1) | — | — | 71.3 | 84.2 | 0.911 | 73.5 | 20.1 | 63.2 | [report](../reports/curve/instruct_zero/test/report.md) | — |
| baseline_8b | Qwen3-Reranker-8B | stock pairs (task-v1) | — | — | 66.2 | 56.1 | 0.658 | 79.8 | 10.2 | 50.3 | [report](../reports/baseline_8b/test/report.md) | — |
| baseline_4b | Qwen3-Reranker-4B | stock pairs (answer-v1) | — | — | 62.8 | 55.0 | 0.604 | 76.2 | 2.0 | 44.4 | [report](../reports/baseline_4b/test/report.md) | — |
| baseline | Qwen3-Reranker-0.6B | stock pairs (task-v1) | — | — | 61.0 | 55.3 | 0.605 | 73.3 | 1.2 | 39.2 | [report](../reports/baseline/test/report.md) | — |
| custom_sim_lora | Qwen3-Reranker-0.6B | shared-state cross-attention (custom-v1) | 10,112 q / 1176 steps | — | 58.2 | 51.7 | 0.514 | 70.2 | 1.7 | 42.1 | [report](../reports/custom_sim_lora/test/report.md) | — |
| custom_sim_frozen | Qwen3-Reranker-0.6B | shared-state cross-attention (custom-v1) | 10,112 q / 1176 steps | — | 48.0 | 51.4 | 0.524 | 53.9 | 1.5 | 38.0 | [report](../reports/custom_sim_frozen/test/report.md) | — |
| custom_distill_lora | Qwen3-Reranker-0.6B | shared-state cross-attention (custom-v1) | 16,671 q / 2028 steps | — | 39.7 | 51.3 | 0.451 | 40.6 | 0.9 | 35.1 | [report](../reports/custom_distill_lora/test/report.md) | — |
| custom_frozen | Qwen3-Reranker-0.6B | shared-state cross-attention (custom-v1) | 10,112 q / 1764 steps | — | 39.0 | 51.9 | 0.536 | 39.1 | 1.2 | 36.3 | [report](../reports/custom_frozen/test/report.md) | — |
| custom_distill_frozen | Qwen3-Reranker-0.6B | shared-state cross-attention (custom-v1) | 16,671 q / 2028 steps | — | 37.7 | 52.8 | 0.507 | 36.7 | 0.6 | 36.8 | [report](../reports/custom_distill_frozen/test/report.md) | — |
<!-- ledger:end -->
<!-- --8<-- [end:ledger] -->

## eval2: the primary benchmark

Full slices (type, tier, author, length, trap) and paired tests: [reports/eval2/summary.md](../reports/eval2/summary.md),
generated by `uv run python scripts/eval/eval2_summary.py`. Score new models with `selfjev eval --data data/ova/eval2.jsonl`
([reproduce](reproduce.md#train-and-evaluate-on-a-gpu-box-never-on-the-laptop)), then re-run the summary.

| model | eval2 acc % | binary | multiclass | multilabel EM | dev benchmark |
|---|---|---|---|---|---|
| Jev | **97.2** | 97.8 | 98.1 | 94.2 | 82.7 |
| **selfjev-4b** (`qwen35_4b_tree_scratch_jevall_`: the `qwen35_4b_tree` recipe from scratch on 79.9K non-test questions of `data/all.jsonl.gz`, texts ≤ 16K, target 0.5 × label + 0.5 × Jev) | **95.8** | 96.8 | 97.0 | **91.4** | 83.8 |
| **qwen35_4b_tree** (Qwen3.5-4B trained with the tree, round-2b + round-3 data, all options listed in the question, r64, texts ≤ 8K) | **95.6** | 96.9 | 96.8 | **90.1** | **84.4** |
| **qwen35_4b_combo** (Qwen3.5-4B, round-2b + round-3 data, all options listed in the question, r64, texts ≤ 2K) | **94.5** | 96.2 | 95.8 | **88.2** | 84.3 |
| **tree_4b_combo** (Instruct base, round-2b + round-3 data, all options listed in the question, r64) | **94.5** | 96.0 | 97.5 | 85.9 | 82.7 |
| **tree_4b_instruct_r2x64** (Instruct base, round-2b data with hard cases exempt from the family cap, r64) | **92.7** | 94.6 | 95.4 | 83.5 | 82.7 |
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

- **Qwen3.5-4B base (2026-09-24, JOURNAL):** `qwen35_4b_r2x64`, same data as `tree_4b_instruct_r2x64` but training texts ≤ 2K and full-sequence training, scores **93.7** (vs 92.7, p = 0.09; vs round-3 tree 93.3, p = 0.53), best on long texts (> 4K: 97.0 vs 94.6) and multilabel (86.6 vs 83.5). Eikos-4B (an open Qwen3.5-4B fine-tune, zero-shot through our mapping) scores 92.8.
- **Qwen3.5-4B + option lists + round 3 (2026-09-25, JOURNAL):** `qwen35_4b_combo` scores **94.5**, a tie with `tree_4b_combo` (61 / 60, p = 1) with different strengths (multilabel EM **88.2** vs 85.9, multiclass 95.8 vs 97.5, temporal 80.3 vs 85.2). The two levers add only +0.8 on Qwen3.5 (vs `qwen35_4b_r2x64`, p = 0.15; +1.8 on Qwen3), likely because the 2K training cap dropped 18.5% of the data. Dev benchmark **84.3**, our best then and above Jev (250 / 194, p = 0.009).
- **Qwen3.5-4B trained with the tree (2026-09-25, JOURNAL):** `qwen35_4b_tree`, the same data and LoRA as `qwen35_4b_combo` but a real shared-prefix tree in training (texts ≤ 8K, 3.7% dropped), scores **95.6**, significantly above both 94.5 models (p = 0.028 and 0.039); multilabel EM 90.1, simple tier 98.6 (Jev 98.5); 1.6 behind Jev (31 / 64). Dev benchmark 84.4.
- **`selfjev-4b`, the default (2026-09-26, JOURNAL 21:25):** the same recipe trained from scratch on 79,943 non-test questions (the LLM-evaluation data and two new batches included, texts ≤ 16K) with half-weight Jev targets scores **95.8** (vs `qwen35_4b_tree` 33 / 29, p = 0.70; vs Jev 23 / 52, p = 0.0011); eval_llm 93.1 (Jev 92.5, 33 / 27, p = 0.52); dev benchmark 83.8 (Jev 82.7, 164 / 128, p = 0.04).

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
base stacks with the data: `tree_4b_instruct_r2x64` 92.7 vs r2b 90.6 (90 / 47, p = 0.0003; that run also used r64 and
kept every hard case, 18,681 vs 16,375 questions).

## Current conclusions (2026-09-28)

Each has a formatted box with its evidence in [findings.md](findings.md).

1. **Default model: `selfjev-4b`** (2026-09-26, fork; `weights/selfjev_4b`, the only adapter on master): the
   `qwen35_4b_tree` recipe (Qwen3.5-4B + LoRA r64, shared-prefix tree, every option listed in the question) trained from
   scratch by `selfjev finetune` on 79.9K non-test questions of `data/all.jsonl.gz` (texts up to 16K; batch
   `mpos_distr_num_v1` came later), target 0.5 × label + 0.5 × Jev's probabilities.
   - eval2 **95.8** (vs `qwen35_4b_tree` 33 / 29, p = 0.70; vs Jev 23 / 52, p = 0.0011), eval_llm **93.1**
     (`qwen35_4b_tree` 82.1, Jev 92.5), dev benchmark 83.8 (−0.7, from Jev's targets on the public emotion set);
     confident mistakes on eval2 30 → 11 (Jev 7). JOURNAL 2026-09-26 21:25.
   - Served by `TreeServer` (`src/selfjev/engine/tree.py`, the default engine of `selfjev serve`) or on vLLM
     (`selfjev merge`, then `--engine vllm`). `TreeServer` is exact against standalone sequences in a CPU test; its GPU
     latency and memory, 1–50 questions on one text, are in `reports/bench/selfjev4b_qsweep_summary.md` (2026-09-30). A retrain with batch 2 (`selfjev_4b_v2`) came out worse (eval_llm 90.5 vs 93.1, p = 0.0002) and was not promoted; a rerun of `selfjev-4b`'s exact recipe with the new code (`selfjev_4b_repro`) scored eval2 95.08 vs 95.78 (28 / 42, p = 0.12), dev benchmark 83.81 vs 83.75 (p = 0.92), eval_llm 91.97 vs 93.13 (16 / 27, p = 0.13): single runs of this recipe differ by about a point (JOURNAL 2026-09-27 22:25).
   Previous: **`qwen35_4b_tree`** (2026-09-25, fork; weights at tag `archive/pre-cleanup-2026-09-27`): Qwen3.5-4B +
   LoRA r64 trained with the shared-prefix tree (`selfjev/engine/tree.py`: DeltaNet layers level by level from copied
   states, attention through the tree mask), every option listed in the question, round-2b + round-3 data uncapped,
   texts ≤ 8K.
   - eval2 **95.6** (vs `qwen35_4b_combo` 94.5, 52 / 31, p = 0.028; vs `tree_4b_combo` 94.5, 63 / 41, p = 0.039; Jev 97.2,
     31 / 64); multilabel EM 90.1; dev benchmark 84.4 (Jev 82.7, p = 0.004).
   - Same data and base as `qwen35_4b_combo`: the tree's +1.1 comes from training on long texts (3.7% dropped instead
     of 18.5%), in 38% less training time.
   - Served then by the forked-cache engine (transformers; removed on 2026-09-27 for `TreeServer`) or on vLLM (eval2
     95.58 there too): vLLM was faster for one question (87 vs 156 ms at 512 tokens, L40S), the fork path for many
     (16 questions: 341 vs 454 ms at 512 tokens, 508 vs 908 at 2K). JOURNAL 2026-09-25 18:05.
   Previous: **`tree_4b_combo`** (2026-09-24, fork; weights at the same tag): Qwen3-4B-Instruct-2507, tree, LoRA r64,
   every option listed in the question, round-2b + round-3 data uncapped.
   - eval2 **94.5** (vs `tree_4b_instruct_r3` 93.3, p = 0.025; Jev 97.2, 27 / 82); dev benchmark 82.7 (Jev 82.7).
   - Option lists and round 3 each add about a point and they stack.
   - Served (with the code at the tag) with `--options-in-question`.
   - **Tied on eval2 by `qwen35_4b_combo`** (2026-09-25): Qwen3.5-4B, same levers, 94.5 (61 / 60, p = 1); multilabel EM 88.2
     vs 85.9; dev benchmark 84.3 vs 82.7 (p = 0.001) and above Jev (p = 0.009). Its training has no tree (texts ≤ 2K,
     18.5% dropped) and it had no vLLM serving path yet, so `tree_4b_combo` stayed the served model then.
   Previous: **`tree_4b_combo_r2`**, `tree_4b_instruct_r2x64` + every option listed in the question.
   - eval2 92.9 (vLLM serving 93.0; the control 92.7, p = 0.83).
   - Dev benchmark 83.5 (the control 82.7, p = 0.08; Jev 82.7, p = 0.22).
   - Old-test multilabel 59.0 vs 52.9.
   - Served with `--options-in-question`. With round 3 it became `tree_4b_combo`.
   Previous best: **`tree_4b_instruct_r2x64`**: Qwen3-4B-Instruct-2507, shared-prefix tree, LoRA r64, round-2b data with
   the hard-case families exempt from the 1,600-per-family cap. eval2 92.7 (Jev 97.2, 25 / 115, p = 5e-15); dev benchmark 82.7, tied with Jev (213 / 214). It was the
   control for round 3.
2. **The dev benchmark cannot rank models.** Public-label noise caps the 4B models and frontier models alike at 80–86%. It called data, base model
   and capacity ties; eval2 shows +5.5, +3.0 and +2.1. Re-check any "no gain" measured on it before treating it as dead.
3. **Verified target-task data is the biggest lever** (+5.5 on eval2). Mix details matter: round 2's `none`-heavy
   multiclass data cost CLINC 94.7 → 83.3; capping `none`-correct at 10% (r2b) restored 92.0 (a test diagnosis).
4. **More of the same data buys ~1.5 points per doubling; a second epoch never helps; a new task type needs thousands
   of examples** (BoolQ +3,000 → BoolQ 86.7, overall unchanged). [reports/curve/summary.md](../reports/curve/summary.md).
5. **Model choice:** 4B ≈ 8B (80.3 vs 80.7, p = 0.52); sub-1B is 17 points behind on eval2 (0.6B Qwen 68.8, jina 73.3);
   the Instruct base beats the reranker once the data is good.
6. **Capacity overlaps with data:** r64 +2.1 on round-1 data, +0 on round-2b data; r64 + MLP +0.7 (n.s.).
7. **Listing every option in the question helps** (`tree_4b_ova`): dev benchmark 82.6 vs 81.2 (p = 0.001), eval2 91.6
   vs 90.6 (p = 0.07).
   - On the Instruct r64 base (`tree_4b_combo_r2`): eval2 +0.2 (tie), dev benchmark +0.8 (p = 0.08), multilabel +6.1.
   - Latency cost: about +120 ms at 16 questions on an A10G, nothing at 1 question.
8. **The 27B teacher is complementary but does not distil** at weight 0.5: teacher zero-shot 91.4 on eval2, 50/50
   ensemble with `tree_4b_ova` 94.5, distilled student 91.0 vs 91.6 (p = 0.21). Closed at the 2026-09-27 cleanup
   (teacher code at the archive tag).
9. **The tree scorer is the architecture:** same quality as stock pairs, 32–37× faster at 16 × 3 on 8K–16K tokens.
   The custom cross-attention model (39.0 / 58.2), T5Gemma 2 (73.0 eval2), jina 0.6B (73.3) and Qwen3.5-2B with a
   forked cache (84.3 eval2 and 79.9 dev benchmark on round-1 data, vs 85.1 and 81.6 for the round-1 tree 4B) all fall
   short.
10. **Calibration:** temperatures fit near 1 after LoRA; the F1-maximizing thresholds fitted for `tree_4b` (the `calib/`
    files are at tag `archive/pre-cleanup-2026-09-27`) lower accuracy (81.6 → 79.3): serve without them. SST-2 (held out) is a bias: AUROC 0.973 but 34.7% predicted positive.
11. **Speed vs Jev** ([reports/latency/summary.md](../reports/latency/summary.md)): Jev is flat at ~150 ms p50 from 8 to
    4,096 tokens and 1 or 16 questions. Tree 4B + vLLM on one A10G matches it up to ~128 tokens with 1 question and is
    5× slower at 4,096 tokens, 2–7× slower with 16 questions. Fully busy, the A10G is 1.3–3.1× cheaper per request for
    one question, 1.0–1.5× with 16. **On one H100 (2026-09-26, p5.4xlarge spot) the Qwen3 tree (`tree_4b_combo`) is
    faster than Jev inside the machine in every cell but 4,096 tokens × 16 questions** (server-side 22–82 ms vs
    110–122 ms for one question; 58–189 vs 117–134 ms for 16); the remaining end-to-end gap (10–100 ms) is the 61 ms
    network hop vs OpenRouter's 11 ms. FP8 adds nothing. The speed gap was hardware, not architecture
    ([speed](speed.md#the-same-model-on-an-h100-2026-09-26)). All these numbers are the Qwen3 tree's: the default
    `selfjev-4b` on `TreeServer` has not been timed on an NVIDIA GPU. On a local M5 Pro with PyTorch MPS, the current
    model took 688 / 2,018 ms for one question and 6,786 / 8,599 ms for 16 questions at 8 / 512 text tokens (10-run
    medians after two warm-ups, [report](../reports/latency/mac_m5_pro_selfjev4b.json)). The MPS path uses a slower
    reference recurrent operation; these are not comparable to the earlier Qwen3-on-vLLM GPU numbers.
12. **Serving:** vLLM + merged weights is the general option (967 → 700 ms at 2K × 16 × 3, dev benchmark 81.53 vs
    81.50). The compact tree format failed its 15% speed gate (7.4%) and adds CLINC over-rejection: experimental only
    ([conclusions](../reports/latency_optimization_2026-09-24/conclusions.md)).
13. **Remaining gap to Jev on eval2** (`selfjev-4b`, 95.8 vs 97.2; slices with n ≥ 100): multi-positive 91.0 vs 96.0,
    numeric 87.5 vs 92.0, multi-turn 92.6 vs 96.0, distractor 93.9 vs 97.0, multilabel EM 91.4 vs 94.2; the simple
    tier level (98.5 vs 98.5), exceptions ahead (96.2 vs 95.3). In wrong questions vs Jev: multi-positive 29 vs 13,
    distractor 29 vs 14, numeric 28 vs 18, the target of batch `mpos_distr_num_v1`. Text length is not a weakness.
    The previous default (`qwen35_4b_tree`, 95.6) also trailed by 3–5 points on double negation, hypothetical, temporal,
    paraphrase, long state and the very hard tier; `selfjev-4b` closed each to under 3.
14. **What Jev's behaviour implies** ([memo](../reports/jev_hypothesis_2026-09-25.md), inference): a shared state
    with isolated per-question branches (its limit is "state plus the longest question"), options inline with one
    readout per option (113 billed tokens per 3-option question), a model of at most a few B parameters on
    H100/B200-class hardware (400K tokens/s marginal), trained on frontier judgments rather than public labels
    (dev-benchmark multilabel EM 40.1 vs our 57.6) with a calibration objective (7 of its 55 eval2 errors are
    confident, 26 of our 110). Fixed 50/50 averages of our models reach 95.9 (`qwen35_4b_tree` + combo) and 96.3
    (`qwen35_4b_tree` + the 27B) with nothing fitted ([eval2/ensembles.md](../reports/eval2/ensembles.md); those
    adapters and `scripts/ensemble_eval2.py` are at the archive tag).

15. **Jev's probabilities as soft targets make the model hedge; RLCD adds nothing over fine-tuning** (2026-09-26):
    0.5 × label + 0.5 × Jev on 69.5K questions from `qwen35_4b_tree`: eval2 95.73 vs 95.58 (n.s.), confident mistakes
    30 → 14 (Jev 7), Brier −9%; dev benchmark flat. RLCD on the same targets: 95.43, 22 (vs the fine-tune p = 0.18).
    Retrained from scratch on everything (16K texts, both new batches) with these targets: eval_llm 82.1 → 93.1 (Jev 92.5),
    eval2 95.78, dev benchmark −0.7 (Jev's targets on emotions, where Jev is weak).
    Hard-label RLCD did nothing (JOURNAL 2026-09-25 23:45). RLCD with a decision cost is different (C): `confident_miss=5` on top of B gives
    8 confident mistakes on eval2 (Jev 7) and 48 on the dev benchmark (Jev 253) at the same accuracy, for a worse Brier (0.052). But at equal coverage
    C is no better than B: it is less sure overall, which a higher threshold on B also gives. Jev's edge is ranking (8 mistakes
    at 92% coverage vs B 20), not hedging.
16. **Images (2026-09-29/30, JOURNAL 18:10 -> 02:05):** `state` may be an image or text + image parts; the tree keeps its
    shape (image in the root, frozen Qwen3.5 vision tower, 3D M-RoPE). L40S: 163 ms per image request vs 136 ms text. Jev takes
    no images. One mixed fine-tune from `selfjev-4b` (11.3K image questions from 6 licence-safe datasets + 11.3K replayed text
    questions, lr 5e-5, 1 epoch): trained image sets 70.4 -> 94.2%, held-out image sets 83.5 -> 84.3 (no transfer), text within
    noise (eval2 96.13, eval_llm 92.49, dev 84.07). Replay is what keeps text: pets-only training without it cost eval2 0.4.
17. **Open competitors, measured (2026-09-30, JOURNAL 14:15; `reports/competitors/matrix.md`):** on our frozen sets
    through Jev's exact requests, selfjev-4b-vision (eval2 94.7, eval_llm 90.7) beats the 7 smaller open models tested
    (Plumb, jpt, imajev, decider, Mica, kev at ≈ 4B; Laya 0.4B at 45) in paired tests (p ≤ 0.023); openjev-27B beats it on eval2 (96.8, p = 4e-5).
    On shared public benchmarks it is mid-pack: JevBench public-231 83.5 (Plumb 89.6, jpt 87.9, openjev 87.4, Jev
    86.6), typed-decisions 66.1 (openjev 71.1, Jev 72.7), Nimble 13 macro 74.8 (Jev 76.0). Held-out images: a tie
    (85.1 vs imajev 85.2). Slower than most 4B peers end to end (eval2 242 s vs 90–162 s). Jev's request shape costs
    us 1.4–1.8 points (multilabel as nouls). A public "best" claim is not supported.

## Dead ends: do not redo

Measured where noted. eval2 revives anything measured only on the dev benchmark until eval2 re-scores it.

| tried | result | evidence |
|---|---|---|
| Chain layout (a verdict line per option in one branch, each seeing the previous; Jev-memo proposal A, 2026-10-01) | paired pilot from the text release, same 15K questions: eval2 94.83 vs 95.48 for leaves (25 / 38, p = 0.13), select-all 89.8 vs 89.3 (n.s.), multi_positive 91.0 vs 89.8 (n.s., Jev 96.0), dev multilabel 50.3 vs 53.8 (p = 0.0075); 2.6% of answers change when options are reversed | `reports/chain_pilot/`, JOURNAL 2026-10-01 02:40 |
| Ensembles of our own adapters (logit average of vision v1, text release, v2) on eval2 | 96.13 -> at best 96.23 (n.s.): same base and data, same mistakes | JOURNAL 2026-10-01 02:40, `scripts/eval/jev_gap.py` |
| Batch `mpos_distr_num_v1` (3,645 several-correct / distractor / number questions) added to the `selfjev-4b` recipe | eval2 95.38 vs 95.78 (33 / 41, p = 0.42), dev benchmark 83.55 vs 83.75 (p = 0.60), eval_llm 90.49 vs 93.13 (9 / 34, p = 0.0002): worse, broadly on hard LLM-evaluation questions; not the eval engine (same weights score the same on both, JOURNAL 11:55); against a same-code rerun without the batch: eval_llm 90.49 vs 91.97 (p = 0.07), eval2 95.38 vs 95.08 (p = 0.55): no gain, part of the drop is run-to-run noise | `reports/selfjev_4b_v2`, JOURNAL 2026-09-27 11:20 |
| Stock LoRA, 2 epochs instead of 1 | dev benchmark 79.8 vs 80.3; best validation checkpoint inside epoch 1 | `reports/curve/vol100_e2` |
| Stock LoRA on 8B instead of 4B | dev benchmark 80.7 vs 80.3, p = 0.52; about 1.5× slower | `reports/lora_8b`, `reports/scale_comparison.md` |
| More of the same training mix | ~1.5 points per doubling; matching Jev this way would take several × the data | `reports/curve/summary.md` |
| Custom model: frozen backbone, Stage A only | 39.0 | `reports/custom_frozen` |
| Custom model: joint LoRA without the similarity term | 39.7, p = 0.32 vs frozen | `reports/custom_diagnostics/logs/` |
| Custom model: distillation from the stock 0.6B teacher (`data/distill.jsonl`, at the archive tag) | no gain over direct training | `reports/custom_distill_frozen`, `reports/custom_distill_lora` |
| Explicit attention mask in the custom encoder | identical outputs, 1.7–2.2× slower on MPS, loses the flash kernel on CUDA | `reports/custom_diagnostics/shapes.py` |
| jina-reranker-v3.5 (0.6B) as a smaller backbone, tree-r2b recipe | eval2 73.3 vs 90.6 (tree 4B r2b); non-commercial license | `reports/jina_r2b`, [jina_model.md](jina_model.md) |
| Applying the fitted calibration file to the tree model | dev benchmark accuracy 81.6 → 79.3 | `reports/tree_4b/test_calibrated` |
| Distilling Qwen3.8-27B-FP8 zero-shot probabilities into the tree 4B (weight 0.5 on target-task rows) | eval2 91.0 vs 91.6 (p = 0.21). Untried: multiclass-only, lower weight, r64 student | `reports/tree_4b_ova_kd` |
| Astra's verbalized probabilities as soft labels | 98.8% of questions have every probability ≤ 0.05 or ≥ 0.95: they equal the hard labels | `data/hardcases/review/batch_results/` |
| Compact tree format (shorter branches) | 7.4% faster on vLLM (gate: 15%), CLINC 94.7 → 91.7 | `reports/latency_optimization_2026-09-24/` |
| RLCD vs a plain fine-tune on the same soft targets (Jev, all data) | eval2 95.43 vs 95.73 (4 / 10, p = 0.18), more confident mistakes (22 vs 14); a proper-score reward of the same target is fine-tuning with noise | `reports/qwen35_4b_tree_rlcd_jevall__last`, JOURNAL 2026-09-26 09:10 |
| RLCD with a 5× confident-mistake cost (`confident_miss=5`) on top of that fine-tune (C) | 8 confident mistakes on eval2 (fine-tune 14, Jev 7), but only by being less sure overall: no better than the fine-tune at equal coverage, Brier 0.0518 vs 0.0438 | `reports/qwen35_4b_tree_cost_jevall__last`, JOURNAL 2026-09-26 15:15 |

Revived by eval2 (dead on the dev benchmark only): the Instruct base (+3.0), LoRA r64 (+2.1) and MLP targets (+1.2).

- **RLCD on questions the model already fits** (2026-09-25): worse on every validation measure within 100 steps
  (ECE 0.005 → 0.024, confident mistakes 15 → 40). Use data the model has not trained on. With hard labels only it
  also did nothing useful on fresh data (JOURNAL 2026-09-25 23:45).

## Known issues and gotchas

- **Image fine-tuning speed is the replayed text, not the images** (measured 2026-09-30): preparing an image costs ~5 ms
  (0.05 s of a 17 s step); the text replay is ~95% of the tokens, and texts over 4K tokens are 11.5% of the replayed
  questions but 64% of the text tokens. `scripts/data/build_images_v1.py LONG_FRAC` keeps that share of the long ones
  (1/3: ~1.7x faster); check eval2's > 4K slice (9.3% of eval2) when using it.

- **Concurrent requests wait for the whole batch.** In the end-to-end test (2026-09-28, L40S, [report](../reports/e2e/2026-09-28/report.md)) 16
  concurrent requests came back together after 18.6 s cold and 4.4–6.4 s warm with a fine-tuning job on the same GPU
  (one request: 0.2–0.3 s). Not measured without the training job; if it holds, cap `max_batch_requests` or split
  batches by size. The first request after start took 39 s: `selfjev serve` now warms up before `/health` answers.
- **Long jobs and `uv run`.** A plain `uv run` re-syncs the environment to the default groups; during the end-to-end
  test that removed `boto3` from under the running deploy and its teardown failed (box up 6 extra minutes). The dev
  group now includes the `deploy` extra.

- **Every report in `reports/` was scored by an engine master no longer has.** The Qwen3.5 reports (`selfjev-4b`
  included) came from the forked-cache engine; master serves and evaluates with `TreeServer`, exact against standalone sequences in a
  CPU test. `scripts/train/selfjev_4b.sh` starts with a GPU preflight: `selfjev-4b` on 400 eval2 questions must agree
  with its stored report on ≥ 97% of decisions. `TreeServer` has not re-scored the full test sets; its GPU latency is
  measured (`reports/bench/selfjev4b_qsweep_summary.md`, 2026-09-30).
- The stock-pair latency benchmarks of 2026-09-22/23 (`reports/bench/`) ran prompt `task-v1` while their quality reports
  used `answer-v1`: latency ratios are valid, exact same-format claims are not. On master `selfjev bench` times the
  served model with its own prompt.
- **Fixed 2026-09-24** (Qwen3 tree, now at the archive tag): `TreeModel.cached` builds only the branch mask instead of
  the full T×T document mask; GPU score parity in `reports/latency_optimization_2026-09-24/parity_a10g.json`. The
  latency gain alone was small.
- **eval2 ids:** join on the expanded row ids (`<source_id>-q<i>`). The first export renumbered ids after drops;
  `data/eval2/review/id_map_sourceformat_to_real.json` remaps reports scored on it.
- Apple MPS caches one graph per tensor shape: the custom trainer (at tag `archive/pre-cleanup-2026-09-27`) bucketed shapes (25% ladder) to keep
  memory flat (2.7 GB → 0.9 GB for +6.7% time).
- No evals or training on the laptop (see [AGENTS.md](../AGENTS.md)). A g5.xlarge (A10G, $1.006/h) trains one 4B LoRA
  on 10K questions in ~40 min and runs the dev benchmark in ~4 min; a `selfjev-4b` retrain with its evals takes ≈ 9 h
  on a g6e.2xlarge (L40S, $2.242/h). Launch boxes with `scripts/aws/aws_launch.sh` (tags, SSH-only security group,
  shutdown cap). AWS GPU capacity is often short: g6e (L40S) and H100 launches failed repeatedly on 2026-09-23/24;
  since 2026-09-25 the g6e.2xlarge in us-east-2 has been available, H100 only once (spot, 2026-09-26).
- `reports/external/failures.md` and `reports/audit_2026-09-26/` describe **test** failures: use them to design data
  families, never as training data.
- Remote boxes: `pkill -f <pattern>` inside `ssh host '<command>'` kills the remote shell when the pattern appears in the
  command string, and vLLM's EngineCore child keeps the GPU memory after its parent dies. Free a GPU by the PIDs from
  `nvidia-smi --query-compute-apps=pid --format=csv,noheader`, then check `memory.used` is 0.
- Paid generation and judging ([hardcases_round2.md](hardcases_round2.md)):
  - OpenRouter's batch API refuses this account's key, so half-price judging goes through OpenAI's Batch API
    (`scripts/data/judge_hardcases.py`; it saves progress after every chunk, so reruns submit only what is left).
  - Cap hidden reasoning per model: Gemini `effort: low`, DeepSeek `enabled: false`; Grok's cannot be disabled
    (8–20K hidden tokens per call; about 2× Gemini's cost per text).
  - Gemini and OpenAI are BYOK on this OpenRouter account: budget checks must use per-call cost, not the account-usage
    delta.
  - One judge process per review dir and one generator per prefix; check the `none`-correct rate after each build.
  - The API caches (`reports/external/cache/`, the judges' sync caches) are keyed by the request body. Since
    2026-09-27 `selfjev.data.providers` asks LLMs for `max_tokens` 8192 (was 6000), so GPT-6 Astra reruns of
    `scripts/eval/compare_external.py` miss the cache and pay again; Jev requests are unchanged.
- Jev as an annotator agrees with authors on 93.0% (worst: temporal, numeric, injection, multilabel): a second opinion,
  not the gate. 432 round-2 questions are author = Astra but Jev wrong (`data/hardcases/review/JUDGE.md`).

- **vLLM and hybrid models (Qwen3.5):** vLLM 0.30 caches the Gated DeltaNet state only at attention-block boundaries
  (528 tokens here, 272 with `mamba_ssm_cache_dtype` bf16); `mamba_block_size` does not change that. Prompts that
  share a document recompute everything after the last boundary, so many questions per text are slow.
  Any script that starts vLLM needs a `__main__` guard (vLLM spawns its engine process).

## Open ideas: claim before starting (edit the status cell)

- **In progress — Claude Ollama, 2026-09-30:** selfjev-4b-vision as an Ollama model + `selfjev serve --engine ollama` (`src/selfjev/engine/ollama.py`). Known gap to measure: Ollama tokenizes the whole prompt, so the space after "Question:" merges into the first question word (the tree engine tokenizes it alone). Scores for f16 / Q8_0 / Q4_K_M on eval2, eval_llm, images to follow.

- **Done — Codex vision website, 2026-09-30 09:46 PDT:** default vision release links and report-backed text/image scores, text-only secondary release, PyPI 0.3.0 image request/training guides. Snapshot regenerated; build, 495-link export check, 93 external destinations and 390 px layout pass. No reports changed; no commit.

- **Done — Codex architecture UX, 2026-09-29 23:47 PDT:** replaced SVG architecture flowchart with a compact responsive shared-context walkthrough, two authored examples, interactive explanations and optional motion-aware replay. Build, 484-link check, desktop/390 px UI and interactions pass. No report or benchmark changes.

- **Done — Codex image copy, 2026-09-29 23:35 PDT:** result card now says “SelfJev + image fine-tune” / “Fine-tuned on images”; photo count removed. Live dev HTML and diff check pass. Retained the sourced 90% and test scope; no unsupported 25-dataset training claim, report changes or commit.

- **Done — Codex website images, 2026-09-29 23:18 PDT:** homepage image announcement, SDK snippet, report-backed L40S timings and explicitly limited pet-photo results; model/API/fine-tuning guide links. Production build, 484-link export check, Copy button and 390 px browser layout pass. No reports, scores snapshot, model behavior or headline text benchmark results changed; no commit.

- **Done — Codex HF config, 2026-09-28:** omitted optional null task_type in local and published adapter config. PEFT configuration/class/state/logits remain identical in a tiny CPU check; weight blobs unchanged. HF page warning cleared. Publication evidence: `reports/releases/selfjev_4b_config_2026-09-28/publication.json`. No benchmark changes.

- **Prepared — Codex README, 2026-09-28:** root README redesigned with website branding, generated SVG banner, current report-backed results, public releases and quickstart. GitHub rendering, browser layout, 32 local links and mocked SDK checks pass. Awaiting user choice on commit/push; no benchmark changes.

- **Done — Codex website benchmarks, 2026-09-28:** main charts compare current SelfJev and Jev; historical runs stay in archive. Fixed missing Jev AI-review result using the audited model-card data (92.5%, vs SelfJev 93.1%). Build/link checks and browser tab verification pass; no benchmark results changed.

- **Done — Codex website HF links, 2026-09-28:** verified and linked public adapter, merged model and Decision Bench on homepage/research/footer/docs; corrected stale unpublished wording. Dataset suite scope is explicit. Build, 476 link checks and mobile verification pass.

- **Done — Codex website examples, 2026-09-28:** animated tree now uses a duplicate-charge message with binary refund, multiclass team and multilabel topic decisions; 1/2/3 candidate branches, selected answers and typed output. Illustrative only, no model run. Build/link checks and desktop/mobile verification pass.

- **Done — Codex website animation, 2026-09-28:** animated SVG tree, pause/reduced-motion support and mobile layout implemented. Added use-case fine-tuning and sourced context specifications: Jev 32K per path / 64K request; Qwen base 262,144; SelfJev default 32,768, full window unvalidated. Website build, 432 link checks and browser verification pass. No new model runs or benchmark changes.



- **Done — Codex website architecture, 2026-09-28:** removed repeated model-version commentary from website hardware copy; provenance remains in linked methodology and raw reports. Added the shared-prefix tree illustration to the homepage and architecture guide. Production/export checks and mobile layout pass; no benchmark numbers changed.




| idea | why | cost | status |
|---|---|---|---|
| **Images v2: diverse human-labelled questions for transfer.** VQAv2 yes/no, A-OKVQA multiple choice, GQA, COCO objects (multilabel, look-alike distractors), all CC BY / Apache, + replayed text (`LONG_FRAC` 1/3). Measure on `eval_images_heldout` (7 sets never trained on) + `eval_images_v1`'s 4 held-out sets; text gate as images v1 | images v1 (fixed-label classification) learnt its 6 tasks but moved unseen tasks only 83.5 -> 84.3 (p = 0.31) | data free; ≈ 4 h L40S ≈ $7.5 | **done, not adopted** (Claude images, 2026-09-30): unseen image tasks +0.8 (held-out QA 88.7 -> 89.5, p = 0.27; v1's held-out 84.3 -> 85.1, p = 0.38), but eval2 96.13 -> 95.23 (p = 0.006) vs the default. JOURNAL 2026-09-30 19:50 |
| **Images v1: does image skill generalize, with text kept?** One mixed fine-tune from `selfjev-4b` (lr 5e-5): ~11K image questions from 6 licence-safe datasets (pets, fashion, beans, rice, EuroSAT, TrashNet) + as many text questions replayed from selfjev-4b's own training rows (Jev soft targets). Frozen test: ~100 photos per training dataset + 4 held-out datasets never trained on (hurricane damage, snacks, indoor scenes, painting style). Ship gate: eval2 / eval_llm / dev benchmark not significantly below `selfjev-4b` (paired McNemar), else a separate image model | the pets-only fine-tune (no text replay) cost eval2 -0.4; sequential image-then-text training forgets | data free; ≈ 2.6 h L40S ≈ $5 | **done** (Claude images, 2026-09-30): trained image sets 70.4 -> **94.2%** (p = 2e-69), held-out image sets 83.5 -> 84.3 (p = 0.31: no transfer), eval2 95.68 -> **96.13**, eval_llm 93.13 -> 92.49, dev 83.78 -> 84.07 (none significant: gate passes). `runs/images_v1/adapter`, `reports/images_v1/`, JOURNAL 2026-09-30 02:05. **The default since 2026-09-30 08:30** (`weights/selfjev_4b_vision`, HF `Jwuthrich/selfjev-4b-vision`) |
| **Images as the state** (`state` = a `data:image/...` URL, Prem's convention): the vision tower of the Qwen3.5-4B checkpoint (untouched by the LoRA) encodes the image once as the tree's root, 3D M-RoPE positions, questions branch as for text; first measure zero-shot `selfjev-4b` vs the base on a frozen image test set with human labels | Jev takes no images (TypeSafe docs: text / JSON only), so this is a capability Jev lacks | code ≈ half a day; eval ≈ 1 h GPU | **done end to end, one dataset** (Claude images, 2026-09-29): engine, API, fine-tuning endpoint and `eval_pets` set built; 163 ms per image request (text 136 ms) on an L40S; zero-shot `selfjev-4b` 78% vs bare base 73% on 100 pets questions; fine-tuned on 2,220 pet photos **90%** (cat breed 42 -> 54 of 61, p = 0.002), eval2 95.68 -> 95.28 (p = 0.19). Open: more datasets ([image_datasets.md](image_datasets.md)) mixed with text rows, the full 1,853 questions (JOURNAL 2026-09-29 20:40) |
| **Parallel-readout branch**: one branch per question, every option listed, then a verdict block with one yes/no readout per option and one for `none`; listwise softmax / per-readout sigmoid ([memo](../reports/jev_hypothesis_2026-09-25.md) A) | the shape Jev's disclosures and billing imply; keeps the option-list gain, fixes what pointers lost, 1 prompt per question on vLLM, permutation-invariant `none` | code ≈ 1 day + ≈ $12 GPU | proposed (fork 2, 2026-09-25), awaiting OK |
| Calibration objective (Brier term / soft targets) in the same run, reporting graded share, confidently-wrong count and ECE ([memo](../reports/jev_hypothesis_2026-09-25.md) B) | Jev's errors are hedged (7 of 55 with margin ≥ 0.4, ours 26 of 110); a proper-scoring loss is RLCD without the RL | none beyond the run above | soft targets **done** separately (2026-09-26, conclusion 15: Jev's targets cut confident mistakes 30 → 14, Brier −9%, and are in `selfjev-4b`); a Brier term inside the parallel-readout run is untried |
| Cascade / ensemble in serving: combo answers unless its margin < tau, else the 50/50 average with the 27B; tau chosen on validation ([eval2/ensembles.md](../reports/eval2/ensembles.md)) | +0.3–0.9 on eval2 with nothing trained, on top of `qwen35_4b_tree` 95.6: average with `tree_4b_combo` 95.9, with the 27B 96.3, with both 96.5; cascade to the 27B average at 7% deferral 96.1 | $0 to decide; 27B compute on ≈ 10% of questions | **parked** (cleanup 2026-09-27): needs the archived adapters (`qwen35_4b_tree`, `tree_4b_combo`), the teacher's code and `scripts/ensemble_eval2.py`, all at tag `archive/pre-cleanup-2026-09-27`; `selfjev-4b` alone scores 95.8 |
| Prefix-LM tree: full attention over the state, causal branches ([memo](../reports/jev_hypothesis_2026-09-25.md) E) | late exceptions and dates cannot reshape early state tokens under a causal mask | ≈ $5, after the parallel readout; no vLLM mask for it | unclaimed |
| **RLCD from the best model**: `pjev rlcd --init weights/qwen35_4b_tree` (that adapter is now at the archive tag) on the training data, compared on eval2 for accuracy, Brier, ECE and confidently-wrong decisions | Jev's errors are hedged; ours were confidently wrong 4× as often per error; RLCD rewards calibrated probabilities (tests show it learns base rates) | ≈ 4 h L40S ≈ $10 | **done, no gain** (fork, 2026-09-25): on fresh questions accuracy 95.63 vs 95.58 (p = 1), ECE 0.0096 vs 0.0051, confident mistakes 34 vs 30; a same-data fine-tune control is neutral; on seen questions it overfits. Next: a reward that carries more than the label. JOURNAL 23:45 |
| **RLCD with Jev soft targets on all data** vs a plain fine-tune on the same targets (A / B), both from `qwen35_4b_tree`, 71,974 non-test questions of `data/all.jsonl.gz`, target 0.5 × label + 0.5 × Jev | hard labels cannot say "be less sure"; Jev hedges on 15% and disagrees on 8% of these questions | ≈ $36 (two L40S, ≈ 8 h) | **done** (fork, 2026-09-26, JOURNAL 09:10): B (fine-tune) eval2 95.73 vs 95.58 (p = 0.74), confident mistakes 30 → 14, Brier 0.0480 → 0.0438; A (RLCD) 95.43, 22, 0.0446; A vs B p = 0.18. Dev benchmark flat. |
| **C: RLCD with a confident-mistake cost** (`confident_miss=5`) from B's result, same data | the one reward a fine-tune cannot express; Jev's edge is hedged mistakes | ≈ $19 (L40S, ≈ 8 h) | **done** (fork, 2026-09-26, JOURNAL 15:15): eval2 95.68 (vs B p = 1), confident mistakes 14 → 8 (Jev 7), dev benchmark 75 → 48 (Jev 253), ECE 0.043 (Jev 0.041); Brier worse (0.0518 vs B 0.0438). |
| **Retrain from scratch with Jev soft targets on everything** (80,093 non-test questions incl. `llm_multilabel_v1` and `numdate_neg_v1`, new LoRA r64, lr 2e-4, target 0.5 × label + 0.5 × Jev) | B's Jev targets halved confident mistakes but, as a gentle update, barely moved multilabel (+0.2); the new batches target the audit's gaps (distractors, multi-positive, double negation, numbers, dates) | ≈ $18 (L40S, ≈ 7.7 h) | **done** (fork, 2026-09-26, JOURNAL 21:25): eval2 95.78 (p = 0.70 vs `qwen35_4b_tree`), eval_llm 93.13 vs 82.14 (Jev 92.49), dev benchmark 83.75 vs 84.44 (p = 0.13, all on hf_emotions_multilabel: Jev's targets). Candidate new best. Promoted to `selfjev-4b`. Soft-weight 0 on hf rows: dropped by the user (2026-09-27). |
| **Targeted batch 2: several correct answers, distractors, numbers** (`mpos_distr_num_v1`, Luna writer, blind Astra judge; test-diagnosis-motivated: the eval2 audit) | on eval2 `selfjev-4b` still errs far more than Jev on multi_positive (29 vs 13), distractor (29 vs 14) and numeric (28 vs 18) | ≈ $19 | **data done** (fork, 2026-09-27, JOURNAL 01:20, $19.81): 3,645 verified questions (writer = judge 95.6%, moderation 0 of 1,671 texts, Jev 94.8%), in `data/all.jsonl.gz` (93,237 q). Retrain **done, worse** (`selfjev_4b_v2`, fork, JOURNAL 2026-09-27 11:20, ≈ $21.46): eval2 95.38 vs 95.78 (33 / 41, p = 0.42), dev benchmark 83.55 vs 83.75 (p = 0.60), eval_llm 90.49 vs 93.13 (9 / 34, p = 0.0002); not promoted. The eval engine is ruled out (JOURNAL 11:55), the new training code too (a rerun of `selfjev-4b`'s data: eval2 95.08 vs 95.78 (28 / 42, p = 0.12), dev benchmark 83.81 vs 83.75 (p = 0.92), eval_llm 91.97 vs 93.13 (16 / 27, p = 0.13), JOURNAL 22:25): the drop is run-to-run noise plus, not significantly, batch 2. |
| **Qwen3.5 many-question serving**: time `TreeServer` on a GPU first (`selfjev bench`; against Jev with `scripts/latency_sweep.py` from the archive tag), then route requests by question count (vLLM for 1–2 questions, `TreeServer` for more), or patch vLLM to checkpoint the DeltaNet state at the shared-prefix junction | vLLM: 454–1,138 ms for 16 questions vs 163–424 for the Qwen3 tree (JOURNAL 2026-09-25 18:05) | timing ≈ 1 h L40S ≈ $2.50; routing ≈ half a day; the vLLM patch more | **timing done** 2026-09-30 (Claude qsweep, [summary](../reports/bench/selfjev4b_qsweep_summary.md)): `TreeServer`, 1–50 questions × 512–32K tokens, L40S, 2K text, 3 options: 300 ms for 10 questions and 484 for 25, against 908 ms for 16 on vLLM (2026-09-25), so routing could only help for 1–2 questions; routing and the vLLM patch unclaimed |
| **Qwen3.5-4B with a real tree in training** (`qwen35_4b_tree`): the text once per state with gradients through copied DeltaNet states, so training texts up to 8K instead of 2K (the combo run dropped 18.5% of its data) | `qwen35_4b_combo` tied the best (94.5) while training on full sequences ≤ 2K | code + ≈ $15–20 L40S | **done** (fork, 2026-09-25): `qwen35_4b_tree` eval2 **95.6**, best (vs both 94.5 models p ≤ 0.04; Jev 97.2, 31 / 64); dev 84.4; 4.1 h L40S, ≈ $10.80. See JOURNAL 16:05 |
| Qwen3.5-4B + option lists + round-3 data: the two best recipes combined (`qwen35_4b_r2x64` 93.7, `tree_4b_combo` 94.5) | the Qwen3.5 base leads on multilabel (86.6) and sarcasm; option lists + round 3 added +1.8 on Qwen3 | ≈ $15 L40S | **done** (fork, 2026-09-25): `qwen35_4b_combo` eval2 **94.5**, tied with `tree_4b_combo` (61 / 60, p = 1); +0.8 over `qwen35_4b_r2x64` (p = 0.15); multilabel EM 88.2; dev benchmark **84.3** (vs Jev p = 0.009). ≈ $15.80. Next: a real tree for Qwen3.5 training to lift the 2K cap. See JOURNAL 2026-09-25 06:55 |
| Option pointers: the options numbered once in the question, each leaf only "option k" (~9 tokens per option instead of the full description); the hybrid "score every option cheaply after one deep read" | latency at 16 questions and with many options, without losing the option-list gain | ≈ $4 GPU | **done, dead end on vLLM** (fork, 2026-09-24): eval2 92.0 vs 92.9, dev 82.7 vs 83.5; only 1.0–1.38x faster because vLLM still takes one prompt per option. See JOURNAL 18:25 |
| **Round 3, full run**: `tree_4b_instruct_r2x64` recipe + `data/hardcases_r3.jsonl` (38.6K verified questions) | the first run was stopped at step ≈ 500 of 915; its step-300 checkpoint (90.8 eval2) is not a verdict | ~10 h A10G ≈ $10 | **done** (Jev classifier with Qwen reranker, 2026-09-24 15:35): `tree_4b_instruct_r3`, eval2 **93.3**, old test 82.8. Only +0.6 over the r2x64 control (62 / 50, p = 0.3): diminishing returns from more of the same data. L40S, ≈ $9.25. See JOURNAL |
| T5Gemma 2 corrected full encoder + decoder adaptation on round-2b data | the pilot trained the decoder only (76.8 eval2) | L40S $3.00424/h | **closed** (cleanup 2026-09-27): never rerun; T5Gemma is a dead end (eval2 73.0 / 76.8), code at tag `archive/pre-cleanup-2026-09-27` |
| **Qwen3.5-4B shared-document model**: port `run_challenger.py` + forked native cache from the Codex worktree; `tree_4b_instruct_r2x64` recipe; score dev benchmark + eval2; also Eikos-4B and the Qwen3.5-2B adapter zero-shot on eval2 | Qwen3.5-2B reached 79.9 on round-1 data; linear attention is 1.4–2× faster at 8K tokens | g5.xlarge ≈ 4–5 h ≈ $5, cap $7 | **done 2026-09-24** (SelfJev state of play): `qwen35_4b_r2x64` **93.7** on eval2 (best; vs Qwen3 Instruct r2x64 73 / 53, p = 0.09; vs round 3 p = 0.53; Jev 97.2), old test 83.4; Eikos-4B zero-shot 92.8; Qwen3.5-2B r1 84.3. Slower than the Qwen3 tree in transformers (1.1–1.5×). Next: round-3 data on Qwen3.5-4B, vLLM hybrid prefix cache. JOURNAL 2026-09-24 |
| Distillation variants: 27B teacher on multiclass only, lower weight, r64 student; or a 50/50 ensemble served as is | 50/50 ensemble scores 94.5 on eval2; weight 0.5 on all rows gave nothing | ≈ $3 GPU each | **closed** (cleanup 2026-09-27): distillation dropped (teacher files and code at tag `archive/pre-cleanup-2026-09-27`); the ensemble lives on in the cascade idea above |
| Multilabel with 3–5 positives | multilabel EM is the largest gap to Jev (83.5 vs 94.2); round 3 has 54% of multilabel questions with 3+ positives | ≈ $3 generation + judge | **done**: batch `llm_multilabel_v1` (Synthetic data generation strategy, 2026-09-26), 7,570 verified LLM-oriented multilabel questions with near-miss negatives ($68.96; multilabel training questions 15,776 → 22,579), trained into `selfjev-4b`: multilabel EM eval2 90.1 → 91.4 (Jev 94.2), eval_llm 68.1 → 86.8 (Jev 81.3). More several-correct questions in batch `mpos_distr_num_v1` (retrain running) |
| **Test-failure audit** (blind Opus 5.5 relabel of what our best model or Jev gets wrong, then patterns) | find label errors and real error patterns worth new data | ≈ $10 | **done** (Synthetic data generation strategy, 2026-09-26, $4.92): eval2 failures are real (114 of 119; 1 clear label error `eg-0024-q1`); ours vs Jev real eval2 errors: distractor 33 vs 13, multi_positive 28 vs 13, temporal 28 vs 21, numeric 26 vs 18; dev benchmark 41% label problems. `reports/audit_2026-09-26/AUDIT.md` |
| Temporal / numeric reasoning batch (dates, business days, thresholds, sums with near-miss numbers), Luna + Gemini batch; test-diagnosis-motivated (eval2 audit) | both models' weakest real eval2 errors (ours temporal 28, numeric 26; Jev 21, 18) | ≈ $20-25 | partly done: `numdate_neg_v1` (549 q) and the numeric traps of `mpos_distr_num_v1`; temporal-heavy data still open |
| **Distill from Jev's stored probabilities**: add a teacher term (e.g. KL to `jev.p_yes` / `jev.probs`) to the authored-label loss, training from `data/all.jsonl.gz` | Jev scores 97.2 on eval2 vs our 95.6; its probabilities exist for all 81,473 questions (`jev` field). Jev disagrees with the human labels on 25% of the public-set rows, so weight or skip the teacher there. [TypeSafe's customer agreement §2.3(b)](https://typesafe.ai/legal/mca) restricts use of outputs for model distillation or a similar product. | code + ≈ $10 L40S | **done** (fork, 2026-09-26): `selfjev finetune --soft-weight 0.5` (target 0.5 × label + 0.5 × Jev), rows B and "Retrain from scratch" above; it is `selfjev-4b`'s recipe. The public-set caveat showed on the dev benchmark (−0.7, emotions). **Published on Hugging Face 2026-09-28 at the user’s explicit instruction** after this concern was reported; no contractual exception was established. |
| **LLM-evaluation data, 2K questions per use case**: score, judge, verify, guardrail, jailbreak detection over prompts, reasoning traces and outputs (Jev's own pitch). Training ≈ 11K generated by Luna / Gemini 3.8 Flash / Grok 4.7 / DeepSeek V4 Flash, blind Astra judge; plus a frozen test slice `data/eval_llm.jsonl` (≈ 1K, eval2's writers, two judges) since eval2 has only 3% such texts | only ≈ 6% of round-2/3 texts are LLM artifacts; `eval_agent_output` (dev benchmark, 26 q): tree 61.5 vs Jev 92.3. Training on it ends that family's held-out status | ≈ $82 training + ≈ $19 test slice | **data done** (Synthetic data generation strategy, 2026-09-25/26): after strict label and content-safety passes, `data/hardcases_llm.jsonl` 9,443 q, frozen test `data/eval_llm.jsonl` 946 q, **Jev 92.5%** on it (verify 86.7). $96.38. Baseline `qwen35_4b_tree` 82.1 on `eval_llm`; retrained with the data: `selfjev-4b` 93.1 (2026-09-26). [llm_eval_data.md](llm_eval_data.md) |
| Binary-judgment data with verified answers (numeric, temporal, agent-output grading) | numeric 87.5 vs 92.0, temporal 88.2 vs 89.2 on eval2 (`selfjev-4b`); the agent-output grading family is no longer held out: the LLM-evaluation data (score, judge, verify) is in `selfjev-4b`'s training | generation + blind judge | partly covered: `numdate_neg_v1` and the LLM-evaluation data (in `selfjev-4b`), the numeric traps of `mpos_distr_num_v1` (retrain running); temporal still open |
| Rejection (`none`) as its own decision: permutation-invariant rule over candidate scores; balanced in/out-of-scope training pairs | the round-2 regression was all CLINC over-rejection; the "all options in the question" part is done (`tree_4b_ova`) | data + small code | unclaimed |
| Round-2 mix, remaining parts: `none`-offered-but-wrong intent-like states; subsample hard cases to ≈ 30% of training | the `none` cap (r2b) is done | ≈ $3 GPU + $2 generation | unclaimed |
| Label-free binary bias fix, e.g. contextual calibration (subtract each question's score on an empty text), chosen on validation | SST-2 + BoolQ explain ≈ 60 of the 63 binary answers behind Jev on the dev benchmark (a test diagnosis: confirm on a fresh holdout) | code + ≈ 1 h GPU | unclaimed |
| Calibration policy: temperature separate from thresholds; thresholds for accuracy, validated on a split not used for fitting | the F1 thresholds fitted for `tree_4b` (the `calib/` files, at the archive tag) cost 2.3 points; `selfjev calibrate` fits new files | code only | unclaimed |
| Prompt-template robustness: a random prompt wording per training example; average over 2–4 wordings at eval | learn the task, not the template; master has one prompt (`challenger-state-first-v1`), the old `formatting.PROMPTS` set is at the archive tag | code + one retrain | unclaimed |
| Tree full fine-tune (no adapter) | upper bound for capacity; r64 gave +2.1 on round-1 data | needs code (`selfjev finetune` always trains a LoRA) + ≥ 48 GB GPU | unclaimed |
| Smaller tree student (Qwen3.5-0.8B / 2B) distilled from `selfjev-4b` | speed; the 0.6B Qwen3 stock model reaches only 68.8 on eval2 | code (`selfjev` trains Qwen3.5-4B only) + 1 GPU-day | unclaimed |
| Latency on a fast GPU: vLLM tree on an H100 (bf16 and FP8), same sweep (`scripts/latency_sweep.py`, now at the archive tag) | Jev's flat ~150 ms at 4K tokens × 16 questions needs ≥ 10× an A10G's compute | ≈ $1.20 (p5.4xlarge spot $2.54/h, 28 min) | **done 2026-09-26** (fork 2): server-side 22–82 ms for one question and 58–189 ms for 16 vs Jev 110–134 ms; end to end 10–100 ms behind = network (61 vs 11 ms). FP8 = bf16 in speed and accuracy (eval2 94.48 vs 94.42 vLLM bf16, transformers 94.48). Fully busy 2.1–6.5× cheaper than Jev. The speed gap was hardware. JOURNAL 2026-09-26. Qwen3 tree (`tree_4b_combo`) only: `selfjev-4b` is not timed |
| Tree execution: structured attention kernel | the direct branch mask is done; kernel work remains | code only | unclaimed |
| vLLM path on eval2 (R1 and compact were checked on the dev benchmark only) | confirm serving quality on the target task | ≈ 15 min GPU | **done** (2026-09-25/26): `qwen35_4b_tree` 95.58 through vLLM (= transformers), `tree_4b_combo` 94.53 on an L40S and 94.42 / 94.48 on an H100 (bf16 / FP8). `selfjev-4b` has not been scored through vLLM |
| Stock 4B on round-2 data (`scripts/run_4b_r2.sh`) | control for the tree's round-2 number; the first run was stopped unfinished | ~1 h A10G | **closed** (cleanup 2026-09-27): stock pairs are superseded; script at tag `archive/pre-cleanup-2026-09-27` |
| jina 0.6B follow-ups: 2 epochs (`configs/jina_r2b_e2.json`), r64 + MLP (`configs/jina_r2b_r64.json`), pairwise layout (`scripts/run_jina_followups.sh`) | adapter- or data-limited? | ~1 h A10G each | **closed** (cleanup 2026-09-27): jina is a dead end (eval2 73.3, non-commercial license); code at tag `archive/pre-cleanup-2026-09-27` |
| Score Laya (`pip install laya`, Apache 2.0) zero-shot on eval2 and the dev benchmark, `max_len=8192`, via its Jev-shaped API | the only open competitor with the same interface | ≈ 1 h on a small GPU box (never on the laptop), no API cost | **done 2026-09-30** (Claude competitors): Laya eval2 45.4 (46.9 with max_len 8192), eval_llm 46.4, typed-decisions 36.0. `reports/competitors/` |
| Score our best tree on the public JevBench items; score 2–3 open models (Laya, open-jev-deberta, kev-4b) on eval2 | the only shared yardstick across open Jev-like models | no API cost; GPU time | **done 2026-09-30** (Claude competitors): selfjev-4b-vision JevBench public-231 83.5 / hard 66.7, typed-decisions 66.1, Nimble 13 74.8; 8 open models on eval2 / eval_llm / images. `reports/competitors/matrix.md`, JOURNAL 2026-09-30 14:15 |
| DecisionBench 1.0 full run (23,900 rows) for selfjev-4b-vision, then a JevBench board request (outward: user's OK) | tokenizer fixed 2026-09-30 (50x at 255 options); the tree engine still does only ≈ 21 rows/min on 60–120-option tasks | ≈ 7 h L40S (≈ $16) from the saved partial rows, or a faster engine | **dropped** by the user 2026-09-30 (too slow on many-option tasks; 3,460 / 23,900 rows kept in `reports/competitors/decisionbench/`) |
| Quantized build for 8 GB GPUs (bitsandbytes 8bit / NF4 of the merged selfjev-4b-vision), Decision Bench vs bf16 + memory by text length | a user asked for it (SELA-003); bf16 weights are ≈ 9 GB | ≈ $4 (2 × g5.xlarge, GPU memory capped at 7.2 GiB) | **claimed 2026-09-30** (Claude quant) |
| Training batches for planted wrong verdicts and JSON-record reconciliation (`verdict_json_v1`, Luna) + typed-decisions train re-judged (`typed_decisions_train_v1`) | JevBench hard misses are 78 % the planted surface answer; typed-decisions gap is mostly invoice JSON cross-field checks (2026-09-30 diagnosis of public benchmarks, reports/competitors/README.md) | ≈ $32 API, then a retrain | **claimed** (Claude competitors, 2026-10-01) |
| Fresh final test set (new authors, templates and documents) | both current test sets have informed decisions | ≈ $40 API | unclaimed |
| GLiClass-Instruct / hybrid backbones | alternatives from the strategy memo | research | deferred |

## Done ideas

- **Done — Codex dataset release, 2026-09-28:** [SelfJev Decision Bench](https://huggingface.co/datasets/Jwuthrich/selfjev-decision-bench) publishes all 3,657 questions across the three authored frozen suites with original labels, provenance, Parquet/JSONL, data card and strict scorer. All uploaded files verified; existing results unchanged. Evidence: `reports/releases/decision_bench_2026-09-28/`. Reuse license awaits the user's selection.

- **Done — Codex website, 2026-09-28:** interactive A10G/L40S/H100 historical latency comparison on the main site, with a separately labeled current-model M5 Pro MPS run (8/512 tokens × 1/16 questions). Ten warmed local samples per cell; [raw report](../reports/latency/mac_m5_pro_selfjev4b.json) and `scripts/bench_local_mps.py`; $0. Current-model NVIDIA latency and a supported Mac server remain open.

- **Done — Codex HF merge, 2026-09-28:** published [full SelfJev-4B merged weights](https://huggingface.co/Jwuthrich/selfjev-4b-merged), commit `aed18d68e951f3cbbb84495c931f321fd5e03f10` (9.32 GB). Verified all 738 tensors, 152 merged targets, two synthetic GPU cases and public file hashes. This is artifact validation, not a new benchmark. [Release evidence](../reports/releases/selfjev_4b_merged_2026-09-28/README.md); source-adapter headline scores unchanged.

| idea | result | where |
|---|---|---|
| Latency and architecture visuals on HF | **Done 2026-09-28:** dedicated prefix-tree diagram, archived NVIDIA and current MPS latency figures/tables, raw samples and recomputed medians. Both cards publicly verified; no inference or weight changes; $0 | `scripts/docs/model_card_figures.py`, `weights/selfjev_4b/assets/latency-data.json`, JOURNAL (Codex HF visuals) |
| Reuse visual model card on merged release | **Done 2026-09-28:** same five figures and data; merged serving instructions and refreshed checksum manifest; all 17 files publicly verified, model artifacts unchanged; $0 | [Merged HF card](https://huggingface.co/Jwuthrich/selfjev-4b-merged), `scripts/docs/build_merged_model_card.py`, JOURNAL |
| Visual Hugging Face card and comparison figures | **Done 2026-09-28:** five original figures; 11 adapted public datasets, internal suites, seven-system size comparison, architecture and research path; 18 hashed inputs, public bytes verified, no new inference; $0. S1Bench remains unmeasured. | [HF card](https://huggingface.co/Jwuthrich/selfjev-4b), `scripts/docs/build_model_card.py`, JOURNAL (Codex HF card) |
| Publish under new Hugging Face account | **Done 2026-09-28:** `Jwuthrich/selfjev-4b`, four release files publicly readable and verified; model card points to the new account; original copy retained; $0 | [Model](https://huggingface.co/Jwuthrich/selfjev-4b), JOURNAL (Codex HF upload) |
| Publish SelfJev-4B weights on Hugging Face | **Done 2026-09-28:** user explicitly directed publication after the reported contractual concern; adapter, configuration, manifest and model card uploaded; anonymous visibility and SHA-256 verified; $0 | [https://huggingface.co/JulienHeysam/selfjev-4b](https://huggingface.co/JulienHeysam/selfjev-4b), `weights/selfjev_4b/README.md`, JOURNAL |
| Theme-colored website code examples | **Done 2026-09-28:** shell, Python and JSON syntax colors, including JSON keys inside curl bodies; original source preserved across all 20 docs examples; production build/link checks and browser inspection passed, $0 | `website/lib/highlight.tsx`, JOURNAL (Codex syntax) |
| Explain self-hosted API keys and audit HF release | **Done 2026-09-28:** operator-chosen server key and client bearer flow documented; AWS-generated key explained; TypeSafe restriction found, so current adapter upload held pending rights clearance; local model-card draft prepared, $0 | `docs/api.md`, `website/content/api.md`, `weights/selfjev_4b/HF_CARD_DRAFT.md`, JOURNAL (Codex API/HF) |
| Visitor-focused website language and local refresh | **Done 2026-09-28:** task-based score explanations; plain-language architecture, examples and experiment lessons; expandable methodology/archive; Next.js Fast Refresh verified on port 3000; build, links and responsive UI checked, $0 | `website/README.md`, JOURNAL (Codex website) |
| Next.js marketing and usage docs | **Done 2026-09-27:** `website/`, static product/research site + ten usage guides; scores from reports, archived latency separated from current engine, CPU support limitations documented; build/links/browser checked, $0 | `website/README.md`, JOURNAL (Codex website) |
| Frozen target-task test set (eval2) | 1,991 q / 647 states, 3 authors, 2 blind judges (96.2% kept), Jev 97.2%, $32.72 | `data/eval2/REVIEW.md` |
| Tree + higher LoRA capacity (r64; r16 + MLP) | dev benchmark flat; eval2 +2.1 / +1.2 | `reports/curve/summary.md` |
| Combine round-2b data with r64 / r64 + MLP | 90.3 / 91.3 vs 90.6 | `reports/curve/tree_4b_r2b_r64*` |
| Instruct base + round-2 data + r64 | **92.7**, best so far | `reports/tree_4b_instruct_r2x64` |
| Full candidate bank in the question ("all options") | eval2 91.6 vs 90.6, dev benchmark 82.6 vs 81.2 | `reports/tree_4b_ova` |
| Round-2 `none` cap at 10% | CLINC back to 92.0, dev benchmark 81.2, eval2 90.6 | `reports/tree_4b_r2b`, `scripts/rebalance_nota.py` (archive tag) |
| Round-3 training data | 38,628 verified questions, ≈ $280 | `data/hardcases_r3/review/REVIEW.md` |
| 27B teacher: validation, eval2, training-split scores, distillation | complementary, but no gain from KD at 0.5 | `reports/teacher/`, `reports/tree_4b_ova_kd` |
| Direct branch-mask construction, vLLM path, `--merge` | scores unchanged; vLLM 1.3–2× faster on an A10G; merge 11–22% faster end to end | `reports/latency_optimization_2026-09-24/`, JOURNAL 2026-09-23 21:10 |
| vLLM quality check on the dev benchmark | R1 vLLM 81.53 vs merged HF 81.50 | `reports/latency_optimization_2026-09-24/` |
| Compact tree format | failed the 15% speed gate | `reports/latency_optimization_2026-09-24/conclusions.md` |
| Architecture review after latency and eval2 | proposed T5Gemma 2; superseded when the earlier T5Gemma run was found | `reports/architecture_next_2026-09-24.md` |
| Integrate the latency/compact experiment into `master` | code, reports and weights moved; 16 tests pass | `reports/latency_optimization_2026-09-24/integration.json` |
| Docs site and cleanup | Zensical site from `docs/`, README rewritten, this file restructured | [JOURNAL 2026-09-24](JOURNAL.md) |
| Repo cleanup and the product | one model (`selfjev-4b`); the `selfjev` package with an SDK, a server with Jev's API and fine-tuning jobs, `selfjev deploy aws`; every other model's code, weights and one-off scripts at tag `archive/pre-cleanup-2026-09-27`; the old `runs/<name>/` folders deleted, training logs kept in `reports/train_meta/` | [JOURNAL 2026-09-27 01:40](JOURNAL.md), [API](api.md), [deploy](deploy.md) |

## Where things are

| what | where |
|---|---|
| formatted findings, leaderboard, models, data, speed | the docs site: `docs/*.md`, built with Zensical (see [README](../README.md)) |
| the product: package, SDK, server, deployment, fine-tuning | `src/selfjev/` (CLI `selfjev`), [README](../README.md), [API](api.md), [deploy](deploy.md), [fine-tune and RLCD](finetune.md); the `selfjev-4b` recipe on a GPU box: `scripts/train/selfjev_4b.sh` |
| tree scorer: design, results, speed, reproduce | [tree_model.md](tree_model.md), the Qwen3.5 tree `src/selfjev/engine/tree.py`; the Qwen3 tree at tag `archive/pre-cleanup-2026-09-27` (`src/personal_jev/tree.py`, `train_tree.py`, `vllm_tree.py`, `configs/tree_4b*.json`, `scripts/run_tree_combined.sh`: the `tree_4b_combo` recipe) |
| custom cross-attention model | [custom_model.md](custom_model.md), `reports/custom_diagnostics/`; code, configs and calibration files at tag `archive/pre-cleanup-2026-09-27` |
| jina and T5Gemma challengers | [jina_model.md](jina_model.md), [challengers.md](challengers.md), `reports/t5_round2b_2026-09-24/`; code at tag `archive/pre-cleanup-2026-09-27` |
| learning curves (data volume, epochs, per-task, base model, capacity) | [reports/curve/summary.md](../reports/curve/summary.md); the configs (`configs/curve/`) and pipeline scripts (`scripts/run_curve.sh`, `scripts/summarize_curve.py`) at tag `archive/pre-cleanup-2026-09-27` |
| eval2 | `data/eval2.jsonl`, `data/eval2/REVIEW.md`, [reports/eval2/summary.md](../reports/eval2/summary.md), `selfjev eval`, `scripts/eval/eval2_summary.py` |
| eval_llm | `data/eval_llm.jsonl`, `data/eval_llm/REVIEW.md`, [llm_eval_data.md](llm_eval_data.md), reports in `reports/<run>/eval_llm/` |
| reviews and strategy | `reports/review_2026-09-23.md`, `reports/deep_review_2026-09-23/`, `reports/strategy_2026-09-23/`, `reports/tree_review_2026-09-23/review.md`, `reports/architecture_next_2026-09-24.md`, `reports/jev_hypothesis_2026-09-25.md`, the test-failure audit `reports/audit_2026-09-26/AUDIT.md` |
| Jev comparison (cached API answers) | `reports/external/`, `scripts/eval/compare_external.py`, failures in `reports/external/failures.md`; Jev's answer to every question of `data/all.jsonl.gz` in `data/jev/predictions.jsonl` (`scripts/data/jev_predictions.py`) |
| latency | `reports/bench/`, `reports/latency/`, `reports/latency_optimization_2026-09-24/`; `selfjev bench` on master, `scripts/latency_sweep.py` (the side-by-side sweep against Jev) at the archive tag |
| data: sources, splits, labeling policy | [data.md](data.md); briefs `data/eval/BRIEF.md`, `data/synthetic/BRIEF.md`, `data/hardcases/BRIEF.md`; builders `scripts/data/build_*.py`; the dataset list of `data/all.jsonl.gz` `src/selfjev/data/catalog.py` |
| round-2 and round-3 hard cases, and the batches since | [hardcases_round2.md](hardcases_round2.md), `scripts/data/gen_hardcases.py`, `scripts/data/judge_hardcases.py`, `scripts/data/grow_batch.sh`, `data/hardcases*/review/`, `data/batches/` |
| paid API clients (OpenRouter, OpenAI), Jev and blind-judge requests | `src/selfjev/data/providers.py`, used by `scripts/data/` and `scripts/eval/` |
| trained weights and training metadata | `weights/selfjev_4b` (Git LFS, `model.json`), the only adapter on master; `qwen35_4b_tree` and `tree_4b_combo` at tag `archive/pre-cleanup-2026-09-27`; every run's training log in `reports/train_meta/<run>.json` (`runs/a/b` saved as `a__b.json`); the other adapters were never in git, and the old `runs/<name>/` folders were deleted on 2026-09-27 |
