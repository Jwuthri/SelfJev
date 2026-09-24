#!/usr/bin/env bash
# Complete independent measurements even when an optional serving treatment fails.
set -uo pipefail
cd "$HOME/SelfJev"
export PYTHONPATH=src OMP_NUM_THREADS=4 HF_HUB_DISABLE_PROGRESS_BARS=1
P=.venv/bin/python
R=reports/t5_round2b_2026-09-24
step() {
  local label="$1"; shift
  "$@" > "$R/${label}_console.log" 2>&1
  local status=$?
  "$P" - "$R/pipeline_steps.jsonl" "$label" "$status" <<'LOG'
import datetime,json,sys
with open(sys.argv[1],'a') as f:
 f.write(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'step':sys.argv[2],'exit_code':int(sys.argv[3])})+'\n')
LOG
  echo "STEP_COMPLETE $label $status"
  return "$status"
}
if [ ! -f runs/t5gemma2_r2b_full/train_meta.json ]; then
  echo 'Corrected training has no verified final metadata'; exit 1
fi
step t5_r2b "$P" scripts/eval_t5_round2b.py t5_r2b
# Complete primary controls before optional serving experiments.
step tree_r2b "$P" scripts/eval_t5_round2b.py tree_r2b
step tree_r2b_merged "$P" scripts/eval_t5_round2b.py tree_r2b_merged
if step merge_tree "$P" -m personal_jev.vllm_tree merge --adapter runs/tree_4b_r2b/adapter --out runs/tree_4b_r2b/merged; then
  step tree_r2b_vllm .venv-vllm/bin/python scripts/eval_t5_round2b.py tree_r2b_vllm
  step tree_r2b_vllm_fp8 .venv-vllm/bin/python scripts/eval_t5_round2b.py tree_r2b_vllm_fp8
fi
step t5_r2b_merged "$P" scripts/eval_t5_round2b.py t5_r2b_merged
step t5_r2b_merged_b48 "$P" scripts/eval_t5_round2b.py t5_r2b_merged_b48
if step prefix_checks "$P" scripts/check_t5_prefix.py; then
  step t5_r2b_merged_prefix48 "$P" scripts/eval_t5_round2b.py t5_r2b_merged_prefix48
fi
step overfit_check "$P" scripts/check_t5_overfit.py
step profile "$P" scripts/profile_t5_round2b.py
step summary "$P" scripts/summarize_t5_round2b.py
"$P" - <<'DONE'
import datetime,json
from pathlib import Path
r=Path('reports/t5_round2b_2026-09-24')
rows=[json.loads(s) for s in (r/'pipeline_steps.jsonl').read_text().splitlines()]
(r/'pipeline_status.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'complete' if all(x['exit_code']==0 for x in rows) else 'finished_with_failures','steps':rows},indent=2))
DONE
echo COMPARISON_COMPLETE
