import { ArrowUpRight, Database, Download, GitBranch } from "lucide-react";
import { HF_RELEASES } from "@/lib/releases";

export function ReleaseLinks() {
  return <section className="release-panel" aria-label="Hugging Face releases">
    <div className="release-heading"><div><span className="tree-overline">AVAILABLE ON HUGGING FACE</span><h3>Get the weights. Explore the evidence.</h3></div><a href={HF_RELEASES.profile}>Jwuthrich <ArrowUpRight size={14}/></a></div>
    <div className="release-grid">
      <a href={HF_RELEASES.adapter}><GitBranch size={20}/><span className="release-kind">DEFAULT / VISION + TEXT</span><h4>SelfJev-4B <ArrowUpRight size={17}/></h4><p>The image-and-text adapter used by the native tree engine. Downloaded automatically by SelfJev.</p><span className="release-action">Get the model ↗</span></a>
      <a href={HF_RELEASES.merged}><Download size={20}/><span className="release-kind">MERGED WEIGHTS</span><h4>Ready for vLLM <ArrowUpRight size={17}/></h4><p>The complete vision release with tokenizer and configuration. vLLM serves text; images need the native engine.</p><span className="release-action">Get merged weights ↗</span></a>
      <a href={HF_RELEASES.dataset}><Database size={20}/><span className="release-kind">EVALUATION DATASET</span><h4>Decision Bench <ArrowUpRight size={17}/></h4><p>3,657 questions across text decisions, AI response review, and record reasoning.</p><span className="release-action">Explore the dataset ↗</span></a>
    </div>
    <div className="release-quant">
      <div><span className="release-kind">SMALL GPUS / QUANTIZED</span><h4>Run it on an 8 GB card</h4><p>The same model with bitsandbytes weights, scored on all 3,657 Decision Bench questions on an A10G capped at 7.2 GiB.</p></div>
      <table>
        <thead><tr><th>Build</th><th>Decision Bench</th><th>eval2</th><th>GPU memory, 8K text</th><th></th></tr></thead>
        <tbody>
          <tr><td>bf16 (full)</td><td>95.9%</td><td>96.1%</td><td>9.7 GiB</td><td>24 GB card</td></tr>
          <tr><td>8-bit</td><td>95.3%</td><td>95.2%</td><td>5.9 GiB</td><td><a href={HF_RELEASES.quant8}>Get 8-bit ↗</a></td></tr>
          <tr><td>4-bit (NF4)</td><td>95.0%</td><td>94.7%</td><td>4.5 GiB</td><td><a href={HF_RELEASES.quant4}>Get 4-bit ↗</a></td></tr>
        </tbody>
      </table>
    </div>
    <div className="release-legacy">Looking for the previous model? <a href={HF_RELEASES.textOnly}>Text-only release <ArrowUpRight size={14}/></a></div>
  </section>;
}
