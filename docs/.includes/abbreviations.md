*[eval2]: Main benchmark: 1,991 frozen target-task questions, labels agreed by the author and two blind LLM judges. Never trained on. See Glossary.
*[dev benchmark]: The original 3,471-question test split (mostly public datasets), reused for many decisions. Caps out at 80–86%.
*[old test]: Same as the dev benchmark: the original 3,471-question test split.
*[round 1]: First training mix: 10,112 questions from public datasets + LLM-written synthetic questions.
*[round-1]: First training mix: 10,112 questions from public datasets + LLM-written synthetic questions.
*[R1]: Round-1 training data (10,112 questions).
*[round 2]: Round 1 + ~10K verified hard cases (LLM-written, kept only when a blind judge agreed).
*[round-2]: Round 1 + ~10K verified hard cases (LLM-written, kept only when a blind judge agreed).
*[round 2b]: Round 2 with 'none of the above' answers capped at 10%.
*[round-2b]: Round 2 with 'none of the above' answers capped at 10%.
*[r2b]: Round-2b data: round 2 with 'none of the above' answers capped at 10%.
*[round 3]: 38,628 more verified hard cases; its training run was stopped halfway.
*[round-3]: 38,628 more verified hard cases; its training run was stopped halfway.
*[r16]: LoRA rank 16 (the default adapter size).
*[r64]: LoRA rank 64: 4× the trainable weights of rank 16.
*[stock pairs]: The standard reranker setup: one sequence per (text, question, candidate), re-reading the text each time.
*[Instruct base]: Qwen3-4B-Instruct-2507 as the starting model, instead of Qwen3-Reranker-4B.
*[LoRA]: Small trainable adapter weights added to a frozen model; the only thing we train.
*[MLP]: LoRA also on the feed-forward (MLP) layers, not only on attention.
*[EM]: Exact match: the chosen set of labels is exactly right.
*[AUROC]: How well scores rank yes above no, ignoring the threshold (0.5 = chance, 1 = perfect).
*[ECE]: Expected calibration error: how far confidence is from actual accuracy. Lower is better.
*[Brier]: Mean squared error of the probabilities. Lower is better.
*[McNemar]: Paired significance test on the questions where exactly one of two models is right.
*[CLINC]: Public intent-classification dataset (held out), with an out-of-scope 'none' option.
*[vLLM]: Fast inference server; its prefix cache shares the text between questions.
*[A10G]: NVIDIA A10G 24 GB GPU (AWS g5), about $1/h.
*[L40S]: NVIDIA L40S 48 GB GPU (AWS g6e).
*[H100]: NVIDIA H100 GPU (AWS p5); never obtained here.
*[BYOK]: Bring your own key: OpenRouter bills the call to our own OpenAI/Google key.
*[KD]: Knowledge distillation: training on a teacher model's probabilities.
*[p50]: Median latency.
*[p95]: 95th-percentile latency.
*[held-out]: Never used in training: measures generalization to new tasks.
*[multi-positive]: Multilabel question with several correct labels.
