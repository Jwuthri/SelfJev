# Latency sweep: Jev vs our tree scorer

- 2026-09-23T20:24:46-0700; 2 sweep run(s) of 10 timed rounds each (after 1 warm-up round), one request at a time, endpoints in random order; Jev is in every run, so it has 20 samples per cell, each of ours 10.
- network round trip (TCP connect, median): openrouter.ai:443 12 ms, 98.84.140.190:22 71 ms
- Jev spend for the whole sweep: $0.0383; failed requests: 0

## 1 question × 3 options

Wall = at the client (this machine), p50 / p95 ms. Server = ours: parse + tokenize + GPU; Jev: time inside OpenRouter incl. Jev.

| text tokens | jev wall p50 | jev wall p95 | jev server p50 | ours wall p50 | ours wall p95 | ours server p50 | ours_merged wall p50 | ours_merged wall p95 | ours_merged server p50 | ours_vllm wall p50 | ours_vllm wall p95 | ours_vllm server p50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 148 | 286 | 127 | 196 | 198 | 127 | 153 | 157 | 85 | 120 | 191 | 49 |
| 16 | 165 | 227 | 144 | 196 | 200 | 127 | 156 | 220 | 85 | 123 | 189 | 52 |
| 32 | 143 | 197 | 124 | 198 | 267 | 126 | 154 | 221 | 85 | 124 | 198 | 53 |
| 64 | 162 | 216 | 142 | 196 | 197 | 126 | 156 | 225 | 86 | 126 | 192 | 56 |
| 128 | 150 | 188 | 133 | 195 | 198 | 126 | 157 | 225 | 87 | 133 | 200 | 63 |
| 256 | 142 | 225 | 124 | 215 | 218 | 145 | 189 | 257 | 118 | 154 | 228 | 84 |
| 512 | 156 | 201 | 137 | 263 | 265 | 192 | 230 | 232 | 161 | 197 | 264 | 126 |
| 1,024 | 145 | 233 | 128 | 384 | 387 | 315 | 343 | 412 | 272 | 273 | 277 | 204 |
| 2,048 | 144 | 278 | 123 | 598 | 667 | 527 | 530 | 612 | 459 | 424 | 493 | 353 |
| 4,096 | 154 | 249 | 132 | 1,062 | 1,130 | 991 | 938 | 1,012 | 865 | 755 | 824 | 682 |

## 16 questions × 3 options

Wall = at the client (this machine), p50 / p95 ms. Server = ours: parse + tokenize + GPU; Jev: time inside OpenRouter incl. Jev.

| text tokens | jev wall p50 | jev wall p95 | jev server p50 | ours wall p50 | ours wall p95 | ours server p50 | ours_merged wall p50 | ours_merged wall p95 | ours_merged server p50 | ours_vllm wall p50 | ours_vllm wall p95 | ours_vllm server p50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 159 | 215 | 138 | 688 | 757 | 616 | 602 | 650 | 530 | 336 | 339 | 264 |
| 16 | 170 | 219 | 153 | 689 | 758 | 618 | 605 | 612 | 534 | 375 | 441 | 303 |
| 32 | 165 | 212 | 147 | 688 | 693 | 618 | 606 | 673 | 534 | 375 | 396 | 304 |
| 64 | 147 | 192 | 131 | 690 | 760 | 619 | 606 | 616 | 536 | 378 | 446 | 306 |
| 128 | 170 | 241 | 149 | 690 | 699 | 621 | 608 | 610 | 538 | 384 | 424 | 314 |
| 256 | 178 | 198 | 154 | 700 | 770 | 629 | 626 | 695 | 556 | 415 | 505 | 344 |
| 512 | 160 | 216 | 140 | 757 | 827 | 686 | 678 | 680 | 608 | 467 | 537 | 396 |
| 1,024 | 164 | 251 | 145 | 901 | 905 | 831 | 807 | 879 | 737 | 569 | 572 | 497 |
| 2,048 | 156 | 220 | 134 | 1,155 | 1,162 | 1,086 | 1,034 | 1,038 | 962 | 767 | 768 | 696 |
| 4,096 | 174 | 222 | 153 | 1,700 | 1,705 | 1,629 | 1,517 | 1,628 | 1,445 | 1,195 | 1,202 | 1,123 |

