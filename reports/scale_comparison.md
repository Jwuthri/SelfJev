**Test split: 3471 identical questions** (`hf.jsonl` test + `eval.jsonl` test). Qwen rows are Qwen3-Reranker checkpoints; "+ LoRA" = the same frozen checkpoint plus our rank-16 adapter on q/k/v/o.

| | 0.6B | 0.6B + LoRA | 4B | 4B + LoRA | 8B | 8B + LoRA | Jev | GPT-6 Astra |
|---|---|---|---|---|---|---|---|---|
| question accuracy % | 61.0 | 73.5 | 62.8 | 80.3 | 66.2 | 80.7 | 82.7 | **85.8** |
| binary accuracy % | 55.3 | 77.8 | 55.0 | 87.5 | 56.1 | 87.3 | 93.5 | **93.8** |
| binary F1 % | 55.8 | 75.1 | 57.8 | 86.7 | 58.6 | 86.6 | 93.2 | **93.4** |
| binary AUROC | 0.605 | 0.863 | 0.604 | 0.945 | 0.658 | 0.945 | **0.981** | 0.971 |
| multiclass accuracy % | 73.3 | 78.3 | 76.2 | 82.3 | 79.8 | 82.9 | 84.6 | **87.0** |
| multiclass macro-F1 % | 79.6 | 82.3 | 83.4 | 86.2 | 86.5 | 88.7 | 91.6 | **95.3** |
| multilabel exact match % | 1.2 | 31.1 | 2.0 | 47.7 | 10.2 | 48.0 | 40.1 | **55.8** |
| multilabel micro-F1 % | 23.6 | 62.9 | 25.1 | 73.6 | 35.6 | 72.1 | 66.3 | **74.0** |
| multilabel label AUROC | 0.679 | 0.882 | 0.691 | 0.930 | 0.815 | 0.931 | 0.890 | **0.940** |
| binary ECE | 0.384 | 0.066 | 0.357 | 0.056 | 0.364 | 0.051 | **0.045** | 0.050 |
| binary Brier | 0.397 | 0.155 | 0.375 | 0.094 | 0.364 | 0.094 | **0.051** | 0.058 |
| multiclass ECE (top-label) | 0.026 | 0.027 | 0.144 | 0.029 | **0.020** | 0.023 | 0.099 | 0.087 |
| dtype / prompt | float32 / task-v1 | float32 / task-v1 | bfloat16 / answer-v1 | bfloat16 / answer-v1 | bfloat16 / task-v1 | bfloat16 / task-v1 | API | API |

**Paired exact McNemar** (questions only one side gets right)

| comparison | left only | right only | p |
|---|---|---|---|
| 0.6B vs 0.6B + LoRA | 172 | 605 | 2.9e-57 |
| 4B vs 4B + LoRA | 156 | 763 | 1.2e-96 |
| 8B vs 8B + LoRA | 112 | 614 | 1.1e-84 |
| 0.6B + LoRA vs 4B + LoRA | 123 | 359 | 7.9e-28 |
| 4B + LoRA vs 8B + LoRA | 141 | 153 | 0.52 |
| 8B + LoRA vs Jev | 205 | 276 | 0.0014 |
| 8B + LoRA vs GPT-6 Astra | 140 | 319 | 3.9e-17 |

**Question accuracy % by family**

