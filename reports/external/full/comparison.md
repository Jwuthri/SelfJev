# Comparison: base vs LoRA vs ~typesafe/jev-latest vs openai/gpt-6-astra

| | base | LoRA | ~typesafe/jev-latest | openai/gpt-6-astra |
|---|---|---|---|---|
| adapter | None | None | None | None |
| calibration | no | no | no | no |
| prompt | ours-base (-) | ours-LoRA (-) | ~typesafe/jev-latest (-) | openai/gpt-6-astra (-) |
| n | 3471 | 3471 | 3471 | 3471 |

| slice | metric | base | LoRA | ~typesafe/jev-latest | openai/gpt-6-astra |
|---|---|---|---|---|---|
| overall | question acc % | 61.0 | 73.5 | 82.7 | 85.8 |
| overall | binary acc % | 55.3 | 77.8 | 93.5 | 93.8 |
| overall | binary F1 % | 55.8 | 75.1 | 93.2 | 93.4 |
| overall | binary AUROC | 0.605 | 0.863 | 0.981 | 0.971 |
| overall | binary ECE | 0.384 | 0.066 | 0.045 | 0.050 |
| overall | multiclass acc % | 73.3 | 78.3 | 84.6 | 87.0 |
| overall | multiclass macro-F1 % | 79.6 | 82.3 | 91.6 | 95.3 |
| overall | multiclass ECE | 0.026 | 0.027 | 0.099 | 0.087 |
| overall | multilabel exact % | 1.2 | 31.1 | 40.1 | 55.8 |
| overall | multilabel micro-F1 % | 23.6 | 62.9 | 66.3 | 74.0 |
| overall | multilabel label AUROC | 0.679 | 0.882 | 0.890 | 0.940 |
| overall | multilabel ECE | 0.203 | 0.052 | 0.066 | 0.063 |
| overall | binary brier | 0.397 | 0.155 | 0.051 | 0.058 |
| overall | binary log_loss | 1.747 | 0.480 | 0.191 | 0.431 |
| overall | multiclass brier | 0.363 | 0.301 | 0.258 | 0.215 |
| overall | multiclass log_loss | 0.717 | 0.601 | 2.134 | 0.605 |
| overall | multilabel brier | 0.208 | 0.113 | 0.112 | 0.087 |
| overall | multilabel log_loss | 1.106 | 0.359 | 0.359 | 0.296 |
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
| heldout_boolq | question acc % | 59.3 | 70.3 | 90.7 | 89.0 |
| heldout_boolq | binary acc % | 59.3 | 70.3 | 90.7 | 89.0 |
| heldout_boolq | binary F1 % | 70.7 | 73.7 | 91.9 | 90.5 |
| heldout_boolq | binary AUROC | 0.631 | 0.768 | 0.965 | 0.940 |
| heldout_boolq | binary ECE | 0.320 | 0.103 | 0.038 | 0.101 |
| heldout_emotion_multiclass | question acc % | 51.0 | 56.0 | 57.7 | 62.3 |
| heldout_emotion_multiclass | multiclass acc % | 51.0 | 56.0 | 57.7 | 62.3 |
| heldout_emotion_multiclass | multiclass macro-F1 % | 41.2 | 47.3 | 47.2 | 54.6 |
| heldout_emotion_multiclass | multiclass ECE | 0.073 | 0.063 | 0.301 | 0.233 |
| heldout_intent_clinc | question acc % | 92.3 | 89.3 | 94.3 | 95.3 |
| heldout_intent_clinc | multiclass acc % | 92.3 | 89.3 | 94.3 | 95.3 |
| heldout_intent_clinc | multiclass macro-F1 % | 94.9 | 90.8 | 95.4 | 95.9 |
| heldout_intent_clinc | multiclass ECE | 0.054 | 0.034 | 0.026 | 0.042 |
| heldout_question_type_trec | question acc % | 64.3 | 68.0 | 94.0 | 95.3 |
| heldout_question_type_trec | multiclass acc % | 64.3 | 68.0 | 94.0 | 95.3 |
| heldout_question_type_trec | multiclass macro-F1 % | 56.0 | 68.1 | 91.5 | 94.5 |
| heldout_question_type_trec | multiclass ECE | 0.093 | 0.066 | 0.035 | 0.042 |
| heldout_sentiment_sst2 | question acc % | 50.0 | 76.7 | 96.7 | 97.0 |
| heldout_sentiment_sst2 | binary acc % | 50.0 | 76.7 | 96.7 | 97.0 |
| heldout_sentiment_sst2 | binary F1 % | 0.0 | 69.8 | 96.6 | 96.9 |
| heldout_sentiment_sst2 | binary AUROC | 0.544 | 0.935 | 0.994 | 0.988 |
| heldout_sentiment_sst2 | binary ECE | 0.471 | 0.189 | 0.097 | 0.020 |
| heldout_topic_dbpedia | question acc % | 89.3 | 91.7 | 98.0 | 99.0 |
| heldout_topic_dbpedia | multiclass acc % | 89.3 | 91.7 | 98.0 | 99.0 |
| heldout_topic_dbpedia | multiclass macro-F1 % | 88.4 | 91.5 | 97.8 | 98.9 |
| heldout_topic_dbpedia | multiclass ECE | 0.050 | 0.040 | 0.012 | 0.009 |
| hf_emotions_multilabel | question acc % | 0.0 | 32.3 | 31.7 | 49.3 |
| hf_emotions_multilabel | multilabel exact % | 0.0 | 32.3 | 31.7 | 49.3 |
| hf_emotions_multilabel | multilabel micro-F1 % | 0.6 | 60.1 | 58.8 | 67.6 |
| hf_emotions_multilabel | multilabel label AUROC | 0.661 | 0.882 | 0.855 | 0.917 |
| hf_emotions_multilabel | multilabel ECE | 0.189 | 0.041 | 0.071 | 0.071 |
| hf_intent_banking77 | question acc % | 89.3 | 92.7 | 95.7 | 96.3 |
| hf_intent_banking77 | multiclass acc % | 89.3 | 92.7 | 95.7 | 96.3 |
| hf_intent_banking77 | multiclass macro-F1 % | 88.5 | 90.3 | 95.0 | 96.4 |
| hf_intent_banking77 | multiclass ECE | 0.011 | 0.027 | 0.023 | 0.023 |
| hf_nli | question acc % | 56.7 | 89.0 | 92.7 | 93.7 |
| hf_nli | binary acc % | 56.7 | 89.0 | 92.7 | 93.7 |
| hf_nli | binary F1 % | 60.8 | 85.5 | 90.4 | 90.6 |
| hf_nli | binary AUROC | 0.804 | 0.946 | 0.985 | 0.977 |
| hf_nli | binary ECE | 0.394 | 0.040 | 0.072 | 0.062 |
| hf_sentiment_tweets | question acc % | 54.3 | 66.7 | 64.3 | 68.7 |
| hf_sentiment_tweets | multiclass acc % | 54.3 | 66.7 | 64.3 | 68.7 |
| hf_sentiment_tweets | multiclass macro-F1 % | 55.1 | 66.6 | 64.6 | 68.9 |
| hf_sentiment_tweets | multiclass ECE | 0.075 | 0.058 | 0.242 | 0.205 |
| hf_topic_agnews | question acc % | 77.3 | 86.7 | 87.3 | 90.0 |
| hf_topic_agnews | multiclass acc % | 77.3 | 86.7 | 87.3 | 90.0 |
| hf_topic_agnews | multiclass macro-F1 % | 76.4 | 86.8 | 87.0 | 89.9 |
| hf_topic_agnews | multiclass ECE | 0.117 | 0.063 | 0.106 | 0.083 |

