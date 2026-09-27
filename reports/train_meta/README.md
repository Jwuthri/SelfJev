# Training logs of past runs

`train_meta.json` of every run whose `runs/<name>/` folder was deleted on 2026-09-27 (the adapters are gone; the
kept ones are in `weights/`). One file per run, `runs/a/b` saved as `a__b.json`: config, data counts, validation after
every checkpoint, the best step. The code that produced most of them is at tag `archive/pre-cleanup-2026-09-27`.
