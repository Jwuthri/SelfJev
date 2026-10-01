#!/usr/bin/env bash
# Laya 0.3.22 (PyPI; GitHub main 6d942c92081fbc139e736bbd9ac0023223c29b7f). Port 8002.
set -euo pipefail
ENV=~/env-laya
[ -d "$ENV" ] || uv venv "$ENV" --python 3.12
uv pip install --python "$ENV/bin/python" "laya[serve]==0.3.22"     # torch 2.14.0 (cu130 wheel), transformers 5.x
"$ENV/bin/python" -c "import laya,torch;print(laya.__version__,torch.__version__,torch.version.cuda,torch.cuda.is_available())"

# laya.serve hard-codes limits that our requests exceed (50,000 state chars; 512 options in total; 64 questions; 2 MiB body).
# They are module constants read at call time, so patching them before main() works.
cat > ~/laya_serve_patched.py <<'PY'
import laya.serve as s
s.MAX_STATE_CHARS = 2_000_000      # default 50_000 -> HTTP 413 for a ~16K-token state
s.MAX_TOTAL_OPTIONS = 100_000      # default 512    -> 413 for 60 choice questions x 30 options
s.MAX_QUESTIONS = 256              # default 64
s.MAX_CHOICE_OPTIONS = 255         # default 100
s.MAX_BODY_BYTES = 32 * 1024 * 1024  # default 2 MiB
s.main()
PY

export LAYA_HOST=127.0.0.1 LAYA_PORT=8002 LAYA_DEVICE=cuda LAYA_PRELOAD=1
export LAYA_MODELS=english,multilingual          # skip typed-decisions (only reachable via model/task anyway)
export LAYA_MAX_TOKEN_BUDGET=8192                # cap on per-request max_len / head_max_len (default 8192)
export LAYA_REVISION=55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851   # HF bundle repo convaiinnovations/laya, sha seen 2026-09-30
nohup "$ENV/bin/python" ~/laya_serve_patched.py > ~/laya.log 2>&1 &
echo $! > ~/laya.pid
until curl -sf localhost:8002/health >/dev/null; do kill -0 $! 2>/dev/null || { echo "server died"; exit 1; }; sleep 3; done
curl -s localhost:8002/health; echo
# expect "device":"cuda","device_is_preference":false. If it says cpu, laya silently fell back.
# kill:  kill $(cat ~/laya.pid)
