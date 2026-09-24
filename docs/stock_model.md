# Stock reranker + LoRA

The first backend and the baseline for everything else: [Qwen3-Reranker](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B)
scores every (text, question, candidate) triple as its own sequence and reads the `yes` − `no` logit. LoRA adapters
on the attention projections are the only trained parameters: no new head, probe or cross-attention. How the scoring
works: [how it works](how_it_works.md).

!!! abstract "Bottom line"
    - **LoRA matters far more than model size.** 0.6B: 61.0 → 73.5% on the dev benchmark. 4B: 62.8 → 80.3%. 8B:
      66.2 → 80.7%, statistically tied with the 4B (p = 0.52).
    - **The 0.6B is out for quality:** 68.8% on eval2 vs 86.5% for the 4B.
    - **The recipe saturates at 80–81% on the dev benchmark** whatever it is fed: data volume, epochs, base model.
      eval2 later showed that the dev benchmark could not see most gains ([findings](findings.md#evaluation)).
    - Every candidate re-reads the whole text, so many questions over a long text are this design's worst case. The
      [shared-prefix tree](tree_model.md) fixes that at the same quality.

## 0.6B on the laptop (Apple M5 Pro, MPS, 2026-09-22)

Dev benchmark: 3,471 questions, identical for all four models.

| | Qwen 0.6B, untrained | Qwen 0.6B + LoRA | Jev (`typesafe/jev-1.13-20260917`) | GPT-6 Astra (reasoning low) |
|---|---|---|---|---|
| question accuracy % | 61.0 | 73.5 | 82.7 | **85.8** |
| binary accuracy % | 55.3 | 77.8 | 93.5 | **93.8** |
| binary F1 % | 55.8 | 75.1 | 93.2 | **93.4** |
| binary AUROC | 0.605 | 0.863 | **0.981** | 0.971 |
| multiclass accuracy % | 73.3 | 78.3 | 84.6 | **87.0** |
| multiclass macro-F1 % | 79.6 | 82.3 | 91.6 | **95.3** |
| multilabel exact match % | 1.2 | 31.1 | 40.1 | **55.8** |
| multilabel micro-F1 % | 23.6 | 62.9 | 66.3 | **74.0** |
| multilabel label AUROC | 0.679 | 0.882 | 0.890 | **0.940** |
| binary ECE | 0.384 | 0.066 | **0.045** | 0.050 |
| binary Brier | 0.397 | 0.155 | **0.051** | 0.058 |
| multiclass ECE (top-label) | **0.026** | 0.027 | 0.099 | 0.087 |
| multiclass log loss | 0.717 | **0.601** | 2.134 | 0.605 |

Paired exact McNemar tests (questions only one of the two models gets right):

| comparison | fine-tune right | other right | p |
|---|---|---|---|
| fine-tune vs untrained | 605 | 172 | ≈ 3e-57 |
| fine-tune vs Jev | 197 | 516 | ≈ 8e-34 |
| fine-tune vs GPT-6 Astra | 153 | 580 | ≈ 3e-59 |

- Jev often returns hard 0/1 choice probabilities, so its confident misses give it a high multiclass log loss.
- The decisions API has no multilabel type, so Jev multilabel is one `noul` per candidate.
- GPT-6 Astra ran with `reasoning.effort=low`, JSON-schema output and our labeling policy in its system prompt.
- Cost: Jev $0.064 on OpenRouter credit; GPT-6 Astra $19.27 (BYOK). Full tables:
  [reports/external/full/comparison.md](../reports/external/full/comparison.md).

### By family

`heldout_*` families never appear in training. `eval_*` families have 17–32 test questions each, so single-family
differences under about 20 points are noise.

| family | n | untrained | + LoRA | Jev | GPT-6 Astra |
|---|---|---|---|---|---|
| eval_adversarial | 27 | 74.1 | 63.0 | 100.0 | 100.0 |
| eval_agent_output (no training data) | 26 | 30.8 | 46.2 | 92.3 | 100.0 |
| eval_evidence | 17 | 41.2 | 82.4 | 100.0 | 100.0 |
| eval_multilabel | 32 | 12.5 | 34.4 | 100.0 | 100.0 |
| eval_policy | 22 | 31.8 | 40.9 | 72.7 | 100.0 |
| eval_routing | 25 | 48.0 | 76.0 | 100.0 | 100.0 |
| eval_urgency_sentiment | 22 | 40.9 | 54.5 | 95.5 | 100.0 |
| heldout_boolq | 300 | 59.3 | 70.3 | 90.7 | 89.0 |
| heldout_emotion_multiclass | 300 | 51.0 | 56.0 | 57.7 | 62.3 |
| heldout_intent_clinc | 300 | 92.3 | 89.3 | 94.3 | 95.3 |
| heldout_question_type_trec | 300 | 64.3 | 68.0 | 94.0 | 95.3 |
| heldout_sentiment_sst2 | 300 | 50.0 | 76.7 | 96.7 | 97.0 |
| heldout_topic_dbpedia | 300 | 89.3 | 91.7 | 98.0 | 99.0 |
| hf_emotions_multilabel | 300 | 0.0 | 32.3 | 31.7 | 49.3 |
| hf_intent_banking77 | 300 | 89.3 | 92.7 | 95.7 | 96.3 |
| hf_nli | 300 | 56.7 | 89.0 | 92.7 | 93.7 |
| hf_sentiment_tweets | 300 | 54.3 | 66.7 | 64.3 | 68.7 |
| hf_topic_agnews | 300 | 77.3 | 86.7 | 87.3 | 90.0 |

The `eval_*` families were written and blind-verified by Claude Opus. GPT-6 Astra scores 100% on all seven and Jev
92–100% on six, so they separate small models from frontier ones rather than frontier models from each other. On
noisy-label public sets (GoEmotions, TweetEval, dair-ai emotion) every model stays well below 100%.

### Where it fails ([reports/external/failures.md](../reports/external/failures.md))

- The fine-tune misses 919 of 3,471 questions. Jev and GPT-6 Astra both get 480 of those right; all three miss 303, and
  235 of those (78%) are in the noisy-label GoEmotions, dair-ai emotion and TweetEval sets.
- Largest gaps to Jev by hard-case tag, in error-rate points: sarcasm +67, numeric reasoning +56, role reversal +53,
  injection +50, paraphrase +50, distractors +49, lexical overlap +45, long states +44, negation +43, temporal
  reasoning +41. Training closed most of the gap on contradiction (+9) and missing evidence (+3).
- [failures.jsonl](../reports/external/failures.jsonl) lists every miss worst-first. These are **test** questions:
  use them to design new training data, never as training data.

### Calibration

- **Untrained:** binary ECE 0.384. The held-out temperature (T = 21.6) brings it to 0.025, but only by squashing every
  probability toward 0.5 (Brier 0.244, a coin flip is 0.25). Calibration cannot add signal that isn't there.
- **LoRA:** calibrated out of the box (binary ECE 0.066); fitted temperatures 1.16 / 1.27 / 1.05 barely change anything.
- **New families:** calibration fitted in distribution does not transfer: ECE 0.19 on SST-2 and 0.35 on agent-output,
  and multiclass temperature scaling makes CLINC and DBpedia *worse*.

### Training run

- LoRA r=16, α=32, dropout 0.05 on `q/k/v/o_proj`: 4,587,520 trainable of 600M parameters (0.76%). Base in bf16 with
  fp32 adapters and gradient checkpointing; lr 2e-4, 5% warmup, linear decay, 1 epoch.
- Data: 10,112 questions (public datasets capped at 1,600 per family + 2,112 synthetic). 183 optimizer steps in 1.05 h.
- Validation loss 1.129 at step 0 → 0.435 at step 150, the selected checkpoint. The adapter reloads exactly.
- Prompt `task-v1` was chosen on validation only (0.614 vs 0.597–0.609 for the other three), a small margin.
- Config [configs/lora_pilot.json](../configs/lora_pilot.json).

### Speed on the laptop (end-to-end p50, one request at a time)

| request | pairs | fp32 base | bf16 base | fp32 LoRA |
|---|---|---|---|---|
| 512-token text, 1 question × 3 candidates | 3 | 351 ms | **150 ms** | 383 ms |
| 512-token text, 16 × 3 | 48 | 5.4 s | 2.5 s | 6.0 s |
| 2,048-token text, 1 × 3 | 3 | 1.4 s | 0.57 s | 1.5 s |
| 2,048-token text, 16 × 3 | 48 | 23.3 s | 9.6 s | 26.6 s |
| 8,192-token text, 1 × 3 | 3 | 8.6 s | 2.9 s | 9.4 s |
| 8,192-token text, 16 × 3 | 48 | 150 s | 46.7 s | 150 s |
| 16K / 32K-token text, 1 binary question | 1 | 9.1 s / 28.8 s | 2.5 s / 7.3 s | — |

- Latency ≈ pairs × text tokens: throughput is flat per token, and bf16 is 2.3–3.2× faster than fp32.
- **bf16 costs no quality:** 73.7% vs 73.5% in fp32, same AUROC; 43 of 3,471 decisions flip.
- The unmerged adapter adds 8–14% latency; merging it into the weights removes that.

## Scaling up: 4B and 8B (one NVIDIA L40S, 2026-09-23)

| | 0.6B | 0.6B + LoRA | 4B | 4B + LoRA | 8B | 8B + LoRA | Jev | GPT-6 Astra |
|---|---|---|---|---|---|---|---|---|
| question accuracy % | 61.0 | 73.5 | 62.8 | 80.3 | 66.2 | 80.7 | 82.7 | **85.8** |
| binary AUROC | 0.605 | 0.863 | 0.604 | 0.945 | 0.658 | 0.945 | **0.981** | 0.971 |
| multiclass macro-F1 % | 79.6 | 82.3 | 83.4 | 86.2 | 86.5 | 88.7 | 91.6 | **95.3** |
| multilabel exact match % | 1.2 | 31.1 | 2.0 | 47.7 | 10.2 | 48.0 | 40.1 | **55.8** |
| binary ECE | 0.384 | 0.066 | 0.357 | 0.056 | 0.364 | 0.051 | **0.045** | 0.050 |

Full tables, per family and per trap, with paired tests: [reports/scale_comparison.md](../reports/scale_comparison.md).

- **8B + LoRA vs Jev:** wins on GoEmotions multilabel (45.7 vs 31.7), tweet sentiment, AG News and missing-evidence
  cases; loses on agent-output grading (53.8 vs 92.3), policy (50.0 vs 72.7) and the traps (numeric 62.5 vs 93.8,
  temporal 51.7 vs 79.3, role reversal 60 vs 100, injection 70 vs 100).
- **Recipe:** prompt picked per model on validation (4B `answer-v1`, 8B `task-v1`); LoRA r16 on q/k/v/o, 11.8M
  trainable parameters for the 4B (0.29%) and 15.3M for the 8B (0.19%); same 10,112 questions; bf16.
- **Time and cost:** 42 min to train the 4B, 50 min for the 8B; 3.16 instance-hours on one `g6e.xlarge` ≈ $5.89.
- **Precision caveat:** the 0.6B columns ran in fp32 on the Mac, the 4B/8B in bf16 on the GPU.

**Speed on the same GPU** (L40S, bf16, end-to-end p50, adapters not merged):

| request | pairs | 0.6B | 0.6B + LoRA | 4B | 4B + LoRA | 8B | 8B + LoRA |
|---|---|---|---|---|---|---|---|
| 512-token text, 1 × 3 | 3 | 28 ms | 43 ms | 99 ms | 116 ms | 162 ms | 188 ms |
| 512-token text, 16 × 3 | 48 | 421 ms | 608 ms | 1.9 s | 2.4 s | 2.9 s | 3.6 s |
| 2,048-token text, 1 × 3 | 3 | 79 ms | 110 ms | 390 ms | 480 ms | 661 ms | 768 ms |
| 2,048-token text, 16 × 3 | 48 | 1.7 s | 2.4 s | 7.1 s | 9.0 s | 11.0 s | 13.2 s |
| 8,192-token text, 1 × 3 | 3 | 409 ms | 553 ms | 1.8 s | 2.2 s | 2.9 s | 3.3 s |
| 8,192-token text, 16 × 3 | 48 | 6.6 s | 8.8 s | 29.1 s | 35.3 s | 43.8 s | 51.9 s |

Peak GPU memory 1.6 GB (0.6B), 8.7 GB (4B) and 16.9 GB (8B); throughput ≈ 66K, 15K and 9.5K tokens/s. The unmerged
LoRA adds 15–50%.

## Learning curves on the 4B ([reports/curve/summary.md](../reports/curve/summary.md))

Ten more stock 4B LoRA runs, one A10G each (≈ $23 in total), to see what moves the 80.3%:

| lever | runs | dev benchmark accuracy % |
|---|---|---|
| more of the same data (nested 25% / 50% / 100%) | 1 epoch | 77.0 / 78.9 / 80.3 |
| | 2 epochs | 79.1 / 79.1 / 79.8 |
| BoolQ training questions added (+0 / +100 / +300 / +1,000 / +3,000) | BoolQ test | 83.3 / 84.3 / 83.3 / 84.3 / 86.7 (Jev 90.7) |
| | overall | 80.3 / 80.0 / 80.9 / 80.9 / 80.9 |
| base model: Qwen3-4B-Instruct-2507, same pair format | untrained | 71.3 (binary 84.2, AUROC 0.911) vs 62.8 for the reranker |
| | + LoRA | 80.6 vs 80.3 (p = 0.68) |

- Each doubling of the data buys about 1.5 points; 2 epochs of 25% equal 1 epoch of 50%.
- A new task type needs thousands of labeled examples for a few points, and the overall score does not move
  significantly (p ≥ 0.09 for every BoolQ run).
- The Instruct base is much better untrained, above all on yes/no, and identical after LoRA *on this benchmark*. In the
  tree format on eval2 it is +3.0 ([findings](findings.md#architecture-and-base-model)).

## Reproduce

```bash
scripts/run_experiments.sh                      # 0.6B: baseline evals, calibration, LoRA, tuned evals, compare, bench
scripts/run_model.sh 4b Qwen/Qwen3-Reranker-4B 22e683669bc0f0bd69640a1354a6d0aebcfeede5   # same pipeline on a GPU box
scripts/run_model.sh 8b Qwen/Qwen3-Reranker-8B 77d193c791ed757ca307ee72715aa132723da912
uv run python scripts/scale_table.py > reports/scale_comparison.md
scripts/run_curve.sh                            # learning curves, configs in configs/curve/
```
