# Reproduce

## Install

```bash
uv sync                  # Python 3.12, torch, transformers, peft, fastapi, pytest (pinned in uv.lock)
uv sync --group data     # + datasets/pyarrow, only needed to rebuild data/hf.jsonl
uv sync --extra gpu      # Linux CUDA boxes: fast Gated DeltaNet kernels (flash-linear-attention)
```

The base model (Qwen3.5-4B, ≈ 9 GB) is pinned to a revision and downloads on first use. The adapter, `selfjev-4b`, is
in [weights/](../weights/README.md) (Git LFS, with its `model.json`: `git lfs pull --include "weights/selfjev_4b/*"`).
New runs write to `runs/`, which is not in git; the training logs of past runs are in `reports/train_meta/`.

## Use

The default model needs a CUDA GPU. Serve it and call it with the SDK ([API](api.md), [deploy](deploy.md)), or from
Python directly:

```python
import json

from selfjev.core.answers import classify
from selfjev.core.options import with_options
from selfjev.engine.tree import TreeServer

scorer = TreeServer("weights/selfjev_4b")  # loads Qwen3.5-4B + the LoRA (merged) on the GPU
request = json.load(open("examples/request.json"))  # the internal schema: {"state": ..., "questions": [...]}
request["questions"] = [with_options(q, q["id"]) for q in request["questions"]]  # the option lists, as the server adds them
result = classify(scorer, request)  # {"questions": [one decision each], "meta": {...}}
```

```bash
uv run selfjev classify examples/request.json   # from the command line; scores the request as given (no option lists)
uv run selfjev --help                           # serve / classify / eval / calibrate / compare / bench / finetune / rlcd / merge / deploy
```

## Serve the best model (CUDA GPU)

```bash
# selfjev-4b (weights/selfjev_4b, eval2 95.8): the shared-prefix tree, exact, any number of questions
uv run selfjev serve --host 0.0.0.0 --port 8000
# or through vLLM (separate venv with vllm): exact, fast for one question, slow for many (speed.md)
uv run selfjev merge --adapter weights/selfjev_4b --out runs/selfjev_4b/merged
~/vllm-env/bin/python -m selfjev.cli serve --engine vllm --model-dir runs/selfjev_4b/merged
```

Both answer Jev's `POST /v1/systemone` (also at `/api/alpha/decisions` and `/v1/decisions`, [API](api.md)) and the
internal `POST /classify`. The vLLM venv: `uv venv ~/vllm-env --python 3.12 && uv pip install --python ~/vllm-env/bin/python
vllm` (0.30.0 measured), run with `PYTHONPATH=src`.

## Fine-tune on your data, then RLCD (CUDA GPU)

```bash
uv run selfjev finetune --data my_train.jsonl --out runs/mine --init weights/selfjev_4b
uv run selfjev rlcd --data my_train.jsonl --out runs/mine_rlcd --init runs/mine/adapter
```

Data format, outputs and what RLCD optimizes: [fine-tune and RLCD](finetune.md).

## Tests

```bash
uv run pytest -q                              # everything, CPU, ~20 s (tiny random models; nothing is downloaded)
uv run pytest tests/engine                    # the Qwen3.5 tree: scores and gradients equal full sequences, the tree server
uv run pytest tests/training                  # RLCD learns calibrated probabilities; finetune + rlcd end to end
```

## Data

New training data is a batch (`scripts/data/grow_batch.sh`, procedure in [data/README.md](../data/README.md)); the sources are
rebuilt with:

```bash
uv run python scripts/data/build_hf.py                                     # data/hf.jsonl from pinned HF revisions
uv run python scripts/data/build_data.py                                   # eval.jsonl + synthetic.jsonl, hash splits, overlap check
zsh -ic 'uv run python scripts/data/gen_hardcases.py --model openai/gpt-6-luna --budget 2 --max-questions 3000'  # resumes
zsh -ic 'uv run python scripts/data/judge_hardcases.py --jev'              # blind judge; never run two at once
uv run python scripts/data/build_hardcases.py                              # keep author = judge, leakage guard
uv run python scripts/data/build_all.py                                    # data/all.jsonl.gz + the catalog
```

## Train and evaluate (on a GPU box, never on the laptop)

