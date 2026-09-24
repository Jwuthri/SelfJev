"""SelfJev design memo. Recommendations are hypotheses, not new training results."""
import html, json, re, hashlib, subprocess
import os
from pathlib import Path
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
PDF=OUT/'selfjev-quality-speed-strategy.pdf'
INK='#18302F'; TEAL='#11776F'; MUTED='#61716F'; PALE='#EFF6F3'; LINE='#D4E2DC'
pages=[]
def page(k,t,d):
 p={'kicker':k,'title':t,'deck':d,'blocks':[]};pages.append(p);return p
def text(p,s):p['blocks'].append(('p',s))
def h(p,s):p['blocks'].append(('h',s))
def note(p,s):p['blocks'].append(('note',s))
def table(p,hs,rs,ws):p['blocks'].append(('table',(hs,rs,ws)))
def local(path,label):return f'[{label}]({os.path.relpath(ROOT/path, OUT)})'

p=page('DESIGN MEMO / 23 SEPTEMBER 2026','A credible path toward Jev quality and speed','Recommendation: preserve pretrained judgment, share document computation, and train on evidence decisions. Treat the backbone and serving method as separate choices.')
text(p,'<b>I would stop making the current two-block cross-attention model the main investment.</b> It demonstrates that sharing the state can save a great deal of computation, but its trained similarity path largely carries multiclass performance while binary discrimination remains weak. That is sufficient reason to choose a better starting point. It is not proof that cross-attention is intrinsically unsuitable.')
text(p,'My primary bet is a capable pretrained model reading one shared document prefix, with short, independent decision branches processed together. Keep its pretrained layers and output readout. Establish quality at roughly the current 4B scale, then challenge it with smaller, more efficient backbones. In parallel as a research plan, screen an existing classification model; pursue a pretrained encoder-decoder if the first approach sacrifices too much judgment quality.')
table(p,['Priority','What to build or test','Why it deserves the investment'],[
 ['1 / Main path','Shared document prefix + pretrained decision branches','Removes repeated document processing while retaining a trained mechanism for reading evidence.'],
 ['2 / Cheap challenger','GLiClass-Instruct, using its native prompted classification interface','Tests whether an existing compact classification model can replace much of this project.'],
 ['3 / Structural alternative','T5Gemma 2 shared encoder + pretrained decoder branches','Preserves already-trained document-to-decision interaction with a genuinely separate encoder.'],
 ['4 / After quality','Smaller backbone, distillation and optimized execution','Makes a demonstrated decision model cheaper; avoids shrinking an already weak model.']],[75,202,218])
text(p,'The target is a measured quality/latency tradeoff, not a particular architecture or a proof that Jev was easy to build. Your results show useful functionality is accessible with standard methods. Matching its behavior on unfamiliar criteria, calibrated uncertainty and cold-request speed together is still an open engineering problem.')
note(p,'Planning assumption: a single NVIDIA GPU for a service comparable to Jev, with the M5 Pro assessed separately. No new training, paid calls, deployments or model downloads were performed for this memo. Current external information was checked on 23 September 2026. Proposed targets and experiment sizes are planning choices, not forecasts.')

p=page('01 / WHAT THE EVIDENCE CHANGES','The remaining gap is judgment','A larger reranker gives little aggregate improvement. A different starting objective already changes binary behavior substantially.')
table(p,['Model / saved test run','Overall','Binary AUROC','Authored cases'],[
 ['4B reranker, unmodified','62.8%','0.604','-'],
 ['4B Instruct, unmodified (new)','71.3%','0.911','-'],
 ['4B reranker + LoRA','80.3%','0.945','70.8%'],
 ['8B reranker + LoRA','80.7%','0.945','74.9%'],
 ['Jev, cached API results','82.7%','0.981','94.7%']],[216,73,103,103])
