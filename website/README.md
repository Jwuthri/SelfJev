# SelfJev website

Next.js marketing, evidence explorer, and practical documentation. Independent of the Python server and the existing Zensical research notebook.

## Local development

From the repository root:

```bash
cd website
npm ci
npm run dev
```

Open http://127.0.0.1:3000. This runs Next.js with Fast Refresh: source edits appear automatically. If switching from the static preview, reload the browser once to connect to the development server. Node 22 is used for this project. No GPU, API credentials, or model downloads are required.

## Build and check

```bash
npm run check
npm run preview
```

`preview` serves the last static build and does **not** reload source changes; use `npm run dev` while editing. Both use port 3000, so stop one before starting the other.

`check` builds every static page (including TypeScript validation) and checks internal export links and source-report links. `out/` is the deployable static site. The build needs the whole repository: evidence is read from sibling `reports/` and `docs/experiments.md` at build time. Visitors receive only compact scores, not datasets or full prediction reports.

The site can be hosted on any static host. No Node process, GPU, database, or paid API is needed at runtime. For a subpath host, build with `NEXT_PUBLIC_BASE_PATH=/your-prefix` and serve `out/` under that prefix. The current GitHub Pages research notebook remains unchanged; this project does not alter its deployment workflow.

## Content and evidence

- `app/page.tsx`: marketing narrative and architecture diagram.
- `app/research/page.tsx`: experiment history and searchable benchmark explorer.
- `content/*.md`: ten task-oriented user guides.
- `lib/evidence.ts`: reads real JSON reports; latency medians exclude warm-up (`rep=0`). Each benchmark tab links to its own source report.
- `components/decision-tree.tsx`: illustrative examples, explicitly not live inference.
- `app/globals.css`: typography, dark instrument palette, responsive layouts, reduced-motion handling.

The homepage describes tasks in visitor language: text decisions and AI response review. Scores still come from the current TreeServer reports (95.7% and 93.1%). Dataset names, original-engine results, and raw run IDs live in the research page’s expandable methodology and experiment archive. Historic H100 speed belongs to archived Qwen3 and must not become a current-model claim. Hardware recommendations are estimates where no minimum was measured. CPU-only is not a supported server CLI mode.

AWS commands reflect the existing deployment helper. Runpod/GCP are manual guides, checked against provider documentation but not executed. No paid resources were provisioned to make the site.

## Validation

Production build, static-link audit, and browser checks of mobile/desktop layouts, example switching, benchmark selection and filtering, latency controls, mobile navigation, and code copying. See the repository journal for the completed check results.
