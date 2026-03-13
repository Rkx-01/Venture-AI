"use client";

import { Suspense } from "react";
import { useRouter } from "next/navigation";
import { cn } from "@/lib/utils";
import { BrutalistButton } from "@/components/ui/brutalist-button";
import {
  Building2,
  Target,
  Wrench,
  DollarSign,
  ArrowLeft,
  LineChart,
  Swords
} from "lucide-react";

import { useState } from "react";
import * as Tabs from "@radix-ui/react-tabs";
import { useAnalysisStore } from "@/store/analysisStore";

function ResultContent() {
  const router = useRouter();
  const result = useAnalysisStore((s) => s.ideaAnalysis);
  const resetAnalysis = useAnalysisStore((s) => s.resetAnalysis);
  const loading = false; // No longer loading from storage asynchronously

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center font-bold uppercase tracking-widest bg-[#F5F2EB] text-[#121212]">Loading Report Data...</div>;
  }

  if (!result) {
    return (
      <div className="min-h-screen flex flex-col gap-4 items-center justify-center bg-[#F5F2EB] text-[#121212] p-6">
        <div className="border-4 border-black bg-[#FF6500] text-black shadow-[8px_8px_0px_0px_#000] p-8 font-bold uppercase">No intelligence report found or session expired.</div>
        <BrutalistButton onClick={() => router.push("/")} className="bg-[#0091B9] text-white border-4 border-black px-6 py-3 font-bold uppercase">Return to Core</BrutalistButton>
      </div>
    );
  }

  const {
    idea_summary = "No summary provided",
    target_users = "No target users identified",
    market_insights = { tam: "", sam: "", som: "", trends: "" },
    competitors = [],
    swot = { strengths: [], weaknesses: [], opportunities: [], threats: [] },
    startup_score = 0,
    investment_recommendation = "No recommendation generated",
    report = "No report generated",
    market_entry_difficulty = { level: "N/A", reasons: [] }
  } = result;

  const TabTrigger = ({ value, label, icon: Icon }: { value: string, label: string, icon: React.ElementType }) => (
    <Tabs.Trigger
      value={value}
      className="flex-1 flex items-center justify-center gap-2 py-4 px-2 font-bold uppercase tracking-wider text-sm border-r-4 border-primary last:border-r-0 hover:bg-muted data-[state=active]:bg-[#0091B9] data-[state=active]:text-white transition-colors"
    >
      <Icon className="h-4 w-4 hidden md:block" />
      <span className="hidden sm:inline">{label}</span>
    </Tabs.Trigger>
  );

  return (
    <div className="min-h-screen bg-[#F5F2EB] text-[#121212] p-4 md:p-12 mb-24">
      <div className="mx-auto max-w-6xl">

        {/* Header */}
        <header className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-6 border-b-4 border-black pb-6">
          <div>
            <div className="inline-block bg-[#BAE4F0] text-black px-2 py-1 font-bold text-xs uppercase tracking-widest mb-4 border-4 border-black shadow-[4px_4px_0px_0px_#000]">
              Intelligence Report Generated
            </div>
            <h1 className="font-display text-5xl md:text-7xl uppercase leading-none text-[#121212]">
              Analysis <br />
              <span className="text-[#FF6500] text-shadow-brutal" style={{ textShadow: "4px 4px 0px #000" }}>
                Results
              </span>
            </h1>
          </div>
          <BrutalistButton
            onClick={() => {
              resetAnalysis();
              router.push("/");
            }}
            className="group font-bold uppercase border-4 border-black px-6 py-3 bg-white text-black hover:bg-[#BAE4F0] transition-colors shadow-[4px_4px_0px_0px_#000] flex items-center gap-2 w-fit"
          >
            <ArrowLeft className="h-5 w-5 group-hover:-translate-x-1 transition-transform" />
            Analyze New Idea
          </BrutalistButton>
        </header>

        <Tabs.Root defaultValue="overview" className="flex flex-col w-full">
          <Tabs.List className="flex border-4 border-black bg-white text-black shadow-[8px_8px_0px_#000] mb-8 overflow-x-auto">
            <TabTrigger value="overview" label="Overview" icon={Wrench} />
            <TabTrigger value="market" label="Insights" icon={LineChart} />
            <TabTrigger value="competitors" label="Competitors" icon={Swords} />
            <TabTrigger value="swot" label="SWOT" icon={Target} />
            <TabTrigger value="score" label="Score" icon={DollarSign} />
            <TabTrigger value="report" label="Report" icon={Building2} />
          </Tabs.List>

          {/* Tab 1: Idea Overview */}
          <Tabs.Content value="overview" className="focus:outline-none space-y-6">
            <div className="border-4 border-black bg-white text-black shadow-[4px_4px_0px_#BAE4F0] p-6 md:p-8">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b-2 border-[#121212]/20 pb-4">
                <h2 className="font-display text-3xl uppercase">Market Entry Difficulty</h2>
                <div className={cn(
                  "px-4 py-2 border-4 border-black font-bold uppercase shadow-[4px_4px_0px_#000] text-lg",
                  market_entry_difficulty?.level === "Low" ? "bg-[#4ADE80]" :
                    market_entry_difficulty?.level === "Medium" ? "bg-[#FFD500]" :
                      "bg-[#FF6500] text-white"
                )}>
                  Level: {market_entry_difficulty?.level || "N/A"}
                </div>
              </div>
              <div className="space-y-4">
                <h3 className="text-xs font-bold uppercase tracking-widest text-[#0091B9]">Analysis Factors:</h3>
                <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {(market_entry_difficulty?.reasons || []).map((reason: string, i: number) => (
                    <li key={i} className="flex gap-3 items-start border-l-4 border-black pl-4 py-2 bg-[#F5F2EB]/50">
                      <span className="font-medium leading-relaxed">{reason}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="border-4 border-black bg-white text-black shadow-[4px_4px_0px_#BAE4F0] p-6 md:p-8">
              <h2 className="font-display text-3xl uppercase mb-4 border-b-2 border-[#121212]/20 pb-2">Idea Summary</h2>
              <p className="text-lg md:text-xl font-medium leading-relaxed border-l-4 border-[#0091B9] pl-4">
                {idea_summary}
              </p>
            </div>
            <div className="border-4 border-black bg-[#004E9B] text-white shadow-[4px_4px_0px_#BAE4F0] p-6 md:p-8 relative overflow-hidden">
              <h2 className="font-display text-3xl uppercase mb-4">Target Users</h2>
              <p className="text-lg md:text-xl font-medium leading-relaxed font-sans text-white/90">
                {target_users}
              </p>
            </div>
          </Tabs.Content>

          {/* Tab 2: Market Insights */}
          <Tabs.Content value="market" className="focus:outline-none space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                { title: "Total Addressable Market (India)", value: market_insights?.tam, bg: "bg-[#BAE4F0]", text: "text-black", shadow: "shadow-[4px_4px_0px_#0091B9]" },
                { title: "Serviceable Available Market (India)", value: market_insights?.sam, bg: "bg-[#004E9B]", text: "text-white", shadow: "shadow-[4px_4px_0px_#0091B9]" },
                { title: "Serviceable Obtainable Market (India)", value: market_insights?.som, bg: "bg-[#0091B9]", text: "text-white", shadow: "shadow-[4px_4px_0px_#BAE4F0]" }
              ].map((item, i) => (
                <div key={i} className={cn("border-4 border-black p-6 flex flex-col items-center text-center overflow-hidden", item.bg, item.text, item.shadow)}>
                  <div className="flex items-center justify-center w-full mb-4 border-b-2 border-black/20 pb-2">
                    <h3 className="font-[900] uppercase tracking-tighter text-sm">
                      {item.title}
                    </h3>
                  </div>
                  <div className="font-display text-xl md:text-2xl leading-snug break-words w-full">
                    {item.value || "N/A"}
                  </div>
                </div>
              ))}
            </div>
            <div className="border-4 border-black bg-white text-black shadow-[4px_4px_0px_#BAE4F0] p-6 md:p-8 mt-6">
              <h2 className="font-display text-3xl uppercase mb-4 border-b-2 border-black/20 pb-2">Indian Market Trends & Growth</h2>
              <p className="text-lg font-medium leading-relaxed">
                {market_insights?.trends || "No trends identified."}
              </p>
            </div>
          </Tabs.Content>

          {/* Tab 3: Competitor Landscape */}
          <Tabs.Content value="competitors" className="focus:outline-none">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {competitors && competitors.length > 0 ? competitors.map((comp: any, idx: number) => (
                <div key={idx} className="border-4 border-black bg-white text-black shadow-[4px_4px_0px_#BAE4F0] p-6 flex flex-col">
                  <h3 className="font-display text-2xl uppercase mb-2 bg-[#0091B9] inline-block px-2 text-white">{comp.name}</h3>
                  <p className="font-medium text-sm mb-4 flex-grow opacity-80">{comp.description}</p>
                  <div className="mt-auto space-y-3 pt-4 border-t-2 border-black/10">
                    <div>
                      <span className="text-xs font-bold uppercase tracking-widest text-[#0091B9] block mb-1">Strength</span>
                      <span className="font-medium text-sm">{comp.strengths}</span>
                    </div>
                    <div>
                      <span className="text-xs font-bold uppercase tracking-widest text-[#FF6500] block mb-1">Weakness</span>
                      <span className="font-medium text-sm">{comp.weaknesses}</span>
                    </div>
                  </div>
                </div>
              )) : (
                <div className="col-span-full border-4 border-black bg-white text-black p-6 font-bold uppercase text-center">No competitors identified</div>
              )}
            </div>
          </Tabs.Content>

          {/* Tab 4: SWOT Analysis */}
          <Tabs.Content value="swot" className="focus:outline-none">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-[#004E9B] border-4 border-black p-6 md:p-8 shadow-[8px_8px_0px_#000]">
              {/* Strengths */}
              <div className="border-4 border-black bg-white text-black p-6 shadow-[4px_4px_0px_#0091B9]">
                <h3 className="font-display text-2xl uppercase mb-4 text-[#0091B9] border-b-2 border-black/10 pb-2">Strengths</h3>
                <ul className="list-disc pl-5 space-y-2 font-medium">
                  {(swot?.strengths || []).map((s: string, i: number) => <li key={i}>{s}</li>)}
                </ul>
              </div>
              {/* Weaknesses */}
              <div className="border-4 border-black bg-white text-black p-6 shadow-[4px_4px_0px_#FF6500]">
                <h3 className="font-display text-2xl uppercase mb-4 text-[#FF6500] border-b-2 border-black/10 pb-2">Weaknesses</h3>
                <ul className="list-disc pl-5 space-y-2 font-medium">
                  {(swot?.weaknesses || []).map((w: string, i: number) => <li key={i}>{w}</li>)}
                </ul>
              </div>
              {/* Opportunities */}
              <div className="border-4 border-black bg-[#BAE4F0] text-black p-6 shadow-[4px_4px_0px_#004E9B]">
                <h3 className="font-display text-2xl uppercase mb-4 text-[#004E9B] border-b-2 border-black/10 pb-2">Opportunities</h3>
                <ul className="list-disc pl-5 space-y-2 font-medium">
                  {(swot?.opportunities || []).map((o: string, i: number) => <li key={i}>{o}</li>)}
                </ul>
              </div>
              {/* Threats */}
              <div className="border-4 border-black bg-[#004E9B] text-white p-6 shadow-[4px_4px_0px_#FFD500]">
                <h3 className="font-display text-2xl uppercase mb-4 text-[#FFD500] border-b-2 border-black/10 pb-2">Threats</h3>
                <ul className="list-disc pl-5 space-y-2 font-medium">
                  {(swot?.threats || []).map((t: string, i: number) => <li key={i}>{t}</li>)}
                </ul>
              </div>
            </div>
          </Tabs.Content>

          {/* Tab 5: Startup Score */}
          <Tabs.Content value="score" className="focus:outline-none flex justify-center mt-12 mb-12">
            <div className="max-w-md w-full border-4 border-black bg-[#FF6500] shadow-[8px_8px_0px_#BAE4F0] p-12 flex flex-col items-center justify-center text-center transform -rotate-1 hover:rotate-0 transition-transform">
              <h2 className="font-bold uppercase tracking-widest mb-4 bg-white text-black px-4 py-2 border-2 border-black shadow-brutal">Overall Proprietary Score</h2>
              <div className="font-display text-9xl mt-2 text-white">
                {startup_score}
              </div>
              <div className="text-sm font-bold text-white uppercase mt-6 opacity-90 border-t-4 border-black pt-4 w-full">Out of 10</div>
              <p className="font-medium text-sm mt-4 text-white opacity-100 max-w-xs leading-relaxed">
                Evaluated dynamically based on real-time market saturation, competitive threats, execution friction, and projected TAM runway.
              </p>
            </div>
          </Tabs.Content>

          {/* Tab 6: Full Report */}
          <Tabs.Content value="report" className="focus:outline-none space-y-6">
            <div className="border-4 border-black bg-white text-black shadow-[4px_4px_0px_#0091B9] p-6 md:p-8">
              <h2 className="font-display text-3xl uppercase mb-4 text-[#004E9B] border-b-2 border-black/20 pb-2">Investment Recommendation</h2>
              <p className="text-lg md:text-xl font-medium leading-relaxed border-l-4 border-[#0091B9] pl-4">
                {investment_recommendation}
              </p>
            </div>
            <div className="border-4 border-black bg-[#BAE4F0] text-black shadow-[4px_4px_0px_#FF6500] p-6 md:p-8 md:p-8">
              <h2 className="font-display text-3xl uppercase mb-6 text-[#004E9B]">Executive Intelligence Report</h2>
              <div className="font-medium whitespace-pre-wrap leading-loose">
                {report}
              </div>
            </div>
          </Tabs.Content>
        </Tabs.Root>

        {/* Faux Footer */}
        <div className="mt-12 pt-6 border-t-4 border-black flex flex-col sm:flex-row justify-between items-center text-xs font-bold uppercase tracking-widest gap-4">
          <div className="flex gap-4">
            <span className="bg-[#BAE4F0] text-black px-2 py-1 font-bold">DATA VERIFIED</span>
            <span className="border-4 border-black px-2 py-1">v3.0 CORTEX</span>
          </div>
          <p className="opacity-50">VENTURE AI // CONFIDENTIAL</p>
        </div>

      </div>
    </div>
  );
}

export default function ResultPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-background p-6 flex items-center justify-center font-bold uppercase uppercase tracking-widest">Loading Results...</div>}>
      <ResultContent />
    </Suspense>
  );
}

