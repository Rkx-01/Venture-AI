"use client";

import * as React from "react";
import { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import {
    Lightbulb,
    Sparkles,
    Loader2,
    ArrowRight,
    Info,
    AlertCircle,
    Building2,
    Users,
    Target,
    Wrench,
    DollarSign,
    CheckCircle2,
    FileText
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select";
import { cn } from "@/lib/utils";

// Import the dedicated frontend service for idea analysis
import { ideaService } from "@/services/ideaService";
import { IdeaAnalysisResponse } from "@/types/api";
import { useAnalysisStore } from "@/store/analysisStore";
import { useRouter } from "next/navigation";
import { useToast } from "@/hooks/use-toast";

// ----------------------------------------
// Zod schema matching backend validation
// ----------------------------------------
const analyzeIdeaSchema = z.object({
    idea_text: z
        .string()
        .min(1, "Idea description is required.")
        .min(30, "Please provide at least 30 characters for an accurate analysis.")
        .max(2000, "Your idea description cannot exceed 2000 characters.")
        .refine(
            (val) => val.trim().split(/\s+/).filter(Boolean).length >= 5,
            { message: "Please use at least 5 words to describe your idea." }
        ),
});

type AnalyzeIdeaFormData = z.infer<typeof analyzeIdeaSchema>;

const EXAMPLE_IDEAS = [
    "An AI-powered mental health assistant specifically for college students during finals week.",
    "A decentralized marketplace for vertical farming equipment and sustainable seeds.",
    "Automated legal compliance checker for small e-commerce businesses expanding internationally."
];

export default function AnalyzePage() {
    const router = useRouter();
    const { toast } = useToast();
    // Component State
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [serverError, setServerError] = useState<string | null>(null);

    // Use unified store
    const setIdeaAnalysis = useAnalysisStore((s) => s.setIdeaAnalysis);
    const setCurrentIdea = useAnalysisStore((s) => s.setCurrentIdea);
    const resetAnalysis = useAnalysisStore((s) => s.resetAnalysis);
    const analysisResult = useAnalysisStore((s) => s.ideaAnalysis);

    const {
        register,
        handleSubmit,
        setValue,
        watch,
        formState: { errors }
    } = useForm<AnalyzeIdeaFormData>({
        resolver: zodResolver(analyzeIdeaSchema),
        defaultValues: {
            idea_text: "",
        }
    });

    const ideaText = watch("idea_text");
    const charCount = ideaText?.length || 0;

    const onSubmit = async (data: AnalyzeIdeaFormData) => {
        setIsAnalyzing(true);
        setServerError(null);
        resetAnalysis();

        try {
            // Call the ideaService, delegating HTTP logic to the service layer
            const result = await ideaService.analyzeIdea(data.idea_text);
            
            // Hydrate unified store
            setCurrentIdea(data.idea_text);
            setIdeaAnalysis(result);

            toast({
                title: "Analysis Complete",
                description: "Venture intelligence report generated successfully.",
            });

            // Navigate to results
            router.push("/result");
        } catch (error: any) {
            console.error("Analysis submission failed:", error);
            setServerError(error.message || "An unexpected error occurred during analysis.");
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div className="mx-auto max-w-5xl space-y-8 pb-12">
            {/* Header Section */}
            <div className="text-center space-y-4">
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
                    <Lightbulb className="h-6 w-6" />
                </div>
                <h1 className="text-4xl font-bold tracking-tight">Venture Intelligence</h1>
                <p className="mx-auto max-w-2xl text-lg text-muted-foreground">
                    Submit your startup idea for a deep-dive AI analysis. We'll identify market gaps,
                    target users, and evaluate your core solution.
                </p>
            </div>

            <div className={cn("grid gap-8", analysisResult ? "lg:grid-cols-1" : "lg:grid-cols-3")}>

                {/* 
                  When we have an analysis result, we hide the sidebar to give full width to the results.
                  When there is no result, we show the input form and sidebar side-by-side. 
                */}

                {/* Main Input Form */}
                <div className={cn(analysisResult ? "mx-auto w-full max-w-3xl" : "lg:col-span-2")}>
                    <Card className="border-2 border-primary/5 shadow-xl">
                        <CardHeader>
                            <CardTitle>Idea Description</CardTitle>
                            <CardDescription>
                                Describe what you're building, who it's for, and the problem it solves.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            {isAnalyzing ? (
                                <div className="min-h-[300px] flex flex-col items-center justify-center space-y-4 text-center">
                                    <div className="relative">
                                        <div className="absolute inset-0 rounded-full blur-xl bg-primary/20 animate-pulse" />
                                        <Loader2 className="h-12 w-12 animate-spin text-primary relative z-10" />
                                    </div>
                                    <div className="space-y-1">
                                        <h3 className="font-semibold text-lg">Analyzing startup idea...</h3>
                                        <p className="text-sm text-muted-foreground animate-pulse text-gray-500">
                                            Our AI is evaluating your concept across multiple dimensions.
                                        </p>
                                    </div>
                                </div>
                            ) : serverError ? (
                                <div className="min-h-[300px] flex flex-col items-center justify-center space-y-4 text-center">
                                    <div className="h-16 w-16 rounded-full bg-destructive/10 flex items-center justify-center mb-2">
                                        <AlertCircle className="h-8 w-8 text-destructive" />
                                    </div>
                                    <div className="space-y-2 max-w-sm">
                                        <h3 className="font-semibold text-lg">Analysis failed</h3>
                                        <p className="text-sm text-muted-foreground">
                                            {serverError} Please try again.
                                        </p>
                                    </div>
                                    <div className="pt-4 flex gap-3">
                                        <Button
                                            variant="outline"
                                            onClick={() => setServerError(null)}
                                        >
                                            Edit Idea
                                        </Button>
                                        <Button
                                            onClick={handleSubmit(onSubmit)}
                                        >
                                            Retry Analysis
                                        </Button>
                                    </div>
                                </div>
                            ) : (
                                <form onSubmit={handleSubmit(onSubmit)} className="space-y-6" noValidate>
                                    {/* Idea Text Area */}
                                    <div className="space-y-2">
                                        <div className="flex items-center justify-between">
                                            <label className="text-sm font-medium text-foreground">The Concept</label>
                                            <span className={cn(
                                                "text-xs tabular-nums",
                                                charCount > 1800 ? "text-destructive font-bold" : "text-muted-foreground"
                                            )}>
                                                {charCount} / 2000
                                            </span>
                                        </div>
                                        <Textarea
                                            {...register("idea_text")}
                                            placeholder="e.g. A platform that uses AI to automate..."
                                            className={cn(
                                                "min-h-[200px] resize-none text-base leading-relaxed transition-colors",
                                                errors.idea_text
                                                    ? "border-destructive focus-visible:ring-destructive/30"
                                                    : "focus:ring-2 focus:ring-primary/20"
                                            )}
                                            disabled={isAnalyzing}
                                        />

                                        {/* Validation Error */}
                                        {errors.idea_text ? (
                                            <div className="flex items-center gap-1.5 text-sm text-destructive">
                                                <AlertCircle className="h-3.5 w-3.5 shrink-0" />
                                                <span>{errors.idea_text.message}</span>
                                            </div>
                                        ) : (
                                            <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                                <Info className="h-3 w-3" />
                                                <span>Minimum 30 characters and 5 words for accurate analysis.</span>
                                            </div>
                                        )}
                                    </div>

                                    <Button
                                        type="submit"
                                        className="w-full h-12 text-lg font-semibold transition-all"
                                        disabled={isAnalyzing}
                                    >
                                        Evaluate Startup Idea
                                        <ArrowRight className="ml-2 h-5 w-5" />
                                    </Button>
                                </form>
                            )}
                        </CardContent>
                    </Card>
                </div>

                {/* Sidebar: Tips & Examples (Only visible before analysis) */}
                {!analysisResult && (
                    <div className="space-y-6">
                        <Card className="bg-slate-50 border-none dark:bg-slate-900/50">
                            <CardHeader>
                                <div className="flex items-center gap-2 text-primary">
                                    <Sparkles className="h-5 w-5" />
                                    <CardTitle className="text-lg">Examples</CardTitle>
                                </div>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                {EXAMPLE_IDEAS.map((example, i) => (
                                    <div
                                        key={i}
                                        className="group relative cursor-pointer rounded-lg border bg-background p-4 text-sm transition-all hover:border-primary/50 hover:shadow-md"
                                        onClick={() => setValue("idea_text", example, { shouldValidate: true })}
                                    >
                                        <p className="text-muted-foreground group-hover:text-foreground line-clamp-3">
                                            "{example}"
                                        </p>
                                        <div className="mt-2 text-[10px] font-bold uppercase tracking-widest text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                                            Click to use
                                        </div>
                                    </div>
                                ))}
                            </CardContent>
                        </Card>

                        <div className="rounded-xl border p-6 bg-gradient-to-br from-primary/5 to-transparent">
                            <h3 className="font-semibold mb-2">Pro Tip</h3>
                            <p className="text-sm text-muted-foreground leading-relaxed">
                                The more detail you provide about the specific problem and your target audience,
                                the more accurate our AI competitive analysis will be.
                            </p>
                        </div>
                    </div>
                )}
            </div>

            {/* Analysis Results Display */}
            {analysisResult && (
                <div className="pt-8 border-t animate-in fade-in slide-in-from-bottom-4 duration-500 space-y-6">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400">
                            <CheckCircle2 className="h-6 w-6" />
                        </div>
                        <h2 className="text-3xl font-bold tracking-tight">AI Analysis Results</h2>
                    </div>

                    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                        {/* Report */}
                        <Card className="md:col-span-2 lg:col-span-3 border-l-4 border-l-primary bg-gradient-to-r from-primary/5 to-transparent">
                            <CardHeader className="pb-2">
                                <FileText className="h-5 w-5 text-primary mb-2" />
                                <CardTitle className="text-lg">Executive Report</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-foreground leading-relaxed whitespace-pre-line">
                                    {analysisResult.report}
                                </p>
                            </CardContent>
                        </Card>
                    </div>
                </div>
            )}
        </div>
    );
}
