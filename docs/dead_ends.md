# What didn't work

Negative results, so nobody pays for them twice. The authoritative list, which sessions update, is the *Dead ends*
table in the [experiment ledger](experiments.md#dead-ends-do-not-redo).

!!! warning "Measured on the dev benchmark only? Re-check on eval2"
    The dev benchmark called three levers dead that eval2 later showed to be real: the Instruct base (+3.0), LoRA rank
    64 (+2.1) and MLP targets (+1.2). Anything below marked *dev benchmark* has not been re-scored on the target task.

## Training recipe

| tried | result | measured on |
|---|---|---|
| A second epoch (stock 4B) | 79.8 vs 80.3; the best validation checkpoint is always inside epoch 1 | dev benchmark |
| 8B instead of 4B (stock + LoRA) | 80.7 vs 80.3, p = 0.52, and about 1.5× slower | dev benchmark |
| More of the same data mix | ~1.5 points per doubling | dev benchmark |
| +100 to +3,000 BoolQ training questions | BoolQ 83.3 → 86.7 at best (Jev 90.7); overall unchanged (p ≥ 0.09) | dev benchmark |
| LoRA r64 on top of round-2b data | 90.3 vs 90.6 (p = 0.61): capacity and data overlap | eval2 |
| Distilling the 27B teacher at weight 0.5 | 91.0 vs 91.6 (p = 0.21) | eval2 |
| Astra's verbalized probabilities as soft labels | 98.8% of questions are all ≤ 0.05 or ≥ 0.95: the same as hard labels | data check |
| Round-2 data with `none` over-represented | CLINC 94.7 → 83.3: the model rejects valid intents | dev benchmark |

## Architectures

| tried | result |
|---|---|
| Custom cross-attention model, as specified (frozen backbone + 2 new blocks + heads) | 39.0% on the dev benchmark (stock LoRA 73.5); binary AUROC ≈ 0.5 |
| ... + mixed-label data distilled from the stock 0.6B, frozen or with joint LoRA | 37.7% / 39.7% (p = 0.32 vs the spec): no gain |
| ... + Stage B LoRA on top of the frozen model | no validation gain; stopped at step 390 of 882 |
| ... + MaxSim similarity term + joint LoRA (best variant) | 58.2%, still at chance on yes/no questions |
| jina-reranker-v3.5 (0.6B) with the best data recipe | eval2 73.3 vs 90.6 for the tree 4B |
| T5Gemma 2 1B–1B with a shared encoder | eval2 73.0 (round 1) and 76.8 (round 2b, decoder-only adapter) |

Why the custom model failed is written up in [custom model](custom_model.md#why-the-spec-version-scored-39): it
removed the pretrained yes/no readout and the deep joint reading of text and question, and its heads memorized the
training label sets.

## Inference and calibration

| tried | result |
|---|---|
| Applying the fitted calibration file (F1-maximizing thresholds) to the tree | 81.6 → 79.3% on the dev benchmark: serve with 0.5 thresholds |
| Temperature scaling the untrained model | ECE 0.384 → 0.025 only by squashing every probability toward 0.5 (Brier 0.244) |
| Explicit attention mask in the custom encoder | identical outputs, 1.7–2.2× slower on MPS, loses the fast kernel on CUDA |
| Compact tree format (shorter branches) | 7.4% faster on vLLM (gate: 15%), CLINC 94.7 → 91.7 |
| Direct branch-mask construction | exact scores, but only 967 → 961 ms: attention and matmuls dominate |

## Operations

- **Stopped runs lose everything after the last checkpoint.** The round-3 run was stopped at step ≈ 500 of 915 by an
  unlogged command; step 300 was the last checkpoint saved. The stock 4B round-2 control was stopped to free a GPU and
  never rerun.
- **GPU capacity is not guaranteed.** g6e (L40S), H100, Blackwell and A100 launches failed across regions on several
  days; plan runs for g5 (A10G) and treat faster GPUs as a bonus.
- **Training on a laptop** (MPS) is slow and unsafe for other work: every 4B/8B number comes from AWS, and the rules now
  forbid heavy jobs on the laptop.
