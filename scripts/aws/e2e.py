"""End-to-end test of the product on a real GPU, recorded. Deploys this commit with `selfjev deploy aws up --fine-tuning`,
then through the SDK checks: health, auth and errors, the models list, every question type on cases the model must get
right, Jev's names and paths, 16 concurrent requests, images (a Path, text + image parts, a bad image, concurrency, the
async client), a supervised and an RLCD fine-tuning job over HTTP, a fine-tune on a folder of photos plus text rows, and
the models they produce. The box is always torn down.

  uv run --extra deploy python scripts/aws/e2e.py --out reports/e2e/2026-09-28          # PAID: a g6e.xlarge for ~1 h
  uv run python scripts/aws/e2e.py --base-url http://host:8000 --api-key KEY --out DIR   # an existing server instead

Writes <out>/report.md (every check, its time and detail) and <out>/transcript.jsonl (every HTTP request and response,
truncated to 2 KB), plus <out>/setup.log (the box's first-boot log) when it deployed. Exit code 1 if any check failed.
Fine-tuning data: batch numdate_neg_v1 from data/all.jsonl.gz (training rows only, never a test set); photos: images v1's
training and validation files (data/images_v1/, scripts/data/build_images_v1.py; never data/ova/eval_images_v1.jsonl).
"""

import argparse
import asyncio
import base64
import gzip
import json
import subprocess
import tempfile
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

from selfjev import AsyncSelfJev, AuthenticationError, Choice, InvalidRequestError, Multi, NotFoundError, Noul, Score, SelfJev

STATE = (
    "Ticket 4411 from Dana (Pro plan, paying since 2023): I was charged twice for invoice INV-2291 this morning. "
    "Please refund the second charge today, I need the money for payroll."
)
QUESTIONS = {  # each has one clearly right answer
    "refund": Noul("Does the customer ask for a refund?"),
    "spam": Noul("Is this message spam or advertising?"),
    "paid": Noul("Is the customer on a paid plan?", {"true": "a paying customer", "false": "a free user"}),
    "team": Choice("Which team should handle this?", {"billing": "payments, invoices and refunds", "tech": "outages, bugs and integrations",
                                                      "sales": "new purchases and upgrades"}),
    "urgency": Score("How urgent is it?", ["not urgent", "this week", "today"]),
    "topics": Multi("Which topics does it mention?", {"invoice": "an invoice or a charge", "shipping": "a delivery or shipment",
                                                      "account": "logging in or account access"}),
}  # fmt: skip


class Recorder:
    """httpx event hooks: every request the SDK sends is written to transcript.jsonl with its response and time."""

    def __init__(self, out: Path):
        self.transcript, self.checks = (out / "transcript.jsonl").open("w"), []

    def client(self, **kw) -> httpx.Client:
        def start(req):
            req.extensions["t0"] = time.perf_counter()

        def done(resp):
            resp.read()
            req = resp.request
            try:
                body = req.content.decode(errors="replace")[:2000]
            except httpx.RequestNotRead:  # a multipart upload is streamed: record its size, not its bytes
                body = f"<upload: {req.headers.get('content-length', '?')} bytes>"
            self.transcript.write(json.dumps({
                "t": round(time.time(), 3), "method": req.method, "path": req.url.path, "status": resp.status_code,
                "ms": round(1e3 * (time.perf_counter() - req.extensions["t0"]), 1), "request_id": resp.headers.get("x-request-id"),
                "request": body, "response": resp.text[:2000],
            }) + "\n")  # fmt: skip
            self.transcript.flush()

        return httpx.Client(timeout=120, event_hooks={"request": [start], "response": [done]}, **kw)

    def check(self, name, fn):
        t0 = time.perf_counter()
        try:
            detail, ok = fn() or "", True
        except Exception as e:  # a failed check is recorded, the next one still runs
            detail, ok = f"{type(e).__name__}: {e}", False
        self.checks.append((name, ok, time.perf_counter() - t0, " ".join(str(detail).split())[:400]))
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {self.checks[-1][3][:160]}", flush=True)


