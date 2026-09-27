# Evaluation report

- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared document / forked native cache branches), adapter/checkpoint `runs/qwen35_4b_tree_scratch_jevall/adapter_last`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / bfloat16; 2026-09-27T04:01:51+0000; wall 169.8s

## Overall

question accuracy 95.6%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.968, precision 0.953, recall 0.972, f1 0.962, auroc 0.996, brier 0.025, log_loss 0.104, ece 0.037

**multiclass**: n 593, accuracy 0.966, macro_f1 0.938, log_loss 0.087, brier 0.044, ece_top_label 0.015

**multilabel**: n 382, labels 1882, exact_match 0.911, micro_f1 0.980, macro_f1 0.960, label_auroc 0.997, brier 0.018, log_loss 0.078, ece 0.029

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 94.4 | bin acc 96.6 F1 95.2 AUROC 0.995 ECE 0.050; mc acc 95.3 mF1 90.0 ECE 0.023; ml EM 87.1 µF1 96.4 ECE 0.029 |
| e2_simple | 664 | 98.5 | bin acc 97.4 F1 97.6 AUROC 0.997 ECE 0.034; mc acc 100.0 mF1 100.0 ECE 0.007; ml EM 99.2 µF1 99.9 ECE 0.028 |
| e2_very_hard | 654 | 94.0 | bin acc 96.3 F1 95.2 AUROC 0.996 ECE 0.051; mc acc 94.5 mF1 91.7 ECE 0.020; ml EM 87.7 µF1 97.6 ECE 0.039 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 98.4 |
| contradiction | 172 | 97.1 |
| distractor | 474 | 93.7 |
| double_negation | 126 | 96.8 |
| evidence_end | 57 | 98.2 |
| evidence_middle | 114 | 99.1 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 96.2 |
| hypothetical | 128 | 96.1 |
| injection | 151 | 95.4 |
| lexical_overlap | 201 | 96.5 |
| long_state | 191 | 98.4 |
| missing_evidence | 141 | 96.5 |
| multi_positive | 322 | 91.0 |
| multi_turn | 149 | 92.6 |
| negation | 257 | 98.1 |
| nota | 118 | 94.9 |
| numeric_reasoning | 224 | 87.1 |
| paraphrase | 218 | 92.2 |
| role_reversal | 187 | 93.6 |
| sarcasm | 149 | 96.0 |
| temporal_reasoning | 203 | 87.2 |
| zero_positive | 73 | 94.5 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 94.6 |
| 00128-00511 | 469 | 94.0 |
| 00512-02047 | 488 | 96.5 |
| 02048-08191 | 329 | 98.2 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 96.8 |
| 03 | 128 | 96.9 |
| 04 | 515 | 94.6 |
| 05 | 224 | 93.3 |
| 06 | 86 | 94.2 |
| 07 | 18 | 94.4 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 77.6%; all correct 84.2%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 3.4 |
| 0.4 | 98.8 | 2.4 |
| 0.5 | 98.0 | 2.1 |
| 0.6 | 97.5 | 1.7 |
| 0.7 | 97.0 | 1.2 |
| 0.8 | 94.4 | 0.9 |
| 0.9 | 91.7 | 0.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 507 | 0.035 | 0.000 |
| [0.1,0.2) | 26 | 0.138 | 0.077 |
| [0.2,0.3) | 9 | 0.242 | 0.000 |
| [0.3,0.4) | 17 | 0.346 | 0.235 |
| [0.4,0.5) | 13 | 0.450 | 0.462 |
| [0.5,0.6) | 15 | 0.544 | 0.467 |
| [0.6,0.7) | 21 | 0.643 | 0.810 |
| [0.7,0.8) | 16 | 0.750 | 0.875 |
| [0.8,0.9) | 37 | 0.853 | 0.892 |
| [0.9,1.0] | 355 | 0.974 | 0.992 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 1 | 0.297 | 0.000 |
| [0.3,0.4) | 6 | 0.365 | 0.167 |
| [0.4,0.5) | 5 | 0.446 | 0.600 |
| [0.5,0.6) | 3 | 0.541 | 0.333 |
| [0.6,0.7) | 3 | 0.667 | 0.000 |
| [0.7,0.8) | 15 | 0.750 | 0.867 |
| [0.8,0.9) | 16 | 0.857 | 0.812 |
| [0.9,1.0] | 544 | 0.993 | 0.996 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 758 | 0.030 | 0.003 |
| [0.1,0.2) | 42 | 0.143 | 0.071 |
| [0.2,0.3) | 23 | 0.252 | 0.261 |
| [0.3,0.4) | 13 | 0.351 | 0.231 |
| [0.4,0.5) | 13 | 0.443 | 0.231 |
| [0.5,0.6) | 17 | 0.537 | 0.471 |
| [0.6,0.7) | 23 | 0.658 | 0.696 |
| [0.7,0.8) | 23 | 0.765 | 0.870 |
| [0.8,0.9) | 54 | 0.853 | 0.944 |
| [0.9,1.0] | 916 | 0.978 | 0.997 |
