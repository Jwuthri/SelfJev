#!/usr/bin/env bash
# Plumb-4B, plain probabilities (T=2.07, one read, no JevBench transform). Not run by the author of this file.
set -euo pipefail
sudo apt-get install -y --no-install-recommends git build-essential
cd "$HOME"
[ -d ~/env-plumb ] || uv venv ~/env-plumb --python 3.12
source ~/env-plumb/bin/activate
# pins = plumb/serve/requirements.txt (torch 2.14 "tested: pytorch 2.14, CUDA 13"; PyPI wheel brings CUDA 13.0.3 libs)
uv pip install torch==2.14.0 transformers==5.17.0 accelerate==1.15.0 huggingface_hub==1.32.0 \
    flash-linear-attention==0.5.2 einops==0.8.2 jinja2 numpy
uv pip install --no-deps "git+https://github.com/allebee/jevk5@v0.2.0"        # provides jevk5-serve (card's "as a service")
hf download crh225/plumb-4b --revision 55de037801a8a9b9de3db5c0e16cef86210c2186 --local-dir ~/plumb-4b     # 8.4 GB, weights identical to main
# Option A (card: "Use it"): jevk5-serve, CUDA graphs <=4096 tokens, T=2.07 read from ~/plumb-4b/jevk5_config.json
nohup jevk5-serve --model ~/plumb-4b --host 127.0.0.1 --port 8090 > ~/plumb.log 2>&1 &
echo $! > ~/plumb.pid
# Option B (same math, eager, clean 400/413 errors): 
#   [ -d ~/plumb ] || git clone https://github.com/crh225/plumb ~/plumb; git -C ~/plumb checkout -q 0e6d558d3ea3002c300ce121db4d3e8df6ad792a
#   nohup python ~/plumb/serve/plumb_server.py --model ~/plumb-4b --host 127.0.0.1 --port 8090 --one-read --temperature 2.07 > ~/plumb.log 2>&1 &
#   (no --noul-commit, no --score-temperature; omit --one-read and you get the experimental v5.1 4-order readout)
until curl -sf localhost:8090/health; do kill -0 $! 2>/dev/null || { echo "server died"; exit 1; }; sleep 2; done     # plumb_server.py has no /health: watch for "ready:" in the log
tail -3 ~/plumb.log
# if CUDA-graph capture fails at startup: JEVK5_GRAPHS=0 jevk5-serve ...   (runtime.py line 99)