def jev_question(q: dict) -> tuple[dict, dict]:
    """An internal question -> Jev's, and the map from its candidate ids to the keys used (the descriptions themselves:
    a choice shows the model "key: description", so opaque ids would add noise)."""
    if q["type"] == "binary":
        return {"type": "noul", "instructions": q["instruction"]}, {}
    keys = {c["id"]: c["description"] for c in q["candidates"]}
    kind = "choice" if q["type"] == "multiclass" else "multi"
    return {"type": kind, "instructions": q["instruction"], "criteria": dict.fromkeys(keys.values())}, keys


def photo_rows(path: str, n: int, family: str | None = None, per_family: int | None = None) -> list[dict]:
    """Up to n photos of an images v1 file (all families, or one) as fine-tuning rows: the photo, its questions, their answers."""
    rows, count = {}, {}
    with open(path) as f:
        for r in map(json.loads, f):
            fam, sid = r["family"], r["source_id"]
            if (family and fam != family) or (sid not in rows and (len(rows) >= n or count.get(fam, 0) >= (per_family or n))):
                continue
            if sid not in rows:
                count[fam] = count.get(fam, 0) + 1
            row = rows.setdefault(sid, {"state": r["state"], "questions": {}, "answers": {}})
            q, keys = jev_question(r["question"])
            qid = f"q{len(row['questions'])}"
            row["questions"][qid] = q
            row["answers"][qid] = keys.get(r["target"], r["target"]) if keys else r["target"]
    return list(rows.values())


def right(res, row) -> list[bool]:
    """Per question: is the answer the expected one?"""
    out = []
    for qid, want in row["answers"].items():
        a = res.answers[qid]
        out.append(a.noul >= 0.5 if a.type == "noul" and want else a.noul < 0.5 if a.type == "noul" else a.choice == want)
    return out


def training_files(out: Path) -> tuple[Path, Path]:
    """numdate_neg_v1's train / validation rows as fine-tuning files: one decisions request + its answers per text."""
    rows = {"train": {}, "validation": {}}
    with gzip.open("data/all.jsonl.gz", "rt") as f:
        for r in map(json.loads, f):
            if r["dataset"] != "numdate_neg_v1" or r["split"] not in rows:
                continue
            row = rows[r["split"]].setdefault(r["source_id"], {"state": r["state"], "questions": {}, "answers": {}})
            qid = f"q{len(row['questions'])}"
            q, keys = jev_question(r["question"])
            row["questions"][qid] = q
            t = r["target"]
            row["answers"][qid] = [keys[x] for x in t] if isinstance(t, list) else keys.get(t, t) if keys else t
    paths = []
    for split, name in (("train", "e2e_train.jsonl"), ("validation", "e2e_val.jsonl")):
        (out / name).write_text("".join(json.dumps(r) + "\n" for r in rows[split].values()))
        paths.append(out / name)
    return paths[0], paths[1]


