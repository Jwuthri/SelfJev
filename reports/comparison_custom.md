# Comparison: base vs stock-LoRA vs custom vs custom-distill-LoRA vs custom-sim vs custom-sim-LoRA

| | base | stock-LoRA | custom | custom-distill-LoRA | custom-sim | custom-sim-LoRA |
|---|---|---|---|---|---|---|
| adapter | None | runs/lora_pilot/adapter | runs/custom_frozen/checkpoint | runs/custom_distill_lora/checkpoint | runs/custom_sim_frozen/checkpoint | runs/custom_sim_lora/checkpoint |
| calibration | no | no | no | no | no | no |
| prompt | task-v1 (f7b8d8022dfb) | task-v1 (f7b8d8022dfb) | custom-v1 (b96b6174a187) | custom-v1 (b96b6174a187) | custom-v1 (b96b6174a187) | custom-v1 (b96b6174a187) |
| n | 3471 | 3471 | 3471 | 3471 | 3471 | 3471 |

| slice | metric | base | stock-LoRA | custom | custom-distill-LoRA | custom-sim | custom-sim-LoRA |
|---|---|---|---|---|---|---|---|
| overall | question acc % | 61.0 | 73.5 | 39.0 | 39.7 | 48.0 | 58.2 |
| overall | binary acc % | 55.3 | 77.8 | 51.9 | 51.3 | 51.4 | 51.7 |
| overall | binary F1 % | 55.8 | 75.1 | 4.8 | 6.3 | 8.1 | 6.7 |
| overall | binary AUROC | 0.605 | 0.863 | 0.536 | 0.451 | 0.524 | 0.514 |
| overall | binary ECE | 0.384 | 0.066 | 0.148 | 0.189 | 0.141 | 0.141 |
| overall | multiclass acc % | 73.3 | 78.3 | 39.1 | 40.6 | 53.9 | 70.2 |
| overall | multiclass macro-F1 % | 79.6 | 82.3 | 24.9 | 23.8 | 54.3 | 76.1 |
| overall | multiclass ECE | 0.026 | 0.027 | 0.112 | 0.205 | 0.033 | 0.030 |
| overall | multilabel exact % | 1.2 | 31.1 | 1.2 | 0.9 | 1.5 | 1.7 |
| overall | multilabel micro-F1 % | 23.6 | 62.9 | 12.5 | 10.0 | 8.6 | 6.8 |
| overall | multilabel label AUROC | 0.679 | 0.882 | 0.565 | 0.501 | 0.544 | 0.686 |
| overall | multilabel ECE | 0.203 | 0.052 | 0.041 | 0.060 | 0.026 | 0.046 |
| overall | binary brier | 0.397 | 0.155 | 0.274 | 0.294 | 0.274 | 0.274 |
| overall | binary log_loss | 1.747 | 0.480 | 0.748 | 0.799 | 0.751 | 0.747 |
| overall | multiclass brier | 0.363 | 0.301 | 0.726 | 0.755 | 0.590 | 0.392 |
| overall | multiclass log_loss | 0.717 | 0.601 | 1.544 | 1.702 | 1.175 | 0.797 |
| overall | multilabel brier | 0.208 | 0.113 | 0.169 | 0.170 | 0.168 | 0.161 |
| overall | multilabel log_loss | 1.106 | 0.359 | 0.520 | 0.524 | 0.518 | 0.495 |
| eval_adversarial | question acc % | 74.1 | 63.0 | 44.4 | 37.0 | 51.9 | 59.3 |
| eval_adversarial | binary acc % | 73.3 | 66.7 | 60.0 | 46.7 | 60.0 | 66.7 |
| eval_adversarial | binary F1 % | 75.0 | 66.7 | 25.0 | 33.3 | 0.0 | 54.5 |
| eval_adversarial | binary AUROC | 0.741 | 0.796 | 0.537 | 0.426 | 0.648 | 0.630 |
| eval_adversarial | binary ECE | 0.351 | 0.276 | 0.045 | 0.103 | 0.060 | 0.143 |
| eval_adversarial | multiclass acc % | 100.0 | 85.7 | 14.3 | 28.6 | 57.1 | 71.4 |
| eval_adversarial | multiclass macro-F1 % | 100.0 | 77.8 | 10.0 | 16.7 | 40.7 | 52.4 |
| eval_adversarial | multiclass ECE | 0.255 | 0.127 | 0.580 | 0.459 | 0.367 | 0.370 |
| eval_adversarial | multilabel exact % | 40.0 | 20.0 | 40.0 | 20.0 | 20.0 | 20.0 |
| eval_adversarial | multilabel micro-F1 % | 75.0 | 72.7 | 50.0 | 20.0 | 0.0 | 20.0 |
| eval_adversarial | multilabel label AUROC | 0.881 | 0.833 | 0.778 | 0.603 | 0.865 | 0.667 |
| eval_adversarial | multilabel ECE | 0.251 | 0.256 | 0.223 | 0.107 | 0.067 | 0.133 |
| eval_agent_output | question acc % | 30.8 | 46.2 | 26.9 | 30.8 | 34.6 | 34.6 |
| eval_agent_output | binary acc % | 42.9 | 57.1 | 35.7 | 50.0 | 50.0 | 42.9 |
| eval_agent_output | binary F1 % | 33.3 | 57.1 | 0.0 | 22.2 | 46.2 | 33.3 |
| eval_agent_output | binary AUROC | 0.510 | 0.592 | 0.592 | 0.571 | 0.449 | 0.551 |
| eval_agent_output | binary ECE | 0.454 | 0.355 | 0.182 | 0.062 | 0.013 | 0.094 |
| eval_agent_output | multiclass acc % | 14.3 | 57.1 | 14.3 | 0.0 | 14.3 | 42.9 |
| eval_agent_output | multiclass macro-F1 % | 11.1 | 38.1 | 7.4 | 0.0 | 7.4 | 33.3 |
| eval_agent_output | multiclass ECE | 0.493 | 0.438 | 0.387 | 0.497 | 0.693 | 0.277 |
| eval_agent_output | multilabel exact % | 20.0 | 0.0 | 20.0 | 20.0 | 20.0 | 0.0 |
| eval_agent_output | multilabel micro-F1 % | 57.1 | 66.7 | 0.0 | 0.0 | 33.3 | 0.0 |
| eval_agent_output | multilabel label AUROC | 0.644 | 0.779 | 0.510 | 0.346 | 0.327 | 0.337 |
| eval_agent_output | multilabel ECE | 0.286 | 0.239 | 0.095 | 0.098 | 0.117 | 0.095 |
| eval_evidence | question acc % | 41.2 | 82.4 | 58.8 | 41.2 | 52.9 | 41.2 |
| eval_evidence | binary acc % | 46.7 | 93.3 | 66.7 | 46.7 | 53.3 | 46.7 |
| eval_evidence | binary F1 % | 55.6 | 90.9 | 28.6 | 33.3 | 53.3 | 33.3 |
| eval_evidence | binary AUROC | 0.820 | 0.980 | 0.460 | 0.520 | 0.760 | 0.520 |
| eval_evidence | binary ECE | 0.526 | 0.147 | 0.139 | 0.129 | 0.153 | 0.185 |
| eval_evidence | multilabel exact % | 0.0 | 0.0 | 0.0 | 0.0 | 50.0 | 0.0 |
| eval_evidence | multilabel micro-F1 % | 54.5 | 40.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| eval_evidence | multilabel label AUROC | 0.625 | 0.667 | 0.375 | 0.167 | 0.125 | 0.083 |
| eval_evidence | multilabel ECE | 0.467 | 0.464 | 0.206 | 0.351 | 0.282 | 0.297 |
| eval_multilabel | question acc % | 12.5 | 34.4 | 12.5 | 15.6 | 15.6 | 18.8 |
| eval_multilabel | binary acc % | 57.1 | 57.1 | 42.9 | 57.1 | 57.1 | 28.6 |
| eval_multilabel | binary F1 % | 66.7 | 57.1 | 33.3 | 40.0 | 57.1 | 28.6 |
| eval_multilabel | binary AUROC | 0.750 | 0.750 | 0.500 | 0.667 | 0.667 | 0.250 |
| eval_multilabel | binary ECE | 0.486 | 0.345 | 0.101 | 0.065 | 0.232 | 0.225 |
| eval_multilabel | multiclass acc % | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| eval_multilabel | multiclass macro-F1 % | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| eval_multilabel | multiclass ECE | 0.434 | 0.496 | 0.253 | 0.280 | 0.312 | 0.717 |
| eval_multilabel | multilabel exact % | 0.0 | 29.2 | 4.2 | 4.2 | 4.2 | 16.7 |
| eval_multilabel | multilabel micro-F1 % | 55.1 | 75.9 | 40.4 | 36.7 | 32.9 | 41.7 |
| eval_multilabel | multilabel label AUROC | 0.660 | 0.888 | 0.572 | 0.534 | 0.563 | 0.634 |
| eval_multilabel | multilabel ECE | 0.358 | 0.138 | 0.117 | 0.126 | 0.111 | 0.165 |
| eval_policy | question acc % | 31.8 | 40.9 | 40.9 | 45.5 | 36.4 | 40.9 |
| eval_policy | binary acc % | 46.2 | 46.2 | 61.5 | 61.5 | 46.2 | 46.2 |
| eval_policy | binary F1 % | 63.2 | 46.2 | 61.5 | 66.7 | 22.2 | 22.2 |
| eval_policy | binary AUROC | 0.548 | 0.429 | 0.571 | 0.714 | 0.548 | 0.452 |
| eval_policy | binary ECE | 0.536 | 0.500 | 0.107 | 0.100 | 0.056 | 0.053 |
| eval_policy | multiclass acc % | 20.0 | 40.0 | 20.0 | 40.0 | 20.0 | 40.0 |
| eval_policy | multiclass macro-F1 % | 12.5 | 23.8 | 8.3 | 23.8 | 12.5 | 23.8 |
| eval_policy | multiclass ECE | 0.241 | 0.521 | 0.262 | 0.369 | 0.465 | 0.231 |
| eval_policy | multilabel exact % | 0.0 | 25.0 | 0.0 | 0.0 | 25.0 | 25.0 |
| eval_policy | multilabel micro-F1 % | 69.6 | 66.7 | 69.6 | 55.6 | 62.5 | 0.0 |
| eval_policy | multilabel label AUROC | 0.464 | 0.732 | 0.482 | 0.286 | 0.536 | 0.464 |
| eval_policy | multilabel ECE | 0.465 | 0.386 | 0.027 | 0.055 | 0.085 | 0.115 |
| eval_routing | question acc % | 48.0 | 76.0 | 48.0 | 44.0 | 40.0 | 56.0 |
| eval_routing | binary acc % | 60.0 | 80.0 | 80.0 | 70.0 | 50.0 | 70.0 |
| eval_routing | binary F1 % | 66.7 | 75.0 | 66.7 | 57.1 | 0.0 | 57.1 |
| eval_routing | binary AUROC | 0.875 | 0.917 | 0.792 | 0.625 | 0.792 | 0.875 |
| eval_routing | binary ECE | 0.382 | 0.189 | 0.233 | 0.179 | 0.283 | 0.168 |
| eval_routing | multiclass acc % | 38.5 | 76.9 | 30.8 | 30.8 | 38.5 | 53.8 |
| eval_routing | multiclass macro-F1 % | 23.1 | 66.7 | 17.6 | 16.7 | 23.8 | 36.7 |
| eval_routing | multiclass ECE | 0.284 | 0.162 | 0.425 | 0.458 | 0.461 | 0.295 |
| eval_routing | multilabel exact % | 50.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| eval_routing | multilabel micro-F1 % | 50.0 | 80.0 | 0.0 | 40.0 | 0.0 | 0.0 |
| eval_routing | multilabel label AUROC | 0.667 | 1.000 | 0.556 | 0.833 | 0.722 | 0.444 |
| eval_routing | multilabel ECE | 0.209 | 0.114 | 0.148 | 0.148 | 0.137 | 0.137 |
| eval_urgency_sentiment | question acc % | 40.9 | 54.5 | 36.4 | 40.9 | 45.5 | 50.0 |
| eval_urgency_sentiment | binary acc % | 60.0 | 80.0 | 40.0 | 30.0 | 50.0 | 50.0 |
| eval_urgency_sentiment | binary F1 % | 66.7 | 80.0 | 0.0 | 36.4 | 28.6 | 44.4 |
| eval_urgency_sentiment | binary AUROC | 0.417 | 0.917 | 0.333 | 0.417 | 0.375 | 0.500 |
| eval_urgency_sentiment | binary ECE | 0.421 | 0.205 | 0.159 | 0.241 | 0.126 | 0.147 |
| eval_urgency_sentiment | multiclass acc % | 30.0 | 40.0 | 40.0 | 60.0 | 50.0 | 60.0 |
| eval_urgency_sentiment | multiclass macro-F1 % | 21.2 | 23.0 | 36.2 | 50.0 | 52.1 | 56.2 |
| eval_urgency_sentiment | multiclass ECE | 0.334 | 0.250 | 0.279 | 0.337 | 0.312 | 0.448 |
| eval_urgency_sentiment | multilabel exact % | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| eval_urgency_sentiment | multilabel micro-F1 % | 66.7 | 83.3 | 0.0 | 0.0 | 0.0 | 0.0 |
| eval_urgency_sentiment | multilabel label AUROC | 0.680 | 0.920 | 0.960 | 0.920 | 0.720 | 0.600 |
| eval_urgency_sentiment | multilabel ECE | 0.477 | 0.160 | 0.043 | 0.242 | 0.050 | 0.143 |
| heldout_boolq | question acc % | 59.3 | 70.3 | 41.0 | 40.0 | 40.3 | 41.0 |
| heldout_boolq | binary acc % | 59.3 | 70.3 | 41.0 | 40.0 | 40.3 | 41.0 |
| heldout_boolq | binary F1 % | 70.7 | 73.7 | 3.3 | 0.0 | 7.3 | 2.2 |
| heldout_boolq | binary AUROC | 0.631 | 0.768 | 0.518 | 0.524 | 0.528 | 0.549 |
| heldout_boolq | binary ECE | 0.320 | 0.103 | 0.206 | 0.292 | 0.173 | 0.246 |
| heldout_emotion_multiclass | question acc % | 51.0 | 56.0 | 15.0 | 13.3 | 27.0 | 45.3 |
| heldout_emotion_multiclass | multiclass acc % | 51.0 | 56.0 | 15.0 | 13.3 | 27.0 | 45.3 |
| heldout_emotion_multiclass | multiclass macro-F1 % | 41.2 | 47.3 | 8.1 | 10.5 | 21.6 | 37.7 |
| heldout_emotion_multiclass | multiclass ECE | 0.073 | 0.063 | 0.102 | 0.206 | 0.052 | 0.092 |
| heldout_intent_clinc | question acc % | 92.3 | 89.3 | 20.7 | 20.0 | 61.0 | 79.3 |
| heldout_intent_clinc | multiclass acc % | 92.3 | 89.3 | 20.7 | 20.0 | 61.0 | 79.3 |
| heldout_intent_clinc | multiclass macro-F1 % | 94.9 | 90.8 | 13.2 | 10.9 | 56.2 | 80.2 |
| heldout_intent_clinc | multiclass ECE | 0.054 | 0.034 | 0.142 | 0.294 | 0.088 | 0.086 |
| heldout_question_type_trec | question acc % | 64.3 | 68.0 | 27.3 | 26.7 | 31.0 | 43.3 |
| heldout_question_type_trec | multiclass acc % | 64.3 | 68.0 | 27.3 | 26.7 | 31.0 | 43.3 |
| heldout_question_type_trec | multiclass macro-F1 % | 56.0 | 68.1 | 13.0 | 7.0 | 25.9 | 41.0 |
| heldout_question_type_trec | multiclass ECE | 0.093 | 0.066 | 0.145 | 0.488 | 0.164 | 0.070 |
| heldout_sentiment_sst2 | question acc % | 50.0 | 76.7 | 50.0 | 50.0 | 50.0 | 50.0 |
| heldout_sentiment_sst2 | binary acc % | 50.0 | 76.7 | 50.0 | 50.0 | 50.0 | 50.0 |
| heldout_sentiment_sst2 | binary F1 % | 0.0 | 69.8 | 0.0 | 0.0 | 0.0 | 0.0 |
| heldout_sentiment_sst2 | binary AUROC | 0.544 | 0.935 | 0.476 | 0.198 | 0.479 | 0.453 |
| heldout_sentiment_sst2 | binary ECE | 0.471 | 0.189 | 0.239 | 0.279 | 0.275 | 0.212 |
| heldout_topic_dbpedia | question acc % | 89.3 | 91.7 | 25.7 | 30.7 | 58.0 | 81.7 |
| heldout_topic_dbpedia | multiclass acc % | 89.3 | 91.7 | 25.7 | 30.7 | 58.0 | 81.7 |
| heldout_topic_dbpedia | multiclass macro-F1 % | 88.4 | 91.5 | 20.0 | 24.0 | 56.4 | 81.5 |
| heldout_topic_dbpedia | multiclass ECE | 0.050 | 0.040 | 0.298 | 0.300 | 0.077 | 0.142 |
| hf_emotions_multilabel | question acc % | 0.0 | 32.3 | 0.0 | 0.0 | 0.0 | 0.0 |
| hf_emotions_multilabel | multilabel exact % | 0.0 | 32.3 | 0.0 | 0.0 | 0.0 | 0.0 |
| hf_emotions_multilabel | multilabel micro-F1 % | 0.6 | 60.1 | 0.0 | 0.0 | 0.0 | 0.0 |
| hf_emotions_multilabel | multilabel label AUROC | 0.661 | 0.882 | 0.514 | 0.430 | 0.487 | 0.680 |
| hf_emotions_multilabel | multilabel ECE | 0.189 | 0.041 | 0.033 | 0.056 | 0.018 | 0.039 |
| hf_intent_banking77 | question acc % | 89.3 | 92.7 | 57.7 | 54.3 | 76.0 | 93.0 |
| hf_intent_banking77 | multiclass acc % | 89.3 | 92.7 | 57.7 | 54.3 | 76.0 | 93.0 |
| hf_intent_banking77 | multiclass macro-F1 % | 88.5 | 90.3 | 51.6 | 46.8 | 72.0 | 93.3 |
| hf_intent_banking77 | multiclass ECE | 0.011 | 0.027 | 0.040 | 0.049 | 0.191 | 0.053 |
| hf_nli | question acc % | 56.7 | 89.0 | 63.7 | 64.0 | 63.7 | 64.3 |
| hf_nli | binary acc % | 56.7 | 89.0 | 63.7 | 64.0 | 63.7 | 64.3 |
| hf_nli | binary F1 % | 60.8 | 85.5 | 0.0 | 1.8 | 5.2 | 3.6 |
| hf_nli | binary AUROC | 0.804 | 0.946 | 0.532 | 0.540 | 0.541 | 0.536 |
| hf_nli | binary ECE | 0.394 | 0.040 | 0.050 | 0.061 | 0.041 | 0.071 |
| hf_sentiment_tweets | question acc % | 54.3 | 66.7 | 41.7 | 52.3 | 45.3 | 62.3 |
| hf_sentiment_tweets | multiclass acc % | 54.3 | 66.7 | 41.7 | 52.3 | 45.3 | 62.3 |
| hf_sentiment_tweets | multiclass macro-F1 % | 55.1 | 66.6 | 29.6 | 43.3 | 31.6 | 62.5 |
| hf_sentiment_tweets | multiclass ECE | 0.075 | 0.058 | 0.080 | 0.055 | 0.129 | 0.087 |
| hf_topic_agnews | question acc % | 77.3 | 86.7 | 87.7 | 88.0 | 81.7 | 89.0 |
| hf_topic_agnews | multiclass acc % | 77.3 | 86.7 | 87.7 | 88.0 | 81.7 | 89.0 |
| hf_topic_agnews | multiclass macro-F1 % | 76.4 | 86.8 | 87.5 | 88.1 | 81.7 | 89.1 |
| hf_topic_agnews | multiclass ECE | 0.117 | 0.063 | 0.048 | 0.066 | 0.088 | 0.045 |

