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
# selfjev-4b (weights/selfjev_4b, eval2 95.8): the shared-prefix tree, exact, any number of questions
uv run selfjev serve --host 0.0.0.0 --port 8000
# or through vLLM (separate venv with vllm): exact, fast for one question, slow for many (speed.md)
uv run selfjev merge --adapter weights/selfjev_4b --out runs/selfjev_4b/merged
~/vllm-env/bin/python -m selfjev.cli serve --engine vllm --model-dir runs/selfjev_4b/merged
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
bash scripts/train/jev_soft_box.sh scratch       # on the box (repo + runs/jev_all synced): selfjev finetune, new LoRA r64, lr 2e-4,
                                                 # texts up to 16K, then eval2, the dev benchmark and eval_llm (≈ 9 h, one L40S)
# score any Qwen3.5 adapter: eval2, the dev benchmark (hf + eval test rows), eval_llm
uv run selfjev eval --adapter runs/mine/adapter --data data/ova/eval2.jsonl --out reports/mine/eval2
uv run selfjev eval --adapter runs/mine/adapter --data data/ova/hf.jsonl data/ova/eval.jsonl --split test --out reports/mine/test
uv run selfjev eval --adapter runs/mine/adapter --data data/ova/eval_llm.jsonl --out reports/mine/eval_llm
uv run python scripts/eval/eval2_summary.py      # regenerate reports/eval2/summary.md
uv run python scripts/eval/ledger.py             # regenerate the ledger table in docs/experiments.md
uv run python scripts/eval/calibration_table.py qwen35_4b_tree_scratch_jevall_ qwen35_4b_tree jev   # Brier, ECE, confident mistakes, McNemar
```

### Older recipes

`weights/qwen35_4b_tree` (the previous default), the Qwen3 tree models (`tree_4b_combo` and earlier), the stock
reranker pipeline, the custom, jina and T5Gemma models and their training scripts and configs are at the tag
[`archive/pre-cleanup-2026-09-27`](https://github.com/Jwuthri/SelfJev/tree/archive/pre-cleanup-2026-09-27). Their round-2b and `data/ova/` training copies rebuild byte for byte with:

```bash
uv run python scripts/data/rebalance_nota.py && uv run python scripts/data/options_in_question.py data/synthetic.jsonl data/hardcases.jsonl data/hardcases_nb.jsonl data/hardcases_r3.jsonl
```

Jev and GPT-6 Astra on the same questions (responses cached under `reports/external/cache/`, so reruns cost nothing;
stops at `--budget` USD):

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
src/selfjev/  schemas.py (validation)  formatting.py (templates, prompts)  model.py (stock Scorer)
                   classify.py (typed outputs)  data.py  evaluate.py  calibration.py  benchmark.py  server.py  cli.py
                   tree.py + train_tree.py + vllm_tree.py (shared-prefix tree, Qwen3)
                   qwen35_tree.py (the tree for Qwen3.5: training, TreeServer)   vllm_qwen35.py (Qwen3.5 on vLLM)
                   challengers.py (the Qwen3.5 prompt and forked cache)   finetune.py (selfjev finetune / selfjev rlcd)
                   options.py (every option in the question)
scripts/           data/ (builders, generators, judges, batches), eval/ (summaries, Jev comparison, calibration),
                   train/ (the selfjev-4b recipe), aws/ (aws_launch.sh), docs/ (the site's link extension)
data/              hf / eval / synthetic / hardcases* / batches / eval2 / eval_llm (+ briefs and reviews); data/README.md
configs/           training configs of the ledger runs (configs/curve/ for the ablations)
weights/           the best adapters (Git LFS) with model.json: base model, revision, recipe, scores, serve commands
reports/           every eval report, benchmark, review and summary
docs/              this site: findings, write-ups, ledger (experiments.md) and journal
tests/             logic, server, tree, Qwen3.5 tree, fine-tune, challengers, real-model tests
```
