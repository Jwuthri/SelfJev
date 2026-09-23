# Eval-set label review

- Authoring: 7 Claude Opus agents, one family each, from `data/eval/BRIEF.md` (no access to training data).
- Blind relabel: 4 separate Claude Opus instances answered every question from target-free copies
  (`blind_r*.jsonl` -> `answers_r*.jsonl`), using the same labeling policy, without seeing the authored labels.
- Result: 398 / 398 questions identical (204 binary, 105 multiclass, 89 multilabel exact sets); 3 answers
  marked medium confidence (erout-019-q0, eurg-016-q1, emul-019-q0), all still matching. No overrides.
- What this does and does not show: the labels are internally consistent and reproducible under the written
  policy by an independent model instance. Both annotators are the same model family, so shared blind spots
  are possible. This is not human review; treat the set as "LLM-authored, LLM-verified, pending human review".
