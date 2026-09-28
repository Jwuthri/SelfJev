"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
export function DocsLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const current = pathname.replace(/\/$/, "") === href.replace(/\/$/, "");
  return (
    <Link href={href} aria-current={current ? "page" : undefined}>
      {children}
    </Link>
  );
}
