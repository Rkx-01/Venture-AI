"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

export interface BrutalistButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> { }

export const BrutalistButton = React.forwardRef<HTMLButtonElement, BrutalistButtonProps>(
    ({ className, children, ...props }, ref) => {
        return (
            <button
                ref={ref}
                className={cn(
                    "relative inline-flex items-center justify-center font-bold tracking-wide uppercase px-8 py-4 transition-all duration-150",
                    "bg-primary text-accent border-2 border-primary",
                    "shadow-brutal hover:shadow-none hover:translate-x-[4px] hover:translate-y-[4px]",
                    "active:translate-x-[2px] active:translate-y-[2px] active:shadow-none",
                    "disabled:opacity-50 disabled:pointer-events-none",
                    className
                )}
                {...props}
            >
                {children}
            </button>
        );
    }
);
BrutalistButton.displayName = "BrutalistButton";
