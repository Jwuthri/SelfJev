# Evaluation report

- model `Qwen/Qwen3-4B-Instruct-2507` @ `cdbee75f17` (tree paths (tree-v1) on vLLM), adapter/checkpoint `merged into runs/tree_4b_combo_r2/merged`, prompt `tree-v1` (c8963d819128)
- data data/ova/hf.jsonl, data/ova/eval.jsonl; splits ['test']; n=3471; calibration `None`
- cuda / bfloat16; 2026-09-24T21:53:34+0000; wall 104.0s

## Overall

question accuracy 83.5%

![reliability](reliability.svg)

**binary**: n 984, positives 475, accuracy 0.898, precision 0.919, recall 0.865, f1 0.892, auroc 0.966, brier 0.072, log_loss 0.247, ece 0.037

**multiclass**: n 2143, accuracy 0.845, macro_f1 0.893, log_loss 0.454, brier 0.225, ece_top_label 0.045

**multilabel**: n 344, labels 2029, exact_match 0.596, micro_f1 0.777, macro_f1 0.808, label_auroc 0.954, brier 0.067, log_loss 0.222, ece 0.016

## By family

| family | n | question acc % | details |
|---|---|---|---|
| eval_adversarial | 27 | 96.3 | bin acc 93.3 F1 90.9 AUROC 0.907 ECE 0.086; mc acc 100.0 mF1 100.0 ECE 0.002; ml EM 100.0 µF1 100.0 ECE 0.011 |
| eval_agent_output | 26 | 61.5 | bin acc 85.7 F1 85.7 AUROC 0.918 ECE 0.157; mc acc 42.9 mF1 31.0 ECE 0.482; ml EM 20.0 µF1 66.7 ECE 0.196 |
| eval_evidence | 17 | 94.1 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.018; ml EM 50.0 µF1 57.1 ECE 0.230 |
| eval_multilabel | 32 | 93.8 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.026; mc acc 0.0 mF1 0.0 ECE 0.555; ml EM 95.8 µF1 98.0 ECE 0.020 |
| eval_policy | 22 | 63.6 | bin acc 69.2 F1 71.4 AUROC 0.738 ECE 0.244; mc acc 40.0 mF1 25.0 ECE 0.505; ml EM 75.0 µF1 94.1 ECE 0.119 |
| eval_routing | 25 | 88.0 | bin acc 90.0 F1 88.9 AUROC 0.958 ECE 0.114; mc acc 92.3 mF1 81.8 ECE 0.071; ml EM 50.0 µF1 80.0 ECE 0.087 |
| eval_urgency_sentiment | 22 | 95.5 | bin acc 90.0 F1 92.3 AUROC 0.958 ECE 0.149; mc acc 100.0 mF1 100.0 ECE 0.037; ml EM 100.0 µF1 100.0 ECE 0.004 |
| heldout_boolq | 300 | 85.3 | bin acc 85.3 F1 87.0 AUROC 0.949 ECE 0.070 |
| heldout_emotion_multiclass | 300 | 55.0 | mc acc 55.0 mF1 44.0 ECE 0.226 |
| heldout_intent_clinc | 300 | 96.0 | mc acc 96.0 mF1 97.2 ECE 0.024 |
| heldout_question_type_trec | 300 | 93.0 | mc acc 93.0 mF1 92.6 ECE 0.040 |
| heldout_sentiment_sst2 | 300 | 90.3 | bin acc 90.3 F1 89.9 AUROC 0.971 ECE 0.060 |
| heldout_topic_dbpedia | 300 | 96.7 | mc acc 96.7 mF1 96.3 ECE 0.020 |
| hf_emotions_multilabel | 300 | 56.3 | ml EM 56.3 µF1 73.8 ECE 0.014 |
| hf_intent_banking77 | 300 | 94.3 | mc acc 94.3 mF1 93.3 ECE 0.013 |
| hf_nli | 300 | 94.0 | bin acc 94.0 F1 91.8 AUROC 0.986 ECE 0.028 |
| hf_sentiment_tweets | 300 | 67.3 | mc acc 67.3 mF1 67.9 ECE 0.086 |
| hf_topic_agnews | 300 | 89.7 | mc acc 89.7 mF1 89.7 ECE 0.049 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 3042 | 83.4 |
| contradiction | 107 | 99.1 |
| distractor | 33 | 69.7 |
| double_negation | 6 | 83.3 |
| evidence_end | 13 | 84.6 |
| evidence_middle | 11 | 81.8 |
| evidence_start | 9 | 88.9 |
| exception | 7 | 57.1 |
| hypothetical | 7 | 100.0 |
| injection | 10 | 90.0 |
| lexical_overlap | 20 | 95.0 |
| long_state | 50 | 82.0 |
| missing_evidence | 104 | 90.4 |
| multi_positive | 81 | 48.1 |
| multi_turn | 9 | 88.9 |
| negation | 30 | 96.7 |
| new_label_names | 3 | 66.7 |
| nota | 46 | 97.8 |
| numeric_reasoning | 16 | 81.2 |
| paraphrase | 22 | 95.5 |
| role_reversal | 15 | 93.3 |
| sarcasm | 12 | 100.0 |
| temporal_reasoning | 29 | 65.5 |
| zero_positive | 6 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 3211 | 83.5 |
| 00128-00511 | 208 | 83.7 |
| 00512-02047 | 52 | 82.7 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 984 | 89.8 |
| 03 | 310 | 68.1 |
| 04 | 333 | 88.6 |
| 05 | 22 | 72.7 |
| 06 | 1218 | 75.4 |
| 07 | 49 | 98.0 |
| 08 | 555 | 95.0 |

