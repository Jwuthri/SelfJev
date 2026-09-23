# Prompt selection (validation splits only)

data: data/hf.jsonl, data/eval.jsonl; n=868 questions; criterion: macro over families of (binary AUROC | multiclass accuracy | multilabel label-AUROC)

**Selected: `task-v1`** (f7b8d8022dfb)

| prompt | sha | macro score | question acc (t=0.5) | eval_adversarial | eval_agent_output | eval_evidence | eval_multilabel | eval_policy | eval_routing | eval_urgency_sentiment | hf_emotions_multilabel | hf_intent_banking77 | hf_nli | hf_sentiment_tweets | hf_topic_agnews |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| task-v1 | f7b8d8022dfb | 0.614 | 51.5 | 0.537 | 0.272 | 0.685 | 0.529 | 0.408 | 0.762 | 0.617 | 0.645 | 0.867 | 0.768 | 0.567 | 0.713 |
| task-v2 | 16961aedae12 | 0.609 | 53.0 | 0.637 | 0.309 | 0.693 | 0.283 | 0.419 | 0.700 | 0.617 | 0.673 | 0.887 | 0.800 | 0.560 | 0.733 |
| hybrid-v1 | b894703d500d | 0.605 | 52.0 | 0.604 | 0.272 | 0.726 | 0.283 | 0.439 | 0.700 | 0.617 | 0.673 | 0.887 | 0.768 | 0.560 | 0.733 |
| answer-v1 | 724795e9b666 | 0.597 | 52.5 | 0.522 | 0.291 | 0.715 | 0.508 | 0.467 | 0.700 | 0.462 | 0.600 | 0.873 | 0.769 | 0.487 | 0.773 |
