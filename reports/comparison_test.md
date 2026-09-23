# Comparison: baseline vs lora vs baseline+cal vs lora+cal

| | baseline | lora | baseline+cal | lora+cal |
|---|---|---|---|---|
| adapter | None | runs/lora_pilot/adapter | None | runs/lora_pilot/adapter |
| calibration | no | no | yes | yes |
| prompt | task-v1 (f7b8d8022dfb) | task-v1 (f7b8d8022dfb) | task-v1 (f7b8d8022dfb) | task-v1 (f7b8d8022dfb) |
| n | 3471 | 3471 | 3471 | 3471 |

| slice | metric | baseline | lora | baseline+cal | lora+cal |
|---|---|---|---|---|---|
| overall | question acc % | 61.0 | 73.5 | 62.5 | 73.7 |
| overall | binary acc % | 55.3 | 77.8 | 59.3 | 77.8 |
| overall | binary F1 % | 55.8 | 75.1 | 50.4 | 74.9 |
| overall | binary AUROC | 0.605 | 0.863 | 0.605 | 0.863 |
| overall | binary ECE | 0.384 | 0.066 | 0.025 | 0.047 |
| overall | multiclass acc % | 73.3 | 78.3 | 73.3 | 78.3 |
| overall | multiclass macro-F1 % | 79.6 | 82.3 | 79.6 | 82.3 |
| overall | multiclass ECE | 0.026 | 0.027 | 0.047 | 0.035 |
| overall | multilabel exact % | 1.2 | 31.1 | 4.1 | 32.6 |
| overall | multilabel micro-F1 % | 23.6 | 62.9 | 41.4 | 65.5 |
| overall | multilabel label AUROC | 0.679 | 0.882 | 0.679 | 0.882 |
| overall | multilabel ECE | 0.203 | 0.052 | 0.037 | 0.056 |
| overall | binary brier | 0.397 | 0.155 | 0.244 | 0.153 |
| overall | binary log_loss | 1.747 | 0.480 | 0.681 | 0.473 |
| overall | multiclass brier | 0.363 | 0.301 | 0.366 | 0.303 |
| overall | multiclass log_loss | 0.717 | 0.601 | 0.723 | 0.598 |
| overall | multilabel brier | 0.208 | 0.113 | 0.160 | 0.113 |
| overall | multilabel log_loss | 1.106 | 0.359 | 0.495 | 0.358 |
| eval_adversarial | question acc % | 74.1 | 63.0 | 63.0 | 63.0 |
| eval_adversarial | binary acc % | 73.3 | 66.7 | 66.7 | 66.7 |
| eval_adversarial | binary F1 % | 75.0 | 66.7 | 61.5 | 66.7 |
| eval_adversarial | binary AUROC | 0.741 | 0.796 | 0.741 | 0.796 |
| eval_adversarial | binary ECE | 0.351 | 0.276 | 0.191 | 0.250 |
| eval_adversarial | multiclass acc % | 100.0 | 85.7 | 100.0 | 85.7 |
| eval_adversarial | multiclass macro-F1 % | 100.0 | 77.8 | 100.0 | 77.8 |
| eval_adversarial | multiclass ECE | 0.255 | 0.127 | 0.280 | 0.224 |
| eval_adversarial | multilabel exact % | 40.0 | 20.0 | 0.0 | 20.0 |
| eval_adversarial | multilabel micro-F1 % | 75.0 | 72.7 | 58.1 | 72.7 |
| eval_adversarial | multilabel label AUROC | 0.881 | 0.833 | 0.881 | 0.833 |
| eval_adversarial | multilabel ECE | 0.251 | 0.256 | 0.250 | 0.235 |
| eval_agent_output | question acc % | 30.8 | 46.2 | 30.8 | 46.2 |
| eval_agent_output | binary acc % | 42.9 | 57.1 | 50.0 | 57.1 |
| eval_agent_output | binary F1 % | 33.3 | 57.1 | 22.2 | 57.1 |
| eval_agent_output | binary AUROC | 0.510 | 0.592 | 0.510 | 0.592 |
| eval_agent_output | binary ECE | 0.454 | 0.355 | 0.112 | 0.354 |
| eval_agent_output | multiclass acc % | 14.3 | 57.1 | 14.3 | 57.1 |
| eval_agent_output | multiclass macro-F1 % | 11.1 | 38.1 | 11.1 | 38.1 |
| eval_agent_output | multiclass ECE | 0.493 | 0.438 | 0.465 | 0.303 |
| eval_agent_output | multilabel exact % | 20.0 | 0.0 | 0.0 | 0.0 |
| eval_agent_output | multilabel micro-F1 % | 57.1 | 66.7 | 48.0 | 57.1 |
| eval_agent_output | multilabel label AUROC | 0.644 | 0.779 | 0.644 | 0.779 |
| eval_agent_output | multilabel ECE | 0.286 | 0.239 | 0.188 | 0.170 |
| eval_evidence | question acc % | 41.2 | 82.4 | 58.8 | 82.4 |
| eval_evidence | binary acc % | 46.7 | 93.3 | 66.7 | 93.3 |
| eval_evidence | binary F1 % | 55.6 | 90.9 | 61.5 | 90.9 |
| eval_evidence | binary AUROC | 0.820 | 0.980 | 0.820 | 0.980 |
| eval_evidence | binary ECE | 0.526 | 0.147 | 0.210 | 0.168 |
| eval_evidence | multilabel exact % | 0.0 | 0.0 | 0.0 | 0.0 |
| eval_evidence | multilabel micro-F1 % | 54.5 | 40.0 | 42.9 | 40.0 |
| eval_evidence | multilabel label AUROC | 0.625 | 0.667 | 0.625 | 0.667 |
| eval_evidence | multilabel ECE | 0.467 | 0.464 | 0.342 | 0.437 |
| eval_multilabel | question acc % | 12.5 | 34.4 | 12.5 | 34.4 |
| eval_multilabel | binary acc % | 57.1 | 57.1 | 57.1 | 57.1 |
| eval_multilabel | binary F1 % | 66.7 | 57.1 | 57.1 | 57.1 |
| eval_multilabel | binary AUROC | 0.750 | 0.750 | 0.750 | 0.750 |
| eval_multilabel | binary ECE | 0.486 | 0.345 | 0.114 | 0.341 |
| eval_multilabel | multiclass acc % | 0.0 | 0.0 | 0.0 | 0.0 |
| eval_multilabel | multiclass macro-F1 % | 0.0 | 0.0 | 0.0 | 0.0 |
| eval_multilabel | multiclass ECE | 0.434 | 0.496 | 0.393 | 0.430 |
| eval_multilabel | multilabel exact % | 0.0 | 29.2 | 0.0 | 29.2 |
| eval_multilabel | multilabel micro-F1 % | 55.1 | 75.9 | 53.6 | 76.7 |
| eval_multilabel | multilabel label AUROC | 0.660 | 0.888 | 0.660 | 0.888 |
| eval_multilabel | multilabel ECE | 0.358 | 0.138 | 0.172 | 0.137 |
| eval_policy | question acc % | 31.8 | 40.9 | 31.8 | 36.4 |
| eval_policy | binary acc % | 46.2 | 46.2 | 46.2 | 38.5 |
| eval_policy | binary F1 % | 63.2 | 46.2 | 63.2 | 33.3 |
| eval_policy | binary AUROC | 0.548 | 0.429 | 0.548 | 0.429 |
| eval_policy | binary ECE | 0.536 | 0.500 | 0.113 | 0.482 |
| eval_policy | multiclass acc % | 20.0 | 40.0 | 20.0 | 40.0 |
| eval_policy | multiclass macro-F1 % | 12.5 | 23.8 | 12.5 | 23.8 |
| eval_policy | multiclass ECE | 0.241 | 0.521 | 0.403 | 0.389 |
| eval_policy | multilabel exact % | 0.0 | 25.0 | 0.0 | 25.0 |
| eval_policy | multilabel micro-F1 % | 69.6 | 66.7 | 69.6 | 66.7 |
| eval_policy | multilabel label AUROC | 0.464 | 0.732 | 0.464 | 0.732 |
| eval_policy | multilabel ECE | 0.465 | 0.386 | 0.278 | 0.333 |
| eval_routing | question acc % | 48.0 | 76.0 | 56.0 | 76.0 |
| eval_routing | binary acc % | 60.0 | 80.0 | 90.0 | 80.0 |
| eval_routing | binary F1 % | 66.7 | 75.0 | 85.7 | 75.0 |
| eval_routing | binary AUROC | 0.875 | 0.917 | 0.875 | 0.917 |
| eval_routing | binary ECE | 0.382 | 0.189 | 0.124 | 0.195 |
| eval_routing | multiclass acc % | 38.5 | 76.9 | 38.5 | 76.9 |
| eval_routing | multiclass macro-F1 % | 23.1 | 66.7 | 23.1 | 66.7 |
| eval_routing | multiclass ECE | 0.284 | 0.162 | 0.319 | 0.178 |
| eval_routing | multilabel exact % | 50.0 | 50.0 | 0.0 | 50.0 |
| eval_routing | multilabel micro-F1 % | 50.0 | 80.0 | 50.0 | 85.7 |
| eval_routing | multilabel label AUROC | 0.667 | 1.000 | 0.667 | 1.000 |
| eval_routing | multilabel ECE | 0.209 | 0.114 | 0.228 | 0.118 |
| eval_urgency_sentiment | question acc % | 40.9 | 54.5 | 22.7 | 54.5 |
| eval_urgency_sentiment | binary acc % | 60.0 | 80.0 | 20.0 | 80.0 |
| eval_urgency_sentiment | binary F1 % | 66.7 | 80.0 | 0.0 | 80.0 |
| eval_urgency_sentiment | binary AUROC | 0.417 | 0.917 | 0.417 | 0.917 |
| eval_urgency_sentiment | binary ECE | 0.421 | 0.205 | 0.101 | 0.220 |
| eval_urgency_sentiment | multiclass acc % | 30.0 | 40.0 | 30.0 | 40.0 |
| eval_urgency_sentiment | multiclass macro-F1 % | 21.2 | 23.0 | 21.2 | 23.0 |
| eval_urgency_sentiment | multiclass ECE | 0.334 | 0.250 | 0.317 | 0.248 |
| eval_urgency_sentiment | multilabel exact % | 0.0 | 0.0 | 0.0 | 0.0 |
| eval_urgency_sentiment | multilabel micro-F1 % | 66.7 | 83.3 | 66.7 | 83.3 |
| eval_urgency_sentiment | multilabel label AUROC | 0.680 | 0.920 | 0.680 | 0.920 |
| eval_urgency_sentiment | multilabel ECE | 0.477 | 0.160 | 0.262 | 0.161 |
| heldout_boolq | question acc % | 59.3 | 70.3 | 57.7 | 71.3 |
| heldout_boolq | binary acc % | 59.3 | 70.3 | 57.7 | 71.3 |
| heldout_boolq | binary F1 % | 70.7 | 73.7 | 60.7 | 74.4 |
| heldout_boolq | binary AUROC | 0.631 | 0.768 | 0.631 | 0.768 |
| heldout_boolq | binary ECE | 0.320 | 0.103 | 0.066 | 0.093 |
| heldout_emotion_multiclass | question acc % | 51.0 | 56.0 | 51.0 | 56.0 |
| heldout_emotion_multiclass | multiclass acc % | 51.0 | 56.0 | 51.0 | 56.0 |
| heldout_emotion_multiclass | multiclass macro-F1 % | 41.2 | 47.3 | 41.2 | 47.3 |
| heldout_emotion_multiclass | multiclass ECE | 0.073 | 0.063 | 0.107 | 0.053 |
| heldout_intent_clinc | question acc % | 92.3 | 89.3 | 92.3 | 89.3 |
| heldout_intent_clinc | multiclass acc % | 92.3 | 89.3 | 92.3 | 89.3 |
| heldout_intent_clinc | multiclass macro-F1 % | 94.9 | 90.8 | 94.9 | 90.8 |
| heldout_intent_clinc | multiclass ECE | 0.054 | 0.034 | 0.085 | 0.083 |
| heldout_question_type_trec | question acc % | 64.3 | 68.0 | 64.3 | 68.0 |
| heldout_question_type_trec | multiclass acc % | 64.3 | 68.0 | 64.3 | 68.0 |
| heldout_question_type_trec | multiclass macro-F1 % | 56.0 | 68.1 | 56.0 | 68.1 |
| heldout_question_type_trec | multiclass ECE | 0.093 | 0.066 | 0.100 | 0.073 |
| heldout_sentiment_sst2 | question acc % | 50.0 | 76.7 | 50.0 | 76.0 |
| heldout_sentiment_sst2 | binary acc % | 50.0 | 76.7 | 50.0 | 76.0 |
| heldout_sentiment_sst2 | binary F1 % | 0.0 | 69.8 | 0.0 | 68.7 |
| heldout_sentiment_sst2 | binary AUROC | 0.544 | 0.935 | 0.544 | 0.935 |
| heldout_sentiment_sst2 | binary ECE | 0.471 | 0.189 | 0.050 | 0.181 |
| heldout_topic_dbpedia | question acc % | 89.3 | 91.7 | 89.3 | 91.7 |
| heldout_topic_dbpedia | multiclass acc % | 89.3 | 91.7 | 89.3 | 91.7 |
| heldout_topic_dbpedia | multiclass macro-F1 % | 88.4 | 91.5 | 88.4 | 91.5 |
| heldout_topic_dbpedia | multiclass ECE | 0.050 | 0.040 | 0.054 | 0.078 |
| hf_emotions_multilabel | question acc % | 0.0 | 32.3 | 4.7 | 34.0 |
| hf_emotions_multilabel | multilabel exact % | 0.0 | 32.3 | 4.7 | 34.0 |
| hf_emotions_multilabel | multilabel micro-F1 % | 0.6 | 60.1 | 38.2 | 63.7 |
| hf_emotions_multilabel | multilabel label AUROC | 0.661 | 0.882 | 0.661 | 0.882 |
| hf_emotions_multilabel | multilabel ECE | 0.189 | 0.041 | 0.026 | 0.044 |
| hf_intent_banking77 | question acc % | 89.3 | 92.7 | 89.3 | 92.7 |
| hf_intent_banking77 | multiclass acc % | 89.3 | 92.7 | 89.3 | 92.7 |
| hf_intent_banking77 | multiclass macro-F1 % | 88.5 | 90.3 | 88.5 | 90.3 |
| hf_intent_banking77 | multiclass ECE | 0.011 | 0.027 | 0.040 | 0.031 |
| hf_nli | question acc % | 56.7 | 89.0 | 71.0 | 89.0 |
| hf_nli | binary acc % | 56.7 | 89.0 | 71.0 | 89.0 |
| hf_nli | binary F1 % | 60.8 | 85.5 | 66.1 | 85.5 |
| hf_nli | binary AUROC | 0.804 | 0.946 | 0.804 | 0.946 |
| hf_nli | binary ECE | 0.394 | 0.040 | 0.166 | 0.050 |
| hf_sentiment_tweets | question acc % | 54.3 | 66.7 | 54.3 | 66.7 |
| hf_sentiment_tweets | multiclass acc % | 54.3 | 66.7 | 54.3 | 66.7 |
| hf_sentiment_tweets | multiclass macro-F1 % | 55.1 | 66.6 | 55.1 | 66.6 |
| hf_sentiment_tweets | multiclass ECE | 0.075 | 0.058 | 0.107 | 0.062 |
| hf_topic_agnews | question acc % | 77.3 | 86.7 | 77.3 | 86.7 |
| hf_topic_agnews | multiclass acc % | 77.3 | 86.7 | 77.3 | 86.7 |
| hf_topic_agnews | multiclass macro-F1 % | 76.4 | 86.8 | 76.4 | 86.8 |
| hf_topic_agnews | multiclass ECE | 0.117 | 0.063 | 0.091 | 0.036 |

