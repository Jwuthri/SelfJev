# Evaluation report

- model `Qwen/Qwen3-4B-Instruct-2507` @ `cdbee75f17` (tree paths (tree-v1) on vLLM), adapter/checkpoint `merged into runs/tree_4b_combo/merged`, prompt `tree-v1` (c8963d819128)
- data data/ova/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / bfloat16; 2026-09-26T08:35:57+0000; wall 16.2s

## Overall

question accuracy 94.5%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.960, precision 0.962, recall 0.943, f1 0.952, auroc 0.992, brier 0.033, log_loss 0.116, ece 0.018

**multiclass**: n 593, accuracy 0.970, macro_f1 0.943, log_loss 0.085, brier 0.045, ece_top_label 0.010

**multilabel**: n 382, labels 1882, exact_match 0.866, micro_f1 0.967, macro_f1 0.935, label_auroc 0.996, brier 0.026, log_loss 0.086, ece 0.012

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 93.8 | bin acc 96.8 F1 95.5 AUROC 0.988 ECE 0.039; mc acc 95.9 mF1 92.1 ECE 0.020; ml EM 82.6 µF1 94.8 ECE 0.023 |
| e2_simple | 664 | 96.7 | bin acc 96.5 F1 96.8 AUROC 0.997 ECE 0.020; mc acc 98.5 mF1 96.8 ECE 0.016; ml EM 94.2 µF1 98.8 ECE 0.014 |
| e2_very_hard | 654 | 93.0 | bin acc 94.4 F1 92.4 AUROC 0.990 ECE 0.023; mc acc 96.5 mF1 94.3 ECE 0.014; ml EM 83.8 µF1 96.3 ECE 0.018 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.0 |
| contradiction | 172 | 96.5 |
| distractor | 474 | 93.5 |
| double_negation | 126 | 96.8 |
| evidence_end | 57 | 96.5 |
| evidence_middle | 114 | 96.5 |
| evidence_start | 17 | 94.1 |
| exception | 213 | 91.1 |
| hypothetical | 128 | 94.5 |
| injection | 151 | 95.4 |
| lexical_overlap | 201 | 97.5 |
| long_state | 191 | 95.3 |
| missing_evidence | 141 | 97.9 |
| multi_positive | 322 | 87.0 |
| multi_turn | 149 | 94.0 |
| negation | 257 | 97.7 |
| nota | 118 | 93.2 |
| numeric_reasoning | 224 | 87.5 |
| paraphrase | 218 | 91.7 |
| role_reversal | 187 | 93.6 |
| sarcasm | 149 | 91.9 |
| temporal_reasoning | 203 | 85.7 |
| zero_positive | 73 | 97.3 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 662 | 93.2 |
| 00128-00511 | 477 | 93.1 |
| 00512-02047 | 484 | 95.7 |
| 02048-08191 | 329 | 97.0 |
| 08192+ | 39 | 97.4 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 96.0 |
| 03 | 128 | 96.9 |
| 04 | 515 | 93.8 |
| 05 | 224 | 91.1 |
| 06 | 86 | 88.4 |
| 07 | 18 | 88.9 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 76.3%; all correct 82.9%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 3.0 |
| 0.4 | 99.7 | 2.9 |
| 0.5 | 98.3 | 2.1 |
| 0.6 | 97.0 | 1.7 |
| 0.7 | 94.8 | 1.1 |
| 0.8 | 93.6 | 0.9 |
| 0.9 | 91.1 | 0.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 531 | 0.004 | 0.015 |
| [0.1,0.2) | 9 | 0.142 | 0.111 |
| [0.2,0.3) | 14 | 0.244 | 0.214 |
| [0.3,0.4) | 16 | 0.349 | 0.438 |
| [0.4,0.5) | 20 | 0.445 | 0.300 |
| [0.5,0.6) | 21 | 0.541 | 0.762 |
| [0.6,0.7) | 8 | 0.658 | 0.750 |
| [0.7,0.8) | 11 | 0.748 | 0.818 |
| [0.8,0.9) | 26 | 0.856 | 0.846 |
| [0.9,1.0] | 360 | 0.989 | 0.992 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 2 | 0.361 | 0.500 |
| [0.4,0.5) | 8 | 0.464 | 0.375 |
| [0.5,0.6) | 8 | 0.553 | 0.750 |
| [0.6,0.7) | 13 | 0.629 | 0.692 |
| [0.7,0.8) | 7 | 0.753 | 0.857 |
| [0.8,0.9) | 15 | 0.849 | 0.800 |
| [0.9,1.0] | 540 | 0.995 | 0.996 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 791 | 0.006 | 0.011 |
| [0.1,0.2) | 20 | 0.146 | 0.150 |
| [0.2,0.3) | 24 | 0.245 | 0.542 |
| [0.3,0.4) | 17 | 0.353 | 0.471 |
| [0.4,0.5) | 23 | 0.450 | 0.435 |
| [0.5,0.6) | 12 | 0.542 | 0.417 |
| [0.6,0.7) | 21 | 0.647 | 0.762 |
| [0.7,0.8) | 27 | 0.741 | 0.815 |
| [0.8,0.9) | 34 | 0.860 | 0.941 |
| [0.9,1.0] | 913 | 0.992 | 0.993 |
