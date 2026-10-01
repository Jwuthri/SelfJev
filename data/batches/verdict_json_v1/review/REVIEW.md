# Hard-case data review (round 2)

Authors: 8 Claude Sonnet sub-agents ([BRIEF_sonnet_agents.md](../../../hardcases/BRIEF_sonnet_agents.md), prefixes h*) and OpenRouter models via scripts/data/gen_hardcases.py ([BRIEF.md](../../../hardcases/BRIEF.md), prefixes gf/gk/df/lu; see each row's provenance). Blind judge: gpt-6-astra effort=low batch batch_6abe2ab7117c8190a8e763fc81b36608, gpt-6-astra effort=low batch batch_6abe2ab8d8c08190a851391b2ab8a1d9. A question is kept only if the judge's answer equals the authored label. LLM-verified, not human-reviewed.

States dropped for overlap with data/eval.jsonl, data/eval2.jsonl, data/eval_llm.jsonl, data/compact_challenge_v1.jsonl: 0

| family | kept | disagreed (dropped) | unanswered (dropped) | agreement % |
|---|---|---|---|---|
| r3_hard | 1385 | 53 | 0 | 96.4 |
| r3_simple | 1403 | 45 | 0 | 97.0 |
| r3_very_hard | 1307 | 82 | 0 | 94.4 |
| **total** | 4095 | 180 | 0 | 95.9 |

--strict: 159 more questions dropped because another question of their text was flagged.
