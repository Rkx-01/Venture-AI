"use client";

import * as React from "react";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { Sparkles, BrainCircuit } from "lucide-react";
import { BrutalistButton } from "@/components/ui/brutalist-button";
import { Textarea } from "@/components/ui/textarea";
import { InteractiveWavesBackground } from "@/components/ui/interactive-waves-background";
import { toast } from "sonner";

export default function LandingPage() {
  const router = useRouter();
  const [idea, setIdea] = useState("");

  const handleEvaluate = () => {
    if (!idea || idea.trim().length === 0) return;

    // Pass the idea encoding it cleanly through URL parameters
    // In a more complex app, we might use Zustand, but 
    // passing via URL is simple, stateless, and shareable.
    const encoded = encodeURIComponent(idea.trim());
    router.push(`/evaluate?q=${encoded}`);
  };

  return (
    <div className="flex min-h-screen flex-col bg-[#F5F2EB] text-[#121212] selection:bg-[#BAE4F0] selection:text-black overflow-hidden">

      {/* Brutalist Top Nav */}
      <nav className="border-b-4 border-black bg-[#F5F2EB] p-4 flex justify-between items-center z-50">
        <div className="font-display text-2xl uppercase flex items-center gap-2 text-[#121212]">
          <span>VENTURE</span>
          <div className="h-6 w-6 bg-[#0091B9] border-2 border-black shadow-[2px_2px_0px_0px_#09090B]"></div>
          <span>AI</span>
        </div>
      </nav>

      {/* Interactive Background */}
      <InteractiveWavesBackground
        lineColor="rgba(0, 78, 155, 0.1)"
        backgroundColor="#F5F2EB"
        waveSpeedX={0.01}
        waveSpeedY={0.005}
        waveAmpX={30}
        waveAmpY={15}
        friction={0.93}
        tension={0.006}
        xGap={15}
        yGap={35}
      />

      {/* Hero Section */}
      <main className="flex-1 flex flex-col relative py-12">

        <div className="mx-auto w-full max-w-7xl px-6 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center relative z-10 mb-[120px]">
          {/* Left Side: 7 Columns */}
          <div className="col-span-1 lg:col-span-7 space-y-8">
            <div className="space-y-4">
              <button
                onClick={() => toast.success("SYSTEM READY: Neural engine analyzing market signals.")}
                className="inline-block bg-[#0091B9] text-white px-3 py-1 border-2 border-black font-bold text-sm uppercase tracking-widest shadow-brutal mb-4 active:translate-x-1 active:translate-y-1 active:shadow-none transition-all"
              >
                System v2.0
              </button>

              <h1 className="font-display text-5xl sm:text-7xl lg:text-8xl leading-[0.9] text-[#121212] uppercase relative">
                <span className="block hover:animate-glitch">Evaluate</span>
                <span className="block hover:animate-glitch">Your Startup</span>
                <span className="block hover:animate-glitch text-[#FF6500] text-shadow-brutal" style={{ textShadow: "4px 4px 0px #000" }}>Idea</span>
              </h1>

              <p className="text-xl font-medium max-w-xl text-[#121212] mt-6 border-l-4 border-[#0091B9] pl-4">
                Drop your raw startup concept into the machine. Our neural engine will extract the market fit, competitor threats, and revenue logic in seconds.
              </p>
            </div>

            <div className="space-y-4 w-full max-w-2xl bg-[#004E9B] border-4 border-black p-6 shadow-[8px_8px_0px_0px_#000]">
              <label htmlFor="idea-input" className="font-display uppercase text-lg flex items-center gap-2 text-white">
                <BrainCircuit className="h-5 w-5 text-[#FFD500]" />
                Data Input
              </label>
              <Textarea
                id="idea-input"
                value={idea}
                onChange={(e) => setIdea(e.target.value)}
                placeholder="Describe your startup idea. E.g., 'A B2B SaaS platform that automates international tax compliance for small e-commerce stores...'"
                className="min-h-[160px] text-lg p-4 font-sans border-4 border-black focus-visible:ring-0 focus-visible:ring-offset-0 focus:border-[#FFD500] shadow-inner bg-white text-black"
              />
              <BrutalistButton
                className="w-full text-xl py-6 bg-[#0091B9] text-white border-4 border-black hover:bg-[#FF6500] transition-colors"
                disabled={!idea.trim()}
                onClick={handleEvaluate}
              >
                Evaluate Idea
              </BrutalistButton>
            </div>
          </div>

          {/* Right Side: 5 Columns */}
          <div className="col-span-1 lg:col-span-5 hidden lg:block">
            <motion.div
              className="relative w-full aspect-square bg-[#0091B9] border-4 border-black shadow-[16px_16px_0px_0px_#000] p-8 flex flex-col justify-between"
              animate={{
                y: ["-10px", "10px", "-10px"],
              }}
              transition={{
                duration: 6,
                ease: "easeInOut",
                repeat: Infinity,
              }}
            >
              <div className="flex justify-between items-start">
                <div className="font-display text-4xl text-white">ANALYSIS<br />MODULE</div>
                <Sparkles className="h-12 w-12 text-[#FFD500] fill-[#FFD500] stroke-black stroke-2" />
              </div>

              <div className="space-y-4">
                <div className="h-8 w-full bg-[#121212] border-2 border-black relative overflow-hidden">
                  <div className="absolute left-0 top-0 bottom-0 bg-[#FF6500] w-[85%] border-r-2 border-black" />
                </div>
                <div className="h-8 w-full bg-[#121212] border-2 border-black relative overflow-hidden">
                  <div className="absolute left-0 top-0 bottom-0 bg-[#BAE4F0] w-[42%] border-r-2 border-black" />
                </div>
                <div className="h-8 w-full bg-[#121212] border-2 border-black relative overflow-hidden">
                  <div className="absolute left-0 top-0 bottom-0 bg-[#004E9B] w-[60%] border-r-2 border-black" />
                </div>
              </div>

              <div className="font-bold border-t-4 border-black pt-4 flex justify-between items-center text-sm uppercase text-white">
                <span>Status: Optimal</span>
                <span className="bg-[#BAE4F0] text-black px-2 py-1">Ready</span>
              </div>

              <div
                className="absolute -bottom-6 -left-6 bg-[#FFD500] border-2 border-black text-black font-display p-2 rotate-[-12deg] shadow-brutal text-center cursor-help hover:scale-110 transition-transform"
                onClick={() => toast.info("Data integrity verified. No manual input required.")}
              >
                NO BS.<br />JUST DATA.
              </div>
            </motion.div>
          </div>
        </div>

        {/* SECTION 1 — HOW THE SYSTEM WORKS */}
        <section id="how-it-works" className="mx-auto w-full max-w-7xl px-6 mb-[120px] relative z-10 scroll-mt-20">
          <h2 className="text-[48px] font-[800] text-black mb-12 uppercase leading-none font-sans">
            HOW THE SYSTEM WORKS
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { step: "01", title: "INPUT IDEA", text: "Describe your startup concept. The AI engine parses market signals, competitors, and revenue logic." },
              { step: "02", title: "AI ANALYSIS", text: "Our neural system evaluates market size, competitor density, and product viability." },
              { step: "03", title: "INTELLIGENCE REPORT", text: "Receive a structured startup intelligence report with SWOT, evaluation matrix, and scoring." }
            ].map((item, i) => (
              <div key={i} className="bg-white border-[3px] border-black shadow-[6px_6px_0px_black] p-6 space-y-4">
                <div className="inline-block bg-[#0091B9] text-white px-3 py-1 border-[3px] border-black font-bold text-sm uppercase tracking-widest">
                  STEP {item.step}
                </div>
                <h3 className="text-2xl font-[900] text-black uppercase">{item.title}</h3>
                <p className="text-lg font-medium text-[#121212]">{item.text}</p>
              </div>
            ))}
          </div>
        </section>

        {/* SECTION 2 — WHAT THE AI ANALYZES */}
        <section id="ai-capabilities" className="mx-auto w-full max-w-7xl px-6 mb-[120px] relative z-10 scroll-mt-20">
          <h2 className="text-[48px] font-[800] text-black mb-12 uppercase leading-none font-sans">
            WHAT THE AI ANALYZES
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { title: "Market Insights", desc: "TAM, SAM, SOM and growth trends analysis." },
              { title: "Competitor Landscape", desc: "Detailed breakdown of direct and indirect threats." },
              { title: "Revenue Logic", desc: "Monetization strategies and unit economics check." },
              { title: "SWOT Analysis", desc: "Deep dive into strengths, weaknesses, and shifts." },
              { title: "Startup Score", desc: "Proprietary algorithm benchmark against industry data." },
              { title: "Evaluation Matrix", desc: "Multi-dimensional performance overview." }
            ].map((item, i) => (
              <div key={i} className="bg-[#0091B9] border-[3px] border-black shadow-[6px_6px_0px_black] p-6 text-white group hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-[8px_8px_0px_black] transition-all">
                <div className="mb-4">
                  <BrainCircuit className="h-10 w-10 text-[#FFD500]" />
                </div>
                <h3 className="text-xl font-[900] mb-2 uppercase">{item.title}</h3>
                <p className="text-sm font-medium opacity-90">{item.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* SECTION 3 — SAMPLE INTELLIGENCE REPORT */}
        <section id="report-preview" className="mx-auto w-full max-w-7xl px-6 mb-[120px] relative z-10 scroll-mt-20">
          <h2 className="text-[48px] font-[800] text-black mb-12 uppercase leading-none font-sans">
            INTELLIGENCE REPORT PREVIEW
          </h2>
          <div className="bg-[#004E9B] border-[3px] border-black shadow-[12px_12px_0px_black] p-8 md:p-12 overflow-hidden">
            <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
              <div className="md:col-span-8 space-y-6">
                <div className="bg-white border-[3px] border-black p-6 shadow-[6px_6px_0px_black]">
                  <h4 className="font-display text-xl mb-4 border-b-2 border-black pb-2">IDEA SUMMARY</h4>
                  <div className="space-y-4">
                    <div className="h-4 w-full bg-[#F5F2EB] border-2 border-black" />
                    <div className="h-4 w-[90%] bg-[#F5F2EB] border-2 border-black" />
                    <div className="h-4 w-[95%] bg-[#F5F2EB] border-2 border-black" />
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-[#FFD500] border-[3px] border-black p-6 shadow-[6px_6px_0px_black]">
                    <h4 className="font-display text-xl mb-4 text-black uppercase">MARKET</h4>
                    <div className="h-12 w-full bg-black border-2 border-black relative">
                      <div className="absolute inset-y-0 left-0 bg-[#0091B9] w-[75%] border-r-2 border-black" />
                    </div>
                  </div>
                  <div className="bg-[#BAE4F0] border-[3px] border-black p-6 shadow-[6px_6px_0px_black]">
                    <h4 className="font-display text-xl mb-4 text-black uppercase">SWOT</h4>
                    <div className="grid grid-cols-2 gap-2">
                      <div className="h-6 bg-green-400 border-2 border-black" />
                      <div className="h-6 bg-red-400 border-2 border-black" />
                    </div>
                  </div>
                </div>
              </div>
              <div className="md:col-span-4 flex flex-col gap-6">
                <div className="bg-[#FF6500] border-[3px] border-black p-6 shadow-[6px_6px_0px_black] flex-1 flex flex-col justify-center items-center text-center text-white">
                  <div className="text-6xl font-[900] mb-2">84</div>
                  <div className="font-display text-xl uppercase">STARTUP SCORE</div>
                </div>
                <div className="bg-white border-[3px] border-black p-6 shadow-[6px_6px_0px_black]">
                  <h4 className="font-display text-sm mb-2 opacity-60 uppercase">COMPETITORS</h4>
                  <div className="space-y-2">
                    <div className="h-3 bg-slate-200 border border-black" />
                    <div className="h-3 bg-slate-200 border border-black" />
                    <div className="h-3 bg-slate-200 border border-black" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 4 — WHY FOUNDERS USE THIS */}
        <section id="founder-validation" className="mx-auto w-full max-w-7xl px-6 mb-[120px] relative z-10 scroll-mt-20">
          <h2 className="text-[48px] font-[800] text-black mb-12 uppercase leading-none font-sans">
            WHY FOUNDERS USE THIS SYSTEM
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { title: "NO BS. JUST DATA", text: "Instant startup intelligence without guesswork." },
              { title: "MARKET VALIDATION", text: "Understand if your idea actually has demand." },
              { title: "COMPETITOR INSIGHTS", text: "Identify threats before you launch." }
            ].map((item, i) => (
              <div key={i} className="bg-white border-[3px] border-black shadow-[6px_6px_0px_black] p-8 text-center flex flex-col justify-center min-h-[200px]">
                <h3 className="text-2xl font-[900] mb-3 uppercase leading-tight">{item.title}</h3>
                <p className="text-lg font-medium text-[#121212]">{item.text}</p>
              </div>
            ))}
          </div>
        </section>

        {/* SECTION 5 — FINAL CALL TO ACTION */}
        <section className="mx-auto w-full max-w-7xl px-6 mb-[120px] relative z-10 text-center">
          <div className="bg-[#0091B9] border-[4px] border-black p-12 md:p-20 shadow-[12px_12px_0px_black] text-white">
            <h2 className="text-5xl md:text-7xl font-[400] mb-6 uppercase">
              READY TO TEST YOUR STARTUP IDEA?
            </h2>
            <p className="text-xl md:text-2xl font-medium mb-10 max-w-2xl mx-auto opacity-90">
              "Drop your concept into the machine and get a full intelligence report."
            </p>
            <BrutalistButton
              className="px-12 py-8 text-2xl bg-[#FF6500] hover:bg-[#FF8C69] text-white border-[3px] border-black shadow-[4px_4px_0px_black] transition-all transform hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-[6px_6px_0px_black]"
              onClick={() => {
                const input = document.getElementById('idea-input');
                if (input) {
                  input.scrollIntoView({ behavior: 'smooth', block: 'center' });
                  input.focus();
                }
              }}
            >
              ANALYZE YOUR IDEA
            </BrutalistButton>
          </div>
        </section>
      </main>

      {/* PROFESSIONAL SAAS FOOTER */}
      <footer className="w-full bg-[#0E0E0E] text-white border-t-[3px] border-black pt-[80px] pb-[60px] relative z-20">
        <div className="mx-auto max-w-[1200px] px-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">

            {/* Column 1: Product Information */}
            <div className="space-y-6">
              <div className="font-display text-2xl font-[400] uppercase flex items-center gap-2">
                <span>AI STARTUP ANALYST</span>
              </div>
              <p className="text-[#B9B9B9] text-sm leading-relaxed max-w-[280px]">
                An AI-powered intelligence engine that evaluates startup ideas using market signals, competitor data, and strategic frameworks.
              </p>
              <div className="inline-block bg-[#1A8AA5] text-white px-3 py-1 border-2 border-black font-bold text-xs uppercase tracking-widest shadow-[2px_2px_0px_#000]">
                SYSTEM V2.0
              </div>
            </div>

            {/* Column 2: Platform Links */}
            <div className="space-y-6">
              <h4 className="text-[14px] font-[700] uppercase tracking-widest text-[#B9B9B9] border-b border-[#1F1F1F] pb-2">PLATFORM</h4>
              <ul className="flex flex-col gap-[10px]">
                {[
                  { name: 'Analyze Idea', id: 'idea-input' },
                  { name: 'How It Works', id: 'how-it-works' },
                  { name: 'Intelligence Report', id: 'report-preview' },
                  { name: 'Startup Score System', id: 'founder-validation' }
                ].map((link) => (
                  <li key={link.name}>
                    <button
                      onClick={() => {
                        document.getElementById(link.id)?.scrollIntoView({ behavior: 'smooth' });
                      }}
                      className="text-[#B9B9B9] hover:text-white text-sm font-medium transition-all hover:underline underline-offset-4 flex items-center group"
                    >
                      <span className="group-hover:translate-x-1 transition-transform">{link.name}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </div>

            {/* Column 3: Resources */}
            <div className="space-y-6">
              <h4 className="text-[14px] font-[700] uppercase tracking-widest text-[#B9B9B9] border-b border-[#1F1F1F] pb-2">RESOURCES</h4>
              <ul className="flex flex-col gap-[10px]">
                {[
                  { name: 'Join Community', action: () => toast.info("Discord Community opening next week! Stay tuned.") },
                  { name: 'Market Updates', action: () => toast.info("Newsletter system initializing. Check back soon!") },
                  { name: 'Founder Guide', id: 'how-it-works' },
                  { name: 'Contact Us', mail: 'mailto:founders@startupanalyst.io' }
                ].map((item) => (
                  <li key={item.name}>
                    {item.action ? (
                      <button
                        onClick={item.action}
                        className="text-[#B9B9B9] hover:text-white text-sm font-medium transition-all hover:underline underline-offset-4 flex items-center group text-left"
                      >
                        <span className="group-hover:translate-x-1 transition-transform">{item.name}</span>
                      </button>
                    ) : item.name === 'Founder Guide' ? (
                      <Link
                        href="/guide"
                        className="text-[#B9B9B9] hover:text-white text-sm font-medium transition-all hover:underline underline-offset-4 flex items-center group text-left"
                      >
                        <span className="group-hover:translate-x-1 transition-transform">{item.name}</span>
                      </Link>
                    ) : (
                      <a
                        href={item.mail}
                        className="text-[#B9B9B9] hover:text-white text-sm font-medium transition-all hover:underline underline-offset-4 flex items-center group"
                      >
                        <span className="group-hover:translate-x-1 transition-transform">{item.name}</span>
                      </a>
                    )}
                  </li>
                ))}
              </ul>
            </div>

            {/* Column 4: System Status */}
            <div className="space-y-6">
              <h4 className="text-[14px] font-[700] uppercase tracking-widest text-[#B9B9B9] border-b border-[#1F1F1F] pb-2">SYSTEM STATUS</h4>
              <motion.div
                whileHover={{ y: -2 }}
                className="bg-[#141414] border-[3px] border-black shadow-[5px_5px_0px_black] p-4 space-y-3"
              >
                <div className="flex items-center justify-between text-xs font-bold uppercase tracking-widest">
                  <span className="text-[#B9B9B9]">Status</span>
                  <div className="flex items-center gap-2 text-white">
                    <div className="h-2 w-2 rounded-full bg-[#4ADE80] animate-pulse shadow-[0_0_8px_#4ADE80]" />
                    ONLINE
                  </div>
                </div>
                <div className="flex items-center justify-between text-xs font-bold uppercase tracking-widest">
                  <span className="text-[#B9B9B9]">Engine</span>
                  <span className="text-white">AI ANALYSIS CORE</span>
                </div>
                <div className="flex items-center justify-between text-xs font-bold uppercase tracking-widest">
                  <span className="text-[#B9B9B9]">Version</span>
                  <span className="text-white">V2.0</span>
                </div>
              </motion.div>
            </div>
          </div>

          {/* BOTTOM FOOTER BAR */}
          <div className="border-t-2 border-[#1F1F1F] pt-8 flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="text-[#B9B9B9] text-xs font-medium">
              © 2026 AI Startup Analyst. Developed for high-growth founders.
            </div>
            <div className="flex items-center gap-8">
              <Link
                href="/privacy"
                className="text-[#B9B9B9] hover:text-white text-xs font-bold uppercase tracking-widest transition-colors hover:underline"
              >
                Privacy Policy
              </Link>
              <button
                onClick={() => toast.info(`Terms of Service is being finalized by our legal engine.`)}
                className="text-[#B9B9B9] hover:text-white text-xs font-bold uppercase tracking-widest transition-colors hover:underline"
              >
                Terms
              </button>
              <a
                href="https://github.com/rkx01/ai-startup-analyst"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[#B9B9B9] hover:text-white text-xs font-bold uppercase tracking-widest transition-colors hover:underline"
              >
                Github
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
