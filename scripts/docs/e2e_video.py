# ruff: noqa: E501  (the video page: HTML, CSS and JS in one template)
"""A short product video of an end-to-end run, made from its record (reports/e2e/<date>/): 1920x1080, 30 fps, 75 s.

Every answer, number and name on screen comes from the run's transcript.jsonl and report.md. The page animates from a
timeline in JavaScript; headless Chromium (Playwright) captures it frame by frame and ffmpeg encodes the MP4, so the
same run always renders the same video.

  uv run --no-project --with playwright python scripts/docs/e2e_video.py reports/e2e/2026-09-28
  -> <run>/selfjev_e2e.mp4 and <run>/poster.png

Chromium: $CHROMIUM, else Playwright's cached headless shell, else Playwright's default. Fonts: the site's DM Sans and
JetBrains Mono from website/node_modules when present.
"""

import argparse
import glob
import json
import os
import re
import statistics
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FPS, SECONDS, POSTER_AT = 30, 75.0, 66.0


def facts(run: Path) -> dict:
    rows = [json.loads(line) for line in (run / "transcript.jsonl").read_text().splitlines()]
    report = (run / "report.md").read_text()
    decide = next(r for r in rows if r["path"] == "/v1/systemone" and r["status"] == 200)
    jev = next(r for r in rows if r["path"] == "/api/alpha/decisions" and r["status"] == 200)
    single = [r["ms"] for r in rows if r["status"] == 200 and r["path"] in ("/v1/systemone", "/api/alpha/decisions") and r["ms"] < 5000]
    err = {r["status"]: json.loads(r["response"])["error"] for r in rows if r["path"] == "/v1/systemone" and r["status"] >= 400}
    files = [json.loads(r["response"]) for r in rows if r["path"] == "/v1/files" and r["status"] == 200]
    bad = next(json.loads(r["response"])["error"] for r in rows if r["path"] == "/v1/files" and r["status"] == 422)
    methods = {
        json.loads(r["response"])["id"]: json.loads(r["request"])["method"]["type"] for r in rows if r["path"] == "/v1/fine_tuning/jobs"
    }
    jobs = []
    for r in rows:
        if r["path"].startswith("/v1/fine_tuning/jobs/ftjob_") and not r["path"].endswith("/events") and '"succeeded"' in r["response"]:
            j = json.loads(r["response"])
            jobs.append({"method": methods[j["id"]], "model": j["fine_tuned_model"], "seconds": j["finished_at"] - j["created_at"]})
    models = next(json.loads(r["response"]) for r in reversed(rows) if r["path"] == "/v1/models")["data"]
    n = re.search(r"\*\*(\d+) of (\d+) checks passed", report)
    return {
        "date": run.name,
        "state": json.loads(decide["request"])["state"],
        "questions": json.loads(decide["request"])["questions"],
        "answers": json.loads(decide["response"])["answers"],
        "jev_answers": json.loads(jev["response"])["answers"],
        "single_ms": statistics.median(single),
        "errors": {str(k): v for k, v in err.items()},
        "file": files[0],
        "bad": bad,
        "jobs": jobs,
        "models": [m["id"] for m in models],
        "passed": int(n.group(1)),
        "checks": int(n.group(2)),
        "ready_min": float(re.search(r"ready after: ([\d.]+) min", report).group(1)),
        "cost": re.search(r"cost: ≈ \$([\d.]+)", report).group(1),
        "commit": re.search(r"commit: `([0-9a-f]{7})", report).group(1),
        "instance": re.search(r"--instance (\S+)", report).group(1),
        "region": re.search(r"--region (\S+)", report).group(1),
        "endpoint": re.search(r"\| (http://[\d.:]+) \|", report).group(1),
    }