## Question accuracy % by hard-case tag

| tag | n | base | stock-LoRA | custom | custom-distill-LoRA | custom-sim | custom-sim-LoRA |
|---|---|---|---|---|---|---|---|
| (none) | 3042 | 64.3 | 74.2 | 35.7 | 36.5 | 45.7 | 58.1 |
| contradiction | 107 | 30.8 | 90.7 | 95.3 | 91.6 | 91.6 | 92.5 |
| distractor | 33 | 21.2 | 45.5 | 30.3 | 18.2 | 21.2 | 24.2 |
| double_negation | 6 | 33.3 | 33.3 | 66.7 | 33.3 | 50.0 | 50.0 |
| evidence_end | 13 | 38.5 | 46.2 | 23.1 | 15.4 | 23.1 | 15.4 |
| evidence_middle | 11 | 45.5 | 54.5 | 18.2 | 36.4 | 9.1 | 36.4 |
| evidence_start | 9 | 55.6 | 77.8 | 44.4 | 33.3 | 44.4 | 55.6 |
| exception | 7 | 0.0 | 0.0 | 42.9 | 0.0 | 14.3 | 28.6 |
| hypothetical | 7 | 57.1 | 57.1 | 42.9 | 42.9 | 57.1 | 42.9 |
| injection | 10 | 60.0 | 50.0 | 60.0 | 60.0 | 60.0 | 60.0 |
| lexical_overlap | 20 | 40.0 | 55.0 | 40.0 | 50.0 | 45.0 | 55.0 |
| long_state | 50 | 36.0 | 46.0 | 36.0 | 24.0 | 22.0 | 34.0 |
| missing_evidence | 104 | 37.5 | 81.7 | 98.1 | 98.1 | 95.2 | 97.1 |
| multi_positive | 81 | 1.2 | 18.5 | 1.2 | 0.0 | 1.2 | 2.5 |
| multi_turn | 9 | 33.3 | 77.8 | 33.3 | 55.6 | 33.3 | 33.3 |
| negation | 30 | 33.3 | 56.7 | 36.7 | 30.0 | 36.7 | 40.0 |
| new_label_names | 3 | 0.0 | 100.0 | 66.7 | 33.3 | 66.7 | 33.3 |
| nota | 46 | 87.0 | 89.1 | 43.5 | 52.2 | 80.4 | 2.2 |
| numeric_reasoning | 16 | 37.5 | 37.5 | 68.8 | 37.5 | 37.5 | 50.0 |
| paraphrase | 22 | 18.2 | 50.0 | 18.2 | 18.2 | 22.7 | 31.8 |
| role_reversal | 15 | 40.0 | 46.7 | 46.7 | 40.0 | 60.0 | 66.7 |
| sarcasm | 12 | 8.3 | 33.3 | 25.0 | 33.3 | 25.0 | 25.0 |
| temporal_reasoning | 29 | 31.0 | 37.9 | 41.4 | 34.5 | 24.1 | 27.6 |
| zero_positive | 6 | 33.3 | 33.3 | 50.0 | 50.0 | 66.7 | 66.7 |
