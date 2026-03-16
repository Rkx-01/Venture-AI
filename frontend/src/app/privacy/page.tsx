"use client";

import * as React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { 
  ArrowLeft, 
  ShieldCheck, 
  Lock, 
  Database, 
  Eye, 
  FileText,
  Scale
} from "lucide-react";

export default function PrivacyPolicyPage() {
  return (
    <div className="flex min-h-screen flex-col bg-[#F5F2EB] text-[#121212] selection:bg-[#BAE4F0] selection:text-black font-sans relative antialiased">
      
      {}
      <div className="fixed inset-0 pointer-events-none z-0 opacity-[0.03]">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#000_1px,transparent_1px),linear-gradient(to_bottom,#000_1px,transparent_1px)] bg-[size:32px_32px]" />
      </div>

      {}
      <nav className="border-b-4 border-black bg-white/95 backdrop-blur-sm p-6 flex justify-between items-center z-50 sticky top-0 shadow-sm">
        <Link href="/" className="font-display text-2xl tracking-tighter uppercase flex items-center gap-4 group">
          <div className="h-10 w-10 border-2 border-black flex items-center justify-center bg-black text-white group-hover:bg-[#0091B9] transition-all">
            <ArrowLeft className="h-5 w-5" />
          </div>
          <span>RETURN_HOME</span>
        </Link>
        <div className="flex items-center gap-4">
           <div className="font-display text-[10px] uppercase tracking-widest px-4 py-2 bg-[#FFD500] border-2 border-black shadow-[4px_4px_0px_black]">
             PRIVACY_DOSSIER_v1.0
           </div>
        </div>
      </nav>

      <main className="flex-1 relative z-10 py-24 px-6 max-w-5xl mx-auto w-full space-y-24">
        
        {}
        <header className="space-y-8 border-b-4 border-black pb-16">
           <div className="space-y-4">
              <div className="inline-flex items-center gap-2 text-[#0091B9]">
                <ShieldCheck className="h-6 w-6" />
                <span className="text-[10px] font-bold uppercase tracking-[0.4em]">Data_Governance_Protocol</span>
              </div>
              <h1 className="font-display text-6xl md:text-8xl uppercase leading-[0.85] tracking-tighter">
                Privacy <br /> <span className="text-white" style={{ WebkitTextStroke: "2px #121212" }}>is Integrity.</span>
              </h1>
           </div>
           <p className="text-xl font-medium leading-relaxed text-gray-700 max-w-3xl">
              We treat your startup data with the same intensity as code. This dossier outlines how we process, store, and protect your intellectual property.
           </p>
        </header>

        {}
        <div className="space-y-20">
           
           {}
           <section className="grid grid-cols-1 md:grid-cols-12 gap-12">
              <div className="md:col-span-4 space-y-4">
                 <div className="flex items-center gap-3">
                   <Database className="h-5 w-5 text-[#FF6500]" />
                   <h2 className="font-display text-2xl uppercase tracking-tight">Data Collection</h2>
                 </div>
                 <div className="h-1 w-12 bg-black" />
              </div>
              <div className="md:col-span-8 bg-white border-2 border-black p-8 shadow-[8px_8px_0px_black] space-y-6">
                 <h3 className="text-xl font-bold uppercase tracking-tight">What we capture</h3>
                 <p className="text-base leading-relaxed opacity-80">
                    We collect the startup descriptions you input for analysis. This data is transmitted to our AI engine (Google Gemini) to generate your Intelligence Reports. 
                 </p>
                 <div className="bg-[#F5F2EB] p-6 border-l-4 border-[#0091B9] text-xs font-bold uppercase tracking-widest leading-loose">
                    [NOTICE] WE DO NOT SELL YOUR STRATEGIC DATA TO THIRD-PARTY BROKERS. YOUR IDEAS REMAIN YOUR INTELLECTUAL PROPERTY.
                 </div>
              </div>
           </section>

           {}
           <section className="grid grid-cols-1 md:grid-cols-12 gap-12">
              <div className="md:col-span-4 space-y-4">
                 <div className="flex items-center gap-3">
                   <Lock className="h-5 w-5 text-[#0091B9]" />
                   <h2 className="font-display text-2xl uppercase tracking-tight">Processing</h2>
                 </div>
                 <div className="h-1 w-12 bg-black" />
              </div>
              <div className="md:col-span-8 bg-white border-2 border-black p-8 shadow-[8px_8px_0px_black] space-y-6">
                 <h3 className="text-xl font-bold uppercase tracking-tight">AI Analysis Pipeline</h3>
                 <p className="text-base leading-relaxed opacity-80">
                    Your inputs are processed using advanced Large Language Models. We use secure API tunnels to ensure that your data is encrypted in transit. We do not use your strategic inputs to "train" our global models.
                 </p>
              </div>
           </section>

           {}
           <section className="grid grid-cols-1 md:grid-cols-12 gap-12">
              <div className="md:col-span-4 space-y-4">
                 <div className="flex items-center gap-3">
                   <Scale className="h-5 w-5 text-[#FFD500]" />
                   <h2 className="font-display text-2xl uppercase tracking-tight">Governance</h2>
                 </div>
                 <div className="h-1 w-12 bg-black" />
              </div>
              <div className="md:col-span-8 bg-[#0E0E0E] text-white border-2 border-black p-8 shadow-[8px_8px_0px_#FF6500] space-y-8">
                 <div className="space-y-4">
                    <h3 className="text-xl font-display uppercase tracking-tight text-[#FFD500]">Your Sovereignty</h3>
                    <p className="text-sm leading-relaxed opacity-80">
                       You have the right to request the deletion of your analysis session data. We maintain minimal logging to improve system performance and prevent abuse.
                    </p>
                 </div>
                 <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 border border-white/20 space-y-1">
                       <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Protocol</p>
                       <p className="text-xs font-bold uppercase tracking-tighter">Encrypted_Transit</p>
                    </div>
                    <div className="p-4 border border-white/20 space-y-1">
                       <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Retention</p>
                       <p className="text-xs font-bold uppercase tracking-tighter">Session_Ephemeral</p>
                    </div>
                 </div>
              </div>
           </section>

        </div>

        {}
        <section className="bg-white border-4 border-black p-12 md:p-16 shadow-[12px_12px_0px_black] text-center space-y-8">
           <h2 className="font-display text-4xl uppercase tracking-tighter italic">Questions_on_Protocol?</h2>
           <p className="text-lg font-medium opacity-60">
              For security disclosures or legal inquiries, contact our Intelligence Unit.
           </p>
           <div className="pt-4">
              <Link href="mailto:privacy@startupanalyst.io" className="inline-block px-12 py-6 bg-black text-white font-display text-xl uppercase tracking-tighter border-2 border-black hover:bg-[#FF6500] transition-all shadow-[6px_6px_0px_#0091B9]">
                Contact Security
              </Link>
           </div>
        </section>

        {}
        <footer className="pt-24 pb-12 border-t-2 border-black flex justify-between items-center opacity-40">
           <div className="font-display text-xl tracking-tighter uppercase">
             <span>VENTURE</span>
             <span className="text-[#0091B9]">INTEL</span>
           </div>
           <p className="text-[10px] font-bold uppercase tracking-[0.3em]">Revision_Sync_2.1</p>
        </footer>

      </main>
    </div>
  );
}
