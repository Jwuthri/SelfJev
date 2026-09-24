# jina-reranker-v3.5 backend: a 0.6B listwise scorer trained the tree-r2b way

Written 2026-09-24. Code: [src/personal_jev/jina.py](../src/personal_jev/jina.py) (scorer), [train_jina.py](../src/personal_jev/train_jina.py)
(trainer), [tests/test_jina.py](../tests/test_jina.py); config [configs/jina_r2b.json](../configs/jina_r2b.json); GPU pipeline
[scripts/run_jina_gpu.sh](../scripts/run_jina_gpu.sh) via [scripts/aws_jina.sh](../scripts/aws_jina.sh). Weights `runs/jina_r2b/adapter`
(LoRA + projector + `jina_head.json`), reports `reports/jina_zeroshot/`, `reports/jina_r2b/`.

## Bottom line

Trained with the best recipe we have (round-2 hard cases with "none" rebalanced, one epoch, LoRA r=16), the 0.6B jina model
lands where the 0.6B Qwen reranker did, far below the 4B tree, on both test sets:

| | jina v3.5 0.6B (this run) | Qwen3-Reranker-0.6B + LoRA (round 1) | Qwen3-Reranker-4B tree r2b | Jev |
|---|---|---|---|---|
| validation (r2 mix, ≈1,380 q) | 77.4 | — | 86.1 | — |
| old test, 3,471 q | 76.6 (calibrated 75.9) | 73.5 | 81.2 | 82.7 |
| **eval2**, 1,991 q | **73.3** | — | **90.6** | 97.2 |
| eval2 binary / multiclass / multilabel EM | 79.8 / 83.5 / 40.1 | — | 92.9 / 94.1 / 78.8 | 97.8 / 98.1 / 94.2 |
| eval2 simple / hard / very hard | 80.6 / 70.7 / 68.5 | — | 95.2 / 89.9 / 86.5 | 98.5 / 96.7 / 96.5 |

Zero-shot (untrained head set at logit 0 = median cosine): validation 58.6, eval2 46.5. Training: 16,301 questions over 11,774
contexts, 346 steps, 72 min on one A10G (g5.xlarge, $1.006/h; whole job ≈ 1.5 h ≈ $1.60). Adapter reloads bit-exact.

Where it loses most on eval2 vs the 4B tree: multilabel (−39 points), long states (59.7 vs 89.0), distractors (65.0 vs 88.2),
injection (57.6 vs 82.1), role reversal (69.5 vs 93.0), evidence in the middle (66.7 vs 94.7). It is closest on plain
questions with no trap (83.1 vs 96.1) and paraphrase (74.8 vs 83.9).

**Speed, same GPU (A10G, bf16, eval2, 5,254 passages over 647 texts):** jina 58 ms per question vs tree 4B r2b 118 ms
(`reports/jina_r2b/eval2_rerun`, `reports/tree_4b_r2b_gpu/eval2_timing`; the tree scores 90.4 there, bf16-on-CUDA noise vs
90.6). Only 2× faster for 17 points less: the tree's cached-prefix path is already efficient, and jina's prompt carries the
state twice (1.38M input tokens vs 914K).

**License:** CC BY-NC 4.0, non-commercial. Fine for these experiments; it cannot ship in a product without a license from Jina.

## What the model is and how we use it

`jinaai/jina-reranker-v3.5` (pinned `e8a93f33`) is Qwen3-0.6B with hybrid sliding-window (1,024) / full attention and a
listwise "last-but-not-late" readout: passages and the query share one causal sequence, an embedding is read at
`<|embed_token|>` after each passage and at `<|rerank_token|>` after the query, both go through an MLP projector
(1024 → 512 → 512) and the score is their cosine. There are no yes/no logits.

Mapping (format `jina-v1`, the model card's prompt with our instruction):

```
[system prompt of the model card]
I will provide you with N passages ... Rank the passages based on their relevance to query: <state>
<instruct> a passage is relevant only if the query text supports its proposed answer ... </instruct>
<passage id="0">\nQuestion: q1\nProposed answer: A<|embed_token|>\n</passage>
<passage id="1">\nQuestion: q1\nProposed answer: B<|embed_token|>\n</passage>
<passage id="2">\nQuestion: q2\nProposed answer: Yes<|embed_token|>\n</passage>      (binary)
<query>\n<first 1,024 tokens of the state><|rerank_token|>\n</query>
logit = scale · cos(proj(query), proj(passage)) + bias
```

- The state is read once per context however many questions there are (the shared-state property of the tree), every
  passage reads it through all 28 layers, and the pretrained relevance readout is kept. Unlike the tree, passages also
  attend to earlier passages, so candidate order can matter; training shuffles question and candidate order, inference
  keeps request order. Contexts are capped at 64 passages (32 in training) and split beyond that.
- Trained parameters: LoRA r=16 on q/k/v/o (4.6M), the projector (0.8M, saved with the adapter as `modules_to_save`) and
  the two head scalars (`jina_head.json`; scale stays ≈ 9.8, bias ≈ −1.07). Loss = train.grouped_loss (BCE / grouped CE)
  on the logits, same schedule as the tree (lr 2e-4, 5% warmup, linear decay, grad accumulation 2, max_batch_tokens 16K,
  max_length 8192: 225 long questions dropped).
- Validation curve (same mix as the tree runs): 46.6 → 69.6 (step 50) → 72.1 → 73.8 → 74.6 → 76.3 → 77.0 → 77.4 (step 345).
  The tree 4B r2b: 74.4 → 80.6 → 84.9 → 85.4 → 85.8 → 86.1. Jina's late-epoch gains (+0.8 to +1.7 per 50 steps) are the
  same size as the 4B's, so it converges more slowly from a lower start rather than more steeply.

## What could still move it (unclaimed)

- Second epoch, or higher LoRA capacity (r=64 + MLP targets): configs `jina_r2b_e2.json`, `jina_r2b_r64.json`, runner
  `scripts/run_jina_followups.sh`. The 4B gained nothing from a second epoch; a 0.6B backbone with a 5M-parameter adapter
  might be adapter-limited.
- Pairwise layout (query = question + proposed answer, passage = state): closer to the model's pretraining, no sharing.
- Round-3 data (40K questions, in flight elsewhere).

## Reproduce

```bash
uv run pjev classify examples/request.json --jina --dtype bfloat16 --adapter runs/jina_r2b/adapter
uv run pjev eval --jina --dtype bfloat16 --max-length 16384 --adapter runs/jina_r2b/adapter --data data/eval2.jsonl --out reports/jina_r2b/eval2
uv run pjev train-jina configs/jina_r2b.json          # ~70 min on an A10G; ~6× slower on the M5 Pro
bash scripts/aws_jina.sh launch && bash scripts/aws_jina.sh run   # then: log | pull | terminate
uv run python -m pytest -q tests/test_jina.py         # padding invariance + length accounting on the real model
```
