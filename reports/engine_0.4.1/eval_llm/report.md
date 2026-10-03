# Evaluation report

- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `weights/selfjev_4b_vision`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / bfloat16; 2026-10-02T23:22:03+0000; wall 123.0s

## Overall

question accuracy 92.6%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.936, precision 0.925, recall 0.951, f1 0.938, auroc 0.984, brier 0.047, log_loss 0.171, ece 0.038

**multiclass**: n 276, accuracy 0.949, macro_f1 0.916, log_loss 0.146, brier 0.077, ece_top_label 0.019

**multilabel**: n 182, labels 864, exact_match 0.863, micro_f1 0.961, macro_f1 0.925, label_auroc 0.991, brier 0.032, log_loss 0.125, ece 0.028

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 90.0 | bin acc 93.8 F1 93.3 AUROC 1.000 ECE 0.133; mc acc 94.1 mF1 87.5 ECE 0.062; ml EM 72.7 µF1 92.3 ECE 0.067 |
| tllm_guardrail_simple | 67 | 98.5 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.026; mc acc 100.0 mF1 100.0 ECE 0.024; ml EM 92.9 µF1 98.5 ECE 0.046 |
| tllm_guardrail_very_hard | 43 | 97.7 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.091; mc acc 92.9 mF1 83.3 ECE 0.061; ml EM 100.0 µF1 100.0 ECE 0.051 |
| tllm_jailbreak_hard | 59 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.061; mc acc 100.0 mF1 100.0 ECE 0.055; ml EM 100.0 µF1 100.0 ECE 0.047 |
| tllm_jailbreak_simple | 70 | 97.1 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.036; mc acc 95.5 mF1 87.5 ECE 0.056; ml EM 90.9 µF1 98.6 ECE 0.033 |
| tllm_jailbreak_very_hard | 60 | 86.7 | bin acc 84.4 F1 81.5 AUROC 0.968 ECE 0.111; mc acc 94.4 mF1 91.7 ECE 0.066; ml EM 80.0 µF1 96.3 ECE 0.057 |
| tllm_judge_hard | 86 | 96.5 | bin acc 95.0 F1 93.3 AUROC 0.971 ECE 0.092; mc acc 100.0 mF1 100.0 ECE 0.011; ml EM 95.2 µF1 96.2 ECE 0.028 |
| tllm_judge_simple | 72 | 97.2 | bin acc 97.4 F1 97.9 AUROC 0.997 ECE 0.053; mc acc 100.0 mF1 100.0 ECE 0.029; ml EM 92.9 µF1 98.8 ECE 0.050 |
| tllm_judge_very_hard | 64 | 92.2 | bin acc 96.9 F1 97.3 AUROC 1.000 ECE 0.074; mc acc 95.2 mF1 96.7 ECE 0.028; ml EM 72.7 µF1 95.8 ECE 0.063 |
| tllm_score_hard | 62 | 96.8 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.110; mc acc 93.8 mF1 85.7 ECE 0.083; ml EM 91.7 µF1 98.0 ECE 0.092 |
| tllm_score_simple | 62 | 96.8 | bin acc 94.1 F1 95.8 AUROC 0.992 ECE 0.071; mc acc 100.0 mF1 100.0 ECE 0.044; ml EM 100.0 µF1 100.0 ECE 0.041 |
| tllm_score_very_hard | 76 | 80.3 | bin acc 84.2 F1 75.0 AUROC 0.970 ECE 0.142; mc acc 86.4 mF1 75.0 ECE 0.102; ml EM 62.5 µF1 86.2 ECE 0.071 |
| tllm_verify_hard | 50 | 78.0 | bin acc 80.8 F1 80.0 AUROC 0.897 ECE 0.241; mc acc 81.2 mF1 70.6 ECE 0.140; ml EM 62.5 µF1 78.6 ECE 0.162 |
| tllm_verify_simple | 60 | 98.3 | bin acc 97.0 F1 97.6 AUROC 1.000 ECE 0.068; mc acc 100.0 mF1 100.0 ECE 0.005; ml EM 100.0 µF1 100.0 ECE 0.041 |
| tllm_verify_very_hard | 55 | 80.0 | bin acc 80.6 F1 75.0 AUROC 0.868 ECE 0.140; mc acc 86.7 mF1 82.2 ECE 0.141; ml EM 66.7 µF1 84.6 ECE 0.103 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 97.7 |
| answer_trace_mismatch | 45 | 86.7 |
| benign_lookalike | 88 | 87.5 |
| confident_wrong | 39 | 74.4 |
| contradiction | 22 | 95.5 |
| distractor | 117 | 89.7 |
| double_negation | 3 | 100.0 |
| evidence_end | 11 | 90.9 |
| evidence_middle | 20 | 75.0 |
| evidence_start | 2 | 50.0 |
| exception | 20 | 95.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 61.4 |
| format_near_miss | 46 | 89.1 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 92.0 |
| injection | 22 | 100.0 |
| judge_injection | 112 | 91.1 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 92.2 |
| long_state | 74 | 91.9 |
| missing_evidence | 35 | 97.1 |
| multi_positive | 124 | 84.7 |
| multi_turn | 44 | 81.8 |
| negation | 62 | 95.2 |
| nota | 55 | 89.1 |
| numeric_reasoning | 109 | 79.8 |
| obfuscation | 1 | 0.0 |
| over_refusal | 50 | 92.0 |
| paraphrase | 73 | 93.2 |
| partial_compliance | 31 | 74.2 |
| role_reversal | 6 | 66.7 |
| sarcasm | 8 | 87.5 |
| speaker_confusion | 58 | 93.1 |
| subtle_violation | 16 | 93.8 |
| sycophancy | 13 | 92.3 |
| temporal_reasoning | 20 | 95.0 |
| tool_misuse | 6 | 100.0 |
| unsupported_claim | 96 | 89.6 |
| zero_positive | 55 | 94.5 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 89.9 |
| 00128-00511 | 284 | 96.5 |
| 00512-02047 | 222 | 93.7 |
| 02048-08191 | 125 | 88.8 |
| 08192+ | 7 | 85.7 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 93.6 |
| 03 | 82 | 93.9 |
| 04 | 239 | 94.6 |
| 05 | 98 | 84.7 |
| 06 | 33 | 87.9 |
| 07 | 3 | 66.7 |
| 08 | 3 | 66.7 |

