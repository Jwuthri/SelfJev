"use client";

import { useEffect, useId, useRef, useState, type CSSProperties } from "react";
import Link from "next/link";
import { ArrowUpRight, Pause, Play } from "lucide-react";

// Binary scores one proposed answer against yes/no logits; choice and multi
// score one branch per candidate. These outputs illustrate the API, not a run.
const lanes = [
  { x: 190, type: "BINARY · YES / NO", question: "Refund requested?", hint: "One yes / no decision", candidates: [{ dx: 0, label: "Yes", width: 150, selected: true }], result: "Yes", readout: "A boolean for your code" },
  { x: 540, type: "MULTICLASS · PICK ONE", question: "Which team?", hint: "Billing or Support", candidates: [{ dx: -78, label: "Billing", width: 128, selected: true }, { dx: 78, label: "Support", width: 128, selected: false }], result: "Billing", readout: "One team selected" },
  { x: 890, type: "MULTILABEL · PICK MANY", question: "Which topics?", hint: "Payments, Refund, Login", candidates: [{ dx: -104, label: "Payments", width: 98, selected: true }, { dx: 0, label: "Refund", width: 98, selected: true }, { dx: 104, label: "Login", width: 98, selected: false }], result: "Payments + Refund", readout: "Every matching topic selected" },
];

function Flow({ d, stage, orange = false }: { d: string; stage: number; orange?: boolean }) {
  return <g className={orange ? "tree-edge tree-edge-orange" : "tree-edge"}>
    <path d={d} className="tree-wire" />
    <path d={d} pathLength={1} className="tree-light tree-light-halo" style={{ "--flow-delay": `${stage * 1.35}s` } as CSSProperties} />
    <path d={d} pathLength={1} className="tree-light" style={{ "--flow-delay": `${stage * 1.35}s` } as CSSProperties} />
  </g>;
}