PAGE = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:"DM Sans";src:url("__FONTS__/dm-sans/files/dm-sans-latin-wght-normal.woff2") format("woff2");font-weight:100 1000}
@font-face{font-family:"JB Mono";src:url("__FONTS__/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2") format("woff2");font-weight:100 800}
:root{--bg:#111211;--panel:#181a18;--panel2:#1d1f1d;--text:#eeeee7;--soft:#c2c6bb;--muted:#9c9f96;--faint:#696e65;--line:#30332e;
--edge:#373d32;--orange:#ff7547;--olive:#bad68e;--amber:#f3bd75;--kw:#c8b5ed;--str:#b9d78c;--fn:#9bd4cd;--num:#f3bd75;--key:#ffc08a;--pun:#aeb8a2}
*{box-sizing:border-box}body{margin:0;background:var(--bg)}
#stage{position:relative;width:1920px;height:1080px;overflow:hidden;background:var(--bg);color:var(--text);
 font-family:"DM Sans","Helvetica Neue",sans-serif;-webkit-font-smoothing:antialiased}
.grid{position:absolute;inset:0;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);
 background-size:40px 40px;opacity:.32;-webkit-mask-image:radial-gradient(ellipse 70% 80% at 72% 50%,#000 25%,transparent 75%)}
.glow{position:absolute;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(255,117,71,.10),transparent 65%);right:-150px;top:60px}
.mono{font-family:"JB Mono",Menlo,monospace}
header{position:absolute;top:44px;left:96px;right:96px;display:flex;align-items:center;justify-content:space-between;z-index:5}
.brand{display:flex;align-items:center;gap:16px}.mark{display:flex;flex-direction:column;gap:6px}.mark i{display:block;height:4px;background:var(--orange);border-radius:1px}
.word{font-weight:700;font-size:32px;letter-spacing:-1.4px}
.kicker{font-family:"JB Mono",monospace;font-size:14px;letter-spacing:3px;color:var(--muted);text-transform:uppercase}
footer{position:absolute;left:96px;right:96px;bottom:40px;display:flex;justify-content:space-between;z-index:5}
#progress{position:absolute;left:0;bottom:0;height:4px;background:var(--orange);z-index:6}
.scene{position:absolute;inset:0;opacity:0}
.left{position:absolute;left:96px;top:0;bottom:0;width:720px;display:flex;flex-direction:column;justify-content:center}
.right{position:absolute;right:96px;top:170px;bottom:130px;width:960px;display:flex;flex-direction:column;justify-content:center;gap:22px}
.tag{font-family:"JB Mono",monospace;font-size:15px;letter-spacing:3px;color:var(--orange);text-transform:uppercase;margin-bottom:30px;display:flex;align-items:center;gap:14px}
.tag:before{content:"";width:34px;height:3px;background:var(--orange)}
.h1{font-size:92px;line-height:.98;letter-spacing:-4.5px;font-weight:560;margin:0}.h1 em{font-style:normal;color:var(--orange)}
.sub{font-size:29px;line-height:1.38;color:var(--soft);margin-top:34px;max-width:680px}
.panel{background:var(--panel);border:1px solid var(--edge);border-radius:18px;box-shadow:0 40px 90px rgba(0,0,0,.5);overflow:hidden}
.pbar{height:52px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:9px;padding:0 22px;font-family:"JB Mono",monospace;
 font-size:14px;letter-spacing:1.5px;color:var(--muted);text-transform:uppercase}
