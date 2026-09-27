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
uv run selfjev classify examples/request.json                                   # untrained 0.6B reranker, runs anywhere
uv run selfjev --help        # classify / eval / calibrate / compare / bench / serve / train / train-tree / finetune / rlcd
```

```python
from selfjev.model import Scorer
from selfjev.classify import classify

scorer = Scorer()                         # fp32 on mps/cuda/cpu; Scorer(adapter=...) for a stock LoRA adapter
result = classify(scorer, request_dict)   # {"questions": [...], "meta": {...}}
```

The default model needs a CUDA GPU: serve it as below. Request format and API:
[how it works](how_it_works.md#request-and-response).

## Serve the best model (CUDA GPU)

```bash
# Qwen3.5-4B + weights/selfjev_4b (eval2 95.8, the default; weights/qwen35_4b_tree: 95.6): the shared-prefix tree, forward only
uv run python -m selfjev.qwen35_tree serve --adapter weights/selfjev_4b --options-in-question   # :8767
# or through vLLM (separate venv): exact, fast for one question, slow for many (speed.md)
uv run python -m selfjev.vllm_qwen35 merge --adapter weights/selfjev_4b --out runs/selfjev_4b/merged
~/vllm-env/bin/python -m selfjev.vllm_qwen35 serve --model-dir runs/selfjev_4b/merged --options-in-question
# Qwen3 tree on vLLM (weights/tree_4b_combo, eval2 94.5): the fastest and cheapest to serve
uv run python -m selfjev.vllm_tree merge --adapter weights/tree_4b_combo --out runs/tree_4b_combo/merged \
  --model-id Qwen/Qwen3-4B-Instruct-2507 --revision cdbee75f17c01a7cc42f958dc650907174af0554
~/vllm-env/bin/python -m selfjev.vllm_tree serve --model-dir runs/tree_4b_combo/merged \
  --model-id Qwen/Qwen3-4B-Instruct-2507 --options-in-question
```

All three answer `POST /classify` and the Decisions-API-shaped `POST /api/alpha/decisions`. The vLLM venv:
`uv venv ~/vllm-env --python 3.12 && uv pip install --python ~/vllm-env/bin/python vllm` (0.30.0 measured), run with
`PYTHONPATH=src`.

## Fine-tune on your data, then RLCD (CUDA GPU)

```bash
uv run selfjev finetune --data my_train.jsonl --out runs/mine --init weights/selfjev_4b
uv run selfjev rlcd --data my_train.jsonl --out runs/mine_rlcd --init runs/mine/adapter
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

New training data is a batch (`scripts/grow_batch.sh`, procedure in [data/README.md](../data/README.md)); the sources are
rebuilt with:

```bash
uv run python scripts/build_hf.py                                          # data/hf.jsonl from pinned HF revisions
uv run python scripts/build_data.py                                        # eval.jsonl + synthetic.jsonl, hash splits, overlap check
zsh -ic 'uv run python scripts/gen_hardcases.py --model openai/gpt-6-luna --budget 2 --max-questions 3000'  # resumes
zsh -ic 'uv run python scripts/judge_hardcases.py --jev'                   # blind judge; never run two at once
uv run python scripts/build_hardcases.py                                   # keep author = judge, leakage guard
uv run python scripts/build_all.py                                         # data/all.jsonl.gz + the catalog
```

## Train and evaluate (on a GPU box, never on the laptop)

```bash
# a tagged box with an SSH-only security group and a shutdown cap (clean-up commands in the script's header)
scripts/aws_launch.sh selfjev-mine 10 "us-east-2:g6e.2xlarge us-east-1:g6e.2xlarge us-west-2:g6e.2xlarge"
# the default model, selfjev-4b: every non-test question of data/all.jsonl.gz, 0.5 × label + 0.5 × Jev
uv run python scripts/jev_soft_targets.py     # local and free: runs/jev_all/{train,val}.jsonl.gz
bash scripts/jev_soft_box.sh scratch          # on the box (repo + runs/jev_all synced): selfjev finetune, new LoRA r64, lr 2e-4,
                                              # texts up to 16K, then eval2, the dev benchmark and eval_llm (≈ 9 h, one L40S)
# score any Qwen3.5 adapter (reports/qwen35_4b<tag>/)
uv run python scripts/run_qwen35.py qwen35_4b --stage eval --tag _mine --adapter runs/mine/adapter \
  --data-dir data/ova --sets eval2,test,eval_llm
uv run python scripts/eval2_summary.py        # regenerate reports/eval2/summary.md
uv run python scripts/ledger.py               # regenerate the ledger table in docs/experiments.md
uv run python scripts/calibration_table.py qwen35_4b_tree_scratch_jevall_ qwen35_4b_tree jev   # Brier, ECE, confident mistakes, McNemar
```

