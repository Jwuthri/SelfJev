"""Static report figure from measured timings; requires matplotlib (not an inference dependency)."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

P=Path('reports/latency_optimization_2026-09-24')
series=[('R1 · Transformers','hf_optimized_a10g.json','median_ms','#64748b'),
        ('Compact · Transformers','hf_compact_a10g.json','median_ms','#b45309'),
        ('R1 · vLLM','vllm_extended_a10g.json','cold_prefix_median_ms','#2563eb'),
        ('Compact · vLLM','vllm_compact_a10g.json','cold_prefix_median_ms','#059669')]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.fonttype':'none'})
fig,ax=plt.subplots(figsize=(10.5,6.5),dpi=160)
fig.patch.set_facecolor('#ffffff');ax.set_facecolor('#ffffff')
for label,file,key,color in series:
    rows=[r for r in json.loads((P/file).read_text())['rows'] if r['state_tokens']==2048]
    rows=sorted(rows,key=lambda r:r['questions'])
    x=[r['questions'] for r in rows];y=[r[key] for r in rows]
    ax.plot(x,y,label=label,color=color,marker='o',markersize=6,linewidth=2.5)
    ax.annotate(f'{y[-1]:.0f} ms',(x[-1],y[-1]),xytext=(9,0),textcoords='offset points',
                color=color,va='center',fontsize=12,weight='bold')
ax.set_xlim(.3,18.8);ax.set_ylim(0,1080);ax.set_xticks([1,4,16])
ax.set_xlabel('Questions per request · 3 candidate answers each',labelpad=12)
ax.set_ylabel('Request latency (ms)',labelpad=10)
ax.grid(axis='y',color='#e2e8f0');ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)
ax.spines[['left','bottom']].set_color('#cbd5e1')
ax.legend(loc='upper left',frameon=False,fontsize=11)
fig.suptitle('Sharing the document does not make extra questions free',x=.095,y=.97,ha='left',fontsize=17,weight='bold')
fig.text(.095,.91,'2,048 document tokens · AWS A10G · resident model · new document / cold prefix',fontsize=11,color='#475569')
fig.text(.095,.025,'Median of 10 timed repetitions after warmup. Model loading, compilation and network time excluded.',fontsize=9,color='#64748b')
fig.subplots_adjust(left=.095,right=.98,bottom=.15,top=.85)
fig.savefig(P/'latency_vs_questions.png',dpi=160)
fig.savefig(P/'latency_vs_questions.svg')
