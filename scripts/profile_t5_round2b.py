"""Post-training stage timing and long-context storage diagnostic, not a quality test."""
import json,time,statistics
import torch
from pathlib import Path
from personal_jev.t5_shared import T5SharedScorer
from personal_jev.classify import classify
from personal_jev import benchmark
from run_challenger import save
ROOT=Path('reports/t5_round2b_2026-09-24')
sc=T5SharedScorer(adapter='runs/t5gemma2_r2b_full/adapter',merge=True,branch_batch=48,max_length=65536)
base=sc.base().model
records={'encoder':[],'decoder':[]};originals={}
for name in records:
    module=getattr(base,name);originals[name]=module.forward
    def wrapped(*a,_name=name,**kw):
        start=torch.cuda.Event(enable_timing=True);end=torch.cuda.Event(enable_timing=True)
        start.record();out=originals[_name](*a,**kw);end.record();records[_name].append((start,end));return out
    module.forward=wrapped
corpus=json.loads((ROOT/'latency_requests.json').read_text())
req=next(x['request'] for x in corpus if x['bucket']=='2048_16')
result={'adapter_sha256':sc.meta['adapter_sha256'],'gpu':torch.cuda.get_device_name(),
        'timing_note':'Diagnostic CUDA stream elapsed intervals; includes dispatch gaps, not pure kernel compute. Full uninstrumented benchmark determines acceptance.',
        'profile':[],'long_context':[]}
for branches,prefix_mode in [(16,False),(48,False),(48,True)]:
    sc.branch_batch=branches;sc.decoder_prefix=prefix_mode
    for _ in range(2):classify(sc,req)
    samples=[]
    for _ in range(8):
        records={k:[] for k in records};torch.cuda.synchronize();start=time.perf_counter()
        out=classify(sc,req);torch.cuda.synchronize();wall=1000*(time.perf_counter()-start)
        stages={k:sum(a.elapsed_time(b) for a,b in v) for k,v in records.items()}
        samples.append({'wall_ms':wall,**{k+'_ms':v for k,v in stages.items()},'counts':sc.last_counts})
    result['profile'].append({'branch_batch':branches,'decoder_prefix':prefix_mode,'samples':samples})
    save(ROOT/'profile.json',result)
# Encoder and decoder have separate positional limits. Keep each within the
# pinned config base max_position_embeddings of 32768; only lift this prototype's combined API budget.
sc.branch_batch=16;sc.decoder_prefix=False
for state_tokens in [16384,32760]:
    req=benchmark.make_request(sc.tokenizer,state_tokens,16,3,'multiclass')
    # This diagnostic stays below both configured base position counts.
    from personal_jev.schemas import parse_request
    parsed=parse_request(req);entries=[sc.entry(parsed.state,q) for q in parsed.questions]
    enc_len=len(entries[0]['root']);dec_len=max(len(b) for e in entries for b in e['branches'])
    assert enc_len<=32768 and dec_len<=32768,(enc_len,dec_len)
    torch.cuda.empty_cache();torch.cuda.reset_peak_memory_stats();torch.cuda.synchronize();start=time.perf_counter()
    row={'requested_state_tokens':state_tokens,'encoder_tokens':enc_len,'max_decoder_tokens':dec_len,
         'branch_batch':16,'questions':16,'candidates_per_question':3}
    try:
        out=classify(sc,req);torch.cuda.synchronize()
        row.update(status='ok',wall_ms=1000*(time.perf_counter()-start),
            peak_allocated_mb=torch.cuda.max_memory_allocated()/2**20,counts=sc.last_counts,
            finite_scores=all(torch.isfinite(torch.tensor(c['score'])) for q in out['questions'] for c in q['candidates']))
        row['finite_scores']=bool(row['finite_scores'])
    except torch.cuda.OutOfMemoryError:
        row.update(status='oom',peak_allocated_mb=torch.cuda.max_memory_allocated()/2**20)
        torch.cuda.empty_cache()
    result['long_context'].append(row);save(ROOT/'profile.json',result);print('LONG_CONTEXT',row,flush=True)
