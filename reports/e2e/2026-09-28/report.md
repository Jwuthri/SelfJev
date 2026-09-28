# End-to-end test, 2026-09-28 (rebuilt: the script crashed at teardown, after every check)

**14 of 14 checks passed.**

- commit: `0a146ba2b2bf0492ba55c35c34174e9a01e5172f` (`git checkout` in [setup.log](setup.log))
- deployment: `selfjev deploy aws up --name e2e-0928-1201 --instance g6e.xlarge --region us-east-2 --ref 0a146ba --fine-tuning` (NVIDIA L40S 48 GB, API port open to one IP)
- ready after: 5.4 min from launch (install, base-model download, server start)
- checks: 79 HTTP calls over 14.8 min ([transcript.jsonl](transcript.jsonl))
- teardown: the script's teardown crashed (see Notes); the instance was terminated by hand at 19:27 UTC, its security group and key pair deleted
- cost: ≈ $0.81 (g6e.xlarge $1.861/h, 19:01–19:27 UTC)

| check | result | detail |
|---|---|---|
| deploy: the server answers /health | pass | http://3.148.219.3:8000 |
| health (open) | pass | {'status': 'ok', 'model': 'selfjev-4b', 'queue': 0} |
| auth: a wrong key is refused | pass | 401 authentication_error |
| models | pass | ['selfjev-4b'] |
| decisions: every question type answered right | pass | {'refund': 0.992, 'spam': 0.017, 'paid': 1.0, 'team': 'billing', 'urgency': 1.976, 'topics': ['invoice']} |
| Jev compatibility: /api/alpha/decisions with model jev-latest | pass | {'refund': 0.992, 'spam': 0.017, 'paid': 1.0, 'team': 'billing', 'urgency': 1.976, 'topics': ['invoice']} |
| object state (JSON) | pass | {'refund': 0.992, 'spam': 0.017, 'paid': 1.0, 'team': 'billing', 'urgency': 1.976, 'topics': ['invoice']} |
| errors: 422 with the field, 404 for an unknown model | pass | 422 questions.q.criteria; 404 model |
| 16 concurrent requests | pass | 16 requests in 18.6 s; per request p50 18637 ms, max 18642 ms |
| fine-tuning: upload the training and validation files | pass | {'train': 'file_91d764f064ff496597eacdfc: 207 rows, 508 questions', 'val': 'file_1d8b9986461b48b7ab28e64a: 17 rows, 41 questions'} |
| fine-tuning: a bad line is named | pass | 422 file.line_2: line 2: Value error, answers must cover exactly the questions: ['q0', 'q1'] |
| fine-tuning: a supervised job succeeds and its model answers | pass | selfjev-4b:ft-e2e-supervised-3e353f6e in 8.4 min; events ['succeeded: selfjev-4b:ft-e2e-supervised-3e353f6e', 'validation at step 0', 'validation at step 16'];  |
| fine-tuning: a rlcd job succeeds and its model answers | pass | selfjev-4b:ft-e2e-rlcd-6405d15d in 5.4 min; events ['succeeded: selfjev-4b:ft-e2e-rlcd-6405d15d', 'validation at step 0', 'validation at step 16']; answers {'re |
| metrics | pass | ['selfjev_requests_total{route="/api/alpha/decisions",status="200"} 1', 'selfjev_requests_total{route="/health",status="200"} 3', 'selfjev_requests_total{route= |

## Notes

- **Cold start.** The first decisions request took 39.0 s (GPU kernels compile on first use); the next single requests took 280–18630 ms round trip, about 70 ms of it network. Fixed after this run: `selfjev serve` now warms the model up before `/health` answers.
- **Concurrency.** The 16 concurrent requests were batched together and all returned after 18.6 s (the first batch of that size, also cold). Bursts sent by hand afterwards, while a fine-tuning job trained on the same GPU: 1 request 0.45 s, 8 concurrent 1.8 s, 16 concurrent 4.4–6.4 s. Concurrent requests share one batch and all wait for it; not yet measured without a training job on the GPU.
- **Fine-tuning over HTTP.** 207 texts / 508 questions (batch `numdate_neg_v1`, training rows) and 41 validation questions: the supervised job took 8.4 min and the RLCD job 5.4 min (16 steps each, starting from `selfjev-4b`); both models were served at once next to `selfjev-4b` and still answered the test ticket right. The uploaded files are `e2e_train.jsonl` and `e2e_val.jsonl`; `e2e_bad.jsonl` is the deliberately broken one.
- **Teardown incident.** While the test ran, a plain `uv run` in the same checkout re-synced the environment without the `deploy` extra and removed `botocore`'s data; the script's `status()` call before `down()` then raised and the box stayed up for about 6 minutes until terminated by hand. Fixed: the dev group installs the `deploy` extra, and the script tears down before anything else.
