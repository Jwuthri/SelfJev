import random, sys, torch
from personal_jev.data import load
from personal_jev.train import grouped_loss, question_correct
from personal_jev.train_custom import DEFAULTS, build, encode_items, forward_items
cfg = DEFAULTS | {"backbone": "frozen", "dtype": sys.argv[1] if len(sys.argv) > 1 else "bfloat16"}
tok, model, _ = build(cfg)
model.to("mps")
ex = [e for e in load("data/hf.jsonl", {"train"}) if e["family"] == "hf_intent_banking77"][:64]
items, states, _ = encode_items(tok, ex, 2048, 256)
model.fit_standardization(states, [x for it in items for x in it["ids"]])
opt = torch.optim.AdamW(model.new_parameters(), lr=1e-3, weight_decay=0.0)
for step in range(151):
    model.train()
    s = forward_items(model, items, states, 8192)
    loss = grouped_loss(s, items) / len(items)
    opt.zero_grad(); loss.backward()
    if step % 25 == 0:
        k, acc = 0, 0
        spread = []
        for it in items:
            x = s[k:k + len(it["ids"])].detach(); k += len(it["ids"])
            acc += question_correct(x.tolist(), it); spread.append(x.std().item())
        g = {n.split(".")[0]: 0.0 for n, p in model.named_parameters() if not n.startswith("backbone.")}
        for n, p in model.named_parameters():
            if p.grad is not None: g[n.split(".")[0]] += p.grad.norm().item() ** 2
        print(f"step {step} loss {loss.item():.4f} acc {acc}/{len(items)} score std across cands {sum(spread)/len(spread):.4f} "
              f"grad {{{', '.join(f'{k}: {v**0.5:.2e}' for k, v in g.items())}}}", flush=True)
    opt.step()
