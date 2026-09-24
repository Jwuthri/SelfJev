# Tree latency and compact-format experiment

**Start with [the final conclusions](conclusions.md) and [result tables](results.md).** The entries below retain the chronological protocol and findings, including intermediate results that were pending at the time.

Started 2026-09-24 UTC. Owner: this Codex task. User authorized AWS GPU provisioning, stages 1 and 2, and a subsequent hardware comparison. Other model experiments run separately; their instances, outputs, and checkout are not modified.

## Questions and protocol

1. Preserve the first-round Qwen3-Reranker-4B tree checkpoint while removing inference overhead. Compare the original cached implementation, direct branch-mask construction, and vLLM on the same GPU. Merge LoRA for deployment; explicitly check numerical and decision changes.
2. Adapt that checkpoint to a compact, versioned tree format. Keep document sharing, question isolation, yes/no readout, and overlength errors. Select checkpoints using validation loss only. Preserve labels and candidate ordering for teacher supervision. Report quality and speed even if the compact experiment fails.
3. Only after the software/format comparison, repeat the chosen configuration on faster hardware.

Latency protocol: model resident; separate previously unseen document requests from exact-prefix reuse; 1/4/16 questions, 3 options, short/512/2048/8192-token documents. Record all repetitions, token counts, hardware, package versions, model/adapter/code/data hashes. GPU timing is distinguished from CPU preparation and client/network time. Benchmark one job at a time per GPU. Confirm actual vLLM cache/computation counters rather than treating logical tree counts as measured work.

Correctness: standalone versus tree scores, unequal-length batching, question/candidate permutation, unrelated-question isolation, reload, and no truncation. BF16 backend comparisons report score/probability errors and decision flips; exact FP32 CPU equivalence is checked separately.

Quality: existing benchmark is a development comparison because it has informed earlier decisions. A fresh programmatically labeled challenge set will test negation, missing evidence, explicit rules, rejection and independent questions with source/template separation from training. It is narrow coverage, not a substitute for human-reviewed generalization. Test labels will not choose a checkpoint or thresholds.

## Original execution provenance

The branch/worktree below describe where the experiment originally ran. Its code, reports and trained artifacts have now been integrated into the original `master` checkout at the user’s request. See `integration.json` for the migration record; use the original repository for all commands.

- Branch: `codex/tree-latency-compact`.
- Worktree: `/Users/julien/.codex/worktrees/selfjev-tree-latency/SelfJev`.
- Source checkout: `/Users/julien/Documents/Repos/SelfJev`.
- Current source, scripts, tests, configs and data were copied as an experiment snapshot, including existing uncommitted merge/vLLM work. Original tree, trainer and vLLM sources are saved under `baseline_source/` for matched comparisons. No claim that all these baseline changes were authored by this task.
- Reference adapter: `runs/tree_4b/adapter`; hashes and copied data hashes are in `manifest.json`.
- Cloud resources created by this task will be individually recorded and stopped/terminated after outputs are retrieved; existing project instances are left alone.

## Findings and event log

- Initial inspection: a vLLM wrapper exists, but no vLLM results are recorded in the original `reports/latency`. Its `state_sequences` metadata counts input trees rather than engine computations.
- Original cached inference creates a full square tree mask and discards document rows. The direct branch mask can preserve semantics while eliminating this allocation.
- Existing 16×3 benchmark: 2,119 branch tokens, including 528 question-template and 480 candidate-template tokens. Token reduction does not imply proportional latency reduction.

Further significant actions, failed attempts, and measured results are appended to `events.jsonl` and summarized here. Raw evidence lives alongside this file.

### Initial measured results

GPU parity: 104 requests, maximum absolute score difference **0.0** between original and direct branch-mask execution. Local focused regression suite: **58 passed**, two real-model/training tests excluded (GPU parity covers the 4B inference path).

