---
hide:
  - navigation
---

# Leaderboard

## eval2: the target task

1,991 authored questions ([how it was built](data.md#eval2-the-frozen-target-task-test-set)). This is the benchmark
that decides between models.

<div class="acc-chart" style="--ref: 97.2" role="img" aria-label="eval2 accuracy by model; Jev scores 97.2%">
  <div class="acc-head"><span>Jev 97.2</span></div>
  <div class="acc-row" title="tree_4b_instruct_r2x64: 92.7% on eval2">
    <span class="acc-label">Tree, Qwen3-4B-Instruct, r64, round-2b data</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 92.7"></span></span>
    <span class="acc-value">92.7</span>
  </div>
  <div class="acc-row" title="tree_4b_ova: 91.6% on eval2">
    <span class="acc-label">Tree, Reranker-4B, all options in question</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 91.6"></span></span>
    <span class="acc-value">91.6</span>
  </div>
  <div class="acc-row" title="tree_4b_r2b: 90.6% on eval2">
    <span class="acc-label">Tree, Reranker-4B, round-2b data</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 90.6"></span></span>
    <span class="acc-value">90.6</span>
  </div>
  <div class="acc-row" title="tree_4b_instruct: 88.1% on eval2">
    <span class="acc-label">Tree, Qwen3-4B-Instruct, round-1 data</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 88.1"></span></span>
    <span class="acc-value">88.1</span>
  </div>
  <div class="acc-row" title="lora_4b: 86.5% on eval2">
    <span class="acc-label">Stock pairs, Reranker-4B, round-1 data</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 86.5"></span></span>
    <span class="acc-value">86.5</span>
  </div>
  <div class="acc-row" title="tree_4b: 85.1% on eval2">
    <span class="acc-label">Tree, Reranker-4B, round-1 data</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 85.1"></span></span>
    <span class="acc-value">85.1</span>
  </div>
  <div class="acc-row" title="jina_r2b: 73.3% on eval2">
    <span class="acc-label">jina-reranker-v3.5 0.6B, round-2b data</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 73.3"></span></span>
    <span class="acc-value">73.3</span>
  </div>
  <div class="acc-row" title="t5_r1: 73.0% on eval2">
    <span class="acc-label">T5Gemma 2 1B–1B, round-1 data</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 73.0"></span></span>
    <span class="acc-value">73.0</span>
  </div>
  <div class="acc-row" title="lora_pilot: 68.8% on eval2">
    <span class="acc-label">Stock pairs, Reranker-0.6B, round-1 data</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 68.8"></span></span>
    <span class="acc-value">68.8</span>
  </div>
</div>
<p class="acc-caption">eval2 question accuracy, %. Bars start at 0; the dashed line is Jev. All ours use LoRA.</p>

| run | base | recipe | eval2 | binary | multiclass | multilabel EM | dev benchmark |
|---|---|---|---|---|---|---|---|
| **Jev** (API) | undisclosed | undisclosed | **97.2** | 97.8 | 98.1 | 94.2 | 82.7 |
| **tree_4b_instruct_r2x64** | Qwen3-4B-Instruct-2507 | tree, r64, round-2b data, hard cases not capped per family | **92.7** | 94.6 | 95.4 | 83.5 | 82.7 |
| tree_4b_ova | Qwen3-Reranker-4B | tree, r16, round-2b data, all options in the question | 91.6 | 93.8 | 94.9 | 80.4 | 82.6 |
| Qwen3.8-27B-FP8, zero-shot (teacher) | Qwen3.8-27B | no training | 91.4 | 93.4 | 97.8 | 75.9 | — |
| curve/tree_4b_r2b_r64_mlp | Qwen3-Reranker-4B | tree, r64 + MLP, round-2b data | 91.3 | 93.7 | 94.3 | 80.4 | 82.4 |
| tree_4b_ova_kd | Qwen3-Reranker-4B | as `tree_4b_ova` + 27B soft targets | 91.0 | 92.9 | 95.6 | 78.5 | 82.5 |
| tree_4b_instruct_r3_step300 | Qwen3-4B-Instruct-2507 | round-3 run, stopped; step 300 of 915 | 90.8 | 93.1 | 95.1 | 78.0 | 81.5 |
| tree_4b_r2b | Qwen3-Reranker-4B | tree, r16, round-2 data, `none` capped | 90.6 | 92.9 | 94.1 | 78.8 | 81.2 |
| tree_4b_r2 | Qwen3-Reranker-4B | tree, r16, round-2 data | 90.4 | 92.8 | 95.8 | 75.4 | 80.6 |
| curve/tree_4b_r2b_r64 | Qwen3-Reranker-4B | tree, r64, round-2b data | 90.3 | 92.9 | 94.9 | 75.9 | 81.2 |
| tree_4b_instruct | Qwen3-4B-Instruct-2507 | tree, r16, round-1 data | 88.1 | 91.4 | 92.7 | 72.3 | 80.4 |
| curve/tree_4b_r64 | Qwen3-Reranker-4B | tree, r64, round-1 data | 87.2 | 90.5 | 92.7 | 69.9 | 81.5 |
| lora_4b | Qwen3-Reranker-4B | stock pairs, r16, round-1 data | 86.5 | 89.7 | 91.6 | 70.4 | 80.3 |
| curve/tree_4b_mlp | Qwen3-Reranker-4B | tree, r16 + MLP, round-1 data | 86.3 | 90.0 | 91.9 | 68.1 | 81.6 |
| tree_4b | Qwen3-Reranker-4B | tree, r16, round-1 data | 85.1 | 89.4 | 91.6 | 63.9 | 81.6 |
| T5Gemma 2, decoder-only LoRA (audit) | t5gemma-2-1b-1b | shared encoder, round-2b data | 76.8 | 82.6 | 83.6 | 50.8 | 73.8 |
| jina_r2b | jina-reranker-v3.5 (0.6B) | listwise, round-2b data | 73.3 | 79.8 | 83.5 | 40.1 | 76.6 |
| T5Gemma 2 (`t5_r1`) | t5gemma-2-1b-1b | shared encoder, round-1 data | 73.0 | 79.5 | 79.8 | 45.0 | 75.4 |
| lora_pilot | Qwen3-Reranker-0.6B | stock pairs, r16, round-1 data | 68.8 | 75.7 | 75.7 | 39.8 | 73.5 |
| jina_zeroshot | jina-reranker-v3.5 (0.6B) | no training | 46.5 | 55.8 | 54.5 | 9.4 | — |

- Sources: [reports/eval2/summary.md](../reports/eval2/summary.md) (generated by `scripts/eval2_summary.py`) and the
  27B teacher's predictions in `reports/teacher/qwen38_27b_eval2.jsonl`.
- GPT-6 Astra is not scored on eval2: it was one of the two judges that decided which questions were kept.
- "Round-1 data" is the 10,112-question mix (public sets + synthetic); round 2 adds about 10K verified hard cases
  ([data](data.md)).

??? note "All eval2 slices: type, tier, author, text length, trap, paired tests (generated)"

    --8<-- "reports/eval2/summary.md"

## Dev benchmark: the original test split

3,471 questions: 3,300 from public datasets (1,800 of them from families never trained on) and 171 authored. Frontier
models top out at 86% here because of public-label noise, so it separates small models from large ones but not good
models from each other. Selected rows:

| model | question acc % | binary AUROC | multiclass macro-F1 % | multilabel EM % | binary ECE |
|---|---|---|---|---|---|
| GPT-6 Astra (reasoning low) | **85.8** | 0.971 | **95.3** | **55.8** | 0.050 |
| Jev | 82.7 | **0.981** | 91.6 | 40.1 | **0.045** |
| tree Instruct-4B, r64, round-2b data | 82.7 | 0.965 | 88.0 | 52.9 | **0.045** |
| tree Reranker-4B, round-1 data | 81.6 | 0.953 | 89.7 | 51.7 | 0.077 |
| stock 8B + LoRA | 80.7 | 0.945 | 88.7 | 48.0 | 0.051 |
| stock 4B + LoRA | 80.3 | 0.945 | 86.2 | 47.7 | 0.056 |
| stock 0.6B + LoRA | 73.5 | 0.863 | 82.3 | 31.1 | 0.066 |
| stock 8B, untrained | 66.2 | 0.658 | 86.5 | 10.2 | 0.364 |
| stock 4B, untrained | 62.8 | 0.604 | 83.4 | 2.0 | 0.357 |
| stock 0.6B, untrained | 61.0 | 0.605 | 79.6 | 1.2 | 0.384 |

Per-family tables for these models: [stock reranker](stock_model.md) and [tree scorer](tree_model.md). Jev and GPT-6
Astra answers are cached in `reports/external/`, so reruns cost nothing.

### Every run (generated)

Written by `uv run python scripts/ledger.py` into the [experiment ledger](experiments.md); sorted by eval2, then by the
dev benchmark.

--8<-- "docs/experiments.md:ledger"
