# Hard-case data review (round 2)

Authors: 8 Claude Sonnet sub-agents ([BRIEF_sonnet_agents.md](../../../hardcases/BRIEF_sonnet_agents.md), prefixes h*) and OpenRouter models via scripts/data/gen_hardcases.py ([BRIEF.md](../../../hardcases/BRIEF.md), prefixes gf/gk/df/lu; see each row's provenance). Blind judge: gpt-6-astra effort=low batch batch_6ab8cdccc55c8190be72136cfedd6e07, gpt-6-astra effort=low batch batch_6ab8cdce9c5c8190a88ab6e095d2e071. A question is kept only if the judge's answer equals the authored label. LLM-verified, not human-reviewed.

States dropped for overlap with data/eval.jsonl, data/eval2.jsonl, data/eval_llm.jsonl, data/compact_challenge_v1.jsonl: 0

| family | kept | disagreed (dropped) | unanswered (dropped) | agreement % |
|---|---|---|---|---|
| r3_hard | 1207 | 72 | 0 | 94.7 |
| r3_simple | 1259 | 30 | 0 | 97.8 |
| r3_very_hard | 1179 | 77 | 0 | 94.3 |
| **total** | 3645 | 179 | 0 | 95.6 |

--strict: 217 more questions dropped because another question of their text was flagged.
