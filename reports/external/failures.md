# Where LoRA fails (full test set, n = 3471)

TEST questions: use for analysis and to steer new training data only; never train on them.

- LoRA wrong: 919 (516 where Jev is right, 403 where Jev is also wrong)
- LoRA right and Jev wrong: 197
- Full list, worst first (Jev-right cases, then by LoRA's confidence in its wrong answer): `reports/external/failures.jsonl`

## Error rate by family (sorted by LoRA - Jev gap)

| slice | n | LoRA error % | Jev error % | gap (pp) | LoRA wrong & Jev right |
|---|---|---|---|---|---|
| eval_multilabel | 32 | 65.6 | 0.0 | +65.6 | 21 |
| eval_agent_output | 26 | 53.8 | 7.7 | +46.2 | 13 |
| eval_urgency_sentiment | 22 | 45.5 | 4.5 | +40.9 | 10 |
| eval_adversarial | 27 | 37.0 | 0.0 | +37.0 | 10 |
| eval_policy | 22 | 59.1 | 27.3 | +31.8 | 8 |
| heldout_question_type_trec | 300 | 32.0 | 6.0 | +26.0 | 79 |
| eval_routing | 25 | 24.0 | 0.0 | +24.0 | 6 |
| heldout_boolq | 300 | 29.7 | 9.3 | +20.3 | 75 |
| heldout_sentiment_sst2 | 300 | 23.3 | 3.3 | +20.0 | 62 |
| eval_evidence | 17 | 17.6 | 0.0 | +17.6 | 3 |
| heldout_topic_dbpedia | 300 | 8.3 | 2.0 | +6.3 | 21 |
| heldout_intent_clinc | 300 | 10.7 | 5.7 | +5.0 | 23 |
| hf_nli | 300 | 11.0 | 7.3 | +3.7 | 21 |
| hf_intent_banking77 | 300 | 7.3 | 4.3 | +3.0 | 12 |
| heldout_emotion_multiclass | 300 | 44.0 | 42.3 | +1.7 | 34 |
| hf_topic_agnews | 300 | 13.3 | 12.7 | +0.7 | 14 |
| hf_emotions_multilabel | 300 | 67.7 | 68.3 | -0.7 | 51 |
| hf_sentiment_tweets | 300 | 33.3 | 35.7 | -2.3 | 53 |

## Error rate by hard-case tag (n >= 10)

| slice | n | LoRA error % | Jev error % | gap (pp) | LoRA wrong & Jev right |
|---|---|---|---|---|---|
| sarcasm | 12 | 66.7 | 0.0 | +66.7 | 8 |
| numeric_reasoning | 16 | 62.5 | 6.2 | +56.2 | 10 |
| role_reversal | 15 | 53.3 | 0.0 | +53.3 | 8 |
| injection | 10 | 50.0 | 0.0 | +50.0 | 5 |
| paraphrase | 22 | 50.0 | 0.0 | +50.0 | 11 |
| distractor | 33 | 54.5 | 6.1 | +48.5 | 16 |
| lexical_overlap | 20 | 45.0 | 0.0 | +45.0 | 9 |
| long_state | 50 | 54.0 | 10.0 | +44.0 | 24 |
| negation | 30 | 43.3 | 0.0 | +43.3 | 13 |
| temporal_reasoning | 29 | 62.1 | 20.7 | +41.4 | 14 |
| evidence_end | 13 | 53.8 | 15.4 | +38.5 | 6 |
| multi_positive | 81 | 81.5 | 43.2 | +38.3 | 37 |
| evidence_middle | 11 | 45.5 | 18.2 | +27.3 | 4 |
| nota | 46 | 10.9 | 0.0 | +10.9 | 5 |
| contradiction | 107 | 9.3 | 0.0 | +9.3 | 10 |
| (none) | 3042 | 25.8 | 17.8 | +8.0 | 424 |
| missing_evidence | 104 | 18.3 | 15.4 | +2.9 | 11 |

## Error rate by question type

| slice | n | LoRA error % | Jev error % | gap (pp) | LoRA wrong & Jev right |
|---|---|---|---|---|---|
| binary | 984 | 22.2 | 6.5 | +15.7 | 182 |
| multilabel | 344 | 68.9 | 59.9 | +9.0 | 84 |
| multiclass | 2143 | 21.7 | 15.4 | +6.3 | 250 |

