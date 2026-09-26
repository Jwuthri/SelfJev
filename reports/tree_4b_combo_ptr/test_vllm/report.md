# Evaluation report

- model `Qwen/Qwen3-4B-Instruct-2507` @ `cdbee75f17` (tree paths (tree-v1) on vLLM), adapter/checkpoint `merged into runs/tree_4b_combo_ptr/merged`, prompt `tree-v1` (c8963d819128)
- data data/ptr/hf.jsonl, data/ptr/eval.jsonl; splits ['test']; n=3471; calibration `None`
- cuda / bfloat16; 2026-09-25T01:01:21+0000; wall 94.7s

## Overall

question accuracy 82.7%

![reliability](reliability.svg)

**binary**: n 984, positives 475, accuracy 0.898, precision 0.935, recall 0.848, f1 0.890, auroc 0.965, brier 0.077, log_loss 0.264, ece 0.054

**multiclass**: n 2143, accuracy 0.836, macro_f1 0.894, log_loss 0.472, brier 0.237, ece_top_label 0.018

**multilabel**: n 344, labels 2029, exact_match 0.564, micro_f1 0.762, macro_f1 0.780, label_auroc 0.951, brier 0.071, log_loss 0.230, ece 0.021

## By family

| family | n | question acc % | details |
|---|---|---|---|
| eval_adversarial | 27 | 92.6 | bin acc 93.3 F1 90.9 AUROC 0.907 ECE 0.082; mc acc 100.0 mF1 100.0 ECE 0.014; ml EM 80.0 µF1 94.1 ECE 0.052 |
| eval_agent_output | 26 | 53.8 | bin acc 71.4 F1 71.4 AUROC 0.878 ECE 0.219; mc acc 28.6 mF1 18.8 ECE 0.515; ml EM 40.0 µF1 71.4 ECE 0.155 |
| eval_evidence | 17 | 94.1 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.010; ml EM 50.0 µF1 66.7 ECE 0.175 |
| eval_multilabel | 32 | 87.5 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.029; mc acc 100.0 mF1 100.0 ECE 0.661; ml EM 83.3 µF1 94.9 ECE 0.034 |
| eval_policy | 22 | 59.1 | bin acc 69.2 F1 66.7 AUROC 0.833 ECE 0.181; mc acc 40.0 mF1 25.0 ECE 0.570; ml EM 50.0 µF1 87.5 ECE 0.228 |
| eval_routing | 25 | 88.0 | bin acc 90.0 F1 88.9 AUROC 0.917 ECE 0.098; mc acc 100.0 mF1 100.0 ECE 0.056; ml EM 0.0 µF1 66.7 ECE 0.169 |
| eval_urgency_sentiment | 22 | 95.5 | bin acc 90.0 F1 92.3 AUROC 0.958 ECE 0.053; mc acc 100.0 mF1 100.0 ECE 0.088; ml EM 100.0 µF1 100.0 ECE 0.008 |
| heldout_boolq | 300 | 86.3 | bin acc 86.3 F1 88.0 AUROC 0.942 ECE 0.087 |
| heldout_emotion_multiclass | 300 | 55.3 | mc acc 55.3 mF1 46.0 ECE 0.140 |
| heldout_intent_clinc | 300 | 95.7 | mc acc 95.7 mF1 96.5 ECE 0.067 |
| heldout_question_type_trec | 300 | 90.7 | mc acc 90.7 mF1 89.8 ECE 0.094 |
| heldout_sentiment_sst2 | 300 | 89.0 | bin acc 89.0 F1 87.9 AUROC 0.971 ECE 0.092 |
| heldout_topic_dbpedia | 300 | 96.7 | mc acc 96.7 mF1 96.3 ECE 0.014 |
| hf_emotions_multilabel | 300 | 54.3 | ml EM 54.3 µF1 72.8 ECE 0.027 |
| hf_intent_banking77 | 300 | 93.7 | mc acc 93.7 mF1 92.3 ECE 0.042 |
| hf_nli | 300 | 95.0 | bin acc 95.0 F1 93.1 AUROC 0.986 ECE 0.041 |
| hf_sentiment_tweets | 300 | 63.0 | mc acc 63.0 mF1 63.6 ECE 0.114 |
| hf_topic_agnews | 300 | 90.7 | mc acc 90.7 mF1 90.7 ECE 0.032 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 3042 | 82.5 |
| contradiction | 107 | 97.2 |
| distractor | 33 | 72.7 |
| double_negation | 6 | 100.0 |
| evidence_end | 13 | 92.3 |
| evidence_middle | 11 | 90.9 |
| evidence_start | 9 | 100.0 |
| exception | 7 | 71.4 |
| hypothetical | 7 | 85.7 |
| injection | 10 | 90.0 |
| lexical_overlap | 20 | 90.0 |
| long_state | 50 | 84.0 |
| missing_evidence | 104 | 93.3 |
| multi_positive | 81 | 44.4 |
| multi_turn | 9 | 88.9 |
| negation | 30 | 83.3 |
| new_label_names | 3 | 33.3 |
| nota | 46 | 97.8 |
| numeric_reasoning | 16 | 81.2 |
| paraphrase | 22 | 77.3 |
| role_reversal | 15 | 86.7 |
| sarcasm | 12 | 75.0 |
| temporal_reasoning | 29 | 65.5 |
| zero_positive | 6 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 3211 | 82.6 |
| 00128-00511 | 208 | 84.1 |
| 00512-02047 | 52 | 84.6 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 984 | 89.8 |
| 03 | 310 | 63.9 |
| 04 | 333 | 89.2 |
| 05 | 22 | 63.6 |
| 06 | 1218 | 74.3 |
| 07 | 49 | 98.0 |
| 08 | 555 | 94.4 |

