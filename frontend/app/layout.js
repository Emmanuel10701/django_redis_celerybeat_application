// This is the root layout file for a Next.js 13+ application.
// It sets global styles, fonts, and metadata configuration
// and wraps all pages in a consistent HTML structure.

import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

// Importing Geist Sans and Geist Mono fonts with CSS variables
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Site-wide metadata for SEO
export const metadata = {
  title: "AI Blog Generation Platform",
  description: "An intelligent platform for scheduling and generating blogs using OpenAI and Django.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
