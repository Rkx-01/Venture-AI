import type { Metadata } from "next";
import { Space_Grotesk, Dela_Gothic_One, Space_Mono, Ranchers, Plus_Jakarta_Sans } from "next/font/google";
import "@/styles/globals.css";
import { cn } from "@/lib/utils";

import { ThemeProvider } from "@/components/shared/ThemeProvider";
import { QueryProvider } from "@/providers/query-provider";
import { GlobalLoader } from "@/components/ui/global-loader";
import { Toaster } from "@/components/ui/sonner";

import { CustomCursor } from "@/components/ui/custom-cursor";

const sans = Space_Grotesk({ 
  subsets: ['latin'], 
  variable: '--font-sans',
  weight: ['300', '400', '500', '600', '700']
});
const display = Dela_Gothic_One({ 
  weight: "400", 
  subsets: ["latin"], 
  variable: '--font-display' 
});
const mono = Space_Mono({
  weight: ["400", "700"],
  subsets: ["latin"],
  variable: "--font-mono"
});
const ranchers = Ranchers({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-ranchers"
});
const jakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-jakarta",
  weight: ["200", "300", "400", "500", "600", "700", "800"]
});

export const metadata: Metadata = {
  title: "AI Startup Analyst | Premium Intelligence",
  description: "Production-level AI SaaS platform for analyzing startup ideas and market opportunities.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning className={cn(
      "font-sans", 
      sans.variable, 
      display.variable, 
      mono.variable, 
      ranchers.variable, 
      jakarta.variable
    )}>
      <body className={cn(
        "min-h-screen bg-background font-sans antialiased",
        sans.variable,
        display.variable,
        mono.variable,
        ranchers.variable,
        jakarta.variable
      )}>
        <CustomCursor />
        <QueryProvider>
          <GlobalLoader />
          <ThemeProvider
            attribute="class"
            defaultTheme="light"
            enableSystem={false}
            disableTransitionOnChange
          >
            <main className="relative flex min-h-screen flex-col">
              {children}
            </main>
            <Toaster position="bottom-right" />
          </ThemeProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
