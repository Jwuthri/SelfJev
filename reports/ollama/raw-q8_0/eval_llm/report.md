# Evaluation report

- model `selfjev-q8_0` @ `307babdfc8` (one request per candidate on Ollama (prefix cache shares the state), readout logprob(yes) - logprob(no)), adapter/checkpoint `merged into the GGUF`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- ollama / Q8_0; 2026-10-01T06:53:00+0000; wall 554.1s

## Overall

question accuracy 91.8%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.936, precision 0.921, recall 0.955, f1 0.938, auroc 0.984, brier 0.048, log_loss 0.172, ece 0.038

**multiclass**: n 276, accuracy 0.938, macro_f1 0.893, log_loss 0.189, brier 0.095, ece_top_label 0.029

**multilabel**: n 182, labels 864, exact_match 0.835, micro_f1 0.956, macro_f1 0.918, label_auroc 0.989, brier 0.037, log_loss 0.140, ece 0.031

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 93.3 | bin acc 93.8 F1 93.3 AUROC 1.000 ECE 0.133; mc acc 100.0 mF1 100.0 ECE 0.069; ml EM 81.8 µF1 95.0 ECE 0.104 |
| tllm_guardrail_simple | 67 | 97.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.026; mc acc 100.0 mF1 100.0 ECE 0.039; ml EM 85.7 µF1 97.0 ECE 0.059 |
| tllm_guardrail_very_hard | 43 | 95.3 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.093; mc acc 92.9 mF1 83.3 ECE 0.052; ml EM 88.9 µF1 98.0 ECE 0.063 |
| tllm_jailbreak_hard | 59 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.060; mc acc 100.0 mF1 100.0 ECE 0.100; ml EM 100.0 µF1 100.0 ECE 0.070 |
| tllm_jailbreak_simple | 70 | 97.1 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.035; mc acc 95.5 mF1 87.5 ECE 0.049; ml EM 90.9 µF1 98.6 ECE 0.039 |
| tllm_jailbreak_very_hard | 60 | 85.0 | bin acc 87.5 F1 85.7 AUROC 0.972 ECE 0.107; mc acc 94.4 mF1 91.7 ECE 0.063; ml EM 60.0 µF1 92.9 ECE 0.084 |
| tllm_judge_hard | 86 | 95.3 | bin acc 95.0 F1 93.3 AUROC 0.971 ECE 0.090; mc acc 96.0 mF1 90.9 ECE 0.056; ml EM 95.2 µF1 96.2 ECE 0.040 |
| tllm_judge_simple | 72 | 97.2 | bin acc 97.4 F1 97.9 AUROC 0.997 ECE 0.065; mc acc 95.0 mF1 92.5 ECE 0.022; ml EM 100.0 µF1 100.0 ECE 0.045 |
| tllm_judge_very_hard | 64 | 92.2 | bin acc 96.9 F1 97.3 AUROC 0.996 ECE 0.073; mc acc 95.2 mF1 96.7 ECE 0.062; ml EM 72.7 µF1 95.8 ECE 0.081 |
| tllm_score_hard | 62 | 93.5 | bin acc 97.1 F1 97.0 AUROC 1.000 ECE 0.110; mc acc 87.5 mF1 73.3 ECE 0.085; ml EM 91.7 µF1 98.0 ECE 0.099 |
| tllm_score_simple | 62 | 95.2 | bin acc 94.1 F1 95.8 AUROC 0.992 ECE 0.068; mc acc 100.0 mF1 100.0 ECE 0.066; ml EM 91.7 µF1 98.5 ECE 0.043 |
| tllm_score_very_hard | 76 | 80.3 | bin acc 84.2 F1 75.0 AUROC 0.970 ECE 0.135; mc acc 86.4 mF1 75.0 ECE 0.064; ml EM 62.5 µF1 87.9 ECE 0.046 |
| tllm_verify_hard | 50 | 72.0 | bin acc 80.8 F1 80.0 AUROC 0.885 ECE 0.215; mc acc 75.0 mF1 61.1 ECE 0.182; ml EM 37.5 µF1 73.3 ECE 0.153 |
| tllm_verify_simple | 60 | 98.3 | bin acc 97.0 F1 97.6 AUROC 1.000 ECE 0.066; mc acc 100.0 mF1 100.0 ECE 0.010; ml EM 100.0 µF1 100.0 ECE 0.047 |
| tllm_verify_very_hard | 55 | 80.0 | bin acc 80.6 F1 75.0 AUROC 0.863 ECE 0.178; mc acc 86.7 mF1 82.2 ECE 0.171; ml EM 66.7 µF1 85.7 ECE 0.105 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 97.0 |
| answer_trace_mismatch | 45 | 86.7 |
| benign_lookalike | 88 | 86.4 |
| confident_wrong | 39 | 74.4 |
| contradiction | 22 | 95.5 |
| distractor | 117 | 89.7 |
| double_negation | 3 | 100.0 |
| evidence_end | 11 | 90.9 |
| evidence_middle | 20 | 75.0 |
| evidence_start | 2 | 50.0 |
| exception | 20 | 95.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 59.1 |
| format_near_miss | 46 | 84.8 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 96.0 |
| injection | 22 | 100.0 |
| judge_injection | 112 | 91.1 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 92.2 |
| long_state | 74 | 90.5 |
| missing_evidence | 35 | 94.3 |
| multi_positive | 124 | 83.1 |
| multi_turn | 44 | 84.1 |
| negation | 62 | 93.5 |
| nota | 55 | 89.1 |
| numeric_reasoning | 109 | 78.0 |
| obfuscation | 1 | 0.0 |
| over_refusal | 50 | 92.0 |
| paraphrase | 73 | 91.8 |
| partial_compliance | 31 | 74.2 |
| role_reversal | 6 | 66.7 |
| sarcasm | 8 | 87.5 |
| speaker_confusion | 58 | 91.4 |
| subtle_violation | 16 | 100.0 |
| sycophancy | 13 | 92.3 |
| temporal_reasoning | 20 | 95.0 |
| tool_misuse | 6 | 100.0 |
| unsupported_claim | 96 | 86.5 |
| zero_positive | 55 | 92.7 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 89.0 |
| 00128-00511 | 284 | 95.4 |
| 00512-02047 | 222 | 93.7 |
| 02048-08191 | 125 | 87.2 |
| 08192+ | 7 | 85.7 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 93.6 |
| 03 | 82 | 95.1 |
| 04 | 239 | 91.6 |
| 05 | 98 | 85.7 |
| 06 | 33 | 78.8 |
| 07 | 3 | 66.7 |
| 08 | 3 | 66.7 |