## Question accuracy % by hard-case tag

| tag | n | base | LoRA | ~typesafe/jev-latest | openai/gpt-6-astra |
|---|---|---|---|---|---|
| (none) | 3042 | 64.3 | 74.2 | 82.2 | 85.0 |
| contradiction | 107 | 30.8 | 90.7 | 100.0 | 100.0 |
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
| missing_evidence | 104 | 37.5 | 81.7 | 84.6 | 98.1 |
| multi_positive | 81 | 1.2 | 18.5 | 56.8 | 58.0 |
| multi_turn | 9 | 33.3 | 77.8 | 100.0 | 100.0 |
| negation | 30 | 33.3 | 56.7 | 100.0 | 100.0 |
| new_label_names | 3 | 0.0 | 100.0 | 100.0 | 100.0 |
| nota | 46 | 87.0 | 89.1 | 100.0 | 100.0 |
| numeric_reasoning | 16 | 37.5 | 37.5 | 93.8 | 100.0 |
| paraphrase | 22 | 18.2 | 50.0 | 100.0 | 100.0 |
| role_reversal | 15 | 40.0 | 46.7 | 100.0 | 100.0 |
| sarcasm | 12 | 8.3 | 33.3 | 100.0 | 100.0 |
| temporal_reasoning | 29 | 31.0 | 37.9 | 79.3 | 100.0 |
| zero_positive | 6 | 33.3 | 33.3 | 100.0 | 100.0 |

## Paired tests vs our LoRA model (exact McNemar on the same questions)

| other | n | LoRA only right | other only right | p |
|---|---|---|---|---|
| base | 3471 | 605 | 172 | 2.9e-57 |
| ~typesafe/jev-latest | 3471 | 197 | 516 | 8.2e-34 |
| openai/gpt-6-astra | 3471 | 153 | 580 | 2.6e-59 |

Spend (USD, from OpenRouter account usage): {'~typesafe/jev-latest': 0.0, 'openai/gpt-6-astra': 16.6886}; total $0.00
