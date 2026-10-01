# Evaluation report

- model `selfjev-bf16` @ `390b27789d` (one request per candidate on Ollama (prefix cache shares the state), readout logprob(yes) - logprob(no)), adapter/checkpoint `merged into the GGUF`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- ollama / BF16; 2026-10-01T07:49:42+0000; wall 1493.4s

## Overall

question accuracy 95.6%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.969, precision 0.959, recall 0.970, f1 0.965, auroc 0.996, brier 0.024, log_loss 0.100, ece 0.035

**multiclass**: n 593, accuracy 0.970, macro_f1 0.944, log_loss 0.089, brier 0.045, ece_top_label 0.017

**multilabel**: n 382, labels 1882, exact_match 0.901, micro_f1 0.979, macro_f1 0.960, label_auroc 0.998, brier 0.016, log_loss 0.069, ece 0.027

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 94.5 | bin acc 96.8 F1 95.7 AUROC 0.996 ECE 0.044; mc acc 95.9 mF1 91.2 ECE 0.026; ml EM 86.4 µF1 96.5 ECE 0.030 |
| e2_simple | 664 | 98.0 | bin acc 97.7 F1 97.9 AUROC 0.997 ECE 0.027; mc acc 99.5 mF1 98.9 ECE 0.007; ml EM 96.7 µF1 99.4 ECE 0.027 |
| e2_very_hard | 654 | 94.3 | bin acc 96.3 F1 95.2 AUROC 0.995 ECE 0.044; mc acc 95.5 mF1 93.5 ECE 0.028; ml EM 87.7 µF1 97.7 ECE 0.028 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.9 |
| contradiction | 172 | 97.1 |
| distractor | 474 | 94.3 |
| double_negation | 126 | 96.8 |
| evidence_end | 57 | 98.2 |
| evidence_middle | 114 | 98.2 |
| evidence_start | 17 | 100.0 |
| exception | 213 | 96.7 |
| hypothetical | 128 | 96.1 |
| injection | 151 | 95.4 |
| lexical_overlap | 201 | 98.0 |
| long_state | 191 | 98.4 |
| missing_evidence | 141 | 98.6 |
| multi_positive | 322 | 90.4 |
| multi_turn | 149 | 91.9 |
| negation | 257 | 98.1 |
| nota | 118 | 94.9 |
| numeric_reasoning | 224 | 87.9 |
| paraphrase | 218 | 93.1 |
| role_reversal | 187 | 94.1 |
| sarcasm | 149 | 97.3 |
| temporal_reasoning | 203 | 87.7 |
| zero_positive | 73 | 94.5 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 93.8 |
| 00128-00511 | 469 | 94.5 |
| 00512-02047 | 488 | 97.1 |
| 02048-08191 | 329 | 98.2 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 96.9 |
| 03 | 128 | 96.1 |
| 04 | 515 | 95.3 |
| 05 | 224 | 91.5 |
| 06 | 86 | 93.0 |
| 07 | 18 | 94.4 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 81.6%; all correct 86.8%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 3.0 |
| 0.4 | 99.3 | 2.4 |
| 0.5 | 98.1 | 2.1 |
| 0.6 | 97.5 | 2.1 |
| 0.7 | 96.6 | 1.4 |
| 0.8 | 94.4 | 1.1 |
| 0.9 | 92.1 | 0.5 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 508 | 0.034 | 0.004 |
| [0.1,0.2) | 31 | 0.141 | 0.000 |
| [0.2,0.3) | 10 | 0.247 | 0.100 |
| [0.3,0.4) | 13 | 0.357 | 0.231 |
| [0.4,0.5) | 14 | 0.440 | 0.500 |
| [0.5,0.6) | 7 | 0.549 | 0.429 |
| [0.6,0.7) | 16 | 0.651 | 0.750 |
| [0.7,0.8) | 27 | 0.753 | 0.852 |
| [0.8,0.9) | 27 | 0.864 | 0.926 |
| [0.9,1.0] | 363 | 0.976 | 0.989 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 4 | 0.345 | 0.000 |
| [0.4,0.5) | 7 | 0.442 | 0.714 |
| [0.5,0.6) | 4 | 0.545 | 1.000 |
| [0.6,0.7) | 5 | 0.646 | 0.200 |
| [0.7,0.8) | 13 | 0.740 | 0.846 |
| [0.8,0.9) | 14 | 0.861 | 0.786 |
| [0.9,1.0] | 546 | 0.994 | 0.995 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 775 | 0.028 | 0.003 |
| [0.1,0.2) | 42 | 0.136 | 0.071 |
| [0.2,0.3) | 12 | 0.244 | 0.333 |
| [0.3,0.4) | 8 | 0.346 | 0.250 |
| [0.4,0.5) | 13 | 0.431 | 0.538 |
| [0.5,0.6) | 14 | 0.539 | 0.357 |
| [0.6,0.7) | 17 | 0.646 | 0.647 |
| [0.7,0.8) | 23 | 0.747 | 0.739 |
| [0.8,0.9) | 47 | 0.858 | 0.957 |
| [0.9,1.0] | 931 | 0.979 | 0.998 |