export function ArchitectureTree() {
  const [paused, setPaused] = useState(false);
  const id = useId();
  const scrollRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    const center = () => { el.scrollLeft = (el.scrollWidth - el.clientWidth) / 2; };
    const observer = new ResizeObserver(center);
    observer.observe(el);
    center();
    return () => observer.disconnect();
  }, []);
  return <figure className={`living-tree${paused ? " is-paused" : ""}`}>
    <div className="living-tree-header">
      <div><p className="tree-overline">SELFJEV / SHARED-PREFIX TREE</p><h3>Read once. Decide many.</h3></div>
      <button type="button" onClick={() => setPaused(!paused)} aria-label={paused ? "Play architecture animation" : "Pause architecture animation"} aria-pressed={paused}>
        {paused ? <Play size={14} /> : <Pause size={14} />}<span>{paused ? "Play" : "Pause"}</span>
      </button>
    </div>
    <div ref={scrollRef} className="living-tree-scroll" tabIndex={0} role="region" aria-label="Architecture diagram; scroll horizontally on small screens">
      <svg className="living-tree-svg" viewBox="0 0 1080 700" role="img" aria-labelledby={`${id}-title ${id}-desc`}>
        <title id={`${id}-title`}>SelfJev shared-prefix tree</title>
        <desc id={`${id}-desc`}>One customer message: I was charged twice. Please refund the duplicate payment. The shared document feeds three different question types. Binary: Refund requested? One Yes candidate is scored with a yes/no readout, returning true. Multiclass: Which team? Billing and Support compete; Billing is selected. Multilabel: Which topics? Payments, Refund and Login are scored independently; Payments and Refund are selected. These are illustrative answers, not live model predictions. Moving light illustrates shared computation and isolated candidate paths.</desc>
        <defs>
          <pattern id={`${id}-grid`} width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#b6ca91" strokeOpacity=".035" /></pattern>
          <linearGradient id={`${id}-panel`} x2="0" y2="1"><stop stopColor="#242b20"/><stop offset="1" stopColor="#171c16"/></linearGradient>
        </defs>
        <rect width="1080" height="700" fill={`url(#${id}-grid)`}/>
        {lanes.map(({x, candidates}) => <g key={`paths-${x}`}>
          <Flow d={`M540 144 C540 175 ${x} 160 ${x} 202`} stage={0} orange />
          {candidates.map(({dx}) => <g key={dx}>
            <Flow d={`M${x} 278 C${x} 308 ${x+dx} 294 ${x+dx} 328`} stage={1} />
            <Flow d={`M${x+dx} 378 C${x+dx} 410 ${x} 396 ${x} 428`} stage={2} />
          </g>)}
          <Flow d={`M${x} 496 C${x} 548 540 515 540 560`} stage={3}/>
        </g>)}
        <g className="tree-node tree-document">
          <rect x="300" y="16" width="480" height="128" rx="13" fill={`url(#${id}-panel)`}/>
          <g transform="translate(324 48)" className="tree-icon"><path d="M0 0H27L40 13V58H0ZM27 0V13H40M10 25H30M10 35H30M10 45H24"/></g>
          <text x="386" y="48" className="tree-node-title">One customer message</text>
          <text x="386" y="75" className="tree-example-quote">“I was charged twice. Please refund</text>
          <text x="386" y="96" className="tree-example-quote">the duplicate payment.”</text>
          <text x="386" y="125" className="tree-node-sub">Read once. Reused by all three questions.</text>
        </g>
        {lanes.map(({x,type,question,hint,candidates,result,readout})=><g key={x}>
          <g className="tree-node">
            <rect x={x-150} y="202" width="300" height="76" rx="11" fill={`url(#${id}-panel)`}/>
            <text x={x-126} y="222" className="tree-example-type">{type}</text>
            <text x={x-126} y="247" className="tree-node-title">{question}</text>
            <text x={x-126} y="267" className="tree-node-sub">{hint}</text>
          </g>
          {candidates.map(({dx,label,width,selected})=><g className={`tree-node tree-candidate tree-example-candidate${selected ? " is-selected" : ""}`} key={label}>
            <rect x={x+dx-width/2} y="328" width={width} height="50" rx="8"/>
            <text x={x+dx} y="350" textAnchor="middle">{label}</text>
            <text x={x+dx} y="367" textAnchor="middle" className="tree-candidate-status">{candidates.length === 1 ? "yes / no readout" : selected ? "✓ selected" : "not selected"}</text>
          </g>)}
          <g className="tree-node tree-example-result">
            <rect x={x-145} y="428" width="290" height="68" rx="10" fill={`url(#${id}-panel)`}/>
            <text x={x} y="457" className="tree-score-title" textAnchor="middle">{result}</text>
            <text x={x} y="479" className="tree-node-sub" textAnchor="middle">{readout}</text>
          </g>
        </g>)}
        <g className="tree-node tree-output">
          <rect x="285" y="560" width="510" height="124" rx="12" fill={`url(#${id}-panel)`}/>
          <text x="540" y="591" className="tree-node-title" textAnchor="middle">Three answers. Ready for your code.</text>
          <text x="323" y="619" className="tree-example-code">refund: <tspan className="tree-code-value">true</tspan></text>
          <text x="323" y="642" className="tree-example-code">team: <tspan className="tree-code-value">"billing"</tspan></text>
          <text x="323" y="665" className="tree-example-code">topics: <tspan className="tree-code-value">["payments", "refund"]</tspan></text>
        </g>
        <text x="40" y="610" className="tree-note">One shared message.</text><text x="40" y="631" className="tree-note">Different answer types.</text>
        <text x="830" y="610" className="tree-note">Probabilities also</text><text x="830" y="631" className="tree-note">returned by the API.</text>
      </svg>
    </div>
    <figcaption className="architecture-bottom"><span><i/>Illustrative answers · not a live model run<span className="tree-swipe">Swipe to explore →</span></span><Link href="/docs/architecture/">Inside the engine <ArrowUpRight size={15}/></Link></figcaption>
  </figure>;
}
