# Evaluation report

- model `jpt-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-09-30T19:30:50+0000; wall 89.6s

## Overall

question accuracy 92.5%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.949, precision 0.915, recall 0.970, f1 0.942, auroc 0.987, brier 0.042, log_loss 0.149, ece 0.025

**multiclass**: n 593, accuracy 0.961, macro_f1 0.937, log_loss 0.131, brier 0.059, ece_top_label 0.035

**multilabel**: n 382, labels 1882, exact_match 0.806, micro_f1 0.951, macro_f1 0.913, label_auroc 0.990, brier 0.038, log_loss 0.136, ece 0.025

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 90.0 | bin acc 92.8 F1 90.6 AUROC 0.980 ECE 0.042; mc acc 94.8 mF1 89.4 ECE 0.035; ml EM 75.8 µF1 93.1 ECE 0.031 |
| e2_simple | 664 | 96.2 | bin acc 96.5 F1 96.8 AUROC 0.997 ECE 0.031; mc acc 99.0 mF1 98.3 ECE 0.035; ml EM 90.8 µF1 98.2 ECE 0.023 |
| e2_very_hard | 654 | 91.3 | bin acc 95.4 F1 94.0 AUROC 0.980 ECE 0.027; mc acc 94.5 mF1 93.3 ECE 0.057; ml EM 76.2 µF1 93.7 ECE 0.039 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.2 |
| contradiction | 172 | 93.6 |
| distractor | 474 | 91.8 |
| double_negation | 126 | 90.5 |
| evidence_end | 57 | 94.7 |
| evidence_middle | 114 | 97.4 |
| evidence_start | 17 | 94.1 |
| exception | 213 | 93.4 |
| hypothetical | 128 | 96.1 |
| injection | 151 | 90.1 |
| lexical_overlap | 201 | 94.5 |
| long_state | 191 | 96.3 |
| missing_evidence | 141 | 94.3 |
| multi_positive | 322 | 82.0 |
| multi_turn | 149 | 93.3 |
| negation | 257 | 94.6 |
| nota | 118 | 94.9 |
| numeric_reasoning | 224 | 83.0 |
| paraphrase | 218 | 89.4 |
| role_reversal | 187 | 93.6 |
| sarcasm | 149 | 84.6 |
| temporal_reasoning | 203 | 81.8 |
| zero_positive | 73 | 89.0 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 89.8 |
| 00128-00511 | 469 | 90.2 |
| 00512-02047 | 488 | 95.7 |
| 02048-08191 | 329 | 96.0 |
| 08192+ | 39 | 97.4 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 94.9 |
| 03 | 128 | 93.8 |
| 04 | 515 | 93.0 |
| 05 | 224 | 85.3 |
| 06 | 86 | 80.2 |
| 07 | 18 | 88.9 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 77.6%; all correct 81.6%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 3.9 |
| 0.4 | 99.8 | 3.7 |
| 0.5 | 99.0 | 3.1 |
| 0.6 | 97.1 | 2.1 |
| 0.7 | 93.3 | 1.4 |
| 0.8 | 90.1 | 1.1 |
| 0.9 | 83.6 | 0.2 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 487 | 0.021 | 0.016 |
| [0.1,0.2) | 37 | 0.143 | 0.081 |
| [0.2,0.3) | 15 | 0.230 | 0.067 |
| [0.3,0.4) | 7 | 0.319 | 0.000 |
| [0.4,0.5) | 9 | 0.434 | 0.111 |
| [0.5,0.6) | 13 | 0.537 | 0.615 |
| [0.6,0.7) | 16 | 0.659 | 0.500 |
| [0.7,0.8) | 22 | 0.765 | 0.500 |
| [0.8,0.9) | 59 | 0.863 | 0.864 |
| [0.9,1.0] | 351 | 0.969 | 0.980 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 1 | 0.391 | 0.000 |
| [0.4,0.5) | 5 | 0.452 | 0.200 |
| [0.5,0.6) | 11 | 0.545 | 0.455 |
| [0.6,0.7) | 23 | 0.654 | 0.826 |
| [0.7,0.8) | 19 | 0.763 | 0.895 |
| [0.8,0.9) | 38 | 0.857 | 0.868 |
| [0.9,1.0] | 496 | 0.975 | 0.998 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 784 | 0.015 | 0.023 |
| [0.1,0.2) | 38 | 0.132 | 0.395 |
| [0.2,0.3) | 14 | 0.226 | 0.429 |
| [0.3,0.4) | 16 | 0.334 | 0.500 |
| [0.4,0.5) | 12 | 0.445 | 0.583 |
| [0.5,0.6) | 19 | 0.546 | 0.263 |
| [0.6,0.7) | 16 | 0.668 | 0.688 |
| [0.7,0.8) | 18 | 0.770 | 0.667 |
| [0.8,0.9) | 75 | 0.862 | 0.827 |
| [0.9,1.0] | 890 | 0.976 | 0.990 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 92.5%.
Paired vs ours (images_v1/eval2): ours only right 96, jpt-4b only right 24, p = 2.2e-11
