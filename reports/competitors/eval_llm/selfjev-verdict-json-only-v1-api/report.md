# Evaluation report

- model `selfjev-verdict-json-only-v1-api` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / -; 2026-10-01T22:07:48+0000; wall 143.2s

## Overall

question accuracy 89.7%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.924, precision 0.885, recall 0.976, f1 0.928, auroc 0.976, brier 0.062, log_loss 0.223, ece 0.056

**multiclass**: n 276, accuracy 0.942, macro_f1 0.906, log_loss 0.164, brier 0.083, ece_top_label 0.016

**multilabel**: n 182, labels 864, exact_match 0.758, micro_f1 0.921, macro_f1 0.855, label_auroc 0.977, brier 0.062, log_loss 0.202, ece 0.033

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 90.0 | bin acc 93.8 F1 93.3 AUROC 1.000 ECE 0.134; mc acc 100.0 mF1 100.0 ECE 0.045; ml EM 63.6 µF1 87.8 ECE 0.080 |
| tllm_guardrail_simple | 67 | 95.5 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.016; mc acc 100.0 mF1 100.0 ECE 0.024; ml EM 78.6 µF1 95.4 ECE 0.039 |
| tllm_guardrail_very_hard | 43 | 93.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.053; mc acc 85.7 mF1 69.2 ECE 0.088; ml EM 88.9 µF1 98.0 ECE 0.052 |
| tllm_jailbreak_hard | 59 | 98.3 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.072; mc acc 100.0 mF1 100.0 ECE 0.062; ml EM 91.7 µF1 98.2 ECE 0.078 |
| tllm_jailbreak_simple | 70 | 95.7 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.014; mc acc 95.5 mF1 92.5 ECE 0.046; ml EM 81.8 µF1 97.1 ECE 0.041 |
| tllm_jailbreak_very_hard | 60 | 85.0 | bin acc 87.5 F1 86.7 AUROC 0.955 ECE 0.130; mc acc 94.4 mF1 91.7 ECE 0.048; ml EM 60.0 µF1 92.9 ECE 0.087 |
| tllm_judge_hard | 86 | 93.0 | bin acc 90.0 F1 87.5 AUROC 0.952 ECE 0.110; mc acc 100.0 mF1 100.0 ECE 0.017; ml EM 90.5 µF1 94.3 ECE 0.050 |
| tllm_judge_simple | 72 | 95.8 | bin acc 97.4 F1 97.9 AUROC 0.994 ECE 0.051; mc acc 100.0 mF1 100.0 ECE 0.029; ml EM 85.7 µF1 97.7 ECE 0.050 |
| tllm_judge_very_hard | 64 | 92.2 | bin acc 93.8 F1 94.7 AUROC 0.980 ECE 0.074; mc acc 95.2 mF1 96.7 ECE 0.057; ml EM 81.8 µF1 97.2 ECE 0.072 |
| tllm_score_hard | 62 | 85.5 | bin acc 91.2 F1 91.4 AUROC 1.000 ECE 0.084; mc acc 100.0 mF1 100.0 ECE 0.053; ml EM 50.0 µF1 72.7 ECE 0.215 |
| tllm_score_simple | 62 | 96.8 | bin acc 97.1 F1 98.0 AUROC 0.983 ECE 0.052; mc acc 100.0 mF1 100.0 ECE 0.051; ml EM 91.7 µF1 98.5 ECE 0.046 |
| tllm_score_very_hard | 76 | 77.6 | bin acc 81.6 F1 74.1 AUROC 0.963 ECE 0.165; mc acc 81.8 mF1 68.0 ECE 0.094; ml EM 62.5 µF1 83.6 ECE 0.107 |
| tllm_verify_hard | 50 | 70.0 | bin acc 76.9 F1 76.9 AUROC 0.855 ECE 0.190; mc acc 75.0 mF1 64.7 ECE 0.229; ml EM 37.5 µF1 71.4 ECE 0.086 |
| tllm_verify_simple | 60 | 98.3 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.041; mc acc 100.0 mF1 100.0 ECE 0.006; ml EM 91.7 µF1 95.5 ECE 0.063 |
| tllm_verify_very_hard | 55 | 74.5 | bin acc 77.4 F1 74.1 AUROC 0.829 ECE 0.226; mc acc 80.0 mF1 70.8 ECE 0.118; ml EM 55.6 µF1 78.8 ECE 0.176 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 95.8 |
| answer_trace_mismatch | 45 | 86.7 |
| benign_lookalike | 88 | 86.4 |
| confident_wrong | 39 | 76.9 |
| contradiction | 22 | 95.5 |
| distractor | 117 | 84.6 |
| double_negation | 3 | 100.0 |
| evidence_end | 11 | 100.0 |
| evidence_middle | 20 | 80.0 |
| evidence_start | 2 | 50.0 |
| exception | 20 | 95.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 59.1 |
| format_near_miss | 46 | 78.3 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 96.0 |
| injection | 22 | 95.5 |
| judge_injection | 112 | 91.1 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 87.4 |
| long_state | 74 | 89.2 |
| missing_evidence | 35 | 91.4 |
| multi_positive | 124 | 78.2 |
| multi_turn | 44 | 84.1 |
| negation | 62 | 90.3 |
| nota | 55 | 87.3 |
| numeric_reasoning | 109 | 72.5 |
| obfuscation | 1 | 100.0 |
| over_refusal | 50 | 90.0 |
| paraphrase | 73 | 89.0 |
| partial_compliance | 31 | 74.2 |
| role_reversal | 6 | 66.7 |
| sarcasm | 8 | 87.5 |
| speaker_confusion | 58 | 89.7 |
| subtle_violation | 16 | 93.8 |
| sycophancy | 13 | 100.0 |
| temporal_reasoning | 20 | 85.0 |
| tool_misuse | 6 | 66.7 |
| unsupported_claim | 96 | 81.2 |
| zero_positive | 55 | 89.1 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 86.7 |
| 00128-00511 | 284 | 93.0 |
| 00512-02047 | 222 | 91.4 |
| 02048-08191 | 125 | 86.4 |
| 08192+ | 7 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 92.4 |
| 03 | 82 | 93.9 |
| 04 | 239 | 90.0 |
| 05 | 98 | 77.6 |
| 06 | 33 | 75.8 |
| 07 | 3 | 100.0 |
| 08 | 3 | 66.7 |

