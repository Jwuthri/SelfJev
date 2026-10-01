# Evaluation report

- model `laya-long` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / -; 2026-09-30T17:36:04+0000; wall 36.0s

## Overall

question accuracy 45.6%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.557, precision 0.547, recall 0.690, f1 0.610, auroc 0.603, brier 0.263, log_loss 0.883, ece 0.150

**multiclass**: n 276, accuracy 0.475, macro_f1 0.306, log_loss 1.221, brier 0.654, ece_top_label 0.064

**multilabel**: n 182, labels 864, exact_match 0.154, micro_f1 0.630, macro_f1 0.478, label_auroc 0.685, brier 0.228, log_loss 0.702, ece 0.071

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 46.7 | bin acc 53.1 F1 61.5 AUROC 0.496 ECE 0.315; mc acc 52.9 mF1 42.1 ECE 0.237; ml EM 18.2 µF1 58.3 ECE 0.203 |
| tllm_guardrail_simple | 67 | 46.3 | bin acc 52.9 F1 55.6 AUROC 0.635 ECE 0.239; mc acc 47.4 mF1 34.4 ECE 0.339; ml EM 28.6 µF1 65.7 ECE 0.137 |
| tllm_guardrail_very_hard | 43 | 48.8 | bin acc 65.0 F1 72.0 AUROC 0.792 ECE 0.254; mc acc 50.0 mF1 29.2 ECE 0.192; ml EM 11.1 µF1 56.4 ECE 0.162 |
| tllm_jailbreak_hard | 59 | 50.8 | bin acc 55.6 F1 62.5 AUROC 0.500 ECE 0.314; mc acc 60.0 mF1 40.1 ECE 0.122; ml EM 25.0 µF1 64.2 ECE 0.089 |
| tllm_jailbreak_simple | 70 | 51.4 | bin acc 62.2 F1 73.1 AUROC 0.829 ECE 0.240; mc acc 54.5 mF1 32.4 ECE 0.159; ml EM 9.1 µF1 72.0 ECE 0.190 |
| tllm_jailbreak_very_hard | 60 | 41.7 | bin acc 50.0 F1 52.9 AUROC 0.611 ECE 0.337; mc acc 38.9 mF1 29.2 ECE 0.281; ml EM 20.0 µF1 71.7 ECE 0.156 |
| tllm_judge_hard | 86 | 50.0 | bin acc 70.0 F1 62.5 AUROC 0.763 ECE 0.110; mc acc 32.0 mF1 16.1 ECE 0.156; ml EM 33.3 µF1 62.0 ECE 0.207 |
| tllm_judge_simple | 72 | 61.1 | bin acc 68.4 F1 72.7 AUROC 0.765 ECE 0.123; mc acc 75.0 mF1 68.5 ECE 0.197; ml EM 21.4 µF1 78.5 ECE 0.149 |
| tllm_judge_very_hard | 64 | 35.9 | bin acc 34.4 F1 32.3 AUROC 0.433 ECE 0.310; mc acc 57.1 mF1 31.5 ECE 0.165; ml EM 0.0 µF1 54.8 ECE 0.130 |
| tllm_score_hard | 62 | 45.2 | bin acc 55.9 F1 57.1 AUROC 0.465 ECE 0.327; mc acc 50.0 mF1 38.5 ECE 0.156; ml EM 8.3 µF1 47.8 ECE 0.204 |
| tllm_score_simple | 62 | 46.8 | bin acc 55.9 F1 68.1 AUROC 0.492 ECE 0.306; mc acc 50.0 mF1 34.8 ECE 0.169; ml EM 16.7 µF1 66.7 ECE 0.168 |
| tllm_score_very_hard | 76 | 42.1 | bin acc 52.6 F1 50.0 AUROC 0.690 ECE 0.262; mc acc 54.5 mF1 38.1 ECE 0.247; ml EM 0.0 µF1 54.3 ECE 0.171 |
| tllm_verify_hard | 50 | 32.0 | bin acc 38.5 F1 52.9 AUROC 0.406 ECE 0.358; mc acc 37.5 mF1 22.7 ECE 0.286; ml EM 0.0 µF1 63.4 ECE 0.142 |
| tllm_verify_simple | 60 | 40.0 | bin acc 63.6 F1 75.0 AUROC 0.591 ECE 0.174; mc acc 13.3 mF1 7.6 ECE 0.465; ml EM 8.3 µF1 68.5 ECE 0.158 |
| tllm_verify_very_hard | 55 | 38.2 | bin acc 51.6 F1 48.3 AUROC 0.509 ECE 0.200; mc acc 26.7 mF1 16.7 ECE 0.136; ml EM 11.1 µF1 37.5 ECE 0.230 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 53.2 |
| answer_trace_mismatch | 45 | 37.8 |
| benign_lookalike | 88 | 53.4 |
| confident_wrong | 39 | 43.6 |
| contradiction | 22 | 50.0 |
| distractor | 117 | 45.3 |
| double_negation | 3 | 33.3 |
| evidence_end | 11 | 72.7 |
| evidence_middle | 20 | 15.0 |
| evidence_start | 2 | 0.0 |
| exception | 20 | 45.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 36.4 |
| format_near_miss | 46 | 30.4 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 71.4 |
| indirect_injection | 25 | 32.0 |
| injection | 22 | 50.0 |
| judge_injection | 112 | 44.6 |
| length_bias | 7 | 0.0 |
| lexical_overlap | 103 | 42.7 |
| long_state | 74 | 37.8 |
| missing_evidence | 35 | 42.9 |
| multi_positive | 124 | 15.3 |
| multi_turn | 44 | 38.6 |
| negation | 62 | 40.3 |
| nota | 55 | 69.1 |
| numeric_reasoning | 109 | 40.4 |
| obfuscation | 1 | 0.0 |
| over_refusal | 50 | 40.0 |
| paraphrase | 73 | 54.8 |
| partial_compliance | 31 | 38.7 |
| role_reversal | 6 | 66.7 |
| sarcasm | 8 | 37.5 |
| speaker_confusion | 58 | 43.1 |
| subtle_violation | 16 | 18.8 |
| sycophancy | 13 | 38.5 |
| temporal_reasoning | 20 | 50.0 |
| tool_misuse | 6 | 33.3 |
| unsupported_claim | 96 | 37.5 |
| zero_positive | 55 | 52.7 |
| zero_positive_partial | 1 | 0.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 55.5 |
| 00128-00511 | 284 | 49.3 |
| 00512-02047 | 222 | 37.4 |
| 02048-08191 | 125 | 27.2 |
| 08192+ | 7 | 42.9 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 55.7 |
| 03 | 82 | 51.2 |
| 04 | 239 | 40.2 |
| 05 | 98 | 18.4 |
| 06 | 33 | 9.1 |
| 07 | 3 | 0.0 |
| 08 | 3 | 0.0 |

