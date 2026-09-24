# Evaluation report

- model `~typesafe/jev-latest` @ `-` (stock reranker pairs), adapter/checkpoint `None`, prompt `~typesafe/jev-latest` (-)
- data reports/external/eval2/subset.jsonl; splits ['test']; n=1991; calibration `None`
- - / -; 2026-09-23T22:59:31-0700; wall 0.0s

## Overall

question accuracy 97.2%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.978, precision 0.956, recall 0.995, f1 0.975, auroc 0.999, brier 0.019, log_loss 0.099, ece 0.061

**multiclass**: n 593, accuracy 0.981, macro_f1 0.971, log_loss 0.055, brier 0.028, ece_top_label 0.004

**multilabel**: n 382, labels 1882, exact_match 0.942, micro_f1 0.988, macro_f1 0.978, label_auroc 0.998, brier 0.014, log_loss 0.076, ece 0.045

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 96.7 | bin acc 97.1 F1 96.1 AUROC 0.998 ECE 0.062; mc acc 97.9 mF1 96.6 ECE 0.011; ml EM 93.9 µF1 98.5 ECE 0.049 |
| e2_simple | 664 | 98.5 | bin acc 98.5 F1 98.7 AUROC 1.000 ECE 0.049; mc acc 99.5 mF1 99.4 ECE 0.005; ml EM 96.7 µF1 99.4 ECE 0.042 |
| e2_very_hard | 654 | 96.5 | bin acc 97.8 F1 97.2 AUROC 0.999 ECE 0.076; mc acc 97.0 mF1 94.9 ECE 0.009; ml EM 92.3 µF1 98.6 ECE 0.049 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 98.4 |
| contradiction | 172 | 98.8 |
| distractor | 474 | 97.0 |
| double_negation | 126 | 99.2 |
| evidence_end | 57 | 100.0 |
| evidence_middle | 114 | 99.1 |
| evidence_start | 17 | 94.1 |
| exception | 213 | 95.3 |
| hypothetical | 128 | 98.4 |
| injection | 151 | 97.4 |
| lexical_overlap | 201 | 98.5 |
| long_state | 191 | 99.0 |
| missing_evidence | 141 | 97.9 |
| multi_positive | 322 | 96.0 |
| multi_turn | 149 | 96.0 |
| negation | 257 | 98.8 |
| nota | 118 | 95.8 |
| numeric_reasoning | 224 | 92.0 |
| paraphrase | 218 | 95.4 |
| role_reversal | 187 | 96.8 |
| sarcasm | 149 | 97.3 |
| temporal_reasoning | 203 | 89.2 |
| zero_positive | 73 | 95.9 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 662 | 97.0 |
| 00128-00511 | 477 | 96.2 |
| 00512-02047 | 484 | 97.3 |
| 02048-08191 | 329 | 98.8 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 97.8 |
| 03 | 128 | 97.7 |
| 04 | 515 | 97.7 |
| 05 | 224 | 94.6 |
| 06 | 86 | 95.3 |
| 07 | 18 | 94.4 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 80.3%; all correct 92.1%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 1.9 |
| 0.4 | 100.0 | 1.9 |
| 0.5 | 99.8 | 1.9 |
| 0.6 | 98.7 | 1.2 |
| 0.7 | 97.6 | 0.9 |
| 0.8 | 96.5 | 0.5 |
| 0.9 | 94.4 | 0.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 436 | 0.051 | 0.000 |
| [0.1,0.2) | 92 | 0.128 | 0.000 |
| [0.2,0.3) | 15 | 0.239 | 0.000 |
| [0.3,0.4) | 16 | 0.343 | 0.062 |
| [0.4,0.5) | 4 | 0.430 | 0.250 |
| [0.5,0.6) | 13 | 0.533 | 0.385 |
| [0.6,0.7) | 12 | 0.642 | 0.583 |
| [0.7,0.8) | 24 | 0.752 | 0.792 |
| [0.8,0.9) | 37 | 0.857 | 0.973 |
| [0.9,1.0] | 367 | 0.968 | 0.997 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.4,0.5) | 1 | 0.470 | 1.000 |
| [0.5,0.6) | 7 | 0.548 | 0.429 |
| [0.6,0.7) | 6 | 0.654 | 0.667 |
| [0.7,0.8) | 7 | 0.726 | 0.714 |
| [0.8,0.9) | 12 | 0.853 | 0.917 |
| [0.9,1.0] | 560 | 0.996 | 0.996 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 756 | 0.043 | 0.003 |
| [0.1,0.2) | 58 | 0.132 | 0.034 |
| [0.2,0.3) | 16 | 0.238 | 0.062 |
| [0.3,0.4) | 10 | 0.335 | 0.200 |
| [0.4,0.5) | 21 | 0.444 | 0.333 |
| [0.5,0.6) | 14 | 0.552 | 0.714 |
| [0.6,0.7) | 15 | 0.657 | 0.933 |
| [0.7,0.8) | 31 | 0.747 | 0.903 |
| [0.8,0.9) | 50 | 0.862 | 0.980 |
| [0.9,1.0] | 911 | 0.972 | 0.999 |
