"use client";

import * as React from "react";
import { Search, Filter, LayoutGrid, List, Loader2, AlertCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { CompetitorCard, type Competitor } from "@/components/shared/CompetitorCard";
import { CompetitorTable } from "@/components/shared/CompetitorTable";
import { useAnalysisStore } from "@/store/analysisStore";

export default function CompetitorsPage() {
    const [searchQuery, setSearchQuery] = React.useState("");
    const [view, setView] = React.useState<"cards" | "table">("cards");

    // Read real data from the Zustand store (populated by useRunFullStartupAnalysis)
    const competitorAnalysis = useAnalysisStore((s) => s.competitorAnalysis);

    // Map backend Competitor shape → the shape CompetitorCard expects
    const competitors: Competitor[] = React.useMemo(() => {
        if (!competitorAnalysis?.competitors) return [];
        return competitorAnalysis.competitors.map((c, i) => ({
            id: String(i),
            name: c.name,
            description: c.description,
            targetMarket: c.market_focus,
            marketShare: undefined,
            pricing: undefined,
            strengths: c.strengths,
            weaknesses: c.weaknesses,
        }));
    }, [competitorAnalysis]);

    const filteredCompetitors = competitors.filter((comp) =>
        comp.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        comp.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // ── Loading / empty state ──────────────────────────────────────────────
    if (!competitorAnalysis) {
        return (
            <div className="flex h-[60vh] flex-col items-center justify-center gap-4 text-center">
                <div className="rounded-full bg-muted p-4">
                    <AlertCircle className="h-8 w-8 text-muted-foreground" />
                </div>
                <h3 className="text-xl font-semibold">No Competitor Data Yet</h3>
                <p className="max-w-sm text-sm text-muted-foreground">
                    Submit a startup idea from the <strong>Analyze</strong> page to run competitor analysis. Results will appear here automatically.
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-8 pb-12">
            {/* Header Section */}
            <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Competitor Landscape</h1>
                    <p className="text-muted-foreground">
                        Analyze market rivals, their strategic positioning, and identified gaps.
                    </p>
                </div>
                <div className="flex items-center gap-2">
                    <div className="bg-muted p-1 rounded-lg flex items-center gap-1 border">
                        <Button
                            variant={view === "cards" ? "secondary" : "ghost"}
                            size="icon"
                            className="h-8 w-8"
                            onClick={() => setView("cards")}
                        >
                            <LayoutGrid className="h-4 w-4" />
                        </Button>
                        <Button
                            variant={view === "table" ? "secondary" : "ghost"}
                            size="icon"
                            className="h-8 w-8"
                            onClick={() => setView("table")}
                        >
                            <List className="h-4 w-4" />
                        </Button>
                    </div>
                    <Button variant="outline" size="sm">
                        <Filter className="mr-2 h-4 w-4" />
                        Filter
                    </Button>
                </div>
            </div>

            {/* Search & Insights Summary */}
            <div className="grid gap-6 md:grid-cols-4">
                <div className="md:col-span-3">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                        <Input
                            placeholder="Search competitor names or descriptions..."
                            className="pl-10 h-11 bg-background shadow-sm"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                </div>
                <div className="rounded-xl border bg-card p-4 flex items-center justify-between">
                    <div>
                        <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Total Rivals</p>
                        <p className="text-2xl font-bold">{competitors.length}</p>
                    </div>
                    <div className="rounded-full bg-primary/10 p-2 text-primary">
                        <List className="h-5 w-5" />
                    </div>
                </div>
            </div>

            {/* Competitors Main View */}
            <div className="min-h-[400px]">
                {view === "cards" ? (
                    <div className="grid gap-6">
                        <AnimatePresence mode="popLayout">
                            {filteredCompetitors.map((competitor) => (
                                <motion.div
                                    key={competitor.id}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, scale: 0.95 }}
                                    layout
                                >
                                    <CompetitorCard competitor={competitor} />
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </div>
                ) : (
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                    >
                        <CompetitorTable competitors={filteredCompetitors} />
                    </motion.div>
                )}

                {filteredCompetitors.length === 0 && (
                    <div className="flex flex-col items-center justify-center py-20 text-center">
                        <div className="rounded-full bg-muted p-4 mb-4">
                            <Search className="h-8 w-8 text-muted-foreground" />
                        </div>
                        <h3 className="text-lg font-semibold">No competitors found</h3>
                        <p className="text-muted-foreground">Try adjusting your search or filters.</p>
                    </div>
                )}
            </div>

            {/* Market Gaps Insight Section */}
            {competitorAnalysis.summary && (
                <Card className="bg-primary text-primary-foreground">
                    <CardContent className="p-8">
                        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                            <div className="space-y-2">
                                <h2 className="text-2xl font-bold">AI Competitive Summary</h2>
                                <p className="text-primary-foreground/80 max-w-xl leading-relaxed">
                                    {competitorAnalysis.summary}
                                </p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}