text(p,'All overall columns use the same 3,471 questions. The authored slice contains only 171 questions, so the exact percentages are uncertain. Nevertheless, the 24-point authored gap for 4B is more relevant to arbitrary rules and agent-output evaluation than the 2.4-point overall gap. The current mixture gives considerable weight to short topic/intent classification.')
text(p,'The newly completed instruction-model test strengthens the case for changing the pretrained objective: binary accuracy is 84.2% without adaptation. However, its multiclass accuracy is 73.5% and multilabel exact match 20.1%, both below the trained reranker. It is a candidate for fine-tuning, not an established replacement. This run also uses the reranker-style wrapper; a native instruction template needs a validation-only comparison.')
h(p,'Why the custom model is a weak foundation today')
text(p,'Separating state and question through every Qwen layer prevents the pretrained model from performing their interaction. The system then asks two new, narrower blocks and new heads to learn that interaction from relatively limited supervision. Its strongest model also has a direct similarity bypass. In the review ablation, removing the head contribution changes validation multiclass accuracy from 82.3% to 82.1%; heads alone give 30.5%. This is post-training removal, not a separately trained control.')
text(p,'Binary test AUROC near 0.514 is the decisive warning: the ordering of examples is weak, not merely the threshold. Calibration can improve multilabel decisions, but a monotone score transform cannot repair a near-random ranking. I would allocate more compute to a better pretrained interaction before adding more blocks to this one.')
note(p,'Sources: '+local('reports/curve/instruct_zero/test/report.json','new instruction-model test')+', '+local('reports/lora_4b/test/report.json','4B LoRA test')+', '+local('reports/deep_review_2026-09-23/audit.json','review audit')+' and '+local('reports/deep_review_2026-09-23/component_ablation.json','component ablation')+'. The earlier test has already informed architecture choices; use it as a development benchmark, then create a fresh final holdout.')

p=page('02 / PRIMARY ARCHITECTURE','Let a pretrained model read the shared state','A state-first decoder can reuse its document computation while each decision still reads document information through its pretrained layers.')
p['blocks'].append(('diagram','prefix'))
text(p,'Encode the document once and retain its per-layer keys and values. Append a question branch, then candidate-specific suffixes where needed. Batch these short branches, preserving their own positions and causal history. Read the final yes/no logits directly. Binary and multilabel use independent support scores; multiclass normalizes candidate scores within its question. Nothing requires generating JSON or explanatory text.')
text(p,'For multiclass, include the candidate bank in the shared question branch when the criterion is comparative or includes none of the above. Otherwise a candidate scorer cannot reliably know what the alternatives are. Keep different questions isolated. Within a question, alternative descriptions may be visible; answers from other questions should not become hidden evidence.')
h(p,'The important architectural choice is where interaction happens')
text(p,'The document does not see future questions, but the question and answer suffixes can read document K/V through every pretrained layer. This retains much more trained interaction than independently encoding both sides and adding two new blocks at the end. The tree prototype already implements this general direction. It still needs a quality result; the existence of a cache is not evidence of retained accuracy.')
h(p,'The control that determines whether to continue')
text(p,'Compare the original query-first scorer with a standalone state-first scorer on the same model and data. Then compare standalone state-first with shared-prefix execution. The latter pair should agree numerically; the former pair measures the quality cost of changing information flow. Fine-tune in the exact state-first format before rejecting it solely on zero-shot degradation.')
text(p,'For this architecture, prefer ordinary supported attention and verified branch cache semantics first. An arbitrary dense tree mask may disable fast kernels. Do not assume a generic inference server already exposes the required branch scores. A correct CUDA implementation must reuse root K/V, batch suffix work and avoid copying the entire prefix per candidate.')
note(p,'FlashInfer documents shared-prefix and multilevel cascade attention, providing a relevant execution building block, not a turnkey SelfJev implementation. Its shared/unique attention pieces require correct normalization when combined. See [Cascade Attention](https://flashinfer.ai/2024/02/02/cascade-inference.html) and [current API documentation](https://docs.flashinfer.ai/api/cascade.html).')

