**I rebuilt the core idea behind Jev in a day, with an open 4B model. On my benchmark it's statistically tied with Jev.**

Jev turns a model into a typed decision engine: yes/no, pick one, pick many, with probabilities and no text generation. I wanted to know how much of that is secret sauce.

**The recipe:**
• Open Qwen3-Reranker-4B, frozen
• A small LoRA adapter (0.3% of the weights), trained on ~10K examples in under an hour on one cloud GPU
• A "shared-prefix tree": the model reads the text once, and every question branches off it. That makes it up to 37× faster than my first version when you ask many questions about the same text.

**Results on the same 3,471 test questions:**
• Open 4B, no training: 62.8%
• + adapter: 80.3%
• + shared-prefix tree: **81.6%**
• Jev: 82.7% (the gap is not statistically significant, p = 0.08)
• GPT-6 Astra: 85.8%

Mine beats Jev on multi-label questions (51.7% vs 40.1% exact match). Jev still wins on dates, arithmetic and sarcasm.

**The honest takeaway:** the idea isn't the moat. A small open model gets there in a day. What's left is data for the hard reasoning cases, calibration that holds on new tasks, and serving. Credit where due: Jev answered all 3,471 questions for $0.06.

**Where Jev is clearly ahead: speed.** Jev answers in ~150 ms whatever the size. Mine, on one small A10G GPU, takes 120 ms for one question on a short text and up to 1.2 s for 16 questions on a 4K-token text.

Caveats: my own benchmark (11 public datasets plus an LLM-written test set of hard cases), single runs.

Round 2 added 10K new verified hard cases:
• My own hard-case questions: 78.4% → 83.0%
• Overall: the same, 81.2%

This benchmark is mostly public datasets, so it can't see the gain. A fresh test set is being built for the rematch.
