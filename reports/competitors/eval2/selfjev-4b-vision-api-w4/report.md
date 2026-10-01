# Evaluation report

- model `selfjev-4b-vision-api-w4` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-09-30T20:14:34+0000; wall 242.4s

## Overall

question accuracy 94.7%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.966, precision 0.937, recall 0.986, f1 0.961, auroc 0.995, brier 0.026, log_loss 0.099, ece 0.028

**multiclass**: n 593, accuracy 0.971, macro_f1 0.948, log_loss 0.090, brier 0.044, ece_top_label 0.010

**multilabel**: n 382, labels 1882, exact_match 0.859, micro_f1 0.967, macro_f1 0.943, label_auroc 0.994, brier 0.028, log_loss 0.102, ece 0.017

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 94.2 | bin acc 96.6 F1 95.3 AUROC 0.996 ECE 0.038; mc acc 96.4 mF1 91.7 ECE 0.027; ml EM 84.8 µF1 95.7 ECE 0.030 |
| e2_simple | 664 | 97.3 | bin acc 97.4 F1 97.6 AUROC 0.994 ECE 0.028; mc acc 99.5 mF1 98.9 ECE 0.007; ml EM 93.3 µF1 98.8 ECE 0.018 |
| e2_very_hard | 654 | 92.5 | bin acc 95.7 F1 94.5 AUROC 0.994 ECE 0.032; mc acc 95.5 mF1 94.1 ECE 0.013; ml EM 80.0 µF1 95.5 ECE 0.019 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.0 |
| contradiction | 172 | 95.3 |
| distractor | 474 | 92.6 |
| double_negation | 126 | 96.0 |
| evidence_end | 57 | 100.0 |
| evidence_middle | 114 | 97.4 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 93.4 |
| hypothetical | 128 | 94.5 |
| injection | 151 | 94.7 |
| lexical_overlap | 201 | 97.0 |
| long_state | 191 | 97.9 |
| missing_evidence | 141 | 96.5 |
| multi_positive | 322 | 88.5 |
| multi_turn | 149 | 91.9 |
| negation | 257 | 96.9 |
| nota | 118 | 90.7 |
| numeric_reasoning | 224 | 87.9 |
| paraphrase | 218 | 93.1 |
| role_reversal | 187 | 94.7 |
| sarcasm | 149 | 94.0 |
| temporal_reasoning | 203 | 85.2 |
| zero_positive | 73 | 93.2 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 93.7 |
| 00128-00511 | 469 | 93.6 |
| 00512-02047 | 488 | 95.7 |
| 02048-08191 | 329 | 96.4 |
| 08192+ | 39 | 97.4 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 96.6 |
| 03 | 128 | 96.9 |
| 04 | 515 | 95.0 |
| 05 | 224 | 88.8 |
| 06 | 86 | 86.0 |
| 07 | 18 | 83.3 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 81.6%; all correct 88.2%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 2.9 |
| 0.4 | 99.5 | 2.5 |
| 0.5 | 98.7 | 1.9 |
| 0.6 | 97.3 | 1.6 |
| 0.7 | 95.8 | 1.1 |
| 0.8 | 94.8 | 1.1 |
| 0.9 | 92.6 | 0.5 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 502 | 0.017 | 0.000 |
| [0.1,0.2) | 30 | 0.146 | 0.067 |
| [0.2,0.3) | 12 | 0.237 | 0.000 |
| [0.3,0.4) | 8 | 0.373 | 0.250 |
| [0.4,0.5) | 6 | 0.453 | 0.333 |
| [0.5,0.6) | 7 | 0.558 | 0.286 |
| [0.6,0.7) | 12 | 0.642 | 0.500 |
| [0.7,0.8) | 15 | 0.755 | 0.867 |
| [0.8,0.9) | 27 | 0.846 | 0.667 |
| [0.9,1.0] | 397 | 0.989 | 0.982 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 3 | 0.369 | 0.333 |
| [0.4,0.5) | 5 | 0.453 | 0.200 |
| [0.5,0.6) | 8 | 0.558 | 0.750 |
| [0.6,0.7) | 9 | 0.652 | 0.667 |
| [0.7,0.8) | 6 | 0.753 | 1.000 |
| [0.8,0.9) | 13 | 0.854 | 0.769 |
| [0.9,1.0] | 549 | 0.994 | 0.995 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 719 | 0.018 | 0.011 |
| [0.1,0.2) | 48 | 0.139 | 0.083 |
| [0.2,0.3) | 31 | 0.248 | 0.065 |
| [0.3,0.4) | 25 | 0.340 | 0.160 |
| [0.4,0.5) | 17 | 0.458 | 0.471 |
| [0.5,0.6) | 12 | 0.556 | 0.250 |
| [0.6,0.7) | 20 | 0.655 | 0.650 |
| [0.7,0.8) | 25 | 0.760 | 0.600 |
| [0.8,0.9) | 33 | 0.867 | 0.848 |
| [0.9,1.0] | 952 | 0.993 | 0.987 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 94.7%.
Paired vs ours (images_v1/eval2): ours only right 44, selfjev-4b-vision-api-w4 only right 15, p = 0.0002