def run_checks(base_url: str, api_key: str, out: Path, rec: Recorder, fine_tuning=True):
    http = rec.client()
    client = SelfJev(api_key=api_key, base_url=base_url, http_client=http, max_retries=0)

    def ok_answers(res):
        a = res.answers
        assert a["refund"].noul > 0.5 and a["spam"].noul < 0.5 and a["paid"].noul > 0.5, "nouls"
        assert a["team"].choice == "billing" and abs(sum(a["team"].probabilities.values()) - 1) < 1e-4, "choice"
        assert a["urgency"].score > 1.0 and a["urgency"].legend == {"0": "not urgent", "1": "this week", "2": "today"}, "score"
        assert "invoice" in a["topics"].multi and "shipping" not in a["topics"].multi, "multi"
        return {k: round(getattr(v, v.type), 3) if v.type in ("noul", "score") else getattr(v, v.type) for k, v in a.items()}

    rec.check("health (open)", lambda: http.get(f"{base_url}/health").raise_for_status().json())

    def wrong_key():
        try:
            SelfJev(api_key="wrong", base_url=base_url, http_client=http, max_retries=0).system_one(STATE, QUESTIONS)
        except AuthenticationError as e:
            return f"401 {e.type}"
        raise AssertionError("a wrong key was accepted")

    rec.check("auth: a wrong key is refused", wrong_key)
    rec.check("models", lambda: [m["id"] for m in client.models()])
    answers = {}

    def decisions():
        res = client.system_one(STATE, QUESTIONS)
        assert res.model == "selfjev-4b" and res.usage.input_tokens > 0
        answers.update(ok_answers(res))
        return answers

    rec.check("decisions: every question type answered right", decisions)

    def jev_compat():
        jev = SelfJev(api_key=api_key, base_url=base_url, http_client=http, max_retries=0, path="/api/alpha/decisions")
        res = jev.system_one(STATE, QUESTIONS, model="jev-latest")
        return ok_answers(res)

    rec.check("Jev compatibility: /api/alpha/decisions with model jev-latest", jev_compat)
    rec.check("object state (JSON)", lambda: ok_answers(client.system_one({"ticket": 4411, "text": STATE}, QUESTIONS)))

    def errors():
        bad = {"state": "x", "questions": {"q": {"type": "choice", "instructions": "?", "criteria": {"only": None}}}}
        r = http.post(f"{base_url}/v1/systemone", headers={"Authorization": f"Bearer {api_key}"}, json=bad)
        assert r.status_code == 422 and r.json()["error"]["param"] == "questions.q.criteria", r.text
        try:
            client.system_one(STATE, QUESTIONS, model="gpt-99")
        except NotFoundError as e:
            return f"422 {r.json()['error']['param']}; 404 {e.param}"
        raise AssertionError("an unknown model was accepted")

    rec.check("errors: 422 with the field, 404 for an unknown model", errors)

    def concurrent():
        def one(i):
            t0 = time.perf_counter()
            client.system_one(f"{STATE} (copy {i})", QUESTIONS)
            return 1e3 * (time.perf_counter() - t0)

        t0 = time.perf_counter()
        with ThreadPoolExecutor(16) as pool:
            ms = sorted(pool.map(one, range(16)))
        return f"16 requests in {time.perf_counter() - t0:.1f} s; per request p50 {ms[8]:.0f} ms, max {ms[-1]:.0f} ms"

    rec.check("16 concurrent requests", concurrent)
    images(client, base_url, api_key, rec)
    if fine_tuning:
        fine_tune(client, out, rec, ok_answers)
        image_fine_tune(client, out, rec)
    rec.check("metrics", lambda: [x for x in http.get(f"{base_url}/metrics").text.splitlines() if x.startswith("selfjev_req")][:6])


def images(client, base_url, api_key, rec):
    photos = photo_rows("data/images_v1/val.jsonl", 24, per_family=4)  # 4 held-out photos of each of the 6 kinds

    def from_files():
        hits, ms = [], []
        with tempfile.TemporaryDirectory() as d:
            for i, row in enumerate(photos):
                path = Path(d) / f"photo{i}"  # a file as a user has it: the SDK reads it and sends a data URL
                path.write_bytes(base64.b64decode(row["state"].split(",", 1)[1]))
                t0 = time.perf_counter()
                hits += right(client.system_one([path], row["questions"]), row)
                ms.append(1e3 * (time.perf_counter() - t0))
        assert sum(hits) >= 0.8 * len(hits), f"{sum(hits)} of {len(hits)} right"
        return f"{sum(hits)} of {len(hits)} questions right on {len(photos)} photos; per request p50 {sorted(ms)[len(ms) // 2]:.0f} ms"

    rec.check("images: photos sent as files, answered right", from_files)

    def with_text():
        row = photos[0]
        alone, mixed = (client.system_one(s, row["questions"]) for s in ([row["state"]], ["A customer sent this photo.", row["state"]]))
        assert right(mixed, row) == right(alone, row), "the text part changed the answer"
        return {k: round(v.noul, 3) if v.type == "noul" else v.choice for k, v in mixed.answers.items()}

    rec.check("images: text and image parts in one state", with_text)

    def bad_image():
        try:
            client.system_one(["data:image/png;base64,iVBORw0KGgo="], {"cat": Noul("Is there a cat?")})
        except InvalidRequestError as e:
            return f"{e.status} {e.type}: {e.message[:120]}"
        raise AssertionError("an unreadable image was accepted")

    rec.check("images: an unreadable image is a 422", bad_image)

    def concurrent():
        t0 = time.perf_counter()
        with ThreadPoolExecutor(8) as pool:
            hits = sum(pool.map(lambda r: sum(right(client.system_one(r["state"], r["questions"]), r)), photos[:8]), 0)
        return f"8 photos at once in {time.perf_counter() - t0:.1f} s; {hits} of 16 right"

    rec.check("images: 8 concurrent requests", concurrent)

    async def asynchronous():
        async with AsyncSelfJev(api_key=api_key, base_url=base_url, timeout=120, max_retries=0) as c:
            res = await asyncio.gather(*(c.system_one(r["state"], r["questions"]) for r in photos[:4]))
        return f"{sum(sum(right(x, r)) for x, r in zip(res, photos))} of 8 right"

    rec.check("images: the async client", lambda: asyncio.run(asynchronous()))


