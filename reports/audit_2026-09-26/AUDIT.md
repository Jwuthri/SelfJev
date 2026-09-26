# Test-set failure audit (2026-09-26)

Blind relabel by anthropic/claude-opus-5.5 (effort medium) of every test question our best model (`qwen35_4b_tree`) or Jev gets wrong (eval_llm: Jev only). Opus never saw the target or any model answer. Opus wrote a third of eval2 and eval_llm, so on those rows it may side with its own label. Proposed label errors are for human review; the frozen files are unchanged.

## eval2: 119 failed questions relabelled

| who is wrong | label right, model wrong | label probably wrong | ambiguous |
|---|---|---|---|
| ours only | 64 | 0 | 0 |
| Jev only | 28 | 3 | 0 |
| both | 22 | 2 | 0 |
| all | 114 | 5 | 0 |

Real errors (label confirmed) by type: multilabel ours 37 / Jev 21, binary ours 30 / Jev 18, multiclass ours 19 / Jev 11

Real errors (label confirmed) by family: e2_very_hard ours 43 / Jev 22, e2_hard ours 35 / Jev 21, e2_simple ours 8 / Jev 7

Real errors (label confirmed) by trap: distractor ours 33 / Jev 13, multi_positive ours 28 / Jev 13, temporal_reasoning ours 28 / Jev 21, numeric_reasoning ours 26 / Jev 18, paraphrase ours 17 / Jev 9, exception ours 13 / Jev 10, role_reversal ours 11 / Jev 5, multi_turn ours 9 / Jev 6, nota ours 8 / Jev 5, injection ours 8 / Jev 4, long_state ours 8 / Jev 2, double_negation ours 7 / Jev 1

## dev: 778 failed questions relabelled

| who is wrong | label right, model wrong | label probably wrong | ambiguous |
|---|---|---|---|
| ours only | 145 | 26 | 7 |
| Jev only | 142 | 67 | 29 |
| both | 106 | 224 | 32 |
| all | 393 | 317 | 68 |

Real errors (label confirmed) by type: multiclass ours 157 / Jev 146, multilabel ours 32 / Jev 69, binary ours 62 / Jev 33

Real errors (label confirmed) by family: hf_emotions_multilabel ours 23 / Jev 68, heldout_emotion_multiclass ours 62 / Jev 62, hf_sentiment_tweets ours 42 / Jev 28, heldout_sentiment_sst2 ours 27 / Jev 3, heldout_boolq ours 24 / Jev 10, heldout_question_type_trec ours 18 / Jev 12, heldout_intent_clinc ours 13 / Jev 17, hf_nli ours 7 / Jev 16, hf_topic_agnews ours 10 / Jev 14, eval_policy ours 7 / Jev 6, hf_intent_banking77 ours 3 / Jev 5, heldout_topic_dbpedia ours 5 / Jev 4

Real errors (label confirmed) by trap: (none) ours 230 / Jev 221, missing_evidence ours 6 / Jev 15, multi_positive ours 9 / Jev 5, distractor ours 9 / Jev 2, temporal_reasoning ours 8 / Jev 6, long_state ours 4 / Jev 5, exception ours 3 / Jev 2, numeric_reasoning ours 2 / Jev 1, paraphrase ours 2 / Jev 0, evidence_end ours 1 / Jev 2, evidence_middle ours 1 / Jev 2, role_reversal ours 1 / Jev 0

## eval_llm: 71 failed questions relabelled

| who is wrong | label right, model wrong | label probably wrong | ambiguous |
|---|---|---|---|
| ours only | 0 | 0 | 0 |
| Jev only | 68 | 3 | 0 |
| both | 0 | 0 | 0 |
| all | 68 | 3 | 0 |

Real errors (label confirmed) by type: multilabel ours 0 / Jev 31, binary ours 0 / Jev 24, multiclass ours 0 / Jev 13

Real errors (label confirmed) by family: tllm_verify_hard ours 0 / Jev 10, tllm_verify_very_hard ours 0 / Jev 10, tllm_jailbreak_very_hard ours 0 / Jev 9, tllm_score_very_hard ours 0 / Jev 8, tllm_guardrail_hard ours 0 / Jev 8, tllm_judge_very_hard ours 0 / Jev 6, tllm_score_hard ours 0 / Jev 4, tllm_judge_hard ours 0 / Jev 4, tllm_guardrail_simple ours 0 / Jev 2, tllm_judge_simple ours 0 / Jev 2, tllm_guardrail_very_hard ours 0 / Jev 2, tllm_score_simple ours 0 / Jev 1

Real errors (label confirmed) by trap: multi_positive ours 0 / Jev 21, numeric_reasoning ours 0 / Jev 20, flawed_step ours 0 / Jev 14, distractor ours 0 / Jev 12, benign_lookalike ours 0 / Jev 12, judge_injection ours 0 / Jev 10, unsupported_claim ours 0 / Jev 9, speaker_confusion ours 0 / Jev 9, confident_wrong ours 0 / Jev 7, lexical_overlap ours 0 / Jev 7, paraphrase ours 0 / Jev 7, zero_positive ours 0 / Jev 7

## Proposed errata (325 questions): `errata_candidates.jsonl`

