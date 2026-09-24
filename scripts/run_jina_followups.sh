#!/usr/bin/env bash
# Follow-ups on the same box after run_jina_gpu.sh: 2 epochs (jina_r2b_e2) and rank-64 + MLP LoRA (jina_r2b_r64),
# each evaluated on the old test split and eval2. Logs: ~/SelfJev/run_jina_followups.log
set -uo pipefail
cd ~/SelfJev
export PATH="$HOME/.local/bin:$PATH"
log() { echo "[$(date +%H:%M:%S)] jina-followup: $*"; }
PJEV=.venv/bin/pjev; DATA="data/hf.jsonl data/eval.jsonl"
J=(--jina --dtype bfloat16 --max-length 16384 --max-batch-tokens 32768)
acc() { grep -m1 'question accuracy' "$1/report.md"; }
for TAG in ${TAGS:-jina_r2b_e2 jina_r2b_r64}; do
  log "train $TAG"; $PJEV train-jina configs/$TAG.json > runs/$TAG.log 2>&1 || { log "TRAIN $TAG FAILED"; tail -30 runs/$TAG.log; continue; }
  tail -1 runs/$TAG.log
  A=(--adapter runs/$TAG/adapter)
  $PJEV eval "${J[@]}" "${A[@]}" --data $DATA --split test --out reports/$TAG/test > /dev/null || log "eval test failed"
  $PJEV eval "${J[@]}" "${A[@]}" --data data/eval2.jsonl --out reports/$TAG/eval2 > /dev/null || log "eval2 failed"
  log "$TAG test: $(acc reports/$TAG/test) | eval2: $(acc reports/$TAG/eval2)"
done
log "ALL DONE"
