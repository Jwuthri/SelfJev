# Evaluation report

- model `/home/ubuntu/ckpt/selfjev-4b-vision-4bit` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `None`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / bfloat16; 2026-10-01T08:14:47+0000; wall 256.0s

## Overall

question accuracy 92.0%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.934, precision 0.931, recall 0.939, f1 0.935, auroc 0.982, brier 0.051, log_loss 0.181, ece 0.039

**multiclass**: n 276, accuracy 0.931, macro_f1 0.873, log_loss 0.223, brier 0.112, ece_top_label 0.039

**multilabel**: n 182, labels 864, exact_match 0.863, micro_f1 0.962, macro_f1 0.928, label_auroc 0.990, brier 0.037, log_loss 0.144, ece 0.041

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 95.0 | bin acc 93.8 F1 93.3 AUROC 1.000 ECE 0.138; mc acc 100.0 mF1 100.0 ECE 0.095; ml EM 90.9 µF1 97.6 ECE 0.100 |
| tllm_guardrail_simple | 67 | 97.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.028; mc acc 100.0 mF1 100.0 ECE 0.037; ml EM 85.7 µF1 96.9 ECE 0.063 |
| tllm_guardrail_very_hard | 43 | 93.0 | bin acc 95.0 F1 95.7 AUROC 1.000 ECE 0.128; mc acc 92.9 mF1 83.3 ECE 0.048; ml EM 88.9 µF1 97.9 ECE 0.076 |
| tllm_jailbreak_hard | 59 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.080; mc acc 100.0 mF1 100.0 ECE 0.124; ml EM 100.0 µF1 100.0 ECE 0.087 |
| tllm_jailbreak_simple | 70 | 97.1 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.041; mc acc 95.5 mF1 87.5 ECE 0.032; ml EM 90.9 µF1 98.6 ECE 0.042 |
| tllm_jailbreak_very_hard | 60 | 85.0 | bin acc 84.4 F1 81.5 AUROC 0.964 ECE 0.120; mc acc 94.4 mF1 91.7 ECE 0.057; ml EM 70.0 µF1 94.5 ECE 0.098 |
| tllm_judge_hard | 86 | 95.3 | bin acc 95.0 F1 93.3 AUROC 0.971 ECE 0.095; mc acc 96.0 mF1 90.9 ECE 0.072; ml EM 95.2 µF1 96.2 ECE 0.038 |
| tllm_judge_simple | 72 | 95.8 | bin acc 97.4 F1 97.9 AUROC 0.997 ECE 0.069; mc acc 95.0 mF1 92.5 ECE 0.061; ml EM 92.9 µF1 98.8 ECE 0.060 |
| tllm_judge_very_hard | 64 | 93.8 | bin acc 96.9 F1 97.3 AUROC 0.996 ECE 0.043; mc acc 95.2 mF1 96.7 ECE 0.051; ml EM 81.8 µF1 97.2 ECE 0.075 |
| tllm_score_hard | 62 | 93.5 | bin acc 97.1 F1 97.0 AUROC 1.000 ECE 0.122; mc acc 87.5 mF1 73.3 ECE 0.135; ml EM 91.7 µF1 98.0 ECE 0.108 |
| tllm_score_simple | 62 | 95.2 | bin acc 94.1 F1 95.8 AUROC 0.996 ECE 0.103; mc acc 93.8 mF1 88.2 ECE 0.075; ml EM 100.0 µF1 100.0 ECE 0.039 |
| tllm_score_very_hard | 76 | 80.3 | bin acc 86.8 F1 78.3 AUROC 0.963 ECE 0.109; mc acc 81.8 mF1 68.0 ECE 0.186; ml EM 62.5 µF1 87.5 ECE 0.071 |
| tllm_verify_hard | 50 | 80.0 | bin acc 84.6 F1 81.8 AUROC 0.903 ECE 0.216; mc acc 87.5 mF1 76.5 ECE 0.233; ml EM 50.0 µF1 75.9 ECE 0.119 |
| tllm_verify_simple | 60 | 98.3 | bin acc 97.0 F1 97.6 AUROC 0.996 ECE 0.071; mc acc 100.0 mF1 100.0 ECE 0.018; ml EM 100.0 µF1 100.0 ECE 0.058 |
| tllm_verify_very_hard | 55 | 76.4 | bin acc 77.4 F1 69.6 AUROC 0.863 ECE 0.176; mc acc 73.3 mF1 59.3 ECE 0.137; ml EM 77.8 µF1 88.9 ECE 0.107 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 97.0 |
| answer_trace_mismatch | 45 | 84.4 |
| benign_lookalike | 88 | 86.4 |
| confident_wrong | 39 | 71.8 |
| contradiction | 22 | 95.5 |
| distractor | 117 | 88.9 |
| double_negation | 3 | 100.0 |
| evidence_end | 11 | 90.9 |
| evidence_middle | 20 | 75.0 |
| evidence_start | 2 | 50.0 |
| exception | 20 | 90.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 65.9 |
| format_near_miss | 46 | 87.0 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 96.0 |
| injection | 22 | 100.0 |
| judge_injection | 112 | 90.2 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 90.3 |
| long_state | 74 | 90.5 |
| missing_evidence | 35 | 97.1 |
| multi_positive | 124 | 84.7 |
| multi_turn | 44 | 79.5 |
| negation | 62 | 93.5 |
| nota | 55 | 87.3 |
| numeric_reasoning | 109 | 79.8 |
| obfuscation | 1 | 0.0 |
| over_refusal | 50 | 94.0 |
| paraphrase | 73 | 90.4 |
| partial_compliance | 31 | 74.2 |
| role_reversal | 6 | 66.7 |
| sarcasm | 8 | 87.5 |
| speaker_confusion | 58 | 94.8 |
| subtle_violation | 16 | 100.0 |
| sycophancy | 13 | 92.3 |
| temporal_reasoning | 20 | 90.0 |
| tool_misuse | 6 | 83.3 |
| unsupported_claim | 96 | 88.5 |
| zero_positive | 55 | 94.5 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 90.3 |
| 00128-00511 | 284 | 94.0 |
| 00512-02047 | 222 | 94.6 |
| 02048-08191 | 125 | 87.2 |
| 08192+ | 7 | 85.7 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 93.4 |
| 03 | 82 | 95.1 |
| 04 | 239 | 91.6 |
| 05 | 98 | 86.7 |
| 06 | 33 | 87.9 |
| 07 | 3 | 33.3 |
| 08 | 3 | 66.7 |