Jev price: $0.0420 per million input tokens (reported cost / reported input tokens).

## Batched throughput, ours (throughput_merged): NVIDIA A10G, shared-prefix tree (tree-v1), merged LoRA

Cost per 1,000 requests at $1.006/h, GPU fully busy; Jev = its reported cost for the same requests (median).

| text tokens | questions | requests/s | ours $ / 1K requests | Jev $ / 1K requests |
|---|---|---|---|---|
| 8 | 1 | 29.9 | 0.0093 | 0.0160 |
| 8 | 16 | 2.2 | 0.1243 | 0.0874 |
| 16 | 1 | 31.1 | 0.0090 | 0.0163 |
| 16 | 16 | 2.2 | 0.1261 | 0.0878 |
| 32 | 1 | 28.7 | 0.0097 | 0.0170 |
| 32 | 16 | 2.2 | 0.1256 | 0.0885 |
| 64 | 1 | 25.1 | 0.0111 | 0.0184 |
| 64 | 16 | 2.2 | 0.1265 | 0.0899 |
| 128 | 1 | 19.7 | 0.0142 | 0.0212 |
| 128 | 16 | 2.2 | 0.1292 | 0.0927 |
| 256 | 1 | 14.0 | 0.0199 | 0.0268 |
| 256 | 16 | 2.1 | 0.1342 | 0.0982 |
| 512 | 1 | 8.7 | 0.0321 | 0.0379 |
| 512 | 16 | 1.9 | 0.1493 | 0.1094 |
| 1,024 | 1 | 4.9 | 0.0566 | 0.0602 |
| 1,024 | 16 | 1.6 | 0.1802 | 0.1317 |
| 2,048 | 1 | 2.6 | 0.1068 | 0.1047 |
| 2,048 | 16 | 1.2 | 0.2415 | 0.1762 |
| 4,096 | 1 | 1.3 | 0.2168 | 0.1938 |
| 4,096 | 16 | 0.7 | 0.3735 | 0.2653 |

## Batched throughput, ours (throughput_vllm): NVIDIA A10G, shared-prefix tree (tree-v1) on vLLM prefix cache

Cost per 1,000 requests at $1.006/h, GPU fully busy; Jev = its reported cost for the same requests (median).

| text tokens | questions | requests/s | ours $ / 1K requests | Jev $ / 1K requests |
|---|---|---|---|---|
| 8 | 1 | 55.2 | 0.0051 | 0.0160 |
| 8 | 16 | 4.9 | 0.0573 | 0.0874 |
| 16 | 1 | 48.4 | 0.0058 | 0.0163 |
| 16 | 16 | 4.0 | 0.0691 | 0.0878 |
| 32 | 1 | 44.8 | 0.0062 | 0.0170 |
| 32 | 16 | 4.1 | 0.0684 | 0.0885 |
| 64 | 1 | 38.4 | 0.0073 | 0.0184 |
| 64 | 16 | 4.0 | 0.0707 | 0.0899 |
| 128 | 1 | 30.7 | 0.0091 | 0.0212 |
| 128 | 16 | 3.8 | 0.0732 | 0.0927 |
| 256 | 1 | 21.3 | 0.0131 | 0.0268 |
| 256 | 16 | 3.6 | 0.0777 | 0.0982 |
| 512 | 1 | 13.2 | 0.0212 | 0.0379 |
| 512 | 16 | 3.1 | 0.0902 | 0.1094 |
| 1,024 | 1 | 7.3 | 0.0381 | 0.0602 |
| 1,024 | 16 | 2.5 | 0.1121 | 0.1317 |
| 2,048 | 1 | 3.8 | 0.0736 | 0.1047 |
| 2,048 | 16 | 1.7 | 0.1607 | 0.1762 |
| 4,096 | 1 | 1.8 | 0.1527 | 0.1938 |
| 4,096 | 16 | 1.0 | 0.2675 | 0.2653 |
