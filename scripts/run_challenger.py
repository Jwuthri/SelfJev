"""Reproducible challenger train/eval/bench using the existing question losses and reports."""
import argparse, gc, hashlib, json, math, random, statistics, time
from pathlib import Path
import torch
from personal_jev.challengers import ChallengerScorer
from personal_jev.schemas import parse_question,parse_request
from personal_jev.train import DEFAULTS,select_data,grouped_loss,question_correct
from personal_jev.data import load,sha256_file
from personal_jev import evaluate,benchmark
from personal_jev.classify import classify

def save(path,d):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(d,indent=2))

def items(sc,examples):
 out=[];dropped=[]
 for ex in examples:
  q=parse_question({'id':'q',**ex['question']})
  try:e=sc.entry(ex['state'],q)
  except Exception as err:
   from personal_jev.model import InputTooLong
   if not isinstance(err,InputTooLong):raise
   dropped.append(ex['id']);continue
  ids=[c.id for c in q.candidates]
  target=ex['target'] if q.type=='binary' else ids.index(ex['target']) if q.type=='multiclass' else [c in ex['target'] for c in ids]
  out.append(dict(entry=e,ids=list(range(e['n'])),target=target,type=q.type,id=ex['id']))
 return out,dropped

def batches(items,budget,rng):
 order=list(range(len(items)));rng.shuffle(order);bs=[]
 for start in range(0,len(order),128):
  cur=[];width=0;n=0
  for i in sorted(order[start:start+128],key=lambda i:items[i]['entry']['length']):
   it=items[i];pairs=it['entry']['n'];w=it['entry']['length']
   if cur and ((n+pairs)*max(width,w)>budget or len(cur)>=8):bs.append(cur);cur=[];n=0;width=0
   cur.append(i);n+=pairs;width=max(width,w)
  if cur:bs.append(cur)
 rng.shuffle(bs);return bs

@torch.no_grad()
def validate(sc,data,budget):
 sc.model.eval();loss=0;correct=0
 for b in batches(data,budget,random.Random(0)):
  chunk=[data[i] for i in b];s=sc.forward_entries([x['entry'] for x in chunk]);loss+=grouped_loss(s,chunk).item();k=0
  for it in chunk:
   n=len(it['ids']);correct+=question_correct(s[k:k+n].tolist(),it);k+=n
 return dict(loss=loss/len(data),accuracy=correct/len(data),n=len(data))

def checks(sc,out,strict=True):
 sc.model.eval();qs=[parse_question(x) for x in json.load(open('examples/request.json'))['questions']]
 state='Alice requested a refund. Bob explicitly did not request a refund. Checkout failed on Tuesday.'
 entries=[sc.entry(state,q) for q in qs]
 with torch.no_grad():
  shared=sc.shared_entries(entries)
  single=torch.cat([sc.shared_entries([e]) for e in entries])
  full=torch.cat([sc.forward_entries([e]) for e in entries])
  permutation=sc.shared_entries(entries[::-1]);splits=list(torch.split(permutation,[e['n'] for e in entries[::-1]]))
  reordered=torch.cat(splits[::-1])
  multi=[sc.entry(state+' Extra document '+str(i),q) for i,q in enumerate(qs)]
  multi_a=sc.forward_entries(multi);multi_b=torch.cat([sc.forward_entries([e]) for e in multi])
  report=dict(multiple_documents_max_abs=float((multi_a-multi_b).abs().max()),shared_single_max_abs=float((shared-single).abs().max()),shared_full_max_abs=float((shared-full).abs().max()),permutation_max_abs=float((shared-reordered).abs().max()),shared=shared.tolist(),full=full.tolist(),dtype=sc.dtype)
 save(out/'correctness.json',report)
 # BF16 batching can perturb scores. Reject gross cache/mask errors, record all residuals.
 if not torch.isfinite(shared).all():raise AssertionError(report)
 if strict and sc.dtype=='float32' and max(report[k] for k in ['shared_single_max_abs','shared_full_max_abs','permutation_max_abs','multiple_documents_max_abs'])>0.005:raise AssertionError(report)
 report['bf16_absolute_tolerance_exceeded']=sc.dtype=='bfloat16' and max(report[k] for k in ['shared_single_max_abs','shared_full_max_abs','permutation_max_abs','multiple_documents_max_abs'])>0.25
 save(out/'correctness.json',report)
 print('CORRECTNESS',report,flush=True)
 return report