## Paraphrase groups

11 groups; same prediction 72.7%; all correct 90.9%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 15.5 |
| 0.4 | 99.2 | 15.0 |
| 0.5 | 96.3 | 13.3 |
| 0.6 | 89.9 | 11.0 |
| 0.7 | 84.7 | 9.3 |
| 0.8 | 79.0 | 7.1 |
| 0.9 | 68.4 | 4.3 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 413 | 0.016 | 0.046 |
| [0.1,0.2) | 41 | 0.151 | 0.268 |
| [0.2,0.3) | 30 | 0.258 | 0.200 |
| [0.3,0.4) | 32 | 0.348 | 0.469 |
| [0.4,0.5) | 21 | 0.451 | 0.619 |
| [0.5,0.6) | 25 | 0.545 | 0.520 |
| [0.6,0.7) | 30 | 0.653 | 0.700 |
| [0.7,0.8) | 33 | 0.758 | 0.788 |
| [0.8,0.9) | 47 | 0.861 | 0.979 |
| [0.9,1.0] | 312 | 0.972 | 0.978 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 4 | 0.273 | 0.250 |
| [0.3,0.4) | 14 | 0.367 | 0.214 |
| [0.4,0.5) | 62 | 0.463 | 0.274 |
| [0.5,0.6) | 136 | 0.548 | 0.544 |
| [0.6,0.7) | 111 | 0.644 | 0.613 |
| [0.7,0.8) | 123 | 0.750 | 0.610 |
| [0.8,0.9) | 228 | 0.857 | 0.746 |
| [0.9,1.0] | 1465 | 0.981 | 0.957 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 1290 | 0.017 | 0.021 |
| [0.1,0.2) | 122 | 0.144 | 0.164 |
| [0.2,0.3) | 75 | 0.249 | 0.160 |
| [0.3,0.4) | 55 | 0.346 | 0.327 |
| [0.4,0.5) | 72 | 0.448 | 0.431 |
| [0.5,0.6) | 54 | 0.545 | 0.370 |
| [0.6,0.7) | 57 | 0.649 | 0.702 |
| [0.7,0.8) | 61 | 0.753 | 0.803 |
| [0.8,0.9) | 91 | 0.851 | 0.846 |
| [0.9,1.0] | 152 | 0.969 | 0.961 |
