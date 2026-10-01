# Evaluation report

- model `decider-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / -; 2026-09-30T17:47:02+0000; wall 52.4s

## Overall

question accuracy 82.8%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.867, precision 0.857, recall 0.882, f1 0.869, auroc 0.937, brier 0.096, log_loss 0.320, ece 0.035

**multiclass**: n 276, accuracy 0.884, macro_f1 0.804, log_loss 0.354, brier 0.177, ece_top_label 0.033

**multilabel**: n 182, labels 864, exact_match 0.637, micro_f1 0.886, macro_f1 0.792, label_auroc 0.957, brier 0.083, log_loss 0.283, ece 0.052

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 81.7 | bin acc 84.4 F1 83.9 AUROC 0.984 ECE 0.170; mc acc 88.2 mF1 76.5 ECE 0.150; ml EM 63.6 µF1 84.2 ECE 0.153 |
| tllm_guardrail_simple | 67 | 92.5 | bin acc 97.1 F1 97.3 AUROC 1.000 ECE 0.086; mc acc 94.7 mF1 93.3 ECE 0.070; ml EM 78.6 µF1 95.2 ECE 0.076 |
| tllm_guardrail_very_hard | 43 | 88.4 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.081; mc acc 92.9 mF1 83.3 ECE 0.073; ml EM 55.6 µF1 91.3 ECE 0.138 |
| tllm_jailbreak_hard | 59 | 71.2 | bin acc 63.0 F1 58.3 AUROC 0.844 ECE 0.251; mc acc 90.0 mF1 81.7 ECE 0.087; ml EM 58.3 µF1 90.2 ECE 0.089 |
| tllm_jailbreak_simple | 70 | 92.9 | bin acc 94.6 F1 95.2 AUROC 0.991 ECE 0.101; mc acc 90.9 mF1 76.5 ECE 0.037; ml EM 90.9 µF1 98.6 ECE 0.112 |
| tllm_jailbreak_very_hard | 60 | 83.3 | bin acc 87.5 F1 84.6 AUROC 0.937 ECE 0.137; mc acc 83.3 mF1 78.4 ECE 0.135; ml EM 70.0 µF1 94.3 ECE 0.136 |
| tllm_judge_hard | 86 | 87.2 | bin acc 90.0 F1 86.7 AUROC 0.941 ECE 0.097; mc acc 88.0 mF1 76.8 ECE 0.072; ml EM 81.0 µF1 90.6 ECE 0.101 |
| tllm_judge_simple | 72 | 86.1 | bin acc 92.1 F1 93.9 AUROC 0.954 ECE 0.075; mc acc 90.0 mF1 81.2 ECE 0.094; ml EM 64.3 µF1 87.5 ECE 0.139 |
| tllm_judge_very_hard | 64 | 84.4 | bin acc 90.6 F1 91.4 AUROC 0.940 ECE 0.114; mc acc 95.2 mF1 90.8 ECE 0.108; ml EM 45.5 µF1 84.8 ECE 0.147 |
| tllm_score_hard | 62 | 79.0 | bin acc 88.2 F1 88.2 AUROC 0.972 ECE 0.134; mc acc 93.8 mF1 85.7 ECE 0.118; ml EM 33.3 µF1 75.0 ECE 0.188 |
| tllm_score_simple | 62 | 90.3 | bin acc 91.2 F1 93.9 AUROC 0.927 ECE 0.084; mc acc 93.8 mF1 88.2 ECE 0.106; ml EM 83.3 µF1 97.1 ECE 0.074 |
| tllm_score_very_hard | 76 | 77.6 | bin acc 86.8 F1 81.5 AUROC 0.965 ECE 0.129; mc acc 81.8 mF1 70.0 ECE 0.092; ml EM 50.0 µF1 81.4 ECE 0.068 |
| tllm_verify_hard | 50 | 68.0 | bin acc 65.4 F1 66.7 AUROC 0.700 ECE 0.162; mc acc 75.0 mF1 64.7 ECE 0.153; ml EM 62.5 µF1 90.3 ECE 0.170 |
| tllm_verify_simple | 60 | 86.7 | bin acc 90.9 F1 92.3 AUROC 0.974 ECE 0.116; mc acc 100.0 mF1 100.0 ECE 0.017; ml EM 58.3 µF1 82.5 ECE 0.155 |
| tllm_verify_very_hard | 55 | 65.5 | bin acc 71.0 F1 60.9 AUROC 0.761 ECE 0.169; mc acc 66.7 mF1 55.6 ECE 0.299; ml EM 44.4 µF1 72.0 ECE 0.145 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 90.9 |
| answer_trace_mismatch | 45 | 73.3 |
| benign_lookalike | 88 | 87.5 |
| confident_wrong | 39 | 61.5 |
| contradiction | 22 | 90.9 |
| distractor | 117 | 77.8 |
| double_negation | 3 | 66.7 |
| evidence_end | 11 | 90.9 |
| evidence_middle | 20 | 50.0 |
| evidence_start | 2 | 0.0 |
| exception | 20 | 100.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 59.1 |
| format_near_miss | 46 | 76.1 |
| gradual_escalation | 1 | 0.0 |
| hypothetical | 7 | 85.7 |
| indirect_injection | 25 | 64.0 |
| injection | 22 | 90.9 |
| judge_injection | 112 | 76.8 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 83.5 |
| long_state | 74 | 71.6 |
| missing_evidence | 35 | 88.6 |
| multi_positive | 124 | 60.5 |
| multi_turn | 44 | 79.5 |
| negation | 62 | 91.9 |
| nota | 55 | 78.2 |
| numeric_reasoning | 109 | 68.8 |
| obfuscation | 1 | 100.0 |
| over_refusal | 50 | 84.0 |
| paraphrase | 73 | 87.7 |
| partial_compliance | 31 | 71.0 |
| role_reversal | 6 | 83.3 |
| sarcasm | 8 | 75.0 |
| speaker_confusion | 58 | 84.5 |
| subtle_violation | 16 | 75.0 |
| sycophancy | 13 | 84.6 |
| temporal_reasoning | 20 | 80.0 |
| tool_misuse | 6 | 33.3 |
| unsupported_claim | 96 | 81.2 |
| zero_positive | 55 | 90.9 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 81.5 |
| 00128-00511 | 284 | 83.8 |
| 00512-02047 | 222 | 86.5 |
| 02048-08191 | 125 | 78.4 |
| 08192+ | 7 | 57.1 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 86.7 |
| 03 | 82 | 89.0 |
| 04 | 239 | 82.8 |
| 05 | 98 | 65.3 |
| 06 | 33 | 66.7 |
| 07 | 3 | 33.3 |
| 08 | 3 | 66.7 |

## Paraphrase groups

29 groups; same prediction 89.7%; all correct 82.8%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 11.6 |
| 0.4 | 99.6 | 11.3 |
| 0.5 | 97.1 | 10.4 |
| 0.6 | 93.8 | 8.9 |
| 0.7 | 88.4 | 7.0 |
| 0.8 | 83.3 | 6.1 |
| 0.9 | 73.6 | 4.9 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 133 | 0.040 | 0.045 |
| [0.1,0.2) | 46 | 0.143 | 0.109 |
| [0.2,0.3) | 25 | 0.250 | 0.280 |
| [0.3,0.4) | 16 | 0.349 | 0.188 |
| [0.4,0.5) | 16 | 0.440 | 0.500 |
| [0.5,0.6) | 25 | 0.552 | 0.480 |
| [0.6,0.7) | 29 | 0.652 | 0.621 |
| [0.7,0.8) | 30 | 0.752 | 0.833 |
| [0.8,0.9) | 51 | 0.852 | 0.961 |
| [0.9,1.0] | 117 | 0.957 | 0.957 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 1 | 0.388 | 0.000 |
| [0.4,0.5) | 7 | 0.462 | 0.571 |
| [0.5,0.6) | 9 | 0.551 | 0.444 |
| [0.6,0.7) | 15 | 0.640 | 0.600 |
| [0.7,0.8) | 14 | 0.755 | 0.786 |
| [0.8,0.9) | 27 | 0.855 | 0.852 |
| [0.9,1.0] | 203 | 0.979 | 0.951 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 244 | 0.035 | 0.029 |
| [0.1,0.2) | 96 | 0.147 | 0.146 |
| [0.2,0.3) | 58 | 0.250 | 0.172 |
| [0.3,0.4) | 38 | 0.343 | 0.395 |
| [0.4,0.5) | 41 | 0.440 | 0.512 |
| [0.5,0.6) | 33 | 0.550 | 0.727 |
| [0.6,0.7) | 37 | 0.658 | 0.811 |
| [0.7,0.8) | 48 | 0.747 | 0.896 |
| [0.8,0.9) | 79 | 0.859 | 0.962 |
| [0.9,1.0] | 190 | 0.954 | 0.989 |


Answered 946/946; errors 0; accuracy counting failures as wrong 82.8%.
Paired vs ours (images_v1/eval_llm): ours only right 117, decider-4b only right 25, p = 2e-15
