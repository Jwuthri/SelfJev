# SelfJev: four backbone experiments

Completed September 24, 2026 UTC · Connectly AWS · identical 3,471-question test set

**Your existing Qwen3 4B tree (R1) remains the strongest overall model in this screen. None of the four newly adapted backbones beats its test accuracy. The most immediately useful improvement is simpler: merging its LoRA weights reduces a short request from 114 ms to 81 ms, with nearly unchanged accuracy.**

The experiments support the shared-document approach as a practical way to reduce repeated computation. They do not yet demonstrate Jev-equivalent application quality or sub-100 ms latency across large workloads.

## The comparison

Raw accuracy uses the existing default decision rule. Calibrated accuracy uses temperatures fitted on the calibration split and thresholds fitted on validation. No checkpoint or calibration parameter was selected on test labels.

Latency is the median of 10 requests on an NVIDIA L40S, with warm weights and document computation repeated from scratch on every request. It includes tokenization and output construction, and excludes loading and network time. Each timing row repeats the same synthetic request; no document cache persists between requests. “16 × 3” means 16 questions, each with three candidates.

| Model / serving path | Raw accuracy | Calibrated | 512 tokens, 1 × 3 | 2K tokens, 16 × 3 |
|---|---:|---:|---:|---:|
| Existing Qwen3 4B tree (R1) | **81.59%** | 79.26% | 114 ms | 339 ms |
| Existing tree, merged LoRA | **81.50%** | 79.20% | **81 ms** | **297 ms** |
| Gemma 4 E2B tree | 79.69% | 80.03% | 130 ms | 348 ms |
| Qwen3.5-2B tree | 78.80% | 79.14% | 123 ms | 312 ms |
| GLiClass tree | 76.98% | 76.92% | **51 ms** | 1,065 ms |
| T5Gemma 2, shared encoder + cross-KV | 75.37% | 75.14% | 115 ms | **203 ms** |
| Jev, existing cached API reference | **82.71%** | — | Not compared | Not compared |

The main backbone screen uses unmerged LoRA. The merged existing tree is a separate serving optimization control. T5's ordinary shared-encoder path scores 75.31%; cross-KV reuse uses the same adapter, with tiny bf16 numerical differences. It is not a second training result. GLiClass was trained on A10G, then reevaluated and timed on L40S for the main comparison.

![Measured accuracy and latency](quality_latency.png)

[Complete tables](tables.md) include binary AUROC, multiclass accuracy, multilabel exact match, calibration, public held-out families, paired comparisons, every standard latency workload and the 16K/32K timings. [CSV](quality.csv) and [machine-readable results](comparison.json) are also saved.

## What each model taught us

**Qwen3.5-2B is a plausible candidate for longer documents, with a quality cost in this run.** The implementation shares the document's native attention cache and recurrent/convolution state, then forks independent candidate branches. At 8K tokens and 16 × 3 it takes 739 ms, versus 1,050 ms for the unmerged existing tree. At 32K and one question it takes 1.65 seconds, versus 4.37 seconds. Its 78.80% test accuracy is 2.79 percentage points below the existing tree. Those speed results justify further investigation, not replacing the current quality leader.

**Gemma 4 E2B has the best aggregate score among the new backbones.** It uses the pretrained text decoder with document-first cached branches and a direct yes/no readout. Its overall 79.69% still trails the existing tree. Its authored application score is 78.95%, versus 78.36% for the existing tree; policy accuracy is 14/22 versus 11/22. These small subsets are a reason to investigate particular errors, not sufficient evidence of a dependable application-quality win. This loader retains the conditional model's multimodal components, although inference here is text-only.

**T5Gemma 2 validates a useful execution idea, but its quality needs work.** It encodes the document once and lets the pretrained decoder score question/candidate branches. Preprojecting each decoder layer's document keys and values once reduces 2K / 16 × 3 from 398 to 203 ms, and 8K / 16 × 3 from 1,481 to 699 ms. Repeated projection was a measurable bottleneck. The current implementation runs out of memory at 32K / 16 × 3 on 48 GB: it materializes cross-KV for all 48 candidate rows. Bounded candidate batches or physical cache sharing are possible follow-ups; this OOM is an implementation limit, not an architectural impossibility. Its 75.37% accuracy does not make it the preferred model today.

**GLiClass wins the smallest latency workload, but scales poorly in this implementation.** Its 51 ms result becomes 451 ms at 2K tokens for one question. The experimental asymmetric bidirectional mask shares document processing while keeping each question/label block isolated. It retains GLiClass's pretrained encoder, projectors and scoring modules, but changes its normal attention pattern. The dense relative-attention implementation is not a sparse serving kernel. Contexts beyond 2K were not validated or benchmarked. A separate native-format, unfine-tuned control scored 58.86%; that control is not a claim about GLiClass's capability ceiling.

The older separate-encoder, cross-attention/probe + similarity + LoRA model scored **58.20%** in its saved FP32 test report. All four new adaptations are substantially stronger on the same test IDs. That historical comparison supports retaining pretrained interaction layers as a promising direction, but differences in backbones, training and precision prevent attributing the entire gain to one architectural choice. Its saved metrics are included in the complete tables; its older GPU timings are not mixed into the L40S comparison.

## Where this leaves the Jev comparison