def train(sc,args,out):
 from peft import LoraConfig,get_peft_model
 torch.manual_seed(13);rng=random.Random(13)
 cfg=DEFAULTS|dict(train_files=['data/hf.jsonl','data/synthetic.jsonl'],val_files=['data/hf.jsonl','data/synthetic.jsonl','data/eval.jsonl'],max_train_per_family=1600,max_val_questions=1200,max_train_questions=args.train_limit)
 train_ex,val_ex=select_data(cfg,rng)
 max_before=sc.max_length;sc.max_length=2048
 tr,dropped=items(sc,train_ex);va,vd=items(sc,val_ex);sc.max_length=max_before
 names=['q_proj','k_proj','v_proj','o_proj']
 if sc.name=='qwen35':names+=['in_proj_qkv','in_proj_z','in_proj_b','in_proj_a','out_proj']
 if sc.name=='gliclass':names=['query_proj','key_proj','value_proj']
 available={n.rsplit('.',1)[-1] for n,m in sc.model.named_modules() if isinstance(m,torch.nn.Linear)}
 targets=sorted(set(names)&available)
 if sc.name=='gemma4':targets=[n for n,m in sc.model.named_modules() if '.language_model.' in n and isinstance(m,torch.nn.Linear) and n.rsplit('.',1)[-1] in names]
 if not targets:raise ValueError(available)
 lc=LoraConfig(r=16,lora_alpha=32,lora_dropout=0.05,target_modules=targets,bias='none',modules_to_save=['text_projector','classes_projector','scorer'] if sc.name=='gliclass' else None)
 sc.model=get_peft_model(sc.model,lc)
 sc.model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
 params=[p for p in sc.model.parameters() if p.requires_grad]
 opt=torch.optim.AdamW(params,lr=2e-4,weight_decay=0.01)
 schedule=batches(tr,args.batch_tokens,rng);steps=math.ceil(len(schedule)/2)*args.epochs
 sched=torch.optim.lr_scheduler.LambdaLR(opt,lambda s:min((s+1)/max(1,int(.05*steps)),max(0,(steps-s)/max(1,.95*steps))))
 meta=dict(model=sc.meta,config=cfg,seed=13,epochs=args.epochs,lr=2e-4,weight_decay=0.01,candidate_shuffle=False,batch_tokens=args.batch_tokens,grad_accum=2,lora_targets=targets,trainable=sum(p.numel() for p in params),train_questions=len(tr),val_questions=len(va),dropped_train=dropped,dropped_val=vd,train_ids_sha=hashlib.sha256(json.dumps([i['id'] for i in tr]).encode()).hexdigest(),data={p:sha256_file(p) for p in set(cfg['train_files']+cfg['val_files'])},log=[])
 save(out/'train_manifest.json',meta);print('TRAIN', {k:meta[k] for k in ['train_questions','trainable','lora_targets']},'steps',steps,flush=True)
 best=float('inf');step=0;start=time.perf_counter()
 def checkpoint():
  nonlocal best
  v=validate(sc,va,args.batch_tokens);meta['log'].append(dict(step=step,validation=v,wall_s=time.perf_counter()-start));print('VALIDATION',step,v,flush=True)
  if v['loss']<best:
   best=v['loss'];sc.model.save_pretrained(out/'adapter');meta['best']=dict(step=step,**v)
  save(out/'train_progress.json',meta)
 checkpoint()
 for epoch in range(args.epochs):
  if epoch:schedule=batches(tr,args.batch_tokens,rng)
  for start_b in range(0,len(schedule),2):
   chunks=schedule[start_b:start_b+2];nq=sum(len(b) for b in chunks);sc.model.train();loss_total=0;opt.zero_grad(set_to_none=True)
   for b in chunks:
    its=[tr[i] for i in b];s=sc.forward_entries([x['entry'] for x in its]);loss=grouped_loss(s,its)/nq
    if not torch.isfinite(loss):raise FloatingPointError('nonfinite loss')
    loss.backward();loss_total+=float(loss.detach())
   norm=torch.nn.utils.clip_grad_norm_(params,1.0)
   if not torch.isfinite(norm):raise FloatingPointError('nonfinite gradients')
   if step==0:
    meta['first_gradient_norm']=float(norm);print('FIRST_GRADIENT',float(norm),flush=True)
    if float(norm)==0:raise RuntimeError('No adapter gradient')
   opt.step();sched.step();step+=1
   if step%10==0:print('STEP',step,'loss',round(loss_total,4),'seconds',round(time.perf_counter()-start),flush=True)
   if step%100==0:checkpoint()
 checkpoint();meta['steps']=step;meta['wall_s']=time.perf_counter()-start;save(out/'train_meta.json',meta)
 return meta