## Paraphrase groups

29 groups; same prediction 96.6%; all correct 89.7%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 5.1 |
| 0.4 | 100.0 | 5.1 |
| 0.5 | 98.6 | 4.0 |
| 0.6 | 96.0 | 3.0 |
| 0.7 | 92.8 | 2.7 |
| 0.8 | 90.2 | 2.0 |
| 0.9 | 85.5 | 1.7 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 181 | 0.040 | 0.006 |
| [0.1,0.2) | 22 | 0.142 | 0.091 |
| [0.2,0.3) | 13 | 0.249 | 0.154 |
| [0.3,0.4) | 10 | 0.348 | 0.200 |
| [0.4,0.5) | 10 | 0.450 | 0.500 |
| [0.5,0.6) | 6 | 0.545 | 0.167 |
| [0.6,0.7) | 9 | 0.674 | 0.889 |
| [0.7,0.8) | 17 | 0.765 | 0.706 |
| [0.8,0.9) | 25 | 0.865 | 0.840 |
| [0.9,1.0] | 195 | 0.970 | 0.979 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.4,0.5) | 4 | 0.475 | 0.250 |
| [0.5,0.6) | 7 | 0.562 | 0.571 |
| [0.6,0.7) | 9 | 0.636 | 0.889 |
| [0.7,0.8) | 7 | 0.740 | 0.714 |
| [0.8,0.9) | 13 | 0.854 | 0.923 |
| [0.9,1.0] | 236 | 0.987 | 0.983 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 388 | 0.035 | 0.021 |
| [0.1,0.2) | 33 | 0.146 | 0.182 |
| [0.2,0.3) | 15 | 0.237 | 0.133 |
| [0.3,0.4) | 8 | 0.366 | 0.500 |
| [0.4,0.5) | 7 | 0.450 | 0.571 |
| [0.5,0.6) | 8 | 0.536 | 0.750 |
| [0.6,0.7) | 8 | 0.649 | 1.000 |
| [0.7,0.8) | 9 | 0.748 | 0.778 |
| [0.8,0.9) | 26 | 0.859 | 0.846 |
| [0.9,1.0] | 362 | 0.974 | 0.997 |