p=page('03 / REPLACE THE BACKBONE WHEN IT HELPS','Three challengers with different strengths','Model-card capabilities identify experiments worth running. They do not establish accuracy or latency on SelfJev.')
h(p,'An existing classification model: GLiClass-Instruct')
text(p,'Screen [gliclass-instruct-large-v1.0](https://huggingface.co/knowledgator/gliclass-instruct-large-v1.0). It is about 0.4B parameters and exposes task prompts, label descriptions and multilabel classification. Its [architecture paper](https://arxiv.org/abs/2508.07662) describes jointly processing text and label representations. Start with native one-question inference; validate any multi-question adaptation separately. This could be a useful replacement for short classification workloads. Its standard context budget is a material limitation for 8K-32K documents, and classification benchmarks do not establish robust arbitrary-rule reasoning. Do not silently chunk or truncate to hide that limitation.')
h(p,'A different structure: pretrained encoder-decoder')
text(p,'[T5Gemma 2 1B-1B](https://huggingface.co/google/t5gemma-2-1b-1b) provides pretrained encoder-decoder interaction, merged decoder self/cross-attention and a stated 128K input context. Proposed adaptation: document in the encoder; question/candidate prefixes in independent decoder branches; direct score readout after the known prefix. Share encoder outputs and reusable decoder-side projections. This moves the evidence-reading job into pretrained machinery. The released checkpoint is pretrained, so task adaptation is required, and moving questions to the decoder is itself a distribution change. Long-context support is not a claim of reliable reasoning throughout that window.')
h(p,'A more efficient decoder backbone')
text(p,'Screen [Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B) for a smaller model with predominantly Gated DeltaNet layers and periodic full attention. Also consider [Gemma 4 E2B-it](https://huggingface.co/google/gemma-4-E2B-it), which combines sliding-window and global attention. E2B means about 2.3B effective parameters, but 5.1B including embeddings; it is not a 2B-memory model. Measure direct decisions with thinking disabled. Generative reasoning scores cannot predict one-forward-pass accuracy.')
text(p,'These are different engineering paths. Qwen3.5 branches require cloning recurrent/convolution state as well as attention K/V; a softmax tree mask alone is insufficient. Gemma branches must preserve local/global attention and its embedding behavior. Both may reduce long-document cost, but neither is a drop-in change to the Qwen3 tree implementation.')
note(p,'Selection order: keep Qwen3-4B-Instruct-2507 and the trained 4B reranker as controls; run a small matched diagnostic for GLiClass and one modern small decoder; promote only a promising challenger to a full pilot. T5Gemma is the structural fallback, not a fourth expensive training run to launch immediately. GLiNER2 is relevant if extraction becomes central; it is not needed for the current decision-only goal.')

p=page('04 / TRAINING THAT TARGETS THE GAP','Teach evidence relationships, not more topic matching','The highest-value data change is controlled variation: almost the same words, but a different correct decision.')
table(p,['Training group','What changes while most text stays the same'],[
 ['Support / contradiction / absent','Requested a refund; explicitly rejected a refund; discussed a refund without requesting one.'],
 ['Role and time','Who approved what; before versus after the deadline; current versus superseded status.'],
 ['Rules and exceptions','Same facts with a changed policy; same policy with one disqualifying exception.'],
 ['Multiple evidence items','Two distant facts must both hold; remove either fact and the answer changes.'],
 ['Candidate semantics','Rename IDs, paraphrase descriptions, permute options; include genuinely confusable alternatives.'],
 ['Document robustness','Move evidence, add irrelevant text, quote hostile instructions, change the number of other questions.']],[127,368])