## Paraphrase groups

29 groups; same prediction 93.1%; all correct 86.2%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 6.9 |
| 0.4 | 99.6 | 6.5 |
| 0.5 | 96.4 | 5.6 |
| 0.6 | 93.5 | 3.9 |
| 0.7 | 88.4 | 3.3 |
| 0.8 | 82.6 | 2.2 |
| 0.9 | 72.8 | 1.0 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 188 | 0.036 | 0.011 |
| [0.1,0.2) | 18 | 0.151 | 0.056 |
| [0.2,0.3) | 14 | 0.259 | 0.429 |
| [0.3,0.4) | 9 | 0.355 | 0.111 |
| [0.4,0.5) | 12 | 0.451 | 0.417 |
| [0.5,0.6) | 11 | 0.555 | 0.636 |
| [0.6,0.7) | 7 | 0.654 | 0.571 |
| [0.7,0.8) | 20 | 0.751 | 0.850 |
| [0.8,0.9) | 32 | 0.861 | 0.875 |
| [0.9,1.0] | 177 | 0.961 | 0.983 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 1 | 0.364 | 0.000 |
| [0.4,0.5) | 9 | 0.471 | 0.667 |
| [0.5,0.6) | 8 | 0.549 | 0.375 |
| [0.6,0.7) | 14 | 0.656 | 0.857 |
| [0.7,0.8) | 16 | 0.752 | 0.812 |
| [0.8,0.9) | 27 | 0.871 | 0.889 |
| [0.9,1.0] | 201 | 0.975 | 0.990 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 362 | 0.033 | 0.025 |
| [0.1,0.2) | 41 | 0.134 | 0.122 |
| [0.2,0.3) | 18 | 0.252 | 0.056 |
| [0.3,0.4) | 16 | 0.353 | 0.312 |
| [0.4,0.5) | 13 | 0.436 | 0.231 |
| [0.5,0.6) | 15 | 0.548 | 0.867 |
| [0.6,0.7) | 12 | 0.633 | 0.833 |
| [0.7,0.8) | 20 | 0.764 | 0.950 |
| [0.8,0.9) | 47 | 0.860 | 0.915 |
| [0.9,1.0] | 320 | 0.962 | 1.000 |
