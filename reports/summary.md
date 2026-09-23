**Test split, n = 3471 questions (hf.jsonl test + eval.jsonl test)**

| | base | base+cal | LoRA | LoRA+cal |
|---|---|---|---|---|
| question accuracy % | 61.0 | 62.5 | 73.5 | 73.7 |
| binary accuracy % | 55.3 | 59.3 | 77.8 | 77.8 |
| binary F1 % | 55.8 | 50.4 | 75.1 | 74.9 |
| binary AUROC | 0.605 | 0.605 | 0.863 | 0.863 |
| multiclass accuracy % | 73.3 | 73.3 | 78.3 | 78.3 |
| multiclass macro-F1 % | 79.6 | 79.6 | 82.3 | 82.3 |
| multilabel exact match % | 1.2 | 4.1 | 31.1 | 32.6 |
| multilabel micro-F1 % | 23.6 | 41.4 | 62.9 | 65.5 |
| multilabel label AUROC | 0.679 | 0.679 | 0.882 | 0.882 |

**Calibration on the test split (lower is better)**

| | base | base+cal | LoRA | LoRA+cal |
|---|---|---|---|---|
| binary ece | 0.384 | 0.025 | 0.066 | 0.047 |
| binary brier | 0.397 | 0.244 | 0.155 | 0.153 |
| binary log_loss | 1.747 | 0.681 | 0.480 | 0.473 |
| multiclass ece_top_label | 0.026 | 0.047 | 0.027 | 0.035 |
| multiclass brier | 0.363 | 0.366 | 0.301 | 0.303 |
| multiclass log_loss | 0.717 | 0.723 | 0.601 | 0.598 |
| multilabel ece | 0.203 | 0.037 | 0.052 | 0.056 |
| multilabel brier | 0.208 | 0.160 | 0.113 | 0.113 |
| multilabel log_loss | 1.106 | 0.495 | 0.359 | 0.358 |

**Question accuracy % by family (test)**

| family | n | base | base+cal | LoRA | LoRA+cal |
|---|---|---|---|---|---|
| eval_adversarial | 27 | 74.1 | 63.0 | 63.0 | 63.0 |
| eval_agent_output | 26 | 30.8 | 30.8 | 46.2 | 46.2 |
| eval_evidence | 17 | 41.2 | 58.8 | 82.4 | 82.4 |
| eval_multilabel | 32 | 12.5 | 12.5 | 34.4 | 34.4 |
| eval_policy | 22 | 31.8 | 31.8 | 40.9 | 36.4 |
| eval_routing | 25 | 48.0 | 56.0 | 76.0 | 76.0 |
| eval_urgency_sentiment | 22 | 40.9 | 22.7 | 54.5 | 54.5 |
| heldout_boolq | 300 | 59.3 | 57.7 | 70.3 | 71.3 |
| heldout_emotion_multiclass | 300 | 51.0 | 51.0 | 56.0 | 56.0 |
| heldout_intent_clinc | 300 | 92.3 | 92.3 | 89.3 | 89.3 |
| heldout_question_type_trec | 300 | 64.3 | 64.3 | 68.0 | 68.0 |
| heldout_sentiment_sst2 | 300 | 50.0 | 50.0 | 76.7 | 76.0 |
| heldout_topic_dbpedia | 300 | 89.3 | 89.3 | 91.7 | 91.7 |
| hf_emotions_multilabel | 300 | 0.0 | 4.7 | 32.3 | 34.0 |
| hf_intent_banking77 | 300 | 89.3 | 89.3 | 92.7 | 92.7 |
| hf_nli | 300 | 56.7 | 71.0 | 89.0 | 89.0 |
| hf_sentiment_tweets | 300 | 54.3 | 54.3 | 66.7 | 66.7 |
| hf_topic_agnews | 300 | 77.3 | 77.3 | 86.7 | 86.7 |

**Question accuracy % by hard-case tag (test, tags with n >= 10)**

| tag | n | base | base+cal | LoRA | LoRA+cal |
|---|---|---|---|---|---|
| (none) | 3042 | 64.3 | 63.9 | 74.2 | 74.4 |
| contradiction | 107 | 30.8 | 64.5 | 90.7 | 90.7 |
| distractor | 33 | 21.2 | 21.2 | 45.5 | 45.5 |
| evidence_end | 13 | 38.5 | 38.5 | 46.2 | 46.2 |
| evidence_middle | 11 | 45.5 | 27.3 | 54.5 | 54.5 |
| injection | 10 | 60.0 | 50.0 | 50.0 | 50.0 |
| lexical_overlap | 20 | 40.0 | 40.0 | 55.0 | 55.0 |
| long_state | 50 | 36.0 | 34.0 | 46.0 | 46.0 |
| missing_evidence | 104 | 37.5 | 65.4 | 81.7 | 81.7 |
| multi_positive | 81 | 1.2 | 6.2 | 18.5 | 21.0 |
| negation | 30 | 33.3 | 33.3 | 56.7 | 53.3 |
| nota | 46 | 87.0 | 87.0 | 89.1 | 89.1 |
| numeric_reasoning | 16 | 37.5 | 50.0 | 37.5 | 31.2 |
| paraphrase | 22 | 18.2 | 18.2 | 50.0 | 50.0 |
| role_reversal | 15 | 40.0 | 40.0 | 46.7 | 46.7 |
| sarcasm | 12 | 8.3 | 25.0 | 33.3 | 33.3 |
| temporal_reasoning | 29 | 31.0 | 27.6 | 37.9 | 41.4 |

**Paraphrase groups** (11 groups, same state with reworded question or candidates): base: same prediction 72.7%, all correct 18.2%; base+cal: same prediction 63.6%, all correct 18.2%; LoRA: same prediction 45.5%, all correct 36.4%; LoRA+cal: same prediction 45.5%, all correct 36.4%

**Paired test, base vs LoRA (uncalibrated): questions only one of them gets right; exact McNemar p**

| slice | n | base only | LoRA only | p |
|---|---|---|---|---|
| all test questions | 3471 | 172 | 605 | 2.9e-57 |
| eval_adversarial | 27 | 5 | 2 | 0.45 |
| eval_agent_output | 26 | 6 | 10 | 0.45 |
| eval_evidence | 17 | 0 | 7 | 0.016 |
| eval_multilabel | 32 | 1 | 8 | 0.039 |
| eval_policy | 22 | 3 | 5 | 0.73 |
| eval_routing | 25 | 1 | 8 | 0.039 |
| eval_urgency_sentiment | 22 | 2 | 5 | 0.45 |
| heldout_boolq | 300 | 32 | 65 | 0.001 |
| heldout_emotion_multiclass | 300 | 19 | 34 | 0.053 |
| heldout_intent_clinc | 300 | 16 | 7 | 0.093 |
| heldout_question_type_trec | 300 | 24 | 35 | 0.19 |
| heldout_sentiment_sst2 | 300 | 1 | 81 | 3.4e-23 |
| heldout_topic_dbpedia | 300 | 6 | 13 | 0.17 |
| hf_emotions_multilabel | 300 | 0 | 97 | 1.3e-29 |
| hf_intent_banking77 | 300 | 8 | 18 | 0.076 |
| hf_nli | 300 | 10 | 107 | 1.2e-21 |
| hf_sentiment_tweets | 300 | 25 | 62 | 9.1e-05 |
| hf_topic_agnews | 300 | 13 | 41 | 0.00018 |

