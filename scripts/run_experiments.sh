#!/usr/bin/env bash
# Reproduces every report in reports/: baseline and LoRA evals, held-out calibration, comparison, benchmarks.
# Test splits are only ever read by `pjev eval`; temperatures come from calibration splits, thresholds from
# validation splits (pjev calibrate refuses anything else).
set -euo pipefail
cd "$(dirname "$0")/.."
PJEV=".venv/bin/pjev"
DATA="data/hf.jsonl data/eval.jsonl"  # synthetic.jsonl is training data; its own test split is reported separately

evals() {  # name [model args...]
  local name=$1; shift
  for split in validation calibration test; do
    $PJEV eval --data $DATA --split $split --out reports/$name/$split "$@" > /dev/null
  done
  $PJEV calibrate --fit reports/$name/calibration/report.json --thresholds reports/$name/validation/report.json \
    --out calib/$name.json > /dev/null
  $PJEV eval --data $DATA --split test --out reports/$name/test_calibrated --calibration calib/$name.json "$@" > /dev/null
}

step=${1:-all}
if [[ $step == all || $step == baseline ]]; then evals baseline; fi
if [[ $step == all || $step == train ]]; then $PJEV train configs/lora_pilot.json; fi
if [[ $step == all || $step == tuned ]]; then evals lora_pilot --adapter runs/lora_pilot/adapter; fi
if [[ $step == all || $step == synthetic ]]; then  # in-distribution check on the synthetic families
  $PJEV eval --data data/synthetic.jsonl --split test --out reports/baseline/synthetic_test > /dev/null
  $PJEV eval --data data/synthetic.jsonl --split test --out reports/lora_pilot/synthetic_test --adapter runs/lora_pilot/adapter > /dev/null
fi
if [[ $step == all || $step == compare ]]; then
  $PJEV compare reports/{baseline,lora_pilot}/test/report.json reports/{baseline,lora_pilot}/test_calibrated/report.json \
    --names baseline lora baseline+cal lora+cal --out reports/comparison_test.md > /dev/null
fi
if [[ $step == all || $step == bench ]]; then
  $PJEV bench --out reports/bench/baseline_fp32
  $PJEV bench --dtype bfloat16 --out reports/bench/baseline_bf16
  $PJEV bench --adapter runs/lora_pilot/adapter --out reports/bench/lora_fp32
fi
if [[ $step == all || $step == custom ]]; then  # custom shared-state model (custom.py, train_custom.py)
  $PJEV train-custom configs/custom_frozen.json       # Stage A: frozen backbone, new modules only (also the frozen ablation)
  $PJEV train-custom configs/custom_lora.json         # Stage B: LoRA + new modules, starting from the Stage A checkpoint
  $PJEV train-custom configs/custom_lora.json --set 'backbone="frozen"' 'out_dir="runs/custom_frozen_cont"'  # same steps, no LoRA
  evals custom_frozen --checkpoint runs/custom_frozen/checkpoint
  evals custom_lora --checkpoint runs/custom_lora/checkpoint
  $PJEV eval --data $DATA --split test --out reports/custom_frozen_cont/test --checkpoint runs/custom_frozen_cont/checkpoint > /dev/null
  $PJEV eval --data $DATA --split test --out reports/custom_lora/test_bf16 --checkpoint runs/custom_lora/checkpoint --dtype bfloat16 > /dev/null
  $PJEV compare reports/{baseline,lora_pilot,custom_frozen,custom_frozen_cont,custom_lora}/test/report.json \
    --names base stock-LoRA custom-frozen custom-frozen-cont custom-LoRA --out reports/comparison_custom.md > /dev/null
fi
if [[ $step == all || $step == custom_bench ]]; then  # same grid, same session, bf16, both with unmerged LoRA
  $PJEV bench --checkpoint runs/custom_lora/checkpoint --dtype bfloat16 --out reports/bench/custom_lora_bf16
  $PJEV bench --adapter runs/lora_pilot/adapter --dtype bfloat16 --out reports/bench/lora_bf16
  .venv/bin/python -c "from personal_jev.benchmark import run; run(checkpoint='runs/custom_lora/checkpoint', dtype='bfloat16', grid=[(16384, 1, 1, 'binary'), (32000, 1, 1, 'binary'), (16384, 16, 3, 'multiclass'), (32000, 16, 3, 'multiclass')], repeats=3, out_dir='reports/bench/custom_long_context_bf16')"
fi
if [[ $step == all || $step == longctx ]]; then  # one binary pair per request at 16K and 32K tokens: does it fit?
  for dt in float32 bfloat16; do
    .venv/bin/python -c "from personal_jev.benchmark import run; run(dtype='$dt', grid=[(16384, 1, 1, 'binary'), (32000, 1, 1, 'binary')], repeats=2, out_dir='reports/bench/long_context_$dt')" || echo "long context $dt failed"
  done
fi
