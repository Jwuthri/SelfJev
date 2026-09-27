# Hard-case data review (round 2)

Authors: 8 Claude Sonnet sub-agents ([BRIEF_sonnet_agents.md](../../hardcases/BRIEF_sonnet_agents.md), prefixes h*) and OpenRouter models via scripts/gen_hardcases.py ([BRIEF.md](../../hardcases/BRIEF.md), prefixes gf/gk/df/lu; see each row's provenance). Blind judge: gpt-6-astra effort=low batch batch_6ab745e004cc8190908c389b9dc95ff3, gpt-6-astra effort=low batch batch_6ab74bb99b988190bc04b38df5558ec2, gpt-6-astra effort=low batch batch_6ab74bbbd3808190a0bc27373f2faf31, gpt-6-astra effort=low batch batch_6ab74bbdaa3481909b5efede8e381f65, gpt-6-astra effort=low batch batch_6ab74bbec818819098ea9006e552eb96. A question is kept only if the judge's answer equals the authored label. LLM-verified, not human-reviewed.

States dropped for overlap with data/eval.jsonl, data/eval2.jsonl, data/eval_llm.jsonl: 0

| family | kept | disagreed (dropped) | unanswered (dropped) | agreement % |
|---|---|---|---|---|
| llm_guardrail_hard | 645 | 53 | 0 | 93.0 |
| llm_guardrail_simple | 639 | 52 | 0 | 93.0 |
| llm_guardrail_very_hard | 635 | 48 | 0 | 93.6 |
| llm_jailbreak_hard | 655 | 58 | 0 | 92.4 |
| llm_jailbreak_simple | 660 | 46 | 0 | 93.9 |
| llm_jailbreak_very_hard | 588 | 61 | 0 | 91.6 |
| llm_judge_hard | 633 | 58 | 0 | 92.3 |
| llm_judge_simple | 628 | 53 | 0 | 92.9 |
| llm_judge_very_hard | 575 | 99 | 0 | 86.9 |
| llm_score_hard | 618 | 63 | 0 | 91.4 |
| llm_score_simple | 643 | 42 | 0 | 94.3 |
| llm_score_very_hard | 587 | 90 | 0 | 88.3 |
| llm_verify_hard | 649 | 43 | 0 | 94.2 |
| llm_verify_simple | 679 | 33 | 0 | 95.6 |
| llm_verify_very_hard | 609 | 63 | 0 | 91.4 |
| **total** | 9443 | 862 | 0 | 92.3 |

--strict: 897 more questions dropped because another question of their text was flagged.
