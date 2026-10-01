import fs from "node:fs";
import path from "node:path";
export const docPages = [
  {
    slug: "quickstart",
    title: "Quickstart",
    group: "GET STARTED",
    description: "Your first self-hosted decision.",
  },
  {
    slug: "hardware",
    title: "Hardware & sizing",
    group: "GET STARTED",
    description: "GPU, CPU, memory, and what is actually tested.",
  },
  {
    slug: "comparison",
    title: "Compared with open models",
    group: "GET STARTED",
    description: "Nine open decision models, one GPU, the same requests.",
  },
  {
    slug: "api",
    title: "API reference",
    group: "BUILD",
    description: "Requests, typed answers, authentication, and errors.",
  },
  {
    slug: "architecture",
    title: "How the model works",
    group: "BUILD",
    description: "Inside the shared-prefix decision tree.",
  },
  {
    slug: "finetuning",
    title: "Fine-tuning",
    group: "BUILD",
    description: "Adapt the decision model to your data.",
  },
  {
    slug: "docker",
    title: "Docker",
    group: "DEPLOY",
    description: "Run the service on a GPU machine you control.",
  },
  {
    slug: "ollama",
    title: "Ollama",
    group: "DEPLOY",
    description: "Run the decisions API on a laptop or CPU box, no GPU.",
  },
  {
    slug: "aws",
    title: "AWS",
    group: "DEPLOY",
    description: "Provision and manage a dedicated GPU endpoint.",
  },
  {
    slug: "runpod",
    title: "Runpod",
    group: "DEPLOY",
    description: "Set up a GPU Pod and expose the decisions API.",
  },
  {
    slug: "gcp",
    title: "Google Cloud",
    group: "DEPLOY",
    description: "Serve on a GPU-backed Compute Engine VM.",
  },
  {
    slug: "operations",
    title: "Operations",
    group: "DEPLOY",
    description: "Health, queues, request limits, and troubleshooting.",
  },
];
export function docContent(slug: string) {
  return fs.readFileSync(
    path.join(process.cwd(), "content", `${slug}.md`),
    "utf8",
  );
}
