# Journal: what is running, what happened when

**Current state** (every test result, conclusions, dead ends, open ideas to claim) lives in
[experiments.md](experiments.md). This file is the chronological part: jobs in flight and a dated log, newest first.
Times are PDT (the user's clock) unless marked UTC. Rules for every session: [AGENTS.md](../AGENTS.md).

## In flight (add a row when you start, delete it when you are done)

| job | owner session | where | since | ends |
|---|---|---|---|---|

## Spend so far (real cost, BYOK upstream included)

| item | cost | who |
|---|---|---|
| AWS: `selfjev_4b_repro` (selfjev-4b's data, new code) g6e.2xlarge `i-0e8a08bdbdfd8cb10` us-east-2, 20:11 UTC 2026-09-27 – 05:18 UTC 09-28 (547 min, 9 min of it after the job), terminated; SG and key pair deleted by the driver | ≈ $20.44 | fork |
| AWS: engine check g5.xlarge `i-088a7878b0264f417` us-east-1, 18:22–18:53 UTC 2026-09-27 (≈ 31 min), terminated; SG and key pair deleted by the driver | ≈ $0.52 | fork |
| AWS: `selfjev_4b_v2` retrain (selfjev-4b recipe + batch 2) g6e.2xlarge `i-0700e0bcadbf72ad6` us-east-2, 08:35–18:10 UTC 2026-09-27 (9.6 h, of which 23 min idle after the job), terminated; SG and key pair deleted | ≈ $21.46 | fork |
| `mpos_distr_num_v1` batch: Luna $1.87 (OpenAI API) + Astra batch judge $17.80 (3.05M in / 0.10M out tokens) + Jev $0.14 | $19.81 (quoted ≈ $19) | fork |
| AWS: retrain from scratch g6e.2xlarge `i-07c6e6d8cb3d6316b` us-east-2, 18:59 UTC 2026-09-26 – 04:17 UTC 09-27 (9.3 h), shut down from inside (terminate on shutdown); SG and key pair deleted after the SSO login | ≈ $20.80 | fork |
| AWS: Jev soft targets C (RLCD + confident-mistake cost) g6e.2xlarge `i-0a89de33e08abb323` us-east-2, 15:08–22:14 UTC 2026-09-26 (7.1 h), terminated; SG and key pair deleted | ≈ $15.90 | fork |
| `numdate_neg_v1` batch: Luna $0.28 (OpenAI API) + Astra batch judge $2.78 + Jev $0.02 | $3.08 | fork |
| AWS: Jev soft targets A (RLCD) g6e.2xlarge `i-0e27aba020500d7fa` us-east-2, 08:49–16:03 UTC 2026-09-26 (7.2 h), terminated; SG and key pair deleted | ≈ $16.20 | fork |
| AWS: Jev soft targets B (fine-tune) g6e.2xlarge `i-0d55a59b8f27aee18` us-east-2, 08:47–14:48 UTC 2026-09-26 (6.0 h), terminated; SG and key pair deleted | ≈ $13.50 | fork |
| AWS: H100 latency sweep, p5.4xlarge **spot** `i-046f7d9cd8bde18bd` us-east-2b at $2.544/h, 08:15–08:43 UTC 2026-09-26 (28 min), terminated; SG and key pair deleted; + Jev calls $0.02 | ≈ $1.20 | fork 2 |
| AWS: Qwen3.5 box `i-0c4633f37c41491d5` g5.xlarge us-east-1, 18:33–23:16 UTC (4.7 h), terminated; SG and key pair deleted (two earlier g6e launch attempts found no capacity, $0) | ≈ $4.75 | SelfJev state of play |
| AWS: RLCD test box `i-05354315b38ac654d` g6e.2xlarge (L40S) us-east-2, 03:56–06:42 UTC 09-26 (2.8 h), terminated; SG and key pair deleted | ≈ $6.20 | fork |
| AWS: `tree_4b_combo` box g5.xlarge us-east-1, 09-24 11:59–23:38, terminated; SG and key pair deleted | ≈ $11.70 | fork |
| AWS: `tree_4b_combo_ptr` box g5.xlarge, 09-24 15:17–18:23, terminated; SG and key pair deleted | ≈ $3.10 | fork |
| AWS: `tree_4b_combo_r2` box g5.xlarge, 09-24 11:58–15:02, terminated; SG and key pair deleted, + Jev $0.02 | ≈ $3.12 | fork |
| AWS: Qwen3.5 vLLM box `i-0971a5f2783c0651e` g6e.2xlarge (L40S) us-east-2, 00:05–00:55 UTC 09-26 (0.83 h), terminated; SG and key pair deleted; + Jev calls in the sweep $0.019 | ≈ $1.88 | fork |
| AWS: `qwen35_4b_tree` box `i-071ef1ae0f0e64101` g6e.2xlarge (L40S) us-east-2, 18:08–22:58 UTC (4.8 h), terminated; SG and key pair deleted | ≈ $10.80 | fork |
| AWS: `qwen35_4b_combo` box `i-0ecb5ba494f7e2bed` g6e.2xlarge (L40S) us-east-2, 06:44–13:47 UTC (7.0 h), terminated; SG and key pair deleted, also those of two no-capacity attempts (us-east-1, us-west-2) | ≈ $15.80 | fork |
| Jev + GPT-6 Astra on the 3,471 test questions (`reports/external/full`) | $19.34 (Jev $0.06, Astra $19.27 on the OpenAI key) | Jev classifier with Qwen reranker |
| AWS: stock 4B and 8B pipelines, one g6e.xlarge, 3.16 h | ≈ $5.89 | Jev classifier with Qwen reranker |
| AWS: 10 learning-curve runs on 8 g5.xlarge | ≈ $23 | fork 2 |
| AWS: tree LoRA-capacity ablation, 2 g5.xlarge, 21:05–21:46 and 21:05–21:59 | ≈ $1.60 | fork 2 |
| AWS: combined levers (r2b data + r=64 / + MLP), 2 g5.xlarge, 00:17–02:38 and 00:17–03:10 | ≈ $5.26 | fork 2 |
| `llm_multilabel_v1` batch: writing $26.60 + Astra judge $42.36 (both sessions) | $68.96 (approved ≈ $60, cap $70) | Synthetic data generation strategy |
| Test-failure audit: Opus 5.5 relabel of 968 failed test questions | $4.92 | Synthetic data generation strategy |
| Jev predictions for `llm_multilabel_v1` | $0.30 | Synthetic data generation strategy |
| Jev predictions for every question of data/all.jsonl.gz (33,707 new texts) | $1.95 | Synthetic data generation strategy |
| LLM-evaluation data: training writing $37.09 + Astra batch judge $37.95; `eval_llm` test writing $15.55 + Astra $3.39 + Sonnet 5 $2.37 + Jev $0.03 | $96.38 (approved ≈ $100) | Synthetic data generation strategy |
| Round-2 hard-case generation (OpenRouter) + blind Astra judge (OpenAI batch) + Jev second opinion | $22.86 + $36.24 + $0.27 | Synthetic data generation strategy |
| Latency sweep: Jev calls $0.04 + AWS g5.xlarge `selfjev-latency` 20:16–21:09 (52 min, terminated) ≈ $0.87 | ≈ $0.91 | fork |
| Round-3 data: writing (Luna $10.17, Gemini $55.30, Grok $49.06) + Astra batch judge (28.5M in / 0.93M out tokens, ≈ $165.61 at list batch prices, an upper bound) | ≈ $280 (approved ≈ $250) | fork |
| AWS 09-24: all-options box ≈ $2.90, 27B teacher box ≈ $6.20, distillation box ≈ $2.90 (all terminated) | ≈ $12.00 | fork |
| eval2 build (generation + 2 judges + Jev second opinion) | $32.72 | Synthetic data generation strategy |
| Jev scored on eval2 (`reports/external/eval2`) | $0.05 | Jev classifier with Qwen reranker |
| AWS: round-3 rerun `i-067cb929be78ed826` g6e.2xlarge (L40S) us-east-2, 11:28–15:36 PDT, terminated; SG and key pair deleted | ≈ $9.25 | Jev classifier with Qwen reranker |
| AWS: round-3 box `i-01e7e056786127d8e` g5.xlarge 04:24–10:17 (stopped by someone else) + g5.2xlarge 10:32–10:47 for scoring, terminated; SG, key pair deleted | ≈ $6.25 | Jev classifier with Qwen reranker |
| AWS: Instruct control box `i-093d2861dcb9d84fb` g5.xlarge, 01:10–03:36 PDT, terminated | ≈ $2.45 | Jev classifier with Qwen reranker |
| AWS: eval2 scoring box `i-08aed2c38168e5da6` g5.xlarge, 23:52–00:58 PDT, terminated; SG and key pair deleted | ≈ $1.12 | Jev classifier with Qwen reranker |
| AWS: round-2 box `i-09dfa0077851dfadc` g6e.4xlarge (tree r2 + stopped stock r2 + tree r2b), 19:04–21:18, terminated; SG `sg-0fe165a71c7b812e6` and key pair `personal-jev-gpu` deleted 23:10 (eval2 scored on the Mac instead) | ≈ $6.70 | Jev classifier with Qwen reranker |

The tree and custom-model GPU runs and the unknown boxes are not in this table yet: their owners should add them.

## Log

### 2026-09-27 22:25 PDT: rerunning `selfjev-4b`'s exact recipe moves the scores by about a point: single runs cannot settle ±1-point questions (fork, user request)

- **What:** `selfjev_4b_repro`, `selfjev-4b`'s exact training data (80,093 rows, content-identical, same order and seed
  13) trained with the restructured code (`scripts/train/selfjev_4b.sh`); 79,943 questions, 1,803 steps, best step 1,800
  as before. Question: was `selfjev_4b_v2`'s eval_llm drop the new code or batch 2?
- **Result** (`reports/selfjev_4b_repro/`), vs `selfjev-4b`: eval2 95.08 vs 95.78 (28 / 42, p = 0.12), dev benchmark 83.81 vs 83.75 (p = 0.92), eval_llm 91.97 vs 93.13 (16 / 27, p = 0.13); final validation 92.7 vs 93.7. vs v2 (same code,
  + batch 2): eval2 95.08 vs 95.38 (p = 0.55), dev benchmark 83.81 vs 83.55 (p = 0.49), eval_llm 91.97 vs 90.49
  (33 / 19, p = 0.07).
- **Verdict:** by the rule set before the results: no significant loss (p = 0.13), but eval_llm is 0.03 under the 92.0
  bar (one question). Read: no evidence that the new training code differs; the same recipe run twice differs by about
  a point on eval2, eval_llm and validation, so `selfjev-4b` was a good draw. v2's eval_llm drop is part noise, part
  (not significant, p = 0.07) batch 2; batch 2 showed no gain anywhere. `selfjev-4b` stays the default (swapping to a
  rerun picked on test would be selection on test). Decisions on differences of about one point need two or more runs
  per arm (≈ $20 each). The adapter was not kept (moved to the Trash).
- **Cost:** ≈ $20.44 (547 min; the self-terminating driver pulled and terminated 9 min after the job ended).

### 2026-09-27 11:55 PDT: the new engine gives `selfjev-4b`'s scores; v2's eval_llm drop is the model, not the engine (fork, user request)

- **Why:** `selfjev_4b_v2` (JOURNAL 11:20) was scored by `TreeServer`, `selfjev-4b` by the archived forked-cache engine,
  and the engines had only been compared on 400 eval2 questions. Its eval_llm drop could have been the engine.
- **How:** `weights/selfjev_4b` re-scored by `selfjev eval` (TreeServer) on eval2, the dev benchmark and eval_llm on a
  g5.xlarge (A10G), compared question by question with its stored reports (L40S, old engine). Reports:
  `reports/selfjev_4b_treeserver/`.
- **Result:** eval2 95.68 vs 95.78 (1 / 3 questions, p = 0.62), dev benchmark 83.78 vs 83.75 (3 / 2, p = 1), eval_llm
  93.13 vs 93.13 (0 / 0); decisions identical on 99.8%, 99.8% and 100% of questions (probability differences: median
  0.0003–0.0006, p99 0.012–0.022). On the same engine, v2 vs `selfjev-4b`: eval_llm 90.49 vs 93.13 (9 / 34, p = 0.00017),
  eval2 95.38 vs 95.68 (35 / 41, p = 0.57), dev benchmark 83.55 vs 83.78 (60 / 68, p = 0.54).
- **Verdict:** `TreeServer` (what `selfjev serve` uses) serves `selfjev-4b` faithfully. v2 really is worse on eval_llm;
  what remains to explain it: batch 2's data, the restructured training code (v2 was its first GPU run) or run-to-run
  noise. A second seed of v2, or `selfjev-4b`'s data trained with the new code, would separate them (≈ $21 each).
- **Cost:** ≈ $0.52 (31 min; a self-terminating driver: launch, evals, pull, terminate, delete SG and key).

### 2026-09-27 11:20 PDT: retraining `selfjev-4b` with batch 2 made it worse; not promoted (fork, user request)

- **What:** the `selfjev-4b` recipe from scratch (`scripts/train/selfjev_4b.sh`: new LoRA r64, lr 2e-4, texts up to 16K,
  0.5 × label + 0.5 × Jev) on 83,581 questions: `selfjev-4b`'s data plus batch `mpos_distr_num_v1` (several correct
  answers, distractors, numbers; test-diagnosis-motivated). One L40S, 1,912 steps, best by validation loss = the last.
- **Result** (`reports/selfjev_4b_v2/`, vs `selfjev-4b`): eval2 95.38 vs 95.78 (33 / 41, p = 0.42), dev benchmark 83.55 vs 83.75 (p = 0.60), eval_llm 90.49 vs 93.13 (9 / 34, p = 0.0002). Confident mistakes on eval2 12 vs 11. The eval_llm loss
  is broad, not one family: hard and very hard verify (−9 questions), judge (−7), guardrail (−5) and very hard score
  multilabel (−3). Validation accuracy was lower at every late checkpoint (92.3–92.7 vs 92.9–93.7, same 1,198 questions).
- **Verdict:** fails the rule set before the results (eval2 ≥ 95.8 and eval_llm ≥ 92.6): `selfjev-4b` stays the
  default. More targeted data did not close the multi-positive, distractor and numeric gaps; one seed, so part of the
  difference may be run-to-run noise, but eval_llm's p = 0.0002 is not. The batch stays in `data/all.jsonl.gz`; the
  adapter was not kept (moved to the Trash with the run folder).
- **Cost:** ≈ $21.46 (g6e.2xlarge 9.6 h, incl. 23 min idle between the end of the job and the shutdown; polling every
  10 min was too slow).

### 2026-09-27 02:20 PDT: only `selfjev-4b` on master, `runs/` deleted, every doc page audited (fork, user request)

- **Code** (`bfa0825`, `a195c38`): Qwen3.5-4B only (the Qwen3.5-2B option and `--base` are gone), the unused
  forked-cache scorer is gone (`TreeServer` and vLLM serve), `weights/qwen35_4b_tree` left master (in history and at tag
  `archive/pre-cleanup-2026-09-27`; its reports stay), scripts that served only archived models are gone, and
  `scripts/train/selfjev_4b.sh` is the recipe (GPU preflight, train, evals).
- **Bugs the audit found** (`e4d3c72`): `selfjev classify` skipped the option lists `selfjev-4b` was trained with (the
  server listed them; now both do); an unhandled error was a plain-text 500 without `x-request-id` (now JSON with the
  id); `.pre-commit-config.yaml` had never been committed (a global gitignore excluded it). 82 CPU tests.
- **`runs/`** (7.4 GB, 72 runs) moved to the macOS Trash; every run's `train_meta.json` is in `reports/train_meta/`
  (`runs/a/b` → `a__b.json`), which the ledger now reads; its weights column names the kept adapter.
- **Docs:** three parallel audits of all 24 pages plus README, AGENTS, `weights/` and the data catalog: stale paths,
  commands and claims fixed, archived models marked (with the tag's `personal_jev` / `pjev` names), the eval2 McNemar
  column now compares with `selfjev-4b`, spend recomputed from the table below (≈ $786 logged as of today), and the nav
  groups the archived model pages. Open: `TreeServer` latency has never been measured on a GPU.
- **Cost:** $0.

### 2026-09-27 01:42 PDT: on a GPU, TreeServer gives `selfjev-4b`'s answers (preflight of the `selfjev_4b_v2` retrain) (fork)

- **Why:** since the cleanup, `selfjev serve` and `selfjev eval` score with `TreeServer` (the shared-prefix tree, forward
  only); `selfjev-4b`'s stored reports came from the archived forked-cache engine, and the restructured code had never
  run on a GPU. `scripts/train/selfjev_4b.sh` checks this before it trains.
- **How:** `selfjev eval --adapter weights/selfjev_4b --data data/ova/eval2.jsonl --limit 400` on the L40S box
  `i-0700e0bcadbf72ad6`, compared question by question with `reports/qwen35_4b_tree_scratch_jevall_/eval2/report.json`.
- **Result:** 99.8% of the 400 decisions agree; largest per-question probability difference: median 0.0003, p99 0.0224.
  Latency was not measured.
- **Cost:** a few minutes of the retrain box (in its line). **Verdict:** the restructured engine is sound on GPU.

### 2026-09-27 01:40 PDT: repo cleanup and the product: `selfjev` package, SDK, server with Jev's API, fine-tuning over HTTP, deployment (fork, user request)

- **Cleanup** (`ead0a73`): the dead-end models (custom cross-attention, jina, T5Gemma, compact tree, option pointers,
  teacher distillation), one-off scripts and caches are gone (562 files changed, 170,519 lines deleted). Everything is at
  tag `archive/pre-cleanup-2026-09-27`, where the package is still `personal_jev` and the CLI `pjev`.
- **Package** (`0bb21c7`, `020cbc3`, `cce9061`): `personal_jev` → `selfjev` 0.2.0 (CLI `selfjev`), split into core /
  engine / training / evaluation / server / data / deploy with tests mirroring it; ruff lint + format, pre-commit, CI.
- **SDK and server** (`ac4f97e`): `SelfJev` / `AsyncSelfJev` (httpx + pydantic only, retries, typed errors) and a
  FastAPI server with Jev's request and answers at `/v1/systemone`, `/api/alpha/decisions` and `/v1/decisions` (plus
  `multi`), cross-request batching, Bearer keys, `/health`, Prometheus `/metrics`. Contract: [api.md](api.md).
