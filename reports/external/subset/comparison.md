# Comparison: base vs LoRA vs ~typesafe/jev-latest vs openai/gpt-6-astra

| | base | LoRA | ~typesafe/jev-latest | openai/gpt-6-astra |
|---|---|---|---|---|
| adapter | None | None | None | None |
| calibration | no | no | no | no |
| prompt | ours-base (-) | ours-LoRA (-) | ~typesafe/jev-latest (-) | openai/gpt-6-astra (-) |
| n | 501 | 501 | 501 | 501 |

| slice | metric | base | LoRA | ~typesafe/jev-latest | openai/gpt-6-astra |
|---|---|---|---|---|---|
| overall | question acc % | 56.3 | 69.9 | 85.6 | 90.2 |
| overall | binary acc % | 54.6 | 73.0 | 92.0 | 94.3 |
| overall | binary F1 % | 60.7 | 72.2 | 91.9 | 93.9 |
| overall | binary AUROC | 0.601 | 0.816 | 0.978 | 0.974 |
| overall | binary ECE | 0.411 | 0.125 | 0.056 | 0.056 |
| overall | multiclass acc % | 72.3 | 78.7 | 85.4 | 89.7 |
| overall | multiclass macro-F1 % | 62.0 | 69.8 | 82.8 | 93.1 |
| overall | multiclass ECE | 0.079 | 0.035 | 0.096 | 0.079 |
| overall | multilabel exact % | 5.4 | 32.4 | 71.6 | 82.4 |
| overall | multilabel micro-F1 % | 51.7 | 71.4 | 87.6 | 92.1 |
| overall | multilabel label AUROC | 0.713 | 0.888 | 0.974 | 0.993 |
| overall | multilabel ECE | 0.264 | 0.099 | 0.052 | 0.028 |
| overall | binary brier | 0.412 | 0.179 | 0.056 | 0.055 |
| overall | binary log_loss | 1.929 | 0.549 | 0.198 | 0.576 |
| overall | multiclass brier | 0.411 | 0.315 | 0.236 | 0.180 |
| overall | multiclass log_loss | 0.830 | 0.628 | 1.652 | 0.499 |
| overall | multilabel brier | 0.273 | 0.137 | 0.054 | 0.035 |
| overall | multilabel log_loss | 1.177 | 0.444 | 0.193 | 0.114 |
| eval_adversarial | question acc % | 74.1 | 63.0 | 100.0 | 100.0 |
| eval_adversarial | binary acc % | 73.3 | 66.7 | 100.0 | 100.0 |
| eval_adversarial | binary F1 % | 75.0 | 66.7 | 100.0 | 100.0 |
| eval_adversarial | binary AUROC | 0.741 | 0.796 | 1.000 | 1.000 |
| eval_adversarial | binary ECE | 0.351 | 0.276 | 0.048 | 0.001 |
| eval_adversarial | multiclass acc % | 100.0 | 85.7 | 100.0 | 100.0 |
| eval_adversarial | multiclass macro-F1 % | 100.0 | 77.8 | 100.0 | 100.0 |
| eval_adversarial | multiclass ECE | 0.255 | 0.127 | 0.027 | 0.000 |
| eval_adversarial | multilabel exact % | 40.0 | 20.0 | 100.0 | 100.0 |
| eval_adversarial | multilabel micro-F1 % | 75.0 | 72.7 | 100.0 | 100.0 |
| eval_adversarial | multilabel label AUROC | 0.881 | 0.833 | 1.000 | 1.000 |
| eval_adversarial | multilabel ECE | 0.251 | 0.256 | 0.036 | 0.000 |
| eval_agent_output | question acc % | 30.8 | 46.2 | 92.3 | 100.0 |
| eval_agent_output | binary acc % | 42.9 | 57.1 | 100.0 | 100.0 |
| eval_agent_output | binary F1 % | 33.3 | 57.1 | 100.0 | 100.0 |
| eval_agent_output | binary AUROC | 0.510 | 0.592 | 1.000 | 1.000 |
| eval_agent_output | binary ECE | 0.454 | 0.355 | 0.045 | 0.000 |
| eval_agent_output | multiclass acc % | 14.3 | 57.1 | 85.7 | 100.0 |
| eval_agent_output | multiclass macro-F1 % | 11.1 | 38.1 | 76.0 | 100.0 |
| eval_agent_output | multiclass ECE | 0.493 | 0.438 | 0.089 | 0.000 |
| eval_agent_output | multilabel exact % | 20.0 | 0.0 | 80.0 | 100.0 |
| eval_agent_output | multilabel micro-F1 % | 57.1 | 66.7 | 94.1 | 100.0 |
| eval_agent_output | multilabel label AUROC | 0.644 | 0.779 | 1.000 | 1.000 |
| eval_agent_output | multilabel ECE | 0.286 | 0.239 | 0.094 | 0.000 |
| eval_evidence | question acc % | 41.2 | 82.4 | 100.0 | 100.0 |
| eval_evidence | binary acc % | 46.7 | 93.3 | 100.0 | 100.0 |
| eval_evidence | binary F1 % | 55.6 | 90.9 | 100.0 | 100.0 |
| eval_evidence | binary AUROC | 0.820 | 0.980 | 1.000 | 1.000 |
| eval_evidence | binary ECE | 0.526 | 0.147 | 0.047 | 0.000 |
| eval_evidence | multilabel exact % | 0.0 | 0.0 | 100.0 | 100.0 |
| eval_evidence | multilabel micro-F1 % | 54.5 | 40.0 | 100.0 | 100.0 |
| eval_evidence | multilabel label AUROC | 0.625 | 0.667 | 1.000 | 1.000 |
| eval_evidence | multilabel ECE | 0.467 | 0.464 | 0.048 | 0.000 |
| eval_multilabel | question acc % | 12.5 | 34.4 | 100.0 | 100.0 |
| eval_multilabel | binary acc % | 57.1 | 57.1 | 100.0 | 100.0 |
| eval_multilabel | binary F1 % | 66.7 | 57.1 | 100.0 | 100.0 |
| eval_multilabel | binary AUROC | 0.750 | 0.750 | 1.000 | 1.000 |
| eval_multilabel | binary ECE | 0.486 | 0.345 | 0.084 | 0.000 |
| eval_multilabel | multiclass acc % | 0.0 | 0.0 | 100.0 | 100.0 |
| eval_multilabel | multiclass macro-F1 % | 0.0 | 0.0 | 100.0 | 100.0 |
| eval_multilabel | multiclass ECE | 0.434 | 0.496 | 0.000 | 0.000 |
| eval_multilabel | multilabel exact % | 0.0 | 29.2 | 100.0 | 100.0 |
| eval_multilabel | multilabel micro-F1 % | 55.1 | 75.9 | 100.0 | 100.0 |
| eval_multilabel | multilabel label AUROC | 0.660 | 0.888 | 1.000 | 1.000 |
| eval_multilabel | multilabel ECE | 0.358 | 0.138 | 0.040 | 0.000 |
| eval_policy | question acc % | 31.8 | 40.9 | 72.7 | 100.0 |
| eval_policy | binary acc % | 46.2 | 46.2 | 76.9 | 100.0 |
| eval_policy | binary F1 % | 63.2 | 46.2 | 76.9 | 100.0 |
| eval_policy | binary AUROC | 0.548 | 0.429 | 0.857 | 1.000 |
| eval_policy | binary ECE | 0.536 | 0.500 | 0.316 | 0.000 |
| eval_policy | multiclass acc % | 20.0 | 40.0 | 40.0 | 100.0 |
| eval_policy | multiclass macro-F1 % | 12.5 | 23.8 | 25.0 | 100.0 |
| eval_policy | multiclass ECE | 0.241 | 0.521 | 0.458 | 0.000 |
| eval_policy | multilabel exact % | 0.0 | 25.0 | 100.0 | 100.0 |
| eval_policy | multilabel micro-F1 % | 69.6 | 66.7 | 100.0 | 100.0 |
| eval_policy | multilabel label AUROC | 0.464 | 0.732 | 1.000 | 1.000 |
| eval_policy | multilabel ECE | 0.465 | 0.386 | 0.139 | 0.000 |
| eval_routing | question acc % | 48.0 | 76.0 | 100.0 | 100.0 |
| eval_routing | binary acc % | 60.0 | 80.0 | 100.0 | 100.0 |
| eval_routing | binary F1 % | 66.7 | 75.0 | 100.0 | 100.0 |
| eval_routing | binary AUROC | 0.875 | 0.917 | 1.000 | 1.000 |
| eval_routing | binary ECE | 0.382 | 0.189 | 0.042 | 0.000 |
| eval_routing | multiclass acc % | 38.5 | 76.9 | 100.0 | 100.0 |
| eval_routing | multiclass macro-F1 % | 23.1 | 66.7 | 100.0 | 100.0 |
| eval_routing | multiclass ECE | 0.284 | 0.162 | 0.000 | 0.000 |
| eval_routing | multilabel exact % | 50.0 | 50.0 | 100.0 | 100.0 |
| eval_routing | multilabel micro-F1 % | 50.0 | 80.0 | 100.0 | 100.0 |
| eval_routing | multilabel label AUROC | 0.667 | 1.000 | 1.000 | 1.000 |
| eval_routing | multilabel ECE | 0.209 | 0.114 | 0.093 | 0.000 |
| eval_urgency_sentiment | question acc % | 40.9 | 54.5 | 95.5 | 100.0 |
| eval_urgency_sentiment | binary acc % | 60.0 | 80.0 | 90.0 | 100.0 |
| eval_urgency_sentiment | binary F1 % | 66.7 | 80.0 | 90.9 | 100.0 |
| eval_urgency_sentiment | binary AUROC | 0.417 | 0.917 | 1.000 | 1.000 |
| eval_urgency_sentiment | binary ECE | 0.421 | 0.205 | 0.095 | 0.002 |
| eval_urgency_sentiment | multiclass acc % | 30.0 | 40.0 | 100.0 | 100.0 |
| eval_urgency_sentiment | multiclass macro-F1 % | 21.2 | 23.0 | 100.0 | 100.0 |
| eval_urgency_sentiment | multiclass ECE | 0.334 | 0.250 | 0.004 | 0.001 |
| eval_urgency_sentiment | multilabel exact % | 0.0 | 0.0 | 100.0 | 100.0 |
| eval_urgency_sentiment | multilabel micro-F1 % | 66.7 | 83.3 | 100.0 | 100.0 |
| eval_urgency_sentiment | multilabel label AUROC | 0.680 | 0.920 | 1.000 | 1.000 |
| eval_urgency_sentiment | multilabel ECE | 0.477 | 0.160 | 0.029 | 0.000 |
| heldout_boolq | question acc % | 66.7 | 56.7 | 80.0 | 80.0 |
| heldout_boolq | binary acc % | 66.7 | 56.7 | 80.0 | 80.0 |
| heldout_boolq | binary F1 % | 79.2 | 66.7 | 84.2 | 84.2 |
| heldout_boolq | binary AUROC | 0.651 | 0.713 | 0.921 | 0.828 |
| heldout_boolq | binary ECE | 0.364 | 0.238 | 0.110 | 0.190 |
| heldout_emotion_multiclass | question acc % | 70.0 | 73.3 | 66.7 | 80.0 |
| heldout_emotion_multiclass | multiclass acc % | 70.0 | 73.3 | 66.7 | 80.0 |
| heldout_emotion_multiclass | multiclass macro-F1 % | 55.4 | 61.3 | 51.7 | 77.8 |
| heldout_emotion_multiclass | multiclass ECE | 0.256 | 0.116 | 0.244 | 0.171 |
| heldout_intent_clinc | question acc % | 96.7 | 93.3 | 86.7 | 86.7 |
| heldout_intent_clinc | multiclass acc % | 96.7 | 93.3 | 86.7 | 86.7 |
| heldout_intent_clinc | multiclass macro-F1 % | 95.4 | 91.4 | 83.9 | 86.2 |
| heldout_intent_clinc | multiclass ECE | 0.086 | 0.114 | 0.093 | 0.122 |
| heldout_question_type_trec | question acc % | 73.3 | 80.0 | 100.0 | 100.0 |
| heldout_question_type_trec | multiclass acc % | 73.3 | 80.0 | 100.0 | 100.0 |
| heldout_question_type_trec | multiclass macro-F1 % | 71.5 | 82.1 | 100.0 | 100.0 |
| heldout_question_type_trec | multiclass ECE | 0.184 | 0.202 | 0.012 | 0.001 |
| heldout_sentiment_sst2 | question acc % | 46.7 | 83.3 | 100.0 | 96.7 |
| heldout_sentiment_sst2 | binary acc % | 46.7 | 83.3 | 100.0 | 96.7 |
| heldout_sentiment_sst2 | binary F1 % | 0.0 | 81.5 | 100.0 | 96.8 |
| heldout_sentiment_sst2 | binary AUROC | 0.603 | 0.996 | 1.000 | 0.996 |
| heldout_sentiment_sst2 | binary ECE | 0.497 | 0.259 | 0.144 | 0.068 |
| heldout_topic_dbpedia | question acc % | 90.0 | 93.3 | 100.0 | 100.0 |
| heldout_topic_dbpedia | multiclass acc % | 90.0 | 93.3 | 100.0 | 100.0 |
| heldout_topic_dbpedia | multiclass macro-F1 % | 72.1 | 93.1 | 100.0 | 100.0 |
| heldout_topic_dbpedia | multiclass ECE | 0.077 | 0.070 | 0.002 | 0.000 |
| hf_emotions_multilabel | question acc % | 0.0 | 46.7 | 33.3 | 56.7 |
| hf_emotions_multilabel | multilabel exact % | 0.0 | 46.7 | 33.3 | 56.7 |
| hf_emotions_multilabel | multilabel micro-F1 % | 0.0 | 67.7 | 61.5 | 71.6 |
| hf_emotions_multilabel | multilabel label AUROC | 0.682 | 0.917 | 0.878 | 0.952 |
| hf_emotions_multilabel | multilabel ECE | 0.179 | 0.064 | 0.088 | 0.063 |
| hf_intent_banking77 | question acc % | 86.7 | 86.7 | 93.3 | 96.7 |
| hf_intent_banking77 | multiclass acc % | 86.7 | 86.7 | 93.3 | 96.7 |
| hf_intent_banking77 | multiclass macro-F1 % | 75.9 | 73.3 | 85.7 | 94.9 |
| hf_intent_banking77 | multiclass ECE | 0.174 | 0.106 | 0.052 | 0.024 |
| hf_nli | question acc % | 50.0 | 90.0 | 86.7 | 90.0 |
| hf_nli | binary acc % | 50.0 | 90.0 | 86.7 | 90.0 |
| hf_nli | binary F1 % | 61.5 | 88.0 | 85.7 | 85.7 |
| hf_nli | binary AUROC | 0.819 | 0.958 | 1.000 | 0.979 |
| hf_nli | binary ECE | 0.458 | 0.145 | 0.139 | 0.089 |
| hf_sentiment_tweets | question acc % | 63.3 | 73.3 | 60.0 | 63.3 |
| hf_sentiment_tweets | multiclass acc % | 63.3 | 73.3 | 60.0 | 63.3 |
| hf_sentiment_tweets | multiclass macro-F1 % | 63.4 | 75.6 | 61.0 | 65.7 |
| hf_sentiment_tweets | multiclass ECE | 0.169 | 0.109 | 0.304 | 0.256 |
| hf_topic_agnews | question acc % | 73.3 | 76.7 | 83.3 | 86.7 |
| hf_topic_agnews | multiclass acc % | 73.3 | 76.7 | 83.3 | 86.7 |
| hf_topic_agnews | multiclass macro-F1 % | 67.7 | 77.2 | 82.0 | 86.1 |
| hf_topic_agnews | multiclass ECE | 0.200 | 0.172 | 0.177 | 0.139 |

