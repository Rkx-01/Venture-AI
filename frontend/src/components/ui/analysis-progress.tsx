"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
    Lightbulb, Globe, Users, Trophy, FileText,
    CheckCircle2, Loader2, Circle
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAnalysisStore, type AnalysisStep } from "@/store/analysisStore";

// ─────────────────────────────────────────────────────────────────────────────
// Step definitions
// ─────────────────────────────────────────────────────────────────────────────
const STEPS: {
    key: AnalysisStep;
    label: string;
    description: string;
    icon: React.ElementType;
    color: string;
    bgColor: string;
}[] = [
        {
            key: "idea",
            label: "Idea Analysis",
            description: "Extracting industry, target users, and core solution type",
            icon: Lightbulb,
            color: "text-amber-500",
            bgColor: "bg-amber-500/10",
        },
        {
            key: "market",
            label: "Market Analysis",
            description: "Sizing TAM, SAM, SOM and estimating industry growth rate",
            icon: Globe,
            color: "text-blue-500",
            bgColor: "bg-blue-500/10",
        },
        {
            key: "competitors",
            label: "Competitor Research",
            description: "Mapping the competitive landscape and identifying market gaps",
            icon: Users,
            color: "text-violet-500",
            bgColor: "bg-violet-500/10",
        },
        {
            key: "score",
            label: "Startup Scoring",
            description: "Calculating viability score across 4 dimensions",
            icon: Trophy,
            color: "text-emerald-500",
            bgColor: "bg-emerald-500/10",
        },
        {
            key: "report",
            label: "Report Generation",
            description: "Synthesizing a full executive-level analysis report",
            icon: FileText,
            color: "text-primary",
            bgColor: "bg-primary/10",
        },
    ];

// ─────────────────────────────────────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────────────────────────────────────
const STEP_KEYS = STEPS.map((s) => s.key);

function getStepStatus(stepKey: AnalysisStep, currentStep: AnalysisStep): "waiting" | "active" | "done" {
    const stepIndex = STEP_KEYS.indexOf(stepKey);
    const currentIndex = STEP_KEYS.indexOf(currentStep);

    if (currentStep === "complete" || currentStep === "error") {
        return currentStep === "complete" ? "done" : stepIndex < currentIndex ? "done" : "waiting";
    }
    if (stepIndex < currentIndex) return "done";
    if (stepIndex === currentIndex) return "active";
    return "waiting";
}

// ─────────────────────────────────────────────────────────────────────────────
// Component
// ─────────────────────────────────────────────────────────────────────────────
export function AnalysisProgress() {
    const currentStep = useAnalysisStore((s) => s.currentStep);
    const currentIdea = useAnalysisStore((s) => s.currentIdea);

    const isVisible = currentStep !== "idle";
    const isComplete = currentStep === "complete";
    const isError = currentStep === "error";

    // Overall progress percentage (0–100)
    const activeIndex = STEP_KEYS.indexOf(currentStep);
    const progressPct = isComplete
        ? 100
        : activeIndex >= 0
            ? Math.round(((activeIndex) / STEPS.length) * 100)
            : 0;

    if (!isVisible) return null;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0, scale: 0.96, y: 16 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.96, y: 16 }}
                transition={{ duration: 0.35, ease: "easeOut" }}
                className="w-full rounded-2xl border bg-card shadow-2xl overflow-hidden"
            >
                {/* Header */}
                <div className="px-6 pt-6 pb-4 border-b">
                    <div className="flex items-start justify-between gap-4">
                        <div className="space-y-1">
                            <h3 className="font-bold text-lg leading-tight">
                                {isComplete ? "Analysis Complete!" : isError ? "Analysis Failed" : "Running Full Analysis..."}
                            </h3>
                            {currentIdea && (
                                <p className="text-xs text-muted-foreground line-clamp-1 max-w-md">
                                    "{currentIdea}"
                                </p>
                            )}
                        </div>
                        <span className={cn(
                            "text-sm font-bold tabular-nums shrink-0",
                            isComplete ? "text-emerald-500" : isError ? "text-destructive" : "text-primary"
                        )}>
                            {progressPct}%
                        </span>
                    </div>

                    {/* Overall progress bar */}
                    <div className="mt-4 h-1.5 w-full rounded-full bg-muted overflow-hidden">
                        <motion.div
                            className={cn(
                                "h-full rounded-full",
                                isError ? "bg-destructive" : "bg-primary"
                            )}
                            initial={{ width: 0 }}
                            animate={{ width: `${progressPct}%` }}
                            transition={{ duration: 0.6, ease: "easeInOut" }}
                        />
                    </div>
                </div>

                {/* Step list */}
                <div className="grid divide-y">
                    {STEPS.map((step, i) => {
                        const status = isComplete
                            ? "done"
                            : isError && STEP_KEYS.indexOf(currentStep as AnalysisStep) <= i
                                ? "waiting"
                                : getStepStatus(step.key, currentStep);

                        const Icon = step.icon;

                        return (
                            <motion.div
                                key={step.key}
                                className={cn(
                                    "flex items-center gap-4 px-6 py-4 transition-colors",
                                    status === "active" && "bg-accent/50"
                                )}
                                initial={{ opacity: 0, x: -8 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: i * 0.05 }}
                            >
                                {/* Step icon / status indicator */}
                                <div className={cn(
                                    "shrink-0 flex items-center justify-center h-10 w-10 rounded-xl transition-colors",
                                    status === "done" ? "bg-emerald-500/10" :
                                        status === "active" ? step.bgColor : "bg-muted"
                                )}>
                                    {status === "done" ? (
                                        <CheckCircle2 className="h-5 w-5 text-emerald-500" />
                                    ) : status === "active" ? (
                                        <Loader2 className={cn("h-5 w-5 animate-spin", step.color)} />
                                    ) : (
                                        <Icon className="h-5 w-5 text-muted-foreground/40" />
                                    )}
                                </div>

                                {/* Text */}
                                <div className="flex-1 min-w-0">
                                    <p className={cn(
                                        "text-sm font-semibold",
                                        status === "done" ? "text-emerald-600 dark:text-emerald-400" :
                                            status === "active" ? "text-foreground" : "text-muted-foreground"
                                    )}>
                                        {step.label}
                                    </p>
                                    {status === "active" && (
                                        <motion.p
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            className="text-xs text-muted-foreground mt-0.5 truncate"
                                        >
                                            {step.description}
                                        </motion.p>
                                    )}
                                </div>

                                {/* Step number (waiting) */}
                                {status === "waiting" && (
                                    <span className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground/40 shrink-0">
                                        {i + 1} / {STEPS.length}
                                    </span>
                                )}
                                {status === "done" && (
                                    <span className="text-[10px] font-bold uppercase tracking-widest text-emerald-500 shrink-0">
                                        Done
                                    </span>
                                )}
                            </motion.div>
                        );
                    })}
                </div>
            </motion.div>
        </AnimatePresence>
    );
}
