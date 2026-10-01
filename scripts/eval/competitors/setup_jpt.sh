#!/usr/bin/env bash
# kirp/jpt-4b (CC-BY-NC-4.0; evaluation only): vLLM 0.30.0 on :8000 + llm2jev 0.6.1 (/v1/systemone) on :8080.
# Images go as chat messages (--image-style messages); a bare data-URL state is read as text by llm2jev.
set -euo pipefail
V=$HOME/venvs/jpt4b
[ -x $V/bin/python ] || uv venv --python 3.12 $V
uv pip install --python $V/bin/python "vllm==0.30.0" "llm2jev==0.6.1" ninja
export PATH=$V/bin:$PATH   # vLLM JIT-builds kernels at start-up and needs `ninja` on PATH
nohup $V/bin/vllm serve kirp/jpt-4b --host 127.0.0.1 --port 8000 --max-model-len 32768 --gpu-memory-utilization 0.90 \
  --enable-prefix-caching --max-logprobs 256 --return-tokens-as-token-ids --enable-scale-out > ~/logs/vllm-jpt.log 2>&1 &
until curl -sf localhost:8000/health >/dev/null; do kill -0 $! 2>/dev/null || { echo "server died"; exit 1; }; sleep 5; done
nohup $V/bin/llm2jev --model kirp/jpt-4b --backend vllm --url http://127.0.0.1:8000 \
  --host 127.0.0.1 --port 8080 --temperature 1.036 > ~/logs/llm2jev.log 2>&1 &
until curl -sf localhost:8080/health; do kill -0 $! 2>/dev/null || { echo "server died"; exit 1; }; sleep 2; done