## Question accuracy % by hard-case tag

| tag | n | base | LoRA | ~typesafe/jev-latest | openai/gpt-6-astra |
|---|---|---|---|---|---|
| (none) | 335 | 67.2 | 77.6 | 82.7 | 86.3 |
| contradiction | 20 | 10.0 | 70.0 | 100.0 | 100.0 |
| distractor | 33 | 21.2 | 45.5 | 93.9 | 100.0 |
| double_negation | 6 | 33.3 | 33.3 | 83.3 | 100.0 |
| evidence_end | 13 | 38.5 | 46.2 | 84.6 | 100.0 |
| evidence_middle | 11 | 45.5 | 54.5 | 81.8 | 100.0 |
| evidence_start | 9 | 55.6 | 77.8 | 100.0 | 100.0 |
| exception | 7 | 0.0 | 0.0 | 71.4 | 100.0 |
| hypothetical | 7 | 57.1 | 57.1 | 100.0 | 100.0 |
| injection | 10 | 60.0 | 50.0 | 100.0 | 100.0 |
| lexical_overlap | 20 | 40.0 | 55.0 | 100.0 | 100.0 |
| long_state | 50 | 36.0 | 46.0 | 90.0 | 100.0 |
| missing_evidence | 18 | 22.2 | 77.8 | 77.8 | 100.0 |
| multi_positive | 35 | 2.9 | 11.4 | 91.4 | 91.4 |
| multi_turn | 9 | 33.3 | 77.8 | 100.0 | 100.0 |
| negation | 30 | 33.3 | 56.7 | 100.0 | 100.0 |
| new_label_names | 3 | 0.0 | 100.0 | 100.0 | 100.0 |
| nota | 2 | 50.0 | 50.0 | 100.0 | 100.0 |
| numeric_reasoning | 16 | 37.5 | 37.5 | 93.8 | 100.0 |
| paraphrase | 22 | 18.2 | 50.0 | 100.0 | 100.0 |
| role_reversal | 15 | 40.0 | 46.7 | 100.0 | 100.0 |
| sarcasm | 12 | 8.3 | 33.3 | 100.0 | 100.0 |
| temporal_reasoning | 29 | 31.0 | 37.9 | 79.3 | 100.0 |
| zero_positive | 6 | 33.3 | 33.3 | 100.0 | 100.0 |

## Paired tests vs our LoRA model (exact McNemar on the same questions)

| other | n | LoRA only right | other only right | p |
|---|---|---|---|---|
| base | 501 | 108 | 40 | 2.1e-08 |
| ~typesafe/jev-latest | 501 | 30 | 109 | 9.9e-12 |
| openai/gpt-6-astra | 501 | 19 | 121 | 2.3e-19 |

Spend (USD, from OpenRouter account usage): {'~typesafe/jev-latest': 0.0109, 'openai/gpt-6-astra': 0.0}; total $0.01
