# Evaluation report

- model `Qwen/Qwen3-4B-Instruct-2507` @ `cdbee75f17` (tree paths (tree-v1) on vLLM), adapter/checkpoint `merged into runs/tree_4b_combo/merged`, prompt `tree-v1` (c8963d819128)
- data data/ova/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / bfloat16; 2026-09-26T08:34:25+0000; wall 18.5s

## Overall

question accuracy 94.4%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.961, precision 0.960, recall 0.947, f1 0.954, auroc 0.992, brier 0.032, log_loss 0.112, ece 0.021

**multiclass**: n 593, accuracy 0.973, macro_f1 0.949, log_loss 0.082, brier 0.043, ece_top_label 0.008

**multilabel**: n 382, labels 1882, exact_match 0.856, micro_f1 0.966, macro_f1 0.937, label_auroc 0.995, brier 0.025, log_loss 0.087, ece 0.012

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 93.9 | bin acc 96.8 F1 95.5 AUROC 0.988 ECE 0.040; mc acc 96.4 mF1 92.7 ECE 0.022; ml EM 82.6 µF1 95.3 ECE 0.020 |
| e2_simple | 664 | 96.8 | bin acc 96.5 F1 96.8 AUROC 0.997 ECE 0.019; mc acc 99.0 mF1 97.8 ECE 0.010; ml EM 94.2 µF1 98.7 ECE 0.015 |
| e2_very_hard | 654 | 92.5 | bin acc 94.8 F1 92.9 AUROC 0.990 ECE 0.023; mc acc 96.5 mF1 94.3 ECE 0.010; ml EM 80.8 µF1 95.9 ECE 0.018 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.4 |
| contradiction | 172 | 95.9 |
| distractor | 474 | 92.6 |
| double_negation | 126 | 96.0 |
| evidence_end | 57 | 94.7 |
| evidence_middle | 114 | 97.4 |
| evidence_start | 17 | 94.1 |
| exception | 213 | 90.1 |
| hypothetical | 128 | 93.8 |
| injection | 151 | 94.0 |
| lexical_overlap | 201 | 96.5 |
| long_state | 191 | 94.8 |
| missing_evidence | 141 | 97.9 |
| multi_positive | 322 | 86.6 |
| multi_turn | 149 | 94.0 |
| negation | 257 | 97.7 |
| nota | 118 | 94.1 |
| numeric_reasoning | 224 | 86.6 |
| paraphrase | 218 | 90.8 |
| role_reversal | 187 | 94.7 |
| sarcasm | 149 | 91.3 |
| temporal_reasoning | 203 | 85.2 |
| zero_positive | 73 | 95.9 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 662 | 94.0 |
| 00128-00511 | 477 | 92.2 |
| 00512-02047 | 484 | 95.7 |
| 02048-08191 | 329 | 96.0 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 96.1 |
| 03 | 128 | 97.7 |
| 04 | 515 | 94.2 |
| 05 | 224 | 91.1 |
| 06 | 86 | 82.6 |
| 07 | 18 | 88.9 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 76.3%; all correct 82.9%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 2.7 |
| 0.4 | 99.7 | 2.5 |
| 0.5 | 98.1 | 1.9 |
| 0.6 | 96.5 | 1.4 |
| 0.7 | 94.9 | 1.1 |
| 0.8 | 93.4 | 0.7 |
| 0.9 | 90.9 | 0.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 528 | 0.004 | 0.011 |
| [0.1,0.2) | 10 | 0.142 | 0.400 |
| [0.2,0.3) | 14 | 0.252 | 0.143 |
| [0.3,0.4) | 11 | 0.344 | 0.364 |
| [0.4,0.5) | 24 | 0.450 | 0.292 |
| [0.5,0.6) | 18 | 0.556 | 0.667 |
| [0.6,0.7) | 11 | 0.649 | 0.818 |
| [0.7,0.8) | 14 | 0.764 | 0.857 |
| [0.8,0.9) | 20 | 0.853 | 0.750 |
| [0.9,1.0] | 366 | 0.989 | 0.995 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 2 | 0.361 | 0.500 |
| [0.4,0.5) | 9 | 0.453 | 0.556 |
| [0.5,0.6) | 10 | 0.556 | 0.700 |
| [0.6,0.7) | 9 | 0.644 | 0.778 |
| [0.7,0.8) | 9 | 0.759 | 0.778 |
| [0.8,0.9) | 15 | 0.863 | 0.867 |
| [0.9,1.0] | 539 | 0.995 | 0.996 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 787 | 0.006 | 0.009 |
| [0.1,0.2) | 25 | 0.142 | 0.240 |
| [0.2,0.3) | 19 | 0.259 | 0.421 |
| [0.3,0.4) | 25 | 0.344 | 0.520 |
| [0.4,0.5) | 8 | 0.457 | 0.500 |
| [0.5,0.6) | 21 | 0.547 | 0.381 |
| [0.6,0.7) | 17 | 0.655 | 0.882 |
| [0.7,0.8) | 29 | 0.745 | 0.759 |
| [0.8,0.9) | 32 | 0.857 | 0.938 |
| [0.9,1.0] | 919 | 0.993 | 0.992 |
