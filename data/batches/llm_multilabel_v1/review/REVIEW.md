# Hard-case data review (round 2)

Authors: 8 Claude Sonnet sub-agents ([BRIEF_sonnet_agents.md](../BRIEF_sonnet_agents.md), prefixes h*) and OpenRouter models via scripts/gen_hardcases.py ([BRIEF.md](../BRIEF.md), prefixes gf/gk/df/lu; see each row's provenance). Blind judge: gpt-6-astra effort=low batch batch_6ab7e73c28dc8190a8681326c95c41d4, gpt-6-astra effort=low batch batch_6ab7e73dd5448190b069bf37a0ab9401, gpt-6-astra effort=low batch batch_6ab7eb264be8819098dcf87cdd959163, gpt-6-astra effort=low batch batch_6ab7eceb8f588190988124f21d9c514e, gpt-6-astra effort=low batch batch_6ab7eced7b048190b9d16f711416bf3f. A question is kept only if the judge's answer equals the authored label. LLM-verified, not human-reviewed.

States dropped for overlap with data/eval.jsonl, data/eval2.jsonl, data/eval_llm.jsonl, data/compact_challenge_v1.jsonl: 0

| family | kept | disagreed (dropped) | unanswered (dropped) | agreement % |
|---|---|---|---|---|
| llmml_guardrail_hard | 485 | 55 | 0 | 90.6 |
| llmml_guardrail_simple | 571 | 34 | 0 | 94.7 |
| llmml_guardrail_very_hard | 439 | 67 | 0 | 88.2 |
| llmml_jailbreak_hard | 461 | 45 | 0 | 91.7 |
| llmml_jailbreak_simple | 543 | 49 | 0 | 92.3 |
| llmml_jailbreak_very_hard | 432 | 60 | 0 | 88.9 |
| llmml_judge_hard | 489 | 76 | 0 | 88.0 |
| llmml_judge_simple | 578 | 48 | 0 | 92.8 |
| llmml_judge_very_hard | 524 | 84 | 0 | 87.3 |
| llmml_score_hard | 537 | 72 | 0 | 89.2 |
| llmml_score_simple | 555 | 57 | 0 | 91.4 |
| llmml_score_very_hard | 493 | 97 | 0 | 84.6 |
| llmml_verify_hard | 474 | 84 | 0 | 86.3 |
| llmml_verify_simple | 512 | 52 | 0 | 91.6 |
| llmml_verify_very_hard | 477 | 75 | 0 | 87.6 |
| **total** | 7570 | 955 | 0 | 89.7 |

--strict: 735 more questions dropped because another question of their text was flagged.
