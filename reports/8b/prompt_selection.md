# Prompt selection (validation splits only): `Qwen/Qwen3-Reranker-8B`

data: data/hf.jsonl, data/eval.jsonl; n=868 questions; criterion: macro over families of (binary AUROC | multiclass accuracy | multilabel label-AUROC)

**Selected: `task-v1`** (f7b8d8022dfb)

| prompt | sha | macro score | question acc (t=0.5) | eval_adversarial | eval_agent_output | eval_evidence | eval_multilabel | eval_policy | eval_routing | eval_urgency_sentiment | hf_emotions_multilabel | hf_intent_banking77 | hf_nli | hf_sentiment_tweets | hf_topic_agnews |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| task-v1 | f7b8d8022dfb | 0.749 | 57.9 | 0.857 | 0.514 | 0.839 | 0.553 | 0.555 | 0.887 | 0.806 | 0.805 | 0.933 | 0.820 | 0.633 | 0.780 |
| task-v2 | 16961aedae12 | 0.745 | 57.9 | 0.963 | 0.528 | 0.786 | 0.544 | 0.512 | 0.938 | 0.700 | 0.779 | 0.907 | 0.845 | 0.667 | 0.767 |
| answer-v1 | 724795e9b666 | 0.737 | 57.1 | 0.896 | 0.534 | 0.812 | 0.786 | 0.414 | 0.875 | 0.648 | 0.718 | 0.913 | 0.812 | 0.607 | 0.827 |
| hybrid-v1 | b894703d500d | 0.729 | 56.9 | 0.846 | 0.519 | 0.802 | 0.546 | 0.555 | 0.887 | 0.672 | 0.778 | 0.907 | 0.819 | 0.647 | 0.767 |
