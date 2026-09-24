# Spend

Real costs logged in the [journal](JOURNAL.md#spend-so-far-real-cost-byok-upstream-included), BYOK upstream charges
included. About **$457 logged** over three days; a few GPU boxes (the early tree and custom-model runs, the jina box
≈ $1.60, the latency/compact and T5Gemma L40S boxes) were not reconciled.

| item | cost |
|---|---|
| **Data** | |
| Round-3 training data: writing (Luna $10.17, Gemini $55.30, Grok $49.06) + Astra batch judge (upper bound at list batch prices) | ≈ $280 |
| Round-2 hard cases: writing $22.86 + blind Astra judge $36.24 + Jev second opinion $0.27 | $59.37 |
| eval2: writing, two judges, Jev second opinion | $32.72 |
| **Evaluation against Jev and GPT-6 Astra** | |
| Jev + GPT-6 Astra on the 3,471 dev-benchmark questions (Jev $0.06, Astra $19.27) | $19.34 |
| Jev on eval2 | $0.05 |
| **AWS GPU** | |
| 10 learning-curve runs, 8 g5.xlarge | ≈ $23.00 |
| All-options, 27B teacher and distillation boxes | ≈ $12.00 |
| Round-2 box: tree r2, stopped stock r2, tree r2b (g6e.4xlarge) | ≈ $6.70 |
| Round-3 training box (stopped) + scoring box | ≈ $6.25 |
| Stock 4B and 8B pipelines, one g6e.xlarge, 3.16 h | ≈ $5.89 |
| Combined levers: round-2b data + r64 / + MLP, 2 g5.xlarge | ≈ $5.26 |
| Instruct base + round-2 data + r64 (best model) | ≈ $2.45 |
| Tree LoRA-capacity ablation, 2 g5.xlarge | ≈ $1.60 |
| eval2 scoring box | ≈ $1.12 |
| Latency sweep vs Jev (AWS $0.87 + Jev $0.04) | ≈ $0.91 |

**Unit costs worth remembering:**

| what | cost |
|---|---|
| g5.xlarge (A10G 24 GB) | $1.006/h: one 4B LoRA on 10K questions ≈ 40 min; the dev benchmark ≈ 4 min |
| g6e.4xlarge (L40S 48 GB), us-east-2 | $3.00424/h |
| p5.4xlarge (H100) | $6.88/h (never obtained) |
| GPT-6 Luna as a data writer | ≈ $0.002 per 5 texts |
| Gemini 3.8 Flash as a data writer | ≈ $0.014 per text; Grok 4.7 costs 4× more (mandatory reasoning) |
| GPT-6 Astra as a blind judge, OpenAI Batch API | ≈ $3.40–4.16 per 1,000 questions |
| Jev | $0.042 per million input tokens |

**Rules** ([AGENTS.md](../AGENTS.md)): paid resources need the user's explicit OK with a price, every time. AWS boxes
are tagged `Project=personal-jev`, get a `shutdown -h` cap with terminate-on-shutdown, and are terminated, with their
security group and key pair deleted, when done.