text(p,'Generate underlying facts and rules with a small executable world first, derive answers programmatically, then render varied natural-language documents. Check that the rendering preserves those facts. Keep all variants of a source, rule template and paraphrase family together when splitting. Combine this with realistic, independently adjudicated examples; a synthetic grammar alone can teach another shortcut.')
text(p,'Use a stronger teacher for difficult interpretation, with audited answers and training-only evidence spans or brief explanations. The earlier custom distillation mostly added confident multiclass hard labels from the 0.6B teacher. That neither transfers a strong general reasoner nor directly repairs binary evidence learning. More providers broaden style but do not automatically improve label validity.')
h(p,'Use richer supervision without requiring longer inference')
text(p,'Keep cross entropy for multiclass and BCE for binary/multilabel as the core objectives. Add a separate auxiliary support/contradiction/not-stated task where the criterion is evidence-grounded. Map it to the public answer according to the task contract; missing evidence is not universally equivalent to false. Add checked evidence/rationale supervision as a training ablation, not mandatory inference text. [Distilling Step-by-Step](https://arxiv.org/abs/2305.02301) demonstrates a multitask rationale approach that predicts labels without generating rationales at test time; it does not guarantee compression of arbitrary long reasoning.')
text(p,'Compare hard-label supervision with and without teacher-distribution distillation, using verified labels as the anchor. Teacher confidence is not automatically calibrated. Balance loss and sampling by question and task family, track positive/negative gradients, and retain ordinary examples to avoid becoming a hard-case specialist. Test broader LoRA targets, including MLP projections, only after a matched pilot shows the data change alone is insufficient.')
note(p,'Proposed learning curve: 10K, 30K, then 100K questions only if held-out-template quality keeps improving. These are experiment sizes, not estimates of the data required to match Jev. Use question groups per shared state during training so the inference layout is represented.')

p=page('05 / LATENCY ENGINEERING','Remove duplicated work before shrinking quality','There are three different costs: encoding a new document, reading it for each decision, and executing the model efficiently on the target hardware.')
text(p,'Let S be document tokens, K candidate decisions, and b tokens in each short branch. Repeated full scoring processes roughly K(S+b) token positions through the backbone; a shared-prefix design processes S+Kb. With S=8,192, K=48 and b=64, that is 396,288 versus 11,264 positions, a <b>35.2x reduction in repeated token processing</b>. This is a simplified accounting example, not a 35.2x latency prediction: attention shapes, memory traffic and utilization differ.')
table(p,['Measured A10G / bf16 case','Stock 0.6B LoRA','Custom shared state'],[
 ['512 tokens / 1 question x 3 candidates','96 ms','95 ms'],
 ['2,048 tokens / 16 x 3','5,138 ms','227 ms'],
 ['8,192 tokens / 16 x 3','24,024 ms','626 ms'],
 ['32K tokens / 1 binary question','3,362 ms','3,428 ms']],[257,119,119])
text(p,'Your own measurements support the mechanism: sharing helps most when the document is reused many times. The custom model is much weaker, so these are not speedups at equal quality. A first request with one binary question cannot benefit from eliminating 48 repeated encodings that never existed.')
h(p,'Implementation changes with a clear purpose')
text(p,'Use a contiguous fused prefill for the root and batched short-branch execution. Cache per-layer K/V once, and reuse it without materializing one full copy per candidate. Remove the existing cached-tree T-by-T mask allocation; create only the required branch visibility or use an appropriate structured kernel. Merge LoRA for inference where supported and verified. Compute only the required output rows at score positions. Profile tokenization, root prefill, branch work and result assembly separately.')
text(p,'After the architecture passes quality gates, evaluate compilation/fused kernels and quantization on the exact hardware and shapes. Four-bit weights may save memory without making long-prefill computation faster. Flash attention addresses attention execution; it does not remove feed-forward work. Quantized calibration and close decision margins need their own check.')
text(p,'For repeated agent state, preserve an exact append-only prefix across calls and process only new tokens. Report this warm-prefix benefit separately from a new document. Inserting an earlier message or changing a policy can invalidate the cache; do not substitute semantic similarity for an exact cache key.')
note(p,'TypeSafe reports 70-500 ms end-to-end in its [launch article](https://typesafe.ai/blog/introducing-system-one-models-and-jev), with workload and location qualifications. It is not a universal 100 ms specification for cold 32K input. SelfJev has no matched Jev latency study yet. Do not compare an M5 Pro PyTorch run with unspecified hosted hardware as if architecture were the only difference.')