## Question accuracy % by hard-case tag

| tag | n | baseline | lora | baseline+cal | lora+cal |
|---|---|---|---|---|---|
| (none) | 3042 | 64.3 | 74.2 | 63.9 | 74.4 |
| contradiction | 107 | 30.8 | 90.7 | 64.5 | 90.7 |
| distractor | 33 | 21.2 | 45.5 | 21.2 | 45.5 |
| double_negation | 6 | 33.3 | 33.3 | 0.0 | 33.3 |
| evidence_end | 13 | 38.5 | 46.2 | 38.5 | 46.2 |
| evidence_middle | 11 | 45.5 | 54.5 | 27.3 | 54.5 |
| evidence_start | 9 | 55.6 | 77.8 | 44.4 | 77.8 |
| exception | 7 | 0.0 | 0.0 | 0.0 | 0.0 |
| hypothetical | 7 | 57.1 | 57.1 | 57.1 | 42.9 |
| injection | 10 | 60.0 | 50.0 | 50.0 | 50.0 |
| lexical_overlap | 20 | 40.0 | 55.0 | 40.0 | 55.0 |
| long_state | 50 | 36.0 | 46.0 | 34.0 | 46.0 |
| missing_evidence | 104 | 37.5 | 81.7 | 65.4 | 81.7 |
| multi_positive | 81 | 1.2 | 18.5 | 6.2 | 21.0 |
| multi_turn | 9 | 33.3 | 77.8 | 33.3 | 88.9 |
| negation | 30 | 33.3 | 56.7 | 33.3 | 53.3 |
| new_label_names | 3 | 0.0 | 100.0 | 0.0 | 100.0 |
| nota | 46 | 87.0 | 89.1 | 87.0 | 89.1 |
| numeric_reasoning | 16 | 37.5 | 37.5 | 50.0 | 31.2 |
| paraphrase | 22 | 18.2 | 50.0 | 18.2 | 50.0 |
| role_reversal | 15 | 40.0 | 46.7 | 40.0 | 46.7 |
| sarcasm | 12 | 8.3 | 33.3 | 25.0 | 33.3 |
| temporal_reasoning | 29 | 31.0 | 37.9 | 27.6 | 41.4 |
| zero_positive | 6 | 33.3 | 33.3 | 0.0 | 33.3 |
