# Evaluation report

- model `plumb-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-09-30T18:54:27+0000; wall 471.2s

## Overall

question accuracy 93.4%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.955, precision 0.947, recall 0.947, f1 0.947, auroc 0.990, brier 0.035, log_loss 0.141, ece 0.042

**multiclass**: n 593, accuracy 0.970, macro_f1 0.951, log_loss 0.117, brier 0.049, ece_top_label 0.037

**multilabel**: n 382, labels 1882, exact_match 0.822, micro_f1 0.956, macro_f1 0.918, label_auroc 0.987, brier 0.038, log_loss 0.146, ece 0.031

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 90.9 | bin acc 94.8 F1 92.8 AUROC 0.985 ECE 0.048; mc acc 95.3 mF1 90.8 ECE 0.056; ml EM 74.2 µF1 93.2 ECE 0.035 |
| e2_simple | 664 | 96.8 | bin acc 96.2 F1 96.6 AUROC 0.990 ECE 0.051; mc acc 99.5 mF1 98.9 ECE 0.043; ml EM 94.2 µF1 98.7 ECE 0.053 |
| e2_very_hard | 654 | 92.4 | bin acc 95.4 F1 93.8 AUROC 0.993 ECE 0.050; mc acc 96.0 mF1 94.7 ECE 0.043; ml EM 79.2 µF1 94.9 ECE 0.027 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.2 |
| contradiction | 172 | 97.1 |
| distractor | 474 | 91.6 |
| double_negation | 126 | 90.5 |
| evidence_end | 57 | 96.5 |
| evidence_middle | 114 | 96.5 |
| evidence_start | 17 | 94.1 |
| exception | 213 | 95.3 |
| hypothetical | 128 | 95.3 |
| injection | 151 | 90.7 |
| lexical_overlap | 201 | 95.5 |
| long_state | 191 | 94.8 |
| missing_evidence | 141 | 94.3 |
| multi_positive | 322 | 84.5 |
| multi_turn | 149 | 95.3 |
| negation | 257 | 93.8 |
| nota | 118 | 91.5 |
| numeric_reasoning | 224 | 84.4 |
| paraphrase | 218 | 90.4 |
| role_reversal | 187 | 93.6 |
| sarcasm | 149 | 91.3 |
| temporal_reasoning | 203 | 84.7 |
| zero_positive | 73 | 86.3 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 91.0 |
| 00128-00511 | 469 | 92.1 |
| 00512-02047 | 488 | 95.3 |
| 02048-08191 | 329 | 96.7 |
| 08192+ | 39 | 97.4 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 95.5 |
| 03 | 128 | 93.8 |
| 04 | 515 | 92.8 |
| 05 | 224 | 88.4 |
| 06 | 86 | 86.0 |
| 07 | 18 | 94.4 |
| 08 | 4 | 50.0 |

## Paraphrase groups

76 groups; same prediction 80.3%; all correct 84.2%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 3.0 |
| 0.4 | 99.8 | 3.0 |
| 0.5 | 98.8 | 2.6 |
| 0.6 | 97.8 | 2.2 |
| 0.7 | 95.6 | 1.6 |
| 0.8 | 89.9 | 0.2 |
| 0.9 | 80.8 | 0.0 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 430 | 0.033 | 0.002 |
| [0.1,0.2) | 88 | 0.140 | 0.045 |
| [0.2,0.3) | 26 | 0.251 | 0.231 |
| [0.3,0.4) | 26 | 0.348 | 0.269 |
| [0.4,0.5) | 11 | 0.433 | 0.455 |
| [0.5,0.6) | 14 | 0.549 | 0.429 |
| [0.6,0.7) | 15 | 0.652 | 0.667 |
| [0.7,0.8) | 19 | 0.763 | 0.842 |
| [0.8,0.9) | 79 | 0.858 | 0.949 |
| [0.9,1.0] | 308 | 0.965 | 0.990 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 1 | 0.370 | 1.000 |
| [0.4,0.5) | 6 | 0.459 | 0.500 |
| [0.5,0.6) | 6 | 0.559 | 0.667 |
| [0.6,0.7) | 13 | 0.653 | 0.692 |
| [0.7,0.8) | 34 | 0.758 | 0.765 |
| [0.8,0.9) | 54 | 0.861 | 0.981 |
| [0.9,1.0] | 479 | 0.973 | 1.000 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 639 | 0.031 | 0.016 |
| [0.1,0.2) | 124 | 0.137 | 0.065 |
| [0.2,0.3) | 47 | 0.247 | 0.191 |
| [0.3,0.4) | 30 | 0.339 | 0.200 |
| [0.4,0.5) | 19 | 0.441 | 0.684 |
| [0.5,0.6) | 22 | 0.547 | 0.591 |
| [0.6,0.7) | 25 | 0.655 | 0.600 |
| [0.7,0.8) | 38 | 0.751 | 0.842 |
| [0.8,0.9) | 122 | 0.862 | 0.902 |
| [0.9,1.0] | 816 | 0.970 | 0.991 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 93.4%.
Paired vs ours (images_v1/eval2): ours only right 86, plumb-4b only right 31, p = 3.7e-07