On the dedicated A10G, merged BF16, 2,048 tokens × 16 questions × 3 options: original median **966.62 ms**, optimized **960.63 ms** (ten measured repetitions after two warmups). This small difference does not establish a material speedup. The allocation improvement is useful, but was not the main bottleneck at these lengths. A profile attributes about **396 ms** to root forward and **562 ms** to branch forward; about **542 ms** of matrix multiplication and **172 ms** of branch attention sit inside those ranges, not in addition to them.

Compact format `tree-compact-v2` changes the benchmark branches from **2,119 to 1,303 tokens** (38.5% fewer) and the 512-token root from 555 to 547 tokens. Quality is pending training; token savings are not a latency forecast. The compact adapter records the complete format and hash so inference cannot silently use the wrong template.

The new challenge is frozen at 120 source records / 720 questions; labels follow explicit generated records and rules. SHA-256: `62e8496880e6577436ffd58bd079a3cb7b7870b29a55bb2af760550c43fec20e`.

### BF16 adapter merging quality check

On the same GPU and evaluation batching, R1 unmerged scored **81.6768%** and merged scored **81.5039%** on 3,471 development questions. There were **12 changed decisions**, including 2 newly correct and 8 newly incorrect (6 net fewer correct). Mean absolute score difference was 0.02950; maximum 0.32784. `merge_comparison.json` records the affected IDs. This is a speed/precision tradeoff; merging is not bitwise-equivalent in BF16. These runs also differ slightly from the historical 81.59% score because the evaluation batch configuration differs; the adapter hash is unchanged.

### vLLM measurements

vLLM 0.30.0 uses Torch 2.13.0+cu130; the HF path uses Torch 2.14.0+cu130. Both use the same merged BF16 checkpoint. vLLM uses FlashAttention 2 and piecewise CUDA graphs (full graphs are unsupported for this pooling runner).

For 2,048 tokens × 16 questions × 3 options, cold-prefix median is **696.93 ms** versus HF **960.63 ms**. Repeating the **entire identical request**, including questions/candidates, takes **186.22 ms**. This latter figure must not be presented as the latency of new questions on a cached document. The cold call submits 103,941 path tokens and reports 99,776 cached tokens: 4,165 uncached prompt positions, demonstrating substantial within-request prefix reuse after an explicit cache clear. The logical HF tree has 4,210 positions; vLLM can additionally share identical question-prefix tokens across questions.

Maximum raw-score difference over the parity requests is **0.17397**; full development-set decision agreement is reported below. The 12 timing cells and individual scores/cache counts are saved in `vllm_a10g.json`.

### Phase 1 complete; phase 2 started

vLLM development accuracy: **81.5327%**, versus merged HF **81.5039%**. It changes **14** decisions (6 newly correct, 5 newly incorrect). Raw numerical differences are recorded in `vllm_quality_comparison.json`; this is not bitwise equivalence. No aggregate quality loss is observed in this development comparison.

Phase 2 now computes teacher probabilities for **10,080 training questions only**, then continues the R1 adapter in compact format for two epochs. The loss is 50% gold supervision and 50% teacher soft-target cross entropy, with candidates aligned through permutation. Validation loss chooses the checkpoint. The fresh challenge is evaluated only after that choice.

### Training hardware fallback

Teacher scores for all 10,080 selected training questions are saved with candidate IDs and data/model hashes. Six L40S launch requests (g6e.2xlarge in zones a–d, g6e.4xlarge in a, g6e.xlarge in b) failed with insufficient capacity. Stage 2 training proceeds on the dedicated A10G; no other task’s machine is used.

### Acceptance criteria, fixed before compact test evaluation

The compact format is an experiment, not the new default. The engineering gate is at least 15% lower A10G cold-prefix latency at 2,048 document tokens / 16 questions / 3 candidates, with no more than 0.5 percentage points of overall development accuracy loss, 2 points on authored cases, or 2 points on the fresh challenge versus the merged R1 reference. These are point-estimate tolerances, not a statistical proof of non-inferiority. Report paired source-cluster bootstrap uncertainty and all family changes; do not tune on the fresh challenge. If the gate fails, retain R1 plus the validated runtime improvements.

