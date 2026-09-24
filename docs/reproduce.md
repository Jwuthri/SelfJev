# Reproduce

## Install

```bash
uv sync                  # Python 3.12, torch, transformers, peft, pytest (pinned in uv.lock)
uv sync --group data     # + datasets/pyarrow, only needed to rebuild data/hf.jsonl
```

Base checkpoints are pinned to a revision and download on first use (0.6B ≈ 1.2 GB). Trained adapters live in `runs/`,
which is not in git.

## Use

```bash
uv run pjev classify examples/request.json                                   # untrained 0.6B reranker
uv run pjev classify examples/request.json --tree --model Qwen/Qwen3-Reranker-4B \
  --revision 22e683669bc0f0bd69640a1354a6d0aebcfeede5 --adapter runs/tree_4b/adapter --dtype bfloat16
uv run pjev serve --adapter runs/lora_pilot/adapter --dtype bfloat16         # http://127.0.0.1:8000
uv run pjev --help        # classify / eval / calibrate / compare / bench / serve / train / train-tree / train-jina ...
```

```python
from personal_jev.model import Scorer
from personal_jev.classify import classify

scorer = Scorer()                         # fp32 on mps/cuda/cpu; Scorer(adapter="runs/lora_pilot/adapter") for LoRA
result = classify(scorer, request_dict)   # {"questions": [...], "meta": {...}}
```

Request format and API: [how it works](how_it_works.md#request-and-response).

## Tests

```bash
uv run pytest -q                          # tests/test_model.py and the real-model tree tests download the 0.6B model
uv run pytest tests/test_tree.py          # tree: exactness vs standalone runs, branch isolation, gradients
```

## Data

```bash
uv run python scripts/build_hf.py                                          # data/hf.jsonl from pinned HF revisions
uv run python scripts/build_data.py                                        # eval.jsonl + synthetic.jsonl, hash splits, overlap check
uv run python scripts/select_prompt.py data/hf.jsonl data/eval.jsonl       # validation-only prompt selection
zsh -ic 'uv run python scripts/gen_hardcases.py --model openai/gpt-6-luna --budget 2 --max-questions 3000'  # resumes
zsh -ic 'uv run python scripts/judge_hardcases.py --jev'                   # blind judge; never run two at once
uv run python scripts/build_hardcases.py                                   # keep author = judge, leakage guard
```

## Train and evaluate (on a GPU box, never on the laptop)

```bash
scripts/setup_gpu_box.sh                  # prepare an AWS box
scripts/run_tree_gpu.sh                   # tree 4B: untrained check, LoRA, evals, benchmarks
scripts/run_tree_r2.sh                    # tree 4B with round-2 data (TAG=..., HARD_TRAIN=...)
scripts/run_tree_instruct_r3.sh           # best recipe (R3=0) and round 3
scripts/run_curve.sh tree_4b_r64 ...      # any config in configs/curve/
scripts/run_eval2.sh                      # score a model on eval2
uv run python scripts/eval2_summary.py    # regenerate reports/eval2/summary.md
uv run python scripts/ledger.py           # regenerate the ledger table in docs/experiments.md
```

Jev and GPT-6 Astra on the same questions (responses cached under `reports/external/cache/`, so reruns cost nothing;
stops at `--budget` USD):

```bash
zsh -ic 'uv run python scripts/compare_external.py --per-hf-family 300 --tag full --only jev --budget 5'
zsh -ic 'uv run python scripts/compare_external.py --data data/eval2.jsonl --ours tree_4b/eval2 --only jev --tag eval2'
uv run python scripts/failures.py         # reports/external/failures.{md,jsonl}
```

`pjev calibrate` fits temperatures only on a report whose every prediction is from the `calibration` split and
selects thresholds only on `validation`; anything else raises `LeakageError`. A calibration file is bound to the model
revision, adapter sha256 and prompt sha that produced it.

## This site

The site is built with [Zensical](https://zensical.org) from `docs/` and `zensical.toml`, and deployed to GitHub Pages
by `.github/workflows/docs.yml` on every push to `master` that touches the docs.

```bash
uv run --no-project --with zensical==0.0.65 python -m zensical serve      # http://127.0.0.1:8000, live reload
uv run --no-project --with zensical==0.0.65 python -m zensical build      # static site in site/
```

Use `python -m zensical` from the repo root: `scripts/docs_links.py`, which points links to repo files outside
`docs/` at GitHub, must be importable. The leaderboard embeds the generated tables (`reports/eval2/summary.md` and the
ledger section of `docs/experiments.md`), so re-running `eval2_summary.py` and `ledger.py` updates the site.

## Layout

```
src/personal_jev/  schemas.py (validation)  formatting.py (templates, prompts)  model.py (stock Scorer)
                   classify.py (typed outputs)  data.py  evaluate.py  calibration.py  benchmark.py  server.py  cli.py
                   tree.py + train_tree.py + vllm_tree.py (shared-prefix tree)   custom.py + train_custom.py (cross-attention)
                   jina.py + train_jina.py (jina listwise)   t5_shared.py (T5Gemma)   challengers.py
scripts/           data builders, run_*.sh GPU pipelines, compare_external.py, summaries (ledger, eval2, curve)
data/              hf / eval / synthetic / hardcases / hardcases_r3 / eval2 (+ briefs and reviews)
configs/           training configs (configs/curve/ for the ablations)
reports/           every eval report, benchmark, review and summary
docs/              this site: findings, write-ups, ledger (experiments.md) and journal
tests/             logic, server, tree, custom, jina, real-model tests
```
