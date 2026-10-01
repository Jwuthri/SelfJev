# End-to-end test, 2026-10-01 15:45 PDT

**21 of 21 checks passed.**

- commit: 6b43d94416b9b1493fc4c3585a3cd4c54fc8a384
- fine-tuning: True
- deployment: `selfjev deploy aws up --name e2e-1001-1519 --instance g6e.2xlarge --region us-east-2 --ref 6b43d94416 --fine-tuning`
- instance: i-05fd0d6595bc17de6
- ready after: 5.4 min (launch, install, model download)
- teardown: terminated; security group and key pair deleted
- cost: ≈ $0.97 (g6e.2xlarge, 0.43 h)

| check | result | time | detail |
|---|---|---|---|
| deploy: the server answers /health | pass | 0.0 s | http://3.21.247.253:8000 |
| health (open) | pass | 0.1 s | {'status': 'ok', 'model': 'selfjev-4b', 'queue': 0} |
| auth: a wrong key is refused | pass | 0.1 s | 401 authentication_error |
| models | pass | 0.1 s | ['selfjev-4b'] |
| decisions: every question type answered right | pass | 0.3 s | {'refund': 0.993, 'spam': 0.011, 'paid': 1.0, 'team': 'billing', 'urgency': 1.99, 'topics': ['invoice']} |
| Jev compatibility: /api/alpha/decisions with model jev-latest | pass | 0.3 s | {'refund': 0.993, 'spam': 0.011, 'paid': 1.0, 'team': 'billing', 'urgency': 1.99, 'topics': ['invoice']} |
| object state (JSON) | pass | 0.3 s | {'refund': 0.993, 'spam': 0.012, 'paid': 1.0, 'team': 'billing', 'urgency': 1.989, 'topics': ['invoice']} |
| errors: 422 with the field, 404 for an unknown model | pass | 0.1 s | 422 questions.q.criteria; 404 model |
| 16 concurrent requests | pass | 1.4 s | 16 requests in 1.4 s; per request p50 1396 ms, max 1400 ms |
| bursts of mixed traffic: none stalls (slowest < 3x median time per token) | pass | 40.5 s | 12 of 20 bursts over 4K tokens: median 214 ms per 1K tokens, slowest 261 |
| images: photos sent as files, answered right | pass | 7.8 s | 45 of 48 questions right on 24 photos; per request p50 308 ms |
| images: text and image parts in one state | pass | 0.8 s | {'q0': 'bean rust', 'q1': 0.963} |
| images: an unreadable image is a 422 | pass | 0.2 s | 422 invalid_request_error: state: an image part must be a base64 image data URL (UnidentifiedImageError: cannot identify image file <_io.BytesIO ob |
| images: 8 concurrent requests | pass | 1.0 s | 8 photos at once in 1.0 s; 15 of 16 right |
| images: the async client | pass | 0.8 s | 7 of 8 right |
| fine-tuning: upload the training and validation files | pass | 0.8 s | {'train': 'file_e7ed397969e4413ca248ab8d: 207 rows, 508 questions', 'val': 'file_b8b56f8556e646f39e7d0d88: 17 rows, 41 questions'} |
| fine-tuning: a bad line is named | pass | 0.1 s | 422 file.line_2: line 2: Value error, answers must cover exactly the questions: ['q0', 'q1'] |
| fine-tuning: a supervised job succeeds and its model answers | pass | 323.1 s | selfjev-4b:ft-e2e-supervised-384bd0b7 in 5.4 min; events ['succeeded: selfjev-4b:ft-e2e-supervised-384bd0b7', 'validation at step 0', 'validation at step 15']; answers {'refund': 1.0, 'spam': 0.001, 'paid': 1.0, 'team': 'billing', 'urgency': 2.0, 'topics': ['invoice']} |
| fine-tuning: a rlcd job succeeds and its model answers | pass | 322.9 s | selfjev-4b:ft-e2e-rlcd-b6336f82 in 5.4 min; events ['succeeded: selfjev-4b:ft-e2e-rlcd-b6336f82', 'validation at step 0', 'validation at step 15']; answers {'refund': 0.999, 'spam': 0.003, 'paid': 1.0, 'team': 'billing', 'urgency': 1.999, 'topics': ['invoice']} |
| fine-tuning: a folder of photos + text rows -> a model that reads images | pass | 136.3 s | 200 rows (150 photos + 50 texts, 421 questions, 19.9 MB) -> selfjev-4b:ft-e2e-images-7f8f7614 in 2.3 min; beans held-out photos right: 30/32 before, 31/32 after |
| metrics | pass | 0.1 s | ['selfjev_requests_total{route="/api/alpha/decisions",status="200"} 1', 'selfjev_requests_total{route="/health",status="200"} 3', 'selfjev_requests_total{route="/v1/files",status="200"} 3', 'selfjev_requests_total{route="/v1/files",status="422"} 1', 'selfjev_requests_total{route="/v1/fine_tuning/jobs",status="200"} 3', 'selfjev_requests_total{route="/v1/fine_tuning/jobs/ftjob_384bd0b7745445b2bd71" |

Every HTTP call, with its request, response and time: [transcript.jsonl](transcript.jsonl).