The synthetic timing workload uses similar question templates and candidate descriptions. It establishes scaling for those token shapes; it is not a production traffic trace. Cache modes are reported separately: unseen prefix, entire identical request, and (in the extended benchmark) only the document root cached.

The paired source-cluster bootstrap (10,000 replicates, fixed seed) for vLLM versus merged HF gives an accuracy difference of +0.0288 percentage points, with a 95% interval of [-0.172, 0.230] points. Questions from a shared source are resampled together. This supports a small backend effect on this development set; it does not validate new tasks.

### Cloud capacity findings

Additional launches of L40S, H100 and RTX PRO Server 6000/Blackwell hosts in us-east-1, us-west-2 and us-east-2 have not succeeded. Attempts include automatic availability-zone selection and larger multi-GPU shapes. Most fail with `InsufficientInstanceCapacity`; the Ohio g6e.12xlarge request fails with a 64-vCPU regional quota limit. Request/result files and timestamped events retain each response. The original dedicated A10G remains the only active compute resource created by this task. Faster-hardware measurements must not be claimed without an actual successful launch and matched benchmark.

Teacher agreement with gold on the selected training subset is **83.125%** (8,379 / 10,080): binary 95.55%, multiclass 87.83%, multilabel exact match 57.75%. This is a training-data diagnostic, not a held-out quality claim. Per-family counts are saved in `teacher_training_agreement.json`. Teacher targets supplement gold labels rather than replacing them.

### Compact validation checkpoint, step 40

On the same 978 validation questions, compact accuracy increases from **79.04% before adaptation to 81.39% at step 40**; gold-label loss falls from 0.363010 to 0.310160. Binary accuracy is 93.12%, multiclass 85.96%, multilabel exact match 55.39%. These are validation results, not test results; the two-epoch run continues as planned. A copy of this intermediate best adapter is preserved for reproducibility, not test-based checkpoint selection.

All **720 fresh-challenge labels** were checked against the serialized state text using a separate parser. Data SHA-256 remains unchanged. The challenge is unbalanced: policy permits reimbursement in 26 / 120 records; manager status is approved in 47, rejected in 34, unmentioned in 39. Diagnostic slices distinguish these cases and exact policy boundaries (`challenge_audit.json`). This confirms label/text consistency, not broad task coverage or human review.

At **step 80**, validation loss improves to **0.307906** and accuracy to **81.5951%** on the same 978 questions. Binary accuracy remains 93.12%, multiclass improves to 86.34%, multilabel exact match remains 55.39%. This replaces step 40 as the validation-selected checkpoint; final training evaluation is still pending.

Authored development cases are exactly the **171 test rows in `data/eval.jsonl`** (`eval_*` families), verified by ID equality. Public held-out families (`heldout_*`) are not authored cases.

Interpretation: the compact candidate combines a shorter format, continuation training, and teacher supervision. Its quality difference against frozen R1 measures that combined change; it does not isolate the separate contribution of each component. The current frozen training file also differs from the file recorded in historical R1 training; hashes are preserved in `manifest.json` and training metadata.

### Compact training complete

Two complete epochs used **100 optimizer steps**, versus the pre-run packing estimate of 102. Length-bucketed batch counts vary with shuffle; this was normal end-of-data completion, not early stopping. Wall time was **35.41 minutes**. Step **80** was selected by lowest validation loss (0.307906); final step 100 loss was 0.310523. The 64-question adapter reload check had **maximum score difference 0.0**. Selected adapter SHA-256: `0b51c5c717b44e0c85a6aae5d98899d128917add7a31448ea21a9ef5ab787a60`. Development and fresh challenge evaluation began only after this selection.

### Compact quality and first timing results

Merged HF compact accuracy is **81.8496%**, versus **81.5039%** for merged R1: 66 newly correct, 54 newly incorrect, 12 net additional correct over 3,471 questions. The paired source-cluster 95% interval for the difference is **−0.286 to +0.979 percentage points**, so this does not establish an accuracy improvement. Authored cases are **78.9474% vs 78.3626%** (135 vs 134 / 171). The six public held-out families together are **83.6667% vs 83.7778%**.

