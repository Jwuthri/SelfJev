"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { ArrowRight, ArrowUpRight, Check, RotateCcw, ScanLine } from "lucide-react";

// Authored examples to explain shared context. No inference or measured scores.
const examples = [
  {
    name: "Customer support",
    source: "Customer message",
    before: "I was ",
    highlight: "charged twice",
    after: " for my subscription. Please refund the duplicate payment.",
    questions: [
      { key: "refund", type: "Yes / no", title: "Refund requested?", answer: "Yes", options: ["Yes", "No"], selected: ["Yes"], reason: "“Please refund” gives the first question a direct answer.", value: "true" },
      { key: "team", type: "Pick one", title: "Who should handle it?", answer: "Billing", options: ["Billing", "Support"], selected: ["Billing"], reason: "The duplicate payment points to Billing. Both teams are considered against the same message.", value: '"billing"' },
      { key: "topics", type: "Pick many", title: "Which topics apply?", answer: "2 matches", options: ["Payments", "Refund", "Login"], selected: ["Payments", "Refund"], reason: "Payments and Refund both apply. Each topic is checked independently against the shared context.", value: '["payments", "refund"]' },
    ],
  },
  {
    name: "AI response review",
    source: "An AI response to review",
    before: "Question: What is 2 + 2? Answer: ",
    highlight: "2 + 2 = 5.",
    after: " You can verify this with basic arithmetic.",
    questions: [
      { key: "correct", type: "Yes / no", title: "Is the answer correct?", answer: "No", options: ["Yes", "No"], selected: ["No"], reason: "The answer is 4. The stated result is incorrect, even though the response sounds confident.", value: "false" },
      { key: "action", type: "Pick one", title: "What happens next?", answer: "Revise", options: ["Accept", "Revise"], selected: ["Revise"], reason: "An incorrect answer needs revision. The review reuses the question and response already read.", value: '"revise"' },
      { key: "issues", type: "Pick many", title: "Which issues apply?", answer: "2 matches", options: ["Arithmetic", "Overconfidence", "Off-topic"], selected: ["Arithmetic", "Overconfidence"], reason: "The arithmetic is wrong and the verification claim is confident. The response still addresses the question.", value: '["arithmetic", "overconfidence"]' },
    ],
  },
];

export function ArchitectureTree() {
  const [exampleIndex, setExampleIndex] = useState(0);
  const [activeQuestion, setActiveQuestion] = useState(0);
  const [revealed, setRevealed] = useState(3);
  const timers = useRef<ReturnType<typeof setTimeout>[]>([]);
  const example = examples[exampleIndex];
  const running = revealed < 3;

  function clearTimers() {
    timers.current.forEach(clearTimeout);
    timers.current = [];
  }
  useEffect(() => () => timers.current.forEach(clearTimeout), []);

  function replay() {
    clearTimers();
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setRevealed(3);
      return;
    }
    setRevealed(0);
    timers.current = [1, 2, 3].map((step) => setTimeout(() => setRevealed(step), 450 + step * 350));
  }
  function chooseExample(index: number) {
    clearTimers();
    setExampleIndex(index);
    setActiveQuestion(0);
    setRevealed(3);
  }

  return (
    <figure className={`context-demo${running ? " is-running" : ""}`} aria-label="Interactive shared-context example">
      <div className="context-demo-toolbar">
        <div className="context-demo-tabs" role="group" aria-label="Choose an example">
          {examples.map(({ name }, index) => <button type="button" key={name} aria-pressed={exampleIndex === index} onClick={() => chooseExample(index)}>{name}</button>)}
        </div>
        <button type="button" className="context-replay" onClick={replay} disabled={running}><RotateCcw size={13} /> Replay flow</button>
      </div>
      <div className="context-demo-body">
        <div className="context-source">
          <div className="context-demo-label"><span>01</span> ONE SHARED INPUT</div>
          <div className="context-source-caption"><ScanLine size={16} />{example.source}</div>
          <blockquote>{example.before}<mark>{example.highlight}</mark>{example.after}</blockquote>
          <div className="context-read-status"><span className="context-status-dot" />{running ? "Reading once, sharing the context…" : "Read once. Available to every question."}</div>
          <div className="context-reason" aria-live="polite"><span>FOLLOW THE DECISION</span><p key={`${exampleIndex}-${activeQuestion}`}>{example.questions[activeQuestion].reason}</p></div>
        </div>
        <div className="context-questions">
          <div className="context-demo-label"><span>02</span> ASK FROM EVERY ANGLE</div>
          <div className="context-question-list">
            {example.questions.map((question, index) => (
              <button type="button" className={`context-question${activeQuestion === index ? " is-active" : ""}${index < revealed ? " is-revealed" : ""}`} aria-pressed={activeQuestion === index} key={question.key} onClick={() => setActiveQuestion(index)}>
                <span className="context-question-top"><span className="context-question-type">{question.type}</span><span className="context-answer">{index < revealed ? <><Check size={12} />{question.answer}</> : "···"}</span></span>
                <span className="context-question-title">{question.title}<ArrowUpRight size={15} /></span>
                <span className="context-options">{question.options.map((option) => <span key={option} className={question.selected.includes(option) && index < revealed ? "is-selected" : ""}>{option}</span>)}</span>
              </button>
            ))}
          </div>
          <div className="context-reason context-reason-mobile" aria-live="polite"><span>FOLLOW THE DECISION</span><p key={`${exampleIndex}-${activeQuestion}`}>{example.questions[activeQuestion].reason}</p></div>
        </div>
      </div>
      <div className="context-output">
        <div className="context-demo-label"><span>03</span> READY FOR YOUR CODE <ArrowRight size={14} /></div>
        <div className="context-output-values" aria-label="Illustrative output, not the full API response">
          {example.questions.map((question, index) => <code key={question.key}><span>{question.key}</span><b>{index < revealed ? question.value : "…"}</b></code>)}
        </div>
      </div>
      <figcaption className="context-demo-footer"><span>Interactive illustration · no live inference. The API also returns probabilities.</span><Link href="/docs/architecture/">Inside the engine <ArrowUpRight size={14} /></Link></figcaption>
    </figure>
  );
}