def image_fine_tune(client, out, rec):
    """A user's flow: a folder of labelled photos (plus some text rows in the same file) -> upload -> job -> its model."""
    val = photo_rows("data/images_v1/val.jsonl", 16, family="img_beans")

    def accuracy(model):
        hits = [h for r in val for h in right(client.system_one(r["state"], r["questions"], model=model), r)]
        return f"{sum(hits)}/{len(hits)}"

    def job():
        t0 = time.time()
        with tempfile.TemporaryDirectory() as d:
            rows = []
            for i, r in enumerate(photo_rows("data/images_v1/train.jsonl", 150, family="img_beans")):
                path = Path(d) / f"leaf{i}.jpg"
                path.write_bytes(base64.b64decode(r["state"].split(",", 1)[1]))
                rows.append(r | {"state": [path]})
            text = [json.loads(x) for x in (out / "e2e_train.jsonl").read_text().splitlines()[:50]]
            f = client.upload_file(rows + text)
        before = accuracy("selfjev-4b")
        j = client.create_fine_tuning_job(f.id, suffix="e2e-images")
        j = client.wait_fine_tuning_job(j.id, poll=20, timeout=45 * 60)
        events = [e.message for e in client.fine_tuning_events(j.id)]
        assert j.status == "succeeded", f"{j.status}: {j.error or events}"
        after = accuracy(j.fine_tuned_model)
        upload = f"{f.rows} rows ({len(rows)} photos + {len(text)} texts, {f.questions} questions, {f.bytes / 2**20:.1f} MB)"
        took = f"{j.fine_tuned_model} in {(time.time() - t0) / 60:.1f} min"
        return f"{upload} -> {took}; beans held-out photos right: {before} before, {after} after"

    rec.check("fine-tuning: a folder of photos + text rows -> a model that reads images", job)


def fine_tune(client, out, rec, ok_answers):
    train, val = training_files(out)
    files = {}

    def upload():
        files["train"], files["val"] = client.upload_file(train), client.upload_file(val)
        return {k: f"{f.id}: {f.rows} rows, {f.questions} questions" for k, f in files.items()}

    rec.check("fine-tuning: upload the training and validation files", upload)

    def bad_file():
        bad = out / "e2e_bad.jsonl"
        good = train.read_text().splitlines()[0]
        bad.write_text(good + "\n" + json.dumps(json.loads(good) | {"answers": {}}) + "\n")
        try:
            client.upload_file(bad)
        except InvalidRequestError as e:
            return f"422 {e.param}: {e.message}"
        raise AssertionError("a bad line was accepted")

    rec.check("fine-tuning: a bad line is named", bad_file)
    for method, hp in (("supervised", {}), ("rlcd", {"reward": {"log": 1, "brier": 1, "spherical": 1, "confident_miss": 2}})):

        def job(method=method, hp=hp):
            t0 = time.time()
            j = client.create_fine_tuning_job(
                files["train"].id, method=method, hyperparameters=hp, validation_file=files["val"].id, suffix=f"e2e-{method}"
            )
            while (j := client.fine_tuning_job(j.id)).status in ("queued", "running"):
                assert time.time() - t0 < 45 * 60, f"still {j.status} after 45 min"
                time.sleep(20)
            events = [e.message for e in client.fine_tuning_events(j.id)]
            assert j.status == "succeeded", f"{j.status}: {j.error or events}"
            assert j.fine_tuned_model in [m["id"] for m in client.models()], "not served"
            res = client.system_one(STATE, QUESTIONS, model=j.fine_tuned_model)
            assert res.model == j.fine_tuned_model
            return f"{j.fine_tuned_model} in {(time.time() - t0) / 60:.1f} min; events {events[-3:]}; answers {ok_answers(res)}"

        rec.check(f"fine-tuning: a {method} job succeeds and its model answers", job)


