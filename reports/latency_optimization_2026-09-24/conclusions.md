# Tree latency experiment: results and decision

Completed 24 September 2026 UTC. Qwen3-Reranker-4B, R1 LoRA initialization, dedicated AWS A10G.

**The useful general improvement is serving R1 with vLLM.** It cuts the representative 2,048-token / 16-question workload from about 967 ms to 700 ms with nearly unchanged aggregate development accuracy. The trained compact format reaches 648 ms, but its additional vLLM improvement is only 7.4%, and it introduces a clear over-rejection regression. Keep the compact adapter experimental.

| Stage | Outcome |
|---|---|
| 1. Optimize and validate the existing tree runtime | Complete: mask allocation improvement, numerical checks, profiling, BF16 merge comparison, vLLM prefix-reuse measurement and quality evaluation |
| 2. Train and evaluate a compact tree format | Complete: trained, selected by validation loss, evaluated on both datasets, benchmarked in HF and vLLM; did not pass the predeclared speed gate |
| 3. Compare faster GPUs | Blocked by AWS capacity; attempted L40S, H100, Blackwell and A100 hosts across three regions. No faster-GPU performance is claimed |

## What changed

Cached tree inference now constructs only the branch-to-branch mask. This avoids allocating a full square document mask, with exactly unchanged scores in the GPU comparison. Its measured speed effect is small; matrix multiplication and attention dominate this workload.

The vLLM backend uses the same logical scoring paths, merged BF16 weights, prefix caching, fused kernels and piecewise CUDA graphs. It records actual cache-hit counts instead of presenting the number of logical document roots as measured computation.

The compact format moves repeated instructions into the shared root and shortens each leaf's readout suffix. At 16 questions × 3 candidates, branch tokens fall from **2,119 to 1,303: 38.5% fewer**. The versioned format travels with the adapter and merged checkpoint, and mismatched formats raise an error.

Adaptation used **10,080 training questions**, initialized from R1, with 50% gold-label loss and 50% teacher-probability loss. Two epochs took **35.4 minutes** and 100 optimizer steps. Step **80** was selected by validation loss; neither development test labels nor the fresh challenge selected the checkpoint. Adapter reload reproduced scores exactly.

## Measured latency

The following are medians of ten measured repetitions, after warmup, on the same A10G. The model is resident. The request has **2,048 document tokens, 16 questions, and 3 candidate answers per question**. Network, model loading and compilation are excluded.

![Measured latency as the number of questions increases](/Users/julien/Documents/Repos/SelfJev/reports/latency_optimization_2026-09-24/latency_vs_questions.png)

| Implementation | New document / cold prefix |
|---|---:|
| Original R1 Transformers tree | 966.62 ms |
| R1 Transformers with branch-mask optimization | 960.63 ms |
| Compact Transformers tree | 743.50 ms |
| R1 vLLM, matched extended run | 700.37 ms |
| Compact vLLM | 648.49 ms |

Compact reduces Transformers latency by **22.6%**, but reduces matched vLLM latency by only **7.4%**. Its vLLM gain is smaller at long document lengths, where reading the document dominates.

| Cache situation, same request shape | R1 vLLM | Compact vLLM |
|---|---:|---:|
| New document | 700.37 ms | 648.49 ms |
| Document root already cached; new questions/candidates | 409.10 ms | 356.91 ms |
| Entire identical request repeated | 185.30 ms | 221.39 ms |

The document-warm figure excludes creation of that cache. Compact root-cache creation alone costs about **315.72 ms**. Repeating the whole request is a different workload and must not be advertised as new-question latency.

Shorter text can also align less favorably with cache blocks. On identical repeats, compact leaves **501 uncached positions**, versus **261** for R1. On cold requests, uncached positions fall only from **4,165 to 3,605**, a 13.4% reduction. These are measured engine counters; the cache-block alignment explanation is an inference consistent with the installed runtime's default 16-token blocks.

## Quality and limitations

| Evaluation | Questions | R1 merged HF | Compact merged HF |
|---|---:|---:|---:|
| Established development benchmark | 3,471 | 81.50% | 81.85% |
| Authored cases, a subset of that benchmark | 171 | 78.36% | 78.95% |
| Entirely held-out public families, another subset | 1,800 | 83.78% | 83.67% |
| Fresh generated challenge | 720 | 95.42% | 95.42% |
| Policy questions within that fresh challenge | 120 | 72.50% | 72.50% |

