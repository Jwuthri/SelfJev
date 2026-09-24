"""Compare identical serving backends/requests across saved L40S and H100 runs."""
import json
from pathlib import Path
from compare_compact_quality import compare
from summarize_t5_round2b import ratio
ROOT=Path('reports/t5_round2b_2026-09-24')

def main():
    out={'note':'Same model, serving code and requests across EC2 host/GPU configurations. This is a host/hardware comparison, not an isolated GPU-chip experiment.','backends':{}}
    lines=['# Hardware follow-up','',out['note'],'','| Backend | L40S eval2 | H100 eval2 | L40S 2K × 16 × 3 p50 | H100 p50 | H100 p95 | Speedup |','|---|---:|---:|---:|---:|---:|---:|']
    for p in sorted((ROOT/'h100').glob('*/bench.json')):
        name=p.parent.name
        a=json.loads((ROOT/name/'bench.json').read_text());b=json.loads(p.read_text())
        assert a['request_sha256']==b['request_sha256']
        qa=json.loads((ROOT/name/'eval2/report.json').read_text());qb=json.loads((p.parent/'eval2/report.json').read_text())
        assert qa['meta']['adapter_sha256']==qb['meta']['adapter_sha256']
        row={'l40s_gpu':a['gpu'],'h100_gpu':b['gpu'],'quality':compare(qa['predictions'],qb['predictions']),'latency':{}}
        for x in a['rows']:
            y=next(y for y in b['rows'] if y['bucket']==x['bucket'])
            row['latency'][x['bucket']]={'l40s_p50_ms':x['p50_ms'],'h100_p50_ms':y['p50_ms'],'l40s_p95_ms':x['p95_ms'],'h100_p95_ms':y['p95_ms'],**ratio(x['raw_ms'],y['raw_ms'])}
        out['backends'][name]=row
        main=row['latency']['2048_16'];q=row['quality']
        lines.append(f"| {name} | {100*q['reference_accuracy']:.2f}% | {100*q['candidate_accuracy']:.2f}% | {main['l40s_p50_ms']:.1f} ms | {main['h100_p50_ms']:.1f} ms | {main['h100_p95_ms']:.1f} ms | {main['median_speedup']:.2f}× |")
    if not out['backends']:raise ValueError('No completed H100 benchmarks')
    lines+=['','Times are local resident-model requests, excluding model loading and network. The primary cell uses 100 requests with cold document prefixes. Full predictions, timing samples and paired confidence intervals are retained.']
    (ROOT/'hardware_comparison.json').write_text(json.dumps(out,indent=2));(ROOT/'hardware.md').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
if __name__=='__main__':main()
