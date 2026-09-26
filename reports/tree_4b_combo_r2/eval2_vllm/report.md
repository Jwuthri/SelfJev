# Evaluation report

- model `Qwen/Qwen3-4B-Instruct-2507` @ `cdbee75f17` (tree paths (tree-v1) on vLLM), adapter/checkpoint `merged into runs/tree_4b_combo_r2/merged`, prompt `tree-v1` (c8963d819128)
- data data/ova/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / bfloat16; 2026-09-24T21:51:09+0000; wall 143.6s

## Overall

question accuracy 93.0%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.946, precision 0.934, recall 0.940, f1 0.937, auroc 0.989, brier 0.039, log_loss 0.132, ece 0.007

**multiclass**: n 593, accuracy 0.958, macro_f1 0.931, log_loss 0.120, brier 0.062, ece_top_label 0.011

**multilabel**: n 382, labels 1882, exact_match 0.846, micro_f1 0.958, macro_f1 0.925, label_auroc 0.993, brier 0.034, log_loss 0.116, ece 0.019

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 90.8 | bin acc 93.7 F1 91.5 AUROC 0.981 ECE 0.014; mc acc 94.3 mF1 89.2 ECE 0.020; ml EM 78.0 µF1 93.3 ECE 0.035 |
| e2_simple | 664 | 97.4 | bin acc 97.4 F1 97.6 AUROC 0.996 ECE 0.013; mc acc 100.0 mF1 100.0 ECE 0.012; ml EM 93.3 µF1 98.7 ECE 0.018 |
| e2_very_hard | 654 | 90.8 | bin acc 92.6 F1 90.1 AUROC 0.986 ECE 0.024; mc acc 93.0 mF1 90.0 ECE 0.035; ml EM 83.1 µF1 95.4 ECE 0.017 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.9 |
| contradiction | 172 | 95.3 |
| distractor | 474 | 90.9 |
| double_negation | 126 | 93.7 |
| evidence_end | 57 | 94.7 |
| evidence_middle | 114 | 97.4 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 89.7 |
| hypothetical | 128 | 93.0 |
| injection | 151 | 87.4 |
| lexical_overlap | 201 | 96.0 |
| long_state | 191 | 95.3 |
| missing_evidence | 141 | 97.2 |
| multi_positive | 322 | 85.7 |
| multi_turn | 149 | 93.3 |
| negation | 257 | 96.5 |
| nota | 118 | 89.8 |
| numeric_reasoning | 224 | 82.1 |
| paraphrase | 218 | 86.2 |
| role_reversal | 187 | 93.0 |
| sarcasm | 149 | 91.3 |
| temporal_reasoning | 203 | 76.4 |
| zero_positive | 73 | 91.8 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 662 | 92.4 |
| 00128-00511 | 477 | 88.5 |
| 00512-02047 | 484 | 95.7 |
| 02048-08191 | 329 | 96.0 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 94.6 |
| 03 | 128 | 94.5 |
| 04 | 515 | 93.8 |
| 05 | 224 | 86.2 |
| 06 | 86 | 83.7 |
| 07 | 18 | 100.0 |
| 08 | 4 | 100.0 |

## Paraphrase groups

76 groups; same prediction 73.7%; all correct 78.9%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 4.2 |
| 0.4 | 99.7 | 3.9 |
| 0.5 | 98.3 | 3.1 |
| 0.6 | 97.5 | 2.8 |
| 0.7 | 96.1 | 2.3 |
| 0.8 | 94.6 | 1.8 |
| 0.9 | 91.4 | 0.7 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 508 | 0.007 | 0.008 |
| [0.1,0.2) | 26 | 0.129 | 0.154 |
| [0.2,0.3) | 13 | 0.245 | 0.308 |
| [0.3,0.4) | 11 | 0.350 | 0.545 |
| [0.4,0.5) | 20 | 0.456 | 0.400 |
| [0.5,0.6) | 10 | 0.565 | 0.600 |
| [0.6,0.7) | 26 | 0.650 | 0.654 |
| [0.7,0.8) | 19 | 0.744 | 0.737 |
| [0.8,0.9) | 38 | 0.862 | 0.868 |
| [0.9,1.0] | 345 | 0.980 | 0.983 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 2 | 0.351 | 0.000 |
| [0.4,0.5) | 8 | 0.457 | 0.375 |
| [0.5,0.6) | 5 | 0.549 | 0.600 |
| [0.6,0.7) | 8 | 0.665 | 0.625 |
| [0.7,0.8) | 9 | 0.751 | 0.667 |
| [0.8,0.9) | 19 | 0.866 | 0.684 |
| [0.9,1.0] | 542 | 0.994 | 0.993 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 780 | 0.006 | 0.015 |
| [0.1,0.2) | 31 | 0.140 | 0.387 |
| [0.2,0.3) | 28 | 0.249 | 0.464 |
| [0.3,0.4) | 19 | 0.343 | 0.316 |
| [0.4,0.5) | 14 | 0.452 | 0.500 |
| [0.5,0.6) | 28 | 0.544 | 0.679 |
| [0.6,0.7) | 27 | 0.640 | 0.778 |
| [0.7,0.8) | 21 | 0.758 | 0.667 |
| [0.8,0.9) | 50 | 0.855 | 0.880 |
| [0.9,1.0] | 884 | 0.989 | 0.992 |
