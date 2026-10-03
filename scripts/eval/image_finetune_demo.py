"""The image fine-tuning flow of docs/api.md, as a user runs it: a folder of labelled photos (<dir>/<label>/*.jpg) -> rows ->
upload -> a job on a `selfjev serve --fine-tuning` server -> its model. Prints the job and where its adapter is, for
`selfjev eval --adapter` on a frozen test.

  uv run python scripts/eval/image_finetune_demo.py --photos runs/hurricane_demo/photos \
      --question "What does this satellite image show?" --suffix hurricane [--base-url http://127.0.0.1:8000]
"""

import argparse
import time
from pathlib import Path

from selfjev import Choice, SelfJev


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--photos", required=True)
    ap.add_argument("--question", required=True)
    ap.add_argument("--suffix", required=True)
    ap.add_argument("--base-url", default="http://127.0.0.1:8000")
    ap.add_argument("--home", default=str(Path.home() / ".selfjev" / "server"), help="the server's --home")
    ap.add_argument("--epochs", type=int, help="the job's epochs (default: the server's)")
    a = ap.parse_args()
    client, t0 = SelfJev(base_url=a.base_url, timeout=600), time.time()
    labels = sorted(p.name for p in Path(a.photos).iterdir() if p.is_dir())
    q = {"label": Choice(a.question, dict.fromkeys(labels))}
    rows = [{"state": [p], "questions": q, "answers": {"label": p.parent.name}} for p in sorted(Path(a.photos).glob("*/*.jpg"))]
    f = client.upload_file(rows)
    hp = {"epochs": a.epochs} if a.epochs else None
    job = client.wait_fine_tuning_job(client.create_fine_tuning_job(f.id, suffix=a.suffix, hyperparameters=hp).id, poll=15)
    events = [e.message for e in client.fine_tuning_events(job.id)]
    took = f"{(time.time() - t0) / 60:.1f} min"
    print(f"{f.rows} photos, {len(labels)} labels -> {job.status} {job.fine_tuned_model} in {took}; {events[-2:]}")
    print(f"ADAPTER {Path(a.home) / 'jobs' / job.id / 'run' / 'adapter'}", flush=True)


if __name__ == "__main__":
    main()
