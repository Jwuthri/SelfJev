# Prompt selection (validation splits only): `Qwen/Qwen3-4B-Instruct-2507`

data: data/hf.jsonl, data/eval.jsonl; n=868 questions; criterion: macro over families of (binary AUROC | multiclass accuracy | multilabel label-AUROC)

**Selected: `answer-v1`** (724795e9b666)

| prompt | sha | macro score | question acc (t=0.5) | eval_adversarial | eval_agent_output | eval_evidence | eval_multilabel | eval_policy | eval_routing | eval_urgency_sentiment | hf_emotions_multilabel | hf_intent_banking77 | hf_nli | hf_sentiment_tweets | hf_topic_agnews |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| answer-v1 | 724795e9b666 | 0.802 | 66.9 | 0.933 | 0.513 | 0.995 | 0.905 | 0.461 | 1.000 | 0.811 | 0.802 | 0.887 | 0.899 | 0.627 | 0.787 |
| task-v2 | 16961aedae12 | 0.788 | 65.9 | 0.933 | 0.470 | 0.958 | 0.923 | 0.322 | 1.000 | 0.783 | 0.808 | 0.880 | 0.910 | 0.673 | 0.793 |
| hybrid-v1 | b894703d500d | 0.783 | 65.8 | 0.933 | 0.480 | 0.947 | 0.928 | 0.308 | 0.950 | 0.783 | 0.810 | 0.880 | 0.911 | 0.673 | 0.793 |
| task-v1 | f7b8d8022dfb | 0.781 | 66.5 | 1.000 | 0.471 | 0.989 | 0.949 | 0.259 | 0.950 | 0.717 | 0.793 | 0.900 | 0.912 | 0.667 | 0.767 |
