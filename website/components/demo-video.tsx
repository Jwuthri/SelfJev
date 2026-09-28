"use client";

import { useEffect, useRef } from "react";

// Muted, plays only while on screen, never on its own for visitors who prefer reduced motion (they get the controls).
export function DemoVideo({ src, poster, label }: { src: string; poster: string; label: string }) {
  const ref = useRef<HTMLVideoElement>(null);
  useEffect(() => {
    const video = ref.current;
    if (!video || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const seen = new IntersectionObserver(([e]) => (e.isIntersecting ? video.play().catch(() => {}) : video.pause()), { threshold: 0.35 });
    seen.observe(video);
    return () => seen.disconnect();
  }, []);
  return <video ref={ref} className="demo-player" src={src} poster={poster} aria-label={label} muted loop playsInline controls preload="metadata" />;
}
