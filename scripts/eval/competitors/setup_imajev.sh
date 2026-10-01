#!/usr/bin/env bash
# mohit67890/imajev-4b (Apache-2.0), the Image JevBench #1 configuration: repo 8501f5c3, torch backend, --fast --merge-lora,
# 1 rotation + calibration.json. Port 8765. At most 8 questions per request (--max-questions 8); bare data-URL state works.
set -euo pipefail
sudo apt-get install -y build-essential > /dev/null
V=$HOME/venvs/imajev
[ -x $V/bin/python ] || uv venv --python 3.12 $V
cd ~ && { [ -d imajev ] || git clone -q https://github.com/mohit67890/imajev; } && cd ~/imajev
git fetch -q origin && git checkout -q 8501f5c3b1ed8ef608744eabed40f22b70de4277
uv pip install --python $V/bin/python -e ".[serve,torch]" "torch==2.8.0" "torchvision==0.23.0" \
  "transformers==5.17.0" "peft==0.21.0" "flash-linear-attention==0.5.2"
$V/bin/python scripts/download_model.py --model 4b
$V/bin/hf download mohit67890/imajev-4b --local-dir adapters/imajev-4b --exclude "mlx/*" --exclude "assets/*"
PYTHONPATH=src:scripts nohup $V/bin/python scripts/playground/server.py --backend torch \
  --model-bundle artifacts/model-qwen4b.json --adapter adapters/imajev-4b \
  --rotations 1 --calibration adapters/imajev-4b/calibration.json --fast --merge-lora \
  --max-input-tokens 20000 --model-name imajev-4b --port 8765 > ~/logs/imajev.log 2>&1 &
until curl -sf localhost:8765/v1/models >/dev/null; do kill -0 $! 2>/dev/null || { echo "server died"; exit 1; }; sleep 5; done
