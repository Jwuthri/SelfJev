# Hard-case data review (round 2)

Authors: 8 Claude Sonnet sub-agents ([BRIEF_sonnet_agents.md](../BRIEF_sonnet_agents.md), prefixes h*) and OpenRouter models via scripts/gen_hardcases.py ([BRIEF.md](../BRIEF.md), prefixes gf/gk/df/lu; see each row's provenance). Blind judge: gpt-6-astra effort=low batch batch_6ab814bce54881909f69cadc50d3f3d3. A question is kept only if the judge's answer equals the authored label. LLM-verified, not human-reviewed.

States dropped for overlap with data/eval.jsonl, data/eval2.jsonl, data/eval_llm.jsonl, data/compact_challenge_v1.jsonl: 0

| family | kept | disagreed (dropped) | unanswered (dropped) | agreement % |
|---|---|---|---|---|
| r3_hard | 174 | 23 | 0 | 89.3 |
| r3_simple | 180 | 14 | 0 | 93.5 |
| r3_very_hard | 195 | 8 | 0 | 96.2 |
| **total** | 549 | 45 | 0 | 93.0 |

--strict: 49 more questions dropped because another question of their text was flagged.
