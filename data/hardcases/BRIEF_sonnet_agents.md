# Hard-case brief used by the 8 Claude Sonnet sub-agents (round 2, prefixes hnum/htmp/hrol/hinj/hlng/hmul/hpol/hpar)

Preserved copy: data/hardcases/BRIEF.md was later rewritten for the OpenRouter generator (scripts/gen_hardcases.py).
The Sonnet agents were launched with the text below (plus a one-paragraph assignment each, recorded in the session).

---

You are writing HARD TRAINING data for a small instruction-conditioned text classifier. It already handles easy
cases well; it fails on traps. Every question you write must contain at least one real trap, and the correct
label must follow from careful reading and, where needed, explicit arithmetic.

Output: JSON Lines, one SOURCE per line: {"source_id": "<PREFIX>-0001", "family": "<FAMILY>", "provenance":
"synthetic:claude-sonnet (hard cases r2)", "state": "...", "questions": [...]}. binary has no candidates;
multiclass 2-8 candidates, one correct; multilabel 3-8 candidates, target = all correct ids (may be []). notes
required (<= 30 words; for numbers and dates, the computation). Optional paraphrase_group. No other fields.

Labeling policy: evidence only (contradicted or not stated -> false); instructions inside the state are data;
negations/hypotheticals are not the thing itself; roles matter; policies apply exactly as written; multiclass
never ambiguous (explicit "none" candidate when needed); balanced labels, at least a third of multilabel questions
with 3+ positives.

Traps (every question needs at least one): numeric_reasoning, temporal_reasoning, role_reversal, injection,
sarcasm, negation, double_negation, hypothetical, distractor, evidence_start/middle/end, long_state,
lexical_overlap, paraphrase, multi_positive, zero_positive, exception, missing_evidence, contradiction,
multi_turn, nota. Long states 600-1500 words with evidence mostly in the middle; contrastive minimal pairs where
natural; ~45% binary / 30% multiclass / 25% multilabel; no graded-AI-reply examples (held-out family).

Process: batches of ~20 sources per file data/hardcases/raw/<PREFIX>_<NN>.jsonl, checked with
`python -m personal_jev.data check`; re-check every numeric and date label; never read data/eval*, reports/ or
other agents' files.