p=page('06 / CONTROLLED EXPERIMENTS','The smallest sequence that can choose a winner','Each stage resolves one uncertainty. Advance a model because it passes a gate, not because its architecture sounds plausible.')
table(p,['Stage','Experiment','Decision it enables'],[
 ['A / Fixed evidence','New source/template splits; 400-600 diagnostic questions balanced across evidence, rules, agent checks, ordinary tasks and lengths. Reserve a separate final test.','A cheap screen can reject weak ideas; it is too small to prove a 1-2 point win.'],
 ['B / Starting model','Same diagnostic and validation protocol: current 4B LoRA; 4B Instruct; native GLiClass; one modern small decoder. No generated rationale at inference.','Choose the best starting representation for the difficult families.'],
 ['C / Information flow','On the chosen decoder: query-first; state-first standalone; state-first cached. Include candidate permutations and unrelated questions.','Separate order/format damage from an implementation bug in sharing.'],
 ['D / Matched training','Train query-first and state-first on the same verified data/exposure. Compare old versus improved data on a fixed format. Add a second seed for finalists.','Distinguish data improvement from architecture improvement.'],
 ['E / Efficient student','Only after a quality winner: smaller model with hard labels, then hard labels + richer distillation. Assess the same families.','Find the smallest model that retains the capability we actually need.'],
 ['F / Deployment','Same checkpoints and prompts; end-to-end p50/p95, concurrency, memory and cost on a named GPU; fresh final test once.','Determine whether quality and speed coexist in one real configuration.']],[68,249,178])
text(p,'For C/D, set an initial engineering tolerance of no more than roughly 2 points below the same-data query-first model overall and 5 points on the hard-family diagnostic. These are screening thresholds, not statistical equivalence claims. Predefine margins and collect enough independent document groups before claiming a match. Do not let easy classification gains conceal a regression in evidence or policy decisions.')
text(p,'For service timing, use 512, 2K and 8K states; 1, 4 and 16 questions; several candidate counts; and actual evidence-bearing 16K/32K cases as a separate extension. Record warm model plus new prefix, warm prefix, and cold process startup separately. Use at least 100 varied requests per key cell for an initial p95 estimate, then more if tails are unstable. Measure Jev from the same client and question batches, with cache state stated as unknown when it cannot be controlled.')
text(p,'Success should mean a predeclared accuracy margin against Jev on a fresh, relevant mix, acceptable binary/multilabel calibration, and latency inside the desired band for specified workloads. Treat 100 ms as a stretch goal for short requests; first test a 500 ms target for 512-2K states with many questions on a named GPU. Neither number here is a prediction.')
note(p,'The current instruction-model test is now complete. No tree-training or instruction-LoRA train_meta.json was present when this memo snapshot was taken. Reuse results from those ongoing experiments as they arrive; do not launch duplicate runs or interpret a missing result as failure.')

p=page('07 / WHAT TO DO IF THE FIRST BET FAILS','Have an architectural fallback, not an endless tuning loop','A controlled failure tells us what to change. It should not automatically trigger a larger dataset or another expensive backbone.')
table(p,['Observed outcome','Next action'],[
 ['State-first loses badly; query-first succeeds on identical data','Test pretrained encoder-decoder interaction, or share only lower layers and keep a few upper layers jointly processing document and question.'],
 ['Both formats fail to fit even a tiny verified training set','Check labels, masks, score positions, gradients and optimization. Permit broader adaptation in this diagnostic before blaming generalization.'],
 ['Both fit; only familiar templates work','Improve source/template diversity, counterfactual training and independent labels. More repetitions of one synthetic style are unlikely to solve this.'],
 ['Quality passes; many-question latency fails','Profile prefix copies, dense masks, branch batching and kernel dispatch. Do not reduce model capacity before locating the wasted work.'],
 ['Quality passes; cold long-document latency fails','Test a more efficient backbone or explicit evidence selection. State the resulting limits and evaluate distributed evidence.'],
 ['Only multilabel thresholds fail','Calibrate on a disjoint representative partition and inspect ranking first; do not retrain an architecture solely to fix an offset.']],[224,271])
