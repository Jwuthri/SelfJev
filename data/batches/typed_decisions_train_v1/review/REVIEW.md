# Hard-case data review (round 2)

Authors: 8 Claude Sonnet sub-agents ([BRIEF_sonnet_agents.md](../../../hardcases/BRIEF_sonnet_agents.md), prefixes h*) and OpenRouter models via scripts/data/gen_hardcases.py ([BRIEF.md](../../../hardcases/BRIEF.md), prefixes gf/gk/df/lu; see each row's provenance). Blind judge: gpt-6-astra effort=low batch batch_6abe07c002c48190939387a2814ee5d1, gpt-6-astra effort=low batch batch_6abe07c11ef88190a0eaaed919c0fe38. A question is kept only if the judge's answer equals the authored label. LLM-verified, not human-reviewed.

States dropped for overlap with data/eval.jsonl, data/eval2.jsonl, data/eval_llm.jsonl, data/compact_challenge_v1.jsonl: 0

| family | kept | disagreed (dropped) | unanswered (dropped) | agreement % |
|---|---|---|---|---|
| td_agent_trace_observability | 1133 | 367 | 0 | 75.5 |
| td_customer_service | 1269 | 231 | 0 | 84.6 |
| td_invoice_processing | 1087 | 413 | 0 | 72.5 |
| td_security_incidents | 1110 | 390 | 0 | 74.0 |
| **total** | 4599 | 1401 | 0 | 76.7 |
