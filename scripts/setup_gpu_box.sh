#!/usr/bin/env bash
# One-time setup on a fresh Deep Learning base AMI (Ubuntu 22.04, NVIDIA driver): uv, the project env, model downloads.
# The repo must already be rsynced to ~/SelfJev. usage: bash scripts/setup_gpu_box.sh [extra HF model ids...]
set -euo pipefail
cd ~/SelfJev
command -v uv > /dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
uv sync --quiet
.venv/bin/python - "$@" <<'EOF'
import sys
from huggingface_hub import snapshot_download
pins = {"Qwen/Qwen3-Reranker-4B": "22e683669bc0f0bd69640a1354a6d0aebcfeede5",
        "Qwen/Qwen3-4B-Instruct-2507": "cdbee75f17c01a7cc42f958dc650907174af0554",
        "Qwen/Qwen3-Reranker-0.6B": "e61197ed45024b0ed8a2d74b80b4d909f1255473"}
for m in ["Qwen/Qwen3-Reranker-4B", *sys.argv[1:]]:
    snapshot_download(m, revision=pins.get(m), allow_patterns=["*.json", "*.safetensors", "*.txt", "*.jinja", "*.py"])
    print("downloaded", m, flush=True)
EOF
.venv/bin/python -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.device_count(), 'GPUs')"
echo "SETUP DONE $(date +%H:%M:%S)"
