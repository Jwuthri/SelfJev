# Evaluation report

- model `ours-LoRA` @ `-` (stock reranker pairs), adapter/checkpoint `None`, prompt `ours-LoRA` (-)
- data reports/external/eval2/subset.jsonl; splits ['test']; n=1991; calibration `None`
- - / -; 2026-09-23T22:59:31-0700; wall 0.0s

## Overall

question accuracy 85.1%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.894, precision 0.856, recall 0.903, f1 0.879, auroc 0.959, brier 0.078, log_loss 0.259, ece 0.022

**multiclass**: n 593, accuracy 0.916, macro_f1 0.847, log_loss 0.248, brier 0.125, ece_top_label 0.022

**multilabel**: n 382, labels 1882, exact_match 0.639, micro_f1 0.894, macro_f1 0.818, label_auroc 0.958, brier 0.083, log_loss 0.281, ece 0.052

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 83.2 | bin acc 86.8 F1 82.6 AUROC 0.938 ECE 0.052; mc acc 88.6 mF1 79.5 ECE 0.027; ml EM 65.9 µF1 89.2 ECE 0.038 |
| e2_simple | 664 | 92.3 | bin acc 96.2 F1 96.5 AUROC 0.985 ECE 0.039; mc acc 98.5 mF1 96.8 ECE 0.034; ml EM 70.8 µF1 92.0 ECE 0.092 |
| e2_very_hard | 654 | 79.8 | bin acc 84.9 F1 80.8 AUROC 0.933 ECE 0.042; mc acc 87.5 mF1 77.5 ECE 0.054; ml EM 55.4 µF1 87.3 ECE 0.057 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 94.4 |
| contradiction | 172 | 86.0 |
| distractor | 474 | 80.4 |
| double_negation | 126 | 85.7 |
| evidence_end | 57 | 82.5 |
| evidence_middle | 114 | 87.7 |
| evidence_start | 17 | 76.5 |
| exception | 213 | 78.4 |
| hypothetical | 128 | 92.2 |
| injection | 151 | 71.5 |
| lexical_overlap | 201 | 88.6 |
| long_state | 191 | 82.7 |
| missing_evidence | 141 | 92.9 |
| multi_positive | 322 | 66.8 |
| multi_turn | 149 | 83.9 |
| negation | 257 | 83.3 |
| nota | 118 | 83.1 |
| numeric_reasoning | 224 | 67.0 |
| paraphrase | 218 | 83.5 |
| role_reversal | 187 | 86.6 |
| sarcasm | 149 | 71.8 |
| temporal_reasoning | 203 | 69.5 |
| zero_positive | 73 | 80.8 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 662 | 85.0 |
| 00128-00511 | 477 | 81.6 |
| 00512-02047 | 484 | 89.5 |
| 02048-08191 | 329 | 84.2 |
| 08192+ | 39 | 84.6 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 89.4 |
| 03 | 128 | 87.5 |
| 04 | 515 | 87.8 |
| 05 | 224 | 70.1 |
| 06 | 86 | 62.8 |
| 07 | 18 | 55.6 |
| 08 | 4 | 50.0 |

## Paraphrase groups

76 groups; same prediction 65.8%; all correct 68.4%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 8.4 |
| 0.4 | 99.0 | 7.5 |
| 0.5 | 97.3 | 6.6 |
| 0.6 | 94.1 | 5.9 |
| 0.7 | 90.1 | 4.5 |
| 0.8 | 84.8 | 2.8 |
| 0.9 | 78.1 | 1.9 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 431 | 0.020 | 0.023 |
| [0.1,0.2) | 49 | 0.133 | 0.163 |
| [0.2,0.3) | 19 | 0.251 | 0.263 |
| [0.3,0.4) | 37 | 0.351 | 0.297 |
| [0.4,0.5) | 21 | 0.456 | 0.381 |
| [0.5,0.6) | 28 | 0.538 | 0.607 |
| [0.6,0.7) | 31 | 0.651 | 0.452 |
| [0.7,0.8) | 34 | 0.756 | 0.676 |
| [0.8,0.9) | 84 | 0.858 | 0.833 |
| [0.9,1.0] | 282 | 0.965 | 0.954 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 6 | 0.366 | 0.000 |
| [0.4,0.5) | 10 | 0.461 | 0.400 |
| [0.5,0.6) | 19 | 0.552 | 0.737 |
| [0.6,0.7) | 24 | 0.641 | 0.625 |
| [0.7,0.8) | 31 | 0.756 | 0.677 |
| [0.8,0.9) | 40 | 0.850 | 0.875 |
| [0.9,1.0] | 463 | 0.987 | 0.981 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 691 | 0.017 | 0.045 |
| [0.1,0.2) | 91 | 0.143 | 0.330 |
| [0.2,0.3) | 54 | 0.249 | 0.444 |
| [0.3,0.4) | 34 | 0.353 | 0.647 |
| [0.4,0.5) | 42 | 0.453 | 0.619 |
| [0.5,0.6) | 48 | 0.550 | 0.625 |
| [0.6,0.7) | 69 | 0.650 | 0.797 |
| [0.7,0.8) | 98 | 0.753 | 0.888 |
| [0.8,0.9) | 142 | 0.860 | 0.880 |
| [0.9,1.0] | 613 | 0.963 | 0.971 |
