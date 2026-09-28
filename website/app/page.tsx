import Link from "next/link";
import {
  ArrowRight,
  ArrowUpRight,
  GitBranch,
  Fingerprint,
  Braces,
  Layers,
  Terminal,
} from "lucide-react";
import { DecisionTree } from "@/components/decision-tree";
import { Benchmarks } from "@/components/explorers";
import { HardwareExplorer } from "@/components/hardware-explorer";
import { CodeBlock } from "@/components/code-block";
import { headlines, leaderboard, hardwareLatencyData, JOURNAL } from "@/lib/evidence";
const sdk = `from selfjev import SelfJev, Noul, Choice

# Use the secret you set as SELFJEV_API_KEYS on your server.

client = SelfJev(
    base_url="http://localhost:8000",
    api_key="your-server-key",
)

result = client.system_one(
    state="I was charged twice. Please refund me.",
    questions={
        "refund": Noul("Does the customer want a refund?"),
        "team": Choice("Which team should handle this?", {
            "billing": "payments and refunds",
            "support": "technical support",
        }),
    },
)`;
export default function Home() {
  const h = headlines();
  const rows = leaderboard();
  const hardware = hardwareLatencyData();
  const featured = rows.filter(
    (r) =>
      r.current ||
      [
        "~typesafe/jev-latest",
        "lora_4b",
      ].includes(r.id),
  );
  return (
    <main id="main">
      <section className="hero wrap">
        <div className="hero-copy">
          <div className="eyebrow">
            <span className="orange-line" /> THE SELF-HOSTED DECISION MODEL{" "}
            <span className="version">v0.2</span>
          </div>
          <h1>
            Intelligence,
            <br />
            <span>decided.</span>
          </h1>
          <p className="hero-description">
            Turn context into decisions.
            <br />A small AI model that reads once, answers many,
            <br className="desktop-break" /> and runs on infrastructure you
            control.
          </p>
          <div className="hero-actions">
            <Link className="button primary" href="/docs/">
              Start building <ArrowUpRight size={17} />
            </Link>
            <Link className="text-link" href="/research/">
              Explore the research <ArrowRight size={16} />
            </Link>
          </div>
          <div className="hero-footnote">
            <span>Runs on one GPU</span>
            <i />
            <span>No text generation</span>
            <i />
            <span>Jev-compatible API</span>
          </div>
        </div>
        <DecisionTree />
      </section>
      <div className="metric-strip wrap">
        <a href={h.eval2.url}>
          <span className="metric-label">TEXT DECISIONS</span>
          <strong>
            {h.eval2.display}
            <small>%</small>
          </strong>
          <span>
            Matches expected answers in our tests <ArrowUpRight size={13} />
          </span>
        </a>
        <a href={h.llm.url}>
          <span className="metric-label">AI RESPONSE REVIEW</span>
          <strong>
            {h.llm.display}
            <small>%</small>
          </strong>
          <span>
            Checks quality, accuracy & safety <ArrowUpRight size={13} />
          </span>
        </a>
        <Link href="/#architecture">
          <span className="metric-label">READ YOUR TEXT ONCE</span>
          <strong>
            1<small> read</small>
          </strong>
          <span>
            Across every question in a request <ArrowRight size={13} />
          </span>
        </Link>
        <Link href="/docs/api/">
          <span className="metric-label">GENERATED TEXT</span>
          <strong>0</strong>
          <span>
            Answers your code can use <ArrowRight size={13} />
          </span>
        </Link>
      </div>
      <p className="metric-context wrap">Accuracy on our project’s test questions, not a guarantee for every use case. <Link href="/research/#test-guide">What did we test? ↗</Link></p>
      <section className="section wrap intro">
        <div className="section-kicker">01 / BUILT TO DECIDE</div>
        <div>
          <h2>
            Some things need an answer.
            <br />
            <span>Not another conversation.</span>
          </h2>
          <p className="section-description">
            Route a request. Check an agent’s work. Apply a policy. SelfJev
            turns your text and questions into structured decisions with
            probabilities—without waiting for a generated response.
          </p>
          <div className="feature-row">
            <article>
              <Braces />
              <h3>Four answer types.</h3>
              <p>
                Yes/no, pick one, rate a result, or select all that apply.
                Ready to use in your application.
              </p>
            </article>
            <article>
              <Fingerprint />
              <h3>Your data stays yours.</h3>
              <p>
                Run the model on your own GPU. Process sensitive text
                without sending it to an external model API.
              </p>
            </article>
            <article>
              <GitBranch />
              <h3>A familiar interface.</h3>
              <p>
                Already using Jev? Keep the same request format and point
                your application to your own server.
              </p>
            </article>
          </div>
        </div>
      </section>
      <section id="architecture" className="section architecture-section">
        <div className="wrap">
          <div className="section-kicker">02 / HOW IT WORKS</div>
          <div className="section-heading">
            <h2>
              One context.
              <br />
              <span>Every angle.</span>
            </h2>
            <p>
              A support message can raise several questions: what happened,
              who should handle it, and what to do next. SelfJev reads the
              message once and reuses that work for every answer.
            </p>
          </div>
          <div className="architecture-plate">
            <div className="arch-label">
              ONE MESSAGE <span>SEVERAL DECISIONS</span>
            </div>
            <div className="arch-flow">
              <div className="arch-root">
                <Layers size={30} />
                <strong>Your text</strong>
                <span>read once</span>
              </div>
              <div className="arch-connector" aria-hidden="true" />
              <div className="arch-questions">
                {["Needs a refund?", "Which team?", "How urgent?"].map((q, i) => (
                  <div className="arch-lane" key={q}>
                    <div className="arch-question">
                      <span>0{i + 1}</span>
                      {q}
                      <small>weigh the choices</small>
                    </div>
                    <div className="candidate-branches">
                      <span>A</span>
                      <span>B</span>
                      <span>C</span>
                    </div>
                    <div className="readout">
                      {["Yes", "Billing", "Normal"][i]}
                      <small>answer + probability</small>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="architecture-bottom">
              <span>
                <i />
                Illustrative answers. The same text informs each decision.
              </span>
              <Link href="/docs/architecture/">
                Inside the engine <ArrowUpRight size={15} />
              </Link>
            </div>
          </div>
          <div className="arch-notes">
            <p>
              <b>01. Give it context</b>A message, document, or AI response,
              together with the questions you need answered.
            </p>
            <p>
              <b>02. Ask several questions</b>Each question uses the same text,
              so the model avoids reading it from scratch each time.
            </p>
            <p>
              <b>03. Act on the answers</b>Get clear choices and probabilities
              to route, filter, or review in your own application.
            </p>
          </div>
        </div>
      </section>
      <section className="section wrap" id="benchmarks">
        <div className="section-kicker">03 / THE EVIDENCE</div>
        <div className="section-heading">
          <h2>
            Strong results.
            <br />
            <span>Receipts included.</span>
          </h2>
          <p>
            Can it choose the right answer from a piece of text? We tested
            yes/no decisions, choosing between options, and selecting every
            answer that applies.
          </p>
        </div>
        <Benchmarks rows={featured} compact />
        <div className="below-panel">
          <p>
            SelfJev approaches Jev’s accuracy on these tests and runs on your
            own infrastructure. The questions and expected answers were created
            and checked by AI; results on your own data may differ.
          </p>
          <Link className="text-link" href="/research/">
            How we tested it <ArrowRight size={16} />
          </Link>
        </div>
        <div className="research-insight">
          <span className="insight-index">↳</span>
          <div>
            <h3>The breakthrough was learning the right task.</h3>
            <p>
              Handling exceptions, weighing alternatives, and checking AI
              responses all needed targeted training. Improving those examples
              mattered more than simply making the model bigger.
            </p>
          </div>
          <a href={`${JOURNAL}/findings/`}>
            Read the findings <ArrowUpRight size={16} />
          </a>
        </div>
      </section>
      <section className="section speed-section" id="hardware">
        <div className="wrap speed-layout">
          <div>
            <div className="section-kicker">04 / THE SPEED STORY</div>
            <h2>
              Less repeated work.
              <br />
              <span>More decisions.</span>
            </h2>
            <p className="section-description">
              See how an earlier shared-text model ran on three self-hosting
              GPUs. Choose your input size and question count to compare the
              measured processing times.
            </p>
            <div className="speed-callout">
              <strong>
                {Math.round(hardware.find((point) => point.tokens === 8 && point.questions === 1)!.h100)}
                <span>ms</span>
              </strong>
              <p>
                Earlier Qwen3 tree · H100
                <br />
                Very short input · one question
              </p>
            </div>
            <a className="text-link" href={`${JOURNAL}/speed/`}>
              How we measured speed <ArrowUpRight size={16} />
            </a>
          </div>
          <HardwareExplorer data={hardware} />
        </div>
      </section>
      <section className="section wrap build-section">
        <div>
          <div className="section-kicker">05 / YOUR INFRASTRUCTURE</div>
          <h2>
            From a question
            <br />
            <span>to your first call.</span>
          </h2>
          <p className="section-description">
            A lightweight Python SDK. One GPU to serve. Docker and an AWS
            deployment command, with practical guides for Runpod and Google
            Cloud.
          </p>
          <div className="deploy-links">
            {[
              ["Quickstart", "/docs/"],
              ["Hardware & sizing", "/docs/hardware/"],
              ["AWS", "/docs/aws/"],
              ["Runpod", "/docs/runpod/"],
              ["Google Cloud", "/docs/gcp/"],
            ].map(([n, l]) => (
              <Link key={n} href={l}>
                {n}
                <ArrowUpRight size={15} />
              </Link>
            ))}
          </div>
        </div>
        <CodeBlock label="Python / your first decision" language="python" code={sdk} />
      </section>
      <section className="closing wrap">
        <span className="section-kicker">
          THE MODEL IS SMALL. THE NOTEBOOK IS OPEN.
        </span>
        <h2>
          Make the next decision
          <br />
          <span>on your terms.</span>
        </h2>
        <Link className="button primary" href="/docs/">
          <Terminal size={17} /> Self-host SelfJev <ArrowUpRight size={17} />
        </Link>
      </section>
    </main>
  );
}
