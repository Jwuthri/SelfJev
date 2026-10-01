# Evaluation report

- model `selfjev-verdict-json-only-v1-api` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-10-01T22:05:22+0000; wall 346.6s

## Overall

question accuracy 94.1%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.961, precision 0.928, recall 0.984, f1 0.955, auroc 0.994, brier 0.030, log_loss 0.112, ece 0.030

**multiclass**: n 593, accuracy 0.970, macro_f1 0.947, log_loss 0.094, brier 0.047, ece_top_label 0.013

**multilabel**: n 382, labels 1882, exact_match 0.843, micro_f1 0.965, macro_f1 0.940, label_auroc 0.994, brier 0.029, log_loss 0.104, ece 0.022

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 93.2 | bin acc 95.4 F1 93.8 AUROC 0.993 ECE 0.036; mc acc 95.9 mF1 91.0 ECE 0.019; ml EM 83.3 µF1 95.4 ECE 0.034 |
| e2_simple | 664 | 97.3 | bin acc 97.4 F1 97.6 AUROC 0.994 ECE 0.029; mc acc 100.0 mF1 100.0 ECE 0.008; ml EM 92.5 µF1 98.7 ECE 0.020 |
| e2_very_hard | 654 | 91.7 | bin acc 95.4 F1 94.2 AUROC 0.993 ECE 0.034; mc acc 95.0 mF1 93.1 ECE 0.037; ml EM 77.7 µF1 95.4 ECE 0.023 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.5 |
| contradiction | 172 | 94.8 |
| distractor | 474 | 92.8 |
| double_negation | 126 | 96.8 |
| evidence_end | 57 | 98.2 |
| evidence_middle | 114 | 96.5 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 92.0 |
| hypothetical | 128 | 93.8 |
| injection | 151 | 96.0 |
| lexical_overlap | 201 | 95.0 |
| long_state | 191 | 96.9 |
| missing_evidence | 141 | 95.7 |
| multi_positive | 322 | 86.3 |
| multi_turn | 149 | 92.6 |
| negation | 257 | 95.7 |
| nota | 118 | 87.3 |
| numeric_reasoning | 224 | 85.7 |
| paraphrase | 218 | 90.4 |
| role_reversal | 187 | 94.7 |
| sarcasm | 149 | 94.0 |
| temporal_reasoning | 203 | 80.8 |
| zero_positive | 73 | 93.2 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 93.2 |
| 00128-00511 | 469 | 92.8 |
| 00512-02047 | 488 | 95.1 |
| 02048-08191 | 329 | 95.4 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 96.1 |
| 03 | 128 | 96.9 |
| 04 | 515 | 94.2 |
| 05 | 224 | 88.4 |
| 06 | 86 | 83.7 |
| 07 | 18 | 83.3 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 76.3%; all correct 85.5%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 3.0 |
| 0.4 | 99.8 | 2.9 |
| 0.5 | 98.5 | 2.6 |
| 0.6 | 97.1 | 1.7 |
| 0.7 | 96.3 | 1.2 |
| 0.8 | 94.3 | 0.9 |
| 0.9 | 92.1 | 0.5 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 497 | 0.017 | 0.002 |
| [0.1,0.2) | 30 | 0.142 | 0.000 |
| [0.2,0.3) | 12 | 0.244 | 0.167 |
| [0.3,0.4) | 9 | 0.345 | 0.222 |
| [0.4,0.5) | 7 | 0.443 | 0.286 |
| [0.5,0.6) | 7 | 0.546 | 0.286 |
| [0.6,0.7) | 13 | 0.668 | 0.615 |
| [0.7,0.8) | 15 | 0.754 | 0.667 |
| [0.8,0.9) | 23 | 0.866 | 0.696 |
| [0.9,1.0] | 403 | 0.991 | 0.973 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 1 | 0.382 | 0.000 |
| [0.4,0.5) | 8 | 0.452 | 0.750 |
| [0.5,0.6) | 8 | 0.556 | 0.375 |
| [0.6,0.7) | 5 | 0.648 | 0.400 |
| [0.7,0.8) | 12 | 0.747 | 0.833 |
| [0.8,0.9) | 13 | 0.870 | 0.846 |
| [0.9,1.0] | 546 | 0.993 | 0.995 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 720 | 0.021 | 0.011 |
| [0.1,0.2) | 44 | 0.140 | 0.068 |
| [0.2,0.3) | 30 | 0.247 | 0.067 |
| [0.3,0.4) | 16 | 0.352 | 0.125 |
| [0.4,0.5) | 16 | 0.459 | 0.375 |
| [0.5,0.6) | 21 | 0.536 | 0.333 |
| [0.6,0.7) | 15 | 0.650 | 0.333 |
| [0.7,0.8) | 26 | 0.752 | 0.615 |
| [0.8,0.9) | 32 | 0.855 | 0.812 |
| [0.9,1.0] | 962 | 0.994 | 0.988 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 94.1%.
Paired vs ours (images_v1/eval2): ours only right 61, selfjev-verdict-json-only-v1-api only right 20, p = 5.7e-06
