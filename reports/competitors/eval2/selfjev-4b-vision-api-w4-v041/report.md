# Evaluation report

- model `selfjev-4b-vision-api-w4-v041-run1` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-10-02T23:10:51+0000; wall 166.2s

## Overall

question accuracy 94.8%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.966, precision 0.937, recall 0.986, f1 0.961, auroc 0.995, brier 0.026, log_loss 0.099, ece 0.028

**multiclass**: n 593, accuracy 0.971, macro_f1 0.948, log_loss 0.091, brier 0.044, ece_top_label 0.009

**multilabel**: n 382, labels 1882, exact_match 0.864, micro_f1 0.967, macro_f1 0.944, label_auroc 0.994, brier 0.028, log_loss 0.102, ece 0.017

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 94.4 | bin acc 96.6 F1 95.3 AUROC 0.996 ECE 0.040; mc acc 96.4 mF1 91.7 ECE 0.027; ml EM 85.6 µF1 95.8 ECE 0.031 |
| e2_simple | 664 | 97.3 | bin acc 97.4 F1 97.6 AUROC 0.994 ECE 0.028; mc acc 99.5 mF1 98.9 ECE 0.007; ml EM 93.3 µF1 98.8 ECE 0.018 |
| e2_very_hard | 654 | 92.7 | bin acc 95.7 F1 94.5 AUROC 0.994 ECE 0.032; mc acc 95.5 mF1 94.1 ECE 0.016; ml EM 80.8 µF1 95.5 ECE 0.018 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.0 |
| contradiction | 172 | 95.3 |
| distractor | 474 | 92.6 |
| double_negation | 126 | 96.8 |
| evidence_end | 57 | 100.0 |
| evidence_middle | 114 | 97.4 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 93.4 |
| hypothetical | 128 | 94.5 |
| injection | 151 | 94.7 |
| lexical_overlap | 201 | 97.0 |
| long_state | 191 | 97.9 |
| missing_evidence | 141 | 96.5 |
| multi_positive | 322 | 89.1 |
| multi_turn | 149 | 92.6 |
| negation | 257 | 97.3 |
| nota | 118 | 90.7 |
| numeric_reasoning | 224 | 88.4 |
| paraphrase | 218 | 93.1 |
| role_reversal | 187 | 94.7 |
| sarcasm | 149 | 94.0 |
| temporal_reasoning | 203 | 85.2 |
| zero_positive | 73 | 93.2 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 94.0 |
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
| 05 | 224 | 89.3 |
| 06 | 86 | 87.2 |
| 07 | 18 | 83.3 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 81.6%; all correct 88.2%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 2.9 |
| 0.4 | 99.5 | 2.5 |
| 0.5 | 98.8 | 2.0 |
| 0.6 | 97.3 | 1.6 |
| 0.7 | 95.8 | 1.1 |
| 0.8 | 94.6 | 1.1 |
| 0.9 | 92.6 | 0.5 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 503 | 0.017 | 0.000 |
| [0.1,0.2) | 28 | 0.145 | 0.071 |
| [0.2,0.3) | 13 | 0.232 | 0.000 |
| [0.3,0.4) | 7 | 0.373 | 0.286 |
| [0.4,0.5) | 7 | 0.436 | 0.286 |
| [0.5,0.6) | 6 | 0.550 | 0.333 |
| [0.6,0.7) | 13 | 0.642 | 0.462 |
| [0.7,0.8) | 15 | 0.755 | 0.867 |
| [0.8,0.9) | 27 | 0.844 | 0.667 |
| [0.9,1.0] | 397 | 0.989 | 0.982 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 3 | 0.367 | 0.333 |
| [0.4,0.5) | 4 | 0.446 | 0.250 |
| [0.5,0.6) | 9 | 0.550 | 0.667 |
| [0.6,0.7) | 9 | 0.654 | 0.667 |
| [0.7,0.8) | 7 | 0.760 | 1.000 |
| [0.8,0.9) | 12 | 0.858 | 0.750 |
| [0.9,1.0] | 549 | 0.994 | 0.995 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 718 | 0.018 | 0.011 |
| [0.1,0.2) | 52 | 0.142 | 0.077 |
| [0.2,0.3) | 27 | 0.252 | 0.074 |
| [0.3,0.4) | 26 | 0.343 | 0.154 |
| [0.4,0.5) | 14 | 0.451 | 0.429 |
| [0.5,0.6) | 13 | 0.540 | 0.385 |
| [0.6,0.7) | 22 | 0.660 | 0.591 |
| [0.7,0.8) | 24 | 0.756 | 0.625 |
| [0.8,0.9) | 33 | 0.864 | 0.848 |
| [0.9,1.0] | 953 | 0.993 | 0.986 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 94.8%.
Paired vs ours (images_v1/eval2): ours only right 43, selfjev-4b-vision-api-w4-v041-run1 only right 16, p = 0.00058