.pbar b{width:11px;height:11px;border-radius:50%;background:#3a3f37;display:inline-block}.pbar b:first-child{background:var(--orange)}
.pbar .sp{flex:1}.pbar .badge{color:var(--bg);background:var(--olive);padding:4px 10px;border-radius:6px;letter-spacing:1.5px;font-size:12px}
.term{padding:30px 34px;font-family:"JB Mono",monospace;font-size:23px;line-height:1.95}
.term .cmd{color:var(--text)}.term .cmd:before{content:"$ ";color:var(--orange)}
.term .k{display:inline-block;width:170px;color:var(--muted)}.term .ok{color:var(--olive)}
.caret:after{content:"";display:inline-block;width:12px;height:26px;background:var(--orange);margin-left:4px;vertical-align:-4px}
.code{padding:26px 30px;font-family:"JB Mono",monospace;font-size:19.5px;line-height:1.72;white-space:pre;color:var(--text)}
.kw{color:var(--kw)}.st{color:var(--str)}.fn{color:var(--fn)}.nu{color:var(--num)}.ky{color:var(--key)}.pu{color:var(--pun)}.cm{color:#a1ad90}
.pill{display:inline-flex;align-items:center;gap:12px;white-space:pre;font-family:"JB Mono",monospace;font-size:18px;padding:10px 16px;border-radius:10px;
 background:var(--panel2);border:1px solid var(--edge);color:var(--soft)}
.dot{width:10px;height:10px;border-radius:50%;background:var(--olive)}
.ans{display:grid;grid-template-columns:170px 1fr 170px;align-items:center;gap:22px;padding:14px 26px;border-bottom:1px solid var(--line);min-height:74px}
.ans .wide{grid-column:2 / 4}
.ans:last-child{border-bottom:0}.qid{font-family:"JB Mono",monospace;font-size:21px;color:var(--text)}.qid small{display:block;font-size:13px;letter-spacing:2px;color:var(--muted);text-transform:uppercase;margin-top:2px}
.track{height:12px;border-radius:6px;background:#262925;position:relative;overflow:hidden}.fill{position:absolute;left:0;top:0;bottom:0;width:0;background:var(--orange);border-radius:6px}
.val{font-family:"JB Mono",monospace;font-size:26px;text-align:right}.val.small{font-size:20px;color:var(--soft)}
.chips{display:flex;gap:10px;flex-wrap:nowrap}.chip{font-family:"JB Mono",monospace;font-size:16px;padding:6px 11px;white-space:nowrap;border-radius:8px;border:1px solid var(--edge);color:var(--faint)}
.chip.on{color:var(--bg);background:var(--orange);border-color:var(--orange)}
.scale{position:relative;height:12px;border-radius:6px;background:#262925}.scale i{position:absolute;top:-5px;width:2px;height:22px;background:#444a40}
.scale .mk{position:absolute;top:-9px;width:30px;height:30px;border-radius:50%;background:var(--orange);margin-left:-15px;box-shadow:0 0 0 6px rgba(255,117,71,.18)}
.row{display:grid;grid-template-columns:120px 1fr;gap:24px;align-items:center;padding:20px 28px;border-bottom:1px solid var(--line)}
.row:last-child{border-bottom:0}.code-pill{font-family:"JB Mono",monospace;font-size:21px;font-weight:600;text-align:center;padding:8px 0;border-radius:9px}
.s2{background:rgba(186,214,142,.14);color:var(--olive)}.s4{background:rgba(255,117,71,.14);color:var(--orange)}.s42{background:rgba(243,189,117,.14);color:var(--amber)}
.what{font-size:25px}.det{font-family:"JB Mono",monospace;font-size:17px;color:var(--muted);margin-top:5px}
.cmp{display:grid;grid-template-columns:200px 1fr 1fr 60px;gap:0;font-family:"JB Mono",monospace;font-size:21px}
.cmp div{padding:13px 24px;border-bottom:1px solid var(--line)}.cmp .hd{color:var(--muted);font-size:14px;letter-spacing:2px;text-transform:uppercase}
.cmp .ck{color:var(--olive);text-align:center}
.job{display:grid;grid-template-columns:170px 1fr 120px 150px;gap:22px;align-items:center;padding:18px 28px;border-bottom:1px solid var(--line);font-family:"JB Mono",monospace;font-size:21px}
.status{font-size:15px;letter-spacing:1.5px;text-transform:uppercase;text-align:center;padding:7px 0;border-radius:8px;background:#262925;color:var(--muted)}
.status.done{background:rgba(186,214,142,.16);color:var(--olive)}
.model{font-family:"JB Mono",monospace;font-size:21px;padding:13px 28px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between}
.model .new{font-size:13px;letter-spacing:2px;color:var(--bg);background:var(--orange);padding:4px 9px;border-radius:6px}
.center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.big{font-size:230px;font-weight:600;letter-spacing:-12px;line-height:.9}.big em{font-style:normal;color:var(--orange)}
.tiles{display:grid;grid-template-columns:repeat(4,330px);gap:26px;margin-top:70px}
.tile{background:var(--panel);border:1px solid var(--edge);border-radius:16px;padding:30px 30px 28px;text-align:left}
.tile b{display:block;font-size:56px;letter-spacing:-2px;font-weight:560;color:var(--text)}.tile span{display:block;font-size:21px;color:var(--muted);margin-top:8px;line-height:1.3}
.cta{margin-top:56px;display:flex;gap:18px}.cta .pill{font-size:22px;padding:14px 22px}
</style></head><body><div id="stage"><div class="grid"></div><div class="glow"></div>
<header><div class="brand"><div class="mark"><i style="width:30px"></i><i style="width:20px"></i><i style="width:30px"></i></div><div class="word">selfjev</div></div>
<div class="kicker" id="kick"></div></header>
<footer><div class="kicker" id="label"></div><div class="kicker" id="src"></div></footer><div id="progress"></div></div>
<script>
const D = __DATA__, TOTAL = __SECONDS__;
const stage = document.getElementById('stage');
function h(tag, cls, html) { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
function fx(e, kind, at, dur = 0.6, extra = {}) { e.dataset.fx = kind; e.dataset.at = at; e.dataset.dur = dur; Object.assign(e.dataset, extra); return e; }
const scenes = [];
function scene(start, end, label) { const s = h('section', 'scene'); s.dataset.start = start; s.dataset.end = end; s.dataset.label = label; stage.append(s); scenes.push(s); return s; }
const fmt = (x, d = 2) => Number(x).toFixed(d);
const mmss = s => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(Math.round(s) % 60).padStart(2, '0')}`;
function left(s, tag, title, sub, at = 0.2) {
  const l = h('div', 'left'); s.append(l);
  l.append(fx(h('div', 'tag', tag), 'fade', at), fx(h('h1', 'h1', title), 'fade', at + 0.15, 0.7), fx(h('div', 'sub', sub), 'fade', at + 0.45, 0.7));
  return l;
}
function panel(title, badge) { const p = h('div', 'panel'); p.append(h('div', 'pbar', `<b></b><b></b><b></b><span style="margin-left:10px">${title}</span><span class="sp"></span>` + (badge ? `<span class="badge">${badge}</span>` : ''))); return p; }
document.getElementById('kick').textContent = `Recorded end-to-end run · ${D.date}`;
document.getElementById('src').textContent = `reports/e2e/${D.date}`;

// 1. title
{ const s = scene(0, 5, '00 / selfjev');
  const c = h('div', 'left'); c.style.width = '1500px'; s.append(c);
  c.append(fx(h('div', 'tag', 'The self-hosted decision model'), 'fade', 0.3),
           fx(h('h1', 'h1', 'Intelligence,<br><em>decided.</em>'), 'fade', 0.5, 0.9),
           fx(h('div', 'sub', "Jev's decisions API, on your own GPU. One recorded run, start to finish."), 'fade', 1.2, 0.8));
  c.querySelector('.h1').style.cssText = 'font-size:180px;letter-spacing:-9px';
  c.querySelector('.sub').style.maxWidth = '1100px'; }

// 2. deploy
{ const s = scene(5, 15.5, '01 / Deploy');
  left(s, '01 · Deploy', 'One command.<br><em>A live API.</em>', 'A GPU box, the model, the server and an API key, from your laptop.');
  const r = h('div', 'right'); s.append(r);
  const p = panel('terminal', ''); r.append(p); const badge = p.querySelector('.pbar'); const tl = h('span', 'badge', 'time-lapse'); badge.append(tl); fx(tl, 'blink', 3.3, 4.6);
  const t = h('div', 'term'); p.append(t);
  t.append(fx(h('div', 'cmd'), 'type', 0.8, 1.6, { full: `selfjev deploy aws up --instance ${D.instance} --fine-tuning` }));
  const lines = [['launching', `${D.instance} · NVIDIA L40S 48 GB · ${D.region}`], ['installing', `selfjev @ ${D.commit}`],
                 ['fetching', 'Qwen3.5-4B + the selfjev-4b adapter'], ['serving', "Jev's decisions API on :8000"]];
  lines.forEach(([k, v], i) => t.append(fx(h('div', '', `<span class="k">${k}</span>${v}`), 'fade', 2.8 + i * 1.0, 0.4)));
  const ok = h('div', '', `<span class="k ok">✓ healthy</span><span class="clock ok"></span><span style="color:var(--muted)"> after launch</span>`);
  t.append(fx(ok, 'fade', 3.3, 0.4)); fx(ok.querySelector('.clock'), 'clock', 3.3, 4.6, { to: Math.round(D.ready_min * 60) });
  t.append(fx(h('div', '', `<span class="k">endpoint</span>${D.endpoint}  <span style="color:var(--muted)">key sj-••••••••</span>`), 'fade', 8.2, 0.5)); }

// 3. decide
{ const s = scene(15.5, 31.5, '02 / Decide');
  const top = h('div', ''); top.style.cssText = 'position:absolute;left:96px;top:140px;width:1728px'; s.append(top);
  top.append(fx(h('div', 'tag', '02 · Decide'), 'fade', 0.2));
  const t1 = fx(h('h1', 'h1', 'One text. <em>Many answers.</em>'), 'fade', 0.35, 0.7); t1.style.fontSize = '76px'; top.append(t1);
  const code = panel('python', ''); code.style.cssText = 'position:absolute;left:96px;top:350px;width:900px;height:610px'; s.append(code);
  const q = D.questions;
  const src = [
    `<span class="ky">client</span> <span class="pu">=</span> <span class="fn">SelfJev</span><span class="pu">(</span>base_url<span class="pu">=</span>URL<span class="pu">,</span> api_key<span class="pu">=</span>KEY<span class="pu">)</span>`,
    `<span class="ky">res</span> <span class="pu">=</span> client<span class="pu">.</span><span class="fn">system_one</span><span class="pu">(</span>`,
    `    state<span class="pu">=</span><span class="st">"Ticket 4411 from Dana (Pro plan, paying since</span>`,
    `<span class="st">           2023): I was charged twice for invoice INV-2291</span>`,
    `<span class="st">           this morning. Please refund the second charge</span>`,
    `<span class="st">           today, I need the money for payroll."</span><span class="pu">,</span>`,
    `    questions<span class="pu">={</span>`,
    ...[['refund', 'Noul'], ['spam', 'Noul'], ['paid', 'Noul'], ['team', 'Choice'], ['urgency', 'Score'], ['topics', 'Multi']].map(([k, f]) =>
      `        <span class="st">"${k}"</span><span class="pu">:</span>${' '.repeat(8 - k.length)}<span class="fn">${f}</span><span class="pu">(</span><span class="st">"${q[k].instructions}"</span>${f === 'Noul' && k !== 'paid' ? '' : '<span class="pu">, …</span>'}<span class="pu">),</span>`),
    `    <span class="pu">},</span>`, `<span class="pu">)</span>`];
  const pre = h('div', 'code'); code.append(pre);
  src.forEach((line, i) => pre.append(fx(h('div', '', line || ' '), 'wipe', 0.9 + i * 0.2, 0.35)));
  const pill = h('div', 'pill', `<span class="dot"></span>POST /v1/systemone → 200 · ${fmt(D.single_ms / 1000, 1)} s round trip`);
  pill.style.cssText = 'position:absolute;left:1036px;top:350px'; s.append(fx(pill, 'fade', 4.3, 0.5));
  const card = h('div', 'panel'); card.style.cssText = 'position:absolute;left:1036px;top:428px;width:788px'; s.append(card);
  const A = D.answers; let at = 4.8;
  const add = (qid, type, mid, val) => { const r = h('div', 'ans'); r.append(h('div', 'qid', `${qid}<small>${type}</small>`), mid); if (val) r.append(val); else mid.classList.add('wide'); card.append(fx(r, 'fade', at, 0.45)); at += 0.35; return r; };
  for (const k of ['refund', 'spam', 'paid']) {
    const tr = h('div', 'track'); const f = h('div', 'fill'); tr.append(f); fx(f, 'bar', at + 0.2, 0.9, { to: A[k].noul });
    add(k, 'yes / no', tr, fx(h('div', 'val'), 'count', at + 0.2, 0.9, { to: A[k].noul, dec: 2 }));
  }
  { const m = h('div', 'chips'); for (const [c, p] of Object.entries(A.team.probabilities)) m.append(h('span', 'chip' + (c === A.team.choice ? ' on' : ''), `${c} ${fmt(p, 2)}`)); add('team', 'pick one', m); }
  { const sc = h('div', 'scale'); const n = q.urgency.criteria.length; for (let i = 0; i < n; i++) { const tick = h('i'); tick.style.left = `${(100 * i) / (n - 1)}%`; sc.append(tick); }
    const mk = h('div', 'mk'); sc.append(mk); fx(mk, 'slide', at + 0.2, 1.0, { to: A.urgency.score / (n - 1) });
    const uv = h('div', 'val small', `${fmt(A.urgency.score, 2)} · ${A.urgency.legend[String(Math.round(A.urgency.score))]}`); uv.style.whiteSpace = 'nowrap'; add('urgency', 'scale 0–2', sc, uv); }
  { const m = h('div', 'chips'); for (const [c, p] of Object.entries(A.topics.probabilities)) m.append(h('span', 'chip' + (A.topics.multi.includes(c) ? ' on' : ''), `${c} ${fmt(p, 2)}`)); add('topics', 'all that apply', m); } }

// 4. compatible
{ const s = scene(31.5, 39.5, '03 / Compatible');
  left(s, "03 · Jev-compatible", "Speaks <em>Jev's API.</em>", 'Code written for Jev runs against your own server: same request, same paths, same model names.');
  const r = h('div', 'right'); s.append(r);
  r.append(fx(h('div', 'pill', `<span class="dot"></span>POST /v1/systemone         "model": "selfjev-4b"`), 'fade', 0.9, 0.5),
           fx(h('div', 'pill', `<span class="dot"></span>POST /api/alpha/decisions  "model": "jev-latest"`), 'fade', 1.3, 0.5));
  const p = h('div', 'panel'); r.append(p); const g = h('div', 'cmp'); p.append(g);
  ['question', '/v1/systemone', '/api/alpha/decisions', ''].forEach(x => g.append(h('div', 'hd', x)));
  const show = a => a.type === 'noul' ? fmt(a.noul, 3) : a.type === 'choice' ? a.choice : a.type === 'score' ? fmt(a.score, 3) : `[${a.multi.join(', ')}]`;
  Object.keys(D.answers).forEach((k, i) => { const same = show(D.answers[k]) === show(D.jev_answers[k]);
    [k, show(D.answers[k]), show(D.jev_answers[k]), same ? '✓' : '✗'].forEach((x, j) => g.append(fx(h('div', j === 3 ? 'ck' : '', x), 'fade', 1.9 + i * 0.3, 0.4))); });
  r.append(fx(h('div', 'pill', '<span class="dot"></span>identical answers on both paths'), 'fade', 4.2, 0.5)); }

// 5. production
{ const s = scene(39.5, 47.5, '04 / Production');
  left(s, '04 · Production', 'Clear errors.<br><em>No surprises.</em>', 'API keys, typed errors that name the field at fault, and requests batched on the GPU.');
  const r = h('div', 'right'); s.append(r); const p = h('div', 'panel'); r.append(p); const E = D.errors;
  const rows = [['401', 's4', 'a wrong API key', E['401'].message], ['422', 's42', 'a choice with one option', `param ${E['422'].param}`],
                ['404', 's4', 'an unknown model', E['404'].message.split(';')[0]], ['200', 's2', 'a JSON object as the text', 'same answers'],
                ['200 ×16', 's2', 'sixteen requests at once', 'all answered, batched together']];
  rows.forEach(([c, cls, what, det], i) => { const row = h('div', 'row'); row.append(h('div', 'code-pill ' + cls, c), h('div', '', `<div class="what">${what}</div><div class="det">${det}</div>`)); p.append(fx(row, 'fade', 0.9 + i * 0.45, 0.45)); }); }

// 6. fine-tune
{ const s = scene(47.5, 63.5, '05 / Fine-tune');
  left(s, '05 · Fine-tune', 'Fine-tune it<br><em>over HTTP.</em>', 'Upload labeled requests, start a job, and the new model is served next to the base one.');
  const r = h('div', 'right'); r.style.gap = '18px'; s.append(r);
  const f = D.file, up = panel('POST /v1/files', ''); r.append(fx(up, 'fade', 0.9, 0.5));
  up.append(h('div', 'model', `<span>${f.filename} · ${f.rows} texts · ${f.questions} questions</span><span style="color:var(--olive)">✓ uploaded</span>`),
            h('div', 'model', `<span style="color:var(--muted)">a malformed line is refused</span><span style="color:var(--amber)">422 ${D.bad.param}</span>`));
  const jp = panel('POST /v1/fine_tuning/jobs', ''); r.append(fx(jp, 'fade', 1.7, 0.5)); const tl = h('span', 'badge', 'time-lapse'); jp.querySelector('.pbar').append(tl); fx(tl, 'blink', 2.4, 5.4);
  const total = D.jobs.reduce((a, j) => a + j.seconds, 0); let start = 2.4;  // one job at a time, as the server's queue runs them
  D.jobs.forEach(j => { const row = h('div', 'job'); const tr = h('div', 'track'); const fl = h('div', 'fill'); tr.append(fl);
    const dur = 5.4 * j.seconds / total; fx(fl, 'bar', start, dur, { to: 1, lin: 1 });
    row.append(h('div', '', j.method), tr, fx(h('div', 'clock'), 'clock', start, dur, { to: j.seconds, lin: 1 }), fx(h('div', 'status'), 'status', start, dur));
    jp.append(row); start += dur; });
  const mp = panel('GET /v1/models', ''); r.append(fx(mp, 'fade', 8.1, 0.5));
  D.models.forEach((m, i) => mp.append(fx(h('div', 'model', `<span>${m}</span>` + (i ? '<span class="new">new</span>' : '<span style="color:var(--muted)">base</span>')), 'fade', 8.5 + i * 0.4, 0.4)));
  r.append(fx(h('div', 'pill', '<span class="dot"></span>both fine-tuned models answer the ticket right'), 'fade', 10.2, 0.5)); }

// 7. the run
{ const s = scene(63.5, 70.5, '06 / The run');
  const c = h('div', 'center'); s.append(c);
  c.append(fx(h('div', 'tag', 'One recorded run'), 'fade', 0.2));
  const big = h('div', 'big', `<span class="n"></span><em>/${D.checks}</em>`); fx(big.querySelector('.n'), 'count', 0.4, 1.2, { to: D.passed, dec: 0 }); c.append(fx(big, 'fade', 0.3, 0.5));
  const cs = h('div', 'sub', 'checks passed, against the real model on an NVIDIA L40S'); cs.style.maxWidth = '1400px'; c.append(fx(cs, 'fade', 0.9, 0.6));
  const tiles = h('div', 'tiles'); c.append(tiles);
  [[`${fmt(D.ready_min, 1)} min`, 'from launch to a live API'], [`${fmt(D.single_ms / 1000, 1)} s`, 'per request, six questions'],
   [`${D.jobs.length}`, 'fine-tuned models, served next to the base'], [`≈ $${D.cost}`, 'for the whole run']]
    .forEach(([b, t], i) => tiles.append(fx(h('div', 'tile', `<b>${b}</b><span>${t}</span>`), 'fade', 1.6 + i * 0.25, 0.5))); }

// 8. end
{ const s = scene(70.5, TOTAL + 1, 'selfjev');
  const c = h('div', 'center'); s.append(c);
  c.append(fx(h('h1', 'h1', 'Intelligence, <em>decided.</em>'), 'fade', 0.2, 0.8));
  const cta = h('div', 'cta'); cta.append(h('span', 'pill', 'github.com/Jwuthri/SelfJev'), h('span', 'pill', '<span class="dot"></span>selfjev deploy aws up'));
  c.append(fx(cta, 'fade', 0.8, 0.6)); c.querySelector('.h1').style.fontSize = '130px'; }

const clamp = x => Math.max(0, Math.min(1, x)), out3 = p => 1 - Math.pow(1 - p, 3);
const back = p => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); };
const fxs = [...document.querySelectorAll('[data-fx]')];
function render(t) {
  let cur = scenes[0];
  for (const s of scenes) { const a = +s.dataset.start, b = +s.dataset.end; const o = clamp((t - a) / 0.45) * clamp((b - t) / 0.45);
    s.style.opacity = o; s.style.visibility = o > 0 ? 'visible' : 'hidden'; if (t >= a) cur = s; }
  document.getElementById('label').textContent = cur.dataset.label;
  document.getElementById('progress').style.width = `${100 * clamp(t / TOTAL)}%`;
  for (const e of fxs) {
    const s0 = +e.closest('.scene').dataset.start, p = clamp((t - s0 - +e.dataset.at) / +e.dataset.dur), q = e.dataset.lin ? p : out3(p);
    switch (e.dataset.fx) {
      case 'fade': e.style.opacity = q; e.style.transform = `translateY(${(1 - q) * 22}px)`; break;
      case 'wipe': e.style.clipPath = `inset(0 ${100 * (1 - q)}% 0 0)`; break;
      case 'type': { const full = e.dataset.full; e.textContent = full.slice(0, Math.round(full.length * p)); e.classList.toggle('caret', p < 1 || (t * 2) % 2 < 1); break; }
      case 'count': e.textContent = (+e.dataset.to * q).toFixed(+e.dataset.dec); break;
      case 'bar': e.style.width = `${100 * +e.dataset.to * q}%`; break;
      case 'slide': e.style.left = `${100 * +e.dataset.to * q}%`; break;
      case 'clock': e.textContent = mmss(+e.dataset.to * q); break;
      case 'blink': e.style.opacity = p > 0 && p < 1 ? 0.55 + 0.45 * Math.cos(t * 7) : 0; break;
      case 'status': e.textContent = t - s0 < +e.dataset.at ? 'queued' : p >= 1 ? 'succeeded' : 'running'; e.classList.toggle('done', p >= 1); break;
    }
  }
}
render(0);
</script></body></html>"""


def chromium() -> str | None:
    if os.environ.get("CHROMIUM"):
        return os.environ["CHROMIUM"]
    found = sorted(
        glob.glob(
            os.path.expanduser("~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell")
        )
    )
    return found[-1] if found else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("run", help="an end-to-end run folder, e.g. reports/e2e/2026-09-28")
    ap.add_argument("--out", help="default <run>/selfjev_e2e.mp4")
    ap.add_argument("--stills", nargs="*", type=float, help="only these times (s), as PNGs next to --out, to check the design")
    a = ap.parse_args()
    run = Path(a.run)
    out = Path(a.out or run / "selfjev_e2e.mp4")
    fonts = (ROOT / "website/node_modules/@fontsource-variable").as_uri()
    html = PAGE.replace("__DATA__", json.dumps(facts(run))).replace("__SECONDS__", str(SECONDS)).replace("__FONTS__", fonts)
    page_file = Path(tempfile.mkdtemp()) / "video.html"
    page_file.write_text(html)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chromium())
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(page_file.as_uri())
        page.evaluate("document.fonts.ready")
        if a.stills:
            for t in a.stills:
                page.evaluate(f"render({t})")
                page.screenshot(path=str(out.with_name(f"still_{t:05.1f}.png")))
            return browser.close()
        page.evaluate(f"render({POSTER_AT})")
        page.screenshot(path=str(run / "poster.png"))
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
               "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]  # fmt: skip
        ffmpeg = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(int(SECONDS * FPS)):
            page.evaluate(f"render({i / FPS})")
            ffmpeg.stdin.write(page.screenshot(type="png"))
        ffmpeg.stdin.close()
        ffmpeg.wait()
        browser.close()
    print(f"{out} ({out.stat().st_size / 1e6:.1f} MB) and {run / 'poster.png'}")


if __name__ == "__main__":
    main()
