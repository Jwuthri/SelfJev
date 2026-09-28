# SelfJev-4B merged Hugging Face release

Published at https://huggingface.co/Jwuthrich/selfjev-4b-merged, commit `aed18d68e951f3cbbb84495c931f321fd5e03f10`.

- Base: `Qwen/Qwen3.5-4B` at `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
- Adapter SHA-256: `dfbf2834d883987893ec305a6093a345fd79c77f903f60f2f914cbe3b6058d1b`.
- Used the existing `selfjev.engine.vllm.merge` implementation in the locked project environment (torch 2.14.0, transformers 5.17.0, peft 0.21.0).
- Full checkpoint: two safetensors shards, 9,319,828,160 bytes total. Includes unchanged base vision weights, tokenizer/configuration and base LICENSE; SelfJev training and validation are text only.
- Integrity: all 738 tensors retain original shapes/dtypes and are finite; exactly the expected 152 adapter target tensors changed. The safetensors index resolves every listed key.
- Synthetic GPU smoke input: “I was charged twice. Please refund the duplicate payment.” Questions: “Does the customer want a refund?” and “Does the customer ask for a new credit card?”
- Adapter and merged checkpoint produced the same yes-minus-no logit margins, 4.5625 and -4.3125. This checks two simple cases; it is not a benchmark or a general numerical-equivalence guarantee. No vLLM benchmark was run.
- Anonymous Hub access checked every checksummed release file, including both shard SHA-256 values, once remotely and independently from the laptop. `publication.json`, `SHA256SUMS`, `verification.json` and `merge_meta.json` record the evidence.
- Model card source is `MODEL_CARD.md`. The adapter repository remains available. No local model computation or local git commit.

AWS: one g5.2xlarge in us-east-1, instance `i-0d2a8155413fe9cd5`, tagged Project=personal-jev and Name=selfjev-hf-merge-0928. User approved $3; on-demand pricing API confirmed $1.212/hour. Launched 17:18:50 UTC and termination requested 17:27:04 UTC on 2026-09-28. One-hour shutdown cap and terminate-on-shutdown were verified. Compute estimate ~ $0.17; storage/public IPv4 and transfer add to this (conservatively allow ~$0.84 for transmitting the complete checkpoint, before free allowances or deduplication). Final billing is not yet available.

Cleanup confirmed: instance terminated; security group `sg-0001aea61abb2fb73`, cloud key pair and local private key deleted. A delayed shutdown required a force/skip-OS-shutdown request.
