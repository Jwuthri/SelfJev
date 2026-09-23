import random, sys, json, torch
from personal_jev.data import load
from personal_jev.train import grouped_loss, question_correct
from personal_jev.train_custom import DEFAULTS, build, encode_items, forward_items, score_items
fam = sys.argv[1]; lr = float(sys.argv[2]); arch = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
cfg = DEFAULTS | {"backbone": "frozen", "dtype": "bfloat16", "arch": DEFAULTS["arch"] | arch}
from personal_jev.custom import ARCH; cfg["arch"] = ARCH | arch
torch.manual_seed(0)
tok, model, _ = build(cfg)
model.to("mps")
tr = [e for e in load("data/hf.jsonl", {"train"}) if e["family"] == fam][:1600]
va = [e for e in load("data/hf.jsonl", {"validation"}) if e["family"] == fam]
items, states, _ = encode_items(tok, tr, 2048, 256)
vitems, vstates, _ = encode_items(tok, va, 2048, 256)
model.fit_standardization(states[:300], [x for it in items[:300] for x in it["ids"]])
opt = torch.optim.AdamW(model.new_parameters(), lr=lr, weight_decay=0.0)
rng = random.Random(0)
def ev():
    sc = score_items(model, vitems, vstates, 8192)
    return sum(question_correct(s, it) for s, it in zip(sc, vitems)) / len(vitems), grouped_loss(torch.tensor([v for s in sc for v in s]), vitems).item() / len(vitems)
print("init", ev(), flush=True)
order = list(range(len(items)))
for step in range(1, 301):
    if (step - 1) % 50 == 0: rng.shuffle(order)
    b = [items[i] for i in order[((step - 1) % 50) * 32:((step - 1) % 50) * 32 + 32]]
    model.train()
    loss = grouped_loss(forward_items(model, b, states, 8192), b) / len(b)
    opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.new_parameters(), 1.0); opt.step()
    if step % 50 == 0:
        print(step, "train", round(loss.item(), 3), "val acc/loss", ev(), flush=True)
