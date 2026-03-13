"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import {
    Lightbulb, BarChart3, Users, FileText, TrendingUp, Trophy,
    type LucideIcon
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";




export type EmptyStateVariant =
    | "dashboard"
    | "reports"
    | "competitors"
    | "market"
    | "score"
    | "custom";

const PRESETS: Record<
    Exclude<EmptyStateVariant, "custom">,
    {
        icon: LucideIcon;
        iconBg: string;
        iconColor: string;
        illustration: LucideIcon[];
        title: string;
        description: string;
        cta: string;
        ctaHref: string;
    }
> = {
    dashboard: {
        icon: Lightbulb,
        iconBg: "bg-amber-500/10",
        iconColor: "text-amber-500",
        illustration: [BarChart3, TrendingUp, FileText],
        title: "Your dashboard is empty",
        description: "Analyze your first startup idea to see insights, scores, and reports here.",
        cta: "Analyze an Idea",
        ctaHref: "/analyze",
    },
    reports: {
        icon: FileText,
        iconBg: "bg-primary/10",
        iconColor: "text-primary",
        illustration: [BarChart3, TrendingUp, Lightbulb],
        title: "No reports yet",
        description: "Generate a full AI synthesis report by completing your first startup analysis.",
        cta: "Run First Analysis",
        ctaHref: "/analyze",
    },
    competitors: {
        icon: Users,
        iconBg: "bg-violet-500/10",
        iconColor: "text-violet-500",
        illustration: [Users, TrendingUp, BarChart3],
        title: "No competitor data available",
        description: "Submit a startup idea to automatically map your competitive landscape and identify market gaps.",
        cta: "Analyze an Idea",
        ctaHref: "/analyze",
    },
    market: {
        icon: BarChart3,
        iconBg: "bg-blue-500/10",
        iconColor: "text-blue-500",
        illustration: [TrendingUp, BarChart3, Lightbulb],
        title: "No market data yet",
        description: "Run a startup analysis to get AI-generated TAM, SAM, SOM estimates and growth projections.",
        cta: "Analyze an Idea",
        ctaHref: "/analyze",
    },
    score: {
        icon: Trophy,
        iconBg: "bg-emerald-500/10",
        iconColor: "text-emerald-500",
        illustration: [Trophy, TrendingUp, BarChart3],
        title: "No scorecard yet",
        description: "Complete your first analysis to get a multi-dimension venture viability score.",
        cta: "Analyze an Idea",
        ctaHref: "/analyze",
    },
};




function Illustration({ icons, iconColor, iconBg }: {
    icons: LucideIcon[];
    iconColor: string;
    iconBg: string;
}) {
    return (
        <div className="relative mx-auto mb-8 h-48 w-48">
            <div className="absolute inset-0 rounded-full bg-gradient-to-br from-primary/5 to-transparent" />
            <div className="absolute inset-4 rounded-full border border-dashed border-border/60 animate-[spin_40s_linear_infinite]" />
            <div className="absolute inset-8 rounded-full border border-dashed border-border/40 animate-[spin_30s_linear_infinite_reverse]" />

            <div className="absolute inset-0 flex items-center justify-center">
                <div className={cn("flex h-20 w-20 items-center justify-center rounded-2xl shadow-lg", iconBg)}>
                    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-10 w-10">
                        <rect x="10" y="14" width="36" height="44" rx="4" className="fill-current opacity-10" />
                        <rect x="14" y="10" width="36" height="44" rx="4" className="fill-current opacity-15" />
                        <rect x="18" y="6" width="36" height="44" rx="4" stroke="currentColor" strokeWidth="2.5" className="fill-current opacity-5" />
                        <line x1="26" y1="20" x2="44" y2="20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="opacity-40" />
                        <line x1="26" y1="28" x2="44" y2="28" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="opacity-30" />
                        <line x1="26" y1="36" x2="36" y2="36" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="opacity-20" />
                    </svg>
                </div>
            </div>

            {icons.map((Icon, i) => {
                const angle = (i * 360) / icons.length - 90;
                const rad = (angle * Math.PI) / 180;
                const r = 80;
                const x = Math.cos(rad) * r + 96 - 18;
                const y = Math.sin(rad) * r + 96 - 18;
                return (
                    <motion.div
                        key={i}
                        className={cn("absolute flex h-9 w-9 items-center justify-center rounded-xl border bg-card shadow-md", iconBg)}
                        style={{ left: x, top: y }}
                        initial={{ opacity: 0, scale: 0 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: i * 0.15 + 0.2, type: "spring", stiffness: 200 }}
                    >
                        <Icon className={cn("h-4 w-4", iconColor)} />
                    </motion.div>
                );
            })}
        </div>
    );
}




interface EmptyStateProps {
    variant?: EmptyStateVariant;
    
    title?: string;
    description?: string;
    cta?: string;
    ctaHref?: string;
    className?: string;
    /** Optional secondary action */
    secondaryCta?: string;
    secondaryCtaHref?: string;
}

export function EmptyState({
    variant = "dashboard",
    title,
    description,
    cta,
    ctaHref,
    className,
    secondaryCta,
    secondaryCtaHref,
}: EmptyStateProps) {
    const preset = variant !== "custom" ? PRESETS[variant] : null;

    const resolvedTitle = title ?? preset?.title ?? "Nothing here yet";
    const resolvedDesc = description ?? preset?.description ?? "Get started by running your first analysis.";
    const resolvedCta = cta ?? preset?.cta ?? "Get Started";
    const resolvedHref = ctaHref ?? preset?.ctaHref ?? "/analyze";
    const icons = preset?.illustration ?? [BarChart3, TrendingUp, FileText];
    const iconBg = preset?.iconBg ?? "bg-primary/10";
    const iconColor = preset?.iconColor ?? "text-primary";

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, ease: "easeOut" }}
            className={cn(
                "flex flex-col items-center justify-center py-20 text-center",
                className
            )}
        >
            <Illustration icons={icons} iconColor={iconColor} iconBg={iconBg} />

            <div className="max-w-md space-y-3">
                <h3 className="text-xl font-bold tracking-tight">{resolvedTitle}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{resolvedDesc}</p>
            </div>

            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
                <Button asChild size="lg" className="font-semibold">
                    <Link href={resolvedHref}>{resolvedCta}</Link>
                </Button>
                {secondaryCta && secondaryCtaHref && (
                    <Button asChild variant="outline" size="lg">
                        <Link href={secondaryCtaHref}>{secondaryCta}</Link>
                    </Button>
                )}
            </div>
        </motion.div>
    );
}
