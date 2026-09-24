# Other challengers

Backbones and architectures tried against the 4B tree, and one teacher. None beats it; the teacher is the most
interesting result.

| challenger | idea | eval2 | dev benchmark | verdict |
|---|---|---|---|---|
| *tree Qwen3-Reranker-4B, round-2b data (reference)* | shared-prefix tree | *90.6* | *81.2* | |
| Qwen3.8-27B-FP8, zero-shot | a big model as a teacher | **91.4** | — | matches `tree_4b_ova` (91.6), with different errors |
| Qwen3.5-2B, shared document with forked native cache | linear attention, smaller | not scored | 79.9 (round-1 data) | promising on speed at 8K tokens; needs eval2 |
| T5Gemma 2 1B–1B, shared encoder + decoder branches | pretrained encoder–decoder | 73.0 | 75.4 | 17 points behind |
| jina-reranker-v3.5 (0.6B), listwise | one pass per text, pretrained relevance head | 73.3 | 76.6 | sub-1B ceiling; non-commercial license |
| custom cross-attention on Qwen 0.6B (v1 spec) | encode once, new cross-attention + heads | — | 39.0 / 58.2 | [not competitive](custom_model.md) |

## Qwen3.8-27B as a teacher, and distillation

- **What:** Qwen3.8-27B-FP8 on vLLM, thinking off, zero-shot. The answer probability is read from the next-token
  distribution restricted to the answer tokens ([scripts/teacher_scores.py](../scripts/teacher_scores.py)).
- **Validation** (2,121 questions): 82.4% overall; 69.7% on public sets, 93.2% on authored, 88.1% on Astra-verified hard
  cases. It loses on public-set label conventions and wins on target-task questions.
- **eval2:** 91.4% (binary 93.4, multiclass 97.8, multilabel 75.9), vs 91.6% for `tree_4b_ova`. 112 questions only
  ours gets right, 108 only the teacher (p = 0.84); one of the two is right on 97.0%.
- **Ensemble:** a fixed 50/50 average of the two models' probabilities, nothing fitted, scores **94.5%** (binary 95.7,
  multiclass 98.5, multilabel 85.1).
- **Its probabilities are graded** (23% of values within 0.05–0.95, vs 0.8% for Astra's verbalized ones), so it can
  give real soft targets, unlike the Astra judge.
- **Distillation did not transfer the gain.** `tree_4b_ova_kd` = the `tree_4b_ova` recipe with teacher weight 0.5 on
  the 8,372 target-task rows (gold on the 8,000 public rows): eval2 91.0 vs 91.6 (33 / 45, p = 0.21), dev benchmark
  82.5 vs 82.6. The teacher disagrees with the verified label on 12–20% of rows, and the 0.5 weight pulls toward those
  wrong answers.
- **Untried:** teacher on multiclass only (its strongest type), a lower weight, an r64 student, or serving the
  ensemble directly.
- Cost: validation and training-split scoring on one L40S ≈ $6.20; the distillation run ≈ $2.90.

## T5Gemma 2: a pretrained encoder–decoder with a shared document

The architecture memo ([reports/architecture_next_2026-09-24.md](../reports/architecture_next_2026-09-24.md)) proposed
it as the next pilot: encode the document once with a pretrained encoder, and run each question/candidate through the
pretrained decoder against that shared memory. It had already been tried in an earlier worktree.

| run | data | adapter | eval2 | dev benchmark | L40S latency, 2K tokens × 16 × 3 |
|---|---|---|---|---|---|
| `t5_r1` (historical, rescored) | round 1 | LoRA r16, encoder + decoder, 823 steps | 73.0 | 75.4 | 203 ms (merged tree 4B: 297 ms) |
| `t5_r2b`, decoder-only audit | round 2b | LoRA r16, **decoder only by mistake** | 76.8 | 73.8 | 266.6 ms |
| `t5_r2b_full` | round 2b | LoRA r16, encoder + decoder | no result yet | | |

- **The pilot bug:** the target filter used `model.encoder.layers`, but the native path is
  `model.encoder.text_model.layers`. The adapter had 208 decoder tensors and 0 encoder tensors. A unit test now checks
  PEFT coverage and non-zero gradients on both stacks.
- **Verdict so far:** 14–18 points behind the tree on eval2. Faster than the tree at 2K × 16 × 3 on the same GPU, but
  not by the 2× the promotion gate asked for, and not with acceptable quality.
- Protocol, audits and raw results: [reports/t5_round2b_2026-09-24/](../reports/t5_round2b_2026-09-24/README.md).
  Code: [src/personal_jev/t5_shared.py](../src/personal_jev/t5_shared.py).

## Qwen3.5-2B: linear attention with a forked cache

From the Codex challenger worktree (`reports/challengers/qwen35` there; not in this repo; summarized in the JOURNAL
entry of 2026-09-24 10:42):

- Qwen3.5-2B + LoRA r16 on all its projections (Gated DeltaNet `in_proj_*`/`out_proj` included). The document is
  shared through the model's native cache (recurrent state + KV), forked per branch. Round-1 data only.
- Dev benchmark **79.9%** (tree 4B 81.6, stock 4B 80.3, 0.6B 73.5). 853 steps in 17 min on an L40S. Never scored on
  eval2.
- Speed vs the tree 4B on the same L40S, p50: 512 tokens × 1 question 125 vs 114 ms; 2K × 16 questions 319 vs 339 ms;
  8K × 1 question 394 vs 805 ms; 8K × 16 questions 765 vs 1,050 ms. Linear attention pays off only on long texts; at
  ≤ 2K the MLPs dominate.
- Why it is not in the tree: Qwen3.5 makes 3 of every 4 layers recurrent, which cannot keep sibling branches isolated
  in one packed pass; the forked cache does it in several.
- Next step, claimed and awaiting approval: Qwen3.5-4B with the best recipe ([open questions](next.md)).

## jina-reranker-v3.5 (0.6B, listwise)

Every question/candidate is a passage in one causal context with the text; the score is the cosine between projected
embeddings. Trained with the round-2b recipe: 73.3% on eval2 (tree 4B r2b 90.6%), multilabel exact match 40.1 vs 78.8.
Only 2× faster per question (58 vs 118 ms on an A10G) for 17 points less. License CC BY-NC 4.0.
Full write-up: [jina-reranker-v3.5](jina_model.md).

## Screened, not run

- **GLiClass-Instruct** (~0.4B, joint text/label encoder): its DeBERTa configuration has
  `max_position_embeddings=512`; long texts and several independent questions are not native. Deferred.
- **Open "Jev-like" models on Hugging Face** (Laya, kev, decider, openjev, Eikos-4B, AutoJev-27B): surveyed, not run.
  See [Jev and open alternatives](landscape.md).
