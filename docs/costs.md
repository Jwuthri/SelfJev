# Spend

Real costs logged in the [journal](JOURNAL.md#spend-so-far-real-cost-byok-upstream-included), BYOK upstream charges
included. About **$695 logged** over four days (09-22 to 09-25); a few GPU boxes (the early tree and custom-model runs,
the jina box ≈ $1.60, the latency/compact and T5Gemma L40S boxes) were not reconciled.

| item | cost |
|---|---|
| **Data** | |
| Round-3 training data: writing (Luna $10.17, Gemini $55.30, Grok $49.06) + Astra batch judge (upper bound at list batch prices) | ≈ $280 |
| Round-2 hard cases: writing $22.86 + blind Astra judge $36.24 + Jev second opinion $0.27 | $59.37 |
| eval2: writing, two judges, Jev second opinion | $32.72 |
| LLM-evaluation data ([llm_eval_data.md](llm_eval_data.md)): 9.4K training questions after safety passes (writing $37.09 + Astra $37.95) + `eval_llm` test set (writing $15.55, judges $5.76, Jev $0.03) | $96.38 |
| **Evaluation against Jev and GPT-6 Astra** | |
| Jev + GPT-6 Astra on the 3,471 dev-benchmark questions (Jev $0.06, Astra $19.27) | $19.34 |
| Jev on eval2 | $0.05 |
| Jev on every question of `data/all.jsonl.gz` (33,707 texts not cached) | $1.95 |
| `numdate_neg_v1`: 549 double-negation / number / date questions (Luna $0.28 + Astra $2.78 + Jev $0.02) | $3.08 |
| `mpos_distr_num_v1`: 3,645 several-correct / distractor / number questions (Luna $1.87 + Astra $17.80 + Jev $0.14) | $19.81 |
| `llm_multilabel_v1` multilabel batch: writing $26.60 + Astra judge $42.36 | $68.96 |
| Test-failure audit (Opus 5.5 relabel, 968 questions) | $4.92 |
| Jev predictions for `llm_multilabel_v1` | $0.30 |
| **AWS GPU** | |
| `qwen35_4b_combo`: Qwen3.5 + option lists + round 3, full sequences (L40S, 7.0 h) | ≈ $15.80 |
| `tree_4b_combo`: Qwen3 tree + option lists + round 3 (g5.xlarge, 11.7 h) | ≈ $11.70 |
| `qwen35_4b_tree`: Qwen3.5 trained with the tree, best model (L40S, 4.8 h) | ≈ $10.80 |
| `tree_4b_instruct_r3`: round-3 rerun (L40S) | ≈ $9.25 |
| `qwen35_4b_r2x64`: first Qwen3.5-4B run (g5.xlarge) | ≈ $4.75 |
| `tree_4b_combo_r2` and `tree_4b_combo_ptr` (2 g5.xlarge) | ≈ $6.22 |
| Qwen3.5 on vLLM: eval2 parity, latency sweep vs Jev, throughput (L40S, 50 min, + Jev $0.02) | ≈ $1.88 |
| First RLCD test: RLCD and a fine-tune control on fresh questions (L40S, 2.8 h) | ≈ $6.20 |
| Jev soft targets on all data: RLCD (L40S, 7.2 h) + fine-tune (L40S, 6.0 h) | ≈ $29.70 |
| Jev soft targets, C: RLCD with a confident-mistake cost from B (L40S, 7.1 h) | ≈ $15.90 |
| Retrain from scratch on everything with Jev targets, texts to 16K (L40S, 9.3 h) | ≈ $20.80 |
| 10 learning-curve runs, 8 g5.xlarge | ≈ $23.00 |
| All-options, 27B teacher and distillation boxes | ≈ $12.00 |
| Round-2 box: tree r2, stopped stock r2, tree r2b (g6e.4xlarge) | ≈ $6.70 |
| Round-3 training box (stopped) + scoring box | ≈ $6.25 |
| Stock 4B and 8B pipelines, one g6e.xlarge, 3.16 h | ≈ $5.89 |
| Combined levers: round-2b data + r64 / + MLP, 2 g5.xlarge | ≈ $5.26 |
| Instruct base + round-2 data + r64 | ≈ $2.45 |
| Tree LoRA-capacity ablation, 2 g5.xlarge | ≈ $1.60 |
| eval2 scoring box | ≈ $1.12 |
| Latency sweep vs Jev (AWS $0.87 + Jev $0.04) | ≈ $0.91 |

**Unit costs worth remembering:**

| what | cost |
|---|---|
| g5.xlarge (A10G 24 GB) | $1.006/h: one 4B LoRA on 10K questions ≈ 40 min; the dev benchmark ≈ 4 min |
| g6e.2xlarge (L40S 48 GB) | $2.242/h: `qwen35_4b_tree` (51.8K questions) trains in 4.1 h; eval2 through vLLM in 2 min |
| g6e.4xlarge (L40S 48 GB), us-east-2 | $3.00424/h |
| p5.4xlarge (H100) | $6.88/h (never obtained) |
| GPT-6 Luna as a data writer | ≈ $0.001 per text ($1.62 for 1,676 in round 2) |
| Gemini 3.8 Flash as a data writer | ≈ $0.014 per text; Grok 4.7 ≈ $0.026 (mandatory hidden reasoning) |
| GPT-6 Astra as a blind judge, OpenAI Batch API | ≈ $3.40–4.16 per 1,000 questions |
| Jev | $0.042 per million input tokens |

**Rules** ([AGENTS.md](../AGENTS.md)): paid resources need the user's explicit OK with a price, every time. AWS boxes
are tagged `Project=personal-jev`, get a `shutdown -h` cap with terminate-on-shutdown, and are terminated, with their
security group and key pair deleted, when done.
