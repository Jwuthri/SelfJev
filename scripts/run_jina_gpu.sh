#!/usr/bin/env bash
# jina-reranker-v3.5 backend (jina.py) on one CUDA GPU: setup -> zero-shot evals -> LoRA training (configs/jina_r2b.json,
# the tree r2b recipe: round-2 hard cases with "none" rebalanced) -> evals on the old test split and on eval2.
# Runs on the box (see scripts/aws_jina.sh); logs to ~/SelfJev/run_jina.log.
set -uo pipefail
cd ~/SelfJev
export PATH="$HOME/.local/bin:$PATH"
log() { echo "[$(date +%H:%M:%S)] jina: $*"; }
command -v uv > /dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
uv sync --quiet && log "env ready"
.venv/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('jinaai/jina-reranker-v3.5', revision='e8a93f33f0b22108f8c2364f8484ce3422552fbc'); print('model ok')"
PJEV=.venv/bin/pjev; DATA="data/hf.jsonl data/eval.jsonl"
J=(--jina --dtype bfloat16 --max-length 16384 --max-batch-tokens 32768)
acc() { grep -m1 'question accuracy' "$1/report.md"; }
log "zero-shot validation"; $PJEV eval "${J[@]}" --data $DATA --split validation --out reports/jina_zeroshot/validation > /dev/null && log "zero-shot validation: $(acc reports/jina_zeroshot/validation)"
log "zero-shot eval2"; $PJEV eval "${J[@]}" --data data/eval2.jsonl --out reports/jina_zeroshot/eval2 > /dev/null && log "zero-shot eval2: $(acc reports/jina_zeroshot/eval2)"
log "train jina_r2b"; $PJEV train-jina configs/jina_r2b.json > runs/jina_r2b.log 2>&1 || { log "TRAIN FAILED"; tail -40 runs/jina_r2b.log; exit 1; }
tail -2 runs/jina_r2b.log
A=(--adapter runs/jina_r2b/adapter)
for split in validation calibration test; do
  $PJEV eval "${J[@]}" "${A[@]}" --data $DATA --split $split --out reports/jina_r2b/$split > /dev/null || log "eval $split failed"
done
$PJEV calibrate --fit reports/jina_r2b/calibration/report.json --thresholds reports/jina_r2b/validation/report.json --out calib/jina_r2b.json > /dev/null || log "calibrate failed"
$PJEV eval "${J[@]}" "${A[@]}" --data $DATA --split test --out reports/jina_r2b/test_calibrated --calibration calib/jina_r2b.json > /dev/null || log "calibrated eval failed"
$PJEV eval "${J[@]}" "${A[@]}" --data data/eval2.jsonl --out reports/jina_r2b/eval2 > /dev/null || log "eval2 failed"
log "jina_r2b test: $(acc reports/jina_r2b/test) | eval2: $(acc reports/jina_r2b/eval2)"
log "ALL DONE"
