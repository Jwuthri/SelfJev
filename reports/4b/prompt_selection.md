# Prompt selection (validation splits only): `Qwen/Qwen3-Reranker-4B`

data: data/hf.jsonl, data/eval.jsonl; n=868 questions; criterion: macro over families of (binary AUROC | multiclass accuracy | multilabel label-AUROC)

**Selected: `answer-v1`** (724795e9b666)

| prompt | sha | macro score | question acc (t=0.5) | eval_adversarial | eval_agent_output | eval_evidence | eval_multilabel | eval_policy | eval_routing | eval_urgency_sentiment | hf_emotions_multilabel | hf_intent_banking77 | hf_nli | hf_sentiment_tweets | hf_topic_agnews |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| answer-v1 | 724795e9b666 | 0.707 | 54.4 | 0.693 | 0.494 | 0.762 | 0.541 | 0.544 | 1.000 | 0.700 | 0.690 | 0.920 | 0.781 | 0.553 | 0.807 |
| task-v1 | f7b8d8022dfb | 0.703 | 55.4 | 0.800 | 0.515 | 0.762 | 0.572 | 0.266 | 0.938 | 0.778 | 0.693 | 0.913 | 0.781 | 0.613 | 0.807 |
| hybrid-v1 | b894703d500d | 0.697 | 55.8 | 0.800 | 0.381 | 0.736 | 0.568 | 0.296 | 0.938 | 0.845 | 0.684 | 0.933 | 0.781 | 0.620 | 0.787 |
| task-v2 | 16961aedae12 | 0.684 | 56.3 | 0.833 | 0.317 | 0.714 | 0.565 | 0.245 | 0.887 | 0.803 | 0.684 | 0.933 | 0.826 | 0.613 | 0.787 |
