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
if [[ $step == all || $step == custom ]]; then  # custom shared-state model, spec version (custom.py, train_custom.py)
  $PJEV train-custom configs/custom_frozen.json        # backbone frozen (Stage A only); ~24 min on the M5 Pro
  evals custom_frozen --checkpoint runs/custom_frozen/checkpoint
fi
if [[ $step == all || $step == custom_distill ]]; then  # label-diversity attempt: teacher-labeled questions with mixed label sets
  .venv/bin/python scripts/build_distill.py            # data/distill.jsonl; teacher = stock reranker + LoRA pilot (local)
  $PJEV train-custom configs/custom_distill_frozen.json
  $PJEV train-custom configs/custom_distill_lora.json  # joint: 50 warm-up steps, then LoRA + new modules (~50 min on an A10G)
  $PJEV eval --data $DATA --split test --out reports/custom_distill_frozen/test --checkpoint runs/custom_distill_frozen/checkpoint > /dev/null
  evals custom_distill_lora --checkpoint runs/custom_distill_lora/checkpoint
fi
if [[ $step == all || $step == custom_sim ]]; then  # opt-in similarity (MaxSim) term, frozen then joint LoRA (A10G: 8 + 29 min)
  $PJEV train-custom configs/custom_sim_frozen.json
  $PJEV train-custom configs/custom_sim_lora.json
  evals custom_sim_frozen --checkpoint runs/custom_sim_frozen/checkpoint
  evals custom_sim_lora --checkpoint runs/custom_sim_lora/checkpoint
  $PJEV compare reports/{baseline,lora_pilot,custom_frozen,custom_distill_lora,custom_sim_frozen,custom_sim_lora}/test/report.json \
    --names base stock-LoRA custom custom-distill-LoRA custom-sim custom-sim-LoRA --out reports/comparison_custom.md > /dev/null
fi
if [[ $step == all || $step == custom_bench ]]; then  # speed on one CUDA GPU (ran on an AWS A10G), bf16, both with unmerged LoRA
  $PJEV bench --dtype bfloat16 --repeats 10 --out reports/bench/gpu_stock_base_bf16 > /dev/null
  $PJEV bench --dtype bfloat16 --repeats 10 --adapter runs/lora_pilot/adapter --out reports/bench/gpu_stock_lora_bf16 > /dev/null
  $PJEV bench --dtype bfloat16 --repeats 10 --checkpoint runs/custom_sim_lora/checkpoint --out reports/bench/gpu_custom_lora_bf16 > /dev/null
  .venv/bin/python -c "from personal_jev.benchmark import run; run(checkpoint='runs/custom_sim_lora/checkpoint', dtype='bfloat16', grid=[(16384, 1, 1, 'binary'), (32000, 1, 1, 'binary'), (16384, 16, 3, 'multiclass'), (32000, 16, 3, 'multiclass')], repeats=3, out_dir='reports/bench/gpu_custom_long_bf16')" > /dev/null
  .venv/bin/python -c "from personal_jev.benchmark import run; run(adapter='runs/lora_pilot/adapter', dtype='bfloat16', grid=[(16384, 1, 1, 'binary'), (32000, 1, 1, 'binary'), (16384, 16, 3, 'multiclass')], repeats=2, out_dir='reports/bench/gpu_stock_long_bf16')" > /dev/null
fi
if [[ $step == all || $step == longctx ]]; then  # one binary pair per request at 16K and 32K tokens: does it fit?
  for dt in float32 bfloat16; do
    .venv/bin/python -c "from personal_jev.benchmark import run; run(dtype='$dt', grid=[(16384, 1, 1, 'binary'), (32000, 1, 1, 'binary')], repeats=2, out_dir='reports/bench/long_context_$dt')" || echo "long context $dt failed"
  done
fi
