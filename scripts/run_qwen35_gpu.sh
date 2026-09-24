#!/usr/bin/env bash
# Qwen3.5 pipeline on one CUDA GPU (see scripts/aws_qwen35.sh): setup -> forked-cache check -> train Qwen3.5-4B with the
# round-2 recipe (scripts/run_qwen35.py) -> old test + eval2 + bench -> Eikos-4B and the Qwen3.5-2B challenger on eval2.
# Logs to ~/SelfJev/run_qwen35.log.
set -uo pipefail
cd ~/SelfJev
export PATH="$HOME/.local/bin:$PATH" PYTHONUNBUFFERED=1
log() { echo "[$(date +%H:%M:%S)] qwen35: $*"; }
command -v uv > /dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
uv sync --quiet && uv pip install --quiet --python .venv/bin/python flash-linear-attention einops && log "env ready"
PY=.venv/bin/python
$PY -c "import fla; print('fla', fla.__version__)" || log "WARNING: flash-linear-attention missing, slow torch fallback"
$PY - <<'P'
from huggingface_hub import snapshot_download
for m, r in [("Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"), ("Qwen/Qwen3.5-2B", "15852e8c16360a2fea060d615a32b45270f8a8fc"),
             ("caiovicentino1/Eikos-4B", "99336c237636288bcddc7f84a7adfc31b20acbd3")]:
    snapshot_download(m, revision=r); print("downloaded", m, flush=True)
P
R=scripts/run_qwen35.py
log "check"; $PY $R qwen35_4b --stage check || { log "CHECK FAILED"; exit 1; }
log "train qwen35_4b_r2x64"; $PY $R qwen35_4b --stage train --tag _r2x64 > runs/qwen35_4b_r2x64.log 2>&1 || { log "TRAIN FAILED"; tail -40 runs/qwen35_4b_r2x64.log; exit 1; }
tail -3 runs/qwen35_4b_r2x64.log
A=runs/qwen35_4b_r2x64/adapter
log "eval"; $PY $R qwen35_4b --stage eval --tag _r2x64 --adapter $A --sets eval2,test 2>&1 | grep -E "EVAL|Error|error" 
log "bench"; $PY $R qwen35_4b --stage bench --tag _r2x64 --adapter $A 2>&1 | grep -E "BENCH|Error"
log "eikos eval2"; $PY scripts/score_eikos.py --data data/eval2.jsonl --out reports/eikos_4b/eval2 2>&1 | grep -E "EVAL|Error|error"
log "qwen3.5-2b challenger eval2"; $PY $R qwen35 --stage eval --tag _r1 --adapter runs/challengers/qwen35/adapter --sets eval2 2>&1 | grep -E "EVAL|Error"
log "ALL DONE"