Aggregate accuracy makes the gap appear smaller than it is on the application tasks. On the 171 authored application questions, Jev scores **94.74%**, the existing tree **78.36%**, and the new backbones range from **59.65% to 78.95%**. On agent-output questions, Jev gets 24/26 right; the existing tree and Gemma get 16/26. These samples are small, and the authored labels still need human review, but this is the gap to investigate next.

Your tree already removes a large amount of redundant computation: at 8K / 16 × 3, the existing pair-by-pair LoRA scorer takes **34.97 seconds**, while the existing tree takes **1.05 seconds**. That comparison uses different trained checkpoints, so it is not an identical-weights architecture ablation. Separate within-checkpoint sharing measurements are also saved; their repeated-document control runs questions serially and should not be mistaken for an optimized global-batch baseline.

Calibration does not erase the quality gap. For example, the existing tree's validation-F1 threshold policy lowers test question accuracy from 81.59% to 79.26%. Threshold selection optimizes a different objective and does not transfer perfectly across families. Both raw and calibrated results are shown rather than choosing whichever looks best on test.

## What I would do next

1. **Keep the existing 4B tree as the quality baseline and start serving work from the merged adapter.** The measured 81 ms short-request result is useful now. Next measure compilation/CUDA graphs, request batching and cache storage changes separately, with identical weights and correctness checks. None of those unmeasured optimizations is included in the numbers above.
2. **Keep Qwen3.5 as the longer-document candidate, and T5's cross-KV path as a useful design reference.** Their larger-workload timings justify a targeted next round. Benchmark bounded cache batches before treating the T5 OOM as a reason to reject the model.
3. **Spend the next quality effort on an independently held-out application set and better supervision.** Audit agent-output, policy, missing-evidence, contradiction and multi-step cases; compare teacher decisions and rationale-supported labels before increasing synthetic volume. The historical hard-case R2 run already shows that adding more data can reduce aggregate accuracy.
4. **Only then compare training recipes more extensively.** Match optimizer/batching choices, run multiple seeds, and test teacher distillation or longer adaptation on the strongest candidates. This screen used one short recipe per backbone and cannot establish their best achievable quality.

## Verification and limits

All four challengers used the same **10,080 training IDs**, identical data-file hashes, **978 selected validation questions**, one epoch, LoRA rank 16 and learning rate 2e-4. No question was excluded for length. Selected training steps were Qwen 600, Gemma 500, T5 700 and GLiClass 300, chosen by validation loss. Training-loop time was approximately 10–21 minutes per model, excluding setup, evaluation, benchmarks and correction reruns.

The experiment follows the repository's schemas, grouped losses, evaluator and calibration machinery, but it is not a fully matched architecture ablation against the historical tree. Batch size, checkpoint frequency, weight decay, candidate shuffling and LoRA targets differ; the synthetic source also has six fewer records than the older training run. Model-specific prompts and native computations differ. Corrected Gemma used an 8-vCPU host; the other L40S hosts had 16 vCPUs, which can affect eager execution and tokenization latency.

**An integration error was found and corrected:** an initial blanket bf16 cast rounded float32 rotary buffers. The final Qwen/Gemma results above use fresh `-nativeprecision` training runs that preserve those buffers. The earlier runs are retained only as an audit trail. T5's primary run and GLiClass were unaffected. This correction was driven by code inspection, not test-score selection.

The local checks passed **41 tests**. Actual-model FP32 checks covered shared/full execution and 1K document roots. Save/reload reproduced serving scores. On 64 validation questions, cached/full causal bf16 decisions agreed on 64/64 for Gemma and 63/64 for Qwen. The T5/GLiClass 64-question routine uses the same per-question path on both sides, so its agreement is not independent evidence of encoder/mask equivalence. Their separate multi-question checks, and T5’s native-versus-preprojected cross-KV check, provide the relevant execution comparisons. Qwen's one disagreement disappeared in FP32, with a maximum score difference of 0.00000763. These checks support cache correctness; they do not establish bit-exact bf16 equivalence on every input. [Artifact audit](audit.json) records the final hashes and completeness checks.

The test set has been used during earlier project development, so it is not a fresh blind benchmark. Public benchmark pretraining overlap is unknown. Paired p values are descriptive and unadjusted for multiple comparisons. Long-document measurements test latency and memory only, not long-document answer quality. Hosted Jev latency was not remeasured on matching hardware or workloads.

## Artifacts and AWS cleanup

**Estimated on-demand GPU compute: $13.40**, versus the authorized $1,000 ceiling. This is a launch-to-termination-request estimate, not an AWS bill; it excludes EBS, transfers, applicable AMI software charges and taxes. **All five experiment instances are confirmed terminated.** The three experiment security groups and three imported AWS key pairs have been deleted. All selected adapters and report artifacts were collected and hash-checked before shutdown.

The selected adapters are in `runs/challengers/{qwen35-nativeprecision,gemma4-nativeprecision,t5gemma2,gliclass}/adapter/`. Per-question predictions, calibration files, raw timing samples and serving checks are under `reports/challengers/`. The original project files and unrelated AWS instance were left untouched.

- [Protocol and execution notes](protocol.md)
- [Reproduction commands and script map](reproduce.md)
- [Complete result tables](tables.md)
- [Model and data audit](audit.json)
- [Resource closure and compute estimate](closure.json)
