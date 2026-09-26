# LLM-oriented multilabel questions (score, judge, verify, guardrail, jailbreak) with near-miss negatives and implicit positives

Built 2026-09-26 with `gen_hardcases.py --usecases train --multilabel --batch llm_multilabel_v1` (GPT-6 Luna, Gemini 3.8 Flash,
Grok 4.7 through OpenRouter) and `gen_gemini_batch.py` (Gemini 3.8 Flash through Google's Batch API after the OpenRouter key
hit its monthly limit). Aimed at our best model's eval2 multilabel errors (26 of 38 added a near-miss candidate). Blind
GPT-6 Astra judge, strict build, moderation screen (11 texts removed: self-harm method details, a reply encouraging suicide, a graphic torture scene). Details:
docs/llm_eval_data.md and docs/JOURNAL.md (2026-09-26).
