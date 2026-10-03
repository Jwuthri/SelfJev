# Image fine-tuning on 300 photos of a new task (hurricane damage), through the API

`scripts/data/hurricane_photos.py` (150 photos per class from rows the frozen test does not use) ->
`scripts/eval/image_finetune_demo.py` (rows from a folder, `upload_file`, a job, `wait_fine_tuning_job`) on
`selfjev serve --fine-tuning` 0.4.1, L40S; each model then scored by `selfjev eval` on the frozen image test
(`data/ova/eval_images_v1.jsonl`) and eval2. Paired against the release on the same engine. JOURNAL 2026-10-02.

| test | release | 1 epoch (2 steps) | 5 epochs (10 steps) |
|---|---|---|---|
| hurricane (100 q) | 61.0 | 79.0 (26 fixed / 8 broken, p = 0.0029) | 86.0 (30 fixed / 5 broken, p = 2.2e-05) |
| beans (204 q) | 97.5 | 99.0 (3 fixed / 0 broken, p = 0.25) | 99.0 (3 fixed / 0 broken, p = 0.25) |
| eurosat (200 q) | 93.5 | 92.5 (1 fixed / 3 broken, p = 0.62) | 91.5 (1 fixed / 5 broken, p = 0.22) |
| fashion (200 q) | 89.0 | 88.0 (0 fixed / 2 broken, p = 0.5) | 87.0 (0 fixed / 4 broken, p = 0.12) |
| indoor (268 q) | 95.5 | 94.8 (0 fixed / 2 broken, p = 0.5) | 95.1 (0 fixed / 1 broken, p = 1) |
| painting (204 q) | 70.6 | 70.6 (2 fixed / 2 broken, p = 1) | 70.6 (2 fixed / 2 broken, p = 1) |
| pets (222 q) | 97.3 | 97.3 (0 fixed / 0 broken, p = 1) | 97.3 (0 fixed / 0 broken, p = 1) |
| rice (200 q) | 92.5 | 93.0 (1 fixed / 0 broken, p = 1) | 92.5 (1 fixed / 1 broken, p = 1) |
| snacks (200 q) | 95.5 | 94.0 (0 fixed / 3 broken, p = 0.25) | 93.5 (0 fixed / 4 broken, p = 0.12) |
| trash (204 q) | 95.6 | 96.1 (1 fixed / 0 broken, p = 1) | 96.1 (1 fixed / 0 broken, p = 1) |
| **all images** (2,002 q) | 90.5 | 91.2 (34 fixed / 20 broken, p = 0.076) | 91.3 (38 fixed / 22 broken, p = 0.052) |
| **eval2 (text)** | 96.1 | 96.1 (5 fixed / 4 broken, p = 1) | 96.1 (5 fixed / 5 broken, p = 1) |
