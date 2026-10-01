# Evaluation report

- model `decider-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / -; 2026-09-30T17:46:05+0000; wall 144.8s

## Overall

question accuracy 90.8%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.923, precision 0.896, recall 0.929, f1 0.912, auroc 0.982, brier 0.052, log_loss 0.177, ece 0.030

**multiclass**: n 593, accuracy 0.961, macro_f1 0.931, log_loss 0.109, brier 0.057, ece_top_label 0.006

**multilabel**: n 382, labels 1882, exact_match 0.783, micro_f1 0.947, macro_f1 0.905, label_auroc 0.986, brier 0.045, log_loss 0.160, ece 0.029

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 88.9 | bin acc 91.7 F1 88.7 AUROC 0.977 ECE 0.044; mc acc 94.3 mF1 90.2 ECE 0.018; ml EM 73.5 µF1 92.5 ECE 0.034 |
| e2_simple | 664 | 94.9 | bin acc 96.2 F1 96.5 AUROC 0.994 ECE 0.033; mc acc 99.0 mF1 97.8 ECE 0.010; ml EM 84.2 µF1 96.6 ECE 0.047 |
| e2_very_hard | 654 | 88.5 | bin acc 88.9 F1 85.9 AUROC 0.970 ECE 0.040; mc acc 95.0 mF1 91.2 ECE 0.026; ml EM 77.7 µF1 94.9 ECE 0.039 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 96.0 |
| contradiction | 172 | 93.6 |
| distractor | 474 | 88.6 |
| double_negation | 126 | 86.5 |
| evidence_end | 57 | 89.5 |
| evidence_middle | 114 | 94.7 |
| evidence_start | 17 | 76.5 |
| exception | 213 | 88.7 |
| hypothetical | 128 | 96.1 |
| injection | 151 | 87.4 |
| lexical_overlap | 201 | 93.5 |
| long_state | 191 | 90.6 |
| missing_evidence | 141 | 92.9 |
| multi_positive | 322 | 79.8 |
| multi_turn | 149 | 90.6 |
| negation | 257 | 93.0 |
| nota | 118 | 91.5 |
| numeric_reasoning | 224 | 78.6 |
| paraphrase | 218 | 87.2 |
| role_reversal | 187 | 89.3 |
| sarcasm | 149 | 87.2 |
| temporal_reasoning | 203 | 74.4 |
| zero_positive | 73 | 97.3 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 89.0 |
| 00128-00511 | 469 | 87.6 |
| 00512-02047 | 488 | 94.7 |
| 02048-08191 | 329 | 93.0 |
| 08192+ | 39 | 89.7 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 92.3 |
| 03 | 128 | 93.0 |
| 04 | 515 | 93.2 |
| 05 | 224 | 83.0 |
| 06 | 86 | 76.7 |
| 07 | 18 | 88.9 |
| 08 | 4 | 50.0 |

## Paraphrase groups

76 groups; same prediction 75.0%; all correct 77.6%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 3.9 |
| 0.4 | 99.7 | 3.7 |
| 0.5 | 98.3 | 3.1 |
| 0.6 | 97.0 | 2.4 |
| 0.7 | 95.1 | 1.8 |
| 0.8 | 93.1 | 1.3 |
| 0.9 | 90.6 | 0.6 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 443 | 0.023 | 0.016 |
| [0.1,0.2) | 58 | 0.144 | 0.052 |
| [0.2,0.3) | 30 | 0.243 | 0.167 |
| [0.3,0.4) | 18 | 0.355 | 0.278 |
| [0.4,0.5) | 16 | 0.447 | 0.688 |
| [0.5,0.6) | 19 | 0.536 | 0.474 |
| [0.6,0.7) | 28 | 0.657 | 0.429 |
| [0.7,0.8) | 34 | 0.750 | 0.735 |
| [0.8,0.9) | 53 | 0.858 | 0.849 |
| [0.9,1.0] | 317 | 0.969 | 0.987 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 2 | 0.376 | 0.500 |
| [0.4,0.5) | 8 | 0.469 | 0.500 |
| [0.5,0.6) | 8 | 0.558 | 0.500 |
| [0.6,0.7) | 11 | 0.651 | 0.636 |
| [0.7,0.8) | 12 | 0.755 | 0.750 |
| [0.8,0.9) | 15 | 0.846 | 0.733 |
| [0.9,1.0] | 537 | 0.993 | 0.994 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 715 | 0.024 | 0.025 |
| [0.1,0.2) | 79 | 0.145 | 0.165 |
| [0.2,0.3) | 42 | 0.257 | 0.357 |
| [0.3,0.4) | 41 | 0.348 | 0.390 |
| [0.4,0.5) | 24 | 0.444 | 0.542 |
| [0.5,0.6) | 29 | 0.559 | 0.759 |
| [0.6,0.7) | 30 | 0.655 | 0.833 |
| [0.7,0.8) | 51 | 0.750 | 0.784 |
| [0.8,0.9) | 122 | 0.860 | 0.951 |
| [0.9,1.0] | 749 | 0.969 | 0.997 |


Answered 1991/1991; errors 0; accuracy counting failures as wrong 90.8%.
Paired vs ours (images_v1/eval2): ours only right 132, decider-4b only right 25, p = 9.1e-19
