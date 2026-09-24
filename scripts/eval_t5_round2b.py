"""Same-host quality and cold-prefix latency, with shared request JSON across backends."""
import argparse,json,random,time,statistics,subprocess
from pathlib import Path
import torch
from personal_jev import evaluate,benchmark
from personal_jev.classify import classify
from personal_jev.data import sha256_file
from personal_jev.schemas import parse_request
from run_challenger import save
ROOT=Path('reports/t5_round2b_2026-09-24')


def make_corpus():
    from transformers import AutoTokenizer
    from personal_jev.tree import RERANKER_4B
    tok=AutoTokenizer.from_pretrained(*RERANKER_4B[:1],revision=RERANKER_4B[1])
    rng=random.Random(9851);corpus=[]
    for n,q in [(512,1),(512,16),(2048,1),(2048,4),(2048,16),(8192,1),(8192,16)]:
        for rep in range(100 if (n,q)==(2048,16) else 20):
            budget=rng.randint(50,150);claim=budget+rng.choice([-10,-1,1,10]);verified=bool(rng.getrandbits(1))
            facts=f'\nCurrent decision record {rng.getrandbits(64)}: Person Iris has identity verified: {str(verified).lower()}. Expense is {claim} dollars. Approval requires verified identity AND an expense at most {budget} dollars.\n'
            filler=benchmark.make_state(tok,max(1,n-len(tok(facts,add_special_tokens=False)['input_ids'])))
            state=filler+facts
            qs=[]
            for i in range(q):
                qs.append({'id':f'q{i}','type':'multiclass',
                    'instruction':f'For check {i+1}, decide whether the current Iris expense satisfies the stated approval rule.',
                    'candidates':[{'id':'approve','description':'Approve: all required conditions are satisfied.'},
                                  {'id':'reject','description':'Reject: at least one required condition is not satisfied.'},
                                  {'id':'unknown','description':'Cannot determine from the supplied record.'}]})
            corpus.append({'bucket':f'{n}_{q}','nominal_qwen_state_tokens':n,'questions':q,'rep':rep,
                'target':'approve' if verified and claim<=budget else 'reject','request':{'state':state,'questions':qs}})
    ROOT.mkdir(exist_ok=True,parents=True);save(ROOT/'latency_requests.json',corpus)
    return corpus


def gpu_state():
    return subprocess.check_output(['nvidia-smi','--query-gpu=name,driver_version,pstate,temperature.gpu,power.draw,clocks.current.sm,clocks.current.memory,memory.used','--format=csv,noheader'],text=True).strip()


def bench(sc,out):
    path=ROOT/'latency_requests.json';corpus=json.loads(path.read_text());buckets={}
    for r in corpus:buckets.setdefault(r['bucket'],[]).append(r)
    result={'model':sc.meta,'gpu':torch.cuda.get_device_name(),'request_sha256':sha256_file(path),
            'gpu_before':gpu_state(), 'timing':'resident model, cold document prefix, same request bytes; excludes model loading and network', 'rows':[]}
    for key, requests in buckets.items():
        for _ in range(2):classify(sc,requests[0]['request'])
        samples=[];counts=[];latency_correct=0
        torch.cuda.synchronize();torch.cuda.reset_peak_memory_stats()
        for r in requests:
            if hasattr(sc,'llm'):
                sc.llm.reset_prefix_cache()
            torch.cuda.synchronize();start=time.perf_counter();res=classify(sc,r['request']);torch.cuda.synchronize()
            samples.append((time.perf_counter()-start)*1000)
            latency_correct+=sum(x['selected']==r['target'] for x in res['questions'])
            counts.append({k:v for k,v in res['meta'].items() if k in ['input_tokens','cached_tokens','cross_projection_pairs','encoder_calls','decoder_batches','cross_kv_storage_bytes']})
        row={'bucket':key,'gpu_after':gpu_state(),'n':len(samples),'p50_ms':statistics.median(samples),'p95_ms':benchmark._pct(samples,.95),
             'raw_ms':samples,'counts':counts,'peak_allocated_mb':torch.cuda.max_memory_allocated()/2**20,
             'state_tokens_actual':[len(sc.tokenizer(r['request']['state'],add_special_tokens=False)['input_ids']) for r in requests],
             'synthetic_correct_decisions':latency_correct,'synthetic_decisions':sum(r['questions'] for r in requests)}
        result['rows'].append(row);save(out/'bench.json',result);print('BENCH',key,row['p50_ms'],row['p95_ms'],flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('backend',choices=['corpus','t5_r1','t5_r2b','t5_r2b_merged','tree_r2b','tree_r2b_merged','tree_r2b_vllm','tree_r2b_vllm_fp8','t5_r2b_merged_b48','t5_r2b_merged_prefix48'])
    ap.add_argument('--bench-only',action='store_true');ap.add_argument('--quality-only',action='store_true');ap.add_argument('--output-root',default=str(ROOT));args=ap.parse_args()
    if args.backend=='corpus':make_corpus();return
    out=Path(args.output_root)/args.backend;out.mkdir(exist_ok=True,parents=True)
    if args.backend.startswith('t5'):
        from personal_jev.t5_shared import T5SharedScorer
        run='runs/t5gemma2_r1_reference' if args.backend=='t5_r1' else 'runs/t5gemma2_r2b_full'
        sc=T5SharedScorer(adapter=run+'/adapter',merge='_merged' in args.backend,branch_batch=48 if args.backend.endswith('48') else 16,decoder_prefix='prefix' in args.backend)
    elif '_vllm' in args.backend:
        from personal_jev.vllm_tree import VllmTreeScorer
        sc=VllmTreeScorer('runs/tree_4b_r2b/merged',max_length=32768,quantization='fp8' if args.backend.endswith('_fp8') else None)
    else:
        from personal_jev.tree import TreeScorer
        sc=TreeScorer(adapter='runs/tree_4b_r2b/adapter',device='cuda',dtype='bfloat16',merge=args.backend.endswith('_merged'))
    sc.meta['gpu']=torch.cuda.get_device_name()
    if not args.bench_only:
        for label,files in [('test',['data/hf.jsonl','data/eval.jsonl']),('eval2',['data/eval2.jsonl'])]:
            result=evaluate.run(sc,files,['test'],out_dir=out/label)
            print('QUALITY',args.backend,label,result['metrics'].get('question_accuracy'),flush=True)
    if not args.quality_only:bench(sc,out)
    save(out/'complete.json',{'backend':args.backend,'adapter_sha256':sc.meta.get('adapter_sha256')})

if __name__=='__main__':main()
