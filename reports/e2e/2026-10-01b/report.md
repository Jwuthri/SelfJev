# End-to-end test, 2026-10-01 14:00 PDT

**20 of 21 checks passed.**

- commit: a666743597a25fc7f87c35bfc22c50dffec6e8ae
- fine-tuning: True
- deployment: `selfjev deploy aws up --name e2e-1001-1331 --instance g6e.2xlarge --region us-east-2 --ref a666743597 --fine-tuning`
- instance: i-0cb58ea7afdd6fb9e
- ready after: 5.8 min (launch, install, model download)
- teardown: terminated; security group and key pair deleted
- cost: ≈ $1.06 (g6e.2xlarge, 0.47 h)

| check | result | time | detail |
|---|---|---|---|
| deploy: the server answers /health | pass | 0.0 s | http://18.191.66.24:8000 |
| health (open) | pass | 0.2 s | {'status': 'ok', 'model': 'selfjev-4b', 'queue': 0} |
| auth: a wrong key is refused | pass | 0.1 s | 401 authentication_error |
| models | pass | 0.1 s | ['selfjev-4b'] |
| decisions: every question type answered right | pass | 0.3 s | {'refund': 0.993, 'spam': 0.011, 'paid': 1.0, 'team': 'billing', 'urgency': 1.99, 'topics': ['invoice']} |
| Jev compatibility: /api/alpha/decisions with model jev-latest | pass | 0.3 s | {'refund': 0.993, 'spam': 0.011, 'paid': 1.0, 'team': 'billing', 'urgency': 1.99, 'topics': ['invoice']} |
| object state (JSON) | pass | 0.3 s | {'refund': 0.993, 'spam': 0.012, 'paid': 1.0, 'team': 'billing', 'urgency': 1.99, 'topics': ['invoice']} |
| errors: 422 with the field, 404 for an unknown model | pass | 0.2 s | 422 questions.q.criteria; 404 model |
| 16 concurrent requests | pass | 9.5 s | 16 requests in 9.5 s; per request p50 9508 ms, max 9511 ms |
| bursts of mixed traffic: no kernel-tuning stalls | **FAIL** | 64.3 s | AssertionError: a burst waited 13883 ms |
| images: photos sent as files, answered right | pass | 7.8 s | 45 of 48 questions right on 24 photos; per request p50 312 ms |
| images: text and image parts in one state | pass | 0.7 s | {'q0': 'keeshond', 'q1': 0.007} |
| images: an unreadable image is a 422 | pass | 0.2 s | 422 invalid_request_error: state: an image part must be a base64 image data URL (UnidentifiedImageError: cannot identify image file <_io.BytesIO ob |
| images: 8 concurrent requests | pass | 1.1 s | 8 photos at once in 1.1 s; 15 of 16 right |
| images: the async client | pass | 0.8 s | 8 of 8 right |
| fine-tuning: upload the training and validation files | pass | 0.8 s | {'train': 'file_171cea854963456184cddc13: 207 rows, 508 questions', 'val': 'file_02abe650001c48da925c3d83: 17 rows, 41 questions'} |
| fine-tuning: a bad line is named | pass | 0.1 s | 422 file.line_2: line 2: Value error, answers must cover exactly the questions: ['q0', 'q1'] |
| fine-tuning: a supervised job succeeds and its model answers | pass | 464.1 s | selfjev-4b:ft-e2e-supervised-502d0a25 in 7.7 min; events ['succeeded: selfjev-4b:ft-e2e-supervised-502d0a25', 'validation at step 0', 'validation at step 15']; answers {'refund': 1.0, 'spam': 0.001, 'paid': 1.0, 'team': 'billing', 'urgency': 2.0, 'topics': ['invoice']} |
| fine-tuning: a rlcd job succeeds and its model answers | pass | 302.9 s | selfjev-4b:ft-e2e-rlcd-521f89a0 in 5.0 min; events ['succeeded: selfjev-4b:ft-e2e-rlcd-521f89a0', 'validation at step 0', 'validation at step 15']; answers {'refund': 0.999, 'spam': 0.002, 'paid': 1.0, 'team': 'billing', 'urgency': 1.999, 'topics': ['invoice']} |
| fine-tuning: a folder of photos + text rows -> a model that reads images | pass | 136.9 s | 200 rows (150 photos + 50 texts, 421 questions, 20.3 MB) -> selfjev-4b:ft-e2e-images-f21c88b1 in 2.3 min; beans held-out photos right: 32/32 before, 29/32 after |
| metrics | pass | 0.1 s | ['selfjev_requests_total{route="/api/alpha/decisions",status="200"} 1', 'selfjev_requests_total{route="/health",status="200"} 3', 'selfjev_requests_total{route="/v1/files",status="200"} 3', 'selfjev_requests_total{route="/v1/files",status="422"} 1', 'selfjev_requests_total{route="/v1/fine_tuning/jobs",status="200"} 3', 'selfjev_requests_total{route="/v1/fine_tuning/jobs/ftjob_502d0a25cb2542f4ab94" |

Every HTTP call, with its request, response and time: [transcript.jsonl](transcript.jsonl).
