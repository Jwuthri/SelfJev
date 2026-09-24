#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
export HF_HUB_DISABLE_PROGRESS_BARS=1
cd "$HOME/SelfJev"
uv sync --quiet
.venv/bin/python - <<'PY'
from huggingface_hub import snapshot_download
for model, revision in [('google/t5gemma-2-1b-1b','dd0a2683227859151b1730ca3a63087df5b5f39b'),('Qwen/Qwen3-Reranker-4B','22e683669bc0f0bd69640a1354a6d0aebcfeede5')]:
 snapshot_download(model,revision=revision,allow_patterns=['*.safetensors','*.json','*.txt','*.jinja','*.model'])
 print('DOWNLOADED',model,flush=True)
PY
PYTHONPATH=src OMP_NUM_THREADS=4 .venv/bin/python scripts/check_t5_round2b.py
PYTHONPATH=src OMP_NUM_THREADS=4 .venv/bin/python scripts/train_t5_round2b.py --smoke
PYTHONPATH=src OMP_NUM_THREADS=4 .venv/bin/python scripts/train_t5_round2b.py
