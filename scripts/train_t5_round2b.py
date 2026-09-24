"""Train the full pretrained T5 reader on the frozen historical R2b question IDs."""
import argparse, gc, json, math, random, time
from pathlib import Path
import torch
from peft import LoraConfig, get_peft_model
from personal_jev.t5_shared import T5SharedScorer, t5_text_lora_targets
from personal_jev.data import load, sha256_file
from personal_jev.train import grouped_loss, question_correct
from run_challenger import items, batches, save


def shuffled(item, rng):
    if item['type']=='binary':return item
    p=list(range(len(item['ids'])));rng.shuffle(p)
    target=p.index(item['target']) if item['type']=='multiclass' else [item['target'][i] for i in p]
    return item|{'ids':[item['ids'][i] for i in p],'target':target,
        'entry':item['entry']|{'branches':[item['entry']['branches'][i] for i in p]}}


@torch.no_grad()
def validate(sc, data, budget):
    sc.model.eval(); total=0.; correct=0
    for batch in batches(data,budget,random.Random(0)):
        chunk=[data[i] for i in batch]; scores=sc.shared_entries([x['entry'] for x in chunk])
        total+=grouped_loss(scores,chunk).item(); k=0
        for it in chunk:
            n=len(it['ids']);correct+=question_correct(scores[k:k+n].tolist(),it);k+=n
    return {'loss':total/len(data),'question_accuracy':correct/len(data),'n':len(data)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',default='configs/t5gemma2_r2b_full.json')
    ap.add_argument('--smoke',action='store_true');args=ap.parse_args()
    cfg=json.loads(Path(args.config).read_text());selection=json.loads(Path(cfg['selection_manifest']).read_text())
    out=Path(cfg['out_dir']+('_smoke' if args.smoke else ''));out.mkdir(parents=True,exist_ok=True)
    if (out/'train_meta.json').exists():raise FileExistsError(f'Refusing to overwrite completed run: {out}')
    for split in ['train','validation']:
        row=selection[split]
        assert sha256_file(row['file'])==row['sha256']
    seed=cfg['seed'];torch.manual_seed(seed);rng=random.Random(seed)
    sc=T5SharedScorer(max_length=cfg['max_length'])
    tr_ex=load([selection['train']['file']],{'train'});va_ex=load([selection['validation']['file']],{'validation'})
    assert [x['id'] for x in tr_ex]==selection['train']['ids']
    assert [x['id'] for x in va_ex]==selection['validation']['ids']
    if args.smoke:tr_ex=tr_ex[:8];va_ex=va_ex[:8]
    tr,dt=items(sc,tr_ex);va,dv=items(sc,va_ex)
    if dt or dv:raise ValueError({'matched_question_exclusions_not_allowed':{'train':dt,'validation':dv}})
    targets,coverage=t5_text_lora_targets(sc.model,cfg['lora']['target_modules'])
    lc=cfg['lora'];sc.model=get_peft_model(sc.model,LoraConfig(r=lc['r'],lora_alpha=lc['alpha'],
        lora_dropout=lc['dropout'],target_modules=targets,bias='none'))
    sc.model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    params=[p for p in sc.model.parameters() if p.requires_grad]
    opt=torch.optim.AdamW(params,lr=cfg['lr'],weight_decay=cfg['weight_decay'])
    # Equal questions per optimizer step; microbatch splitting changes memory only.
    nper=8 if args.smoke else cfg['optimizer_questions'];epochs=1 if args.smoke else cfg['epochs']
    steps=math.ceil(len(tr)/nper)*epochs; warm=max(1,round(cfg['warmup_ratio']*steps))
    sched=torch.optim.lr_scheduler.LambdaLR(opt,lambda s:min((s+1)/warm,max(0.,(steps-s)/max(1,steps-warm))))
    meta={'config':cfg,'model':sc.meta,'trainable_parameters':sum(p.numel() for p in params),
        'train_questions':len(tr),'val_questions':len(va),'selection_sha256':sha256_file(cfg['selection_manifest']),
        'train_ids_sha256':sha256_file(selection['train']['file']),'candidate_shuffle':True,
        'lora_targets':targets,'lora_target_coverage':coverage,'initialization':'fresh pretrained T5Gemma 2, not the R1 adapter',
        'comparison_limits':'same R2b eligible IDs and one epoch; tokenizer, format, 72-question step grouping and architecture differ',
        'versions':{'torch':torch.__version__},'gpu':torch.cuda.get_device_name(),'log':[]}
    save(out/'manifest.json',meta); print('TRAIN',len(tr),len(va),'steps',steps,'LoRA',meta['trainable_parameters'],flush=True)
    best=float('inf');step=0;start=time.perf_counter();ref_items=va[:32];reference=None
    def checkpoint():
        nonlocal best,reference
        v=validate(sc,va,cfg['microbatch_tokens']);meta['log'].append({'step':step,'validation':v,'wall_s':time.perf_counter()-start})
        print('VALIDATION',step,v,flush=True)
        if v['loss']<best:
            best=v['loss'];sc.model.save_pretrained(out/'adapter');meta['best']={'step':step,**v}
            reference=[sc.shared_entries([it['entry']]).cpu().tolist() for it in ref_items]
        save(out/'progress.json',meta)
    checkpoint()
    for epoch in range(epochs):
        order=list(range(len(tr)));rng.shuffle(order)
        for pos in range(0,len(order),nper):
            its=[shuffled(tr[i],rng) for i in order[pos:pos+nper]]
            sc.model.train();opt.zero_grad(set_to_none=True);total=0.
            for mb in batches(its,cfg['microbatch_tokens'],rng):
                chunk=[its[i] for i in mb];scores=sc.forward_entries([it['entry'] for it in chunk])
                loss=grouped_loss(scores,chunk)/len(its)
                if not torch.isfinite(loss):raise FloatingPointError('nonfinite training loss')
                loss.backward();total+=loss.item()
            missing=[n for n,p in sc.model.named_parameters() if p.requires_grad and p.grad is None]
            if missing:raise RuntimeError({'missing_gradients':missing})
            if step==0:
                gradient_audit={}
                for side,path in [('encoder','.encoder.text_model.layers.'),('decoder','.decoder.layers.')]:
                    selected=[p for n,p in sc.model.named_parameters() if path in n and p.requires_grad]
                    if not selected:raise AssertionError(f'No trainable {side} parameters')
                    gn=float(torch.stack([p.grad.float().norm().square() for p in selected]).sum().sqrt())
                    if not math.isfinite(gn) or gn<=0:raise AssertionError(f'No finite nonzero {side} gradient: {gn}')
                    gradient_audit[side]={'trainable_parameters':sum(p.numel() for p in selected),'gradient_norm':gn}
                meta['first_step_gradient_audit']=gradient_audit
                print('GRADIENT_AUDIT',gradient_audit,flush=True)
            norm=torch.nn.utils.clip_grad_norm_(params,cfg['max_grad_norm'])
            if not torch.isfinite(norm) or float(norm)==0:raise FloatingPointError(f'invalid gradient {norm}')
            opt.step();sched.step();step+=1
            if step%10==0 or args.smoke:
                meta['log'].append({'step':step,'train_loss':total,'gradient_norm':float(norm)})
                print('STEP',step,'/',steps,'loss',round(total,4),'elapsed',round(time.perf_counter()-start),flush=True)
            if step%cfg['eval_every']==0 or step==steps:checkpoint()
    meta.update(steps=step,wall_s=time.perf_counter()-start,adapter_sha256=sha256_file(out/'adapter/adapter_model.safetensors'))
    del scores,loss,opt,sched,params,sc;gc.collect();torch.cuda.empty_cache()
    re=T5SharedScorer(adapter=str(out/'adapter'),max_length=cfg['max_length'])
    again=[re.shared_entries([it['entry']]).cpu().tolist() for it in ref_items]
    delta=max(abs(a-b) for x,y in zip(reference,again) for a,b in zip(x,y))
    meta['reload_check']={'questions':len(ref_items),'max_abs_score_diff':delta}
    if delta>1e-4:raise AssertionError(meta['reload_check'])
    save(out/'train_meta.json',meta);print('TRAIN_COMPLETE',meta['best'],'reload',delta,flush=True)

if __name__=='__main__':main()