## Paraphrase groups

29 groups; same prediction 96.6%; all correct 89.7%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 6.2 |
| 0.4 | 100.0 | 6.2 |
| 0.5 | 98.9 | 5.5 |
| 0.6 | 95.3 | 3.8 |
| 0.7 | 90.2 | 3.2 |
| 0.8 | 84.8 | 2.1 |
| 0.9 | 76.1 | 0.5 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 180 | 0.040 | 0.006 |
| [0.1,0.2) | 23 | 0.139 | 0.043 |
| [0.2,0.3) | 13 | 0.249 | 0.231 |
| [0.3,0.4) | 9 | 0.331 | 0.333 |
| [0.4,0.5) | 9 | 0.446 | 0.333 |
| [0.5,0.6) | 8 | 0.543 | 0.250 |
| [0.6,0.7) | 9 | 0.671 | 0.889 |
| [0.7,0.8) | 15 | 0.755 | 0.800 |
| [0.8,0.9) | 27 | 0.857 | 0.778 |
| [0.9,1.0] | 195 | 0.970 | 0.979 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.4,0.5) | 3 | 0.439 | 0.333 |
| [0.5,0.6) | 10 | 0.532 | 0.500 |
| [0.6,0.7) | 14 | 0.654 | 0.857 |
| [0.7,0.8) | 15 | 0.756 | 0.800 |
| [0.8,0.9) | 24 | 0.856 | 0.833 |
| [0.9,1.0] | 210 | 0.979 | 0.995 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 352 | 0.036 | 0.017 |
| [0.1,0.2) | 52 | 0.137 | 0.154 |
| [0.2,0.3) | 12 | 0.247 | 0.000 |
| [0.3,0.4) | 16 | 0.347 | 0.188 |
| [0.4,0.5) | 11 | 0.437 | 0.455 |
| [0.5,0.6) | 14 | 0.545 | 0.643 |
| [0.6,0.7) | 13 | 0.655 | 0.769 |
| [0.7,0.8) | 13 | 0.759 | 0.923 |
| [0.8,0.9) | 31 | 0.865 | 0.903 |
| [0.9,1.0] | 350 | 0.971 | 0.991 |
