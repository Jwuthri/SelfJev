# Hard-case data review (round 2)

Authors: 8 Claude Sonnet sub-agents ([BRIEF_sonnet_agents.md](../../../hardcases/BRIEF_sonnet_agents.md), prefixes h*) and OpenRouter models via scripts/data/gen_hardcases.py ([BRIEF.md](../../../hardcases/BRIEF.md), prefixes gf/gk/df/lu; see each row's provenance). Blind judge: gpt-6-astra effort=low batch batch_6abc9f8e192481908bae45158b2050f5. A question is kept only if the judge's answer equals the authored label. LLM-verified, not human-reviewed.

States dropped for overlap with data/eval.jsonl, data/eval2.jsonl, data/eval_llm.jsonl, data/compact_challenge_v1.jsonl: 0

| family | kept | disagreed (dropped) | unanswered (dropped) | agreement % |
|---|---|---|---|---|
| cc_hard | 578 | 2 | 0 | 99.7 |
| cc_simple | 176 | 2 | 0 | 98.9 |
| cc_very_hard | 539 | 3 | 0 | 99.5 |
| **total** | 1293 | 7 | 0 | 99.5 |

--strict: 14 more questions dropped because another question of their text was flagged.
