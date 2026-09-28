import Link from "next/link";
export default function NotFound() {
  return (
    <main id="main" className="wrap page-intro">
      <div className="eyebrow">404 / NO MATCH</div>
      <h1>This branch ends here.</h1>
      <p>The page could not be found.</p>
      <Link
        className="button primary"
        href="/"
        style={{ margin: "32px 0 80px" }}
      >
        Back to SelfJev →
      </Link>
    </main>
  );
}
