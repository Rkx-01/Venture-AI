"use client";

import * as React from "react";
import { Progress } from "@/components/ui/progress";

interface SuccessProbabilityProps {
    percentage: number;
}

export function SuccessProbability({ percentage }: SuccessProbabilityProps) {
    return (
        <div className="space-y-4 w-full">
            <div className="flex justify-between items-center text-sm font-bold uppercase tracking-widest">
                <span>Success Probability</span>
                <span>{percentage}%</span>
            </div>
            <Progress value={percentage} className="h-4 bg-muted border-2 border-black" />
            <p className="text-[10px] text-muted-foreground uppercase font-bold text-center">
                Based on AI confidence models and historical startup data.
            </p>
        </div>
    );
}
