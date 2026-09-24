#!/bin/zsh
# All four generators in parallel; logs in reports/hardcases/run_<prefix>.log
cd /Users/julien/Documents/Repos/SelfJev
run() { uv run python scripts/gen_hardcases.py "$@" > reports/hardcases/run_$1.log 2>&1; }
uv run python scripts/gen_hardcases.py --model google/gemini-3.8-flash --budget 12 --workers 8 --seed 11 > reports/hardcases/run_gf.log 2>&1 &
uv run python scripts/gen_hardcases.py --model x-ai/grok-4.7 --budget 8 --workers 8 --seed 12 > reports/hardcases/run_gk.log 2>&1 &
uv run python scripts/gen_hardcases.py --model deepseek/deepseek-v4-flash --budget 2.5 --max-questions 4000 --workers 8 --seed 13 > reports/hardcases/run_df.log 2>&1 &
uv run python scripts/gen_hardcases.py --model openai/gpt-6-luna --budget 2.5 --max-questions 4000 --workers 8 --seed 14 > reports/hardcases/run_lu.log 2>&1 &
wait
echo ALL_GEN_DONE
