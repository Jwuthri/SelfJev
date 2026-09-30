import { ArrowUpRight } from "lucide-react";
import { CodeBlock } from "@/components/code-block";
import { REPO } from "@/lib/evidence";

const IMAGE_API = `${REPO}/blob/master/docs/api.md#request`;
const REPORTS = `${REPO}/blob/master/reports/images_2026-09-29`;
const imageSdk = `from pathlib import Path
from selfjev import SelfJev, Choice

# Uses your SELFJEV_API_KEY.
client = SelfJev(
    base_url="http://localhost:8000",
)

result = client.system_one(
    state=[Path("cat.jpg")],
    questions={
        "breed": Choice(
            "What breed is it?",
            {
                "persian": "a Persian cat",
                "siamese": "a Siamese cat",
                "other": "another breed",
            },
        ),
    },
)`;

// Recorded medians: reports/images_2026-09-29/timing.txt (L40S, warm).
const timings = [
  { label: "Text · 1 question", ms: 136 },
  { label: "Image · 1 question", ms: 163 },
  { label: "Image · 5 questions", ms: 167 },
];
// Accuracy from each report's 100 test predictions.
// No images_v1 results; the dataset catalog is not a training manifest.
const results = [
  { label: "Bare Qwen3.5-4B", detail: "Base model", score: "73%", report: "base_pets100" },
  { label: "SelfJev-4B", detail: "No image training", score: "78%", report: "selfjev_4b_pets100" },
  { label: "SelfJev + image fine-tune", detail: "Fine-tuned on images", score: "90%", report: "pets_ft_pets100" },
];

export function ImageFeature() {
  return (
    <section className="section wrap image-section" id="images" aria-labelledby="images-title">
      <div className="section-kicker">NEW / IMAGES</div>
      <div className="section-heading">
        <h2 id="images-title">One photo.<br /><span>More answers.</span></h2>
        <p>SelfJev now takes images, too. Ask about a photo and get choices and probabilities through the same API. Image input is a SelfJev extension: Jev accepts text, not images.</p>
      </div>
      <div className="image-feature-grid">
        <div className="image-code">
          <CodeBlock code={imageSdk} label="Python / Images" language="python" />
          <p>Pass a <code>Path</code>, image bytes, or a PIL image. Over HTTP, use a base64 <code>data:image/…</code> URL as <code>state</code>, or a list of text and image parts.</p>
          <a className="text-link" href={IMAGE_API}>Image input reference <ArrowUpRight size={15} /></a>
        </div>
        <div className="image-explainer">
          <span className="tree-overline">SAME TREE. A VISUAL ROOT.</span>
          <h3>See it once.<br />Ask away.</h3>
          <p>Qwen3.5’s own frozen vision encoder processes the image once at the root. Every question and option branches from that shared work.</p>
          <dl className="image-timings">
            {timings.map(({ label, ms }) => (
              <div key={label}>
                <dt>{label}</dt><dd>{ms}<small> ms</small></dd>
                <span className="image-timing-track" aria-hidden="true"><i style={{ width: `${ms / 167 * 100}%` }} /></span>
              </div>
            ))}
          </dl>
          <p className="image-timing-takeaway">Five questions, almost the same wait.</p>
          <p className="image-measurement">Median warm request times on one NVIDIA L40S, measured over 20 photos. The one-question image request is yes/no; five questions mix answer types. Model loading and network time are excluded. Your images and hardware will affect latency.</p>
          <a className="text-link" href={`${REPORTS}/timing.txt`}>Read the timing record <ArrowUpRight size={15} /></a>
        </div>
      </div>
      <div className="image-study">
        <div className="image-study-heading">
          <div><span className="tree-overline">EARLY RESULTS / WIP </span><h3>Teach it what to look for.</h3></div>
          <p>Fine-tune on your own photos with <code>selfjev finetune</code> or <code>/v1/fine_tuning/jobs</code>. Training rows accept images as <code>state</code>, too.</p>
        </div>
        <div className="image-results">
          {results.map(({ label, detail, score, report }) => (
            <a key={report} href={`${REPORTS}/${report}/report.json`}>
              <span>{label}<ArrowUpRight size={14} /></span>
              <strong>{score}</strong><small>{detail}</small>
            </a>
          ))}
        </div>
        <div className="image-study-note">
          <p>Training and evaluation are ongoing on broader data.</p>
          <a className="text-link" href={`${REPO}/blob/master/docs/image_datasets.md`}>Find image training data <ArrowUpRight size={15} /></a>
        </div>
      </div>
    </section>
  );
}