## Paraphrase groups

29 groups; same prediction 93.1%; all correct 86.2%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 5.8 |
| 0.4 | 99.3 | 5.1 |
| 0.5 | 98.6 | 4.4 |
| 0.6 | 97.1 | 3.7 |
| 0.7 | 94.2 | 2.7 |
| 0.8 | 90.6 | 2.4 |
| 0.9 | 85.5 | 1.3 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 169 | 0.020 | 0.006 |
| [0.1,0.2) | 17 | 0.142 | 0.059 |
| [0.2,0.3) | 8 | 0.262 | 0.250 |
| [0.3,0.4) | 10 | 0.339 | 0.000 |
| [0.4,0.5) | 14 | 0.458 | 0.143 |
| [0.5,0.6) | 10 | 0.567 | 0.500 |
| [0.6,0.7) | 8 | 0.644 | 0.250 |
| [0.7,0.8) | 10 | 0.754 | 0.500 |
| [0.8,0.9) | 15 | 0.851 | 0.800 |
| [0.9,1.0] | 227 | 0.985 | 0.947 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 2 | 0.368 | 0.000 |
| [0.4,0.5) | 2 | 0.438 | 0.000 |
| [0.5,0.6) | 4 | 0.537 | 0.500 |
| [0.6,0.7) | 8 | 0.642 | 0.625 |
| [0.7,0.8) | 10 | 0.769 | 0.900 |
| [0.8,0.9) | 14 | 0.866 | 0.786 |
| [0.9,1.0] | 236 | 0.988 | 0.987 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 306 | 0.020 | 0.026 |
| [0.1,0.2) | 42 | 0.149 | 0.143 |
| [0.2,0.3) | 33 | 0.245 | 0.182 |
| [0.3,0.4) | 29 | 0.339 | 0.172 |
| [0.4,0.5) | 18 | 0.439 | 0.278 |
| [0.5,0.6) | 14 | 0.546 | 0.429 |
| [0.6,0.7) | 10 | 0.641 | 0.600 |
| [0.7,0.8) | 16 | 0.744 | 0.562 |
| [0.8,0.9) | 22 | 0.865 | 0.591 |
| [0.9,1.0] | 374 | 0.988 | 0.973 |


Answered 946/946; errors 0; accuracy counting failures as wrong 89.7%.
Paired vs ours (images_v1/eval_llm): ours only right 41, selfjev-verdict-json-only-v1-api only right 15, p = 0.00069
