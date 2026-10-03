# Evaluation report

- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `/home/ubuntu/.selfjev/server/jobs/ftjob_4e4f0ce0d40f4cfbb677/run/adapter`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / bfloat16; 2026-10-02T23:45:17+0000; wall 358.4s

## Overall

question accuracy 96.1%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.971, precision 0.961, recall 0.972, f1 0.967, auroc 0.996, brier 0.025, log_loss 0.106, ece 0.042

**multiclass**: n 593, accuracy 0.976, macro_f1 0.953, log_loss 0.089, brier 0.044, ece_top_label 0.018

**multilabel**: n 382, labels 1882, exact_match 0.908, micro_f1 0.980, macro_f1 0.961, label_auroc 0.998, brier 0.017, log_loss 0.077, ece 0.034

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 94.8 | bin acc 96.8 F1 95.6 AUROC 0.996 ECE 0.054; mc acc 96.4 mF1 91.7 ECE 0.032; ml EM 87.1 µF1 96.5 ECE 0.035 |
| e2_simple | 664 | 98.3 | bin acc 97.7 F1 97.9 AUROC 0.997 ECE 0.036; mc acc 99.5 mF1 98.9 ECE 0.010; ml EM 98.3 µF1 99.7 ECE 0.033 |
| e2_very_hard | 654 | 95.1 | bin acc 96.9 F1 96.0 AUROC 0.995 ECE 0.053; mc acc 97.0 mF1 95.5 ECE 0.030; ml EM 87.7 µF1 97.7 ECE 0.041 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 98.4 |
| contradiction | 172 | 97.7 |
| distractor | 474 | 94.9 |
| double_negation | 126 | 96.8 |
| evidence_end | 57 | 98.2 |
| evidence_middle | 114 | 98.2 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 97.2 |
| hypothetical | 128 | 95.3 |
| injection | 151 | 96.7 |
| lexical_overlap | 201 | 98.0 |
| long_state | 191 | 97.9 |
| missing_evidence | 141 | 98.6 |
| multi_positive | 322 | 90.4 |
| multi_turn | 149 | 92.6 |
| negation | 257 | 98.1 |
| nota | 118 | 96.6 |
| numeric_reasoning | 224 | 89.7 |
| paraphrase | 218 | 95.0 |
| role_reversal | 187 | 95.2 |
| sarcasm | 149 | 97.3 |
| temporal_reasoning | 203 | 88.7 |
| zero_positive | 73 | 95.9 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 94.9 |
| 00128-00511 | 469 | 95.1 |
| 00512-02047 | 488 | 96.7 |
| 02048-08191 | 329 | 98.5 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 97.1 |
| 03 | 128 | 96.9 |
| 04 | 515 | 95.9 |
| 05 | 224 | 92.9 |
| 06 | 86 | 93.0 |
| 07 | 18 | 94.4 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 82.9%; all correct 88.2%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 2.4 |
| 0.4 | 98.8 | 2.0 |
| 0.5 | 98.0 | 1.9 |
| 0.6 | 97.0 | 1.7 |
| 0.7 | 95.1 | 1.1 |
| 0.8 | 93.1 | 0.5 |
| 0.9 | 90.1 | 0.2 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 496 | 0.037 | 0.002 |
| [0.1,0.2) | 38 | 0.134 | 0.026 |
| [0.2,0.3) | 13 | 0.235 | 0.077 |
| [0.3,0.4) | 17 | 0.349 | 0.235 |
| [0.4,0.5) | 12 | 0.451 | 0.417 |
| [0.5,0.6) | 14 | 0.548 | 0.714 |
| [0.6,0.7) | 20 | 0.667 | 0.700 |
| [0.7,0.8) | 21 | 0.745 | 0.905 |
| [0.8,0.9) | 39 | 0.858 | 0.923 |
| [0.9,1.0] | 346 | 0.972 | 0.994 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 2 | 0.287 | 0.500 |
| [0.3,0.4) | 5 | 0.363 | 0.800 |
| [0.4,0.5) | 5 | 0.451 | 0.800 |
| [0.5,0.6) | 6 | 0.544 | 0.833 |
| [0.6,0.7) | 11 | 0.660 | 0.636 |
| [0.7,0.8) | 12 | 0.758 | 0.750 |
| [0.8,0.9) | 18 | 0.853 | 0.889 |
| [0.9,1.0] | 534 | 0.991 | 0.998 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 764 | 0.033 | 0.001 |
| [0.1,0.2) | 47 | 0.136 | 0.064 |
| [0.2,0.3) | 16 | 0.245 | 0.250 |
| [0.3,0.4) | 13 | 0.348 | 0.385 |
| [0.4,0.5) | 16 | 0.444 | 0.438 |
| [0.5,0.6) | 17 | 0.556 | 0.529 |
| [0.6,0.7) | 22 | 0.650 | 0.591 |
| [0.7,0.8) | 23 | 0.758 | 0.957 |
| [0.8,0.9) | 60 | 0.857 | 0.967 |
| [0.9,1.0] | 904 | 0.974 | 0.999 |
