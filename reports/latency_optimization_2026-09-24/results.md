# Measured tree latency and compact-format results

This file is regenerated from saved JSON artifacts. Missing results are pending, not zero.
Server-side timings use a resident model; vLLM cold-prefix calls explicitly clear the prefix cache. No network time is included.

## A10G latency

The vLLM columns here are the original phase-one R1 run. The extended table below compares R1 and compact using the same three cache modes.

| Document tokens | Questions × 3 options | Original HF ms | Optimized HF ms | Compact HF ms | R1 vLLM cold ms | R1 vLLM identical-request ms |
|---:|---:|---:|---:|---:|---:|---:|
| 8 | 1 | 85.61 | 83.01 | 83.49 | 49.87 | 43.13 |
| 8 | 4 | 156.19 | 157.63 | 117.47 | 89.94 | 55.73 |
| 8 | 16 | 525.00 | 521.36 | 331.55 | 267.22 | 135.60 |
| 512 | 1 | 159.66 | 159.51 | 152.74 | 114.50 | 26.38 |
| 512 | 4 | 236.66 | 236.04 | 194.57 | 188.96 | 55.69 |
| 512 | 16 | 607.02 | 607.39 | 414.05 | 401.64 | 105.92 |
| 2048 | 1 | 458.73 | 458.05 | 438.42 | 359.53 | 56.19 |
| 2048 | 4 | 544.38 | 543.95 | 496.55 | 431.30 | 79.81 |
| 2048 | 16 | 966.62 | 960.63 | 743.50 | 696.93 | 186.22 |
| 8192 | 1 | 1777.45 | 1769.85 | 1734.23 | 1419.23 | 96.13 |
| 8192 | 4 | 1903.01 | 1894.82 | 1829.30 | 1556.27 | 176.05 |
| 8192 | 16 | 2506.33 | 2495.51 | 2186.71 | 2073.05 | 517.72 |

## Matched extended vLLM benchmark

Document-warm excludes root-cache creation; each raw repetition also records that creation cost. Identical-request warm additionally reuses question/candidate prefixes.

| Document tokens | Questions × 3 options | R1 cold ms | Compact cold ms | R1 document-warm ms | Compact document-warm ms | R1 identical-request ms | Compact identical-request ms |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 1 | 41.13 | 47.32 | 46.34 | 43.28 | 23.31 | 40.51 |
| 8 | 4 | 90.42 | 65.47 | 85.78 | 63.39 | 55.66 | 45.68 |
| 8 | 16 | 268.38 | 207.63 | 264.91 | 204.89 | 137.03 | 65.43 |
| 512 | 1 | 125.90 | 118.89 | 54.01 | 48.11 | 45.24 | 46.70 |
| 512 | 4 | 188.55 | 164.16 | 111.12 | 95.28 | 55.00 | 58.84 |
| 512 | 16 | 401.58 | 344.07 | 323.10 | 276.36 | 103.64 | 140.05 |
| 2048 | 1 | 352.05 | 348.81 | 63.41 | 56.95 | 55.50 | 56.97 |
| 2048 | 4 | 422.24 | 410.81 | 136.29 | 119.97 | 80.93 | 85.80 |
| 2048 | 16 | 700.37 | 648.49 | 409.10 | 356.91 | 185.30 | 221.39 |
| 8192 | 1 | 1419.15 | 1412.56 | 104.34 | 97.63 | 96.14 | 97.74 |
| 8192 | 4 | 1556.40 | 1541.58 | 236.89 | 221.42 | 170.15 | 186.93 |
| 8192 | 16 | 2073.78 | 1999.93 | 736.37 | 680.86 | 516.92 | 552.69 |

## Quality

| Run | Evaluation | Questions | Question accuracy | Binary AUROC |
|---|---|---:|---:|---:|
| R1 unmerged | development | 3471 | 81.677% | 0.9534 |
| R1 merged | development | 3471 | 81.504% | 0.9530 |
| Compact merged | development | 3471 | 81.850% | 0.9576 |
| R1 merged | fresh rules | 720 | 95.417% | 0.9882 |
| Compact merged | fresh rules | 720 | 95.417% | 0.9907 |
| vLLM R1 | development | 3471 | 81.533% | 0.9532 |
| vLLM compact | development | 3471 | 81.850% | 0.9574 |

## Authored development cases

| Run | Questions | Accuracy |
|---|---:|---:|
| R1 unmerged | 171 | 78.363% |
| R1 merged | 171 | 78.363% |
| Compact merged | 171 | 78.947% |

## Development quality by family

| Family | Questions | R1 accuracy | Compact accuracy | Change, points |
|---|---:|---:|---:|---:|
| eval_adversarial | 27 | 96.30% | 92.59% | -3.70 |
| eval_agent_output | 26 | 61.54% | 61.54% | +0.00 |
| eval_evidence | 17 | 82.35% | 88.24% | +5.88 |
| eval_multilabel | 32 | 81.25% | 78.12% | -3.12 |
| eval_policy | 22 | 50.00% | 59.09% | +9.09 |
| eval_routing | 25 | 84.00% | 84.00% | +0.00 |
| eval_urgency_sentiment | 22 | 90.91% | 90.91% | +0.00 |
| heldout_boolq | 300 | 83.33% | 83.67% | +0.33 |
| heldout_emotion_multiclass | 300 | 55.33% | 55.67% | +0.33 |
| heldout_intent_clinc | 300 | 94.67% | 91.67% | -3.00 |
| heldout_question_type_trec | 300 | 89.00% | 87.33% | -1.67 |
| heldout_sentiment_sst2 | 300 | 83.67% | 87.67% | +4.00 |
| heldout_topic_dbpedia | 300 | 96.67% | 96.00% | -0.67 |
| hf_emotions_multilabel | 300 | 48.67% | 50.33% | +1.67 |
| hf_intent_banking77 | 300 | 95.67% | 95.67% | +0.00 |
| hf_nli | 300 | 94.33% | 94.67% | +0.33 |
| hf_sentiment_tweets | 300 | 67.33% | 68.00% | +0.67 |
| hf_topic_agnews | 300 | 89.67% | 91.33% | +1.67 |

## Calibration and output types

| Metric | R1 merged | Compact merged |
|---|---:|---:|
| Binary accuracy | 0.8699 | 0.8862 |
| Binary AUROC | 0.9530 | 0.9576 |
| Binary ECE | 0.0774 | 0.0697 |
| Multiclass accuracy | 0.8390 | 0.8362 |
| Multiclass ECE | 0.0290 | 0.0188 |
| Multilabel exact match | 0.5087 | 0.5145 |
| Multilabel ECE | 0.0164 | 0.0166 |

development: compact-only correct **66**; reference-only correct **54**.

fresh rules: compact-only correct **1**; reference-only correct **1**.

## Compact training

Selected step **80** by validation loss **0.30791**. Training wall time 35.4 minutes; 10,080 training questions.

| Step | Validation loss | Validation accuracy |
|---:|---:|---:|
| 0 | 0.36301 | 79.039% |
| 40 | 0.31016 | 81.391% |
| 80 | 0.30791 | 81.595% |
| 100 | 0.31052 | 81.186% |

Adapter reload maximum score difference: `0.0`.

## Interpretation boundaries

- The established benchmark has informed development; it is not a new untouched test.
- The fresh challenge is programmatically labeled and narrow. It does not establish broad human-judgment quality.
- A shorter token sequence is an architectural change and must be evaluated after adaptation.
- Cold-prefix and warm-prefix latency answer different deployment questions.
- Different Torch versions between HF and vLLM are recorded; this is a serving-stack comparison, not a kernel-only ablation.