## Paraphrase groups

29 groups; same prediction 72.4%; all correct 44.8%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 52.5 |
| 0.4 | 69.6 | 47.4 |
| 0.5 | 45.3 | 38.4 |
| 0.6 | 27.5 | 32.9 |
| 0.7 | 17.8 | 30.6 |
| 0.8 | 11.6 | 31.2 |
| 0.9 | 8.0 | 27.3 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 13 | 0.049 | 0.077 |
| [0.1,0.2) | 27 | 0.156 | 0.185 |
| [0.2,0.3) | 38 | 0.257 | 0.395 |
| [0.3,0.4) | 38 | 0.341 | 0.474 |
| [0.4,0.5) | 63 | 0.458 | 0.587 |
| [0.5,0.6) | 72 | 0.548 | 0.500 |
| [0.6,0.7) | 75 | 0.656 | 0.520 |
| [0.7,0.8) | 68 | 0.751 | 0.529 |
| [0.8,0.9) | 67 | 0.844 | 0.612 |
| [0.9,1.0] | 27 | 0.979 | 0.630 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 17 | 0.264 | 0.353 |
| [0.3,0.4) | 67 | 0.346 | 0.358 |
| [0.4,0.5) | 67 | 0.448 | 0.358 |
| [0.5,0.6) | 49 | 0.546 | 0.531 |
| [0.6,0.7) | 27 | 0.652 | 0.630 |
| [0.7,0.8) | 17 | 0.740 | 0.706 |
| [0.8,0.9) | 10 | 0.856 | 0.600 |
| [0.9,1.0] | 22 | 0.946 | 0.727 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 32 | 0.068 | 0.031 |
| [0.1,0.2) | 64 | 0.152 | 0.266 |
| [0.2,0.3) | 84 | 0.253 | 0.262 |
| [0.3,0.4) | 89 | 0.350 | 0.427 |
| [0.4,0.5) | 134 | 0.451 | 0.522 |
| [0.5,0.6) | 163 | 0.548 | 0.491 |
| [0.6,0.7) | 115 | 0.652 | 0.626 |
| [0.7,0.8) | 81 | 0.750 | 0.667 |
| [0.8,0.9) | 67 | 0.851 | 0.761 |
| [0.9,1.0] | 35 | 0.952 | 0.657 |


Answered 946/946; errors 0; accuracy counting failures as wrong 45.6%.
Paired vs ours (images_v1/eval_llm): ours only right 465, laya-long only right 21, p = 3.5e-110
