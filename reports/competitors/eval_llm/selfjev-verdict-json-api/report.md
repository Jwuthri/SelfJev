# Evaluation report

- model `selfjev-verdict-json-api` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / -; 2026-10-01T13:47:45+0000; wall 60.8s

## Overall

question accuracy 88.5%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.914, precision 0.877, recall 0.963, f1 0.918, auroc 0.976, brier 0.064, log_loss 0.220, ece 0.050

**multiclass**: n 276, accuracy 0.949, macro_f1 0.919, log_loss 0.155, brier 0.083, ece_top_label 0.019

**multilabel**: n 182, labels 864, exact_match 0.709, micro_f1 0.908, macro_f1 0.835, label_auroc 0.974, brier 0.069, log_loss 0.227, ece 0.047

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 81.7 | bin acc 84.4 F1 84.8 AUROC 1.000 ECE 0.165; mc acc 94.1 mF1 87.5 ECE 0.052; ml EM 54.5 µF1 85.7 ECE 0.096 |
| tllm_guardrail_simple | 67 | 97.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.017; mc acc 100.0 mF1 100.0 ECE 0.022; ml EM 85.7 µF1 97.0 ECE 0.051 |
| tllm_guardrail_very_hard | 43 | 95.3 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.047; mc acc 92.9 mF1 83.3 ECE 0.048; ml EM 88.9 µF1 98.0 ECE 0.062 |
| tllm_jailbreak_hard | 59 | 94.9 | bin acc 96.3 F1 96.6 AUROC 1.000 ECE 0.082; mc acc 100.0 mF1 100.0 ECE 0.046; ml EM 83.3 µF1 96.4 ECE 0.079 |
| tllm_jailbreak_simple | 70 | 97.1 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.016; mc acc 100.0 mF1 100.0 ECE 0.042; ml EM 81.8 µF1 97.1 ECE 0.047 |
| tllm_jailbreak_very_hard | 60 | 83.3 | bin acc 87.5 F1 86.7 AUROC 0.947 ECE 0.153; mc acc 94.4 mF1 91.7 ECE 0.077; ml EM 50.0 µF1 89.7 ECE 0.117 |
| tllm_judge_hard | 86 | 88.4 | bin acc 85.0 F1 82.4 AUROC 0.949 ECE 0.142; mc acc 96.0 mF1 90.9 ECE 0.039; ml EM 85.7 µF1 92.6 ECE 0.071 |
| tllm_judge_simple | 72 | 93.1 | bin acc 97.4 F1 97.9 AUROC 0.994 ECE 0.059; mc acc 100.0 mF1 100.0 ECE 0.023; ml EM 71.4 µF1 95.3 ECE 0.047 |
| tllm_judge_very_hard | 64 | 92.2 | bin acc 93.8 F1 94.7 AUROC 0.996 ECE 0.081; mc acc 95.2 mF1 96.7 ECE 0.032; ml EM 81.8 µF1 97.2 ECE 0.066 |
| tllm_score_hard | 62 | 87.1 | bin acc 94.1 F1 94.1 AUROC 1.000 ECE 0.092; mc acc 100.0 mF1 100.0 ECE 0.055; ml EM 50.0 µF1 72.7 ECE 0.218 |
| tllm_score_simple | 62 | 96.8 | bin acc 94.1 F1 96.0 AUROC 0.983 ECE 0.056; mc acc 100.0 mF1 100.0 ECE 0.047; ml EM 100.0 µF1 100.0 ECE 0.048 |
| tllm_score_very_hard | 76 | 80.3 | bin acc 86.8 F1 80.0 AUROC 0.976 ECE 0.124; mc acc 86.4 mF1 75.0 ECE 0.100; ml EM 56.2 µF1 80.0 ECE 0.133 |
| tllm_verify_hard | 50 | 66.0 | bin acc 76.9 F1 76.9 AUROC 0.873 ECE 0.255; mc acc 75.0 mF1 64.7 ECE 0.199; ml EM 12.5 µF1 74.3 ECE 0.148 |
| tllm_verify_simple | 60 | 96.7 | bin acc 97.0 F1 97.6 AUROC 1.000 ECE 0.077; mc acc 100.0 mF1 100.0 ECE 0.005; ml EM 91.7 µF1 93.9 ECE 0.076 |
| tllm_verify_very_hard | 55 | 72.7 | bin acc 77.4 F1 72.0 AUROC 0.829 ECE 0.189; mc acc 86.7 mF1 82.2 ECE 0.134; ml EM 33.3 µF1 70.6 ECE 0.181 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 96.2 |
| answer_trace_mismatch | 45 | 84.4 |
| benign_lookalike | 88 | 81.8 |
| confident_wrong | 39 | 79.5 |
| contradiction | 22 | 95.5 |
| distractor | 117 | 84.6 |
| double_negation | 3 | 100.0 |
| evidence_end | 11 | 90.9 |
| evidence_middle | 20 | 75.0 |
| evidence_start | 2 | 50.0 |
| exception | 20 | 90.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 56.8 |
| format_near_miss | 46 | 82.6 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 96.0 |
| injection | 22 | 95.5 |
| judge_injection | 112 | 90.2 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 86.4 |
| long_state | 74 | 87.8 |
| missing_evidence | 35 | 97.1 |
| multi_positive | 124 | 75.0 |
| multi_turn | 44 | 84.1 |
| negation | 62 | 91.9 |
| nota | 55 | 89.1 |
| numeric_reasoning | 109 | 76.1 |
| obfuscation | 1 | 100.0 |
| over_refusal | 50 | 92.0 |
| paraphrase | 73 | 87.7 |
| partial_compliance | 31 | 71.0 |
| role_reversal | 6 | 66.7 |
| sarcasm | 8 | 87.5 |
| speaker_confusion | 58 | 82.8 |
| subtle_violation | 16 | 93.8 |
| sycophancy | 13 | 92.3 |
| temporal_reasoning | 20 | 90.0 |
| tool_misuse | 6 | 66.7 |
| unsupported_claim | 96 | 81.2 |
| zero_positive | 55 | 76.4 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 82.5 |
| 00128-00511 | 284 | 92.6 |
| 00512-02047 | 222 | 92.8 |
| 02048-08191 | 125 | 86.4 |
| 08192+ | 7 | 85.7 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 91.4 |
| 03 | 82 | 93.9 |
| 04 | 239 | 86.2 |
| 05 | 98 | 79.6 |
| 06 | 33 | 78.8 |
| 07 | 3 | 66.7 |
| 08 | 3 | 66.7 |

