# Superseded: decoder-only targeting error

The initial pilot accidentally applied LoRA only to the decoder: its encoder filter used `model.encoder.layers`, while the real native path is `model.encoder.text_model.layers`. The retained pretrained encoder was frozen. The adapter contains 208 decoder tensors and zero encoder tensors (2,981,888 trainable parameters).

Its measured 73.84% development / 76.80% eval2 accuracy and 266.61 ms L40S primary latency are valid **decoder-only** results, not results of the intended encoder-and-decoder adaptation. The old T5 adapter rescore remains valid. No test labels were used to retrain or select this checkpoint, but this implementation correction was discovered after reviewing evaluation results and adapter coverage.

Raw results and the original adapter are retained. The corrected run uses `runs/t5gemma2_r2b_full`, the same frozen data and recipe, explicit coverage of both native text stacks, and first-step gradient audits. Do not promote this superseded pilot as the requested model.
