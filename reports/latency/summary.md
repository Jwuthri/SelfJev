# Latency sweep: Jev vs our tree scorer

- 2026-09-23T20:24:46-0700; 1 sweep run(s) of 10 timed rounds each (after 1 warm-up round), one request at a time, endpoints in random order; Jev is in every run, so it has 10 samples per cell, each of ours 10.
- network round trip (TCP connect, median): openrouter.ai:443 12 ms, 98.84.140.190:22 71 ms
- Jev spend for the whole sweep: $0.0191; failed requests: 0

## 1 question × 3 options

Wall = at the client (this machine), p50 / p95 ms. Server = ours: parse + tokenize + GPU; Jev: time inside OpenRouter incl. Jev.

| text tokens | jev wall p50 | jev wall p95 | jev server p50 | ours wall p50 | ours wall p95 | ours server p50 | ours_merged wall p50 | ours_merged wall p95 | ours_merged server p50 |
|---|---|---|---|---|---|---|---|---|---|
| 8 | 148 | 407 | 127 | 196 | 198 | 127 | 153 | 157 | 85 |
| 16 | 161 | 193 | 140 | 196 | 200 | 127 | 156 | 220 | 85 |
| 32 | 143 | 195 | 126 | 198 | 267 | 126 | 154 | 221 | 85 |
| 64 | 161 | 184 | 139 | 196 | 197 | 126 | 156 | 225 | 86 |
| 128 | 148 | 195 | 130 | 195 | 198 | 126 | 157 | 225 | 87 |
| 256 | 129 | 238 | 111 | 215 | 218 | 145 | 189 | 257 | 118 |
| 512 | 156 | 201 | 137 | 263 | 265 | 192 | 230 | 232 | 161 |
| 1,024 | 145 | 180 | 124 | 384 | 387 | 315 | 343 | 412 | 272 |
| 2,048 | 144 | 849 | 122 | 598 | 667 | 527 | 530 | 612 | 459 |
| 4,096 | 147 | 249 | 125 | 1,062 | 1,130 | 991 | 938 | 1,012 | 865 |

## 16 questions × 3 options

Wall = at the client (this machine), p50 / p95 ms. Server = ours: parse + tokenize + GPU; Jev: time inside OpenRouter incl. Jev.

| text tokens | jev wall p50 | jev wall p95 | jev server p50 | ours wall p50 | ours wall p95 | ours server p50 | ours_merged wall p50 | ours_merged wall p95 | ours_merged server p50 |
|---|---|---|---|---|---|---|---|---|---|
| 8 | 145 | 201 | 126 | 688 | 757 | 616 | 602 | 650 | 530 |
| 16 | 166 | 222 | 140 | 689 | 758 | 618 | 605 | 612 | 534 |
| 32 | 153 | 178 | 135 | 688 | 693 | 618 | 606 | 673 | 534 |
| 64 | 131 | 192 | 109 | 690 | 760 | 619 | 606 | 616 | 536 |
| 128 | 170 | 283 | 145 | 690 | 699 | 621 | 608 | 610 | 538 |
| 256 | 178 | 264 | 154 | 700 | 770 | 629 | 626 | 695 | 556 |
| 512 | 160 | 199 | 140 | 757 | 827 | 686 | 678 | 680 | 608 |
| 1,024 | 160 | 273 | 136 | 901 | 905 | 831 | 807 | 879 | 737 |
| 2,048 | 154 | 187 | 134 | 1,155 | 1,162 | 1,086 | 1,034 | 1,038 | 962 |
| 4,096 | 168 | 233 | 147 | 1,700 | 1,705 | 1,629 | 1,517 | 1,628 | 1,445 |

Jev price: $0.0420 per million input tokens (reported cost / reported input tokens).