| family | n | 0.6B | 0.6B + LoRA | 4B | 4B + LoRA | 8B | 8B + LoRA | Jev | GPT-6 Astra |
|---|---|---|---|---|---|---|---|---|---|
| eval_adversarial | 27 | 74.1 | 63.0 | 55.6 | 81.5 | 63.0 | 81.5 | 100.0 | 100.0 |
| eval_agent_output | 26 | 30.8 | 46.2 | 46.2 | 53.8 | 57.7 | 53.8 | 92.3 | 100.0 |
| eval_evidence | 17 | 41.2 | 82.4 | 47.1 | 82.4 | 41.2 | 94.1 | 100.0 | 100.0 |
| eval_multilabel | 32 | 12.5 | 34.4 | 18.8 | 75.0 | 31.2 | 84.4 | 100.0 | 100.0 |
| eval_policy | 22 | 31.8 | 40.9 | 40.9 | 50.0 | 31.8 | 50.0 | 72.7 | 100.0 |
| eval_routing | 25 | 48.0 | 76.0 | 56.0 | 84.0 | 64.0 | 92.0 | 100.0 | 100.0 |
| eval_urgency_sentiment | 22 | 40.9 | 54.5 | 54.5 | 68.2 | 63.6 | 68.2 | 95.5 | 100.0 |
| heldout_boolq | 300 | 59.3 | 70.3 | 62.0 | 83.3 | 62.0 | 83.0 | 90.7 | 89.0 |
| heldout_emotion_multiclass | 300 | 51.0 | 56.0 | 47.3 | 58.0 | 52.7 | 57.0 | 57.7 | 62.3 |
| heldout_intent_clinc | 300 | 92.3 | 89.3 | 94.7 | 93.0 | 89.3 | 93.7 | 94.3 | 95.3 |
| heldout_question_type_trec | 300 | 64.3 | 68.0 | 73.7 | 76.3 | 82.0 | 81.7 | 94.0 | 95.3 |
| heldout_sentiment_sst2 | 300 | 50.0 | 76.7 | 50.3 | 88.0 | 50.0 | 88.7 | 96.7 | 97.0 |
| heldout_topic_dbpedia | 300 | 89.3 | 91.7 | 93.7 | 96.0 | 96.0 | 96.0 | 98.0 | 99.0 |
| hf_emotions_multilabel | 300 | 0.0 | 32.3 | 0.7 | 46.7 | 8.0 | 45.7 | 31.7 | 49.3 |
| hf_intent_banking77 | 300 | 89.3 | 92.7 | 91.0 | 96.7 | 94.0 | 95.0 | 95.7 | 96.3 |
| hf_nli | 300 | 56.7 | 89.0 | 52.7 | 92.3 | 57.7 | 91.7 | 92.7 | 93.7 |
| hf_sentiment_tweets | 300 | 54.3 | 66.7 | 54.3 | 69.3 | 64.3 | 69.0 | 64.3 | 68.7 |
| hf_topic_agnews | 300 | 77.3 | 86.7 | 81.3 | 89.3 | 81.3 | 89.3 | 87.3 | 90.0 |

**Question accuracy % by hard-case tag (n >= 10)**

| tag | n | 0.6B | 0.6B + LoRA | 4B | 4B + LoRA | 8B | 8B + LoRA | Jev | GPT-6 Astra |
|---|---|---|---|---|---|---|---|---|---|
| (none) | 3042 | 64.3 | 74.2 | 66.7 | 80.5 | 70.5 | 80.9 | 82.2 | 85.0 |
| contradiction | 107 | 30.8 | 90.7 | 25.2 | 99.1 | 35.5 | 99.1 | 100.0 | 100.0 |
| distractor | 33 | 21.2 | 45.5 | 27.3 | 51.5 | 33.3 | 72.7 | 93.9 | 100.0 |
| evidence_end | 13 | 38.5 | 46.2 | 53.8 | 76.9 | 30.8 | 92.3 | 84.6 | 100.0 |
| evidence_middle | 11 | 45.5 | 54.5 | 45.5 | 54.5 | 54.5 | 63.6 | 81.8 | 100.0 |
| injection | 10 | 60.0 | 50.0 | 50.0 | 70.0 | 50.0 | 70.0 | 100.0 | 100.0 |
| lexical_overlap | 20 | 40.0 | 55.0 | 30.0 | 80.0 | 45.0 | 90.0 | 100.0 | 100.0 |
| long_state | 50 | 36.0 | 46.0 | 46.0 | 64.0 | 38.0 | 76.0 | 90.0 | 100.0 |
| missing_evidence | 104 | 37.5 | 81.7 | 32.7 | 91.3 | 37.5 | 87.5 | 84.6 | 98.1 |
| multi_positive | 81 | 1.2 | 18.5 | 2.5 | 38.3 | 8.6 | 37.0 | 56.8 | 58.0 |
| negation | 30 | 33.3 | 56.7 | 30.0 | 90.0 | 36.7 | 90.0 | 100.0 | 100.0 |
| nota | 46 | 87.0 | 89.1 | 91.3 | 97.8 | 41.3 | 95.7 | 100.0 | 100.0 |
| numeric_reasoning | 16 | 37.5 | 37.5 | 43.8 | 50.0 | 31.2 | 62.5 | 93.8 | 100.0 |
| paraphrase | 22 | 18.2 | 50.0 | 22.7 | 59.1 | 63.6 | 63.6 | 100.0 | 100.0 |
| role_reversal | 15 | 40.0 | 46.7 | 26.7 | 60.0 | 33.3 | 60.0 | 100.0 | 100.0 |
| sarcasm | 12 | 8.3 | 33.3 | 25.0 | 66.7 | 41.7 | 66.7 | 100.0 | 100.0 |
| temporal_reasoning | 29 | 31.0 | 37.9 | 34.5 | 41.4 | 31.0 | 51.7 | 79.3 | 100.0 |