## Paraphrase groups

11 groups; same prediction 63.6%; all correct 72.7%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 16.4 |
| 0.4 | 97.3 | 15.3 |
| 0.5 | 92.9 | 13.5 |
| 0.6 | 86.8 | 10.9 |
| 0.7 | 79.4 | 8.0 |
| 0.8 | 71.1 | 6.0 |
| 0.9 | 56.3 | 3.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 422 | 0.015 | 0.045 |
| [0.1,0.2) | 47 | 0.143 | 0.340 |
| [0.2,0.3) | 30 | 0.251 | 0.367 |
| [0.3,0.4) | 28 | 0.341 | 0.357 |
| [0.4,0.5) | 26 | 0.451 | 0.615 |
| [0.5,0.6) | 29 | 0.555 | 0.724 |
| [0.6,0.7) | 29 | 0.647 | 0.828 |
| [0.7,0.8) | 34 | 0.749 | 0.765 |
| [0.8,0.9) | 74 | 0.856 | 0.946 |
| [0.9,1.0] | 265 | 0.967 | 0.989 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 8 | 0.270 | 0.375 |
| [0.3,0.4) | 49 | 0.362 | 0.449 |
| [0.4,0.5) | 95 | 0.455 | 0.474 |
| [0.5,0.6) | 130 | 0.549 | 0.485 |
| [0.6,0.7) | 160 | 0.647 | 0.588 |
| [0.7,0.8) | 178 | 0.749 | 0.747 |
| [0.8,0.9) | 316 | 0.857 | 0.842 |
| [0.9,1.0] | 1207 | 0.974 | 0.966 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 1167 | 0.021 | 0.015 |
| [0.1,0.2) | 181 | 0.144 | 0.110 |
| [0.2,0.3) | 95 | 0.242 | 0.211 |
| [0.3,0.4) | 98 | 0.346 | 0.255 |
| [0.4,0.5) | 70 | 0.448 | 0.443 |
| [0.5,0.6) | 73 | 0.553 | 0.438 |
| [0.6,0.7) | 63 | 0.647 | 0.651 |
| [0.7,0.8) | 85 | 0.753 | 0.788 |
| [0.8,0.9) | 74 | 0.851 | 0.905 |
| [0.9,1.0] | 123 | 0.967 | 0.976 |
