# Hard-case data review (round 2)

Authors: 8 Claude Sonnet sub-agents ([BRIEF_sonnet_agents.md](../BRIEF_sonnet_agents.md), prefixes h*) and OpenRouter models via scripts/gen_hardcases.py ([BRIEF.md](../BRIEF.md), prefixes gf/gk/df/lu; see each row's provenance). Blind judge: gpt-6-astra effort=low batch batch_6ab46b0e1eec8190b59a7d41bb55581f, gpt-6-astra effort=low batch batch_6ab4820209d0819093c7dd63d846060a, gpt-6-astra effort=low batch batch_6ab48204a24c8190adae8ef26c86ada6, gpt-6-astra effort=low batch batch_6ab482062e808190b47676c1afaf20cb, gpt-6-astra effort=low batch batch_6ab484b48f8c81909dda709f1e8a82e6. A question is kept only if the judge's answer equals the authored label. LLM-verified, not human-reviewed.

States dropped for overlap with eval.jsonl: 0

| family | kept | disagreed (dropped) | unanswered (dropped) | agreement % |
|---|---|---|---|---|
| hard_contrastive | 235 | 5 | 0 | 97.9 |
| hard_injection_tone | 218 | 2 | 0 | 99.1 |
| hard_long_evidence | 210 | 0 | 0 | 100.0 |
| hard_multilabel | 212 | 14 | 0 | 93.8 |
| hard_numeric | 237 | 1 | 0 | 99.6 |
| hard_policy | 237 | 5 | 0 | 97.9 |
| hard_roles | 291 | 4 | 0 | 98.6 |
| hard_temporal | 219 | 1 | 0 | 99.5 |
| r2_hard | 2730 | 179 | 0 | 93.8 |
| r2_simple | 2823 | 78 | 0 | 97.3 |
| r2_very_hard | 2730 | 196 | 0 | 93.3 |
| **total** | 10142 | 485 | 0 | 95.4 |
