# Evaluation report

- model `kev-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-09-30T17:58:03+0000; wall 108.6s

## Overall

question accuracy 88.4%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.920, precision 0.877, recall 0.947, f1 0.910, auroc 0.981, brier 0.058, log_loss 0.209, ece 0.065

**multiclass**: n 593, accuracy 0.946, macro_f1 0.911, log_loss 0.226, brier 0.095, ece_top_label 0.098

**multilabel**: n 382, labels 1882, exact_match 0.694, micro_f1 0.919, macro_f1 0.858, label_auroc 0.974, brier 0.073, log_loss 0.250, ece 0.081

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 86.6 | bin acc 90.5 F1 87.6 AUROC 0.979 ECE 0.086; mc acc 93.3 mF1 88.4 ECE 0.115; ml EM 66.7 µF1 90.8 ECE 0.075 |
| e2_simple | 664 | 93.1 | bin acc 95.9 F1 96.4 AUROC 0.992 ECE 0.055; mc acc 99.0 mF1 98.3 ECE 0.094; ml EM 75.0 µF1 93.6 ECE 0.092 |
| e2_very_hard | 654 | 85.6 | bin acc 89.5 F1 86.6 AUROC 0.960 ECE 0.059; mc acc 91.5 mF1 86.7 ECE 0.116; ml EM 66.9 µF1 91.2 ECE 0.084 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 93.8 |
| contradiction | 172 | 90.7 |
| distractor | 474 | 85.9 |
| double_negation | 126 | 88.1 |
| evidence_end | 57 | 91.2 |
| evidence_middle | 114 | 95.6 |
| evidence_start | 17 | 94.1 |
| exception | 213 | 86.4 |
| hypothetical | 128 | 89.1 |
| injection | 151 | 84.1 |
| lexical_overlap | 201 | 90.0 |
| long_state | 191 | 92.7 |
| missing_evidence | 141 | 92.9 |
| multi_positive | 322 | 75.2 |
| multi_turn | 149 | 91.3 |
| negation | 257 | 93.4 |
| nota | 118 | 89.0 |
| numeric_reasoning | 224 | 75.9 |
| paraphrase | 218 | 83.5 |
| role_reversal | 187 | 91.4 |
| sarcasm | 149 | 78.5 |
| temporal_reasoning | 203 | 73.4 |
| zero_positive | 73 | 87.7 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 86.6 |
| 00128-00511 | 469 | 84.9 |
| 00512-02047 | 488 | 92.4 |
| 02048-08191 | 329 | 91.2 |
| 08192+ | 39 | 89.7 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 92.0 |
| 03 | 128 | 92.2 |
| 04 | 515 | 88.2 |
| 05 | 224 | 76.8 |
| 06 | 86 | 77.9 |
| 07 | 18 | 66.7 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 78.9%; all correct 77.6%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 5.4 |
| 0.4 | 98.7 | 4.8 |
| 0.5 | 95.3 | 2.7 |
| 0.6 | 90.4 | 0.6 |
| 0.7 | 85.3 | 0.4 |
| 0.8 | 76.9 | 0.2 |
| 0.9 | 54.1 | 0.0 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 305 | 0.044 | 0.007 |
| [0.1,0.2) | 128 | 0.141 | 0.016 |
| [0.2,0.3) | 53 | 0.241 | 0.075 |
| [0.3,0.4) | 37 | 0.345 | 0.162 |
| [0.4,0.5) | 23 | 0.437 | 0.391 |
| [0.5,0.6) | 32 | 0.553 | 0.281 |
| [0.6,0.7) | 30 | 0.648 | 0.533 |
| [0.7,0.8) | 35 | 0.751 | 0.800 |
| [0.8,0.9) | 65 | 0.854 | 0.862 |
| [0.9,1.0] | 308 | 0.960 | 0.984 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 1 | 0.298 | 1.000 |
| [0.3,0.4) | 7 | 0.358 | 0.429 |
| [0.4,0.5) | 20 | 0.450 | 0.350 |
| [0.5,0.6) | 29 | 0.555 | 0.586 |
| [0.6,0.7) | 30 | 0.649 | 0.967 |
| [0.7,0.8) | 50 | 0.762 | 0.980 |
| [0.8,0.9) | 135 | 0.856 | 0.993 |
| [0.9,1.0] | 321 | 0.953 | 1.000 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 271 | 0.053 | 0.000 |
| [0.1,0.2) | 199 | 0.142 | 0.045 |
| [0.2,0.3) | 132 | 0.249 | 0.053 |
| [0.3,0.4) | 89 | 0.349 | 0.101 |
| [0.4,0.5) | 67 | 0.446 | 0.194 |
| [0.5,0.6) | 59 | 0.548 | 0.288 |
| [0.6,0.7) | 60 | 0.650 | 0.533 |
| [0.7,0.8) | 91 | 0.750 | 0.681 |
| [0.8,0.9) | 135 | 0.858 | 0.815 |
| [0.9,1.0] | 779 | 0.959 | 0.983 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 88.4%.
Paired vs ours (images_v1/eval2): ours only right 175, kev-4b only right 22, p = 9e-31
