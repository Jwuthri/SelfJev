#!/usr/bin/env bash
set -euo pipefail
cd "$HOME/SelfJev"
export PYTHONPATH=src OMP_NUM_THREADS=4 HF_HUB_DISABLE_PROGRESS_BARS=1
.venv/bin/python - <<'CHECK'
import json
from pathlib import Path
m=json.loads(Path('runs/t5gemma2_r2b_full_smoke/train_meta.json').read_text())
assert m['trainable_parameters']==5963776
for side in ['encoder','decoder']:
 assert m['lora_target_coverage'][side]['modules']==104
 assert m['first_step_gradient_audit'][side]['gradient_norm']>0
assert m['reload_check']['max_abs_score_diff']<=1e-4
print('Full encoder and decoder GPU smoke verified',flush=True)
CHECK
.venv/bin/python scripts/train_t5_round2b.py
bash scripts/evaluate_t5_round2b.sh
