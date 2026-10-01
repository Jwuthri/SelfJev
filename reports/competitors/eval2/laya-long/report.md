# Evaluation report

- model `laya-long` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-09-30T17:35:26+0000; wall 108.0s

## Overall

question accuracy 46.9%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.568, precision 0.497, recall 0.839, f1 0.624, auroc 0.663, brier 0.263, log_loss 0.735, ece 0.179

**multiclass**: n 593, accuracy 0.509, macro_f1 0.367, log_loss 1.192, brier 0.635, ece_top_label 0.083

**multilabel**: n 382, labels 1882, exact_match 0.144, micro_f1 0.695, macro_f1 0.541, label_auroc 0.672, brier 0.229, log_loss 0.656, ece 0.057

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 43.4 | bin acc 51.1 F1 54.3 AUROC 0.623 ECE 0.234; mc acc 49.2 mF1 33.7 ECE 0.126; ml EM 14.4 µF1 66.5 ECE 0.088 |
| e2_simple | 664 | 57.1 | bin acc 67.2 F1 74.3 AUROC 0.707 ECE 0.094; mc acc 62.0 mF1 49.6 ECE 0.055; ml EM 20.0 µF1 74.7 ECE 0.061 |
| e2_very_hard | 654 | 40.2 | bin acc 51.9 F1 56.4 AUROC 0.634 ECE 0.224; mc acc 41.5 mF1 26.0 ECE 0.121; ml EM 9.2 µF1 68.0 ECE 0.108 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 60.6 |
| contradiction | 172 | 34.9 |
| distractor | 474 | 39.7 |
| double_negation | 126 | 49.2 |
| evidence_end | 57 | 38.6 |
| evidence_middle | 114 | 36.8 |
| evidence_start | 17 | 29.4 |
| exception | 213 | 39.4 |
| hypothetical | 128 | 42.2 |
| injection | 151 | 35.1 |
| lexical_overlap | 201 | 40.3 |
| long_state | 191 | 35.1 |
| missing_evidence | 141 | 38.3 |
| multi_positive | 322 | 21.1 |
| multi_turn | 149 | 41.6 |
| negation | 257 | 44.4 |
| nota | 118 | 45.8 |
| numeric_reasoning | 224 | 42.9 |
| paraphrase | 218 | 41.3 |
| role_reversal | 187 | 45.5 |
| sarcasm | 149 | 36.9 |
| temporal_reasoning | 203 | 36.0 |
| zero_positive | 73 | 38.4 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 58.9 |
| 00128-00511 | 469 | 43.5 |
| 00512-02047 | 488 | 41.2 |
| 02048-08191 | 329 | 37.1 |
| 08192+ | 39 | 38.5 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 56.8 |
| 03 | 128 | 64.1 |
| 04 | 515 | 43.5 |
| 05 | 224 | 20.1 |
| 06 | 86 | 7.0 |
| 07 | 18 | 0.0 |
| 08 | 4 | 0.0 |

## Paraphrase groups

76 groups; same prediction 69.7%; all correct 28.9%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 49.1 |
| 0.4 | 69.1 | 44.1 |
| 0.5 | 50.8 | 37.2 |
| 0.6 | 35.9 | 33.8 |
| 0.7 | 26.3 | 28.2 |
| 0.8 | 19.2 | 25.4 |
| 0.9 | 9.8 | 22.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 18 | 0.068 | 0.111 |
| [0.1,0.2) | 59 | 0.153 | 0.186 |
| [0.2,0.3) | 64 | 0.251 | 0.188 |
| [0.3,0.4) | 62 | 0.349 | 0.306 |
| [0.4,0.5) | 79 | 0.453 | 0.329 |
| [0.5,0.6) | 141 | 0.557 | 0.376 |
| [0.6,0.7) | 187 | 0.652 | 0.449 |
| [0.7,0.8) | 200 | 0.751 | 0.520 |
| [0.8,0.9) | 170 | 0.845 | 0.571 |
| [0.9,1.0] | 36 | 0.927 | 0.750 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 33 | 0.281 | 0.455 |
| [0.3,0.4) | 150 | 0.353 | 0.387 |
| [0.4,0.5) | 109 | 0.442 | 0.367 |
| [0.5,0.6) | 88 | 0.548 | 0.545 |
| [0.6,0.7) | 57 | 0.644 | 0.509 |
| [0.7,0.8) | 42 | 0.748 | 0.643 |
| [0.8,0.9) | 56 | 0.847 | 0.714 |
| [0.9,1.0] | 58 | 0.953 | 0.776 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 41 | 0.058 | 0.049 |
| [0.1,0.2) | 68 | 0.157 | 0.191 |
| [0.2,0.3) | 109 | 0.252 | 0.330 |
| [0.3,0.4) | 164 | 0.351 | 0.409 |
| [0.4,0.5) | 233 | 0.456 | 0.472 |
| [0.5,0.6) | 320 | 0.550 | 0.519 |
| [0.6,0.7) | 371 | 0.651 | 0.585 |
| [0.7,0.8) | 298 | 0.747 | 0.705 |
| [0.8,0.9) | 212 | 0.840 | 0.750 |
| [0.9,1.0] | 66 | 0.932 | 0.682 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 46.9%.
Paired vs ours (images_v1/eval2): ours only right 995, laya-long only right 15, p = 1.5e-271