```bash
# a tagged box with an SSH-only security group and a shutdown cap (clean-up commands in the script's header)
scripts/aws/aws_launch.sh selfjev-mine 10 "us-east-2:g6e.2xlarge us-east-1:g6e.2xlarge us-west-2:g6e.2xlarge"
# the default model, selfjev-4b: every non-test question of data/all.jsonl.gz, 0.5 × label + 0.5 × Jev
uv run python scripts/train/jev_soft_targets.py  # local and free: runs/jev_all/{train,val}.jsonl.gz
nohup bash scripts/train/selfjev_4b.sh mine > train.log 2>&1 < /dev/null &   # on the box (what to sync: the script's header):
    # a GPU preflight against selfjev-4b's eval2 report, selfjev finetune (new LoRA r64, lr 2e-4, texts up to 16K), then
    # eval2, the dev benchmark and eval_llm for the best and the last checkpoint (≈ 9–10 h, one L40S)
# score any Qwen3.5 adapter: eval2, the dev benchmark (hf + eval test rows), eval_llm
uv run selfjev eval --adapter runs/mine/adapter --data data/ova/eval2.jsonl --out reports/mine/eval2
uv run selfjev eval --adapter runs/mine/adapter --data data/ova/hf.jsonl data/ova/eval.jsonl --split test --out reports/mine/test
uv run selfjev eval --adapter runs/mine/adapter --data data/ova/eval_llm.jsonl --out reports/mine/eval_llm
uv run python scripts/eval/eval2_summary.py      # regenerate reports/eval2/summary.md
uv run python scripts/eval/ledger.py             # regenerate the ledger table in docs/experiments.md
uv run python scripts/eval/calibration_table.py qwen35_4b_tree_scratch_jevall_ qwen35_4b_tree jev   # Brier, ECE, confident mistakes, McNemar
```

### Older recipes

The previous default `qwen35_4b_tree` (adapter in `weights/qwen35_4b_tree`), the Qwen3 tree models (`tree_4b_combo`
and earlier), the stock reranker pipeline, the forked-cache Qwen3.5 engine, the custom, jina and T5Gemma models and
their training scripts and configs are at the tag
[`archive/pre-cleanup-2026-09-27`](https://github.com/Jwuthri/SelfJev/tree/archive/pre-cleanup-2026-09-27), where the
package is `src/personal_jev/`, the CLI `uv run pjev ...` and the scripts sit directly in `scripts/`. Their round-2b
and `data/ova/` training copies rebuild byte for byte, from a checkout of the tag, with:

```bash
uv run python scripts/rebalance_nota.py && uv run python scripts/options_in_question.py data/synthetic.jsonl data/hardcases.jsonl data/hardcases_nb.jsonl data/hardcases_r3.jsonl
```

Jev and GPT-6 Astra on the same questions (responses cached under `reports/external/cache/`, so Jev reruns cost
nothing; Astra's request asks for 8,192 output tokens since 2026-09-27, 6,000 before, so an Astra rerun misses the old
cache and pays again; the run stops at `--budget` USD):

```bash
zsh -ic 'uv run python scripts/eval/compare_external.py --per-hf-family 300 --tag full --only jev --budget 5'
zsh -ic 'uv run python scripts/eval/compare_external.py --data data/eval2.jsonl --ours tree_4b/eval2 --only jev --tag eval2'
zsh -ic 'uv run python scripts/eval/audit_failures.py relabel --limit 40'   # PAID (user OK): blind relabel of failed test questions
uv run python scripts/eval/audit_failures.py report                         # free: reports/audit_2026-09-26/AUDIT.md
```

`selfjev calibrate` fits temperatures only on a report whose every prediction is from the `calibration` split and
selects thresholds only on `validation`; anything else raises `LeakageError`. A calibration file is bound to the model
revision, adapter sha256 and prompt sha that produced it.

## This site

The site is built with [Zensical](https://zensical.org) from `docs/` and `zensical.toml`, and deployed to GitHub Pages
by `.github/workflows/docs.yml` on every push to `master` that touches the docs.

```bash
uv run --no-project --with zensical==0.0.65 python -m zensical serve      # http://127.0.0.1:8000, live reload
uv run --no-project --with zensical==0.0.65 python -m zensical build      # static site in site/
```

Use `python -m zensical` from the repo root: `scripts/docs/docs_links.py`, which points links to repo files outside
`docs/` at GitHub, must be importable. The leaderboard embeds the generated tables (`reports/eval2/summary.md` and the
ledger section of `docs/experiments.md`), so re-running `eval2_summary.py` and `ledger.py` updates the site.

## Layout

```
src/selfjev/       client.py + types.py (the SDK)   server/ (the HTTP API, fine-tuning jobs)   engine/ (qwen35: model,
                   prompt, readout; tree: shared-prefix tree, TreeServer; vllm)   core/ (request schema, option lists,
                   typed answers)   training/ (finetune, RLCD, losses, tree batching)   evaluation/ (eval, calibration,
                   benchmark, stats)   data/ (loading, validation, catalog, paid API clients)   deploy/ (AWS)   cli.py
scripts/           data/ (builders, generators, judges, batches), eval/ (summaries, Jev comparison, calibration),
                   train/ (the selfjev-4b recipe), aws/ (aws_launch.sh), docs/ (the site's link extension)
data/              hf / eval / synthetic / hardcases* / batches / eval2 / eval_llm (+ briefs and reviews), ova/ (the test
                   sets with option lists), all.jsonl.gz (built locally, not in git); data/README.md
deploy/            Dockerfile, docker-compose.yml
weights/           selfjev_4b (Git LFS) with model.json: base model, revision, recipe, scores
reports/           every eval report, benchmark, review and summary
docs/              this site: API, deploy, findings, write-ups, ledger (experiments.md) and journal
tests/             mirrors src/selfjev: core, data, engine, training, evaluation, server, client, deploy (CPU only)
```