def write_report(out: Path, rec: Recorder, env: dict):
    passed = sum(ok for _, ok, _, _ in rec.checks)
    lines = [f"# End-to-end test, {time.strftime('%Y-%m-%d %H:%M %Z')}", "", f"**{passed} of {len(rec.checks)} checks passed.**", ""]
    lines += [f"- {k}: {v}" for k, v in env.items()]
    lines += ["", "| check | result | time | detail |", "|---|---|---|---|"]
    lines += [f"| {n} | {'pass' if ok else '**FAIL**'} | {s:.1f} s | {d.replace('|', '/')} |" for n, ok, s, d in rec.checks]
    lines += ["", "Every HTTP call, with its request, response and time: [transcript.jsonl](transcript.jsonl)."]
    (out / "report.md").write_text("\n".join(lines) + "\n")
    print(f"{passed} / {len(rec.checks)} passed -> {out / 'report.md'}")
    return passed == len(rec.checks)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("--base-url", help="test this server instead of deploying one")
    ap.add_argument("--api-key", default="")
    ap.add_argument("--no-fine-tuning", action="store_true")
    ap.add_argument("--instance", default="g6e.xlarge", help="48 GB for fine-tuning next to serving")
    ap.add_argument("--region", default="us-east-2")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rec = Recorder(out)
    sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    env = {"commit": sha, "fine-tuning": not a.no_fine_tuning}
    if a.base_url:
        run_checks(a.base_url.rstrip("/"), a.api_key, out, rec, not a.no_fine_tuning)
        raise SystemExit(0 if write_report(out, rec, env | {"server": a.base_url}) else 1)

    from selfjev.deploy import aws

    name, t0 = f"e2e-{time.strftime('%m%d-%H%M')}", time.time()
    my_ip = urllib.request.urlopen("https://checkip.amazonaws.com", timeout=10).read().decode().strip()
    cmd = f"selfjev deploy aws up --name {name} --instance {a.instance} --region {a.region} --ref {sha[:10]} --fine-tuning"
    env |= {"deployment": f"`{cmd}`"}
    try:
        d = aws.up(name, a.instance, a.region, allow_cidr=f"{my_ip}/32", ref=sha, max_hours=2, ssh=True, fine_tuning=True)
        env |= {"instance": d["instance_id"], "ready after": f"{(time.time() - t0) / 60:.1f} min (launch, install, model download)"}

        def ready():
            assert d["ready"], "not healthy after 30 min: see setup.log"
            return d["endpoint"]

        rec.check("deploy: the server answers /health", ready)
        if d["ready"]:
            run_checks(d["endpoint"], d["api_key"], out, rec, not a.no_fine_tuning)
    finally:  # teardown first and on its own: nothing below may skip it
        rec_path = aws.STATE / f"{name}.json"
        if rec_path.exists():
            d = json.loads(rec_path.read_text())
            if d.get("ssh"):  # the box's first-boot log, for the record
                opts = ["-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=15"]
                cmd = [*d["ssh"].split(), *opts, "sudo cat /var/log/selfjev-setup.log"]
                (out / "setup.log").write_text(subprocess.run(cmd, capture_output=True, text=True).stdout[-200_000:])
            try:
                aws.down(name)
                env["teardown"] = "terminated; security group and key pair deleted"
            except Exception as e:
                env["teardown"] = f"FAILED ({e!r}): terminate {d['instance_id']} in {d['region']} by hand"
                print(env["teardown"])
            hours = (time.time() - t0) / 3600
            env["cost"] = f"≈ ${hours * aws.MACHINES.get(a.instance, ('', 0))[1]:.2f} ({a.instance}, {hours:.2f} h)"
        else:  # up() failed before it recorded the box: say where to look instead of leaving it silently
            env["teardown"] = f"NO RECORD: check EC2 in {a.region} for Name=selfjev-{name} and terminate it by hand"
            print(env["teardown"])
    raise SystemExit(0 if write_report(out, rec, env) else 1)


if __name__ == "__main__":
    main()
