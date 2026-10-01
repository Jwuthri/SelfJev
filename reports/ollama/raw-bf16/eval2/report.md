# Evaluation report

- model `selfjev-bf16` @ `390b27789d` (one request per candidate on Ollama (prefix cache shares the state), readout logprob(yes) - logprob(no)), adapter/checkpoint `merged into the GGUF`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- ollama / BF16; 2026-10-01T06:44:18+0000; wall 1388.4s

## Overall

question accuracy 95.1%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.969, precision 0.959, recall 0.970, f1 0.965, auroc 0.996, brier 0.024, log_loss 0.100, ece 0.035

**multiclass**: n 593, accuracy 0.965, macro_f1 0.934, log_loss 0.107, brier 0.052, ece_top_label 0.017

**multilabel**: n 382, labels 1882, exact_match 0.880, micro_f1 0.973, macro_f1 0.949, label_auroc 0.997, brier 0.020, log_loss 0.084, ece 0.032

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 94.2 | bin acc 96.8 F1 95.7 AUROC 0.996 ECE 0.044; mc acc 95.3 mF1 90.4 ECE 0.026; ml EM 85.6 µF1 96.0 ECE 0.033 |
| e2_simple | 664 | 97.4 | bin acc 97.7 F1 97.9 AUROC 0.997 ECE 0.027; mc acc 99.5 mF1 98.9 ECE 0.020; ml EM 93.3 µF1 98.7 ECE 0.035 |
| e2_very_hard | 654 | 93.6 | bin acc 96.3 F1 95.2 AUROC 0.995 ECE 0.044; mc acc 94.5 mF1 91.1 ECE 0.018; ml EM 85.4 µF1 97.2 ECE 0.037 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 97.0 |
| contradiction | 172 | 95.9 |
| distractor | 474 | 93.5 |
| double_negation | 126 | 96.8 |
| evidence_end | 57 | 98.2 |
| evidence_middle | 114 | 98.2 |
| evidence_start | 17 | 94.1 |
| exception | 213 | 95.3 |
| hypothetical | 128 | 96.9 |
| injection | 151 | 96.0 |
| lexical_overlap | 201 | 97.5 |
| long_state | 191 | 97.4 |
| missing_evidence | 141 | 98.6 |
| multi_positive | 322 | 88.8 |
| multi_turn | 149 | 91.3 |
| negation | 257 | 97.7 |
| nota | 118 | 94.1 |
| numeric_reasoning | 224 | 86.2 |
| paraphrase | 218 | 92.2 |
| role_reversal | 187 | 94.1 |
| sarcasm | 149 | 95.3 |
| temporal_reasoning | 203 | 86.7 |
| zero_positive | 73 | 94.5 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 93.1 |
| 00128-00511 | 469 | 93.8 |
| 00512-02047 | 488 | 97.5 |
| 02048-08191 | 329 | 96.7 |
| 08192+ | 39 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 96.9 |
| 03 | 128 | 96.1 |
| 04 | 515 | 95.3 |
| 05 | 224 | 88.4 |
| 06 | 86 | 89.5 |
| 07 | 18 | 88.9 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 80.3%; all correct 86.8%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 3.5 |
| 0.4 | 99.3 | 3.2 |
| 0.5 | 97.6 | 2.2 |
| 0.6 | 96.5 | 1.6 |
| 0.7 | 94.3 | 1.1 |
| 0.8 | 91.4 | 0.6 |
| 0.9 | 88.0 | 0.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 508 | 0.034 | 0.004 |
| [0.1,0.2) | 31 | 0.141 | 0.000 |
| [0.2,0.3) | 10 | 0.247 | 0.100 |
| [0.3,0.4) | 13 | 0.356 | 0.231 |
| [0.4,0.5) | 14 | 0.439 | 0.500 |
| [0.5,0.6) | 7 | 0.548 | 0.429 |
| [0.6,0.7) | 16 | 0.650 | 0.750 |
| [0.7,0.8) | 27 | 0.753 | 0.852 |
| [0.8,0.9) | 26 | 0.863 | 0.923 |
| [0.9,1.0] | 364 | 0.975 | 0.989 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 4 | 0.376 | 0.500 |
| [0.4,0.5) | 10 | 0.450 | 0.400 |
| [0.5,0.6) | 7 | 0.546 | 0.429 |
| [0.6,0.7) | 13 | 0.655 | 0.769 |
| [0.7,0.8) | 17 | 0.749 | 0.824 |
| [0.8,0.9) | 20 | 0.864 | 0.950 |
| [0.9,1.0] | 522 | 0.989 | 0.996 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 762 | 0.029 | 0.003 |
| [0.1,0.2) | 47 | 0.136 | 0.128 |
| [0.2,0.3) | 18 | 0.252 | 0.389 |
| [0.3,0.4) | 18 | 0.344 | 0.222 |
| [0.4,0.5) | 11 | 0.456 | 0.727 |
| [0.5,0.6) | 27 | 0.536 | 0.481 |
| [0.6,0.7) | 23 | 0.667 | 0.652 |
| [0.7,0.8) | 28 | 0.751 | 0.893 |
| [0.8,0.9) | 58 | 0.857 | 0.966 |
| [0.9,1.0] | 890 | 0.977 | 0.999 |
