# Evaluation report

- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared document / forked native cache branches), adapter/checkpoint `runs/qwen35_4b_tree_scratch_jevall/adapter`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / bfloat16; 2026-09-27T03:48:44+0000; wall 171.2s

## Overall

question accuracy 95.8%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.968, precision 0.953, recall 0.972, f1 0.962, auroc 0.996, brier 0.026, log_loss 0.104, ece 0.038

**multiclass**: n 593, accuracy 0.970, macro_f1 0.944, log_loss 0.087, brier 0.044, ece_top_label 0.012

**multilabel**: n 382, labels 1882, exact_match 0.914, micro_f1 0.981, macro_f1 0.962, label_auroc 0.997, brier 0.018, log_loss 0.078, ece 0.029

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 94.5 | bin acc 96.6 F1 95.2 AUROC 0.995 ECE 0.048; mc acc 95.9 mF1 90.6 ECE 0.025; ml EM 87.1 µF1 96.5 ECE 0.029 |
| e2_simple | 664 | 98.5 | bin acc 97.4 F1 97.6 AUROC 0.997 ECE 0.037; mc acc 100.0 mF1 100.0 ECE 0.007; ml EM 99.2 µF1 99.9 ECE 0.028 |
| e2_very_hard | 654 | 94.3 | bin acc 96.3 F1 95.2 AUROC 0.996 ECE 0.049; mc acc 95.0 mF1 92.9 ECE 0.026; ml EM 88.5 µF1 97.7 ECE 0.041 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 98.4 |
| contradiction | 172 | 97.7 |
| distractor | 474 | 93.9 |
| double_negation | 126 | 96.8 |
| evidence_end | 57 | 98.2 |
| evidence_middle | 114 | 99.1 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 96.2 |
| hypothetical | 128 | 96.1 |
| injection | 151 | 95.4 |
| lexical_overlap | 201 | 97.0 |
| long_state | 191 | 98.4 |
| missing_evidence | 141 | 96.5 |
| multi_positive | 322 | 91.0 |
| multi_turn | 149 | 92.6 |
| negation | 257 | 98.1 |
| nota | 118 | 95.8 |
| numeric_reasoning | 224 | 87.5 |
| paraphrase | 218 | 93.1 |
| role_reversal | 187 | 94.1 |
| sarcasm | 149 | 96.0 |
| temporal_reasoning | 203 | 88.2 |
| zero_positive | 73 | 94.5 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 94.7 |
| 00128-00511 | 469 | 94.5 |
| 00512-02047 | 488 | 96.5 |
| 02048-08191 | 329 | 98.2 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 96.8 |
| 03 | 128 | 97.7 |
| 04 | 515 | 94.8 |
| 05 | 224 | 93.8 |
| 06 | 86 | 94.2 |
| 07 | 18 | 94.4 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 78.9%; all correct 85.5%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 3.0 |
| 0.4 | 98.8 | 2.2 |
| 0.5 | 98.0 | 2.1 |
| 0.6 | 97.5 | 1.7 |
| 0.7 | 96.8 | 1.2 |
| 0.8 | 94.4 | 0.7 |
| 0.9 | 91.9 | 0.6 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 505 | 0.035 | 0.000 |
| [0.1,0.2) | 29 | 0.139 | 0.069 |
| [0.2,0.3) | 8 | 0.245 | 0.000 |
| [0.3,0.4) | 16 | 0.344 | 0.250 |
| [0.4,0.5) | 14 | 0.447 | 0.429 |
| [0.5,0.6) | 17 | 0.549 | 0.471 |
| [0.6,0.7) | 20 | 0.650 | 0.850 |
| [0.7,0.8) | 15 | 0.751 | 0.867 |
| [0.8,0.9) | 36 | 0.851 | 0.889 |
| [0.9,1.0] | 356 | 0.973 | 0.992 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 7 | 0.354 | 0.286 |
| [0.4,0.5) | 5 | 0.448 | 0.800 |
| [0.5,0.6) | 3 | 0.543 | 0.333 |
| [0.6,0.7) | 4 | 0.668 | 0.250 |
| [0.7,0.8) | 14 | 0.752 | 0.786 |
| [0.8,0.9) | 15 | 0.853 | 0.933 |
| [0.9,1.0] | 545 | 0.993 | 0.994 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 758 | 0.030 | 0.003 |
| [0.1,0.2) | 42 | 0.144 | 0.071 |
| [0.2,0.3) | 23 | 0.251 | 0.261 |
| [0.3,0.4) | 12 | 0.350 | 0.083 |
| [0.4,0.5) | 16 | 0.448 | 0.312 |
| [0.5,0.6) | 16 | 0.549 | 0.562 |
| [0.6,0.7) | 21 | 0.658 | 0.667 |
| [0.7,0.8) | 20 | 0.755 | 0.850 |
| [0.8,0.9) | 58 | 0.848 | 0.948 |
| [0.9,1.0] | 916 | 0.978 | 0.997 |
