"""python smoke.py PORT: one noul + one choice question to a /v1/systemone server; prints the status line, then the reply."""

import json
import sys
import time
import urllib.error
import urllib.request

body = {
    "model": "x",
    "state": "Hi, I was charged twice for March. Please refund the duplicate today or I will cancel my plan.",
    "questions": {
        "q0": {"type": "noul", "instructions": "Is the customer asking for a refund?",
               "criteria": {"true": "the customer asks for a refund", "false": "the customer does not ask for a refund"}},
        "q1": {"type": "choice", "instructions": "Which team should handle this?",
               "criteria": {"billing": "payments, invoices, refunds", "tech": "bugs, outages, login problems"}},
    },
}  # fmt: skip
req = urllib.request.Request(
    f"http://127.0.0.1:{sys.argv[1]}/v1/systemone", json.dumps(body).encode(), {"content-type": "application/json"}
)
t = time.time()
try:
    with urllib.request.urlopen(req, timeout=600) as r:
        print(r.status, f"{(time.time() - t) * 1000:.0f} ms")
        print(json.dumps(json.load(r), indent=1)[:2500])
except urllib.error.HTTPError as e:
    print(e.code, e.read().decode()[:500])
