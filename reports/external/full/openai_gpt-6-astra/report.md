# Evaluation report

- model `openai/gpt-6-astra` @ `-`, adapter `None`, prompt `openai/gpt-6-astra` (-)
- data reports/external/full/subset.jsonl; splits ['test']; n=3471; calibration `None`
- - / -; 2026-09-23T09:40:46-0700; wall 0.0s

## Overall

question accuracy 85.8%

![reliability](reliability.svg)

**binary**: n 984, positives 475, accuracy 0.938, precision 0.964, recall 0.905, f1 0.934, auroc 0.971, brier 0.058, log_loss 0.431, ece 0.050

**multiclass**: n 2143, accuracy 0.870, macro_f1 0.953, log_loss 0.605, brier 0.215, ece_top_label 0.087

**multilabel**: n 344, labels 2029, exact_match 0.558, micro_f1 0.740, macro_f1 0.902, label_auroc 0.940, brier 0.087, log_loss 0.296, ece 0.063

## By family

| family | n | question acc % | details |
|---|---|---|---|
| eval_adversarial | 27 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.001; mc acc 100.0 mF1 100.0 ECE 0.000; ml EM 100.0 µF1 100.0 ECE 0.000 |
| eval_agent_output | 26 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.000; mc acc 100.0 mF1 100.0 ECE 0.000; ml EM 100.0 µF1 100.0 ECE 0.000 |
| eval_evidence | 17 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.000; ml EM 100.0 µF1 100.0 ECE 0.000 |
| eval_multilabel | 32 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.000; mc acc 100.0 mF1 100.0 ECE 0.000; ml EM 100.0 µF1 100.0 ECE 0.000 |
| eval_policy | 22 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.000; mc acc 100.0 mF1 100.0 ECE 0.000; ml EM 100.0 µF1 100.0 ECE 0.000 |
| eval_routing | 25 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.000; mc acc 100.0 mF1 100.0 ECE 0.000; ml EM 100.0 µF1 100.0 ECE 0.000 |
| eval_urgency_sentiment | 22 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.002; mc acc 100.0 mF1 100.0 ECE 0.001; ml EM 100.0 µF1 100.0 ECE 0.000 |
| heldout_boolq | 300 | 89.0 | bin acc 89.0 F1 90.5 AUROC 0.940 ECE 0.101 |
| heldout_emotion_multiclass | 300 | 62.3 | mc acc 62.3 mF1 54.6 ECE 0.233 |
| heldout_intent_clinc | 300 | 95.3 | mc acc 95.3 mF1 95.9 ECE 0.042 |
| heldout_question_type_trec | 300 | 95.3 | mc acc 95.3 mF1 94.5 ECE 0.042 |
| heldout_sentiment_sst2 | 300 | 97.0 | bin acc 97.0 F1 96.9 AUROC 0.988 ECE 0.020 |
| heldout_topic_dbpedia | 300 | 99.0 | mc acc 99.0 mF1 98.9 ECE 0.009 |
| hf_emotions_multilabel | 300 | 49.3 | ml EM 49.3 µF1 67.6 ECE 0.071 |
| hf_intent_banking77 | 300 | 96.3 | mc acc 96.3 mF1 96.4 ECE 0.023 |
| hf_nli | 300 | 93.7 | bin acc 93.7 F1 90.6 AUROC 0.977 ECE 0.062 |
| hf_sentiment_tweets | 300 | 68.7 | mc acc 68.7 mF1 68.9 ECE 0.205 |
| hf_topic_agnews | 300 | 90.0 | mc acc 90.0 mF1 89.9 ECE 0.083 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 3042 | 85.0 |
| contradiction | 107 | 100.0 |
| distractor | 33 | 100.0 |
| double_negation | 6 | 100.0 |
| evidence_end | 13 | 100.0 |
| evidence_middle | 11 | 100.0 |
| evidence_start | 9 | 100.0 |
| exception | 7 | 100.0 |
| hypothetical | 7 | 100.0 |
| injection | 10 | 100.0 |
| lexical_overlap | 20 | 100.0 |
| long_state | 50 | 100.0 |
| missing_evidence | 104 | 98.1 |
| multi_positive | 81 | 58.0 |
| multi_turn | 9 | 100.0 |
| negation | 30 | 100.0 |
| new_label_names | 3 | 100.0 |
| nota | 46 | 100.0 |
| numeric_reasoning | 16 | 100.0 |
| paraphrase | 22 | 100.0 |
| role_reversal | 15 | 100.0 |
| sarcasm | 12 | 100.0 |
| temporal_reasoning | 29 | 100.0 |
| zero_positive | 6 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 3211 | 85.1 |
| 00128-00511 | 208 | 94.2 |
| 00512-02047 | 52 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 984 | 93.8 |
| 03 | 310 | 69.7 |
| 04 | 333 | 91.0 |
| 05 | 22 | 100.0 |
| 06 | 1218 | 76.8 |
| 07 | 49 | 100.0 |
| 08 | 555 | 95.5 |

## Paraphrase groups

11 groups; same prediction 81.8%; all correct 100.0%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 13.0 |
| 0.4 | 99.9 | 12.9 |
| 0.5 | 99.7 | 12.9 |
| 0.6 | 99.1 | 12.5 |
| 0.7 | 96.2 | 11.3 |
| 0.8 | 92.0 | 9.8 |
| 0.9 | 86.0 | 7.3 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 530 | 0.007 | 0.075 |
| [0.1,0.2) | 6 | 0.138 | 0.667 |
| [0.3,0.4) | 2 | 0.375 | 0.500 |
| [0.7,0.8) | 4 | 0.748 | 1.000 |
| [0.8,0.9) | 14 | 0.856 | 0.786 |
| [0.9,1.0] | 428 | 0.988 | 0.970 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 1 | 0.200 | 0.000 |
| [0.3,0.4) | 2 | 0.320 | 0.500 |
| [0.4,0.5) | 3 | 0.473 | 0.333 |
| [0.5,0.6) | 14 | 0.557 | 0.286 |
| [0.6,0.7) | 61 | 0.654 | 0.475 |
| [0.7,0.8) | 90 | 0.754 | 0.567 |
| [0.8,0.9) | 130 | 0.850 | 0.546 |
| [0.9,1.0] | 1842 | 0.989 | 0.927 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 1429 | 0.013 | 0.041 |
| [0.1,0.2) | 93 | 0.141 | 0.247 |
| [0.2,0.3) | 37 | 0.245 | 0.432 |
| [0.3,0.4) | 16 | 0.341 | 0.438 |
| [0.4,0.5) | 18 | 0.443 | 0.611 |
| [0.5,0.6) | 13 | 0.558 | 0.462 |
| [0.6,0.7) | 36 | 0.653 | 0.528 |
| [0.7,0.8) | 47 | 0.751 | 0.553 |
| [0.8,0.9) | 59 | 0.851 | 0.576 |
| [0.9,1.0] | 281 | 0.976 | 0.851 |
