#!/usr/bin/env bash
# Mica v0.1 4B: llama.cpp b11010 (CUDA, sm_89) via ctypes + Python http.server. NOT run by the author of this file (no GPU box); see notes.
set -euo pipefail
sudo apt-get update -y
sudo apt-get install -y --no-install-recommends git cmake build-essential ca-certificates curl
CU=$(ls -d /usr/local/cuda /usr/local/cuda-1* 2>/dev/null | head -1); echo "cuda toolkit: $CU"; export PATH=$CU/bin:$PATH
nvcc --version | tail -2; export CUDACXX=$(command -v nvcc)
cd "$HOME"
[ -d mica ] || git clone https://github.com/akivet/Mica-v0.1-4B.git mica
git -C mica checkout -q 24e8cea06113e6d553e538c0c0c76dfdb8b78e5e
[ -d ~/env-mica ] || uv venv ~/env-mica --python 3.12
source ~/env-mica/bin/activate
uv pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu     # tokenizer only; CPU wheel is what the Dockerfile uses
uv pip install transformers==5.5.0 safetensors "huggingface_hub>=1.0"
cd ~/mica
if [ ! -f runtime/libllama.so ]; then            # same cmake line as scripts/build_runtime.sh, arch 89, idempotent
  [ -d llama.cpp-b11010 ] || git clone -q --depth 1 --branch b11010 https://github.com/ggml-org/llama.cpp llama.cpp-b11010
  cmake -S llama.cpp-b11010 -B llama.cpp-b11010/build -DGGML_CUDA=ON -DBUILD_SHARED_LIBS=ON \
        -DCMAKE_CUDA_ARCHITECTURES=89 -DLLAMA_CURL=OFF -DLLAMA_BUILD_TESTS=OFF
  cmake --build llama.cpp-b11010/build --target llama -j "$(nproc)"
  mkdir -p runtime && find llama.cpp-b11010/build -name 'lib*.so*' -exec cp -P {} runtime/ \;
fi
ls runtime
hf download sky7350/Mica-v0.1-4B mica-v0.1-4b-BF16.gguf tokenizer.json tokenizer_config.json chat_template.jinja config.json \
   --revision ca36594cc2067c7252704f9f304cc10ef11c7c5c --local-dir weights       # 9.70 GB GGUF + 20 MB tokenizer
export LD_LIBRARY_PATH=$PWD/runtime:$CU/lib64:${LD_LIBRARY_PATH:-}
nohup python -m mica.typesafe_server --gguf weights/mica-v0.1-4b-BF16.gguf --hf weights --runtime runtime \
  --calibration calibration.json --flash-attn -1 --host 127.0.0.1 --port 8010 --name mica-v0.1-4b > ~/mica.log 2>&1 &
echo $! > ~/mica.pid
until curl -sf localhost:8010/health; do kill -0 $! 2>/dev/null || { echo "server died"; exit 1; }; sleep 2; done
tail -3 ~/mica.log
# stop: kill $(cat ~/mica.pid)
