# Reproduce

## Install

```bash
uv sync                  # Python 3.12, torch, transformers, peft, pytest (pinned in uv.lock)
uv sync --group data     # + datasets/pyarrow, only needed to rebuild data/hf.jsonl
```

Base checkpoints are pinned to a revision and download on first use (0.6B ≈ 1.2 GB, Qwen3.5-4B ≈ 9 GB). The best
adapters are in [weights/](../weights/README.md) (Git LFS, with a `model.json` each); every other trained adapter lives
in `runs/`, which is not in git.

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

## Serve the best model (CUDA GPU)

```bash
# Qwen3.5-4B + weights/selfjev_4b (eval2 95.8, the default; weights/qwen35_4b_tree: 95.6): the shared-prefix tree, forward only
uv run python -m personal_jev.qwen35_tree serve --adapter weights/selfjev_4b --options-in-question   # :8767
# or through vLLM (separate venv): exact, fast for one question, slow for many (speed.md)
uv run python -m personal_jev.vllm_qwen35 merge --adapter weights/selfjev_4b --out runs/selfjev_4b/merged
~/vllm-env/bin/python -m personal_jev.vllm_qwen35 serve --model-dir runs/qwen35_4b_tree/merged --options-in-question
# Qwen3 tree on vLLM (weights/tree_4b_combo, eval2 94.5): the fastest and cheapest to serve
uv run python -m personal_jev.vllm_tree merge --adapter weights/tree_4b_combo --out runs/tree_4b_combo/merged \
  --model-id Qwen/Qwen3-4B-Instruct-2507 --revision cdbee75f17c01a7cc42f958dc650907174af0554
~/vllm-env/bin/python -m personal_jev.vllm_tree serve --model-dir runs/tree_4b_combo/merged \
  --model-id Qwen/Qwen3-4B-Instruct-2507 --options-in-question
```

All three answer `POST /classify` and the Decisions-API-shaped `POST /api/alpha/decisions`. The vLLM venv:
`uv venv ~/vllm-env --python 3.12 && uv pip install --python ~/vllm-env/bin/python vllm` (0.30.0 measured), run with
`PYTHONPATH=src`.

## Fine-tune on your data, then RLCD (CUDA GPU)

```bash
uv run pjev finetune --data my_train.jsonl --out runs/mine --init weights/selfjev_4b
uv run pjev rlcd --data my_train.jsonl --out runs/mine_rlcd --init runs/mine/adapter
```

Data format, outputs and what RLCD optimizes: [fine-tune and RLCD](finetune.md).

## Tests

```bash
uv run pytest -q                          # tests/test_model.py and the real-model tree tests download the 0.6B model
uv run pytest tests/test_tree.py          # tree: exactness vs standalone runs, branch isolation, gradients
uv run pytest tests/test_qwen35_tree.py   # Qwen3.5 tree: scores and gradients vs full sequences, the tree server
uv run pytest tests/test_finetune.py      # RLCD learns calibrated probabilities; finetune + rlcd end to end (tiny model)
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
uv run python scripts/run_qwen35.py qwen35_4b --stage check-tree --data-dir data/ova --r3 --tree   # tree vs full, GPU
uv run python scripts/run_qwen35.py qwen35_4b --stage train --tag _tree --data-dir data/ova --r3 --tree \
  --train-max-len 8192 --batch-tokens 8192 --grad-accum 4                                        # the best model, 4.1 h L40S
uv run python scripts/run_qwen35.py qwen35_4b --stage eval --tag _tree --adapter runs/qwen35_4b_tree/adapter \
  --data-dir data/ova --sets eval2,test
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
                   qwen35_tree.py (the tree for Qwen3.5: training, TreeServer)   vllm_qwen35.py (Qwen3.5 on vLLM)
                   finetune.py (pjev finetune / pjev rlcd)   options.py (every option in the question)
                   jina.py + train_jina.py (jina listwise)   t5_shared.py (T5Gemma)   challengers.py
scripts/           data builders, run_*.sh GPU pipelines, compare_external.py, summaries (ledger, eval2, curve)
data/              hf / eval / synthetic / hardcases / hardcases_r3 / eval2 (+ briefs and reviews)
configs/           training configs (configs/curve/ for the ablations)
weights/           the best adapters (Git LFS) with model.json: base model, revision, recipe, scores, serve commands
reports/           every eval report, benchmark, review and summary
docs/              this site: findings, write-ups, ledger (experiments.md) and journal
tests/             logic, server, tree, custom, jina, real-model tests
```
