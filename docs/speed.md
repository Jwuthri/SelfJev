# Speed and cost

!!! abstract "Bottom line"
    - **Sharing the text is the big win.** The shared-prefix tree is 32–37× faster than stock pairs for 16 questions ×
      3 candidates on 8K–16K-token texts, at the same quality.
    - **Jev is flat at ~150 ms**, from 8 to 4,096 tokens and 1 to 16 questions. Our Qwen3 tree 4B on one A10G matches
      it only for short texts with one question and is 5× slower at 4,096 tokens. **On one H100 the same model is faster
      than Jev inside the machine** at every size with one question (22 vs 110 ms server-side for short texts, 82 vs
      122 ms at 4,096 tokens) and with 16 questions up to 2,048 tokens (4,096 × 16: 189 vs 134 ms); the remaining
      end-to-end gap is network distance. FP8 adds nothing.
    - **Serving:** for an attention model, vLLM with the prefix cache and merged weights is the best general option. A
      shorter "compact" tree format did not pay off.
    - **Cost:** a fully busy A10G is cheaper per request than Jev (up to 3×, less with many questions); an idle one is
      not. On an L40S the Qwen3 tree on vLLM is cheaper than Jev in every cell measured.
    - **The default model, `selfjev-4b`, on its own engine (`TreeServer`, 2026-09-30): extra questions on one text are
      nearly free.** From 1 to 50 questions, memory grows by at most 1.4 GiB and latency by 1.3–6.1×; a 24 GB A10G holds
      a 32K-token text with 50 questions ([below](#many-questions-on-one-text-2026-09-30)). The Jev comparisons above
      are the older Qwen3 tree's (`tree_4b_combo`, weights at tag `archive/pre-cleanup-2026-09-27`); the current model
      has not been timed against Jev. On vLLM the Qwen3.5 architecture is fast for one question but slow for many
      (it reuses the recurrent state only every 528 tokens), which is why `selfjev serve` uses `TreeServer`. A separate
      Apple M5 Pro MPS experiment is reported below.

## Many questions on one text (2026-09-30)

`selfjev-4b` (`weights/selfjev_4b_vision`, merged, bf16) on `TreeServer`, `selfjev bench`: one synthetic text, 1 to 50
questions with 3 options each, one request at a time, in process (no network), p50. Same run on three AWS GPUs in
parallel. Full tables (every length, decisions/s, per-question cost) and limits:
[reports/bench/selfjev4b_qsweep_summary.md](../reports/bench/selfjev4b_qsweep_summary.md).

| GPU | text tokens | 1 q | 5 q | 10 q | 25 q | 50 q |
|---|---|---|---|---|---|---|
| A10G 24 GB | 2,048 | 584 ms | 653 | 741 | 1,165 | 1,945 |
| A10G 24 GB | 32,000 | 22,019 ms | 22,434 | 22,978 | 24,643 | 27,760 |
| L40S 48 GB | 2,048 | 243 ms | 269 | 300 | 484 | 894 |
| L40S 48 GB | 32,000 | 9,146 ms | 9,335 | 9,478 | 10,337 | 11,544 |
| H100 80 GB | 2,048 | 166 ms | 176 | 189 | 252 | 404 |
| H100 80 GB | 32,000 | 4,033 ms | 4,122 | 4,200 | 4,574 | 5,206 |
| peak memory, allocated / reserved (all GPUs) | 2,048 | 8.3 / 8.5 GiB | 8.3 / 8.5 | 8.3 / 8.5 | 8.7 / 9.0 | 9.5 / 9.6 |
| peak memory, allocated / reserved (all GPUs) | 32,000 | 14.2 / 20.2 GiB | 14.3 / 20.3 | 14.1 / 18.5 | 15.0 / 21.1 | 14.4 / 19.5 |

- **Memory follows the text, not the questions.** The weights take 8 GiB; 50 questions add at most 1.4 GiB. Every cell
  fits on the 24 GB A10G (22.5 GiB usable); the tightest, 32K × 25 questions, reserved 21.1 GiB.
- **Each extra question costs** 3–24 ms on the H100, 10–49 ms on the L40S and 25–117 ms on the A10G (more for longer
  texts). One 50-question request is 8–40× faster than 50 one-question requests.
- **Throughput inside one request** rises with questions: on a 2K text 1.7 → 25.7 decisions/s (A10G), 4.1 → 55.9
  (L40S), 6.0 → 124 (H100). Concurrent requests batched together are not measured.
- The H100 needed a fix: PyTorch picks cuDNN attention there and it failed to load; `TreeServer` now turns it off.

## Tree vs stock pairs (same A10G, bf16, unmerged LoRA)

End-to-end p50, one request at a time. Sources: `reports/bench/gpu_{tree_4b,stock_lora_4b}_bf16/` and `…_long_bf16/`.

| text tokens | questions × candidates | stock 4B + LoRA | tree 4B + LoRA | speed-up |
|---|---|---|---|---|
| 512 | 1 × 3 | 375 ms | 192 ms | 2.0× |
| 512 | 16 × 3 | 5,414 ms | 686 ms | 7.9× |
| 2,048 | 16 × 3 | 20,460 ms | 1,091 ms | 18.8× |
| 8,192 | 16 × 3 | 90,449 ms | 2,798 ms | 32.3× |
| 16,384 | 1 binary | 4,324 ms | 4,483 ms | 1.0× |
| 16,384 | 16 × 3 | 206,915 ms | 5,638 ms | 36.7× |
| 32,000 | 16 × 3 | — | 14,235 ms (14.7 GB peak) | |

The stock model pays pairs × text tokens. The tree pays for the text once plus a short branch per question and
candidate, so adding questions barely changes its time. With one binary question there is nothing to share.

## End to end vs Jev (2026-09-23)

Same decisions-API requests from a Mac in California, one at a time, endpoints in random order. Jev through OpenRouter
(edge 12 ms away); ours, tree 4B + LoRA, on one AWS A10G in us-east-1 (71 ms away). p50 over 10 timed rounds; choice
questions with 3 options. Full tables with p95 and server-side times: [reports/latency/summary.md](../reports/latency/summary.md).

![Latency vs text length, Jev vs our tree scorer](https://raw.githubusercontent.com/Jwuthri/SelfJev/master/reports/latency/latency.png)

| text tokens | Jev, 1 q | ours vLLM, 1 q | ours transformers, 1 q | Jev, 16 q | ours vLLM, 16 q |
|---|---|---|---|---|---|
| 8 | 148 ms | **120 ms** | 196 ms | 159 ms | 336 ms |
| 512 | **156 ms** | 197 ms | 263 ms | **160 ms** | 467 ms |
| 2,048 | **144 ms** | 424 ms | 598 ms | **156 ms** | 767 ms |
| 4,096 | **154 ms** | 755 ms | 1,062 ms | **174 ms** | 1,195 ms |

**How Jev stays flat.** A fit on its 400 requests gives 132–137 ms fixed + 2.2–2.6 ms per 1,000 input tokens: about
400K tokens/s of marginal speed for one request, against ~6K tokens/s for our tree on the A10G. Every architecture must
touch each token, so the flat curve means a very small cost per token: consistent with a ~0.5–1B-parameter model (or
an MoE with ~1B active) on H100/B200-class GPUs, or a larger model split over several GPUs. Jev does read the whole
text: 97.2% on round-2 questions whose evidence is at the end of a text over 4K tokens (up to 17.6K).

## The same model on an H100 (2026-09-26)

The same sweep, same day, same client: Jev through OpenRouter (11 ms away) against `tree_4b_combo` merged on vLLM 0.30
on one **p5.4xlarge spot** (1× H100 80 GB, ≈ $2.54/h, us-east-2, 61 ms away), in bf16 and with vLLM's dynamic FP8
(`--quantization fp8`). The A10G and L40S columns are the earlier sweeps of the same model. p50 ms, wall at the client /
server inside the box (Jev: inside OpenRouter). Raw rows: `reports/latency/requests_h100.jsonl`. The model's weights,
its vLLM code and the sweep script (`scripts/latency_sweep.py`) are at tag `archive/pre-cleanup-2026-09-27`.

| text tokens | questions | Jev wall / server | A10G | L40S | H100 bf16 | H100 FP8 |
|---|---|---|---|---|---|---|
| 8 | 1 | 130 / 110 | 125 / 55 | 158 / 36 | **140 / 22** | 139 / 22 |
| 512 | 1 | 135 / 115 | 204 / 136 | 177 / 55 | **149 / 30** | 146 / 29 |
| 2,048 | 1 | 132 / 110 | 429 / 361 | 244 / 121 | **164 / 47** | 163 / 46 |
| 4,096 | 1 | 142 / 122 | 770 / 698 | 356 / 228 | **200 / 82** | 195 / 75 |
| 8 | 16 | 140 / 117 | 471 / 401 | 199 / 135 | **179 / 58** | 175 / 56 |
| 512 | 16 | 145 / 123 | 566 / 496 | 279 / 163 | **166 / 76** | 190 / 71 |
| 2,048 | 16 | 153 / 134 | 882 / 808 | 342 / 268 | **186 / 120** | 231 / 114 |
| 4,096 | 16 | 156 / 134 | 1,336 / 1,263 | 505 / 424 | **250 / 189** | 245 / 179 |

- **Inside the machine the H100 is 2–5× faster than Jev's server time**, at every size with one question and up to
  2,048 tokens with 16; the one slower cell is 4,096 tokens × 16 questions (189 vs 134 ms).
- **End to end we trail by 10–100 ms, and that is the network**: 61 ms to Ohio against 11 ms to OpenRouter's edge.
  Served from a point as close as theirs, this model beats Jev's latency.
- **FP8 changes nothing**: a 4B on an H100 is bound by per-request overhead at these sizes, not by arithmetic.
- Per-token cost, one question, server-side: ours ≈ 20 ms fixed + ≈ 15 ms per 1,000 text tokens (≈ 68K tokens/s);
  Jev 132–137 ms fixed + 2.2–2.6 ms per 1,000 (≈ 400K tokens/s). Jev's marginal cost per token is still ≈ 6× lower,
  so it is a smaller model or more GPUs per request, but at request sizes up to 4K tokens the fixed costs decide.
- **Accuracy is kept:** eval2 through vLLM on the H100 scores 94.42 in bf16 (5 of 1,991 decisions differ from the
  transformers run's 94.48) and 94.48 with FP8 (25 differ); all 1,991 questions take 16–18 s (A10G: 144 s).
- **Cost, GPU fully busy** (`reports/latency/throughput_h100.json`, at $2.63/h): 294 requests/s and $0.0025 per 1,000
  at 8 tokens × 1 question (Jev $0.016); 105 requests/s and $0.007 at 512 × 1 (Jev $0.038); 5.9 requests/s and $0.124 at
  4,096 × 16 (Jev $0.265). 2.1–6.5× cheaper than Jev in every cell on spot; at $6.88/h on demand still below Jev
  everywhere except within 10% at 4,096 × 16.
- So the speed gap was hardware, not architecture. For this model speed is a deployment question (GPU class and
  placement); the default `selfjev-4b` still has to be timed on its own engine
  ([below](#qwen35-on-vllm-2026-09-25-l40s)).

## Serving optimizations (2026-09-24)

A controlled experiment on one A10G, R1 LoRA, 2,048-token text × 16 questions × 3 candidates, new document each
request, model resident, network excluded ([conclusions](../reports/latency_optimization_2026-09-24/conclusions.md)):

| implementation | p50 |
|---|---|
| original transformers tree | 966.62 ms |
| + direct branch-mask construction | 960.63 ms |
| compact tree format, transformers | 743.50 ms |
| **tree on vLLM** (merged bf16, prefix cache, CUDA graphs) | **700.37 ms** |
| compact tree format on vLLM | 648.49 ms |

- **vLLM** keeps quality: 81.53% on the dev benchmark vs 81.50% for merged transformers.
- **Merging the LoRA** into bf16 weights costs a little precision: unmerged 81.68% vs merged 81.50%.
- **The compact format** moves repeated instructions into the shared root: 38.5% fewer branch tokens (2,119 → 1,303).
  It is 22.6% faster on transformers but only 7.4% on vLLM, below the predeclared 15% gate, and it adds CLINC
  over-rejection (94.67 → 91.67%, all nine changes to `none`). Experimental only.
- **Cache matters:** with the document root already cached, R1 vLLM answers new questions in 409 ms; a fully repeated
  request takes 185 ms. Those are different workloads from a new document.
- Faster GPUs (L40S, H100, Blackwell, A100) could not be launched in three regions that day; the L40S (2026-09-25)
  and H100 (2026-09-26) numbers on this page came later.

## Qwen3.5 on vLLM (2026-09-25, L40S)

`qwen35_4b_tree` (the same architecture as `selfjev-4b`) merged into Qwen3.5-4B and served by vLLM 0.30 (the code is
now `src/selfjev/engine/vllm.py`: `selfjev merge`, then `selfjev serve --engine vllm`), next to the Qwen3 tree
(`tree_4b_combo`) on the same GPU, with Jev in the same sweep from California. Accuracy through vLLM is unchanged: eval2
95.58% (transformers 95.58%), and 94.53% for the Qwen3 tree (94.48%). Server-side p50 (ms; Jev: time inside
OpenRouter):

| text tokens × questions | Jev | Qwen3 tree, vLLM | Qwen3.5, vLLM |
|---|---|---|---|
| 512 × 1 | 106 | **55** | 87 |
| 2,048 × 1 | **102** | 121 | 131 |
| 4,096 × 1 | **114** | 228 | 230 |
| 512 × 16 | **106** | 163 | 454 |
| 2,048 × 16 | **123** | 268 | 908 |
| 4,096 × 16 | **130** | 424 | 1,138 |

Both models run at about the same speed per token (17–24K tokens/s); the difference is how much of the text each has
to recompute. vLLM's prefix cache shares an attention model's text at any 16-token boundary, so the Qwen3 tree computes
the text once and each candidate only adds its own tokens. For Qwen3.5 the cache has to store the recurrent state
itself (tens of MB), and vLLM sets its block to 528 tokens for that; every candidate prompt recomputes the text after
the last block boundary plus its question:

| 16 questions | Qwen3 tree: tokens computed → time | Qwen3.5: tokens computed → time |
|---|---|---|
| 256 tokens | 3,346 → 139 ms | 20,064 → 993 ms (nothing shared below 528 tokens) |
| 2,048 tokens | 5,138 → 254 ms | 16,320 → 855 ms |
| 4,096 tokens | 7,186 → 400 ms | 17,424 → 1,025 ms |

`mamba_block_size` does not change this in vLLM 0.30; caching the state in bf16 halves the block to 272 tokens, with
mixed effects (256 tokens 407 ms, 1K 744 ms, 4K 689 ms). Sources: [JOURNAL 2026-09-25 18:05](JOURNAL.md),
`reports/latency/requests_qwen35.jsonl`, the probe script `reports/qwen35_4b_tree/vllm/cache_probe.py` (its log is not
in git).

**What serves `selfjev-4b` now.** The fix is to serve Qwen3.5 with its own tree, as in training: `TreeServer`
(`src/selfjev/engine/tree.py`) computes the text once, each question once and each candidate's own tokens, the same
work as the Qwen3 tree. Since the 2026-09-27 cleanup it is the default engine of `selfjev serve`, `eval` and `bench`
(vLLM stays available with `--engine vllm`). It matches standalone sequences in a CPU test
(`tests/engine/test_tree.py`) and, on GPU, the forked-cache engine's answers: the same `selfjev-4b` weights score the same on both engines: eval2 95.68 vs 95.78, dev benchmark 83.78 vs 83.75, eval_llm 93.13 vs 93.13 (99.8%, 99.8% and 100% of decisions identical)
([JOURNAL 2026-09-27 11:55](JOURNAL.md)). Its latency on A10G, L40S and H100 is [above](#many-questions-on-one-text-2026-09-30);
the L4 (g6.xlarge) that `selfjev deploy aws` picks by default is still untimed. The end-to-end test
([2026-09-28](../reports/e2e/2026-09-28/report.md): an L40S, the adapter unmerged for fine-tuning, round trips including ~70 ms of network) saw 0.2–0.3 s
for one warm request with six questions, 39 s for the very first request (kernel compilation, now done at startup),
and 16 concurrent requests, batched together, returning after 18.6 s cold and 4.4–6.4 s warm while a fine-tuning job
shared the GPU: requests in one batch all wait for it. For reference, the forked-cache engine it replaced took 156 and 252 ms for one question at 512 and
2,048 tokens, and 341 and 508 ms for 16 questions (in-process p50 on the L40S, `reports/qwen35_4b_tree/bench.json`).

## Current model on Apple Silicon (2026-09-28)

The current `selfjev-4b` adapter merged into Qwen3.5-4B runs through `TreeServer` on a local Apple M5 Pro (20-core GPU,
48 GB unified memory) with PyTorch MPS in bf16. The CLI still defaults to CUDA; this is a lower-level engine experiment,
not a validated Mac server. Each cell uses one request with synthetic repeated text and three options per question. Times include
tokenization and scoring but exclude HTTP/network. Median of 10 timed calls after two warm-ups, with MPS synchronized at
both ends. [Raw samples](../reports/latency/mac_m5_pro_selfjev4b.json) · [reproduction script](../scripts/bench_local_mps.py).

| Text tokens | 1 question | 16 questions |
|---|---:|---:|
| 8 | 688 ms | 6,786 ms |
| 512 | 2,018 ms | 8,599 ms |

`flash-linear-attention` is not installed for MPS, so the gated recurrent operation uses the correct but slower PyTorch
reference path. The NVIDIA figures above belong to an older Qwen3 model on vLLM; their difference from these Mac times
does **not** isolate the hardware effect. The same engine and model on NVIDIA GPUs: [above](#many-questions-on-one-text-2026-09-30)
(512 tokens × 1 question: 241 ms on an A10G).

## Cost vs Jev

Jev charges $0.042 per million input tokens and bills about 372 tokens of overhead per request plus about 113 per
extra 3-option question. Our cost assumes the A10G ($1.006/h) is fully busy ([batched throughput](../reports/latency/summary.md)):

| request | ours, vLLM | Jev |
|---|---|---|
| 8 tokens, 1 question | $0.0051 / 1K requests | $0.0160 |
| 512 tokens, 1 question | $0.0212 | $0.0379 |
| 512 tokens, 16 questions | $0.0902 | $0.1094 |
| 2,048 tokens, 16 questions | $0.1607 | $0.1762 |
| 4,096 tokens, 16 questions | $0.2675 | $0.2653 |

A g5.xlarge left on all month (≈ $734) beats Jev only above about 7 requests/s sustained, for 512-token requests.

On an L40S ($2.242/h, fully busy; `reports/latency/throughput_*_l40s.json`), per 1,000 requests:

| request | Qwen3 tree, vLLM | Qwen3.5, vLLM | Jev |
|---|---|---|---|
| 8 tokens, 1 question | **$0.0054** | $0.0168 | $0.0160 |
| 1,024 tokens, 1 question | **$0.0320** | $0.0422 | $0.0602 |
| 4,096 tokens, 1 question | **$0.1239** | $0.1268 | $0.1938 |
| 256 tokens, 16 questions | **$0.0787** | $0.6330 | $0.0982 |
| 4,096 tokens, 16 questions | **$0.2426** | $0.6330 | $0.2653 |

## Other backends, for scale

| backend | request | latency | source |
|---|---|---|---|
| custom cross-attention (0.6B) | 8K tokens, 16 × 3, A10G | 626 ms (stock 0.6B + LoRA: 24,024 ms) | [custom model](custom_model.md#speed) |
| jina-reranker-v3.5 (0.6B) | eval2, per question, A10G | 58 ms (tree 4B r2b: 118 ms) | [jina](jina_model.md) |
| T5Gemma 2 1B–1B | 2K × 16 × 3, L40S | 203 ms (merged tree 4B: 297 ms) | [challengers](challengers.md#t5gemma-2-a-pretrained-encoderdecoder-with-a-shared-document) |
| Qwen3.5-2B, forked cache | 8K × 16, L40S | 765 ms (tree 4B: 1,050 ms) | [challengers](challengers.md#qwen35-2b-linear-attention-with-a-forked-cache) |
| stock 0.6B / 4B / 8B + LoRA | 512 × 1 × 3, L40S | 43 / 116 / 188 ms | [stock reranker](stock_model.md#scaling-up-4b-and-8b-one-nvidia-l40s-2026-09-23) |
