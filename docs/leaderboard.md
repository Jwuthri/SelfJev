---
hide:
  - navigation
---

# Leaderboard

## eval2: the target task

1,991 authored questions ([how it was built](data.md#eval2-the-frozen-target-task-test-set)). This is the benchmark
that decides between models, with [eval_llm](#eval_llm-llm-evaluation-use-cases) for the LLM-evaluation use cases.

<div class="acc-chart" style="--ref: 97.2" role="img" aria-label="eval2 accuracy by model; Jev scores 97.2%">
  <div class="acc-head"><span>Jev 97.2</span></div>
  <div class="acc-row" title="selfjev-4b: 95.8% on eval2">
    <span class="acc-label">selfjev-4b: Qwen3.5-4B tree, trained from scratch on all 80K questions, texts to 16K, Jev soft targets</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 95.8"></span></span>
    <span class="acc-value">95.8</span>
  </div>
  <div class="acc-row" title="qwen35_4b_tree: 95.6% on eval2">
    <span class="acc-label">Qwen3.5-4B trained with the tree, r64, round-2b + round-3 data, all options in question</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 95.6"></span></span>
    <span class="acc-value">95.6</span>
  </div>
  <div class="acc-row" title="qwen35_4b_combo: 94.5% on eval2">
    <span class="acc-label">Qwen3.5-4B, r64, round-2b + round-3 data, all options in question</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 94.5"></span></span>
    <span class="acc-value">94.5</span>
  </div>
  <div class="acc-row" title="tree_4b_combo: 94.5% on eval2">
    <span class="acc-label">Tree, Qwen3-4B-Instruct, r64, round-2b + round-3 data, all options in question</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 94.5"></span></span>
    <span class="acc-value">94.5</span>
  </div>
  <div class="acc-row" title="tree_4b_instruct_r3: 93.3% on eval2">
    <span class="acc-label">Tree, Qwen3-4B-Instruct, r64, round-2b + round-3 data</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 93.3"></span></span>
    <span class="acc-value">93.3</span>
  </div>
  <div class="acc-row" title="tree_4b_combo_r2: 92.9% on eval2">
    <span class="acc-label">Tree, Qwen3-4B-Instruct, r64, round-2b data, all options in question</span>
    <span class="acc-track"><span class="acc-bar" style="--v: 92.9"></span></span>
    <span class="acc-value">92.9</span>
  </div>
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
| **selfjev-4b vision** (`images_v1`), the default since 2026-09-30 | Qwen3.5-4B | the text release below + 1 epoch on 11.3K image questions (6 datasets) and 11.3K replayed text questions, lr 5e-5; eval_llm 92.5; image test 90.4 | **96.1** | **97.4** | **97.3** | 90.8 | **84.1** |
| **selfjev-4b** (`qwen35_4b_tree_scratch_jevall_`), the text release (default until 2026-09-30) | Qwen3.5-4B | tree, trained from scratch on 79.9K non-test questions of `data/all.jsonl.gz` (texts ≤ 16K, incl. the LLM-evaluation data, `llm_multilabel_v1`, `numdate_neg_v1`), target 0.5 × label + 0.5 × Jev, r64, all options in the question; eval_llm 93.1 (Jev 92.5) | **95.8** | 96.8 | **97.0** | **91.4** | 83.8 |
| **qwen35_4b_tree**, the previous default | Qwen3.5-4B | shared-prefix tree in training (`src/selfjev/engine/tree.py`, texts ≤ 8K: 51.8K q), text shared at inference, r64, round-2b + round-3 data, all options in the question | **95.6** | **96.9** | 96.8 | **90.1** | **84.4** |
| **qwen35_4b_combo** | Qwen3.5-4B | each option trained as a full sequence (no tree in training, texts ≤ 2K: 43.8K q), text shared at inference, r64, round-2b + round-3 data, all options in the question | 94.5 | 96.2 | 95.8 | 88.2 | 84.3 |
| **tree_4b_combo** | Qwen3-4B-Instruct-2507 | tree, r64, round-2b + round-3 data (51.8K q), hard cases not capped, all options in the question | **94.5** | 96.0 | 97.5 | 85.9 | 82.7 |
| **tree_4b_instruct_r3** | Qwen3-4B-Instruct-2507 | tree, r64, round-2b + round-3 data (51.9K q), hard cases not capped | **93.3** | 95.1 | 96.1 | 84.3 | 82.8 |
| **tree_4b_combo_r2** | Qwen3-4B-Instruct-2507 | tree, r64, round-2b data, hard cases not capped, all options in the question (served: merged + vLLM, 93.0) | **92.9** | 94.4 | 95.8 | 84.3 | **83.5** |
| **tree_4b_instruct_r2x64** | Qwen3-4B-Instruct-2507 | tree, r64, round-2b data, hard cases not capped per family | **92.7** | 94.6 | 95.4 | 83.5 | 82.7 |
| tree_4b_combo_ptr | Qwen3-4B-Instruct-2507 | as `tree_4b_combo_r2`, options numbered once, leaves say "option k" | 92.0 | 94.9 | 94.3 | 80.9 | 82.7 |
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

- Sources: [reports/eval2/summary.md](../reports/eval2/summary.md) (generated by `scripts/eval/eval2_summary.py`) and the
  27B teacher's predictions in `reports/teacher/qwen38_27b_eval2.jsonl`.
- GPT-6 Astra is not scored on eval2: it was one of the two judges that decided which questions were kept.
- "Round-1 data" is the 10,112-question mix (public sets + synthetic); round 2 adds about 10K verified hard cases
  ([data](data.md)).
- Only `selfjev-4b`'s adapter is on master (`weights/selfjev_4b`). `qwen35_4b_tree` and `tree_4b_combo` are at tag
  `archive/pre-cleanup-2026-09-27`, with the code of every other architecture (Qwen3 trees, stock pairs, jina,
  T5Gemma, the 27B teacher). All these reports were scored before the 2026-09-27 cleanup, the Qwen3.5 rows by the
  forked-cache engine that `TreeServer` replaced.

??? note "All eval2 slices: type, tier, author, text length, trap, paired tests (generated)"

    --8<-- "reports/eval2/summary.md"

## eval_llm: LLM-evaluation use cases

946 frozen questions about LLM prompts, reasoning traces and outputs (score, judge, verify, guardrail, jailbreak),
written by eval2's authors and kept only when two blind judges agree ([how it was built](llm_eval_data.md)). Scored
so far:

| run | eval_llm | binary | multiclass | multilabel EM |
|---|---|---|---|---|
| **Jev** (API) | 92.5 | **95.1** | **95.3** | 81.3 |
| **selfjev-4b** | **93.1** | 94.3 | **95.3** | **86.8** |
| `qwen35_4b_tree_sft_jevall__last`: `qwen35_4b_tree` + one epoch on Jev's soft targets (incl. the LLM-evaluation data) | 90.1 | 92.8 | 93.1 | 78.0 |
| `qwen35_4b_tree`: never trained on LLM-evaluation data | 82.1 | 83.8 | 88.4 | 68.1 |

`selfjev-4b` vs Jev: 33 / 27, p = 0.52. Sources: `reports/*/eval_llm/report.json`; Jev from
`data/eval_llm/review/jev_answers.jsonl` ([llm_eval_data.md](llm_eval_data.md)).

## Dev benchmark: the original test split

3,471 questions: 3,300 from public datasets (1,800 of them from families never trained on) and 171 authored. Frontier
models top out at 86% here because of public-label noise, so it separates small models from large ones but not good
models from each other. Selected rows:

| model | question acc % | binary AUROC | multiclass macro-F1 % | multilabel EM % | binary ECE |
|---|---|---|---|---|---|
| GPT-6 Astra (reasoning low) | **85.8** | 0.971 | **95.3** | **55.8** | 0.050 |
| Jev | 82.7 | **0.981** | 91.6 | 40.1 | **0.045** |
| `selfjev-4b`: Qwen3.5-4B tree, from scratch on 80K questions with Jev's soft targets | 83.8 | 0.974 | 92.7 | 52.3 | 0.048 |
| Qwen3.5-4B trained with the tree, r64, round-2b + round-3 data, all options in question (`qwen35_4b_tree`) | 84.4 | 0.972 | 92.6 | 59.3 | 0.038 |
| Qwen3.5-4B, r64, round-2b + round-3 data, all options in question | 84.3 | 0.963 | 92.2 | 62.2 | 0.047 |
| tree Instruct-4B, r64, round-2b + round-3 data, all options in question | 82.7 | 0.959 | 89.3 | 57.6 | 0.064 |
| tree Instruct-4B, r64, round-2b data, all options in question | 83.5 | 0.966 | 89.3 | 59.0 | 0.038 |
| tree Instruct-4B, r64, round-2b data | 82.7 | 0.965 | 88.0 | 52.9 | **0.045** |
| tree Reranker-4B, round-1 data | 81.6 | 0.953 | 89.7 | 51.7 | 0.077 |
| stock 8B + LoRA | 80.7 | 0.945 | 88.7 | 48.0 | 0.051 |
| stock 4B + LoRA | 80.3 | 0.945 | 86.2 | 47.7 | 0.056 |
| stock 0.6B + LoRA | 73.5 | 0.863 | 82.3 | 31.1 | 0.066 |
| stock 8B, untrained | 66.2 | 0.658 | 86.5 | 10.2 | 0.364 |
| stock 4B, untrained | 62.8 | 0.604 | 83.4 | 2.0 | 0.357 |
| stock 0.6B, untrained | 61.0 | 0.605 | 79.6 | 1.2 | 0.384 |

Per-family tables for these models: [stock reranker](stock_model.md) and [tree scorer](tree_model.md). Jev and GPT-6
Astra answers are cached in `reports/external/cache/`, keyed by the request body: Jev reruns cost nothing, but GPT-6
Astra's requests changed on 2026-09-27 (`max_tokens` 6000 → 8192), so its reruns miss the cache and pay again.
`selfjev-4b`'s 52.3 multilabel exact match is the emotion-set effect of Jev's targets (finding 1).

### Every run (generated)

Written by `uv run python scripts/eval/ledger.py` into the [experiment ledger](experiments.md); sorted by eval2, then by the
dev benchmark.

--8<-- "docs/experiments.md:ledger"
