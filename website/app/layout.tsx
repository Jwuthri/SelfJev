import type { Metadata } from "next";
import "@fontsource-variable/dm-sans";
import "@fontsource-variable/jetbrains-mono";
import "./globals.css";
import { Header, Footer } from "@/components/chrome";
export const metadata: Metadata = {
  title: {
    default: "SelfJev — Intelligence, decided.",
    template: "%s · SelfJev",
  },
  description:
    "A self-hosted 4B decision model. Typed answers, shared-prefix inference, and an open record of every experiment.",
  icons: { icon: `${process.env.NEXT_PUBLIC_BASE_PATH || ""}/icon.svg` },
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-scroll-behavior="smooth">
      <body>
        <a href="#main" className="skip-link">
          Skip to content
        </a>
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  );
}