h(p,'Partial sharing can trade some speed for better interaction')
text(p,'[PreTTR](https://arxiv.org/abs/2004.14255) trains separate processing in lower transformer layers, then allows joint interaction in upper layers. This suggests a fallback using pretrained upper layers rather than a new two-block reader. Its evidence is from retrieval with precomputed documents, not this online classification task. For a simplified 28-layer model sharing 24 layers across 48 decisions, state-token layer work drops from 48x28 to 24+48x4: about 6.2x. Actual speed must include attention and online state encoding. Adapting the idea to causal Qwen requires consistent positions and matching training masks.')
h(p,'Two shortcuts I would keep out of the first claim')
text(p,'A small-model/large-model cascade can reduce average cost, but may miss the latency target. With independent 2% per-question deferral and 16 questions, 27.6% of requests invoke the slow path: 1 - 0.98^16. A fast average or median is not a fast p95. Measure routing by complete request and do not trust uncalibrated self-confidence.')
text(p,'Retrieving a few chunks or compressing the state can help local-evidence tasks, but may discard an exception, a distant second fact, or evidence of absence. If used, train and test evidence recall as well as final accuracy, preserve a full-document fallback, and disclose its cost. Deterministic tools for dates or arithmetic are useful in a product, but constitute a different system comparison.')
note(p,'I would defer speculative latent reasoning blocks and a homemade RLCD objective. Supervised decision losses, strong supervision and representation preservation have not been exhausted. Jev\'s undisclosed training label does not establish that a new RL algorithm is necessary here.')

p=page('08 / COMMITMENT AND EVIDENCE','What I would commit to next','One main architecture, one inexpensive external baseline, and a clear point at which to switch approaches.')
text(p,'<b>Main implementation:</b> complete the shared-prefix experiment with a pretrained 4B model, correct branch batching and no quadratic root mask. Run the existing instruction-model adaptation as a controlled competitor to reranker adaptation. Use new evidence/rule data with trustworthy labels. Optimize a winner only after its difficult-family performance is established.')
text(p,'<b>First challenge:</b> native GLiClass-Instruct on short, difficult criteria. If it performs well, it may supply an efficient short-input product or student; if it only handles topic/intent, that is a useful boundary. Screen a newer small instruction model before committing to 0.6B as the required endpoint.')
text(p,'<b>Architectural switch:</b> if state-first adaptation cannot retain quality, move to pretrained encoder-decoder interaction, with partial lower-layer sharing as the less radical fallback. This directly tests whether the missing ingredient is query-conditioned document processing or trained interaction across inputs.')
text(p,'<b>Training strategy:</b> teach the decisions with verifiable counterfactual groups, realistic independent examples and a strong teacher. Distill evidence and reasoning only as checked auxiliary targets. Increase dataset size on a held-out-template learning curve. Measure calibration after learning discrimination, then after quantization.')
text(p,'The project can plausibly get much closer with these changes. The strongest evidence for that is already local: supervised adaptation produces large gains, the newer instruction base is much better at binary judgments before training, and sharing eliminates a substantial amount of repeated work. None of those results yet establishes the combination. The next experiments should be designed to establish exactly that.')
h(p,'Evidence files and provenance')
text(p,local('reports/deep_review_2026-09-23/review.md','Full project review')+' records architecture details, 78 passing tests, saved metrics, data limitations and the new component ablation. '+local('reports/curve/instruct_zero/test/report.json','Latest instruction-model test')+' is the main additional local result in this memo. '+local('reports/strategy_2026-09-23/snapshot.json','Memo snapshot')+' records hashes of the source reports and the repository revision.')
note(p,'External links throughout this memo are primary model cards, original research or implementer documentation. Public benchmark figures are deliberately not converted into SelfJev predictions. Model choices, training schedules, architectural transfers and screening thresholds are recommendations to test. The published Jev architecture, model size and training details remain undisclosed.')

