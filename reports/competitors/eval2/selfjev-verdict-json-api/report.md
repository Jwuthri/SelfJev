# Evaluation report

- model `selfjev-verdict-json-api` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-10-01T13:46:42+0000; wall 152.8s

## Overall

question accuracy 94.0%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.964, precision 0.931, recall 0.989, f1 0.959, auroc 0.994, brier 0.029, log_loss 0.108, ece 0.034

**multiclass**: n 593, accuracy 0.966, macro_f1 0.945, log_loss 0.098, brier 0.049, ece_top_label 0.012

**multilabel**: n 382, labels 1882, exact_match 0.835, micro_f1 0.962, macro_f1 0.938, label_auroc 0.993, brier 0.032, log_loss 0.115, ece 0.026

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 92.7 | bin acc 96.0 F1 94.7 AUROC 0.995 ECE 0.048; mc acc 95.3 mF1 90.4 ECE 0.030; ml EM 80.3 µF1 94.7 ECE 0.038 |
| e2_simple | 664 | 97.3 | bin acc 97.4 F1 97.6 AUROC 0.994 ECE 0.029; mc acc 100.0 mF1 100.0 ECE 0.008; ml EM 92.5 µF1 98.7 ECE 0.022 |
| e2_very_hard | 654 | 91.9 | bin acc 95.7 F1 94.5 AUROC 0.994 ECE 0.038; mc acc 94.5 mF1 93.1 ECE 0.027; ml EM 78.5 µF1 95.1 ECE 0.025 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.5 |
| contradiction | 172 | 94.8 |
| distractor | 474 | 92.0 |
| double_negation | 126 | 96.0 |
| evidence_end | 57 | 98.2 |
| evidence_middle | 114 | 95.6 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 92.5 |
| hypothetical | 128 | 94.5 |
| injection | 151 | 94.0 |
| lexical_overlap | 201 | 95.5 |
| long_state | 191 | 96.3 |
| missing_evidence | 141 | 96.5 |
| multi_positive | 322 | 86.0 |
| multi_turn | 149 | 91.3 |
| negation | 257 | 94.9 |
| nota | 118 | 85.6 |
| numeric_reasoning | 224 | 87.1 |
| paraphrase | 218 | 90.8 |
| role_reversal | 187 | 94.1 |
| sarcasm | 149 | 94.0 |
| temporal_reasoning | 203 | 83.3 |
| zero_positive | 73 | 90.4 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 92.9 |
| 00128-00511 | 469 | 91.7 |
| 00512-02047 | 488 | 95.5 |
| 02048-08191 | 329 | 96.4 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 96.4 |
| 03 | 128 | 95.3 |
| 04 | 515 | 94.0 |
| 05 | 224 | 86.2 |
| 06 | 86 | 87.2 |
| 07 | 18 | 83.3 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 80.3%; all correct 85.5%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 3.4 |
| 0.4 | 99.5 | 2.9 |
| 0.5 | 98.8 | 2.2 |
| 0.6 | 97.3 | 1.9 |
| 0.7 | 95.6 | 1.2 |
| 0.8 | 94.3 | 0.9 |
| 0.9 | 92.4 | 0.7 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 490 | 0.022 | 0.000 |
| [0.1,0.2) | 33 | 0.152 | 0.061 |
| [0.2,0.3) | 13 | 0.246 | 0.077 |
| [0.3,0.4) | 11 | 0.343 | 0.182 |
| [0.4,0.5) | 7 | 0.458 | 0.000 |
| [0.5,0.6) | 7 | 0.541 | 0.143 |
| [0.6,0.7) | 10 | 0.647 | 0.400 |
| [0.7,0.8) | 14 | 0.758 | 0.786 |
| [0.8,0.9) | 33 | 0.854 | 0.667 |
| [0.9,1.0] | 398 | 0.990 | 0.985 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 3 | 0.377 | 0.000 |
| [0.4,0.5) | 4 | 0.433 | 0.000 |
| [0.5,0.6) | 9 | 0.537 | 0.778 |
| [0.6,0.7) | 10 | 0.649 | 0.600 |
| [0.7,0.8) | 8 | 0.745 | 0.750 |
| [0.8,0.9) | 11 | 0.856 | 0.909 |
| [0.9,1.0] | 548 | 0.994 | 0.993 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 693 | 0.023 | 0.012 |
| [0.1,0.2) | 52 | 0.146 | 0.038 |
| [0.2,0.3) | 33 | 0.241 | 0.061 |
| [0.3,0.4) | 23 | 0.344 | 0.174 |
| [0.4,0.5) | 18 | 0.454 | 0.278 |
| [0.5,0.6) | 23 | 0.544 | 0.304 |
| [0.6,0.7) | 26 | 0.640 | 0.538 |
| [0.7,0.8) | 22 | 0.761 | 0.636 |
| [0.8,0.9) | 37 | 0.863 | 0.730 |
| [0.9,1.0] | 955 | 0.994 | 0.986 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 94.0%.
Paired vs ours (images_v1/eval2): ours only right 63, selfjev-verdict-json-api only right 20, p = 2.4e-06
