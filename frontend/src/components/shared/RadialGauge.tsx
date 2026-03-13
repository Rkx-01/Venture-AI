"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

interface RadialGaugeProps {
    value: number;
    size?: number;
    strokeWidth?: number;
    color?: string;
    className?: string;
}

export function RadialGauge({
    value,
    size = 100,
    strokeWidth = 10,
    color = "text-primary",
    className
}: RadialGaugeProps) {
    const radius = (size - strokeWidth) / 2;
    const circumference = radius * 2 * Math.PI;
    const offset = circumference - (value / 10) * circumference;

    return (
        <div className={cn("relative flex items-center justify-center", className)} style={{ width: size, height: size }}>
            <svg className="transform -rotate-90" width={size} height={size}>
                <circle
                    className="text-muted/20"
                    strokeWidth={strokeWidth}
                    stroke="currentColor"
                    fill="transparent"
                    r={radius}
                    cx={size / 2}
                    cy={size / 2}
                />
                <circle
                    className={cn(color, "transition-all duration-500 ease-out")}
                    strokeWidth={strokeWidth}
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    strokeLinecap="round"
                    stroke="currentColor"
                    fill="transparent"
                    r={radius}
                    cx={size / 2}
                    cy={size / 2}
                />
            </svg>
            <span className="absolute text-xl font-bold">{value}</span>
        </div>
    );
}
