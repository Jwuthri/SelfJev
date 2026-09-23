import random, sys, json, torch
from collections import Counter, defaultdict
from personal_jev.custom import ARCH
from personal_jev.train import grouped_loss, question_correct, select_data
from personal_jev.train_custom import DEFAULTS, build, encode_items, forward_items, score_items
bs = int(sys.argv[1]); lr = float(sys.argv[2]); steps = int(sys.argv[3])
cfg = DEFAULTS | json.load(open("configs/custom_frozen.json"))
cfg["arch"] = ARCH | cfg["arch"] | json.loads(sys.argv[4] if len(sys.argv) > 4 else "{}")
torch.manual_seed(0)
tok, model, _ = build(cfg)
model.to("mps")
rng = random.Random(13)
tr, va = select_data(cfg, rng)
items, states, _ = encode_items(tok, tr, 2048, 256)
vitems, vstates, _ = encode_items(tok, va, 2048, 256)
vitems = random.Random(1).sample(vitems, 400)
smp = random.Random(13).sample(items, 512)
model.fit_standardization([states[k] for k in sorted({it["state"] for it in smp})], [x for it in smp for x in it["ids"]])
opt = torch.optim.AdamW(model.new_parameters(), lr=lr, weight_decay=0.0)
def ev():
    sc = score_items(model, vitems, vstates, 8192)
    by = defaultdict(list)
    for s, it in zip(sc, vitems):
        by[it["type"]].append(question_correct(s, it))
    return {t: round(sum(v) / len(v), 3) for t, v in sorted(by.items())}, round(grouped_loss(torch.tensor([v for s in sc for v in s]), vitems).item() / len(vitems), 4)
print("init", ev(), flush=True)
order = list(range(len(items))); rng.shuffle(order)
pos = 0
for step in range(1, steps + 1):
    if pos + bs > len(order): rng.shuffle(order); pos = 0
    b = [items[i] for i in order[pos:pos + bs]]; pos += bs
    model.train()
    loss = grouped_loss(forward_items(model, b, states, 16384), b) / len(b)
    opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.new_parameters(), 1.0); opt.step()
    if step % 50 == 0:
        print(step, "train", round(loss.item(), 3), "val", ev(), flush=True)
