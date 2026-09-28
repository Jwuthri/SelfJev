import { notFound } from "next/navigation";
import { docPages } from "@/lib/docs";
import { DocPage } from "@/components/doc-page";
export function generateStaticParams() {
  return docPages
    .filter((p) => p.slug !== "quickstart")
    .map((p) => ({ slug: p.slug }));
}
export const dynamicParams = false;
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return {
    title: docPages.find((p) => p.slug === slug)?.title || "Documentation",
  };
}
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  if (!docPages.some((p) => p.slug === slug)) notFound();
  return <DocPage slug={slug} />;
}
