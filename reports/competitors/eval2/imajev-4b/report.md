# Evaluation report

- model `imajev-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-09-30T19:17:43+0000; wall 489.4s

## Overall

question accuracy 91.5%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.934, precision 0.883, recall 0.975, f1 0.927, auroc 0.989, brier 0.048, log_loss 0.173, ece 0.070

**multiclass**: n 593, accuracy 0.958, macro_f1 0.929, log_loss 0.130, brier 0.062, ece_top_label 0.015

**multilabel**: n 382, labels 1882, exact_match 0.798, micro_f1 0.951, macro_f1 0.911, label_auroc 0.987, brier 0.041, log_loss 0.155, ece 0.036

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 89.7 | bin acc 92.0 F1 89.7 AUROC 0.983 ECE 0.092; mc acc 94.3 mF1 90.3 ECE 0.037; ml EM 77.3 µF1 94.2 ECE 0.047 |
| e2_simple | 664 | 95.9 | bin acc 96.2 F1 96.6 AUROC 0.998 ECE 0.055; mc acc 99.5 mF1 98.9 ECE 0.019; ml EM 89.2 µF1 97.8 ECE 0.044 |
| e2_very_hard | 654 | 88.8 | bin acc 92.0 F1 90.0 AUROC 0.981 ECE 0.074; mc acc 93.5 mF1 89.3 ECE 0.027; ml EM 73.8 µF1 93.3 ECE 0.037 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 96.3 |
| contradiction | 172 | 93.0 |
| distractor | 474 | 90.9 |
| double_negation | 126 | 90.5 |
| evidence_end | 57 | 96.5 |
| evidence_middle | 114 | 93.0 |
| evidence_start | 17 | 94.1 |
| exception | 213 | 87.8 |
| hypothetical | 128 | 94.5 |
| injection | 151 | 88.7 |
| lexical_overlap | 201 | 92.5 |
| long_state | 191 | 92.7 |
| missing_evidence | 141 | 93.6 |
| multi_positive | 322 | 83.9 |
| multi_turn | 149 | 88.6 |
| negation | 257 | 91.8 |
| nota | 118 | 87.3 |
| numeric_reasoning | 224 | 82.6 |
| paraphrase | 218 | 90.4 |
| role_reversal | 187 | 92.5 |
| sarcasm | 149 | 83.9 |
| temporal_reasoning | 203 | 76.4 |
| zero_positive | 73 | 86.3 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 90.4 |
| 00128-00511 | 469 | 89.1 |
| 00512-02047 | 488 | 94.1 |
| 02048-08191 | 329 | 93.0 |
| 08192+ | 39 | 94.9 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 93.4 |
| 03 | 128 | 93.0 |
| 04 | 515 | 92.2 |
| 05 | 224 | 86.6 |
| 06 | 86 | 82.6 |
| 07 | 18 | 66.7 |
| 08 | 4 | 50.0 |

## Paraphrase groups

76 groups; same prediction 77.6%; all correct 85.5%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 4.2 |
| 0.4 | 99.8 | 4.1 |
| 0.5 | 99.2 | 3.9 |
| 0.6 | 96.8 | 2.6 |
| 0.7 | 94.4 | 1.8 |
| 0.8 | 92.7 | 1.5 |
| 0.9 | 87.2 | 0.8 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 382 | 0.042 | 0.008 |
| [0.1,0.2) | 66 | 0.135 | 0.000 |
| [0.2,0.3) | 38 | 0.251 | 0.000 |
| [0.3,0.4) | 26 | 0.345 | 0.077 |
| [0.4,0.5) | 24 | 0.452 | 0.250 |
| [0.5,0.6) | 27 | 0.561 | 0.259 |
| [0.6,0.7) | 29 | 0.661 | 0.517 |
| [0.7,0.8) | 30 | 0.758 | 0.567 |
| [0.8,0.9) | 48 | 0.858 | 0.896 |
| [0.9,1.0] | 346 | 0.964 | 0.988 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 1 | 0.343 | 0.000 |
| [0.4,0.5) | 4 | 0.451 | 0.750 |
| [0.5,0.6) | 14 | 0.538 | 0.429 |
| [0.6,0.7) | 14 | 0.647 | 0.643 |
| [0.7,0.8) | 10 | 0.763 | 0.800 |
| [0.8,0.9) | 33 | 0.853 | 0.879 |
| [0.9,1.0] | 517 | 0.984 | 0.992 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 632 | 0.038 | 0.014 |
| [0.1,0.2) | 92 | 0.137 | 0.000 |
| [0.2,0.3) | 41 | 0.243 | 0.171 |
| [0.3,0.4) | 28 | 0.350 | 0.357 |
| [0.4,0.5) | 27 | 0.451 | 0.259 |
| [0.5,0.6) | 23 | 0.552 | 0.304 |
| [0.6,0.7) | 30 | 0.651 | 0.533 |
| [0.7,0.8) | 61 | 0.751 | 0.754 |
| [0.8,0.9) | 131 | 0.861 | 0.878 |
| [0.9,1.0] | 817 | 0.965 | 0.989 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 91.5%.
Paired vs ours (images_v1/eval2): ours only right 115, imajev-4b only right 23, p = 6.5e-16
