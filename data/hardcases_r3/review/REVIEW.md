# Hard-case data review (round 2)

Authors: 8 Claude Sonnet sub-agents ([BRIEF_sonnet_agents.md](../BRIEF_sonnet_agents.md), prefixes h*) and OpenRouter models via scripts/gen_hardcases.py ([BRIEF.md](../BRIEF.md), prefixes gf/gk/df/lu; see each row's provenance). Blind judge: gpt-6-astra effort=low batch batch_6ab4daccea9c8190a683bf08d81330f1, gpt-6-astra effort=low batch batch_6ab4dacecfe0819086148f13b226c737, gpt-6-astra effort=low batch batch_6ab4dad167ec81908e0cfe5c149fbe46, gpt-6-astra effort=low batch batch_6ab4dad2ac8081909f41834f0fdefc12, gpt-6-astra effort=low batch batch_6ab4e57e52888190b002ce061ba199ea. A question is kept only if the judge's answer equals the authored label. LLM-verified, not human-reviewed.

States dropped for overlap with data/eval.jsonl, data/eval2.jsonl: 0

| family | kept | disagreed (dropped) | unanswered (dropped) | agreement % |
|---|---|---|---|---|
| r3_hard | 12859 | 466 | 0 | 96.5 |
| r3_simple | 13124 | 160 | 0 | 98.8 |
| r3_very_hard | 12645 | 579 | 0 | 95.6 |
| **total** | 38628 | 1205 | 0 | 97.0 |
