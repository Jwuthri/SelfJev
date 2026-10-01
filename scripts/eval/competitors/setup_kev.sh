#!/usr/bin/env bash
# kev-4b (LoRA r16 + pointer head on Qwen/Qwen3.5-4B-Base). Port 8008.
# KEV_REF = GitHub main HEAD 2026-09-29 (the source read for the schema). The repo's own deploy script pins f2bb629d670f5b746f712fc05550a098526c836b (2026-09-25).
set -euo pipefail
ENV=~/env-kev
KEV_REF=0fe8fc97c2bcc247fa3efb6e5c32af4e99770e91
[ -d "$ENV" ] || uv venv "$ENV" --python 3.12        # kev needs >=3.12,<3.14; the repo's .python-version says 3.13 but 3.12 is fine
uv pip install --python "$ENV/bin/python" "kev[serve] @ git+https://github.com/jaredpalmer/kev.git@${KEV_REF}"   # torch>=2.6,<2.9 -> torch 2.8.0 (cu128 wheel), transformers>=5.17, peft>=0.21
uv pip install --python "$ENV/bin/python" "flash-linear-attention==0.5.2" "triton>=3.7.1"   # same two lines as skills/kev-deploy/scripts/kev_serve.py; fla must be EXACTLY 0.5.2 for the fused kernels
"$ENV/bin/python" -c "import torch,transformers,peft,fla;print(torch.__version__,torch.version.cuda,torch.cuda.is_available(),transformers.__version__,peft.__version__,fla.__version__)"
export HF_HOME=${HF_HOME:-$HOME/.cache/huggingface} TRITON_CACHE_DIR=$HOME/.triton-kev TOKENIZERS_PARALLELISM=false
nohup "$ENV/bin/python" -m kev.serve --run "jaredpalmer/kev-4b@139fdd94f1b6a6ad80cc15e08fcb99cac885a101" --host 127.0.0.1 --port 8008 > ~/kev.log 2>&1 &
echo $! > ~/kev.pid
until curl -sf localhost:8008/v1/models >/dev/null; do kill -0 $! 2>/dev/null || { echo "server died"; exit 1; }; sleep 5; done     # no /health route; /v1/models is the probe
grep -m1 -i "fused Qwen3.5 kernels off" ~/kev.log && echo "WARNING: fused kernels off (fla != 0.5.2)" || true
curl -s localhost:8008/v1/models | python3 -c "import json,sys; m=json.load(sys.stdin)['models'][0]; print({k:m[k] for k in ('device','backend','dtype','temperature','cuda_graphs')})"
# CUDA graphs are NOT pre-captured by `python -m kev.serve` (the Modal script warms up via Server.answer + wait_idle).
# Warm up by sending a few requests (states of ~1, 4, 16 short paragraphs) and polling /v1/models .cuda_graphs.pending until 0.
# kill:  kill $(cat ~/kev.pid)