pdfmetrics.registerFont(TTFont('Memo','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('MemoBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('Memo',normal='Memo',bold='MemoBold',italic='Memo',boldItalic='MemoBold')
styles={
 'kicker':ParagraphStyle('k',fontName='MemoBold',fontSize=8.4,leading=12,textColor=colors.HexColor(TEAL),spaceAfter=8),
 'title':ParagraphStyle('t',fontName='MemoBold',fontSize=25,leading=28,textColor=colors.HexColor(INK),spaceAfter=10),
 'deck':ParagraphStyle('d',fontName='Memo',fontSize=11,leading=15,textColor=colors.HexColor(MUTED),spaceAfter=15),
 'p':ParagraphStyle('p',fontName='Memo',fontSize=10.2,leading=14.2,textColor=colors.HexColor(INK),spaceAfter=9),
 'h':ParagraphStyle('h',fontName='MemoBold',fontSize=11.5,leading=15,textColor=colors.HexColor(TEAL),spaceBefore=5,spaceAfter=6,keepWithNext=True),
 'note':ParagraphStyle('n',fontName='Memo',fontSize=9,leading=12.6,textColor=colors.HexColor(MUTED),spaceBefore=5,spaceAfter=10),
 'cell':ParagraphStyle('c',fontName='Memo',fontSize=9.1,leading=11.7,textColor=colors.HexColor(INK)),
 'th':ParagraphStyle('th',fontName='MemoBold',fontSize=8.5,leading=11,textColor=colors.white)}
def pdfmarkup(s):
 s=s.replace('&','&amp;').replace('\n','<br/>')
 return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<link href="{html.escape(m[2],quote=True)}" color="{TEAL}">{m[1]}</link>',s)
def htmlmarkup(s):return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<a href="{html.escape(m[2],quote=True)}">{m[1]}</a>',s)
class Graphic(Flowable):
 def __init__(self):super().__init__();self.width=495;self.height=130
 def draw(self):
  c=self.canv
  def box(x,y,w,title,sub):
   c.setFillColor(colors.HexColor(PALE));c.setStrokeColor(colors.HexColor(LINE));c.roundRect(x,y,w,43,5,fill=1,stroke=1)
   c.setFillColor(colors.HexColor(INK));c.setFont('MemoBold',9);c.drawCentredString(x+w/2,y+25,title)
   c.setFillColor(colors.HexColor(MUTED));c.setFont('Memo',7.8);c.drawCentredString(x+w/2,y+11,sub)
  def line(x,y,xx,yy):
   c.setStrokeColor(colors.HexColor(TEAL));c.setLineWidth(1.2);c.line(x,y,xx,yy)
  box(0,43,145,'Document encoded once','per-layer shared K/V')
  box(175,78,149,'Question A + candidates','pretrained branch computation')
  box(175,8,149,'Question B + candidates','pretrained branch computation')
  box(353,43,142,'Direct decision scores','no generated answer text')
  line(145,65,174,100);line(145,65,174,30);line(325,100,352,65);line(325,30,352,65)

story=[];md=['# SelfJev: quality and speed strategy\n'];ht=[];heights=[]
for i,p in enumerate(pages):
 if i:story.append(PageBreak())
 part=[Paragraph(pdfmarkup(p['kicker']),styles['kicker']),Paragraph(pdfmarkup(p['title']),styles['title']),Paragraph(pdfmarkup(p['deck']),styles['deck'])]
 md += ['\n## '+p['title']+'\n',p['deck']+'\n'];ht.append(f'<section id="p{i+1}"><div class="kicker">{p["kicker"]}</div><h1>{p["title"]}</h1><p class="deck">{p["deck"]}</p>')
 for kind,val in p['blocks']:
  if kind in ['p','h','note']:
   part.append(Paragraph(pdfmarkup(val),styles[kind]));md.append(('### ' if kind=='h' else '> ' if kind=='note' else '')+val.replace('<b>','**').replace('</b>','**')+'\n')
   tag='h2' if kind=='h' else 'p';ht.append(f'<{tag} class="{kind}">{htmlmarkup(val)}</{tag}>')
  elif kind=='table':
   hs,rs,ws=val
   cells=[[Paragraph(pdfmarkup(x),styles['th']) for x in hs]]+[[Paragraph(pdfmarkup(x),styles['cell']) for x in row] for row in rs]
   tb=Table(cells,colWidths=ws,hAlign='LEFT',repeatRows=1)
   tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor(TEAL)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor(PALE),colors.white]),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor(LINE))]))
   part += [tb,Spacer(1,11)]
   md += ['| '+' | '.join(hs)+' |','|'+'---|'*len(hs)]+['| '+' | '.join(row)+' |' for row in rs]+['']
   ht.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in hs)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+htmlmarkup(x)+'</td>' for x in row)+'</tr>' for row in rs)+'</tbody></table></div>')
  else:
   part += [Graphic(),Spacer(1,8)]
   md.append('```mermaid\nflowchart LR\nD[Document encoded once] --> A[Question A: pretrained layers]\nD --> B[Question B: pretrained layers]\nA --> S[Direct decision scores]\nB --> S\n```\n')
   ht.append('<div class="flow"><div>Document encoded once<br>Shared per-layer K/V</div><span>&rarr;</span><div>Independent question branches<br>Pretrained interaction</div><span>&rarr;</span><div>Direct decision scores<br>No answer generation</div></div>')
 heights.append(round(sum(x.wrap(495,10000)[1]+x.getSpaceBefore()+x.getSpaceAfter() for x in part),1));story+=part;ht.append('</section>')
