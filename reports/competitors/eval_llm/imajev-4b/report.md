# Evaluation report

- model `imajev-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / -; 2026-09-30T19:20:33+0000; wall 154.6s

## Overall

question accuracy 84.9%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.869, precision 0.832, recall 0.927, f1 0.876, auroc 0.956, brier 0.090, log_loss 0.294, ece 0.075

**multiclass**: n 276, accuracy 0.917, macro_f1 0.857, log_loss 0.248, brier 0.127, ece_top_label 0.046

**multilabel**: n 182, labels 864, exact_match 0.692, micro_f1 0.915, macro_f1 0.845, label_auroc 0.971, brier 0.068, log_loss 0.233, ece 0.042

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 78.3 | bin acc 78.1 F1 80.0 AUROC 0.960 ECE 0.191; mc acc 94.1 mF1 91.7 ECE 0.122; ml EM 54.5 µF1 82.6 ECE 0.121 |
| tllm_guardrail_simple | 67 | 97.0 | bin acc 97.1 F1 97.3 AUROC 1.000 ECE 0.070; mc acc 100.0 mF1 100.0 ECE 0.039; ml EM 92.9 µF1 98.5 ECE 0.051 |
| tllm_guardrail_very_hard | 43 | 95.3 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.126; mc acc 100.0 mF1 100.0 ECE 0.144; ml EM 77.8 µF1 93.6 ECE 0.110 |
| tllm_jailbreak_hard | 59 | 72.9 | bin acc 66.7 F1 60.9 AUROC 0.856 ECE 0.240; mc acc 80.0 mF1 65.9 ECE 0.150; ml EM 75.0 µF1 92.6 ECE 0.095 |
| tllm_jailbreak_simple | 70 | 90.0 | bin acc 86.5 F1 88.4 AUROC 0.965 ECE 0.115; mc acc 95.5 mF1 87.5 ECE 0.066; ml EM 90.9 µF1 98.6 ECE 0.053 |
| tllm_jailbreak_very_hard | 60 | 81.7 | bin acc 81.2 F1 78.6 AUROC 0.931 ECE 0.137; mc acc 94.4 mF1 95.6 ECE 0.136; ml EM 60.0 µF1 89.3 ECE 0.105 |
| tllm_judge_hard | 86 | 86.0 | bin acc 90.0 F1 87.5 AUROC 0.968 ECE 0.136; mc acc 92.0 mF1 82.6 ECE 0.058; ml EM 71.4 µF1 87.7 ECE 0.091 |
| tllm_judge_simple | 72 | 94.4 | bin acc 92.1 F1 93.9 AUROC 1.000 ECE 0.130; mc acc 100.0 mF1 100.0 ECE 0.081; ml EM 92.9 µF1 97.6 ECE 0.079 |
| tllm_judge_very_hard | 64 | 82.8 | bin acc 93.8 F1 94.7 AUROC 1.000 ECE 0.120; mc acc 85.7 mF1 74.1 ECE 0.121; ml EM 45.5 µF1 88.2 ECE 0.131 |
| tllm_score_hard | 62 | 83.9 | bin acc 85.3 F1 86.5 AUROC 0.976 ECE 0.194; mc acc 100.0 mF1 100.0 ECE 0.113; ml EM 58.3 µF1 85.7 ECE 0.144 |
| tllm_score_simple | 62 | 91.9 | bin acc 94.1 F1 95.8 AUROC 0.983 ECE 0.090; mc acc 87.5 mF1 77.8 ECE 0.119; ml EM 91.7 µF1 98.6 ECE 0.075 |
| tllm_score_very_hard | 76 | 80.3 | bin acc 84.2 F1 78.6 AUROC 0.970 ECE 0.173; mc acc 95.5 mF1 90.9 ECE 0.168; ml EM 50.0 µF1 88.6 ECE 0.074 |
| tllm_verify_hard | 50 | 74.0 | bin acc 80.8 F1 80.0 AUROC 0.867 ECE 0.173; mc acc 81.2 mF1 66.7 ECE 0.146; ml EM 37.5 µF1 85.0 ECE 0.170 |
| tllm_verify_simple | 60 | 88.3 | bin acc 90.9 F1 93.0 AUROC 0.976 ECE 0.093; mc acc 100.0 mF1 100.0 ECE 0.070; ml EM 66.7 µF1 91.2 ECE 0.069 |
| tllm_verify_very_hard | 55 | 72.7 | bin acc 80.6 F1 78.6 AUROC 0.885 ECE 0.176; mc acc 66.7 mF1 53.7 ECE 0.234; ml EM 55.6 µF1 82.4 ECE 0.164 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 92.1 |
| answer_trace_mismatch | 45 | 84.4 |
| benign_lookalike | 88 | 84.1 |
| confident_wrong | 39 | 71.8 |
| contradiction | 22 | 90.9 |
| distractor | 117 | 83.8 |
| double_negation | 3 | 66.7 |
| evidence_end | 11 | 100.0 |
| evidence_middle | 20 | 70.0 |
| evidence_start | 2 | 0.0 |
| exception | 20 | 100.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 72.7 |
| format_near_miss | 46 | 78.3 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 76.0 |
| injection | 22 | 95.5 |
| judge_injection | 112 | 77.7 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 87.4 |
| long_state | 74 | 82.4 |
| missing_evidence | 35 | 88.6 |
| multi_positive | 124 | 69.4 |
| multi_turn | 44 | 84.1 |
| negation | 62 | 90.3 |
| nota | 55 | 81.8 |
| numeric_reasoning | 109 | 77.1 |
| obfuscation | 1 | 0.0 |
| over_refusal | 50 | 80.0 |
| paraphrase | 73 | 90.4 |
| partial_compliance | 31 | 74.2 |
| role_reversal | 6 | 83.3 |
| sarcasm | 8 | 87.5 |
| speaker_confusion | 58 | 77.6 |
| subtle_violation | 16 | 81.2 |
| sycophancy | 13 | 92.3 |
| temporal_reasoning | 20 | 75.0 |
| tool_misuse | 6 | 16.7 |
| unsupported_claim | 96 | 80.2 |
| zero_positive | 55 | 81.8 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 82.1 |
| 00128-00511 | 284 | 86.6 |
| 00512-02047 | 222 | 88.7 |
| 02048-08191 | 125 | 81.6 |
| 08192+ | 7 | 71.4 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 86.9 |
| 03 | 82 | 86.6 |
| 04 | 239 | 85.8 |
| 05 | 98 | 78.6 |
| 06 | 33 | 69.7 |
| 07 | 3 | 33.3 |
| 08 | 3 | 66.7 |

## Paraphrase groups

29 groups; same prediction 89.7%; all correct 82.8%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 8.3 |
| 0.4 | 100.0 | 8.3 |
| 0.5 | 96.4 | 6.4 |
| 0.6 | 92.0 | 5.5 |
| 0.7 | 85.1 | 3.8 |
| 0.8 | 77.2 | 2.3 |
| 0.9 | 63.4 | 1.1 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 104 | 0.045 | 0.010 |
| [0.1,0.2) | 46 | 0.141 | 0.130 |
| [0.2,0.3) | 30 | 0.236 | 0.133 |
| [0.3,0.4) | 20 | 0.357 | 0.250 |
| [0.4,0.5) | 15 | 0.454 | 0.133 |
| [0.5,0.6) | 17 | 0.544 | 0.118 |
| [0.6,0.7) | 29 | 0.655 | 0.448 |
| [0.7,0.8) | 41 | 0.753 | 0.829 |
| [0.8,0.9) | 48 | 0.862 | 0.854 |
| [0.9,1.0] | 138 | 0.953 | 0.993 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.4,0.5) | 10 | 0.464 | 0.400 |
| [0.5,0.6) | 12 | 0.548 | 0.750 |
| [0.6,0.7) | 19 | 0.660 | 0.737 |
| [0.7,0.8) | 22 | 0.746 | 0.818 |
| [0.8,0.9) | 38 | 0.860 | 0.921 |
| [0.9,1.0] | 175 | 0.964 | 0.989 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 254 | 0.035 | 0.012 |
| [0.1,0.2) | 65 | 0.144 | 0.092 |
| [0.2,0.3) | 35 | 0.246 | 0.057 |
| [0.3,0.4) | 29 | 0.337 | 0.172 |
| [0.4,0.5) | 26 | 0.453 | 0.308 |
| [0.5,0.6) | 32 | 0.552 | 0.500 |
| [0.6,0.7) | 31 | 0.646 | 0.677 |
| [0.7,0.8) | 47 | 0.744 | 0.787 |
| [0.8,0.9) | 52 | 0.860 | 0.846 |
| [0.9,1.0] | 293 | 0.956 | 0.976 |


Answered 946/946; errors 0; accuracy counting failures as wrong 84.9%.
Paired vs ours (images_v1/eval_llm): ours only right 105, imajev-4b only right 33, p = 6.1e-10
