#!/usr/bin/env bash
# On the GPU box (~/sj = repo subset): score one quantization (8bit|4bit) of selfjev-4b-vision on Decision Bench's three
# suites with the GPU memory capped at 8 GB-card size, then bench memory by text length. Results -> ~/out/$BITS/.
# usage: quant_box.sh 4bit
set -uo pipefail
BITS=$1; cd ~/sj; export PATH=$HOME/.local/bin:$PATH
uv sync --frozen --no-dev --extra serve --extra gpu --extra quant > ~/setup_$BITS.log 2>&1 || { echo SETUP_FAIL; tail -20 ~/setup_$BITS.log; exit 1; }
mkdir -p ~/out/$BITS
# an RTX 4060 has 8188 MiB, ~7.6 GiB usable after the CUDA context: cap this process at 7.2 GiB of allocator memory
sj() { uv run --no-sync python -c "import sys, torch; torch.cuda.set_per_process_memory_fraction(7.2 * 2**30 / torch.cuda.get_device_properties(0).total_memory); from selfjev.cli import main; main(sys.argv[1:])" "$@"; }
A="--adapter weights/selfjev_4b_vision --quantize $BITS --max-batch-tokens 4096"
for f in eval_llm eval2 compact_challenge_v1; do
  echo "=== $f $(date +%T)"; sj eval $A --data data/$f.jsonl --split test --out ~/out/$BITS/$f > ~/out/$BITS/$f.log 2>&1; tail -2 ~/out/$BITS/$f.log
done
echo "=== bench $(date +%T)"
sj bench $A --lengths 2048,8192,16384 --questions 1,10 --repeats 5 --out ~/out/$BITS/bench > ~/out/$BITS/bench.log 2>&1; tail -3 ~/out/$BITS/bench.log
echo "=== done $(date +%T)"; touch ~/out/$BITS/DONE