### Older recipes

`weights/qwen35_4b_tree` (`scripts/run_qwen35.py --stage train --tree`), `weights/tree_4b_combo`
(`scripts/run_tree_combined.sh`) and the configs that read `data/hardcases_nb.jsonl` (`configs/tree_4b_instruct_r3.json`,
`configs/curve/tree_4b_r2b_r64*.json`) need the round-2b file and the `data/ova/` training copies, which are no longer
tracked. Rebuild them first (byte-identical to the removed files: sha256 checked against their LFS oids on 2026-09-27):

```bash
uv run python scripts/rebalance_nota.py && uv run python scripts/options_in_question.py data/synthetic.jsonl data/hardcases.jsonl data/hardcases_nb.jsonl data/hardcases_r3.jsonl
```

```bash
uv run python scripts/run_qwen35.py qwen35_4b --stage check-tree --data-dir data/ova --r3 --tree   # tree vs full, GPU
uv run python scripts/run_qwen35.py qwen35_4b --stage train --tag _tree --data-dir data/ova --r3 --tree \
  --train-max-len 8192 --batch-tokens 8192 --grad-accum 4                                        # qwen35_4b_tree, 4.1 h L40S
bash scripts/run_tree_combined.sh                                                                # tree_4b_combo
```

The scripts of finished experiments (the Qwen3 tree and stock pipelines `run_tree_gpu.sh`, `run_tree_r2.sh`,
`run_tree_instruct_r3.sh`, `run_curve.sh`, `run_eval2.sh`, `run_model.sh`, `setup_gpu_box.sh`, prompt selection, the
custom, jina and T5Gemma models) are at tag
[`archive/pre-cleanup-2026-09-27`](https://github.com/Jwuthri/SelfJev/tree/archive/pre-cleanup-2026-09-27).

Jev and GPT-6 Astra on the same questions (responses cached under `reports/external/cache/`, so reruns cost nothing;
stops at `--budget` USD):

```bash
zsh -ic 'uv run python scripts/compare_external.py --per-hf-family 300 --tag full --only jev --budget 5'
zsh -ic 'uv run python scripts/compare_external.py --data data/eval2.jsonl --ours tree_4b/eval2 --only jev --tag eval2'
zsh -ic 'uv run python scripts/audit_failures.py relabel --limit 40'   # PAID (user OK): blind relabel of failed test questions
uv run python scripts/audit_failures.py report                         # free: reports/audit_2026-09-26/AUDIT.md
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

Use `python -m zensical` from the repo root: `scripts/docs_links.py`, which points links to repo files outside
`docs/` at GitHub, must be importable. The leaderboard embeds the generated tables (`reports/eval2/summary.md` and the
ledger section of `docs/experiments.md`), so re-running `eval2_summary.py` and `ledger.py` updates the site.

## Layout

```
src/selfjev/  schemas.py (validation)  formatting.py (templates, prompts)  model.py (stock Scorer)
                   classify.py (typed outputs)  data.py  evaluate.py  calibration.py  benchmark.py  server.py  cli.py
                   tree.py + train_tree.py + vllm_tree.py (shared-prefix tree, Qwen3)
                   qwen35_tree.py (the tree for Qwen3.5: training, TreeServer)   vllm_qwen35.py (Qwen3.5 on vLLM)
                   challengers.py (the Qwen3.5 prompt and forked cache)   finetune.py (selfjev finetune / selfjev rlcd)
                   options.py (every option in the question)
scripts/           data builders and batches, the selfjev-4b recipe, aws_launch.sh, compare_external.py, summaries
data/              hf / eval / synthetic / hardcases* / batches / eval2 / eval_llm (+ briefs and reviews); data/README.md
configs/           training configs of the ledger runs (configs/curve/ for the ablations)
weights/           the best adapters (Git LFS) with model.json: base model, revision, recipe, scores, serve commands
reports/           every eval report, benchmark, review and summary
docs/              this site: findings, write-ups, ledger (experiments.md) and journal
tests/             logic, server, tree, Qwen3.5 tree, fine-tune, challengers, real-model tests
```
