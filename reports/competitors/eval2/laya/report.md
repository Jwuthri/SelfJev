# Evaluation report

- model `laya` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-09-30T17:33:08+0000; wall 23.3s

## Overall

question accuracy 45.4%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.559, precision 0.491, recall 0.793, f1 0.606, auroc 0.650, brier 0.268, log_loss 0.746, ece 0.176

**multiclass**: n 593, accuracy 0.479, macro_f1 0.341, log_loss 1.257, brier 0.657, ece_top_label 0.100

**multilabel**: n 382, labels 1882, exact_match 0.134, micro_f1 0.659, macro_f1 0.496, label_auroc 0.650, brier 0.241, log_loss 0.726, ece 0.097

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 41.6 | bin acc 51.1 F1 53.3 AUROC 0.636 ECE 0.226; mc acc 44.0 mF1 29.6 ECE 0.137; ml EM 12.9 µF1 64.3 ECE 0.097 |
| e2_simple | 664 | 54.1 | bin acc 64.8 F1 71.7 AUROC 0.699 ECE 0.095; mc acc 56.5 mF1 44.2 ECE 0.089; ml EM 19.2 µF1 68.4 ECE 0.102 |
| e2_very_hard | 654 | 40.4 | bin acc 51.5 F1 54.8 AUROC 0.599 ECE 0.233; mc acc 43.0 mF1 28.2 ECE 0.148; ml EM 8.5 µF1 65.3 ECE 0.115 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 57.3 |
| contradiction | 172 | 37.2 |
| distractor | 474 | 36.9 |
| double_negation | 126 | 48.4 |
| evidence_end | 57 | 29.8 |
| evidence_middle | 114 | 36.0 |
| evidence_start | 17 | 41.2 |
| exception | 213 | 40.8 |
| hypothetical | 128 | 39.1 |
| injection | 151 | 34.4 |
| lexical_overlap | 201 | 39.3 |
| long_state | 191 | 31.9 |
| missing_evidence | 141 | 41.8 |
| multi_positive | 322 | 19.9 |
| multi_turn | 149 | 36.2 |
| negation | 257 | 43.2 |
| nota | 118 | 46.6 |
| numeric_reasoning | 224 | 42.9 |
| paraphrase | 218 | 41.3 |
| role_reversal | 187 | 44.9 |
| sarcasm | 149 | 36.9 |
| temporal_reasoning | 203 | 35.5 |
| zero_positive | 73 | 43.8 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 58.9 |
| 00128-00511 | 469 | 43.5 |
| 00512-02047 | 488 | 38.9 |
| 02048-08191 | 329 | 31.6 |
| 08192+ | 39 | 33.3 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 55.9 |
| 03 | 128 | 63.3 |
| 04 | 515 | 41.0 |
| 05 | 224 | 18.3 |
| 06 | 86 | 2.3 |
| 07 | 18 | 0.0 |
| 08 | 4 | 0.0 |

## Paraphrase groups

76 groups; same prediction 68.4%; all correct 28.9%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 52.1 |
| 0.4 | 75.0 | 47.6 |
| 0.5 | 54.5 | 39.9 |
| 0.6 | 39.5 | 37.2 |
| 0.7 | 29.2 | 31.2 |
| 0.8 | 20.1 | 26.1 |
| 0.9 | 10.3 | 26.2 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 20 | 0.067 | 0.100 |
| [0.1,0.2) | 70 | 0.156 | 0.214 |
| [0.2,0.3) | 75 | 0.254 | 0.240 |
| [0.3,0.4) | 72 | 0.344 | 0.361 |
| [0.4,0.5) | 76 | 0.452 | 0.382 |
| [0.5,0.6) | 113 | 0.556 | 0.336 |
| [0.6,0.7) | 172 | 0.649 | 0.453 |
| [0.7,0.8) | 198 | 0.749 | 0.505 |
| [0.8,0.9) | 184 | 0.847 | 0.543 |
| [0.9,1.0] | 36 | 0.927 | 0.806 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 13 | 0.282 | 0.308 |
| [0.3,0.4) | 135 | 0.357 | 0.348 |
| [0.4,0.5) | 122 | 0.445 | 0.320 |
| [0.5,0.6) | 89 | 0.547 | 0.528 |
| [0.6,0.7) | 61 | 0.645 | 0.459 |
| [0.7,0.8) | 54 | 0.756 | 0.574 |
| [0.8,0.9) | 58 | 0.847 | 0.741 |
| [0.9,1.0] | 61 | 0.959 | 0.738 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 53 | 0.055 | 0.170 |
| [0.1,0.2) | 95 | 0.154 | 0.316 |
| [0.2,0.3) | 181 | 0.248 | 0.365 |
| [0.3,0.4) | 183 | 0.347 | 0.464 |
| [0.4,0.5) | 215 | 0.452 | 0.544 |
| [0.5,0.6) | 251 | 0.549 | 0.522 |
| [0.6,0.7) | 323 | 0.648 | 0.548 |
| [0.7,0.8) | 275 | 0.748 | 0.687 |
| [0.8,0.9) | 231 | 0.843 | 0.736 |
| [0.9,1.0] | 75 | 0.932 | 0.680 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 45.4%.
Paired vs ours (images_v1/eval2): ours only right 1028, laya only right 17, p = 2.8e-278
