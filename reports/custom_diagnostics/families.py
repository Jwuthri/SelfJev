import random, sys, json, torch
from collections import defaultdict
from personal_jev.custom import ARCH
from personal_jev.data import load
from personal_jev.train import grouped_loss, question_correct
from personal_jev.train_custom import DEFAULTS, build, encode_items, forward_items, score_items
fams = sys.argv[1].split(","); steps = int(sys.argv[2]); arch = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
files = ["data/hf.jsonl", "data/synthetic.jsonl"]
cfg = DEFAULTS | {"backbone": "frozen", "dtype": "bfloat16"}
cfg["arch"] = ARCH | arch
torch.manual_seed(0)
tok, model, _ = build(cfg)
model.to("mps")
rng = random.Random(0)
tr = [e for e in load(files, {"train"}) if e["family"] in fams]
by = defaultdict(list)
for e in tr: by[e["family"]].append(e)
tr = [e for f in sorted(by) for e in (rng.sample(by[f], 1600) if len(by[f]) > 1600 else by[f])]
va = [e for e in load(files, {"validation"}) if e["family"] in fams]
items, states, _ = encode_items(tok, tr, 2048, 256)
vitems, vstates, _ = encode_items(tok, va, 2048, 256)
smp = random.Random(13).sample(items, min(512, len(items)))
model.fit_standardization([states[k] for k in sorted({it["state"] for it in smp})], [x for it in smp for x in it["ids"]])
opt = torch.optim.AdamW(model.new_parameters(), lr=1e-3, weight_decay=0.0)
def ev():
    sc = score_items(model, vitems, vstates, 8192)
    acc = defaultdict(list)
    for s, it in zip(sc, vitems): acc[it["family"]].append(question_correct(s, it))
    return {f[:12]: round(sum(v) / len(v), 3) for f, v in sorted(acc.items())}
order = list(range(len(items))); rng.shuffle(order); pos = 0
print(len(items), "train questions", flush=True)
for step in range(1, steps + 1):
    if pos + 32 > len(order): rng.shuffle(order); pos = 0
    b = [items[i] for i in order[pos:pos + 32]]; pos += 32
    model.train()
    loss = grouped_loss(forward_items(model, b, states, 16384), b) / len(b)
    opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.new_parameters(), 1.0); opt.step()
    if step % 50 == 0: print(step, round(loss.item(), 3), ev(), flush=True)
