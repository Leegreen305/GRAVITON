import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { Sidebar } from "../components/Sidebar";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const jetbrains = JetBrains_Mono({
  variable: "--font-jetbrains",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "GRAVITON — Spacetime Engineering Simulator",
  description: "Exotic propulsion and spacetime engineering dashboard powered by peer-reviewed physics.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrains.variable} h-full antialiased`}>
      <body className="min-h-full bg-[#0a0a14]">
        <Sidebar />
        <main className="ml-[220px] min-h-screen p-8">
          {children}
        </main>
      </body>
    </html>
  );
}