The overall compact change is 66 gains versus 54 losses. Its paired source-cluster bootstrap interval is **−0.29 to +0.98 percentage points**, so the small aggregate gain is not established statistically. Quality changes combine format adaptation, continued training and teacher supervision; this run does not isolate those contributions.

Two findings matter more than the headline:

- **CLINC intent accuracy falls from 94.67% to 91.67%.** All nine changed decisions reject a correct intent as `none`; there are no gains on that family. For example, “am i eligible for a new credit card” changes from `new_card` to `none`.
- **Numerical policy conditions remain weak.** All 33 fresh-challenge errors occur in its policy questions. With identity verified but an expense above the permitted limit, both models answer correctly on only 10 of 35 records. The high overall challenge score hides this failure.

Compact vLLM also scores **81.85%** overall. It changes 12 decisions relative to compact HF, with four gains and four losses. Backend agreement is approximate, not bitwise. R1 vLLM scores **81.53%**, compared with merged HF's 81.50%.

BF16 merging itself has a small measured precision cost: unmerged R1 scores **81.68%**, versus merged R1's **81.50%**, with six net fewer correct answers. The latency comparisons above use merged weights. These are measured deployment tradeoffs, not claims of exact numerical equivalence.

The established benchmark has informed development. Authored labels lack human review. The fresh challenge has mechanically verified labels but narrow template coverage. These results do not establish a match to Jev across tasks, hardware or API latency.

## Decision

The predeclared gate required at least **15% lower cold-prefix vLLM latency** at the representative workload, alongside aggregate quality limits. The quality point-estimate gates pass; the speed gate fails. The CLINC regression is an additional reason to keep compact optional.

Use R1 + vLLM as the current general serving option. Retain the branch-mask improvement and the experimental compact adapter. The next quality work should address positive intents being rejected as `none` and explicit numerical policy conditions, using training/validation data rather than tuning thresholds on these test outcomes. A faster-GPU comparison remains necessary to quantify the hardware benefit.

## Evidence and reproduction

Code, reports and trained adapters are now in the original repository `/Users/julien/Documents/Repos/SelfJev` on `master`, as uncommitted changes. The compact adapter is available at `runs/tree_4b_compact_v2/adapter`. The code was reconciled with the newer original checkout; concurrent edits and the other experiment’s checkout were preserved.

A second copy of the trained adapter, intermediate checkpoints and training metadata is saved under `runs/latency_optimization_2026-09-24/tree_4b_compact_v2`, with exact dataset snapshots beside it in `frozen_data`. A verified snapshot of the former worktree and its Git history is retained under `runs/latency_optimization_2026-09-24/integration_archive`; historical source paths in the raw experiment records remain unchanged for provenance.

- [Complete result tables](results.md): all 12 workload shapes, output-type metrics and family changes.
- [Experiment record](README.md) and `events.jsonl`: decisions, failures, intermediate scores and provenance.
- [Reproduction instructions](reproduce.md): environments and commands.
- `acceptance.json`: explicit gate results.
- `compact_development_comparison.json`, `compact_fresh_comparison.json`, `clinc_regressions.json`, and `challenge_audit.json`: paired changes and diagnostic cases.
- Raw benchmark JSON files: every measured repetition, score and cache count. `cloud_logs/` and the compressed profiler trace preserve execution evidence.
- `runs/tree_4b_compact_v2/adapter`: the trained adapter; SHA-256 `0b51c5c717b44e0c85a6aae5d98899d128917add7a31448ea21a9ef5ab787a60`.

Validation includes **58 focused tests** (two separate real-model tests excluded), GPU mask equivalence on **104 R1 requests and 104 compact requests**, full evaluations, and an exact adapter reload check. **34 downloaded data/model/result artifacts were checked against remote SHA-256 hashes with no mismatches.** Intermediate selected adapters are preserved locally. The derived merged base-weight copy can be regenerated from the pinned base model and saved adapter; it is not needed to preserve the trained result.

Cloud cleanup: the experiment GPU instance is **terminated**; its temporary security groups and imported AWS keys are deleted, and no experiment instances remain active in any of the three regions. The root disk is in AWS’s automatic **deleting** state at the last check. `cleanup.json` records this remaining asynchronous transition.
