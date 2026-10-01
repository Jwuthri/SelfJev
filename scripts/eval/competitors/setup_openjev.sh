#!/usr/bin/env bash
# OpenJev (27B) on one L40S 48GB: FP8 checkpoint (30.4 GB) or BF16 repo + online FP8 (54.7 GB download). Not run by the author of this file.
set -euo pipefail
sudo apt-get install -y --no-install-recommends git build-essential
cd "$HOME"
[ -d ~/env-openjev ] || uv venv ~/env-openjev --python 3.12
source ~/env-openjev/bin/activate
uv pip install "vllm==0.29.0" "openai==3.16.2" "httpx==0.28.1" "transformers==5.17.0" ninja   # ninja: vLLM JIT builds at start-up     # vllm pins torch==2.13.0 (cu13.0.3 libs), wheel links libcudart.so.13
python - <<'PY'
import torch, vllm; print(torch.__version__, torch.version.cuda, vllm.__version__, torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))
PY
MODEL=${MODEL:-fp8}                                   # fp8 | bf16
if [ "$MODEL" = fp8 ]; then
  hf download openjev/openjev-FP8 --local-dir ~/openjev                       # 30.4 GB; serves as a dir named "openjev"
else
  hf download openjev/openjev --local-dir ~/openjev --exclude 'assets/*'     # 54.7 GB
fi
hf download openjev/openjev helper/shim.py serve/SERVE.md --local-dir ~/openjev-card        # helper lives only in the BF16 repo
echo "81a22f1b1b8912a465059207ef9f60b7c6c16b4de6372305d867efbe38a1987a  $HOME/openjev-card/helper/shim.py" | sha256sum -c -
nohup vllm serve ~/openjev --host 127.0.0.1 --served-model-name qwen --port 8000 --enable-prefix-caching \
  --max-model-len 16384 --gpu-memory-utilization 0.90 --limit-mm-per-prompt '{"image":1}' --trust-remote-code \
  --max-num-seqs 16 --max-logprobs 64 --gdn-prefill-backend triton --quantization fp8 > ~/vllm.log 2>&1 &
echo $! > ~/vllm.pid
until curl -sf localhost:8000/health >/dev/null; do kill -0 $! 2>/dev/null || { echo "server died"; exit 1; }; sleep 5; done; tail -5 ~/vllm.log
VLLM=http://localhost:8000/v1 TOKENIZER=$HOME/openjev READOUT_T=0.85 READOUT_NOUL_T=1.829074 READOUT_NOUL_BIAS=0 \
READOUT_TARGETED=1 READOUT_INSTR_STYLE=pyrepr SHIM_STAGGER=1 \
nohup python ~/openjev-card/helper/shim.py --host 127.0.0.1 --port 3000 > ~/shim.log 2>&1 &
echo $! > ~/shim.pid
until curl -sf localhost:3000/v1/version; do kill -0 $! 2>/dev/null || { echo "shim died"; exit 1; }; sleep 2; done
