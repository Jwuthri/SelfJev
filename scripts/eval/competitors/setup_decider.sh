#!/usr/bin/env bash
# decider-4b v2.1. decider-ai 1.4.0 == the decider/ subset in the HF repo (serve.py, systemone.py, engine_v2.py, shared_prefix.py,
# prompt*.py, temperature.py verified byte-identical). Port 8001.
set -euo pipefail
ENV=~/env-decider
[ -d "$ENV" ] || uv venv "$ENV" --python 3.12
uv pip install --python "$ENV/bin/python" "decider-ai[serve]==1.4.0"   # pulls torch 2.14.0, transformers 5.x, flash-linear-attention 0.5.2, numpy<2 (1.4.0 pin)
"$ENV/bin/python" - <<'PY'
import torch, transformers, fla
from fla.ops.gated_delta_rule import chunk_gated_delta_rule
print(torch.__version__, torch.version.cuda, torch.cuda.is_available(), transformers.__version__, fla.__version__)
PY
MODEL_DIR=$("$ENV/bin/python" - <<'PY'
from huggingface_hub import snapshot_download
print(snapshot_download("Mapika/decider-4b", revision="eb5fbdfc9448473ec25e399882912863afbdb70e",
                        allow_patterns=["*.json", "*.safetensors", "*.jinja"]))
PY
)
echo "model dir: $MODEL_DIR"
export DECIDER_MODEL="$MODEL_DIR" DECIDER_DEVICE=cuda
export DECIDER_MAX_REQUEST_TOKENS=16777216   # default 1,048,576 total row tokens: 60 rows x ~17.5K-token state would 413
export DECIDER_SHARED_FORK_GB=4              # default 8; the 89 captured graphs reserve ~25 GB on the 4B (SERVING.md) + 8.4 GB weights
# If start-up dies with torch.OutOfMemoryError: add DECIDER_GRAPH_TOKEN_BUDGET=16384 (or DECIDER_WARMUP=0 to skip graph capture).
nohup "$ENV/bin/uvicorn" decider.serve:app --host 127.0.0.1 --port 8001 > ~/decider.log 2>&1 &
echo $! > ~/decider.pid
until curl -sf localhost:8001/health | grep -q '"ok":true'; do kill -0 $! 2>/dev/null || { echo "server died"; exit 1; }; sleep 5; done   # port refuses connections until graphs are captured
curl -s localhost:8001/health; echo
# kill:  kill $(cat ~/decider.pid)
