# Evaluation report

- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `weights/selfjev_4b_vision`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / bfloat16; 2026-10-02T23:19:50+0000; wall 359.7s

## Overall

question accuracy 96.1%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.974, precision 0.966, recall 0.975, f1 0.970, auroc 0.996, brier 0.024, log_loss 0.099, ece 0.037

**multiclass**: n 593, accuracy 0.971, macro_f1 0.946, log_loss 0.088, brier 0.045, ece_top_label 0.019

**multilabel**: n 382, labels 1882, exact_match 0.908, micro_f1 0.981, macro_f1 0.963, label_auroc 0.998, brier 0.016, log_loss 0.069, ece 0.026

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 94.9 | bin acc 97.4 F1 96.4 AUROC 0.996 ECE 0.049; mc acc 96.4 mF1 91.7 ECE 0.028; ml EM 86.4 µF1 96.5 ECE 0.030 |
| e2_simple | 664 | 98.3 | bin acc 98.0 F1 98.1 AUROC 0.997 ECE 0.027; mc acc 99.5 mF1 98.9 ECE 0.007; ml EM 97.5 µF1 99.6 ECE 0.026 |
| e2_very_hard | 654 | 95.0 | bin acc 96.9 F1 96.0 AUROC 0.995 ECE 0.042; mc acc 95.5 mF1 93.5 ECE 0.032; ml EM 89.2 µF1 98.0 ECE 0.033 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 98.2 |
| contradiction | 172 | 97.7 |
| distractor | 474 | 94.7 |
| double_negation | 126 | 96.8 |
| evidence_end | 57 | 98.2 |
| evidence_middle | 114 | 98.2 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 97.2 |
| hypothetical | 128 | 96.1 |
| injection | 151 | 95.4 |
| lexical_overlap | 201 | 98.0 |
| long_state | 191 | 98.4 |
| missing_evidence | 141 | 98.6 |
| multi_positive | 322 | 90.7 |
| multi_turn | 149 | 92.6 |
| negation | 257 | 98.1 |
| nota | 118 | 95.8 |
| numeric_reasoning | 224 | 89.3 |
| paraphrase | 218 | 94.0 |
| role_reversal | 187 | 95.7 |
| sarcasm | 149 | 97.3 |
| temporal_reasoning | 203 | 88.7 |
| zero_positive | 73 | 95.9 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 94.7 |
| 00128-00511 | 469 | 94.7 |
| 00512-02047 | 488 | 97.1 |
| 02048-08191 | 329 | 98.8 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 97.4 |
| 03 | 128 | 96.9 |
| 04 | 515 | 95.5 |
| 05 | 224 | 92.0 |
| 06 | 86 | 94.2 |
| 07 | 18 | 94.4 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 81.6%; all correct 89.5%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 2.9 |
| 0.4 | 99.2 | 2.2 |
| 0.5 | 98.1 | 1.9 |
| 0.6 | 97.3 | 1.9 |
| 0.7 | 96.5 | 1.4 |
| 0.8 | 94.6 | 1.2 |
| 0.9 | 91.7 | 0.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 505 | 0.034 | 0.004 |
| [0.1,0.2) | 32 | 0.136 | 0.000 |
| [0.2,0.3) | 10 | 0.240 | 0.000 |
| [0.3,0.4) | 18 | 0.355 | 0.333 |
| [0.4,0.5) | 12 | 0.462 | 0.250 |
| [0.5,0.6) | 6 | 0.556 | 0.833 |
| [0.6,0.7) | 14 | 0.647 | 0.714 |
| [0.7,0.8) | 29 | 0.747 | 0.828 |
| [0.8,0.9) | 26 | 0.859 | 0.962 |
| [0.9,1.0] | 364 | 0.976 | 0.989 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 1 | 0.298 | 0.000 |
| [0.3,0.4) | 4 | 0.348 | 0.250 |
| [0.4,0.5) | 6 | 0.447 | 0.667 |
| [0.5,0.6) | 5 | 0.539 | 1.000 |
| [0.6,0.7) | 5 | 0.659 | 0.400 |
| [0.7,0.8) | 11 | 0.733 | 0.909 |
| [0.8,0.9) | 17 | 0.862 | 0.706 |
| [0.9,1.0] | 544 | 0.994 | 0.996 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 774 | 0.028 | 0.003 |
| [0.1,0.2) | 44 | 0.135 | 0.068 |
| [0.2,0.3) | 12 | 0.251 | 0.333 |
| [0.3,0.4) | 5 | 0.342 | 0.200 |
| [0.4,0.5) | 16 | 0.441 | 0.438 |
| [0.5,0.6) | 15 | 0.550 | 0.467 |
| [0.6,0.7) | 15 | 0.639 | 0.667 |
| [0.7,0.8) | 22 | 0.744 | 0.727 |
| [0.8,0.9) | 47 | 0.856 | 0.957 |
| [0.9,1.0] | 932 | 0.979 | 0.998 |
