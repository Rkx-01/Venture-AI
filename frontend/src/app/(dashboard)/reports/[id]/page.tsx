"use client";

import * as React from "react";
import { useRouter, useParams } from "next/navigation";
import {
    FileText, ArrowLeft, Download, Copy, FileDown, Share2, Calendar, User, ExternalLink, Zap, CheckCircle2, AlertCircle, Loader2
} from "lucide-react";
import { motion } from "framer-motion";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { RadialGauge } from "@/components/shared/RadialGauge";
import { SuccessProbability } from "@/components/shared/SuccessProbability";
import { toast } from "@/components/ui/toast-system";
import { useAnalysisStore } from "@/store/analysisStore";

export default function ReportViewerPage() {
    const router = useRouter();
    const params = useParams();
    const id = params.id as string;

    // Read all analysis slices from the global Zustand store
    const report = useAnalysisStore((s) => s.report);
    const marketAnalysis = useAnalysisStore((s) => s.marketAnalysis);
    const competitorAnalysis = useAnalysisStore((s) => s.competitorAnalysis);
    const startupScore = useAnalysisStore((s) => s.startupScore);
    const currentIdea = useAnalysisStore((s) => s.currentIdea);

    // ── Empty state ──────────────────────────────────────────────────────
    if (!report) {
        return (
            <div className="flex h-[60vh] flex-col items-center justify-center gap-4 text-center">
                <div className="rounded-full bg-muted p-4">
                    <AlertCircle className="h-8 w-8 text-muted-foreground" />
                </div>
                <h3 className="text-xl font-semibold">No Report Available</h3>
                <p className="max-w-sm text-sm text-muted-foreground">
                    Submit and fully analyze a startup idea to generate a comprehensive report.
                </p>
                <Button onClick={() => router.push("/analyze")} className="mt-2">
                    Analyze a New Idea
                </Button>
            </div>
        );
    }

    const handleCopyReport = () => {
        const text = `Executive Summary\n\n${report.executive_summary}\n\nProblem & Solution\n\n${report.problem_solution_analysis}`;
        navigator.clipboard.writeText(text);
        toast.success({ title: "Report copied", description: "Executive summary copied to clipboard." });
    };

    const handleDownloadMarkdown = () => {
        const blob = new Blob([report.markdown_report], { type: "text/markdown" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `Startup_Report_${id || "export"}.md`;
        a.click();
        URL.revokeObjectURL(url);
        toast.success({ title: "Markdown downloaded" });
    };

    const successPct = startupScore
        ? parseInt(startupScore.success_probability.replace("%", ""), 10) || 0
        : 0;

    return (
        <div className="mx-auto max-w-5xl space-y-8 pb-20">
            {/* Top Bar Actions */}
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between sticky top-0 z-30 bg-background/80 backdrop-blur-md py-4 border-b">
                <Button variant="ghost" size="sm" onClick={() => router.back()} className="group w-fit">
                    <ArrowLeft className="mr-2 h-4 w-4 transition-transform group-hover:-translate-x-1" />
                    Back
                </Button>
                <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm" onClick={handleCopyReport}>
                        <Copy className="mr-2 h-4 w-4" />Copy Report
                    </Button>
                    <Button variant="outline" size="sm" onClick={handleDownloadMarkdown}>
                        <FileDown className="mr-2 h-4 w-4" />Download Markdown
                    </Button>
                </div>
            </div>

            {/* Report Header */}
            <div className="space-y-4">
                <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="px-2 py-0.5 text-[10px] font-bold uppercase tracking-widest bg-primary/10 text-primary border-none">
                        Confidential Report
                    </Badge>
                    <Badge variant="outline" className="px-2 py-0.5 text-[10px] font-bold uppercase tracking-widest border-emerald-500/20 text-emerald-600">
                        AI Generated
                    </Badge>
                </div>
                <h1 className="text-4xl font-black tracking-tight leading-none md:text-5xl text-foreground">
                    {currentIdea ? `"${currentIdea.slice(0, 80)}${currentIdea.length > 80 ? "..." : ""}"` : "Startup Analysis Report"}
                </h1>
                <div className="flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-muted-foreground">
                    <div className="flex items-center gap-1.5">
                        <Calendar className="h-4 w-4" />
                        {new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}
                    </div>
                    <div className="flex items-center gap-1.5">
                        <User className="h-4 w-4" />
                        By Venture Intelligence Engine
                    </div>
                    <div className="flex items-center gap-1.5">
                        <FileText className="h-4 w-4" />
                        ID: {id || "VTR-LIVE"}
                    </div>
                </div>
            </div>

            <Separator className="my-8" />

            {/* Report Content Sections */}
            <div className="grid gap-12">
                {/* Executive Summary */}
                <section id="executive-summary" className="scroll-mt-24 space-y-4">
                    <div className="flex items-center gap-2">
                        <div className="h-10 w-1 bg-primary rounded-full" />
                        <h2 className="text-2xl font-bold tracking-tight">Executive Summary</h2>
                    </div>
                    <p className="text-lg leading-relaxed text-muted-foreground font-medium">
                        {report.executive_summary}
                    </p>
                </section>

                {/* Problem and Solution */}
                <section id="problem-solution" className="space-y-4">
                    <div className="flex items-center gap-2">
                        <div className="h-10 w-1 bg-rose-500 rounded-full" />
                        <h2 className="text-2xl font-bold tracking-tight">Problem & Solution</h2>
                    </div>
                    <p className="text-sm leading-relaxed text-muted-foreground">
                        {report.problem_solution_analysis}
                    </p>
                </section>

                {/* Market Opportunity */}
                <section id="market-opportunity" className="space-y-6">
                    <div className="flex items-center gap-2">
                        <div className="h-10 w-1 bg-emerald-500 rounded-full" />
                        <h2 className="text-2xl font-bold tracking-tight">Market Opportunity</h2>
                    </div>
                    {marketAnalysis && (
                        <div className="grid gap-4 md:grid-cols-4">
                            {[
                                { label: "TAM", value: marketAnalysis.tam },
                                { label: "SAM", value: marketAnalysis.sam },
                                { label: "SOM", value: marketAnalysis.som },
                                { label: "CAGR", value: marketAnalysis.industry_growth_rate },
                            ].map((m) => (
                                <div key={m.label} className="p-4 rounded-xl border bg-muted/20">
                                    <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground mb-1">{m.label}</p>
                                    <p className="text-2xl font-black">{m.value}</p>
                                </div>
                            ))}
                        </div>
                    )}
                    <p className="text-sm leading-relaxed text-muted-foreground">{report.market_opportunity}</p>
                </section>

                {/* Startup Scorecard */}
                {startupScore && (
                    <section id="startup-score" className="space-y-6">
                        <div className="flex items-center gap-2">
                            <div className="h-10 w-1 bg-indigo-500 rounded-full" />
                            <h2 className="text-2xl font-bold tracking-tight">Venture Intelligence Score</h2>
                        </div>
                        <Card className="border-primary/10 overflow-hidden shadow-none ring-1 ring-primary/5">
                            <CardContent className="p-0">
                                <div className="grid md:grid-cols-2 lg:grid-cols-4 divide-x divide-y md:divide-y-0">
                                    {[
                                        { label: "Market", value: startupScore.market_potential_score, color: "text-emerald-500" },
                                        { label: "Competition", value: startupScore.competition_score, color: "text-amber-500" },
                                        { label: "Scalability", value: startupScore.scalability_score, color: "text-indigo-500" },
                                        { label: "Risk", value: startupScore.execution_risk_score, color: "text-rose-500" },
                                    ].map((score) => (
                                        <div key={score.label} className="flex flex-col items-center justify-center p-8 gap-4">
                                            <RadialGauge value={score.value} size={80} strokeWidth={8} color={score.color} />
                                            <span className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">{score.label}</span>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                        <div className="bg-accent/30 p-8 rounded-2xl border flex flex-col md:flex-row items-center justify-between gap-8">
                            <div className="space-y-2 text-center md:text-left">
                                <h3 className="text-xl font-bold">Comprehensive Success Probability</h3>
                                <p className="text-sm text-muted-foreground">Synthesized cross-metric venture viability score.</p>
                                <p className="text-3xl font-black text-primary">{startupScore.success_probability}</p>
                            </div>
                            <div className="w-full max-w-sm bg-background p-6 rounded-xl border">
                                <SuccessProbability percentage={successPct} />
                            </div>
                        </div>
                        <p className="text-sm text-muted-foreground leading-relaxed">{report.startup_score_summary}</p>
                    </section>
                )}

                {/* Competitor Landscape */}
                <section id="competitor-landscape" className="space-y-6">
                    <div className="flex items-center gap-2">
                        <div className="h-10 w-1 bg-amber-500 rounded-full" />
                        <h2 className="text-2xl font-bold tracking-tight">Competitor Landscape</h2>
                    </div>
                    <p className="text-sm text-muted-foreground leading-relaxed">{report.competitor_landscape}</p>
                    {competitorAnalysis?.competitors.map((comp) => (
                        <div key={comp.name} className="p-6 rounded-2xl border bg-card flex items-start justify-between group hover:border-primary/20 transition-all">
                            <div className="space-y-2">
                                <div className="flex items-center gap-2">
                                    <h4 className="font-bold">{comp.name}</h4>
                                    <Badge variant="outline" className="text-[10px] uppercase">{comp.product_category}</Badge>
                                </div>
                                <p className="text-sm text-muted-foreground">{comp.description}</p>
                            </div>
                        </div>
                    ))}
                </section>

                {/* Final CTA */}
                <section className="bg-primary text-primary-foreground p-12 rounded-[2rem] text-center space-y-6">
                    <div className="mx-auto w-fit p-3 rounded-full bg-white/10 mb-4">
                        <Zap className="h-6 w-6 fill-current" />
                    </div>
                    <h2 className="text-3xl font-black tracking-tight">Move to Development Phase?</h2>
                    <p className="text-primary-foreground/80 max-w-2xl mx-auto font-medium">
                        {startupScore && `With a ${startupScore.success_probability} success probability, `}
                        our intelligence engine recommends building a focused MVP to validate your core assumptions.
                    </p>
                    <div className="flex flex-wrap justify-center gap-4 pt-4">
                        <Button variant="secondary" size="lg" className="font-bold" onClick={handleDownloadMarkdown}>
                            Download Full Report
                        </Button>
                    </div>
                </section>
            </div>

            {/* TOC (Desktop) */}
            <div className="hidden lg:block fixed left-12 top-1/2 -translate-y-1/2 space-y-4">
                {[
                    { id: "executive-summary", label: "Executive Summary" },
                    { id: "problem-solution", label: "Problem & Solution" },
                    { id: "market-opportunity", label: "Market Opportunity" },
                    { id: "startup-score", label: "Venture Score" },
                    { id: "competitor-landscape", label: "Competitors" },
                ].map((link) => (
                    <a
                        key={link.id}
                        href={`#${link.id}`}
                        className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-muted-foreground/50 hover:text-primary transition-colors group"
                    >
                        <div className="h-2 w-2 rounded-full border-2 border-current group-hover:bg-primary" />
                        {link.label}
                    </a>
                ))}
            </div>
        </div>
    );
}
