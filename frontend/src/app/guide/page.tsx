"use client";

import * as React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
   ArrowLeft,
   Coffee,
   AlertCircle,
   Zap,
   Target,
   DollarSign,
   ChevronRight,
   Sparkles
} from "lucide-react";
import { BrutalistButton } from "@/components/ui/brutalist-button";

const FounderNote = ({ children, title }: { children: React.ReactNode; title: string }) => (
   <div className="bg-[#FFF9E6] border-l-4 border-black p-6 shadow-sm relative group">
      <div className="absolute -top-3 -left-2 bg-black text-white px-2 py-0.5 text-[8px] font-bold uppercase tracking-widest">Founder_Insight</div>
      <h4 className="font-display text-sm uppercase tracking-tight mb-2">{title}</h4>
      <div className="text-sm font-medium leading-relaxed italic opacity-80 whitespace-pre-wrap">{children}</div>
   </div>
);

export default function FounderGuidePage() {
   return (
      <div className="flex min-h-screen flex-col bg-[#F5F2EB] text-[#121212] selection:bg-[#BAE4F0] selection:text-black font-sans relative antialiased">

         <div className="fixed inset-0 pointer-events-none z-0 opacity-[0.03]">
            <div className="absolute inset-0 bg-[linear-gradient(to_right,#000_1px,transparent_1px),linear-gradient(to_bottom,#000_1px,transparent_1px)] bg-[size:40px_40px]" />
         </div>

         <nav className="border-b-4 border-black bg-white/95 backdrop-blur-sm p-6 flex justify-between items-center z-50 sticky top-0 shadow-sm">
            <Link href="/" className="font-display text-2xl tracking-tighter uppercase flex items-center gap-4 group">
               <div className="h-10 w-10 border-2 border-black flex items-center justify-center bg-black text-white group-hover:bg-[#FF6500] transition-all overflow-hidden relative">
                  <ArrowLeft className="h-5 w-5 relative z-10" />
                  <motion.div
                     className="absolute inset-x-0 bottom-0 top-full bg-[#FFD500] z-0"
                     whileHover={{ top: 0 }}
                     transition={{ duration: 0.2 }}
                  />
               </div>
               <span className="hidden sm:inline">RETURN TO OPS</span>
               <span className="sm:hidden">BACK</span>
            </Link>
            <div className="flex items-center gap-4">
               <span className="text-[10px] font-bold uppercase tracking-widest text-gray-400 hidden lg:block">Revision: Alpha_0.1</span>
               <div className="h-4 w-[2px] bg-black/10 hidden lg:block" />
               <div className="font-display text-xs uppercase tracking-widest px-4 py-2 border-2 border-black bg-[#BAE4F0] shadow-[4px_4px_0px_black] hidden sm:block">
                  FOUNDER_PLAYBOOK
               </div>
            </div>
         </nav>

         <main className="flex-1 relative z-10 py-16 lg:py-32 px-6 max-w-7xl mx-auto w-full space-y-32 lg:space-y-48">

            <header className="space-y-12">
               <div className="space-y-6">
                  <motion.div
                     initial={{ opacity: 0, x: -20 }}
                     animate={{ opacity: 1, x: 0 }}
                     className="flex items-center gap-3 text-[#0091B9]"
                  >
                     <Sparkles className="h-5 w-5" />
                     <span className="text-[10px] font-bold uppercase tracking-[0.4em]">Essential_Wisdom</span>
                  </motion.div>
                  <h1 className="font-display text-6xl md:text-[8rem] uppercase leading-[0.85] tracking-tighter">
                     The Real <br /> <span className="text-white" style={{ WebkitTextStroke: "2px #121212" }}>Talk</span> Guide
                  </h1>
               </div>

               <div className="max-w-4xl space-y-8">
                  <p className="text-2xl md:text-3xl font-medium leading-relaxed text-gray-800">
                     Founding is messy. Most guides are theoretical textbooks. This is the collection of things I wish someone had told me before I wrote line one of code.
                  </p>
               </div>
            </header>

            <div className="space-y-32 md:space-y-64">

               <section className="grid grid-cols-1 lg:grid-cols-12 gap-16 items-start">
                  <div className="lg:col-span-4 sticky top-40 space-y-8">
                     <div className="space-y-2">
                        <span className="text-4xl font-display text-black opacity-10">01</span>
                        <h2 className="font-display text-4xl uppercase tracking-tighter leading-none">
                           The Cold <br /> Start
                        </h2>
                     </div>
                     <div className="h-1 w-12 bg-black" />
                     <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#FF6500]">Phase: Day Zero</p>
                  </div>

                  <div className="lg:col-span-8 space-y-12">
                     <div className="bg-white border-2 border-black p-10 shadow-[8px_8px_0px_black] space-y-10 group transition-all hover:shadow-[12px_12px_0px_black]">
                        <div className="space-y-6">
                           <h3 className="text-2xl font-bold uppercase tracking-tight">How to find pre-product users</h3>
                           <p className="text-lg font-medium leading-relaxed opacity-70">
                              Don&apos;t build in a vacuum. Your first 10 users shouldn&apos;t find you—you should find them where they already hang out.
                           </p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                           <div className="space-y-4">
                              <h4 className="text-sm font-bold uppercase tracking-[0.1em] text-[#0091B9]">The Playbook:</h4>
                              <ul className="space-y-4 text-sm font-bold uppercase">
                                 <li className="flex gap-3"><ChevronRight className="h-4 w-4 shrink-0" /> Find 3 subreddits where the pain is mentioned.</li>
                                  <li className="flex gap-3"><ChevronRight className="h-4 w-4 shrink-0" /> DM 50 people asking for a &quot;Research Interview.&quot;</li>
                                 <li className="flex gap-3"><ChevronRight className="h-4 w-4 shrink-0" /> No pitching. Just listen to their workaround.</li>
                              </ul>
                           </div>
                           <FounderNote title="The Insider Truth">
                               &quot;If they aren&apos;t currently using a messy spreadsheet to solve the problem, they don&apos;t have the problem.&quot;
                           </FounderNote>
                        </div>
                     </div>
                  </div>
               </section>

               <section className="grid grid-cols-1 lg:grid-cols-12 gap-16 items-start">
                  <div className="lg:col-span-4 lg:order-last sticky top-40 space-y-8 lg:text-right">
                     <div className="space-y-2">
                        <span className="text-4xl font-display text-black opacity-10">02</span>
                        <h2 className="font-display text-4xl uppercase tracking-tighter leading-none">
                           The <br /> $100 Rule
                        </h2>
                     </div>
                     <div className="h-1 w-12 bg-black lg:ml-auto" />
                     <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#FF6500]">Metric: Economic Signal</p>
                  </div>

                  <div className="lg:col-span-8 space-y-12">
                     <div className="bg-[#BAE4F0] border-2 border-black p-10 shadow-[8px_8px_0px_black] space-y-10 relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-8 opacity-10">
                           <DollarSign className="h-24 w-24" />
                        </div>
                        <div className="space-y-6 relative z-10">
                           <h3 className="text-2xl font-bold uppercase tracking-tight">Validation Through Transaction</h3>
                           <p className="text-lg font-medium leading-relaxed">
                               Compliments are fake. Money is the only honest feedback. If they won&apos;t pay $100 for access today, they won&apos;t pay for it tomorrow either.
                           </p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
                           <div className="bg-white border-2 border-black p-6 space-y-4">
                              <p className="text-xs font-bold uppercase tracking-widest opacity-50">Signal Strength</p>
                              <div className="flex items-end gap-2 text-4xl font-display uppercase tracking-tighter">
                                 <span>$100.</span>
                                 <span className="text-xs text-[#0091B9] mb-1">Pre-Commit</span>
                              </div>
                              <p className="text-[10px] font-bold uppercase text-gray-400">If you get 3 of these, start building.</p>
                           </div>
                           <FounderNote title="Hard Reality">
                               &quot;A &apos;This is cool&apos; is a polite way of saying &apos;I&apos;m never going to use this.&apos; Demand skin in the game early.&quot;
                           </FounderNote>
                        </div>
                     </div>
                  </div>
               </section>

               <section className="grid grid-cols-1 lg:grid-cols-12 gap-16 items-start">
                  <div className="lg:col-span-4 sticky top-40 space-y-8">
                     <div className="space-y-2">
                        <span className="text-4xl font-display text-black opacity-10">03</span>
                        <h2 className="font-display text-4xl uppercase tracking-tighter leading-none">
                           Hire <br /> Yourself
                        </h2>
                     </div>
                     <div className="h-1 w-12 bg-black" />
                     <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#FF6500]">Focus: Capital Efficiency</p>
                  </div>

                  <div className="lg:col-span-8 space-y-12">
                     <div className="bg-white border-2 border-black p-10 shadow-[8px_8px_0px_black] space-y-10">
                        <div className="space-y-6">
                           <h3 className="text-2xl font-bold uppercase tracking-tight">Do the manual labor first</h3>
                           <p className="text-lg font-medium leading-relaxed opacity-70">
                               Before you automate it with code, do it manually for a single customer. If you can&apos;t solve it with a manual process, code won&apos;t save you.
                           </p>
                        </div>

                        <div className="space-y-8">
                           <div className="border-y-2 border-black/10 py-8 grid grid-cols-1 md:grid-cols-3 gap-8">
                              {[
                                 { label: "Phase One", title: "Manual Ops", icon: Coffee },
                                 { label: "Phase Two", title: "Scale Work", icon: Zap },
                                 { label: "Phase Three", title: "Full Code", icon: Target }
                              ].map((item, i) => (
                                 <div key={i} className="space-y-2">
                                    <item.icon className="h-5 w-5 text-[#0091B9]" />
                                    <p className="text-[10px] font-bold uppercase text-gray-400">{item.label}</p>
                                    <p className="text-sm font-bold uppercase tracking-tight">{item.title}</p>
                                 </div>
                              ))}
                           </div>
                           <FounderNote title="The Ghost Pattern">
                               &quot;Perform the &apos;Concierge&apos; service. Let them think it&apos;s software while you&apos;re behind the scenes doing the work. You&apos;ll learn more in 1 week of manual work than 1 month of coding.&quot;
                           </FounderNote>
                        </div>
                     </div>
                  </div>
               </section>

            </div>

            <section className="bg-black text-white border-4 border-black p-12 md:p-24 shadow-[20px_20px_0px_#FFD500] relative overflow-hidden text-center space-y-12 group">
               <div className="absolute top-0 left-0 w-full h-[1px] bg-white/20" />
               <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1px] h-full bg-white/20" />

               <div className="space-y-6 relative z-10">
                  <motion.div
                     animate={{ scale: [1, 1.1, 1] }}
                     transition={{ duration: 2, repeat: Infinity }}
                     className="inline-flex items-center gap-2 text-[#BAE4F0]"
                  >
                     <AlertCircle className="h-5 w-5" />
                     <span className="text-[10px] font-bold uppercase tracking-[0.4em]">Ready_To_Deploy</span>
                  </motion.div>
                  <h2 className="font-display text-5xl md:text-8xl uppercase tracking-tighter leading-none">
                     Stop Reading. <br /> <span className="text-[#FFD500] italic">Start Building.</span>
                  </h2>
                  <p className="text-xl font-bold uppercase opacity-60 max-w-xl mx-auto">
                     Theoretical knowledge has a half-life. Action is the only constant.
                  </p>
               </div>

               <div className="relative z-10 pt-8">
                  <Link href="/">
                     <BrutalistButton className="px-16 py-8 text-2xl md:text-4xl bg-[#FF6500] text-black font-display border-4 border-black shadow-[10px_10px_0px_white] uppercase tracking-tighter hover:bg-white hover:text-black hover:shadow-[10px_10px_0px_#FFD500] transition-all">
                        Execute Analysis
                     </BrutalistButton>
                  </Link>
               </div>
            </section>

            <footer className="pt-32 pb-16 flex flex-col md:flex-row justify-between items-end gap-12 border-t-2 border-black/10">
               <div className="space-y-8 w-full md:w-auto">
                  <div className="font-display text-4xl tracking-tighter uppercase leading-none">
                     <span>STARTUP_</span>
                     <span className="text-[#0091B9]">PLAYBOOK</span>
                  </div>
                  <div className="flex flex-wrap gap-12 text-[10px] font-bold uppercase tracking-[0.15em] text-gray-500">
                     <Link href="/" className="hover:text-black transition-colors">Analyst_Core</Link>
                     <Link href="/guide" className="hover:text-black transition-colors">Founder_Notes</Link>
                     <Link href="/privacy" className="hover:text-black transition-colors">Privacy_Dossier</Link>
                     <a href="mailto:ops@startupanalyst.io" className="hover:text-black transition-colors">Alert_Ops</a>
                  </div>
               </div>

               <div className="flex flex-col items-end gap-3 opacity-20">
                  <div className="flex gap-1">
                     {[1, 2, 3, 4, 5, 6, 7, 8].map(i => <div key={i} className="h-8 w-2 bg-black" />)}
                  </div>
                  <p className="text-[10px] font-bold uppercase tracking-widest leading-none">Stable_Build_2026</p>
               </div>
            </footer>

         </main>
      </div>
   );
}
