# T5Gemma 2 on matched round-2b data

Status: **correcting and rerunning the intended full encoder–decoder adaptation**, 24 September 2026 UTC. An implementation audit found that the first pilot targeted only decoder LoRA: the encoder filter missed the native `encoder.text_model` path. Its 73.84% development / 76.80% eval2 scores and 266.61 ms primary latency belong to that decoder-only run. They are preserved in [decoder_only_audit](decoder_only_audit/README.md) and are not a result for the intended full adaptation. The corrected run is `runs/t5gemma2_r2b_full`; it uses identical frozen data and recipe, explicit adapter coverage of both text stacks, and separate first-step gradient checks. No corrected quality result is available yet.

The historical T5 rescore is valid: all 3,471 decisions reproduce the old report (75.37% development); eval2 is 72.98%. Tree round-2b's existing eval2 report is 90.56%; dedicated same-L40S tree controls remain pending.

## Why this experiment exists

The user correctly remembered a completed T5Gemma experiment. It lives in `/Users/julien/.codex/worktrees/1d33/SelfJev`, outside the original checkout. The preceding architecture recommendation missed it. That experiment already used the complete pretrained encoder, decoder, full document memory and preprojected cross-attention keys/values. Its 3,471-question development accuracy was 75.37%, versus the R1 tree's 81.50%; its L40S 2,048-token × 16-question × 3-candidate median was 203 ms versus the merged tree's 297 ms. That was not a successful speed/accuracy replacement. Historical evidence and source hashes are preserved in `prior_run/` and `prior_provenance.json`.

This follow-up changes the training data to exactly the historical round-2b eligible question IDs and bounds decoder cache memory. It is not a previously untried architecture.

## Frozen protocol

- Model: `google/t5gemma-2-1b-1b`, revision `dd0a2683227859151b1730ca3a63087df5b5f39b`. Fresh pretrained initialization, complete text encoder/decoder; original challenger's token format and native yes/no readout. No new probe, memory compression or token pruning.
- Training: exactly 16,375 training and 1,388 validation questions selected by the historical Qwen round-2b tokenizer, length rule, sampling and seed. All source hashes match the original run. Expanded examples and exact IDs/hashes are frozen in `selection.json` and `runs/t5_round2b_inputs/`. T5-specific eligibility checks reject any further exclusions; maximum combined lengths are 8,375 train and 8,630 validation tokens, with a 16,384 training limit.
- One epoch, seed 13, attention LoRA rank 16 / alpha 32 / dropout 0.05, q/k/v/o on encoder and decoder text layers, LR 0.0002, weight decay zero, gradient clipping 1. Checkpoints selected exclusively by minimum validation loss, including initialization, every 50 steps and at the end. No test-driven checkpoint, prompt, threshold or temperature selection.
- The older T5 R1 run had 823 optimizer updates; this matched-R2b pilot has 228 larger updates. New-versus-old T5 therefore changes training recipe as well as data, and does not isolate the effect of adding round-2 examples.
- Same eligible questions and epoch exposure as round-2b, but NOT a fully controlled architecture-only ablation: tokenizer, prompt format, optimizer grouping (72 questions/step, 228 steps versus 225 packed Qwen steps), and parameterization differ. This is a bounded first pilot, not a hyperparameter search or proof of an architectural ceiling.
- Original round-2b control adapter SHA256: `2a73e5f707e9d8bfdcad440d5c7c66f106f9cb3b0028851dfb5b6a3bf3f0ad86`. Inference controls: unmerged Hugging Face tree, merged Hugging Face tree, merged vLLM tree. T5: historical R1 adapter, new R2b adapter, optional merged R2b adapter.
- Quality: existing 3,471-question development benchmark plus 1,991-question eval2, with whole-question accuracy, per-type/family results and paired comparisons. Eval2 is the primary current-task screen. Both datasets have informed research decisions; neither is a fresh final confirmation set. Authored/LLM-reviewed labels are not human ground truth.
- Proposed screening gate: at least 2× lower p50 latency at 2,048 text tokens × 16 questions × 3 candidates and no more than 1 percentage-point overall accuracy loss on eval2. Compare with the fastest measured matched round-2b implementation, not an intentionally slow control. Report confidence intervals and important family losses; a point-estimate pass alone would require fresh confirmation before a replacement claim.
- Serving-only treatments fixed before quality results (decoder-prefix reuse added during training, before any new evaluation score was observed): T5 merged BF16 with 16 versus 48 branches per decoder batch, plus common decoder-prefix reuse with 48 branches; vLLM tree BF16 versus online FP8 quantization supported by the installed vLLM 0.30.0/L40S stack. Both receive full quality and latency evaluation, without tuning thresholds on evaluation labels.
- Latency: one dedicated NVIDIA L40S, resident models, identical request bytes frozen in `latency_requests.json`. 100 varied requests in the primary cell, 20 in each additional cell; two warmups/cell; synchronized wall-clock p50/p95, raw samples and actual model tokenizer lengths. New document prefixes; reset vLLM prefix cache between requests outside the timer. Include request parsing/tokenization and model inference, exclude loading and network. These are local model measurements, not Jev service latency. Synthetic decision outcomes are a benchmark diagnostic, not a quality dataset.

