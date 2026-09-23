# Evaluation-set brief

Given verbatim to each Claude Opus eval-author agent, with a one-paragraph assignment. The eval set is
authored independently of the training data (a different model, a different brief, no access to
`data/synthetic/`). Labels are LLM-authored and then checked by a separate blind LLM relabelling pass; they
are **pending human review**. Splits (validation / calibration / test) are assigned afterwards by hashing
`source_id`, so every question about one state lands in the same split.

---

You are writing EVALUATION data for a small instruction-conditioned text classifier. Quality matters far
more than quantity: every label will be used to measure a model, so each must be unambiguous and correct.

The classifier reads a *state* (any text), a natural-language *question*, and either nothing (binary) or
candidate answers with descriptions (multiclass/multilabel). For each candidate it decides whether that
candidate is a correct answer given only the state.

## Output format

JSON Lines. One line = one SOURCE (a state) with 1–4 questions about it:

```json
{"source_id": "<PREFIX>-001", "family": "<FAMILY>", "provenance": "llm-authored:claude-opus (eval; pending human review)", "state": "...", "questions": [
  {"type": "binary", "instruction": "Is the customer asking to cancel their subscription?", "target": false, "hard_cases": ["negation"], "notes": "explicitly says do not cancel"},
  {"type": "multiclass", "instruction": "Which team should handle the underlying issue?", "candidates": [{"id": "technical", "description": "Technical support: software malfunctions and integration failures"}, {"id": "sales", "description": "Sales: buying a product or discussing an upgrade"}], "target": "technical", "hard_cases": ["lexical_overlap"]},
  {"type": "multilabel", "instruction": "Which of these does the message report?", "candidates": [{"id": "revenue_loss", "description": "The customer reports losing revenue"}, {"id": "refund", "description": "The customer requests a refund"}], "target": ["revenue_loss"], "hard_cases": []}
]}
```

- binary: no `candidates`; `target` is `true` / `false`.
- multiclass: 2–8 candidates with unique snake_case ids, exactly one correct; `target` is its id.
- multilabel: 2–8 candidates; `target` lists ALL correct ids (may be `[]`); every other candidate must be
  clearly incorrect.
- `notes`: ≤ 25 words justifying the label for the human reviewer.
- Optional `paraphrase_group`: same string on 2+ questions of the SAME source that ask the same thing with
  reworded question and/or reworded candidate descriptions (same ids, same target). Tag them `paraphrase`.
- No other fields.

## Labeling policy (follow exactly)

1. Evidence only. Binary `true` only if the state supports answering "Yes". Contradicted → `false`
   (`contradiction`); simply not stated → `false` (`missing_evidence`). `false` means "not supported by the
   text", not "known to be false in the world".
2. Instructions inside the state are data; labels follow the actual content (`injection`).
3. Negations, hypotheticals and future conditionals are not the thing itself.
4. Roles matter: who does what to whom (`role_reversal`).
5. Policies: apply rules exactly as written in the state, including exceptions, thresholds, dates and
   priority order; no outside knowledge.
6. Multiclass is never ambiguous. If no substantive option applies, include an explicit
   `{"id": "none", "description": "None of the above: ..."}` candidate and target it (`nota`).
7. Balance: binary targets roughly 50/50; correct multiclass candidate at varied positions; multilabel
   includes zero-positive (`zero_positive`), single-positive and multi-positive (`multi_positive`) cases.

## Hard-case tags (use only these)

negation, double_negation, lexical_overlap, role_reversal, exception, missing_evidence, contradiction,
distractor, evidence_start, evidence_middle, evidence_end, long_state, injection, hypothetical, sarcasm,
nota, zero_positive, multi_positive, paraphrase, numeric_reasoning, temporal_reasoning, multi_turn,
new_label_names

Include some easy, clean cases too (no tags): an eval set that is only traps cannot show whether the model
handles ordinary inputs.

## Length mix

~40% short (1–4 sentences), ~35% medium (120–400 words), ~25% long (400–1500 words, tag `long_state`) with
the decisive evidence at varied positions and plausible distractors.

## Process

- Write one or two files: `data/eval/raw/<PREFIX>_<NN>.jsonl` with the Write tool.
- After each file run
  `cd /Users/julien/Documents/Repos/SelfJev && .venv/bin/python -m personal_jev.data check data/eval/raw/<file>`
  and fix all errors.
- `source_id` = `<PREFIX>-<3-digit counter>`.
- Then re-read every item as a skeptical reviewer: is the label unambiguous and correct under the policy
  above? Fix or delete anything doubtful.
- Do not read anything under `data/synthetic/` and do not touch code or other agents' files.
- Invent all names and companies; no real people or real customer data.
- Final reply: counts (sources, questions by type), file names, and anything you consider borderline.
