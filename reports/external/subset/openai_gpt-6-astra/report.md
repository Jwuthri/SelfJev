# Evaluation report

- model `openai/gpt-6-astra` @ `-`, adapter `None`, prompt `openai/gpt-6-astra` (-)
- data reports/external/subset/subset.jsonl; splits ['test']; n=501; calibration `None`
- - / -; 2026-09-23T01:54:54-0700; wall 0.0s

## Overall

question accuracy 90.2%

![reliability](reliability.svg)

**binary**: n 174, positives 84, accuracy 0.943, precision 0.963, recall 0.917, f1 0.939, auroc 0.974, brier 0.055, log_loss 0.576, ece 0.056

**multiclass**: n 253, accuracy 0.897, macro_f1 0.931, log_loss 0.499, brier 0.180, ece_top_label 0.079

**multilabel**: n 74, labels 409, exact_match 0.824, micro_f1 0.921, macro_f1 0.926, label_auroc 0.993, brier 0.035, log_loss 0.114, ece 0.028

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
| heldout_boolq | 30 | 80.0 | bin acc 80.0 F1 84.2 AUROC 0.828 ECE 0.190 |
| heldout_emotion_multiclass | 30 | 80.0 | mc acc 80.0 mF1 77.8 ECE 0.171 |
| heldout_intent_clinc | 30 | 86.7 | mc acc 86.7 mF1 86.2 ECE 0.122 |
| heldout_question_type_trec | 30 | 100.0 | mc acc 100.0 mF1 100.0 ECE 0.001 |
| heldout_sentiment_sst2 | 30 | 96.7 | bin acc 96.7 F1 96.8 AUROC 0.996 ECE 0.068 |
| heldout_topic_dbpedia | 30 | 100.0 | mc acc 100.0 mF1 100.0 ECE 0.000 |
| hf_emotions_multilabel | 30 | 56.7 | ml EM 56.7 µF1 71.6 ECE 0.063 |
| hf_intent_banking77 | 30 | 96.7 | mc acc 96.7 mF1 94.9 ECE 0.024 |
| hf_nli | 30 | 90.0 | bin acc 90.0 F1 85.7 AUROC 0.979 ECE 0.089 |
| hf_sentiment_tweets | 30 | 63.3 | mc acc 63.3 mF1 65.7 ECE 0.256 |
| hf_topic_agnews | 30 | 86.7 | mc acc 86.7 mF1 86.1 ECE 0.139 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 335 | 86.3 |
| contradiction | 20 | 100.0 |
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
| missing_evidence | 18 | 100.0 |
| multi_positive | 35 | 91.4 |
| multi_turn | 9 | 100.0 |
| negation | 30 | 100.0 |
| new_label_names | 3 | 100.0 |
| nota | 2 | 100.0 |
| numeric_reasoning | 16 | 100.0 |
| paraphrase | 22 | 100.0 |
| role_reversal | 15 | 100.0 |
| sarcasm | 12 | 100.0 |
| temporal_reasoning | 29 | 100.0 |
| zero_positive | 6 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 372 | 87.4 |
| 00128-00511 | 79 | 97.5 |
| 00512-02047 | 50 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 174 | 94.3 |
| 03 | 40 | 72.5 |
| 04 | 63 | 93.7 |
| 05 | 22 | 100.0 |
| 06 | 138 | 86.2 |
| 07 | 5 | 100.0 |
| 08 | 59 | 91.5 |

## Paraphrase groups

11 groups; same prediction 81.8%; all correct 100.0%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 10.3 |
| 0.4 | 100.0 | 10.3 |
| 0.5 | 99.6 | 9.9 |
| 0.6 | 98.8 | 9.6 |
| 0.7 | 96.0 | 9.5 |
| 0.8 | 93.7 | 8.9 |
| 0.9 | 88.9 | 7.1 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 91 | 0.005 | 0.055 |
| [0.1,0.2) | 2 | 0.120 | 1.000 |
| [0.3,0.4) | 1 | 0.370 | 0.000 |
| [0.7,0.8) | 2 | 0.725 | 1.000 |
| [0.9,1.0] | 78 | 0.994 | 0.962 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.4,0.5) | 1 | 0.450 | 0.000 |
| [0.5,0.6) | 2 | 0.580 | 0.500 |
| [0.6,0.7) | 7 | 0.655 | 0.857 |
| [0.7,0.8) | 6 | 0.758 | 0.667 |
| [0.8,0.9) | 12 | 0.861 | 0.583 |
| [0.9,1.0] | 225 | 0.992 | 0.929 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 273 | 0.007 | 0.011 |
| [0.1,0.2) | 11 | 0.149 | 0.364 |
| [0.2,0.3) | 2 | 0.250 | 0.500 |
| [0.3,0.4) | 2 | 0.365 | 0.000 |
| [0.4,0.5) | 2 | 0.430 | 1.000 |
| [0.6,0.7) | 4 | 0.660 | 0.500 |
| [0.7,0.8) | 3 | 0.763 | 0.667 |
| [0.8,0.9) | 7 | 0.846 | 0.571 |
| [0.9,1.0] | 105 | 0.996 | 0.971 |
