# Evaluation report

- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `/home/ubuntu/.selfjev/server/jobs/ftjob_41120853b4b54553832c/run/adapter`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / bfloat16; 2026-10-02T23:34:09+0000; wall 359.8s

## Overall

question accuracy 96.1%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.973, precision 0.966, recall 0.972, f1 0.969, auroc 0.996, brier 0.025, log_loss 0.109, ece 0.046

**multiclass**: n 593, accuracy 0.976, macro_f1 0.953, log_loss 0.091, brier 0.045, ece_top_label 0.022

**multilabel**: n 382, labels 1882, exact_match 0.906, micro_f1 0.980, macro_f1 0.961, label_auroc 0.998, brier 0.017, log_loss 0.078, ece 0.035

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 94.9 | bin acc 97.1 F1 96.0 AUROC 0.996 ECE 0.058; mc acc 96.4 mF1 91.7 ECE 0.030; ml EM 87.1 µF1 96.7 ECE 0.036 |
| e2_simple | 664 | 98.5 | bin acc 98.0 F1 98.1 AUROC 0.997 ECE 0.038; mc acc 99.5 mF1 98.9 ECE 0.010; ml EM 98.3 µF1 99.7 ECE 0.034 |
| e2_very_hard | 654 | 95.0 | bin acc 96.9 F1 96.0 AUROC 0.995 ECE 0.055; mc acc 97.0 mF1 95.5 ECE 0.042; ml EM 86.9 µF1 97.6 ECE 0.045 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 98.4 |
| contradiction | 172 | 97.7 |
| distractor | 474 | 95.4 |
| double_negation | 126 | 96.8 |
| evidence_end | 57 | 98.2 |
| evidence_middle | 114 | 98.2 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 96.7 |
| hypothetical | 128 | 96.1 |
| injection | 151 | 95.4 |
| lexical_overlap | 201 | 98.0 |
| long_state | 191 | 98.4 |
| missing_evidence | 141 | 98.6 |
| multi_positive | 322 | 90.1 |
| multi_turn | 149 | 92.6 |
| negation | 257 | 97.7 |
| nota | 118 | 96.6 |
| numeric_reasoning | 224 | 89.7 |
| paraphrase | 218 | 95.0 |
| role_reversal | 187 | 95.7 |
| sarcasm | 149 | 97.3 |
| temporal_reasoning | 203 | 88.2 |
| zero_positive | 73 | 95.9 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 94.9 |
| 00128-00511 | 469 | 94.7 |
| 00512-02047 | 488 | 97.1 |
| 02048-08191 | 329 | 98.8 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 97.3 |
| 03 | 128 | 96.1 |
| 04 | 515 | 95.9 |
| 05 | 224 | 92.4 |
| 06 | 86 | 94.2 |
| 07 | 18 | 94.4 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 81.6%; all correct 89.5%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 2.4 |
| 0.4 | 98.7 | 1.9 |
| 0.5 | 97.5 | 1.9 |
| 0.6 | 96.8 | 1.7 |
| 0.7 | 94.9 | 1.2 |
| 0.8 | 93.1 | 0.5 |
| 0.9 | 89.2 | 0.2 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 490 | 0.041 | 0.000 |
| [0.1,0.2) | 43 | 0.134 | 0.047 |
| [0.2,0.3) | 15 | 0.243 | 0.067 |
| [0.3,0.4) | 16 | 0.351 | 0.250 |
| [0.4,0.5) | 14 | 0.446 | 0.357 |
| [0.5,0.6) | 12 | 0.550 | 0.833 |
| [0.6,0.7) | 21 | 0.669 | 0.714 |
| [0.7,0.8) | 21 | 0.745 | 0.905 |
| [0.8,0.9) | 38 | 0.856 | 0.921 |
| [0.9,1.0] | 346 | 0.972 | 0.994 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 2 | 0.288 | 0.500 |
| [0.3,0.4) | 6 | 0.362 | 0.667 |
| [0.4,0.5) | 7 | 0.484 | 1.000 |
| [0.5,0.6) | 4 | 0.572 | 0.750 |
| [0.6,0.7) | 11 | 0.668 | 0.727 |
| [0.7,0.8) | 11 | 0.762 | 0.636 |
| [0.8,0.9) | 23 | 0.861 | 0.913 |
| [0.9,1.0] | 529 | 0.992 | 0.998 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 760 | 0.036 | 0.001 |
| [0.1,0.2) | 53 | 0.138 | 0.057 |
| [0.2,0.3) | 16 | 0.248 | 0.312 |
| [0.3,0.4) | 10 | 0.351 | 0.300 |
| [0.4,0.5) | 19 | 0.442 | 0.474 |
| [0.5,0.6) | 18 | 0.560 | 0.500 |
| [0.6,0.7) | 21 | 0.656 | 0.714 |
| [0.7,0.8) | 22 | 0.760 | 0.909 |
| [0.8,0.9) | 61 | 0.857 | 0.984 |
| [0.9,1.0] | 902 | 0.975 | 0.998 |
