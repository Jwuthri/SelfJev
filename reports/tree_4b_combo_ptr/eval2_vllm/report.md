# Evaluation report

- model `Qwen/Qwen3-4B-Instruct-2507` @ `cdbee75f17` (tree paths (tree-v1) on vLLM), adapter/checkpoint `merged into runs/tree_4b_combo_ptr/merged`, prompt `tree-v1` (c8963d819128)
- data data/ptr/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / bfloat16; 2026-09-25T00:59:00+0000; wall 140.1s

## Overall

question accuracy 91.9%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.948, precision 0.938, recall 0.940, f1 0.939, auroc 0.990, brier 0.038, log_loss 0.129, ece 0.015

**multiclass**: n 593, accuracy 0.941, macro_f1 0.903, log_loss 0.158, brier 0.079, ece_top_label 0.018

**multilabel**: n 382, labels 1882, exact_match 0.809, micro_f1 0.952, macro_f1 0.915, label_auroc 0.988, brier 0.038, log_loss 0.136, ece 0.011

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 90.2 | bin acc 95.1 F1 93.3 AUROC 0.986 ECE 0.036; mc acc 90.7 mF1 84.4 ECE 0.035; ml EM 76.5 µF1 93.5 ECE 0.012 |
| e2_simple | 664 | 96.7 | bin acc 97.7 F1 97.9 AUROC 0.996 ECE 0.016; mc acc 98.0 mF1 96.5 ECE 0.016; ml EM 91.7 µF1 98.1 ECE 0.014 |
| e2_very_hard | 654 | 88.8 | bin acc 91.4 F1 88.4 AUROC 0.982 ECE 0.029; mc acc 93.5 mF1 89.4 ECE 0.033; ml EM 75.4 µF1 94.1 ECE 0.018 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.4 |
| contradiction | 172 | 94.2 |
| distractor | 474 | 89.9 |
| double_negation | 126 | 87.3 |
| evidence_end | 57 | 93.0 |
| evidence_middle | 114 | 94.7 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 88.3 |
| hypothetical | 128 | 94.5 |
| injection | 151 | 86.8 |
| lexical_overlap | 201 | 94.5 |
| long_state | 191 | 93.2 |
| missing_evidence | 141 | 95.7 |
| multi_positive | 322 | 81.4 |
| multi_turn | 149 | 91.9 |
| negation | 257 | 91.4 |
| nota | 118 | 88.1 |
| numeric_reasoning | 224 | 80.4 |
| paraphrase | 218 | 87.6 |
| role_reversal | 187 | 89.3 |
| sarcasm | 149 | 91.9 |
| temporal_reasoning | 203 | 81.3 |
| zero_positive | 73 | 90.4 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 662 | 90.6 |
| 00128-00511 | 477 | 88.7 |
| 00512-02047 | 484 | 94.6 |
| 02048-08191 | 329 | 95.1 |
| 08192+ | 39 | 92.3 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 94.8 |
| 03 | 128 | 93.0 |
| 04 | 515 | 91.1 |
| 05 | 224 | 87.1 |
| 06 | 86 | 76.7 |
| 07 | 18 | 83.3 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 73.7%; all correct 76.3%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 5.9 |
| 0.4 | 98.3 | 4.8 |
| 0.5 | 97.0 | 4.2 |
| 0.6 | 94.9 | 3.0 |
| 0.7 | 93.3 | 1.8 |
| 0.8 | 90.7 | 0.9 |
| 0.9 | 85.7 | 0.8 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 514 | 0.008 | 0.006 |
| [0.1,0.2) | 18 | 0.143 | 0.222 |
| [0.2,0.3) | 10 | 0.250 | 0.300 |
| [0.3,0.4) | 17 | 0.355 | 0.412 |
| [0.4,0.5) | 21 | 0.457 | 0.429 |
| [0.5,0.6) | 20 | 0.564 | 0.650 |
| [0.6,0.7) | 22 | 0.652 | 0.727 |
| [0.7,0.8) | 23 | 0.756 | 0.696 |
| [0.8,0.9) | 40 | 0.856 | 0.925 |
| [0.9,1.0] | 331 | 0.978 | 0.988 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 10 | 0.357 | 0.300 |
| [0.4,0.5) | 8 | 0.484 | 0.500 |
| [0.5,0.6) | 12 | 0.546 | 0.417 |
| [0.6,0.7) | 10 | 0.646 | 0.300 |
| [0.7,0.8) | 15 | 0.747 | 0.667 |
| [0.8,0.9) | 30 | 0.864 | 0.967 |
| [0.9,1.0] | 508 | 0.991 | 0.992 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 759 | 0.013 | 0.018 |
| [0.1,0.2) | 33 | 0.144 | 0.152 |
| [0.2,0.3) | 25 | 0.254 | 0.400 |
| [0.3,0.4) | 21 | 0.351 | 0.286 |
| [0.4,0.5) | 28 | 0.451 | 0.643 |
| [0.5,0.6) | 25 | 0.558 | 0.600 |
| [0.6,0.7) | 32 | 0.643 | 0.656 |
| [0.7,0.8) | 30 | 0.749 | 0.833 |
| [0.8,0.9) | 39 | 0.860 | 0.897 |
| [0.9,1.0] | 890 | 0.985 | 0.984 |
