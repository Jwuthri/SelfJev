# Evaluation report

- model `mica-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1944; calibration `None`
- cuda / -; 2026-09-30T18:40:58+0000; wall 161.9s

## Overall

question accuracy 91.8%

![reliability](reliability.svg)

**binary**: n 996, positives 427, accuracy 0.952, precision 0.932, recall 0.958, f1 0.945, auroc 0.991, brier 0.036, log_loss 0.125, ece 0.021

**multiclass**: n 578, accuracy 0.958, macro_f1 0.926, log_loss 0.114, brier 0.055, ece_top_label 0.021

**multilabel**: n 370, labels 1810, exact_match 0.762, micro_f1 0.943, macro_f1 0.897, label_auroc 0.983, brier 0.048, log_loss 0.166, ece 0.011

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 650 | 89.7 | bin acc 93.5 F1 91.2 AUROC 0.984 ECE 0.035; mc acc 95.2 mF1 89.7 ECE 0.032; ml EM 71.4 µF1 91.8 ECE 0.017 |
| e2_simple | 657 | 95.0 | bin acc 97.4 F1 97.6 AUROC 0.994 ECE 0.020; mc acc 98.5 mF1 97.2 ECE 0.015; ml EM 82.2 µF1 96.1 ECE 0.023 |
| e2_very_hard | 637 | 90.6 | bin acc 94.7 F1 93.1 AUROC 0.991 ECE 0.043; mc acc 93.8 mF1 90.6 ECE 0.039; ml EM 75.4 µF1 94.7 ECE 0.025 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 563 | 95.9 |
| contradiction | 165 | 96.4 |
| distractor | 449 | 91.1 |
| double_negation | 116 | 88.8 |
| evidence_end | 49 | 93.9 |
| evidence_middle | 96 | 95.8 |
| evidence_start | 17 | 88.2 |
| exception | 211 | 92.4 |
| hypothetical | 121 | 93.4 |
| injection | 145 | 90.3 |
| lexical_overlap | 193 | 94.8 |
| long_state | 160 | 94.4 |
| missing_evidence | 137 | 94.9 |
| multi_positive | 311 | 80.1 |
| multi_turn | 143 | 91.6 |
| negation | 257 | 92.2 |
| nota | 108 | 91.7 |
| numeric_reasoning | 221 | 81.9 |
| paraphrase | 218 | 89.0 |
| role_reversal | 179 | 94.4 |
| sarcasm | 145 | 91.7 |
| temporal_reasoning | 194 | 77.8 |
| zero_positive | 73 | 91.8 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 89.6 |
| 00128-00511 | 469 | 88.7 |
| 00512-02047 | 488 | 95.1 |
| 02048-08191 | 321 | 95.6 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 996 | 95.2 |
| 03 | 128 | 93.8 |
| 04 | 507 | 91.1 |
| 05 | 217 | 80.2 |
| 06 | 77 | 81.8 |
| 07 | 15 | 93.3 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 73.7%; all correct 82.9%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 4.2 |
| 0.4 | 98.6 | 3.3 |
| 0.5 | 96.5 | 2.5 |
| 0.6 | 94.5 | 1.6 |
| 0.7 | 92.4 | 0.9 |
| 0.8 | 89.8 | 0.4 |
| 0.9 | 85.5 | 0.2 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 499 | 0.010 | 0.008 |
| [0.1,0.2) | 20 | 0.148 | 0.050 |
| [0.2,0.3) | 7 | 0.236 | 0.143 |
| [0.3,0.4) | 10 | 0.355 | 0.300 |
| [0.4,0.5) | 21 | 0.456 | 0.429 |
| [0.5,0.6) | 41 | 0.547 | 0.561 |
| [0.6,0.7) | 26 | 0.650 | 0.885 |
| [0.7,0.8) | 32 | 0.751 | 0.844 |
| [0.8,0.9) | 26 | 0.858 | 0.923 |
| [0.9,1.0] | 314 | 0.978 | 0.994 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 3 | 0.285 | 0.667 |
| [0.3,0.4) | 5 | 0.347 | 0.200 |
| [0.4,0.5) | 12 | 0.462 | 0.583 |
| [0.5,0.6) | 12 | 0.551 | 0.583 |
| [0.6,0.7) | 12 | 0.636 | 0.667 |
| [0.7,0.8) | 15 | 0.753 | 0.800 |
| [0.8,0.9) | 25 | 0.859 | 0.960 |
| [0.9,1.0] | 494 | 0.989 | 0.998 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 669 | 0.018 | 0.024 |
| [0.1,0.2) | 55 | 0.147 | 0.127 |
| [0.2,0.3) | 43 | 0.250 | 0.256 |
| [0.3,0.4) | 38 | 0.352 | 0.342 |
| [0.4,0.5) | 26 | 0.456 | 0.346 |
| [0.5,0.6) | 33 | 0.547 | 0.606 |
| [0.6,0.7) | 35 | 0.649 | 0.629 |
| [0.7,0.8) | 41 | 0.754 | 0.756 |
| [0.8,0.9) | 81 | 0.856 | 0.926 |
| [0.9,1.0] | 789 | 0.980 | 0.982 |


Answered 1944/1991; errors 13; accuracy counting failures as wrong 89.6%.
Paired vs ours (images_v1/eval2): ours only right 157, mica-4b only right 27, p = 1.7e-23