## Paraphrase groups

29 groups; same prediction 96.6%; all correct 82.8%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 5.1 |
| 0.4 | 99.6 | 5.1 |
| 0.5 | 98.2 | 4.4 |
| 0.6 | 97.1 | 3.7 |
| 0.7 | 94.9 | 3.4 |
| 0.8 | 90.9 | 2.4 |
| 0.9 | 87.3 | 2.1 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 165 | 0.022 | 0.006 |
| [0.1,0.2) | 23 | 0.142 | 0.087 |
| [0.2,0.3) | 14 | 0.241 | 0.071 |
| [0.3,0.4) | 9 | 0.359 | 0.333 |
| [0.4,0.5) | 8 | 0.443 | 0.250 |
| [0.5,0.6) | 7 | 0.543 | 0.429 |
| [0.6,0.7) | 9 | 0.646 | 0.111 |
| [0.7,0.8) | 15 | 0.749 | 0.733 |
| [0.8,0.9) | 20 | 0.845 | 0.650 |
| [0.9,1.0] | 218 | 0.984 | 0.954 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 1 | 0.388 | 1.000 |
| [0.4,0.5) | 4 | 0.460 | 0.500 |
| [0.5,0.6) | 3 | 0.537 | 0.333 |
| [0.6,0.7) | 6 | 0.661 | 0.833 |
| [0.7,0.8) | 11 | 0.752 | 0.727 |
| [0.8,0.9) | 10 | 0.854 | 0.900 |
| [0.9,1.0] | 241 | 0.988 | 0.979 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 280 | 0.024 | 0.018 |
| [0.1,0.2) | 53 | 0.144 | 0.151 |
| [0.2,0.3) | 31 | 0.250 | 0.097 |
| [0.3,0.4) | 23 | 0.352 | 0.217 |
| [0.4,0.5) | 24 | 0.455 | 0.292 |
| [0.5,0.6) | 11 | 0.552 | 0.091 |
| [0.6,0.7) | 22 | 0.639 | 0.545 |
| [0.7,0.8) | 18 | 0.759 | 0.667 |
| [0.8,0.9) | 30 | 0.848 | 0.467 |
| [0.9,1.0] | 372 | 0.987 | 0.970 |


Answered 946/946; errors 0; accuracy counting failures as wrong 88.5%.
Paired vs ours (images_v1/eval_llm): ours only right 51, selfjev-verdict-json-api only right 13, p = 1.9e-06
