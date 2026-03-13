"use client";

import * as React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export interface Competitor {
    id: string;
    name: string;
    description: string;
    targetMarket?: string;
    marketShare?: string;
    pricing?: string;
    strengths: string[];
    weaknesses: string[];
}

interface CompetitorCardProps {
    competitor: Competitor;
}

export function CompetitorCard({ competitor }: CompetitorCardProps) {
    return (
        <Card className="h-full border-2 border-black shadow-brutal hover:scale-[1.01] transition-transform">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 bg-primary/5">
                <CardTitle className="text-xl font-bold uppercase">{competitor.name}</CardTitle>
                {competitor.targetMarket && (
                    <Badge variant="outline" className="text-[10px] uppercase font-bold tracking-tighter">
                        {competitor.targetMarket}
                    </Badge>
                )}
            </CardHeader>
            <CardContent className="pt-4 space-y-4">
                <p className="text-sm text-muted-foreground leading-relaxed">
                    {competitor.description}
                </p>
                
                <div className="grid grid-cols-2 gap-4 pt-2">
                    <div className="space-y-1">
                        <span className="text-[10px] font-bold uppercase text-emerald-600 block">Strengths</span>
                        <ul className="text-[11px] font-medium list-disc pl-4">
                            {competitor.strengths.slice(0, 2).map((s, i) => <li key={i}>{s}</li>)}
                        </ul>
                    </div>
                    <div className="space-y-1">
                        <span className="text-[10px] font-bold uppercase text-rose-600 block">Weaknesses</span>
                        <ul className="text-[11px] font-medium list-disc pl-4">
                            {competitor.weaknesses.slice(0, 2).map((w, i) => <li key={i}>{w}</li>)}
                        </ul>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
