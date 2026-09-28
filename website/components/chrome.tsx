"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { ArrowUpRight, GitBranch, Github, Menu, X } from "lucide-react";
export function Header() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  return (
    <header className="header">
      <Link href="/" className="brand" aria-label="SelfJev home">
        <span className="brand-mark">
          <GitBranch size={19} />
        </span>
        selfjev<span className="brand-slash">/</span>
      </Link>
      <nav className={open ? "nav open" : "nav"} aria-label="Main navigation">
        <Link
          onClick={() => setOpen(false)}
          className={pathname === "/" ? "active" : ""}
          href="/"
        >
          Overview
        </Link>
        <Link onClick={() => setOpen(false)} href="/#architecture">
          How it works
        </Link>
        <Link
          onClick={() => setOpen(false)}
          className={pathname.startsWith("/research") ? "active" : ""}
          href="/research/"
        >
          Research
        </Link>
        <Link
          onClick={() => setOpen(false)}
          className={pathname.startsWith("/docs") ? "active" : ""}
          href="/docs/"
        >
          Docs
        </Link>
      </nav>
      <a className="github-link" href="https://github.com/Jwuthri/SelfJev">
        <Github size={17} />
        <span>GitHub</span>
        <ArrowUpRight size={14} />
      </a>
      <button
        className="mobile-menu"
        aria-label={open ? "Close navigation" : "Open navigation"}
        aria-expanded={open}
        onClick={() => setOpen(!open)}
      >
        {open ? <X /> : <Menu />}
      </button>
    </header>
  );
}
export function Footer() {
  return (
    <footer className="footer">
      <div>
        <Link className="brand" href="/">
          selfjev<span className="brand-slash">/</span>
        </Link>
        <p>Small model. Open notebook. Your infrastructure.</p>
      </div>
      <div className="footer-links">
        <Link href="/docs/">Documentation</Link>
        <Link href="/research/">Evidence</Link>
        <a href="https://jwuthri.github.io/SelfJev/">Lab notebook ↗</a>
        <a href="https://github.com/Jwuthri/SelfJev">GitHub ↗</a>
      </div>
      <span className="footnote">
        Independent research. Not affiliated with TypeSafe.
      </span>
    </footer>
  );
}