The frozen challenge is **95.4167% for both models** (687 / 720), with one gain and one loss. This high aggregate hides a clear weakness: all 33 errors are in the 120 policy questions (**72.5%** accuracy). When identity is verified but the expense exceeds the limit, both models get only **10 / 35** correct. For verified, within-limit requests they get **18 / 26** correct. Missing approval, explicit rejection, delivery negation, team selection, and none-of-the-above are perfect on this narrow generated set. No claim of general reasoning quality follows from this challenge.

CLINC intent accuracy falls from **94.67% to 91.67%** (9 fewer correct / 300), while SST-2 rises from **83.67% to 87.67%** (12 more / 300). Family-level results and paired changes are retained; the aggregate score must not hide the intent regression.

On A10G, compact HF at 2,048 document tokens / 16 questions / 3 candidates takes **743.50 ms** versus optimized R1 **960.63 ms**: **22.6% lower latency**. At 512 tokens / 16 questions, **414.05 vs 607.39 ms**: **31.8% lower**. These are same-stack comparisons; the final matched vLLM measurements are pending.

CLINC diagnosis: **all 9 changed decisions are regressions from the correct intent to `none`; there are no CLINC gains**. This is a specific over-rejection failure, not a uniform decline across labels. Example: “am i eligible for a new credit card” changes from `new_card` to `none`. Raw score margins and all cases are saved in `clinc_regressions.json`. The descriptive source-bootstrap interval is −5.00 to −1.33 percentage points (not adjusted for examining multiple families). The observed pattern motivates a separate training/validation study of rejection calibration; no test-based threshold correction is applied here.

Compact GPU mask equivalence also passes: **104 requests, maximum raw-score difference 0.0** between the original square-mask and optimized branch-mask implementations using the selected compact adapter. This is separate from HF/vLLM numerical agreement, which uses different kernels and a converted scoring head.

### Cache granularity finding

At 2,048 tokens / 16 questions, compact vLLM reports **3,605 uncached prompt tokens** on a cold-prefix call, versus R1’s 4,165 in the original run: only **13.4% fewer actual uncached positions**, despite 38.5% fewer logical branch tokens. The compact logical tree has 3,386 tokens versus 4,210 total for R1.

On an identical-request repeat, compact reports **501 uncached positions** versus **261** for R1, and is slower in these initial timings (221.39 vs 186.22 ms). This is consistent with changed alignment at cache-block boundaries; the installed runtime defaults to 16-token blocks. A shorter prompt does not guarantee fewer uncached tail tokens. The raw counts are measured; the alignment explanation is an inference.

The compact document-warm measurement is **356.91 ms** after caching only the root; the excluded root-cache creation costs a median **315.72 ms**. This correctly distinguishes new questions about a cached document from repeating all questions and candidates.

### Compact vLLM quality complete

Compact vLLM scores **81.8496%** on the 3,471-question development set, exactly the same aggregate as compact HF. There are **12 changed decisions**, including 4 gains and 4 losses. Mean absolute raw-score difference is **0.02826**, maximum **0.32209**; this remains approximate numerical agreement, not bitwise equivalence. `compact_vllm_backend_comparison.json` records paired results.

### Final decision and preservation

Stages 1 and 2 are complete. The matched compact vLLM speed gain is **7.407%** (700.365 → 648.489 ms at 2,048 tokens / 16 questions / 3 candidates), below the 15% gate; aggregate quality point-estimate gates pass, but the CLINC over-rejection regression remains. The compact adapter stays experimental. Stage 3 could not obtain faster AWS capacity. All 34 critical remote/local artifact hashes match. Model checkpoints and exact datasets are backed up inside the original repository under `runs/latency_optimization_2026-09-24`, independently of the temporary worktree.

Cloud instance `i-0172e64b9d0dc20ac` is terminated. All experiment SSH groups and imported AWS keys are deleted. No experiment instances remain active. The automatically deleted root volume was still in `deleting` state at the last check; see `cleanup.json`. Other tasks’ resources were left untouched.