## Implementation and checks

`src/personal_jev/t5_shared.py` encodes each distinct document once, projects document keys/values once per decoder layer, and feeds independent branches in bounded batches (16 initially). Expanded cross-cache tensors are views; native attention still constructs merged self/cross tensors per layer. This reduces persistent cache copying, not branch arithmetic, and is not a specialized shared-KV attention kernel.

The earlier local checks passed (two real-model integration tests excluded from this CPU regression run), including a real tiny T5 decoder, independent-vs-shared scoring, distinct-document isolation, cache storage scaling and gradients through the full encoder/decoder. Full-model FP32 independent/shared/permuted inference differs by at most 0.000014 on 64/1,024-token inputs (`actual_fp32_checks.json`). The original smoke test failed to detect the decoder-only adapter scope. A new real native full-model unit test now checks both PEFT target coverage and nonzero gradients; the corrected GPU smoke test is running. The complete run rechecks the selected adapter after reload.

## Cloud and reproducibility

User authorized GPU provisioning in the conversation. Dedicated `g6e.4xlarge` L40S in Ohio, instance `i-087b024b35cff657b`, launched 06:37:50 UTC. Quoted compute rate $3.00424/hour; 200 GB encrypted gp3, delete on termination. Eight-hour OS shutdown cap, terminate on shutdown, scheduled for 14:38:54 UTC. Virginia had insufficient capacity; no instance was launched there. Its temporary security group/key pair have been removed. Final wall time, cost estimate and cleanup evidence will be recorded.

Raw configuration, training logs, checkpoints, data hashes, predictions and timing samples will be retained locally. All work stays on original `master`, without commits or new branches.

Data audit: zero overlapping question IDs, nonempty source IDs or exact document texts between the frozen training and validation splits (`data_audit.json`). Ohio pricing was independently verified from AWS Pricing (`pricing_ohio.json`).

## Interpreting a possible quality shortfall

Google describes this checkpoint as a pretrained Gemma-to-encoder–decoder adaptation using UL2, rather than a reranker checkpoint ([model card](https://huggingface.co/google/t5gemma-2-1b-1b)). A classification adaptation therefore starts from a different objective and parameterization than Qwen3-Reranker. If this pilot underperforms, insufficient task adaptation, the inherited question/candidate format, and model capacity remain competing hypotheses. This one recipe cannot attribute the result to any one of them, or show that encoder–decoder architectures cannot work. Full-text reader retention and successful equivalence/gradient checks address specific implementation concerns, not achievable quality ceilings.

The decoder-prefix treatment reuses a native common-prefix self-cache and its document cross-cache. Each branch gets an independent copy of the small self-cache while cross-cache tensors remain views. A tiny real-decoder check covers a prefix longer than the sliding window, unequal branches, distinct documents and reordered questions. Actual-model FP32 and trained-BF16 validation checks run before this treatment is evaluated.

## Hardware follow-up and correction provenance

H100 (`p5.4xlarge`, $6.88/hour) launch attempts failed with insufficient capacity in all three Ohio zones; no H100 instance was launched (`h100_cloud.json`). The corrected training therefore runs on the existing L40S, followed by sequential controls on that same GPU. Hardware acceleration remains unmeasured. The initial decoder-only adapter and all raw reports are retained; its comparison with the historical T5 also changes adapter scope and cannot isolate a data effect. The correction was discovered after evaluation, and is reported openly rather than presenting the rerun as a previously unseen test.