- **Deploy** (`b5abc75`): `selfjev deploy aws up|down|status|list|machines` (NVIDIA DLAMI, systemd, API key, cost cap;
  default g6.xlarge $0.805/h) and a Dockerfile. [deploy.md](deploy.md).
- **Fine-tuning over HTTP** (`c431591`): `/v1/files` and `/v1/fine_tuning/jobs` in OpenAI's shape, supervised or RLCD.
  Training files are Jev-shaped requests with answers; jobs run `selfjev finetune|rlcd` one at a time; a finished job's
  adapter is served next to `selfjev-4b` under its own model name. `selfjev serve --fine-tuning`.
- **Scripts** (`b9bcc24`, `1064ccd`): into `scripts/{data,eval,train,aws,docs}`, shared code into
  `selfjev.data.providers` and `selfjev.data.catalog`.
- **Checks:** 83 CPU tests, ruff clean, the docs site builds, the SDK wheel installs without torch. **Not run on a GPU
  yet:** the server, the AWS deploy and fine-tuning jobs over HTTP (a g6.xlarge trial ≈ 1 h ≈ $0.80 needs the user's OK).
- **Heads-up for other sessions:** `selfjev.data.providers` now asks for `max_tokens` 8192 (was 6000; another session's
  edit, kept). Request bodies changed, so reruns of `compare_external.py` miss their cache and pay again.
- **Cost:** $0.

### 2026-09-27 01:20 PDT: `mpos_distr_num_v1` built: 3,645 verified several-correct, distractor and number questions ($19.81) (fork)

- **Why:** on eval2 `selfjev-4b` still makes far more real errors than Jev on several-correct-answer questions (29 vs
  13), near-miss distractors (29 vs 14) and numbers (28 vs 18). Test-diagnosis-motivated (the eval2 audit,
  `reports/audit_2026-09-26/AUDIT.md`): the writer saw only the abstract trap names, never test items.
- **How:** `gen_hardcases.py --batch mpos_distr_num_v1 --round3 --traps multi_positive,distractor,numeric_reasoning`
  (GPT-6 Luna, 1,671 texts from 8 to 8,192 tokens, 4,041 questions), then `scripts/data/grow_batch.sh` judge / build /
  finish: blind GPT-6 Astra judge, strict build with the overlap guard against every test set, OpenAI moderation, Jev.
- **Result:** writer = judge on 95.6% (distractor 97.4, multi_positive 95.4, numeric 94.5); 3,645 of 4,041 questions kept
  (train 3,282, validation 363; multilabel 1,471, binary 1,299, multiclass 875): 179 dropped where the judge
  disagreed, 217 more by `--strict` because another question of the same text did. Moderation flagged 0 of 1,671 texts. Jev gets 94.8% right.
  `data/all.jsonl.gz` now has 93,237 questions. Review: `data/batches/mpos_distr_num_v1/review/JUDGE.md`.
- **Cost:** Luna $1.87 + Astra batch judge $17.80 + Jev $0.14 = $19.81 (quoted ≈ $19; the judge ran ≈ $2 over my estimate).
- **Verdict:** data only; `selfjev-4b` does not include it. Using it takes one more retrain (≈ $21, ≈ 9 h), not started.

### 2026-09-26 21:40 PDT: `selfjev-4b` is the default model (fork, user request)

- The from-scratch retrain's best checkpoint (`runs/qwen35_4b_tree_scratch_jevall/adapter`, JOURNAL 21:25) is now
  `weights/selfjev_4b` (name `selfjev-4b`, `model.json`, adapter sha256 dfbf2834…, Git LFS): eval2 95.8, eval_llm 93.1, dev
  benchmark 83.8. README, AGENTS, docs (index, findings box 1, leaderboard, reproduce), `weights/README.md` and the code examples
  point to it; `qwen35_4b_tree` stays in `weights/` as the previous default (best on the dev benchmark, 84.4).
- AWS: the retrain box's SG and key pair deleted after the SSO login; no `selfjev-jev-*` resource left in us-east-1/2, us-west-2.

### 2026-09-26 21:25 PDT: retrain from scratch on everything with Jev targets: eval_llm 82.1 → 93.1 (Jev 92.5), eval2 95.78, dev benchmark −0.7 from Jev's targets on emotions (fork)

- What: Qwen3.5-4B, new LoRA r64, lr 2e-4, 1 epoch (1,803 steps), `pjev finetune` on 79,943 non-test questions of
  `data/all.jsonl.gz` (every train and validation row of hardcases, hardcases_r3, hardcases_llm, hf, synthetic,
  `llm_multilabel_v1`, `numdate_neg_v1`, minus the 1,200-question validation sample), texts up to 16K tokens
  (`--max-length 16384 --batch-tokens 16384 --grad-accum 2`: the 8K default dropped 2,548 questions, mostly round-3 long
  texts; only 150 dropped now), target 0.5 × label + 0.5 × Jev. One L40S, `scripts/jev_soft_box.sh scratch`. Validation:
  78.2 → 93.66 (best, step 1,800; `qwen35_4b_tree` 92.9 on the same code).
- Results (best checkpoint; the last, 3 steps later, scores 95.63 / 83.84 / 93.13):

  | | eval2 (1,991 q) | dev benchmark (3,471 q) | eval_llm (946 q) | eval_llm multilabel EM |
  |---|---|---|---|---|
  | `qwen35_4b_tree` (original best) | 95.58 | **84.44** | 82.14 | 68.1 |
  | B: + Jev targets (gentle update) | 95.73 | 84.41 | 90.06 | 78.0 |
  | **retrain from scratch** | **95.78** (33 / 29 vs original, p = 0.70) | 83.75 (103 / 127, p = 0.13) | **93.13** (vs Jev 33 / 27, p = 0.52) | **86.8** |
  | Jev | 97.24 | 82.71 | 92.49 | 81.3 |

  | eval2 wrong questions, by trap | original | retrain | Jev |
  |---|---|---|---|
  | long texts | 8 | **3** | 2 |
  | double negation | 7 | **4** | 1 |
  | temporal | 29 | **24** | 22 |
  | distractor | 34 | **29** | 14 |
  | paraphrase | 17 | 15 | 10 |
  | multi-positive | 28 | 29 | 13 |
  | numeric | 26 | 28 | 18 |
  | role reversal | 11 | 11 | 6 |

  eval2 calibration: Brier 0.0466 (original 0.0480), ECE 0.026, confident mistakes 11 (original 30, Jev 7), mean confidence
  when wrong 0.676 (Jev 0.670). Wrong questions 84 (original 88, Jev 55): multilabel 38 → 33, binary 31 → 33, multiclass 19 → 18.
- Reading:
  - **eval_llm, the clean check** (not mined for our errors): +11.0 over the original and level with Jev (93.13 vs 92.49,
    p = 0.52), multilabel EM 86.8 vs Jev 81.3. This is the LLM-evaluation data (`hardcases_llm`, `llm_multilabel_v1`), which the
    original never saw; B (same data, gentle update) got 90.06.
  - eval2: best of our models, not significant (+0.2). The 16K texts fixed long-text errors (8 → 3); double negation, temporal and
    distractors improved; multi-positive and numeric did not.
  - Dev benchmark −0.7 (p = 0.13) is almost all `hf_emotions_multilabel` (−27 questions): Jev is weak on that subjective public set
    (68 real errors in the audit), and half-weight Jev targets pulled the model toward it. Next time: `--soft-weight 0` on hf rows.
- Files: reports `reports/qwen35_4b_tree_scratch_jevall_[_last]/` (eval2, test, eval_llm), baselines on eval_llm
  `reports/qwen35_4b_tree/eval_llm`, `reports/qwen35_4b_tree_sft_jevall__last/eval_llm`; logs and train_meta
  `reports/rlcd_jev_2026-09-26/`; adapters `runs/qwen35_4b_tree_scratch_jevall/adapter` (best) and `adapter_last` (not in `weights/`).
- Cost: ≈ $20.80 (L40S, 18:59–04:17 UTC, 9.3 h incl. a 25-minute 8K start that was restarted at 16K). The AWS SSO token expired
  before `terminate-instances`: the box was shut down from inside (terminate on shutdown); its SG and key pair still need deleting.
- Repo note: after the 16:48 LFS commit (efe3a5c) and merge, 97 data files in this checkout were LFS pointers (e.g.
  `data/eval2.jsonl`, `data/ova/*.jsonl`), which broke `eval2_summary.py`; `git lfs checkout` restored them from the local store.
- Verdict: a better model on the LLM-evaluation use cases and eval2, a worse one on emotions. Candidate new best, pending the
  user's call; the fix for the dev benchmark is Jev targets only where Jev is reliable.

### 2026-09-26 15:15 PDT: C: RLCD with a confident-mistake cost: 8 confident mistakes on eval2 (Jev 7), but only by being less sure overall; at equal coverage no better than B (fork)

- What: `pjev rlcd --reward log=1,brier=1,spherical=1,confident_miss=5` from B's result (`runs/qwen35_4b_tree_sft_jevall/adapter_last`),
  the same 69,528 questions, Jev targets (0.5), lr 2e-5, KL 0.2, 1,230 steps, one L40S. `confident_miss`: −1 for every decision
  ≥ 0.9 sure that the target says is wrong, not differentiable, so only the sampled-report policy gradient can optimize it.
- Results (final checkpoint; best-by-validation was step 0, B itself):

  | eval2 (1,991 q) | accuracy (paired vs start) | Brier | ECE | wrong decisions | ≥ 0.9 sure | mean confidence when wrong |
  |---|---|---|---|---|---|---|
  | `qwen35_4b_tree` (start) | 95.58 | 0.0480 | 0.0051 | 99 | 30 | 0.755 |
  | B: fine-tune on Jev targets | 95.73 (19 / 16, p = 0.74) | **0.0438** | 0.0245 | 94 | 14 | 0.708 |
  | **C: B + RLCD with a 5× confident-mistake cost** | 95.68 (24 / 22, p = 0.88; vs B 9 / 10, p = 1) | 0.0518 | 0.0431 | 96 | **8** | 0.690 |
  | Jev | 97.24 | 0.0335 | 0.0406 | 57 | 7 | 0.670 |
  
  | dev benchmark (3,471 q) | accuracy | Brier | ECE | wrong decisions | ≥ 0.9 sure | mean confidence when wrong |
  |---|---|---|---|---|---|---|
  | `qwen35_4b_tree` (start) | 84.44 | 0.1787 | 0.0056 | 582 | 83 | 0.686 |
  | B | 84.41 | 0.1820 | 0.0127 | 603 | 75 | 0.693 |
  | **C** | 84.41 (vs B 17 / 17) | 0.1835 | 0.0298 | 597 | **48** | 0.672 |
  | Jev | 82.71 | 0.2105 | 0.0444 | 708 | 253 | 0.791 |

- Reading:
  - The cost does what a fine-tune cannot: confident mistakes 14 → 8 on eval2 (Jev 7) and 75 → 48 on the dev benchmark (Jev
    253), mean confidence when wrong 0.690 (Jev 0.670), ECE 0.043 (Jev 0.041), at the same accuracy (vs B 9 / 10 and 17 / 17).
  - The price is sharpness: Brier 0.0438 → 0.0518 on eval2 (worse than the start's 0.0480), because the model also backs off
    on answers it gets right. B has the best probabilities; C has Jev's caution.
  - The first RLCD result that differs from fine-tuning, and only because its reward is a decision cost, not a proper score.
  - **Correction (same day, equal-coverage check):** At equal coverage (acting on the same share of decisions), C is no better than B: its 8 confident mistakes at ≥ 0.9 come from being ≥ 0.9 sure on only 77% of decisions (B 88.8%, Jev 87.7%). A higher threshold on B gives the same trade for free. B ranks better than the original at every coverage; Jev ranks far better (8 mistakes at 92% coverage, B 20).

    | mistakes among the k most confident decisions (eval2, 3,491) | 70% | 77% | 85% | 88% | 92% |
    |---|---|---|---|---|---|
    | `qwen35_4b_tree` | 3 | 8 | 14 | 16 | 29 |
    | B | 4 | **5** | **9** | 13 | **20** |
    | C | 4 | 8 | 10 | 12 | 24 |
    | Jev | 3 | 3 | 4 | 7 | 8 |

- Files: `reports/qwen35_4b_tree_cost_jevall__last/`, logs and train_meta in `reports/rlcd_jev_2026-09-26/`, adapter
  `runs/qwen35_4b_tree_cost_jevall/adapter_last`.
- Cost: ≈ $15.90 (L40S, 7.1 h). Box terminated; SG and key pair deleted.
- Next: the from-scratch retrain (In flight) can get the same C stage afterwards; a smaller weight (`confident_miss=2`) may keep more
  of B's Brier.

### 2026-09-26 12:05 PDT: `numdate_neg_v1` built: 549 verified double-negation, number and date questions ($3.08) (fork)

- Why: the eval2 failure audit (`reports/audit_2026-09-26/AUDIT.md`): our real errors vs Jev's on double negation 7 vs 1,
  temporal 28 vs 21, numeric 26 vs 18. **Motivated by a test-set diagnosis**: the writer saw only the abstract trap names.
- What: `gen_hardcases.py --batch numdate_neg_v1 --round3 --traps double_negation,numeric_reasoning,temporal_reasoning`
  (new `--traps`: only those focus traps, balanced, one per question on every tier), GPT-6 Luna through the OpenAI API:
  264 texts, 643 questions, 8 to 8K tokens, tiers balanced. Blind Astra batch judge: author = judge 93.0% (double negation
  97.9, numeric 91.0, temporal 90.8). Strict build + test-overlap guard: **549 kept** (train 508, validation 41; binary 273,
  multiclass 169, multilabel 107). Moderation: 0 of 264 texts flagged. Jev column added: Jev right on 92.9%.
- `data/all.jsonl.gz` now 89,592 questions, all with `jev`.
- Cost: Luna $0.28 + Astra $2.78 + Jev ≈ $0.02 = $3.08.
- Next: the from-scratch retrain on every non-test question (80,093 incl. `llm_multilabel_v1` and this batch), In flight.

### 2026-09-26 11:19 PDT: test-failure audit complete; eval2 labels are sound, our real gaps vs Jev are distractors and multi-positive; Jev on the multilabel batch ($2.72)

- Owner: Synthetic data generation strategy. The OpenRouter limit was raised by the user.
- Jev step of `llm_multilabel_v1`: $0.30, 0 errors; all 89,043 rows of `data/all.jsonl.gz` now have `jev`. Jev gets 86.1% of
  the batch's multilabel questions exactly right (eval2 multilabel EM: 94.2): the batch is hard for Jev too.
- Audit part 2 (`scripts/audit_failures.py`, Opus 5.5 blind, $2.42; total audit $4.92): all 968 failed test questions
  relabelled. `reports/audit_2026-09-26/AUDIT.md`.
  - **eval2: 114 of 119 failures are real model errors**; 5 proposed label errors: `eg-0024-q1` clear (Opus 0.9, = ours), four
    debatable Kimi-written binary questions phrased "Which is true about …?" (Opus 0.5-0.6). eval2 stays frozen; errata list
    in `errata_candidates.jsonl`.
  - Our real eval2 errors (86): by trap distractor 33, multi_positive 28, temporal 28, numeric 26, paraphrase 17, exception 13,
    role_reversal 11; by type multilabel 37, binary 30, multiclass 19; very hard 43, hard 35, simple 8. Jev's real errors (50):
    temporal 21, numeric 18, distractor 13, multi_positive 13. **Where we lose most to Jev: distractors (33 vs 13), multi-positive
    multilabel (28 vs 13), long texts (8 vs 2), double negation (7 vs 1), role reversal (11 vs 5).** Temporal and numeric
    reasoning are weak for both.
  - eval_llm (Jev only; ours not scored yet): 68 of 71 Jev failures are real; worst traps multi_positive 21, numeric 20,
    flawed_step 14, benign_lookalike 12, judge_injection 10.
  - Dev benchmark: 317 of 778 failures (41%) look like label problems (both models wrong: 224 of 362); real errors sit in
    subjective public sets (emotion, tweet sentiment, SST-2, BoolQ): not a data-generation target.
- This is a test-set diagnosis: any data built from it is labelled as such, the generator only sees abstract pattern
  descriptions, and eval_llm (not mined for our errors) is the clean check.
- Next (proposed, needs OKs): retrain with `llm_multilabel_v1` first (it already targets near-miss distractors and
  multi-positive), then a small temporal/numeric batch if those errors remain.

### 2026-09-26 09:14 PDT: `llm_multilabel_v1` built: 7,570 verified LLM-oriented multilabel questions ($68.96, cap $70)

- Owner: Synthetic data generation strategy (a fork of it also worked on this batch by mistake, then handed it back; its
  parts are counted here). Why: multilabel is the largest gap (eval2 multilabel EM 90.1 vs Jev 94.2); our best model's
  wrong multilabel answers on eval2 mostly add a near-miss candidate (26 of 38).
- What: `gen_hardcases.py --usecases train --multilabel --batch llm_multilabel_v1` (every question multilabel, 4-8
  candidates, ≥ 2 near-miss negatives and ≥ 1 implicit positive per question, 0 / 1 / 4+ positives spread, LLM question menus
  per use case). Writers: Luna 2,460 questions (1,065 through the OpenAI API directly, fork's `--openai`), Gemini 3.8 Flash
  1,726 sync + 4,652 through Google's Batch API (`scripts/gen_gemini_batch.py`, first live use, 3 jobs), Grok 4.7 448
  (stopped on the user's call). Blind Astra batch judge on 9,286 questions: 89.7% agree (Gemini batch 92.0, Gemini sync 91.9,
  Grok 91.1, Luna 83.5).
- Kept (strict build, overlap guards): **7,570 questions** (train 6,803 / validation 767), `data/batches/llm_multilabel_v1.jsonl`,
  now in `data/all.jsonl.gz`. Use cases 1,436-1,591 each; positives 0: 1,057, 1: 1,160, 2: 1,815, 3: 1,596, 4: 1,490,
  5+: 452; 5.0 candidates on average. Multilabel training questions in the combined file: 15,776 → 22,579.
- Safety: moderation screen (free) flagged 254 of 4,364 texts; all read; 11 removed from the raw files and the raw outputs
  (self-harm method details, an assistant reply encouraging suicide, a graphic torture scene). Kept: harmful requests,
  injections, crisis messages without method details, insults, fantasy violence.
- Incidents: the OpenRouter key hit its monthly limit (403) and the account ran out of credits (402) mid-run; Gemini moved
  to Google's Batch API (half price, ≈ $2.3 per 1K questions vs ≈ $7 through OpenRouter) and Luna to the OpenAI API. The
  first Grok writer died when the fork stopped it; `gen_gemini_batch.py` collect crashed on a bare string (fixed by the fork);
  Gemini-batch rows are tagged `synthetic:google-batch/`.
- Cost: writing $26.60 (Gemini sync $12.01, Grok $5.21, Luna $1.14, Gemini batch $8.24) + Astra judge $42.36 = $68.96.
  Pending: Jev predictions for the batch (≈ $0.30), blocked by the OpenRouter limit.
- Next: retrain with it (AWS, needs a price OK) and compare multilabel EM on eval2 and eval_llm.

### 2026-09-26 09:10 PDT: Jev's probabilities as soft targets on all data: the fine-tune halves confident mistakes on eval2; RLCD adds nothing over it (fork)

- What (user request: RLCD with soft targets, "we kinda distill Jev", on all the data): from `weights/qwen35_4b_tree`,
  one epoch over 69,528 non-test questions of `data/all.jsonl.gz` (every train and validation row of hardcases,
  hardcases_r3, hardcases_llm, hf and synthetic, minus the model's 1,200-question validation sample and 2,446 questions
  over 8K; `scripts/jev_soft_targets.py`). Target: 0.5 × verified label + 0.5 × Jev's probabilities (`--soft-weight
  0.5`: the label stays the argmax, so Jev never decides a label). A = `pjev rlcd` (log + Brier + spherical, 8 samples,
  sd 0.3, KL 0.2), B = `pjev finetune` (soft cross-entropy), both lr 2e-5, 1,230 steps, one L40S each
  (`scripts/jev_soft_box.sh`). No H100 capacity in us-east-2, us-east-1 or us-west-2.
- Jev on these questions: probability of the verified answer ≥ 0.9 on 77.3%, 0.5–0.9 on 14.8%, < 0.5 on 7.8%.
- Results, final checkpoints. Best-by-validation picked step 0 in both runs (hard-label validation loss and Brier
  penalize hedging); both boxes re-scored it and got the start's 95.58 / 84.44 exactly
  (kept outside the ledger: `runs/rlcd_jev_start_recheck/`).

  | eval2 (1,991 q) | accuracy (paired vs start) | Brier | ECE | wrong decisions | ≥ 0.9 sure | mean confidence when wrong |
  |---|---|---|---|---|---|---|
  | `qwen35_4b_tree` (start) | 95.58 | 0.0480 | 0.0051 | 99 | 30 | 0.755 |
  | A: RLCD on Jev targets | 95.43 (15 / 18, p = 0.73) | 0.0446 | 0.0119 | 100 | 22 | 0.724 |
  | **B: fine-tune on Jev targets** | **95.73** (19 / 16, p = 0.74) | **0.0438** | 0.0245 | 94 | **14** | 0.708 |
  | Jev | 97.24 | 0.0335 | 0.0406 | 57 | 7 | 0.670 |

  | dev benchmark (3,471 q) | accuracy (paired vs start) | Brier | ECE | wrong decisions | ≥ 0.9 sure | mean confidence when wrong |
  |---|---|---|---|---|---|---|
  | `qwen35_4b_tree` (start) | 84.44 | 0.1787 | 0.0056 | 582 | 83 | 0.686 |
  | A: RLCD on Jev targets | 84.50 (76 / 74, p = 0.93) | 0.1816 | 0.0113 | 593 | 88 | 0.701 |
  | B: fine-tune on Jev targets | 84.41 (87 / 88, p = 1) | 0.1820 | 0.0127 | 603 | 75 | 0.693 |
  | Jev | 82.71 | 0.2105 | 0.0444 | 708 | 253 | 0.791 |

- Reading:
  - Soft targets deliver the hedging hard labels could not: confident mistakes on eval2 30 → 14 (Jev 7), mean
    confidence when wrong 0.755 → 0.708, Brier −9%, at the same accuracy (eval2 +0.15, p = 0.74: multiclass 96.8 →
    97.5, binary 96.9 → 96.8, multilabel EM 90.1 → 90.3). The dev benchmark is flat (84.41 vs 84.44; 83 → 75 confident
    mistakes, Brier slightly worse).
  - ECE rises (0.005 → 0.025) by design: the model keeps some doubt on answers it gets right, as Jev does (0.041).
  - RLCD on the same targets moved less (KL anchor, noisier gradient) and beats the fine-tune on nothing but ECE: A vs
    B 4 / 10 on eval2 (p = 0.18), 25 / 22 on the dev benchmark (p = 0.77). Expected: its three rewards peak at the same
    target as the fine-tune's cross-entropy.
- Files: reports `reports/qwen35_4b_tree_{rlcd,sft}_jevall__last/`; logs, box logs, train_meta
  `reports/rlcd_jev_2026-09-26/`; adapters (not in `weights/`) `runs/qwen35_4b_tree_{rlcd,sft}_jevall/adapter_last`.
- Cost: A ≈ $16.20 (7.2 h), B ≈ $13.50 (6.0 h), Jev $0 (already in `all.jsonl.gz`). Boxes terminated; SGs and key
  pairs deleted, including those of the failed H100 attempts.
- Verdict: Jev's soft targets are the useful part; RLCD's sampling adds nothing when the reward is a proper score of
  the same target. Running (user request): C = RLCD from B's result with a 5× cost per confident mistake
  (`--reward log=1,brier=1,spherical=1,confident_miss=5`), the one reward a fine-tune cannot express.

### 2026-09-26 08:59 PDT: test-failure audit, part 1: on the public dev-benchmark rows, 43% of failures look like label problems ($2.50)

- Owner: Synthetic data generation strategy (user request). `scripts/audit_failures.py`: every test question that
  `qwen35_4b_tree` or Jev gets wrong (968 questions in 926 texts: eval2 119, dev benchmark 778, eval_llm 71 Jev-only), blind
  relabel by Claude Opus 5.5 (effort medium, never sees the label or any model answer), then sorted.
- **Partial:** 602 texts relabelled, all public-set rows of the dev benchmark; the OpenRouter key then hit its monthly limit
  (403) and the account ran out of credits (402), so eval2, eval_llm, the authored eval rows and 155 public rows are pending.
- Result (`reports/audit_2026-09-26/AUDIT.md`), 602 dev-benchmark failures: label right / probably wrong / ambiguous =
  ours only 82 / 21 / 7, Jev only 124 / 59 / 29, **both wrong 71 / 180 / 29**. Of 260 proposed label errors, 84 are clear
  (Opus confidence ≥ 0.8; mostly tweet sentiment 27, GoEmotions 21, AG News 11, emotion 10) and 176 debatable. Spot checks:
  genuinely subjective public labels ("i do feel stressed": sadness vs fear; an Iraq stock exchange story: world vs business).
- Verdict so far: when both models miss a public-set question, the label is usually the problem. Real errors of ours cluster
  in tweet sentiment (42), emotion (32), GoEmotions multilabel (23), TREC (18), CLINC (13): subjective public sets, not a
  data-generation target. The target-task sets (eval2, eval_llm) are the ones still to audit.
- Errata candidates for human review: `reports/audit_2026-09-26/errata_candidates.jsonl`; frozen files unchanged.

### 2026-09-26 01:50 PDT: the speed gap was hardware: on one H100 the 4B tree beats Jev's server time (fork 2 session)

- User-approved open idea D (spot first, then on-demand, then g7e). The spot p5.4xlarge (1× H100 80 GB) was fulfilled
  at the first try in us-east-2b at $2.544/h (spot placement score 9/10 that morning; every 2026-09-24 launch had failed).
  Box `i-046f7d9cd8bde18bd`, DLAMI Ubuntu 22.04 (driver 595.91.07), vLLM 0.30.0, torch 2.13+cu130. Setup to servers up:
  9 min. Terminated 08:43 UTC; SG and key pair deleted; nothing of this session runs in AWS.
- What ran: `tree_4b_combo` merged (`vllm_tree merge`), served on vLLM in bf16 (:8002) and with `--quantization fp8`
  (:8003, new flag on `vllm_tree serve` and `scripts/eval_vllm.py`), both resident (0.42 of the GPU each); the same
  latency sweep as before from the Mac through an SSH tunnel (`scripts/latency_sweep.py sweep`, 10 rounds, Jev in
  random order with ours; `reports/latency/requests_h100.jsonl`); then eval2 through vLLM in both precisions and the
  batched throughput benchmark. RTT: OpenRouter 11 ms, box 61 ms.
- Latency, p50 ms, wall at the client / server inside the box (Jev: inside OpenRouter):

  | text tokens | questions | Jev | A10G (09-24) | L40S (09-25) | H100 bf16 | H100 FP8 |
  |---|---|---|---|---|---|---|
  | 8 | 1 | 130 / 110 | 125 / 55 | 158 / 36 | 140 / 22 | 139 / 22 |
  | 512 | 1 | 135 / 115 | 204 / 136 | 177 / 55 | 149 / 30 | 146 / 29 |
  | 2,048 | 1 | 132 / 110 | 429 / 361 | 244 / 121 | 164 / 47 | 163 / 46 |
  | 4,096 | 1 | 142 / 122 | 770 / 698 | 356 / 228 | 200 / 82 | 195 / 75 |
  | 8 | 16 | 140 / 117 | 471 / 401 | 199 / 135 | 179 / 58 | 175 / 56 |
  | 512 | 16 | 145 / 123 | 566 / 496 | 279 / 163 | 166 / 76 | 190 / 71 |
  | 2,048 | 16 | 153 / 134 | 882 / 808 | 342 / 268 | 186 / 120 | 231 / 114 |
  | 4,096 | 16 | 156 / 134 | 1,336 / 1,263 | 505 / 424 | 250 / 189 | 245 / 179 |

  - Inside the machine the H100 is 2–5× faster than Jev's server time in every cell but 4,096 tokens × 16 questions
    (189 vs 134 ms). End to end we trail by 10–100 ms: the 61 ms hop to Ohio against 11 ms to OpenRouter's edge.
  - FP8 changes nothing: the 4B is overhead-bound on an H100 at these sizes. Fit, one question, server-side: ours
    ≈ 20 ms + ≈ 15 ms per 1,000 text tokens (≈ 68K tokens/s); Jev 132–137 ms + 2.2–2.6 ms per 1,000 (≈ 400K tokens/s).
    Jev's per-token cost is still ≈ 6× lower, so a smaller model or more GPUs per request; below 4K tokens the fixed
    costs decide.
- Accuracy of the serving paths on eval2 (`reports/tree_4b_combo/eval2_vllm_h100{,_fp8}`; transformers reference 94.48):
  vLLM bf16 **94.42** (5 of 1,991 decisions differ, 3 / 2), vLLM FP8 **94.48** (25 differ, 9 / 9; multilabel EM 86.6 vs
  85.9). FP8 costs no accuracy. All 1,991 questions in 18 s (bf16) and 16 s (FP8); the A10G took 144 s.
- Throughput, GPU fully busy (`reports/latency/throughput_h100.json`, cost at $2.63/h in the table; actual spot $2.54):
  294 requests/s at 8 tokens × 1 question ($0.0025 per 1,000 vs Jev $0.016), 105 req/s at 512 × 1 ($0.007 vs $0.038),
  5.9 req/s at 4,096 × 16 ($0.124 vs $0.265). Cheaper than Jev in every cell, 2.1–6.5×, on spot. At the on-demand
  price ($6.88/h) multiply ours by 2.6: still below Jev everywhere except within 10% at 4,096 × 16.
- Verdict: **the speed gap was hardware, not architecture.** No speed-driven architecture work is needed; speed is a
  deployment question (H100-class GPU, placement near the client). The open work is accuracy (memo proposals A–C, E).
- Process notes: (1) `pkill -f "<pattern>"` inside an `ssh host '<command>'` kills the remote shell itself when the
  pattern appears in the command string, and vLLM's EngineCore child keeps the GPU memory after its parent dies: free
  the GPU by `nvidia-smi --query-compute-apps=pid` PIDs instead. (2) vLLM 0.30 aborts at interpreter exit after the
  throughput run ("terminate called without an active exception") once results are written; harmless.
- Cost ≈ $1.20 (spot 28 min $1.18 + Jev $0.02). Docs updated: findings 19–21, speed.md (new H100 section), ledger
  conclusion 11, open idea D done, landscape, next, the memo.

### 2026-09-26 01:34 PDT: Jev's prediction on all 81,473 questions; one dataset that grows by batches ($1.95)

- Owner: Synthetic data generation strategy. User: store Jev's probabilities once per row (no recompute, usable for
  fine-tuning); always use one dataset and grow it instead of creating a new one each time.
- Jev: `scripts/jev_predictions.py --call` answered the 33,707 texts not in any cache, $1.95, 0 errors; with the 16,543
  cached questions every row of `data/all.jsonl.gz` now has `jev` (P(yes) or per-candidate probabilities, answer,
  confidence, correct, version `typesafe/jev-1.13-20260917`). Stored in `data/jev/predictions.jsonl` + `data/jev/cache.jsonl`.
- Jev vs our labels (from the stored rows; test sets for reporting only): hf 75.2, synthetic 99.0, round 2 95.7, round 3
  96.4, hardcases_llm 94.9, eval 96.7, eval2 97.2, eval_llm 92.5, compact challenge 100.0. Checks: dev benchmark 82.7 and
  eval2 97.2 equal the reports. **Caveat for distillation:** on the public sets Jev disagrees with the human labels on
  a quarter of the questions, so a Jev teacher term would pull against the gold labels there.
- Growth: `gen_hardcases.py --batch <name>` writes `data/batches/<name>/raw`; `scripts/grow_batch.sh <name>
  judge|build|finish` judges blind, builds strict with overlap guards and a moderation screen, adds Jev predictions and
  rebuilds; `build_all.py` discovers `data/batches/*.jsonl` by itself. BoolQ curve rows moved out of the combined file
  (BoolQ is a held-out dev-benchmark family). AGENTS.md, README, docs/data.md, data/README.md and memory updated.

### 2026-09-26 01:23 PDT: Jev's prediction stored per question (`jev` field in data/all.jsonl.gz), 16.5K from cache ($0)

- Owner: Synthetic data generation strategy; the user wants Jev's probabilities stored once per row, to stop recomputing
  them and to use them for fine-tuning. `scripts/jev_predictions.py` writes `data/jev/predictions.jsonl` (id, P(yes) or
  per-candidate probabilities, answer, confidence, correct, Jev version, request hash); `build_all.py` joins it as `jev`.
- Free pass: 16,543 questions recovered from the caches of earlier Jev runs (dev-benchmark test, round-2 judge, eval2,
  eval_llm). Check: Jev on the dev benchmark 82.7% and eval2 97.2% from the stored rows, identical to the reports.
- Missing: 67,930 questions in 36,707 texts (hf train/val/cal, synthetic, round 3, hardcases_llm, BoolQ curve, eval
  val/cal, compact challenge, 6 changed eval_llm rows), estimated ≈ $2.12. Awaiting the user's price OK.

### 2026-09-26 01:18 PDT: one catalog and one file for all our data ($0)

- Owner: Synthetic data generation strategy; the user found the data scattered. `scripts/build_all.py` writes
  `data/all.jsonl.gz` (every original question once, 84,473 from 10 datasets, each row tagged `dataset`, own `split`
  kept; 85 MB, gitignored, rebuildable) and the generated catalog [data/README.md](../data/README.md): what each
  dataset is, used as (training / dev benchmark / frozen test), questions, texts, splits, types, sha256, and the
  derived files left out on purpose (hardcases_nb, ova, ptr, curve subsets, distill, teacher, fixtures).
- `personal_jev.data` reads `.gz` and accepts the `dataset` field, so `load(["data/all.jsonl.gz"])` works.
- Linked from README, AGENTS.md and docs/data.md. Rerun the script after adding a dataset (edit its DATASETS list).

### 2026-09-26 01:10 PDT: LLM-evaluation data made safe: strict labels, moderation review, PII fix. Now 9,443 training / 946 test ($0)

- Owner: Synthetic data generation strategy; the user asked for these data to be safe. Supersedes the counts of the
  entry below. Details: [llm_eval_data.md](llm_eval_data.md#safety-passes-2026-09-26-the-user-asked-for-safe-data).
- Labels: `--strict` in `build_hardcases.py` and `build_eval2.py` drops a whole text when any of its questions was
  flagged by a judge (training −897 sibling questions, test −160).
- Content: all 4,732 sources through OpenAI moderation (free, `scripts/moderate_texts.py`); the 169 flagged texts were
  read. 11 more texts removed (13 in all): working attack code, weapon and hazmat smuggling tips, a step-by-step fraud
  plan, self-harm encouragement, self-harm method details. Raw files edited and tracked generation caches scrubbed.
- PII: 7 SSN-shaped numbers in issuable ranges rewritten to the never-issued group `00`; no public figures.
- Result: `data/hardcases_llm.jsonl` **9,443** questions / 3,654 texts (sha256 `b694f5a0…`), `data/eval_llm.jsonl`
  **946** questions / 317 texts (sha256 `6cfc3e16…`). Jev on eval_llm **92.5%** (verify 86.7, multilabel EM 81.3).

### 2026-09-25 23:45 PDT: first RLCD test: no gain in accuracy or calibration (fork session)

- What: `pjev rlcd` from `weights/qwen35_4b_tree` (reward log + Brier + spherical, 8 sampled reports per question,
  sd 0.3), validated on the fine-tune run's 1,200 validation questions. Logs and settings: `reports/rlcd_2026-09-25/`.
- Take 1, on 16K of the model's own training questions (lr 5e-5, KL 0.05): worse on every validation measure by step
  100 of 504 (accuracy 92.74 → 92.05, cross-entropy 0.128 → 0.231, ECE 0.005 → 0.024, confidently wrong 15 → 40).
  Stopped. On questions it already fits, a proper score keeps pushing the given answer toward 100%, like a second
  fine-tuning epoch.
- Take 2, on 4,412 questions it never trained on (validation-split rows outside the 1,200-question sample), lr 1e-5,
  KL 0.2, against a plain fine-tune control on the same questions and settings. Both select their last step.

  | eval2 (1,991 q) | accuracy | Brier | ECE | wrong decisions | of which ≥ 0.9 sure | mean confidence when wrong |
  |---|---|---|---|---|---|---|
  | `qwen35_4b_tree` (start) | 95.58 | 0.0480 | 0.0051 | 99 | 30 | 0.755 |
  | + RLCD | 95.63 (3 / 2, p = 1) | 0.0481 | 0.0096 | 96 | 34 | 0.776 |
  | + fine-tune, same data (control) | 95.43 (4 / 7, p = 0.55) | 0.0480 | 0.0053 | 100 | 31 | 0.756 |
  | Jev | 97.24 | 0.0335 | 0.0406 | 57 | 7 | 0.670 |

  Dev benchmark: start 84.44 (ECE 0.0056, 83 confident mistakes), RLCD 84.36 (ECE 0.020, 118), control 84.50 (ECE
  0.011, 91). Reports `reports/qwen35_4b_tree_rlcd_fresh_/`, `reports/qwen35_4b_tree_sft_fresh_/`.
- Reading:
  - Our model is already better calibrated than Jev by ECE (0.005 vs 0.041); what Jev has is fewer mistakes and
    hedged ones (7 of 57 at ≥ 0.9 against our 30 of 99). With one hard label per question, a proper-score reward gives
    the same signal as cross-entropy, only noisier, so it cannot teach "be less sure here"; RLCD came out slightly
    more confident when wrong.
  - The Gaussian sampling of reports also biases the optimum toward overconfidence as the noise grows (CPU check, 70%
    base rate: sd 0.3 → 0.695, sd 0.6 → 0.717, sd 1.0 → 0.754); small at the sd used, so not the main cause.
- Cost: ≈ $6.20 (L40S 2.8 h; the duplicate evals of identical checkpoints were skipped).
- Verdict: RLCD v1 as implemented is not worth running on hard labels. For it to matter the reward has to carry
  something labels don't: soft targets (the judges' agreement, a teacher's probabilities) or a cost that punishes
  confident mistakes more than it rewards confident rights.

### 2026-09-25 23:40 PDT: LLM-evaluation data built: 10.4K training questions + frozen 1.1K test set `eval_llm` ($96.38)

- Owner: Synthetic data generation strategy. The user asked for ≈ 2K synthetic questions per use case of Jev's pitch
  ("score, judge, verify, guardrail, and detect jailbreaks of LLM prompts, reasoning traces, and/or outputs"). Before
  this, ≈ 6% of round-2/3 texts and 3% of eval2 were LLM artifacts; the dev benchmark's `eval_agent_output` slice
  (26 q) had the tree at 61.5 vs Jev 92.3. Write-up: [llm_eval_data.md](llm_eval_data.md).
- **Training: `data/hardcases_llm.jsonl`, 10,369 verified questions / 4,243 texts** (train 9,333 / validation 1,036,
  sha256 `cf46e0cf…`); judge 2,040, guardrail 2,101, score 2,053, jailbreak 2,084, verify 2,091; ≈ 1K per length step
  8 → 8K tokens. Writers Luna / Gemini 3.8 Flash / Grok 4.7 / DeepSeek V4 Flash via `gen_hardcases.py --usecases train`
  (brief `data/hardcases/BRIEF_llm.md`). Blind Astra batch judge: 92.3% agree (Grok 97.7, Gemini 96.9, Luna 93.1,
  DeepSeek 73.7). `data/hardcases_llm/review/`.
- **Test: `data/eval_llm.jsonl`, 1,106 questions / 398 texts, frozen like eval2** (sha256 `6f163506…`): eval2's writers
  (Opus 5.5, Kimi K3, GLM 5.3), a third of the calls on LLM applications absent from training, judges Astra 94.5% and
  Claude Sonnet 5 95.1% (not Gemini 3.1 Pro: the user's call), kept only when both agree with the author.
  **Jev scores 93.3%** (verify 88.6, guardrail 93.8, score 93.8, jailbreak 94.7, judge 95.3; multilabel EM 83.2).
  `data/eval_llm/REVIEW.md`, `review/SPOTCHECK.md`.
- Safety scan of the kept texts: two working exploit snippets (`lgf-0135` reverse shell, `lgf-0251` netcat injection)
  removed from the raw file and scrubbed from `reports/hardcases_llm/gen_cache/lgf.jsonl`. 0 texts dropped by the
  8-gram overlap guards.
- Not done: no model trained on it or scored on `eval_llm` yet. Next: baseline the best models on `eval_llm`, then
  retrain with `hardcases_llm.jsonl` (AWS, needs a price OK). Training on it ends `eval_agent_output`'s held-out status.
- Cost $96.38 (approved ≈ $100): training writing $37.09 + Astra $37.95; test writing $15.55 + judges $5.76 + Jev $0.03.
- Fixes: `build_eval2.py` takes `--raw/--review/--out/--guard` (its report title used a shadowed variable, fixed).
### 2026-09-25 19:30 PDT: weights in the repo, `pjev finetune` / `pjev rlcd`, a Qwen3.5 tree server, docs refresh (fork session; $0)

- **Weights:** `weights/qwen35_4b_tree` (eval2 95.6) and `weights/tree_4b_combo` (94.5) copied from `runs/`, tracked
  with Git LFS (`weights/**/*.safetensors`), each with a `model.json` (base model and revision, recipe, prompt, scores,
  sha256, serve commands); `weights/README.md`. Not committed.
- **`pjev finetune` / `pjev rlcd`** (`src/personal_jev/finetune.py`, `cli.py`): the Qwen3.5 tree recipe on any JSONL of
  (state, question, target), from scratch or `--init weights/qwen35_4b_tree`; validation reports accuracy, cross-entropy,
  Brier, ECE and confidently-wrong counts. RLCD = policy gradient on strictly proper scoring-rule rewards (log, Brier,
  spherical; `accuracy` optional): per question, `--samples` reports sampled from a Gaussian around the logits,
  reward minus the question's mean reward as the advantage, `--beta` KL to the starting model. Tests
  (`tests/test_finetune.py`, CPU): trained only on RLCD, a shared question with 70% "yes" learns p = 0.70 and a
  60/30/10 choice p = 0.60 (calibration); finetune then rlcd end to end on a tiny random Qwen3.5. Not run on the real
  model yet ([finetune.md](finetune.md)).
- **`qwen35_tree.TreeServer`**: serves Qwen3.5 with the training tree, forward only (text once, each question once,
  each candidate's own tokens), LoRA merged; `python -m personal_jev.qwen35_tree serve`, `run_qwen35.py --stage eval
  --tree`, `latency_sweep.py throughput --qwen35-tree`. Exact vs standalone sequences in a CPU test (mixed requests,
  several packed batches); not timed on a GPU.
- **Docs:** home page, how it works, speed (Qwen3.5 on vLLM, L40S costs), reproduce, open questions, dead ends, spend
  ($517 logged; three runs added to the spend table), data mixes, challengers, findings box 22, README; new page
  "Fine-tune and RLCD" in the nav.

### 2026-09-25 18:05 PDT: Qwen3.5 on vLLM keeps its 95.6 and is fast for one question, slow for sixteen (fork session)

- What: `src/personal_jev/vllm_qwen35.py`.
  - `merge`: the LoRA merged into a copy of the original (multimodal) checkpoint, replacing exactly the 152
    LoRA-targeted tensors (a first version also replaced tensors that differed only by dtype; the count check caught it).
  - `VllmQwen35Scorer`: one prompt per candidate with `ChallengerScorer.entry`'s token ids, vLLM's prefix cache, readout
    logprob(yes) − logprob(no) over the two allowed tokens (= z_yes − z_no); `serve` CLI.
  - Also: `scripts/eval_vllm.py --qwen35` (now under a main guard: vLLM spawns its engine), `latency_sweep.py
    throughput --qwen35 --options-in-question --gpu-price --name`, `vllm_tree serve --gpu-memory-utilization`.
- Accuracy through vLLM 0.30 on eval2: `qwen35_4b_tree` **95.58**, identical to transformers (4 / 4 flips, max score
  difference 0.40; `reports/qwen35_4b_tree/eval2_vllm`); `tree_4b_combo` 94.53 vs 94.48 (3 / 2;
  `reports/tree_4b_combo/eval2_vllm`). All of eval2 in 112 s and 51 s.
- Latency, server side p50 ms (L40S, both models served on one GPU, Jev in the same sweep from the Mac;
  `reports/latency/requests_qwen35.jsonl`, `reports/latency/summary.md`; the transformers column is `bench.json`):

  | text tokens × questions | Jev | Qwen3 tree, vLLM | Qwen3.5, vLLM | Qwen3.5, transformers fork |
  |---|---|---|---|---|
  | 512 × 1 | 106 | 55 | 87 | 156 |
  | 2,048 × 1 | 102 | 121 | 131 | 252 |
  | 4,096 × 1 | 114 | 228 | 230 | — |
  | 512 × 16 | 106 | 163 | 454 | 341 |
  | 2,048 × 16 | 123 | 268 | 908 | 508 |
  | 4,096 × 16 | 130 | 424 | 1,138 | — |

  End to end from California add ≈ 60–120 ms to ours (us-east-2 box through an SSH tunnel).
- Why 16 questions are slow: for this hybrid model vLLM sets the attention block to 528 tokens (one DeltaNet state per
  page) and caches the recurrent state only at block boundaries (`mamba_cache_mode` "align"). Each of the 48 prompts
  recomputes the text after the last boundary plus its question; texts under ≈ 500 tokens share nothing (993 ms at 256
  tokens). `mamba_block_size` 64 or 16 changes nothing (hits stay on the 528 lcm); a bf16 state cache halves the block to
  272 (256 tokens 407 ms, 4K 689 ms, but 1K 744 ms). Probe: `reports/qwen35_4b_tree/vllm/probe.log`.
- Cost per 1,000 requests, GPU fully busy (L40S $2.242/h; `reports/latency/throughput_*_l40s.json`): the Qwen3 tree on
  vLLM is below Jev in every cell (1 q × 8 tokens $0.005 vs $0.016; 16 q × 4K $0.243 vs $0.265). Qwen3.5 is at Jev's
  price for one question from 1K tokens up ($0.127 vs $0.194 at 4K) and 2–6× Jev with 16 questions.
- Cost: ≈ $1.88 (spend table).
- Verdict: Qwen3.5 serves on vLLM at full accuracy and 1.7–1.9× faster than transformers for one question; for many
  questions vLLM's coarse hybrid prefix cache makes it 1.3–1.8× slower than our own fork path and 2–4× slower than the
  Qwen3 tree. Options: route by question count; patch vLLM to checkpoint the state at the shared-prefix junction (0.30
  does it only for EAGLE, `enable_mamba_fine_grained_prefix_cache`); or a faster custom fork server.

### 2026-09-25 16:05 PDT: Qwen3.5-4B trained with a real tree scores 95.6 on eval2, our best, 1.6 behind Jev (fork session)

- What: a shared-prefix tree for Qwen3.5 training (`src/personal_jev/qwen35_tree.py`, `run_qwen35.py --tree`).
  - One packed row per state: root (system + document), question segments (the longest common prefix of the question's
    branches), one leaf per candidate. Same token ids as `ChallengerScorer.entry`, so the existing forked-cache inference
    serves the adapter unchanged.
  - Full-attention layers read the row through `tree.tree_mask`. Gated DeltaNet layers run level by level (roots, then
    question segments from their root's final recurrent and conv state, then leaves), with gradients through those
    states; right padding inside a level is a no-op for the state (q = k = v = 0, beta = 0, g = 0). Own per-layer
    activation checkpointing (HF's drops the cache path).
  - Exactness: `tests/test_qwen35_tree.py` (tiny random hybrid model, fp32, CPU): scores within 5e-6 and every gradient
    within 1e-4 of full sequences. On the real model (`--stage check-tree`, reports in `reports/qwen35_4b_tree/checks/`):
    fp32 scores within 0.004, LoRA-gradient cosine 0.99997; bf16 cosine 0.981, the same as the full-sequence reference
    against itself re-batched (0.980), so the bf16 gap is rounding. The fla kernel's initial-state gradient was checked
    separately against the torch reference (rel 1.8e-3 in bf16).
- Run: `qwen35_4b_tree` = `qwen35_4b_combo`'s data and LoRA (option lists, round-2b + round-3, r64) with the tree,
  texts ≤ 8K (was 2K), batch 8192 × GA 4 as `tree_4b_combo`.
  - 51,774 training questions (2,013 = 3.7% dropped, was 18.5%), 24.4M tree tokens (the combo run: 54.9M pair tokens),
    941 steps, 4.1 h on one L40S (the combo run: 6.6 h).
  - Validation (1,170 q): 78.1 at step 0, 92.7 at the end; the evals use the final checkpoint (lowest loss, 0.128).
- eval2 (`reports/qwen35_4b_tree/eval2`, paired):
  - **95.6**: binary 96.9, multiclass 96.8, multilabel EM **90.1** (Jev 97.8 / 98.1 / 94.2).
  - vs `qwen35_4b_combo` 94.5: 52 / 31, p = 0.028: the tree (more and longer training texts) adds +1.1 on the same base.
  - vs `tree_4b_combo` 94.5: 63 / 41, p = 0.039.
  - vs Jev 97.2: 31 / 64, p = 0.0009 (the gap was 2.7). Simple tier 98.6 vs Jev 98.5.
  - Errors: 88, of which 23 with margin ≥ 0.4 (`tree_4b_combo`: 110 and 26).
  - Diagnostic only (fixed 50/50 averages, nothing fitted): with `tree_4b_combo` 95.9; with it + the 27B teacher 96.5.
- Dev benchmark (`reports/qwen35_4b_tree/test`): **84.4** (binary AUROC 0.972, ECE 0.038; multiclass macro-F1 92.6;
  multilabel EM 59.3). vs `qwen35_4b_combo` 84.3 (p = 0.84); vs `tree_4b_combo` 82.7 (154 / 94, p = 0.0002); vs Jev 82.7
  (238 / 178, p = 0.004).
- Speed (`reports/qwen35_4b_tree/bench.json`): unchanged, same inference code (transformers + forked cache, L40S): 156 ms
  at 512 tokens, 252 ms at 2K, 950 ms at 8K for 1 question. No vLLM path for Qwen3.5 yet.
- Cost: ≈ $10.80 (spend table). Three check attempts failed first on memory in the check itself (the full-sequence
  reference, and an unbucketed batch), not in training.
- Verdict: **new best model**. The tree was the missing piece for Qwen3.5: same data and base as `qwen35_4b_combo`,
  +1.1 on eval2, 38% less training time. Next: serve it on vLLM (hybrid prefix cache) for latency.

### 2026-09-25 06:55 PDT: Qwen3.5-4B + option lists + round 3 ties the best on eval2 (94.5) and beats Jev on the dev benchmark (84.3) (fork session)

- Run: `qwen35_4b_combo` (`scripts/run_qwen35.py qwen35_4b --stage train --tag _combo --data-dir data/ova --r3`; the
  `--data-dir` and `--r3` flags are new and additive).
  - Recipe: `qwen35_4b_r2x64` (Qwen3.5-4B rev 851bf6e, LoRA r64 / alpha 128, every candidate trained as its own full
    sequence, training texts ≤ 2K, batch 8192 × GA 4, 1 epoch) + every option listed in the question (`data/ova/`) +
    round-3 data with r3_* uncapped.
  - 43,827 training questions, 2,474 steps, 6.6 h on one L40S. **9,960 questions (18.5%) dropped for > 2K tokens**
    (7.8% in `qwen35_4b_r2x64`): round-3 texts are longer and the option lists lengthen every question.
  - Validation (992 q, round 3 included): 77.5 at step 0, 90.7 at the end. The evals use the lowest-loss checkpoint,
    step 2,250 (loss 0.165, 90.5).
- eval2 (`reports/qwen35_4b_combo/eval2`, paired):
  - **94.5**: binary 96.2, multiclass 95.8, multilabel EM **88.2** (our best multilabel; Jev 94.2).
  - vs `tree_4b_combo` 94.5: 61 / 60, p = 1. A tie with different strengths: multilabel +2.3, multiclass −1.7,
    temporal reasoning 80.3 vs 85.2, multi-turn 90.6 vs 94.0, sarcasm 94.0 vs 91.3.
  - vs `qwen35_4b_r2x64` 93.7: 62 / 46, p = 0.15. The two levers add +0.8 here (not significant) vs +1.8 on Qwen3
    (p = 0.001); the 2K training cap is the likely reason.
  - vs Jev 97.2: 23 / 77, p = 6e-8.
  - Diagnostic only (fixed 50/50 probability average, nothing fitted, 2× the compute): with `tree_4b_combo` 95.5 (either
    right 97.5); with `tree_4b_combo` + the 27B teacher 95.9.
- Dev benchmark (`reports/qwen35_4b_combo/test`): **84.3**, our best (binary 90.0, multiclass 85.3, multilabel EM 62.2).
  vs `tree_4b_combo` 82.7: 172 / 116, p = 0.001; vs Jev 82.7: 250 / 194, p = 0.009; vs `qwen35_4b_r2x64` 83.4: p = 0.053.
- Speed (`reports/qwen35_4b_combo/bench.json`; transformers + forked cache, in-process p50 on the L40S; bench requests
  have 3 short options and no option list): 512 tokens 157 ms (1 question) / 343 ms (16); 2K 252 / 510 ms; 8K 943 /
  1,504 ms. The same code on the A10G (`qwen35_4b_r2x64`) was 1.5–2.6× slower. Not comparable with the Qwen3 tree's
  vLLM numbers; vLLM serving of Qwen3.5 is untested.
- Cost: ≈ $15.80 (spend table).
- Verdict: ties the best on eval2 and is the first model significantly above Jev on the dev benchmark. `tree_4b_combo`
  stays the served model (vLLM path). Next for Qwen3.5: a real tree in training (fork the recurrent state with
  gradients) to lift the 2K cap, then vLLM serving.

### 2026-09-25 00:45 PDT: how Jev probably works, and the next architecture (fork 2 session; $0, nothing run)

- The user asked what all the findings say about how Jev was built and whether a new architecture is needed.
- Memo: [reports/jev_hypothesis_2026-09-25.md](../reports/jev_hypothesis_2026-09-25.md). Measured facts first, then
  inference: shared state + isolated per-question branches (the "state plus the longest question" limit), options
  inline with one readout per option (113 billed tokens per 3-option question), ≤ a few B parameters on fast GPUs
  (400K tokens/s marginal; the 113–136 ms floor at 8 tokens is hop + batching), trained on frontier judgments (dev
  benchmark multilabel EM 40.1 vs our 57.6) with a calibration objective. Nothing measured requires a from-scratch
  backbone; our three failed new-architecture attempts say the pretrained LM's joint reading and readout are the quality.
- New $0 analysis, `scripts/ensemble_eval2.py` → [reports/eval2/ensembles.md](../reports/eval2/ensembles.md):
  - Jev's probabilities are rounded to 0.01, 19.3% graded (ours 10.8%); 7 of its 55 eval2 errors have margin ≥ 0.4,
    26 of our 110. On 44 of the 82 questions Jev wins over `tree_4b_combo`, our margin is below 0.2.
  - Fixed 50/50 averages, nothing fitted: combo + Eikos-4B 95.3, combo + Qwen3.5-4B 95.0, combo + 27B teacher 95.8
    (multilabel 89.5), all four 95.8. Cascade combo → average with the 27B when margin < 0.3: 9.1% deferred, 95.5; with
    Jev as the fallback (upper bound) 96.7 at 12% deferred. Deferring to the 27B alone gains nothing (94.9).
  - Thresholds must come from validation, never eval2; the curve is flat between tau 0.2 and 0.45.
- Proposals added to the open ideas (awaiting the user's OK): A parallel-readout branch (one branch per question,
  verdict block with a readout per option + `none`, listwise loss; ≈ $12), B a calibration term in the same run,
  C the serving cascade ($0 to decide), D the H100/H200 latency sweep first (RunPod H100 SXM $3.49/h, H200 $4.59/h,
  low stock; AWS had none), E a prefix-LM (bidirectional state) pilot (≈ $5).
- Eikos report: 3 of 1,991 predictions have a `correct` flag that a 0.5-threshold recomputation does not reproduce;
  its own flags are used.
- 01:05 update: the fork's `qwen35_4b_tree` (95.6) landed meanwhile; ensembles.md regenerated with it as the primary:
  + `tree_4b_combo` 95.9, + the 27B 96.3, + both 96.5; cascade to the 27B average at 7% deferred 96.1. The memo's gates
  now refer to 95.6.

### 2026-09-24 23:40 PDT: everything combined scores 94.5 on eval2, the best of our runs, 2.7 behind Jev (fork session)

- Run: `tree_4b_combo` (`scripts/run_tree_combined.sh`, R3=1).
  - Recipe: tree + Qwen3-4B-Instruct-2507 + LoRA r64, every option listed in the question (`data/ova/`), hf + synthetic
    + hardcases_nb + hardcases_r3 with r2_*/r3_* uncapped.
  - Batching: MBT 8192 × GA 4, 51,826 questions, 967 steps, g5.xlarge.
  - It differs from `tree_4b_instruct_r3` only in the option lists.
- eval2 (paired):
  - **94.5**: binary 96.0, multiclass 97.5, multilabel EM 85.9.
  - vs `tree_4b_instruct_r3` 93.3: 60 / 37, p = 0.025. The option lists stack with round 3.
  - vs `tree_4b_combo_r2` 92.9: 63 / 31, p = 0.001. Round 3 stacks with the option lists.
  - vs `tree_4b_instruct_r2x64` 92.7: 75 / 40, p = 0.001.
  - vs Jev 97.2: 27 / 82, p = 1e-7. The gap narrows from 4.5 to 2.7 points.
  - It matches the 50/50 ensemble of the 27B teacher with `tree_4b_ova` (94.5), with one 4B model.
- Dev benchmark: 82.7, the same as Jev (230 / 230) and the control. This benchmark cannot rank these models.
- Validation 92.5, loss 0.126.
- Latency: same architecture and option format as `tree_4b_combo_r2`, so its vLLM numbers apply (JOURNAL 15:05). The
  vLLM path was not re-scored for this run; B's and C's matched transformers within 0.1.
- Cost: g5.xlarge 11:59–23:38 ≈ $11.70 (terminated; SG and key pair deleted).
- Serving: merge with `vllm_tree merge --model-id Qwen/Qwen3-4B-Instruct-2507 ...`, then serve with `--options-in-question`.

### 2026-09-24 18:25 PDT: option pointers lose about a point and are only ~1.1x faster, so a dead end on vLLM (fork session)

- Idea (the hybrid "read deeply once, score the options cheaply"): number the options once in the question and let each
  leaf say only "option k" (`personal_jev/options.py` pointers=True, `data/ptr/`, serve `--option-pointers`), instead
  of repeating the option's description at its leaf.
- Run: `tree_4b_combo_ptr`, the recipe of `tree_4b_combo_r2` (B) with only the leaf text changed. 18.7K questions, 232
  steps, g5.xlarge.
- Accuracy vs B (paired):
  - eval2: 92.0 vs 92.9 (41 / 58, p = 0.11); multiclass 94.3 vs 95.8, multilabel 80.9 vs 84.3, binary 94.9 vs 94.4.
  - Dev benchmark: 82.7 vs 83.5 (88 / 116, p = 0.06).
  - vLLM path: 91.9 / 82.7.
  - The loss is where the pointer applies: the readout position no longer holds the option's text.
- Latency, `scripts/bench_options.py`: vLLM, same A10G, in-process, cold prefix, p50, `reports/tree_4b_combo_ptr/bench_options_*.json`.
  - Pointers are 1.00–1.38x faster: 1 × 3 options at 512 tokens 136 → 135 ms; 16 × 8 at 512 1,146 → 833 ms; 16 × 64
    at 2,048 11.8 → 10.7 s.
  - Why so little: vLLM still receives one full prompt per option (text + question + option list + leaf). Prefix caching
    saves the compute, but 16 × 64 options means 1,024 prompts and 2–4M submitted tokens to hash and schedule per
    request, whatever the leaf length.
  - A real many-options speed-up needs one sequence per question with a readout at every option (e.g. vLLM per-token
    pooling), which means a new readout and training.
- Cost: g5.xlarge 15:17–18:23 ≈ $3.10 (terminated; SG and key pair deleted). The Jev sweep was skipped: it would not
  change the verdict.

### 2026-09-24 16:18 PDT: Qwen3.5-4B scores 93.7 on eval2, our best; Eikos-4B zero-shot 92.8 (session "SelfJev state of play")

- **Run** `qwen35_4b_r2x64` (`scripts/run_qwen35.py`, pipeline `scripts/run_qwen35_gpu.sh`, launcher `scripts/aws_qwen35.sh`):
  - Qwen3.5-4B (rev `851bf6e8`), LoRA r64 / alpha 128 on q/k/v/o + in_proj_qkv/z/b/a + out_proj (57.5M trainable).
  - Data: the `tree_4b_instruct_r2x64` mix (hf + synthetic + hardcases_nb, r2_* uncapped), **training texts ≤ 2,048 tokens**
    (17,435 questions kept, 1,484 dropped). One epoch, 769 steps, grad accumulation 4, lr 2e-4, 3.8 h on one A10G.
  - Training scores each candidate as its own full sequence (14.3M pair tokens): the Qwen3.5 cache writes its recurrent
    state in place, so the tree's shared-root backward pass is not available. Inference shares the text by forking the native
    cache; check vs full sequences: max |Δscore| 0.10 (bf16).
  - Validation (≤ 2K-token items, not comparable with the tree runs' mix): 74.3 → 81.4 (150) → 86.0 (300) → 88.5 (769, best).
- **eval2** (`reports/eval2/summary.md`; reports `reports/qwen35_4b_r2x64/eval2`, `reports/eikos_4b/eval2`, `reports/qwen35_r1/eval2`):

  | model | eval2 | binary | multiclass | multilabel EM | old test |
  |---|---|---|---|---|---|
  | Jev | 97.2 | 97.8 | 98.1 | 94.2 | 82.7 |
  | **qwen35_4b_r2x64** | **93.7** | 95.6 | 95.1 | **86.6** | **83.4** |
  | tree_4b_instruct_r3 (Qwen3 Instruct, round-3 data, 51.9K q) | 93.3 | 95.1 | 96.1 | 84.3 | 82.8 |
  | Eikos-4B, zero-shot (our mapping, as for Jev) | 92.8 | 94.9 | 95.8 | 82.5 | — |
  | tree_4b_instruct_r2x64 (same data, Qwen3 Instruct) | 92.7 | 94.6 | 95.4 | 83.5 | 82.7 |
  | Qwen3.5-2B challenger, round-1 data | 84.3 | 87.5 | 88.7 | 68.8 | 79.9 |

  - Paired (only-row / only-other): vs r2x64 73 / 53, p = 0.09; vs r3 65 / 57, p = 0.53; vs Eikos 75 / 56, p = 0.12;
    vs Jev 21 / 91, p = 1e-11 (Jev still +3.5). Eikos vs Jev 20 / 109.
  - Long texts, although it never trained on > 2K tokens: > 2,048 tokens 97.6 (r2x64 95.7, Jev 98.9); > 4,096 97.0
    (r2x64 94.6, Jev 98.8). Sarcasm 92.6 (r2x64 86.6), multi-positive 88.2 (86.3); numeric 80.4 and temporal 82.8 unchanged.
  - Old test 83.4: the first run above Jev's 82.7 there. Binary ECE on eval2 0.024 (Jev 0.061).
  - Either Qwen3.5-4B or Eikos right: 96.5% of eval2 (their errors differ).
- **Speed** (`reports/qwen35_4b_r2x64/bench.json`, same A10G, transformers, forked cache, branch batches of 16; p50 ms) vs the
  Qwen3 tree R1 transformers path (`reports/latency_optimization_2026-09-24/results.md`): 512 × 1 q 239 vs 160; 2K × 16 q
  1,300 vs 967; 8K × 1 q 1,988 vs 1,777; 8K × 16 q 3,332 vs 2,506. **Slower**, 1.1–1.5×: at ≤ 8K tokens linear attention does
  not pay for the per-batch cache copies. vLLM ≥ 0.30 with its hybrid prefix cache (as Eikos ships) is untested here.
- **Verdict:** best eval2 and old-test scores, but not a significant gain over the Qwen3 Instruct tree (p = 0.09 on the same
  data, 0.53 vs round 3), with 3× less training data than round 3 and texts ≤ 2K in training. Worth: round-3 data on this base,
  a vLLM serving path, and (cheap) a Qwen3.5-4B + Eikos ensemble check. Cost ≈ $4.75.

### 2026-09-24 15:35 PDT: round 3 on the Instruct base: 93.3 on eval2, only +0.6 over round 2 (not significant)

- Owner: Jev classifier with Qwen reranker.
- Run: `tree_4b_instruct_r3`.
  - Recipe: `configs/tree_4b_instruct_r3.json` = Qwen3-4B-Instruct-2507, tree, LoRA r64, max_length 8192.
  - Data: hf + synthetic + `hardcases_nb` + `hardcases_r3` (sha `d20ecb98…`), r2_*/r3_* uncapped. 51,853 questions
    after 1,934 overlength drops; 910 steps.
  - Hardware: g6e.2xlarge (L40S) us-east-2, MBT 16384 × GA 2 (same 32K-token effective batch as the control), ≈ 14 s/step,
    3.9 h. Cost ≈ $9.25, terminated.
  - Best checkpoint: step 900 (val loss 0.1447, val acc 91.7%, still improving at the end); reload exact.
  - Reports: `reports/tree_4b_instruct_r3/{validation,test,eval2}`; adapter `runs/tree_4b_instruct_r3/adapter`.
- Scores:

  | model | eval2 | binary | multiclass | multilabel EM | old test |
  |---|---|---|---|---|---|
  | tree_4b_instruct_r3 | **93.3** | 95.1 | 96.1 | 84.3 | 82.8 |
  | control `tree_4b_instruct_r2x64` | 92.7 | 94.6 | 95.4 | 83.5 | 82.7 |

- Paired tests on eval2 (only-row / only-other):

  | vs | only-row / only-other | p |
  |---|---|---|
  | control | 62 / 50 | 0.3 |
  | r2b | 96 / 41 | 3e-6 |
  | tree_4b_ova | 86 / 51 | 0.004 |
  | Jev | 21 / 99 | 3e-13 |

  - Old test vs control: 92 / 87 (p = 0.77). vs Jev: 216 / 212, a tie.
- Verdict:
  - This is the highest eval2 score so far, but 35K more verified hard cases buy only a non-significant +0.6 on top of
    round 2's ~7K. More of this kind of data has hit diminishing returns.
  - Jev still leads by 3.9 points; multilabel EM (84.3 vs 94.2) is the biggest gap.
  - Next levers: the options-in-question format (fork's runs A/B, in flight), teacher ensembles / distillation, and
    multilabel-specific work.
  - Updated `docs/findings.md` (1, 1b), `docs/leaderboard.md`, the ledger and the eval2 summary.


### 2026-09-24 15:05 PDT: combined recipe B, the best accuracy so far on both test sets; latency on vLLM (fork session)

- Run: `tree_4b_combo_r2` (`scripts/run_tree_combined.sh`, R3=0).
  - Recipe: tree + Qwen3-4B-Instruct-2507 + LoRA r64, every option listed in the question (`data/ova/`), hf + synthetic
    + hardcases_nb with the r2_* families uncapped.
  - Batching: MBT 8192 × GA 4, 18,676 questions, 240 steps.
  - Otherwise identical to `tree_4b_instruct_r2x64`.
- Accuracy vs that control (paired):
  - eval2: **92.9** vs 92.7 (45 / 42, p = 0.83).
  - Old test: **83.5** vs 82.7 (121 / 94, p = 0.08); Jev scores 82.7 (p = 0.22).
  - By type, old test: multilabel 59.0 vs 52.9, multiclass 84.4 vs 83.7, binary 90.0 vs 90.9.
  - Validation 88.1 vs 85.8.
  - So on the Instruct base the option lists help mainly the old test's multilabel questions and tie on eval2.
- Serving path: merged LoRA (bf16) + vLLM, via `scripts/eval_vllm.py` → `reports/tree_4b_combo_r2/{eval2,test}_vllm`.
  - Scores: eval2 **93.02**, old test **83.52**; merging and vLLM cost no accuracy.
  - Throughput: all 1,991 eval2 questions in 144 s, 3,471 old-test questions in 104 s.
  - `pjev serve` / `vllm_tree serve` have a new `--options-in-question` flag (`src/personal_jev/options.py`, shared with
    `scripts/options_in_question.py`; test in tests/test_server.py).
- Latency, end to end from the Mac (p50, 10 rounds, `reports/latency/requests_combo.jsonl`; box RTT 67 ms, OpenRouter 7 ms):

  | text | Jev (1 / 16 q) | combined, 1 q | combined, 16 q |
  |---|---|---|---|
  | 8 tokens | 133 / 124 ms | 125 ms | 471 ms |
  | 512 | 124 / 145 ms | 204 ms | 566 ms |
  | 2,048 | 138 / 158 ms | 429 ms | 882 ms |
  | 4,096 | 141 / 147 ms | 770 ms | 1,336 ms |

  - Against the round-1 reranker on vLLM: the option lists cost about +120 ms at 16 questions (each question carries its
    list) and nothing at 1 question. The A10G is still the limit.
- Cost: g5.xlarge 11:58–15:02 ≈ $3.10 (terminated; SG and key pair deleted) and Jev $0.02.

### 2026-09-24 12:40 PDT: docs site glossary and hover definitions (cloud session; $0)

- New `docs/glossary.md` (test sets, data rounds, trap tags, models, run-name decoder, metrics, services) in the top nav.
- Hover tooltips for shorthand on every page: `docs/.includes/abbreviations.md`, auto-appended by `pymdownx.snippets`.
  Add a line there when a new term appears on the site.

### 2026-09-24 11:50 PDT: docs site and cleanup (cloud session, branch `claude/modest-shannon-epq8g4`; $0, nothing run)

- **What:** every finding of the project, formatted as a docs site built with Zensical from `docs/` (`zensical.toml`,
  GitHub Pages workflow `.github/workflows/docs.yml`). New pages: `index`, `findings` (24 findings with evidence),
  `leaderboard` (embeds the generated eval2 summary and the ledger), `speed`, `dead_ends`, `stock_model`,
  `challengers`, `data`, `landscape`, `next`, `costs`, `how_it_works`, `reproduce`. Numbers copied from the generated
  tables and report files; the 27B teacher's eval2 score re-computed from `reports/teacher/qwen38_27b_eval2.jsonl`.
- **Cleanup:**
  - README rewritten as a short landing page; its detailed 0.6B/4B/8B sections moved to `docs/stock_model.md`.
  - `experiments.md` restructured: current conclusions first, done ideas moved out of the open-ideas table, and the
    ledger sorted by eval2 (`scripts/ledger.py` now sorts that way and links Jev/Astra rows to their real reports).
  - Absolute `/Users/julien/...` links in `reports/*.md` made repo-relative; `tmp/pdfs/` page renders removed; the two
    review PDFs moved from `output/pdf/` next to their sources.
- **Merge note:** other sessions edit `docs/experiments.md` and this file on `master`; merge this branch with care.

### 2026-09-24 11:50 PDT: combined runs started; the 10:17 stop was not the fork session; LFS pointers fixed (fork session)

- The unlogged 10:17 PDT `stop-instances` was not this session. It never calls stop-instances; its last AWS action that
  day before 11:58 was `terminate-instances` on its own box (selfjev-tree-ova-kd) at 06:19 PDT.
- After commit ae5a581 the working tree held Git LFS **pointer files** for data/hardcases*.jsonl, data/ova/hardcases*.jsonl
  and data/hardcases_r3.jsonl (134-byte files). `git lfs checkout` restored them from the local LFS store; the hashes match
  the LFS oids and git status is clean. Check file sizes before syncing data to a box.
- The user asked for all winning approaches combined and trained, then accuracy and latency measured. The owner of the
  round-3 rerun agreed; runs A and B are in In flight.

### 2026-09-24 10:45 PDT: partial round-3 checkpoint scores 90.8 on eval2, inconclusive (the run was stopped at step ≈ 500 / 915)

- Owner: Jev classifier with Qwen reranker. Scored `runs/tree_4b_instruct_r3_step300`, the best-validation-loss checkpoint
  saved before the 10:17 stop (see below). Reports: `reports/tree_4b_instruct_r3_step300/{eval2,test}`.
- Scores:

  | checkpoint | eval2 | old test |
  |---|---|---|
  | tree_4b_instruct_r3_step300 (partial) | **90.8** | 81.5 |
  | control `tree_4b_instruct_r2x64` (finished) | 92.7 | 82.7 |

- Not a verdict on round 3.
  - Step 300 of 915 had seen about a third of the 52K-question mix, at peak learning rate with no decay.
  - The control finished its schedule.
  - A full round-3 run (~10 h on an A10G, ~$10) is needed to judge the data.
- Cost ≈ $6.25. Box terminated; SG, key pair and pem deleted. Nothing of this session runs in AWS.


### 2026-09-24 10:42 PDT: Qwen3.5 / Qwen3.8 as the next base, and Eikos-4B (session "SelfJev state of play"; $0, nothing run)

- **What exists.** Qwen3.8 has no small dense model: only 27B (`qwen3_5_text`, 48 linear-attention + 16 full layers), a
  180B MoE "Flash-Next" and a 2.4T MoE. Qwen3.5 has 0.8/2/4/9/27B plus Base variants; 4B = 32 layers, 24 Gated DeltaNet +
  8 full attention, hidden 2560, 262K positions.
- **We already have a Qwen3.5 result**, in the Codex challenger worktree (`~/.codex/worktrees/1d33/SelfJev`,
  `reports/challengers/qwen35`, trainer `scripts/run_challenger.py`, scorer `src/personal_jev/challengers.py`):
  Qwen3.5-2B + LoRA r16 on all its projections (DeltaNet `in_proj_*`/`out_proj` included), shared document with the
  native cache (recurrent state + KV) forked per branch, round-1 data only. Old test **79.9%** (tree 4B 81.6, stock 4B
  80.3, 0.6B 73.5); 853 steps in 17 min on an L40S. Never scored on eval2.
- **Speed, same L40S, p50 ms** (`bench.json`): Qwen3.5-2B vs tree 4B: 512 tok × 1 q 125 vs 114; 2K × 16 q 319 vs 339;
  8K × 1 q 394 vs 805; 8K × 16 q 765 vs 1,050. Linear attention pays off only on long texts; at ≤2K the MLPs dominate.
- **Eikos-4B** (`caiovicentino1/Eikos-4B`, MIT, created 2026-09-23): a full fine-tune of Qwen3.5-4B, distilled from
  GLM-5.3-Flash on finance/rules data; options as letters, softmax over the letter logits; vLLM ≥ 0.30 with
  `--enable-prefix-caching --mamba-cache-mode all` shares the state across questions (the card reports vLLM 0.11 lost
  3–6 points on batched long shared documents). Own-harness claims: JevBench public hard 72.1 (Jev 73.0 on the official
  leaderboard), long context to 32K trained, ECE 0.033. Not comparable with our numbers.
- Proposal (awaiting the user's OK on the GPU spend): open idea "Qwen3.5-4B tree-equivalent" in experiments.md.

### 2026-09-24 10:36 PDT: survey of open "Jev-like" models on Hugging Face (session "SelfJev state of play")

- Read the model cards of the trending text-classification models; nothing downloaded or run; $0.
- Two camps. Small encoders, 0.15–0.4B: Laya (ModernBERT / mmBERT), open-jev-deberta-v3-large, rlcd-modernbert-151m
  (GLiClass), plus MLX / CoreML ports. LoRA on decoders with answer-token readout, 0.6–27B: kev 0.5/0.8/4/9B and decider
  0.8/2/4/35B-A3B (Qwen3.5 bases), openjev (Qwen3.5 0.8/2/4B), Bespoke-Nimble-9B (Qwen3.5-9B), AutoJev-27B (Qwen3.8-27B),
  Lumma-fev-0.6b (own base).
- Their claims, each on its own benchmark and not comparable with ours: AutoJev-27B 84.6 vs Jev 82.8; kev-4b beats Jev in
  distribution but trails out of domain (0.817 vs 0.857); kev-0.8b trails Jev everywhere; decider-35b-a3b JevBench hard
  0.676, decider-4b 0.541. Small models advertise speed (33–46 ms vs a quoted 236–276 ms for Jev; we measured 143–178 ms).
- Same pattern as ours: sub-1B trails (our 0.6B −17.7 on eval2, jina 0.6B 73.3), 4B and up is where quality is. Most
  decoder entries use our recipe (LoRA, logit readout, no generation). Many use Qwen3.5 bases, whose linear-attention layers
  our tree cannot branch.
- "JevBench" public items exist and several cards report on them: a shared yardstick. Open idea added.

### 2026-09-24 10:17 PDT: round-3 training box stopped by an unlogged `aws ec2 stop-instances` from this Mac

- Owner of the box: Jev classifier with Qwen reranker (`i-01e7e056786127d8e`, "personal-jev-instruct-r3", tagged, listed in
  In flight).
- What happened, per CloudTrail:
  - `StopInstances` at 17:17:57 UTC by `julien@connectly.ai`, from this Mac's IP.
  - User agent `aws-cli … md/command#ec2.stop-instances`: a CLI call, not the console.
  - No session logged it. Training was at step ≈ 500 of 915.
  - Fork 2 (curve / capacity session): not this session. Its scratchpad and task logs contain no `stop-instances`; its only
    lifecycle calls were `terminate-instances` on its own four boxes, the last at 03:10 PDT, and it was idle from 03:17.
- Rule for every session: **never stop, terminate or modify another session's box.** Check JOURNAL In flight first; if a
  box looks orphaned, ask its owner session or the user.
- Recovery (user's choice): score the best checkpoint saved before the stop.
  - That is step 300: val loss 0.176, val acc 89.2%. Step 500 was 0.178 / 89.2, so it wasn't saved.
  - The box restarted as a g5.2xlarge, since its AZ had no g5.xlarge capacity. Results in the next entry.
- Validation trajectory: 78.5 (init) → 85.3 (100) → 87.8 (200) → 89.2 (300) → 89.5 (400) → 89.2 (500).
  - This validation set includes round-3 questions, so it does not compare with the control's 85.8.

### 2026-09-24 10:32 PDT: review of Laya (NandhaKishorM/laya), an open "Jev-style" engine (session "SelfJev state of play")

- What: read the repo (README, BENCHMARKS pointers, `laya/common.py`, `laya/agent.py`) at commit `970dc8c`. Nothing was run
  or downloaded beyond the git clone; $0.
- Architecture: a bidirectional encoder (ModernBERT-large 421M for English, mmBERT-base 322M multilingual), one sequence per
  question `[CLS] type question [SEP] [MASK] opt0 [MASK] opt1 … [SEP] state [SEP]`, all options in one listwise row. A new
  2-layer transformer head + MLP scores each `[MASK]`; softmax over options. `noul` is a 2-option choice (false/true),
  `score` a softmax over levels. Trained end to end with a GRPO-style policy gradient on proper-scoring-rule rewards
  (log + spherical + RPS), which they call RLCD. A script/language router picks one of three checkpoints.
- Limits it documents: the state is **truncated** to max_len − head_max_len (≈320 tokens on `laya`, ≈768 on multilingual;
  up to 8K opt-in), options share a 192–256-token budget (Banking77 0.425 vs Jev 0.870), base checkpoints are near chance
  zero-shot on its own typed-decisions set (0.36 vs 0.318 random; 0.766 only after fine-tuning on that set's train split),
  negation and `noul` label-following failures, over-confident before temperature fitting (ECE 0.466 → 0.081).
- Its Jev numbers are third-party published, on different samples and prompts: not comparable with ours. Its Jev latency
  (236–276 ms p50) is slower than what we measured (143–178 ms, `reports/latency/summary.md`).
- Relation to our work: the listwise idea (a candidate sees its alternatives) is what `tree_4b_ova` added (+1.0 on eval2).
  The new-head-on-encoder idea resembles our custom model, but Laya keeps state and options in one sequence, so they
  interact in every layer. Closest measured analogue: our jina v3.5 0.6B listwise run, 73.3 on eval2 (`docs/jina_model.md`).
- Verdict: Laya is the faster and multilingual option (≈33 ms on a T4, CPU/ONNX), not the more accurate one on long,
  trap-heavy texts; ours reads up to 32K tokens untruncated. Expected, not measured: well below our 92.7 on eval2. Scoring
  it on eval2 is free on the Mac and is logged as an open idea.

### 2026-09-24 06:20 PDT: distilling the 27B into the tree does not help (fork session)

- Run: `tree_4b_ova_kd`, the tree_4b_ova recipe with `teacher_weight` 0.5 and `data/teacher/qwen38_27b_ova_train.json`.
  - The teacher file holds Qwen3.8-27B-FP8 zero-shot probabilities on the 8,372 target-task training rows and gold on
    the 8,000 hf rows.
  - Hardware: g5.xlarge, 241 steps, ≈ $2.90, box terminated.
- Scores vs tree_4b_ova (the same run without the teacher):
  - Old test: 82.5 vs 82.6 (45 / 50, p = 0.68).
  - eval2: 91.0 vs 91.6 (33 / 45, p = 0.21). By type: multiclass +0.7, binary −0.9, multilabel −1.9.
  - Validation: 86.1 vs 86.2.
- Verdict: the 50/50 ensemble's +2.9 on eval2 (94.5%) does not transfer through soft targets on the training rows.
  - Where the teacher disagrees with the verified label (12–20% of rows), the 0.5 weight pulls toward a wrong answer.
  - Untested variants: teacher on multiclass only (where it is strongest), a lower weight, the r64 student.
  - Logged as a dead end for this setting in experiments.md.

### 2026-09-24 04:22 PDT: round-3 data built (38.6K verified), all-options wins, the 27B teacher is complementary (fork session)

- **04:22 (09-24): round-3 training data built: `data/hardcases_r3.jsonl`, 38,628 verified questions** (fork; sha256
  `d20ecb98…`; review `data/hardcases_r3/review/REVIEW.md`).
  - Writers, via `gen_hardcases.py --round3`: GPT-6 Luna 23,336, Gemini 3.8 Flash 9,772, Grok 4.7 5,520 (60/25/14%).
    Never eval2's writers or its NOVEL_* domain lists.
  - Blind Astra judge (OpenAI Batch): 97.0% agree with the authors (simple 98.8, hard 96.5, very hard 95.6). Only
    agreements are kept. 0 states dropped by the 8-gram guard vs eval.jsonl + eval2.jsonl.
  - Splits: train 34,868 / validation 3,760. Types: binary 16,770 / multiclass 12,402 / multilabel 9,456.
  - "None" correct in 7.0% of the multiclass questions offering a none-like option (round 2: 28%); 54% of multilabel
    questions have 3+ positives (round 2: 21%).
  - Cost ≈ $280 (writing $114.5, judge ≈ $165.6 at list batch prices, $4.16 per 1K questions) vs ≈ $250 approved.
  - Training on it: owned by "Jev classifier with Qwen reranker" (Instruct base, r64). Remember `cap_exempt_families` for
    r2_*/r3_*.
- **03:25 (09-24): the 27B teacher is as good as our best model on eval2, and its errors differ from ours** (fork;
  `reports/teacher/`). eval2 is used here for reporting only: nothing was tuned on it.
  - Qwen3.8-27B-FP8 zero-shot on eval2: **91.4%** (binary 93.4, multiclass 97.8, multilabel 75.9); tree_4b_ova 91.6%.
  - Paired: 112 questions only ours gets right, 108 only the teacher (p = 0.84). Either one right: 97.0%.
  - A fixed 50/50 average of the two models' probabilities (nothing fitted) scores **94.5%** (binary 95.7, multiclass 98.5,
    multilabel 85.1); Jev scores 97.2%. That is the case for distillation.
  - Training split: the teacher scored 22,893 of 22,919 train rows (26 overlong), agreeing 80.1% with the labels.
    - Teacher file: `scripts/teacher_scores.py teacher-file --gold-families hf_`. The hf rows keep gold targets
      because the teacher is weaker on them on validation (69.7%).
  - Cost: g6e.xlarge us-east-2 07:06–10:26 UTC ≈ $6.20. Box terminated; SG and key pair deleted.
- **02:45 (09-24): all options listed in the question wins on both test sets** (fork; `tree_4b_ova`).
  - What: `scripts/options_in_question.py` lists every candidate in the question text, in a fixed random order per
    question ("one vs all in context"). Each leaf still judges one candidate, but now sees all the alternatives.
    - The r2b recipe is otherwise unchanged (`scripts/run_tree_ova.sh`, `data/ova/`, same 1,600-per-family cap).
    - 154 overlong questions were dropped at max_length 8192.
  - Old test (3,471 q): **82.6%** vs r2b 81.2% (130 vs 82, p = 0.001), vs tree_4b 81.6% (p = 0.02), vs Jev 82.7%
    (p = 0.93, tied).
    - By type vs r2b: multilabel 57.8 vs 51.7, multiclass 83.6 vs 82.8, binary 89.2 vs 88.1.
  - eval2 (1,991 q): **91.6%** vs r2b 90.6% (66 vs 46, p = 0.07); Jev 97.2%. Every type is 0.8–1.6 points up.
  - Validation: 86.2 vs 86.1, loss 0.234 vs 0.247.
  - Caveat: one run each. Binary rows, which the transform leaves unchanged, also moved ~1 point, so part of the gain may
    be run-to-run variance.
  - Inference must apply the same transform to requests.
  - Cost: g5.xlarge 23:53–02:46 ≈ $2.90. Box terminated; SG and key pair deleted.
  - The round-3 owner decides with the user whether round 3 uses it.
- **01:30 (09-24): Qwen3.8-27B-FP8 zero-shot as a soft-label teacher, validation check** (fork;
  `scripts/teacher_scores.py`, AWS us-east-2 L40S; scores in `reports/teacher/qwen38_27b_validation.jsonl`).
  - Method: vLLM, thinking off; the answer probability is read from the next-token distribution restricted to the answer
    tokens.
  - Validation, 2,121 questions (hf, synthetic, eval and hardcases validation rows): 82.4% overall.
    - by file: hf 69.7%, synthetic 98.2%, eval (authored) 93.2%, hardcases (Astra-verified) 88.1%;
    - by type: binary 89.4, multiclass 88.4, multilabel 61.1.
  - Same 868 hf + eval validation questions: our r2b 79.8% vs the teacher 72.9% (115 vs 55, p = 5e-6).
    - On the 118 authored ones the teacher leads: 93.2% vs 83.1%.
    - It loses on public-set label conventions and wins on target-task questions.
  - Its probabilities are graded (23% of values within 0.05–0.95, vs 0.8% for Astra's verbalized ones), so it is usable as
    a soft-label teacher for the target-task rows, not the public-set rows.
  - It agrees with Astra-verified labels on 88.1% of hard cases, so it cannot replace Astra as the checker.
  - Its training-split scores are running (for a later, separate distillation ablation, not the round-3 run). A reference
    eval2 score (test: reporting only) follows.

### 2026-09-24 03:35 PDT: Instruct base + round-2 data + r64 scores 92.7 on eval2, the best of our runs

- Owner: Jev classifier with Qwen reranker.
- Run: `tree_4b_instruct_r2x64`, the control for round 3.
  - Recipe: `configs/tree_4b_instruct_r3.json` with `R3=0`: Qwen3-4B-Instruct-2507, tree, LoRA r64 on q/k/v/o, max_length 8192.
  - Data: hf + synthetic + `hardcases_nb`, with the r2_* families uncapped. 18,681 questions, 218 steps.
  - Hardware: AWS g5.xlarge, MBT 8192 × GA 4, about 2.3 h. Cost ≈ $2.45, box terminated.
  - Best checkpoint: the last one (val loss 0.226, 85.8%); reload exact.
- Scores:

  | eval2 | overall | binary | multiclass | multilabel EM |
  |---|---|---|---|---|
  | tree_4b_instruct_r2x64 | **92.7** | 94.6 | 95.4 | 83.5 |

  - Old test: 82.7, identical to Jev (213 / 214, p = 1).
- Paired tests on eval2 (only-row / only-other):

  | vs | only-row / only-other | p |
  |---|---|---|
  | r2b | 90 / 47 | 0.0003 |
  | tree_4b_ova | 78 / 55 | 0.06 |
  | r2b + r64 + MLP | 87 / 59 | 0.03 |
  | Instruct base on round-1 data (88.1) | 123 / 32 | 9e-14 |
  | Jev | 25 / 115 | 5e-15 |

- Verdict: the Instruct base stacks with the data. Most of the gain over r2b is the base, since r2b + r64 alone gives
  90.3.
- Jev still leads by 4.5 points, with multilabel EM 94.2 vs 83.5 the biggest gap.
- Round 3 uses the same recipe plus `data/hardcases_r3.jsonl`.

### 2026-09-24 03:17 PDT — combined levers: round-2b data + LoRA capacity

- Owner: fork 2. Two g5.xlarge (no g6e capacity), max_batch_tokens 8192 × grad_accum 4 (same 32K effective batch), 208
  steps each; ≈ $5.26; both boxes terminated, SG and key pair deleted. Configs `configs/curve/tree_4b_r2b_r64*.json`,
  runner `scripts/run_curve.sh` (tree_* branch now also scores eval2); tables `reports/curve/summary.md`,
  `reports/eval2/summary.md`, ledger.
- `tree_4b_r2b_r64` (r=64, 47.2M params): eval2 **90.3%** vs 90.6 for r2b (44 / 50, p = 0.61); old test 81.2 (= r2b);
  validation 86.6. The +2.1 that r=64 gave on round-1 data is gone on round-2b data.
- `tree_4b_r2b_r64_mlp` (r=64 + gate/up/down, 132.1M params): eval2 **91.3%** (59 / 44 vs r2b, p = 0.17); old test **82.4**
  (129 / 88 vs r2b, p = 0.0065; best old-test score of any of our models); validation **87.0** (best). vs Jev 26 / 144,
  p = 5e-21; Jev 97.2.
  - Slices vs r2b: binary 93.7 vs 92.9, multilabel EM 80.4 vs 78.8, multiclass 94.3 vs 94.1; very-hard tier 89.6 vs 86.5;
    by author Opus +1.1, GLM +1.3, Kimi −0.2; every trap tag with n ≥ 150 improves (+2 to +4: paraphrase, injection,
    numeric, long_state, temporal). Small everywhere, significant nowhere: consistent with a real but sub-point gain,
    not with style overfitting.
- Verdict: capacity and verified data overlap; the best recipes today are r2b data + r=64 + MLP (91.3 eval2) and the fork's
  `tree_4b_ova` (91.6, options listed in the question), within noise of each other and 6 points below Jev. The remaining
  gap is not a capacity or volume problem; it needs data or format changes aimed at the very-hard tier and multilabel
  (80 vs 94). Instruct base + round-2 data + r=64 is training in the "Jev classifier with Qwen reranker" session.

### 2026-09-24 08:17 UTC: T5 adaptation scope correction; initial pilot was decoder-only

- Owner: Codex tree latency/compact. The initial target filter missed native `model.encoder.text_model.layers`; the first adapter has 208 decoder tensors, zero encoder tensors, 2,981,888 trainable parameters. Earlier entries describing full text adaptation are superseded by this audit.
- Initial 73.84% development / 76.80% eval2 and 266.61 ms primary latency remain valid **decoder-only** measurements, archived in `reports/t5_round2b_2026-09-24/decoder_only_audit/`. They cannot decide the intended full-adaptation experiment. Historical R1 reproduction remains valid: all 3,471 old decisions match, 75.37%; eval2 72.98%.
- Fixed exact module coverage and added an actual native full T5 + PEFT unit test, plus independent encoder/decoder first-step gradient audits. Rerun uses `configs/t5gemma2_r2b_full.json`, the unchanged frozen 16,375/1,388 questions, seed and recipe. Correction was discovered after evaluation; no evaluation labels enter training or checkpoint selection.
- H100 attempts failed in all Ohio zones; no instance launched, no H100 compute charge. Corrected smoke/training use our existing L40S `i-087b024b35cff657b`, $3.00424/hour, with the original termination cap. Other sessions' resources untouched.

### 2026-09-24 01:00 PDT: eval2 re-scoring. The Instruct base and rank 64 help on the real task; 0.6B is far behind

- Owner: Jev classifier with Qwen reranker.
  - Scored on AWS g5.xlarge `i-08aed2c38168e5da6`, ≈ $1.12, terminated; SG and key pair deleted.
  - The Mac run was stopped at the user's order: no evals or training on the laptop, now in AGENTS.md.
  - Table: `reports/eval2/summary.md`; lever table in `experiments.md` (eval2 section).
- eval2 accuracy, all trained on round-1 data unless noted:

  | model | eval2 acc % | old test |
  |---|---|---|
  | tree_4b_r2b (round-2 data) | 90.6 | 81.2 |
  | tree_4b_r2 (round-2 data) | 90.4 | 80.6 |
  | **tree_4b_instruct** | **88.1** | 80.4 |
  | **tree r64** | **87.2** | 81.5 |
  | stock 4B pairs | 86.5 | 80.3 |
  | tree + MLP targets | 86.3 | 81.6 |
  | tree_4b | 85.1 | 81.6 |
  | 0.6B stock | 68.8 | 73.5 |

- Paired tests vs tree_4b (only-row / only-ref):

  | model | only-row / only-ref | p |
  |---|---|---|
  | Instruct base | 129 / 69 | 2e-5 |
  | r64 | 77 / 36 | 1e-4 |
  | MLP targets | 62 / 38 | 0.02 |
  | stock pairs | 129 / 101 | 0.08 |

- The old test ranked these the opposite way, or called them ties.
- Round 2 vs r2b: equal overall. r2 is better on multiclass (95.8 vs 94.1) and r2b on multilabel (78.8 vs 75.4). The
  "none" cap only mattered for CLINC.
- Verdict: three independent levers measured one at a time: data +5.5, Instruct base +3.0, rank 64 +2.1.
  - fork 2's combined run (r2b data + r64) uses the reranker base. An Instruct-base + r2b-data (+ r64) run is the
    missing combination.
  - The 0.6B size is out for quality: −17.7 vs stock 4B.

### 2026-09-24 07:58 UTC — T5 matched-R2b pilot: quality shortfall

- Owner: Codex tree latency/compact. Training completed in 3,685 seconds, 228 steps; best validation loss selected the final checkpoint (77.59% validation accuracy, loss 0.379396). Reload matches scores exactly on 32 validation questions. Adapter SHA256 `4c4d1f9d683052f0f2b32196f409a9b46a250255ae84caf49b3288131bfa9c43`, saved locally at `runs/t5gemma2_r2b/adapter/`.
- Fixed unmerged T5 with bounded 16-branch decoder batches: **73.84%** on the 3,471-question development benchmark, **76.80%** on eval2 (1,991 questions); primary same-L40S local latency **266.61 ms p50 / 269.38 ms p95**, 100 fresh-prefix 2K × 16 × 3 requests. [Predictions](../reports/t5_round2b_2026-09-24/decoder_only_audit/t5_r2b/eval2/report.md), [timings](../reports/t5_round2b_2026-09-24/decoder_only_audit/t5_r2b/bench.json), [protocol](../reports/t5_round2b_2026-09-24/README.md).
- Verdict so far: large quality shortfall versus the existing round-2b eval2 report (90.56%); this pilot is not a replacement. Same-GPU tree controls, old-T5 rescore, merged/prefix-cache treatments and conditional hardware follow-up are still running. No test-driven retraining or checkpoint change. Compute spend and resource cleanup remain in progress. Ledger refreshed from report files.

### 2026-09-24 07:19 UTC — prior T5 experiment found; matched round-2b follow-up underway

- Owner: Codex tree latency/compact, original `master`. The user correctly recalled the earlier T5Gemma 2 experiment in the challenger worktree. It already used the pretrained full encoder/decoder and shared cross-KV: 75.37% old development accuracy versus R1 merged tree 81.50%, and 203 versus 297 ms on its L40S 2K × 16 × 3 benchmark. The preceding architecture memo now carries a correction. Historical reports/hashes are preserved under [the new experiment folder](../reports/t5_round2b_2026-09-24/README.md).
- Matched-data pilot: replayed original R2b sampling/length eligibility exactly, 16,375 train / 1,388 validation questions; all original file hashes match. No train/validation overlap in IDs, source IDs or exact states. One epoch, attention LoRA rank 16, LR 2e-4, 228 larger optimizer updates; checkpoint selection by validation loss. This does not isolate data from training recipe compared with the old T5 run's 823 updates.
- Prototype: bounded decoder batches, view-based document cross-cache, optional native decoder common-prefix sharing. 26 local checks pass; real pretrained FP32 independent/shared inference error <= 0.000014. Current validation at step 100: 73.20% question accuracy, loss 0.445829; initial validation 37.25%, loss 1.006185. No new development/eval2 result yet; 2× speed / <=1 pp quality-loss gate is pending. Source snapshots, checks, exact requests and progress are saved in `reports/t5_round2b_2026-09-24/` and `runs/t5gemma2_r2b/`.
- Cloud: user explicitly authorized GPU provisioning in the conversation. Dedicated Ohio L40S `i-087b024b35cff657b`, verified $3.00424/hour, eight-hour terminate-on-shutdown cap at 14:38:54 UTC. Virginia capacity attempts launched no instances; their temporary SG and key are deleted. Final cost and Ohio cleanup pending.

### 2026-09-24 00:11 PDT — correction: LoRA capacity does help, on eval2

- Owner: fork 2. My 22:00 verdict "capacity is not the ceiling" was measured on the old test only and is wrong for the
  target task. Recomputed from the prediction files: on eval2, `tree_4b_r64` scores **87.2%** (77 / 36 vs `tree_4b`,
  p = 0.00014) and `tree_4b_mlp` **86.3%** (62 / 38, p = 0.021) vs 85.1%, with the same adapters that tie on the old test
  (81.5 / 81.6 vs 81.6). The trainer's validation split predicted the ranking; the old test did not.
- Updated: `docs/experiments.md` (conclusion 2, dead-end row struck, idea status), `reports/curve/summary.md` (eval2
  columns in the tree-capacity section, generated), the ledger table (new eval2 column, `scripts/ledger.py`), README.
- Proposed next run (needs the user's OK): round-2b data + r=64 (and + MLP), one A10G each, ≈ $3 each; the two gains have
  only been measured separately. Cost of this correction: $0.

### 2026-09-24 06:27 UTC — next architecture recommendation

- Owner: Codex tree latency/compact. Reviewed current eval2, controlled latency, previous cross-attention implementation, and primary model/paper sources. Recommendation: pretrained encoder–decoder with shared full-token memory and pretrained independent readers; T5Gemma 2 1B–1B is the proposed pilot, with the other session's smaller-tree work as control.
- Evidence and bounded protocol: [architecture memo](../reports/architecture_next_2026-09-24.md). Current eval2: round-2b 90.6% versus Jev 97.2% (`reports/eval2/summary.md`). Current compact experiment's speed gain is 7.4% (`reports/latency_optimization_2026-09-24/acceptance.json`). No proposed architecture has been trained or benchmarked here.
- Findings: our tree already shares the document and avoids generation; the prospective gain must come from cheaper pretrained token processing. The old two-block custom reader does not test a deeply pretrained encoder–decoder. More questions still require more arithmetic. Jev's exact internals and training origin remain undisclosed in the official announcement.
- Cost: $0 new cloud/API spend. Verdict: research proposal only; no new branches, commits, GPU instances or model downloads. Eval2 must stay out of tuning, with a fresh final confirmation set after these test-informed choices.

### 2026-09-24 06:17 UTC — latency/compact work integrated into original master

- Owner: Codex tree latency/compact. At the user's request, moved this session's completed experiment into the original `master` checkout, preserving the newer source and concurrent edits. No new commits. Removed only this session's extra branch/worktree; the other experiment's worktree remains.
- Code and results: [conclusions](../reports/latency_optimization_2026-09-24/conclusions.md), [integration record](../reports/latency_optimization_2026-09-24/integration.json). Compact weights are at `runs/tree_4b_compact_v2/adapter`. Archived the former worktree and its Git history in `runs/latency_optimization_2026-09-24/integration_archive` and verified every one of its 597 regular files. Verified all 24 migrated model/metadata files.
- Verification in the original checkout: 16 focused tree/compact tests passed, 2 real-model tests excluded (previous GPU evidence is in the experiment report). All 190 preexisting files outside the explicitly updated documentation remained byte-identical.
- Completed experiment findings are now available to the other sessions: direct branch-mask allocation preserves scores; vLLM's development quality was checked; compact training reduces branch tokens but fails the predeclared 15% cold-prefix vLLM speed-improvement gate and increases CLINC over-rejection. See measured tables and raw predictions in `reports/latency_optimization_2026-09-24/`. These runs use R1 and have not been evaluated on eval2.
- This session owned `i-0172e64b9d0dc20ac` (`selfjev-tree-compact-20260924`); it is terminated and its security group/key pair are deleted. Root EBS deletion remains asynchronous (`cleanup.json`). The two `selfjev-challengers` instances belong to another session. Faster GPU launches failed due to capacity/quota; no faster-GPU measurements exist from this experiment.
- Cost of this integration: $0 new cloud/API spend. Prior experiment billing has not been reconciled. Verdict: all further work stays in the original branch; compact remains experimental.

### 2026-09-24

- **01:30–02:00: jina-reranker-v3.5 (0.6B, listwise) trained the tree-r2b way** (Synthetic data generation strategy;
  write-up `docs/jina_model.md`, box `selfjev-jina-20260924` g5.xlarge $1.006/h, ≈ 1.5 h ≈ $1.60).
  - What: new backend `jina.py` (state = query, every question/candidate = a passage in one causal context, logit =
    scale·cos(proj(query), proj(passage)) + bias; LoRA r=16 on q/k/v/o + the projector + 2 head scalars), trainer
    `train_jina.py`, `pjev --jina` / `train-jina`, config `configs/jina_r2b.json` = the r2b recipe (hf + synthetic +
    hardcases_nb, max_length 8192, 1 epoch). 16,301 train questions / 11,774 contexts, 346 steps, 72 min on the A10G.
  - Numbers: validation 77.4 (tree 4B r2b 86.1); old test 76.6 (calibrated 75.9; 0.6B Qwen LoRA 73.5, tree 4B r2b 81.2);
    **eval2 73.3** (tree 4B r2b 90.6, Jev 97.2): binary 79.8 / multiclass 83.5 / multilabel EM 40.1; simple 80.6 / hard
    70.7 / very hard 68.5. Zero-shot 58.6 validation, 46.5 eval2. Reload check 0.0.
  - Verdict: behaves like the 0.6B Qwen reranker, not like the 4B: ≈ 17 points behind the tree on eval2, multilabel and
    long/distractor/injection cases worst. Its late-epoch gains equal the 4B's, so it is a slower learner from a lower
    start, not a steeper one. Speed on the same A10G, eval2: jina 58 ms per question vs tree 4B r2b 118 ms
    (`reports/tree_4b_r2b_gpu/eval2_timing`, 90.4 there): only 2× faster for 17 points less. License CC BY-NC 4.0: experiments only.
  - Follow-ups prepared, not run: `configs/jina_r2b_e2.json` (2 epochs), `configs/jina_r2b_r64.json` (r=64 + MLP),
    `scripts/run_jina_followups.sh`.
- **00:40: judge_hardcases.py made crash-safe for large runs** (Synthetic data generation strategy): `submit()` saves
  `review/batches.json` after every chunk and stops cleanly on an OpenAI error (e.g. enqueued-token limit), so a rerun
  submits only the remaining sources instead of paying twice. Pitfall list for the round-3 run sent to the fork session
  (judge ≈ $3.40 per 1K questions ≈ $135 for 40K; Grok 4× Gemini per state; one judge process per review dir; one
  generator per prefix; check the none-correct rate after the build).

- **23:05: first eval2 scores: the round-2 data is worth +5.5 points on the real task, and Jev leads by 6.6**
  (session "Jev classifier with Qwen reranker"; table `reports/eval2/summary.md` via `scripts/eval2_summary.py`).
  - Scores: Jev 97.2%; tree_4b_r2b 90.6%; tree_4b 85.1%.
  - Paired tests: r2b vs r1 142 / 34 (p = 7e-17). r2b vs Jev 24 / 157 (p = 4e-25).
  - Multilabel exact match: 63.9 → 78.8, Jev 94.2.
  - Very-hard tier: 79.8 → 86.5, Jev 96.5.
  - Traps, r1 → r2b (Jev):
    - improved: multi-positive 67 → 80 (96), numeric 67 → 79 (92), temporal 70 → 78 (89), injection 72 → 82 (97),
      sarcasm 72 → 83 (97), distractor 80 → 88 (97);
    - unchanged: paraphrase 83.5 → 83.9 (95).
  - Text length is not a weakness: 1K–4K tokens scores 93.9, >4K 91.6.
  - By author: Opus-written questions are hardest for us (87.7), Kimi's easiest (93.4).
  - Takeaways:
    - The old test's near-tie was a public-label-noise ceiling.
    - Verified target-task data is the lever the old test could not see. The round-1 "saturation" and dead ends need
      re-checking on eval2.
  - How it was scored:
    - `scripts/run_eval2.sh` on this Mac (MPS bf16, `--max-length 16384`), about 22 min per tree model.
    - Jev via `compare_external.py --data data/eval2.jsonl --ours tree_4b/eval2 --only jev --tag eval2`, $0.05
      (a re-run on the corrected file came from cache for $0).
    - tree_4b and r2b were scored on the first export and their ids remapped (`meta.remapped_to`), after checking
      every target, type and candidate list.
- **≈ 21:20–23:40: eval2, the frozen target-task test set, built** (session "Synthetic data generation strategy";
  `data/eval2.jsonl`, sha256 `2fa954592d0a3124…`, review `data/eval2/REVIEW.md`, human spot-check `data/eval2/review/SPOTCHECK.md`).
  - What: 1,991 questions / 647 states, every row split=test. Authors never used for training data: Claude Opus 5.5
    (560 q, $13.05), Kimi K3 (649 q, $5.55), GLM 5.3 (782 q, $2.81). Tiers 673 / 664 / 654 (hard / simple / very hard);
    lengths 177–222 questions per bucket of the 8 → 8K ladder; types 1,016 binary / 593 multiclass / 382 multilabel;
    per-trap n 57–474 (evidence_start 17); multilabel with 3+ positives 245 of 382; `none` offered in 391 multiclass
    questions and correct in 14.8% of them. A third of the calls used domains, genres and instruction styles absent from
    the training brief.
  - Judges: GPT-6 Astra (OpenAI batch, $7.95) and Gemini 3.1 Pro (sync, $3.32), blind; kept only where both equal the
    author: 1,991 of 2,070 (96.2%; Astra alone 97.5%, Gemini alone 97.0%). 0 states dropped by the 8-gram guard.
  - Jev on eval2 (never used for keep/drop): **97.2%** (Jev $0.05; the other session's compare_external run agrees,
    1,981 of 1,991 decisions identical, the rest is Jev's own run-to-run noise). Weakest: numeric, temporal, multilabel.
    On the old test Jev scores 82.7, so most of that gap was public-set label noise.
  - Correction 00:10: the first export (sha `f18549eb…`) used source-format lines, which renumber question ids after a
    drop, so my review answers no longer joined and I reported Jev 95.2%. The file now holds expanded rows with the raw
    ids (sha `2fa95459…`, same 1,991 questions and targets); `data/eval2/review/id_map_sourceformat_to_real.json` remaps
    reports scored on the first export.
  - Cost: $32.72 total, all API. Scoring of tree r1 / r2 / r2b, stock 4B and Jev on eval2 is the other session's job.
  - Verdict: usable now; still LLM-verified only, the 50-question SPOTCHECK is for the user.

### 2026-09-23

- **23:35: what TypeSafe discloses about Jev** (fork; public web, no spend).
  - Architecture: per MarkTechPost, TypeSafe says Jev is "transformer-based, but it is not a large language model",
    with a "new model architecture, parallel sampler": all outputs come from one pass, with no token-by-token
    generation.
  - Questions run "in parallel and in isolation against the same state" (docs).
  - Limits: "64k tokens per request; 32k tokens for `state` plus the longest question" (docs/models); rate limit
    250K tokens/s. This is the shape of our tree: each question sees the state plus itself.
  - Training: "Reinforcement Learning for Calibrated Decisions (RLCD)", with no details. Their benchmark's reference
    answer is the average of GPT-6 Astra and Fable 5.1.
  - Not disclosed: size, base model, data, context details. They "cannot prove the price is unsubsidized".
  - Sources: typesafe.ai/blog/introducing-system-one-models-and-jev, docs.typesafe.ai/models.md,
    marktechpost.com/2026/09/19/typesafe-ai-releases-jev/.
  - Reading, with our own evidence:
    - the gap is mostly training, not architecture;
    - model 4B → 8B, adapter r64/MLP and stock → tree each moved ≤ 1.3 points, while 10K verified target-task
      questions moved eval2 +5.5;
    - candidates next: soft Astra targets (already paid for), more verified data, a listwise choice branch.
- **23:15: how Jev stays flat** (fork; free analyses of data already paid for).
  - Fit on the 400 Jev requests of the latency sweep: time = 132–137 ms fixed + 2.2–2.6 ms per 1,000 input tokens.
    That is ~400K tokens/s of marginal speed for one request; our tree 4B with vLLM on the A10G does 165 ms per 1,000
    tokens (~6K tokens/s).
  - Jev reads the whole text:
    - on the verified round-2 hard cases (`data/hardcases.jsonl` × `data/hardcases/review/jev_answers.jsonl`), it is
      right on 97.2% of the 107 questions tagged `evidence_end` whose text is over 4K tokens (up to 17.6K);
    - start and middle score 96.8% and 98.8%;
    - its accuracy by text length is 94.7% up to 256 tokens and 97–98% from 2K to 8K+.
    - So it doesn't truncate.
  - Reading: every architecture must touch each token, so the flat curve means a very small cost per token, not "no
    attention". Consistent with a ~0.5–1B-parameter model (or an MoE with ~1B active parameters) on H100/B200-class
    GPUs, or a larger model split over several GPUs.
  - Jev's billed token count for our text is 1.036× Qwen's, so it probably doesn't use the Qwen tokenizer.
- **21:17: tree 4B round 2b result: 81.2%** (`runs/tree_4b_r2b`, `reports/tree_4b_r2b`; box terminated, ≈ $6.70 for
  all of round 2).
  - Overall: vs round 1 81.6 p = 0.39, vs round 2 80.6 p = 0.08, vs Jev 82.7 p = 0.02. Calibrated: 80.9.
  - CLINC is back to 92.0% (round 1: 94.7, round 2: 83.3). In-scope requests sent to `none`: 24 (16, 50).
  - Authored slice: 83.0% (round 1: 78.4, round 2: 81.9, Jev: 94.7).
  - Traps vs round 1: temporal 52 → 69, numeric 44 → 69, multi-positive 44 → 51, long state 76 → 84,
    exception 29 → 57 (small n).
  - TREC dropped 88.7 → 84.7: numeric/description questions sent to `entities`. Cause unknown; single seed.
  - Outside CLINC, rounds 1, 2 and 2b score 80.35 / 80.35 / 80.23. The round-2 data changes only what this test
    barely measures.
  - Verdict: keep `tree_4b` as the aggregate reference. `tree_4b_r2b` is the candidate for the target task, and
    eval2 decides. The CLINC fix came from a test diagnosis.
  - Scripts: `scripts/rebalance_nota.py`, `scripts/run_tree_r2.sh`.
  - Ready for eval2: `scripts/run_eval2.sh` (our 4B models, `--max-length 16384`), and
    `scripts/compare_external.py --data data/eval2.jsonl --ours <run>/eval2 --only jev` for Jev on the same questions.
- **21:10: latency and cost vs Jev, text 8 → 4,096 tokens** (fork; `scripts/latency_sweep.py`,
  `src/personal_jev/vllm_tree.py`; tables in `reports/latency/summary.md`).
  - Setup:
    - the same decisions-API requests from the Mac (California), one at a time, endpoints in random order;
    - Jev through OpenRouter (edge 12 ms away) vs our tree 4B + LoRA (`runs/tree_4b`) on one AWS A10G in us-east-1
      (71 ms away);
    - 1 or 16 choice questions × 3 options, 10 timed rounds, fresh random text each time.
  - Jev: flat 143–178 ms p50 at every size, including 4,096 tokens × 16 questions. OpenRouter's server timing
    (OpenRouter + Jev) is 109–154 ms.
  - Ours, p50 from the Mac (8 → 4,096 tokens):

    | server | 1 question | 16 questions |
    |---|---|---|
    | transformers | 196 → 1,062 ms | 688 → 1,700 ms |
    | transformers, merged LoRA (`--merge`) | 153 → 938 ms | 602 → 1,517 ms |
    | vLLM | 120 → 755 ms | 336 → 1,195 ms |

  - vLLM beats Jev end to end up to 128 tokens with 1 question (120–133 vs 143–165 ms), despite the 71 ms network
    handicap. Jev is 5× faster at 4,096 tokens and 2–7× faster with 16 questions.
  - The A10G is the limit: it processes 6.5–10K tokens/s with vLLM (4.7–6K with transformers). Jev's flat curve means
    its compute for about 6K tokens takes tens of ms: much faster GPUs, a smaller model, or both.
  - Cost with the GPU fully busy ($1.006/h):
    - vLLM $0.005–0.27 per 1,000 requests vs Jev $0.016–0.27: 1.3–3× cheaper, and equal at 4,096 × 16;
    - Jev charges $0.042 per million input tokens and bills about 372 tokens of overhead per request plus about 113
      per extra 3-option question;
    - a g5.xlarge left on all month (≈ $734) beats Jev only above about 7 requests/s sustained, for 512-token requests.
  - vLLM path:
    - merged LoRA (bf16), with vLLM's prefix cache sharing the text between leaves;
    - readout = vLLM's Qwen3-reranker 1-logit head;
    - on the example request it makes the same decisions as the transformers path (max score difference 0.06 logit);
    - engine start takes about 6 min the first time (compilation) and about 1 min cached.
  - Cost: AWS ≈ $0.87, Jev $0.04. Box terminated; SG and key pair deleted.
  - Not measured: the vLLM path's accuracy on the test set, and any GPU faster than the A10G. The L40S was out of
    capacity in every zone.
- **22:00: tree LoRA capacity is not the ceiling** (fork 2; two g5.xlarge, ≈ $1.60, both terminated, SG and key pair
  deleted). Same data and recipe as `runs/tree_4b` (10,080 questions, 84 steps), configs `configs/curve/tree_4b_r64.json`,
  `tree_4b_mlp.json`, runner `scripts/run_curve.sh`; tables in `reports/curve/summary.md`.
  - r=64 on q/k/v/o (47.2M trainable, 4×): **81.5%** test (binary 88.5, AUROC 0.956, multiclass 83.0, multilabel EM 52.3);
    82 run-only vs 84 reference-only, p = 0.94. Validation 81.8% vs 80.2%.
  - r=16 on q/k/v/o + gate/up/down (33.0M, 2.8×): **81.6%** (binary 87.9, AUROC 0.955, multiclass 83.4, EM 51.7);
    72 vs 73, p = 1.0. Validation 81.4%.
  - Both vs Jev: p = 0.07–0.08, unchanged. Family swings (±5–12 points on eval_agent_output, TREC, eval_policy) go both
    ways and are within noise for 26–300-question slices.
  - Verdict: with this data, more adapter capacity fits validation better and moves the test by nothing. Together with
    the data curves and 4B = 8B, the recipe (data + objective), not the model or the adapter, sets the 80–82% level.
    Full fine-tuning is now low priority. Remaining levers: rejection/threshold policy (in progress in the other
    sessions) and new verified data for the binary families.
- **20:40: SST-2's binary gap is a bias, not a reading problem** (`reports/tree_4b/test`, a diagnosis on test only;
  nothing was tuned).
  - SST-2 is held out: no SST-2 data was trained on.
  - The tree ranks SST-2 reviews well (AUROC 0.973, Jev 0.994), but predicts "positive" on 34.7% of reviews when 50%
    are positive.
  - Accuracy is 84.0%; the best possible single threshold would give 91.7% (Jev 96.7%).
  - BoolQ is different: AUROC 0.927 vs Jev 0.965, best threshold only 84.3% vs 83.3% at 0.5. That's a real ranking gap.
  - Across all families, SST-2 and BoolQ account for about 60 of the 63 binary answers the tree is behind Jev.
  - Next step: a label-free fix, see experiments.md "Calibration policy". One option is contextual calibration:
    subtract each question's score on an empty text. Pick it on validation, then confirm on a fresh holdout. It is
    test-motivated now, so an SST-2 gain alone is not proof.
- **20:24: learning curves done: the stock 4B recipe saturates at 80–81%** (fork 2; 10 runs, 8 g5.xlarge 16:05–19:20,
  ≈ $23, all boxes terminated, SG and key pair deleted). Tables and paired tests: `reports/curve/summary.md`; README
  subsection "Data and base-model curves (4B)"; configs `configs/curve/`, runner `scripts/run_curve.sh`.
  - Nested data subsets 25/50/100% of the 10,112-question mix: 77.0 / 78.9 / 80.3 (1 epoch), 79.1 / 79.1 / 79.8
    (2 epochs). About 1.5 points per doubling; the second epoch never helps (best checkpoint inside epoch 1).
  - New task type: +100 / +300 / +1,000 / +3,000 BoolQ training questions → BoolQ test 84.3 / 83.3 / 84.3 / 86.7
    (from 83.3; Jev 90.7); overall 80.0 / 80.9 / 80.9 / 80.9, none significant (p ≥ 0.09).
  - Base model: Qwen3-4B-Instruct-2507 zero-shot 71.3 (binary 84.2) vs 62.8 for the reranker; after LoRA 80.6 vs
    80.3 (p = 0.68). Prompt picked on validation (`reports/curve/instruct_prompt_selection`).
  - Verdict: not a data-volume or model-size problem. Next lever claimed: tree LoRA capacity (r=64, MLP targets;
    `configs/curve/tree_4b_r64.json`, `tree_4b_mlp.json`, `scripts/run_curve.sh tree_4b_r64 tree_4b_mlp`), waiting for
    the user's OK on the spend.
- **20:19: tree 4B round 2b started.**
  - Why: round 2 lost CLINC (94.7 → 83.3%). In the hard-case training data, "none" is the correct answer in 23% of the
    multiclass questions that offer it, vs 8% in round 1.
  - Fix: `scripts/rebalance_nota.py` drops 160 random none-answer train questions to reach 10%, giving
    `data/hardcases_nb.jsonl` with 9,982 questions. Validation is unchanged.
  - Run: `TAG=tree_4b_r2b HARD_TRAIN=data/hardcases_nb.jsonl scripts/run_tree_r2.sh`.
  - Motivated by a test diagnosis: report CLINC with that caveat.
  - Validation during training: step 100 84.9% (round 2: 83.9%), step 150 85.4% (round 2: 85.6%).
- **20:15: stock 4B round 2 (`scripts/run_4b_r2.sh`) stopped before it finished** to free the GPU for r2b. No report
  exists; the stock-vs-tree round-2 control is still open.
- **≈ 19:20–20:10: tree 4B round 2** (`runs/tree_4b_r2`, recipe from the tree session, + `data/hardcases.jsonl`,
  max_length 8192): 80.6% vs 81.6% for round 1 (p = 0.01).
  - Traps improved: numeric +25, paraphrase +14, role reversal +13, injection +10, distractor +9 points.
  - CLINC in-scope requests routed to "none" rose from 16 to 50 of 255.
  - On the other 3,171 questions, rounds 1 and 2 score the same (80.35%).
  - Full analysis: `docs/hardcases_round2.md` and `reports/tree_review_2026-09-23/review.md`.
- **≈ 16:30–19:15: round-2 hard cases, OpenRouter part + blind judge** (session "Synthetic data generation strategy";
  write-up `docs/hardcases_round2.md`).
  - Why: more trap-heavy training data without Claude Code usage limits; the user asked for 1/3 simple / hard / very hard,
    a clean state-length ladder (8 → 8K tokens) and heavy prompt variance so the model learns the task, not one phrasing.
  - How: `scripts/gen_hardcases.py` (system prompt `data/hardcases/BRIEF.md`, random per-call ASSIGNMENT). Gemini 3.8
    Flash $12.87 → 950 states / 2,462 q; Grok 4.7 $8.19 → 319 / 1,022 (reasoning cannot be disabled, 4× Gemini per
    state); GPT-6 Luna $1.62 → 1,676 / 3,988; DeepSeek V4 Flash $0.17 → 458 / 1,264 (stopped early, slow provider).
    Total 3,403 states / 8,736 questions, $22.86.
  - Judge: `scripts/judge_hardcases.py`, GPT-6 Astra reasoning low, blind, OpenAI Batch API (OpenRouter's batch endpoint
    rejects this key). 5 batches, 0 failures, $36.24 for 10,627 questions incl. the 1,891 Sonnet ones; Jev second
    opinion $0.27. Author = judge 95.4% (Grok 98.9, Sonnet 98.3, Gemini 97.6, Luna 96.0, DeepSeek 82.1); tables in
    `data/hardcases/review/JUDGE.md`. 432 questions are author = Astra but Jev wrong.
  - Verdict: pipeline works and resumes; data quality good except DeepSeek; the retrain diagnosis above (CLINC `none`)
    is the data's one known flaw. Nothing in flight from this session; no AWS boxes launched by it.
- **≈ 14:20: custom shared-state model (v1 spec) finished and written up** (fork 2 + the "Synthetic data" fork;
  `docs/custom_model.md`, `reports/custom_diagnostics/`, tests in `tests/test_custom.py`, 0.6B backbone, A10G).
  - As specified (frozen backbone + cross-attention + heads): 39.0%. Joint LoRA alone: 39.7% (p = 0.32). With the
    similarity term + joint LoRA (`runs/custom_sim_lora`): 58.2%; distillation from the stock 0.6B teacher: no gain.
  - Why: label memorization, binary head at chance (text and question never meet inside the backbone), and the frozen
    features already match unseen labels better than the trained heads (MaxSim 75–77% vs 23–28%).
  - Speed: 38–43× faster than stock pairs for 16 × 3 questions on 8K–16K-token texts. Its lesson (share the text, keep
    deep joint reading) led to the tree scorer.
  - Engineering notes: MPS caches one graph per tensor shape, hence shape buckets in `custom.py`; an explicit attention
    mask was 1.7–2.2× slower for identical outputs and was removed.
- **Hard-case data, Sonnet part:**
  - 8 Claude Sonnet sub-agents wrote 700 sources / 1,891 questions (`data/hardcases/raw/h*`, brief
    `data/hardcases/BRIEF_sonnet_agents.md`).
  - The OpenRouter part and the Astra judge were run by the "Synthetic data generation strategy" session.
  - `scripts/build_hardcases.py` keeps only questions where the blind Astra judge agrees with the author: 10,142 kept.
- **Stock 4B and 8B on AWS** (`scripts/run_model.sh`, one g6e.xlarge, 3.16 h):
  - 4B: 62.8 → 80.3% with LoRA. 8B: 66.2 → 80.7%. 4B + LoRA ≈ 8B + LoRA (p = 0.52).
  - Tables: `reports/scale_comparison.md`.
- **Jev and GPT-6 Astra on the full test** (`scripts/compare_external.py`): Jev 82.7%, Astra 85.8%.
  - The questions we fail most: `reports/external/failures.md`. That's a test-set list: use it to design data, never
    to train on.
  - Decisions-API-shaped endpoint added to `server.py` (`/api/alpha/decisions`).
- **LinkedIn draft and chart:** `docs/linkedin_post.md`, `docs/linkedin_accuracy.png` (`scripts/make_post_chart.py`).

### 2026-09-22

- **Project built:**
  - Qwen3-Reranker yes/no scorer, validation, typed decisions, grouped-loss LoRA training, held-out calibration,
    evaluation harness, benchmark.
  - Data: `data/eval.jsonl` (398 authored questions, blind-reviewed by LLM), `data/hf.jsonl` (16,800 questions from 11
    pinned datasets, 6 of them held-out families), `data/synthetic.jsonl` (2,448 questions).
  - 0.6B on the Mac: 61.0% unmodified → 73.5% with LoRA (`reports/summary.md`).
