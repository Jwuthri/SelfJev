# Evaluation report

- model `openjev-27b-fp8` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-09-30T20:46:39+0000; wall 753.4s

## Overall

question accuracy 96.8%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.979, precision 0.979, recall 0.972, f1 0.976, auroc 0.998, brier 0.017, log_loss 0.077, ece 0.035

**multiclass**: n 593, accuracy 0.983, macro_f1 0.980, log_loss 0.054, brier 0.026, ece_top_label 0.006

**multilabel**: n 382, labels 1882, exact_match 0.916, micro_f1 0.980, macro_f1 0.963, label_auroc 0.997, brier 0.017, log_loss 0.077, ece 0.028

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 97.0 | bin acc 97.1 F1 96.0 AUROC 0.995 ECE 0.033; mc acc 99.0 mF1 98.2 ECE 0.010; ml EM 93.9 µF1 98.0 ECE 0.030 |
| e2_simple | 664 | 98.8 | bin acc 99.1 F1 99.2 AUROC 1.000 ECE 0.037; mc acc 100.0 mF1 100.0 ECE 0.004; ml EM 95.8 µF1 99.1 ECE 0.033 |
| e2_very_hard | 654 | 94.6 | bin acc 97.5 F1 96.7 AUROC 0.998 ECE 0.045; mc acc 96.0 mF1 94.9 ECE 0.014; ml EM 85.4 µF1 96.9 ECE 0.037 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 98.9 |
| contradiction | 172 | 98.3 |
| distractor | 474 | 95.8 |
| double_negation | 126 | 93.7 |
| evidence_end | 57 | 96.5 |
| evidence_middle | 114 | 97.4 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 95.3 |
| hypothetical | 128 | 100.0 |
| injection | 151 | 91.4 |
| lexical_overlap | 201 | 96.5 |
| long_state | 191 | 97.9 |
| missing_evidence | 141 | 97.2 |
| multi_positive | 322 | 93.2 |
| multi_turn | 149 | 96.6 |
| negation | 257 | 97.7 |
| nota | 118 | 94.1 |
| numeric_reasoning | 224 | 89.3 |
| paraphrase | 218 | 91.3 |
| role_reversal | 187 | 96.8 |
| sarcasm | 149 | 98.0 |
| temporal_reasoning | 203 | 89.7 |
| zero_positive | 73 | 97.3 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 96.7 |
| 00128-00511 | 469 | 94.0 |
| 00512-02047 | 488 | 99.2 |
| 02048-08191 | 329 | 97.3 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 97.9 |
| 03 | 128 | 98.4 |
| 04 | 515 | 97.7 |
| 05 | 224 | 91.5 |
| 06 | 86 | 91.9 |
| 07 | 18 | 94.4 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 84.2%; all correct 88.2%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 1.7 |
| 0.4 | 100.0 | 1.7 |
| 0.5 | 99.3 | 1.2 |
| 0.6 | 99.0 | 1.2 |
| 0.7 | 98.1 | 0.9 |
| 0.8 | 96.5 | 0.5 |
| 0.9 | 94.9 | 0.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 534 | 0.027 | 0.002 |
| [0.1,0.2) | 17 | 0.130 | 0.000 |
| [0.2,0.3) | 14 | 0.250 | 0.214 |
| [0.3,0.4) | 13 | 0.348 | 0.462 |
| [0.4,0.5) | 6 | 0.430 | 0.333 |
| [0.5,0.6) | 4 | 0.550 | 0.750 |
| [0.6,0.7) | 4 | 0.677 | 0.500 |
| [0.7,0.8) | 9 | 0.770 | 1.000 |
| [0.8,0.9) | 31 | 0.864 | 0.839 |
| [0.9,1.0] | 384 | 0.964 | 0.997 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.4,0.5) | 4 | 0.453 | 0.250 |
| [0.5,0.6) | 2 | 0.578 | 1.000 |
| [0.6,0.7) | 5 | 0.648 | 0.600 |
| [0.7,0.8) | 10 | 0.748 | 0.800 |
| [0.8,0.9) | 9 | 0.848 | 0.889 |
| [0.9,1.0] | 563 | 0.995 | 0.996 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 803 | 0.027 | 0.005 |
| [0.1,0.2) | 31 | 0.140 | 0.161 |
| [0.2,0.3) | 10 | 0.237 | 0.600 |
| [0.3,0.4) | 13 | 0.342 | 0.385 |
| [0.4,0.5) | 7 | 0.426 | 0.571 |
| [0.5,0.6) | 7 | 0.560 | 0.714 |
| [0.6,0.7) | 10 | 0.657 | 0.700 |
| [0.7,0.8) | 19 | 0.769 | 0.737 |
| [0.8,0.9) | 38 | 0.872 | 0.868 |
| [0.9,1.0] | 944 | 0.969 | 0.998 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 96.8%.
Paired vs ours (images_v1/eval2): ours only right 34, openjev-27b-fp8 only right 48, p = 0.15