def footer(c,doc):
 c.saveState();c.setStrokeColor(colors.HexColor(LINE));c.line(50,40,545,40)
 c.setFillColor(colors.HexColor(MUTED));c.setFont('Memo',8);c.drawString(50,27,'SELFJEV / QUALITY + SPEED STRATEGY / 23 SEP 2026');c.drawRightString(545,27,f'{doc.page:02d}');c.restoreState()
PDF.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(PDF),pagesize=(595.28,841.89),leftMargin=50,rightMargin=50.28,topMargin=42,bottomMargin=55,title='SelfJev - Quality and Speed Strategy',author='Codex for Julien',pageCompression=1).build(story,onFirstPage=footer,onLaterPages=footer)
(OUT/'strategy.md').write_text('\n'.join(md))
css='''*{box-sizing:border-box}body{margin:0;background:#f3f5f1;color:#18302f;font:17px/1.65 system-ui,sans-serif}header,main{max-width:1040px;margin:auto}header{padding:38px 42px 16px}section{background:white;margin:24px 0;padding:46px 54px;border-top:4px solid #11776f}h1{font-size:34px;line-height:1.16;letter-spacing:-1px;margin:14px 0}h2{font-size:20px;color:#11776f;margin:24px 0 6px}.kicker{font-size:12px;font-weight:700;letter-spacing:1px;color:#11776f}.deck{font-size:19px;color:#61716f}.note{font-size:15px;color:#61716f;border-left:3px solid #d4e2dc;padding-left:16px}a{color:#11776f;text-underline-offset:3px;overflow-wrap:anywhere}table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5;margin:18px 0}th{background:#11776f;color:white;text-align:left;font-size:13px}th,td{padding:12px;vertical-align:top}tbody tr:nth-child(odd){background:#eff6f3}.table-wrap{overflow-x:auto}.flow{display:flex;align-items:center;gap:12px;margin:26px 0;font-size:15px}.flow div{flex:1;background:#eff6f3;border:1px solid #d4e2dc;padding:16px}@media(max-width:700px){section{padding:25px 20px;margin:16px 10px}h1{font-size:28px}.flow{flex-direction:column}.flow span{transform:rotate(90deg)}table{min-width:540px}}'''
(OUT/'strategy.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SelfJev - Quality and Speed Strategy</title><style>'+css+'</style></head><body><header><b>SelfJev / Design memo</b><p>Evidence, architectural choices and controlled experiments.</p></header><main>'+''.join(ht)+'</main></body></html>')
paths=['reports/curve/instruct_zero/test/report.json','reports/curve/instruct_zero/validation/report.json','reports/lora_4b/test/report.json','reports/lora_8b/test/report.json','reports/external/full/typesafe_jev-latest/report.json','reports/deep_review_2026-09-23/audit.json','reports/deep_review_2026-09-23/component_ablation.json','src/personal_jev/tree.py']
snapshot={'created_at':datetime.now().astimezone().isoformat(),'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source_sha256':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'new_training_performed':False,'experiment_targets':'Recommendations, not measured outcomes'}
(OUT/'snapshot.json').write_text(json.dumps(snapshot,indent=2)+'\n')
print(json.dumps({'pdf':str(PDF),'designed_pages':len(pages),'page_heights':heights,'words':len(' '.join(md).split())}))
