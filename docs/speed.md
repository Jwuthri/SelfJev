# Speed and cost

!!! abstract "Bottom line"
    - **Sharing the text is the big win.** The shared-prefix tree is 32–37× faster than stock pairs for 16 questions ×
      3 candidates on 8K–16K-token texts, at the same quality.
    - **Jev is flat at ~150 ms**, from 8 to 4,096 tokens and 1 to 16 questions. Our tree 4B on one A10G matches it only
      for short texts with one question; it is 5× slower at 4,096 tokens.
    - **Serving:** vLLM with the prefix cache and merged weights is the best general option. A shorter "compact" tree
      format did not pay off.
    - **Cost:** a fully busy A10G is 1.3–3× cheaper per request than Jev; an idle one is not.

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
- Faster GPUs (L40S, H100, Blackwell, A100) could not be launched in three regions: no faster-GPU numbers exist.

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

## Other backends, for scale

| backend | request | latency | source |
|---|---|---|---|
| custom cross-attention (0.6B) | 8K tokens, 16 × 3, A10G | 626 ms (stock 0.6B + LoRA: 24,024 ms) | [custom model](custom_model.md#speed) |
| jina-reranker-v3.5 (0.6B) | eval2, per question, A10G | 58 ms (tree 4B r2b: 118 ms) | [jina](jina_model.md) |
| T5Gemma 2 1B–1B | 2K × 16 × 3, L40S | 203 ms (merged tree 4B: 297 ms) | [challengers](challengers.md#t5gemma-2-a-pretrained-encoderdecoder-with-a-shared-document) |
| Qwen3.5-2B, forked cache | 8K × 16, L40S | 765 ms (tree 4B: 1,050 ms) | [challengers](challengers.md#qwen35-2b-linear-attention-with-a-forked-cache) |
| stock 0.6B / 4B / 8B + LoRA | 512 × 1 × 3, L40S | 43 / 116 / 188 ms | [stock reranker](stock_model.md#scaling-up-4b-and-8b-one-nvidia-l40s-2026-09-23) |
