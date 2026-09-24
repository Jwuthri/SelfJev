"""Training-only wiring diagnostic; this adapter is never used for evaluation."""
import json,time
from pathlib import Path
import torch
from peft import LoraConfig,get_peft_model
from personal_jev.t5_shared import T5SharedScorer,t5_text_lora_targets
from personal_jev.data import load
from personal_jev.train import grouped_loss,question_correct
from run_challenger import items,save

torch.manual_seed(13)
sc=T5SharedScorer(max_length=16384)
es=load(['runs/t5_round2b_inputs/train.jsonl'],{'train'})[:8]
data,dropped=items(sc,es);assert not dropped
names,coverage=t5_text_lora_targets(sc.model)
sc.model=get_peft_model(sc.model,LoraConfig(r=16,lora_alpha=32,lora_dropout=.05,target_modules=names,bias='none'))
sc.model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
params=[p for p in sc.model.parameters() if p.requires_grad]
opt=torch.optim.AdamW(params,lr=2e-4,weight_decay=0)
result={'ids':[e['id'] for e in es],'source':'first eight frozen training examples; no validation/test labels',
        'purpose':'wiring/optimization diagnostic only; adapter is not used for quality measurements','log':[]}
start=time.perf_counter()
for step in range(81):
    if step%5==0:
        sc.model.eval()
        with torch.no_grad():
            scores=sc.shared_entries([x['entry'] for x in data]);loss=grouped_loss(scores,data).item()/len(data)
        k=0;correct=0
        for it in data:
            n=len(it['ids']);correct+=question_correct(scores[k:k+n].tolist(),it);k+=n
        result['log'].append({'step':step,'loss':loss,'correct':correct,'n':len(data),'wall_s':time.perf_counter()-start})
        save('reports/t5_round2b_2026-09-24/overfit_check.json',result)
        print('OVERFIT',result['log'][-1],flush=True)
        if correct==len(data) and loss<.05:break
    if step==80:break
    sc.model.train();opt.zero_grad(set_to_none=True)
    for it in data:
        loss=grouped_loss(sc.forward_entries([it['entry']]),[it])/len(data)
        loss.backward()
    torch.nn.utils.clip_grad_norm_(params,1.)
    opt.step()
result['passed']=correct==len(data) and result['log'][-1]['loss']<.05
save('reports/t5_round2b_2026-09-24/overfit_check.json',result)