def bench(sc,out,grid=None,repeats=10):
 rows=[]
 for n,q,c,kind in (grid or [(512,1,3,'multiclass'),(512,16,3,'multiclass'),(2048,1,3,'multiclass'),(2048,16,3,'multiclass'),(8192,1,3,'multiclass'),(8192,16,3,'multiclass'),(2048,16,1,'binary')]):
  if sc.name=='gliclass' and n>2048:
   rows.append(dict(state_tokens=n,questions=q,candidates=c,status='not attempted: bidirectional dense tree memory/context extension unvalidated'));continue
  req=benchmark.make_request(sc.tokenizer,n,q,c,kind)
  try:
   classify(sc,req);torch.cuda.synchronize();torch.cuda.reset_peak_memory_stats();times=[]
   for _ in range(repeats):
    t=time.perf_counter();result=classify(sc,req);torch.cuda.synchronize();times.append((time.perf_counter()-t)*1000)
   row=dict(state_tokens=n,questions=q,candidates=c,type=kind,repeats=len(times),e2e_ms_p50=statistics.median(times),e2e_ms_p95=benchmark._pct(times,.95),peak_mb=torch.cuda.max_memory_allocated()/2**20,raw_ms=times,stats=result['meta'])
  except torch.OutOfMemoryError:
   gc.collect();torch.cuda.empty_cache();row=dict(state_tokens=n,questions=q,candidates=c,status='OOM')
  rows.append(row);save(out/'bench.json',dict(meta=sc.meta,gpu=torch.cuda.get_device_name(),rows=rows));print('BENCH',n,q,row.get('e2e_ms_p50',row.get('status')),flush=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('name',choices=['qwen35','gemma4','t5gemma2','gliclass']);ap.add_argument('--stage',choices=['smoke','all','eval','bench'],default='all');ap.add_argument('--adapter');ap.add_argument('--dtype',default='bfloat16');ap.add_argument('--check-long',action='store_true');ap.add_argument('--reference-kernels',action='store_true');ap.add_argument('--skip-zero-validation',action='store_true');ap.add_argument('--tag',default='');ap.add_argument('--batch-tokens',type=int,default=4096);ap.add_argument('--epochs',type=int,default=1);ap.add_argument('--train-limit',type=int);ap.add_argument('--gli-native',action='store_true');ap.add_argument('--t5-share-kv',action='store_true');ap.add_argument('--legacy-bf16-buffers',action='store_true');args=ap.parse_args()
 out=Path('runs/challengers')/(args.name+args.tag);report=Path('reports/challengers')/(args.name+args.tag);out.mkdir(parents=True,exist_ok=True);report.mkdir(parents=True,exist_ok=True)
 if args.reference_kernels:
  import inspect
  from transformers.models.qwen3_5 import modeling_qwen3_5 as native
  for key in ['torch_chunk_gated_delta_rule','torch_recurrent_gated_delta_rule','causal_conv1d_fn','causal_conv1d_update']:
   setattr(native,key,inspect.unwrap(getattr(native,key)))
 sc=ChallengerScorer(args.name,adapter=args.adapter,gli_native=args.gli_native,dtype=args.dtype,t5_share_kv=args.t5_share_kv,legacy_bf16_buffers=args.legacy_bf16_buffers)
 checks(sc,report/('native' if args.gli_native else 'shared'))
 if args.check_long:
  req=benchmark.make_request(sc.tokenizer,1024,2,3,'multiclass');req=parse_request(req)
  with torch.no_grad():
   es=[sc.entry(req.state,q) for q in req.questions];a=sc.shared_entries(es);b=sc.forward_entries(es)
  delta=float((a-b).abs().max());save(report/'long_check.json',dict(max_abs=delta,dtype=sc.dtype,shared=a.tolist(),full=b.tolist()))
  if sc.dtype=='float32' and delta>0.005:raise AssertionError(('long context cache check',delta))
 if args.stage=='smoke':
  ex=load(['data/eval.jsonl'],{'validation'})[:8];sc.model.train();its,_=items(sc,ex);s=sc.forward_entries([its[0]['entry']]);print('SMOKE SCORES',s.tolist(),flush=True)
 elif args.stage=='all':
  if not args.skip_zero_validation:evaluate.run(sc,['data/hf.jsonl','data/eval.jsonl'],['validation'],out_dir=report/'zero_validation')
  train(sc,args,out);del sc;gc.collect();torch.cuda.empty_cache()
  sc=ChallengerScorer(args.name,adapter=str(out/'adapter'),dtype=args.dtype,gli_native=args.gli_native,t5_share_kv=args.t5_share_kv,legacy_bf16_buffers=args.legacy_bf16_buffers);checks(sc,report/'trained_checks')
  for split in ['validation','calibration','test']:evaluate.run(sc,['data/hf.jsonl','data/eval.jsonl'],[split],out_dir=report/split)
  bench(sc,report)
 elif args.stage=='eval':
  for split in ['validation','calibration','test']:evaluate.run(sc,['data/hf.jsonl','data/eval.jsonl'],[split],out_dir=report/('native_'+split if args.gli_native else split))
 elif args.stage=='bench':bench(sc,report)
 print('COMPLETE',args.name,args.stage,flush=True)
