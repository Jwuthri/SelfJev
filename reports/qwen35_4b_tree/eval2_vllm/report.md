# Evaluation report

- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared document on vLLM (prefix cache), readout logprob(yes) - logprob(no) over {yes, no}), adapter/checkpoint `merged into runs/qwen35_4b_tree/merged`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval2.jsonl; splits ['test']; n=1991; calibration `None`
- cuda / bfloat16; 2026-09-26T00:22:37+0000; wall 112.4s

## Overall

question accuracy 95.6%

![reliability](reliability.svg)

**binary**: n 1016, positives 435, accuracy 0.968, precision 0.957, recall 0.968, f1 0.962, auroc 0.995, brier 0.025, log_loss 0.089, ece 0.010

**multiclass**: n 593, accuracy 0.970, macro_f1 0.946, log_loss 0.099, brier 0.048, ece_top_label 0.007

**multilabel**: n 382, labels 1882, exact_match 0.903, micro_f1 0.976, macro_f1 0.957, label_auroc 0.996, brier 0.020, log_loss 0.076, ece 0.008

## By family

| family | n | question acc % | details |
|---|---|---|---|
| e2_hard | 673 | 94.4 | bin acc 96.3 F1 94.9 AUROC 0.995 ECE 0.026; mc acc 96.9 mF1 93.3 ECE 0.021; ml EM 85.6 µF1 96.1 ECE 0.024 |
| e2_simple | 664 | 98.6 | bin acc 97.4 F1 97.6 AUROC 0.997 ECE 0.015; mc acc 100.0 mF1 100.0 ECE 0.007; ml EM 100.0 µF1 100.0 ECE 0.007 |
| e2_very_hard | 654 | 93.7 | bin acc 96.6 F1 95.5 AUROC 0.992 ECE 0.021; mc acc 94.0 mF1 90.5 ECE 0.035; ml EM 86.2 µF1 96.8 ECE 0.013 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 569 | 98.8 |
| contradiction | 172 | 96.5 |
| distractor | 474 | 92.8 |
| double_negation | 126 | 95.2 |
| evidence_end | 57 | 96.5 |
| evidence_middle | 114 | 98.2 |
| evidence_start | 17 | 94.1 |
| exception | 213 | 94.4 |
| hypothetical | 128 | 93.8 |
| injection | 151 | 95.4 |
| lexical_overlap | 201 | 97.0 |
| long_state | 191 | 95.8 |
| missing_evidence | 141 | 97.9 |
| multi_positive | 322 | 91.6 |
| multi_turn | 149 | 94.0 |
| negation | 257 | 97.7 |
| nota | 118 | 94.1 |
| numeric_reasoning | 224 | 88.4 |
| paraphrase | 218 | 92.2 |
| role_reversal | 187 | 94.7 |
| sarcasm | 149 | 94.6 |
| temporal_reasoning | 203 | 84.2 |
| zero_positive | 73 | 93.2 |
| zero_positive_distractor | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 666 | 96.1 |
| 00128-00511 | 469 | 92.8 |
| 00512-02047 | 488 | 95.9 |
| 02048-08191 | 329 | 97.9 |
| 08192+ | 39 | 97.4 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 1016 | 96.8 |
| 03 | 128 | 96.9 |
| 04 | 515 | 95.9 |
| 05 | 224 | 92.0 |
| 06 | 86 | 88.4 |
| 07 | 18 | 94.4 |
| 08 | 4 | 75.0 |

## Paraphrase groups

76 groups; same prediction 80.3%; all correct 86.8%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 3.0 |
| 0.4 | 99.7 | 2.9 |
| 0.5 | 98.3 | 2.2 |
| 0.6 | 97.3 | 1.7 |
| 0.7 | 95.6 | 1.1 |
| 0.8 | 94.8 | 1.1 |
| 0.9 | 92.2 | 0.7 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 530 | 0.006 | 0.006 |
| [0.1,0.2) | 14 | 0.143 | 0.143 |
| [0.2,0.3) | 12 | 0.253 | 0.250 |
| [0.3,0.4) | 12 | 0.351 | 0.083 |
| [0.4,0.5) | 8 | 0.446 | 0.625 |
| [0.5,0.6) | 9 | 0.545 | 0.556 |
| [0.6,0.7) | 8 | 0.648 | 0.750 |
| [0.7,0.8) | 20 | 0.758 | 0.700 |
| [0.8,0.9) | 16 | 0.870 | 0.938 |
| [0.9,1.0] | 387 | 0.990 | 0.984 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 2 | 0.363 | 0.500 |
| [0.4,0.5) | 8 | 0.438 | 0.500 |
| [0.5,0.6) | 6 | 0.544 | 0.500 |
| [0.6,0.7) | 10 | 0.631 | 0.600 |
| [0.7,0.8) | 5 | 0.745 | 1.000 |
| [0.8,0.9) | 15 | 0.862 | 0.867 |
| [0.9,1.0] | 547 | 0.996 | 0.993 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 798 | 0.006 | 0.008 |
| [0.1,0.2) | 8 | 0.150 | 0.125 |
| [0.2,0.3) | 13 | 0.242 | 0.154 |
| [0.3,0.4) | 7 | 0.337 | 0.286 |
| [0.4,0.5) | 10 | 0.441 | 0.300 |
| [0.5,0.6) | 14 | 0.538 | 0.571 |
| [0.6,0.7) | 11 | 0.651 | 0.455 |
| [0.7,0.8) | 22 | 0.744 | 0.682 |
| [0.8,0.9) | 31 | 0.866 | 0.871 |
| [0.9,1.0] | 968 | 0.994 | 0.988 |
