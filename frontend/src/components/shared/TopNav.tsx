"use client";

import { Bell, Search, User } from "lucide-react";
import { cn } from "@/lib/utils";
import { ThemeToggle } from "./ThemeToggle";
import { MobileNav } from "./MobileNav";

interface TopNavProps {
    className?: string;
}

export function TopNav({ className }: TopNavProps) {
    return (
        <header
            className={cn(
                "flex h-16 items-center justify-between border-b bg-background/95 px-4 md:px-6 backdrop-blur supports-[backdrop-filter]:bg-background/60",
                className
            )}
        >
            <div className="flex items-center gap-2 md:gap-4">
                <MobileNav />
                <div className="relative hidden w-96 md:block">
                    <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                    <input
                        type="text"
                        placeholder="Search ideas, reports, or market data..."
                        className="h-10 w-full rounded-full border bg-muted/50 pl-10 pr-4 text-sm transition-all focus:border-primary focus:bg-background focus:outline-none focus:ring-1 focus:ring-primary"
                    />
                </div>
            </div>

            <div className="flex items-center gap-4">
                <ThemeToggle />

                <button className="relative flex h-9 w-9 items-center justify-center rounded-full transition-colors hover:bg-accent hover:text-accent-foreground">
                    <Bell className="h-5 w-5" />
                    <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-red-500 ring-2 ring-background"></span>
                </button>

                <div className="flex items-center gap-3 border-l pl-4">
                    <div className="flex flex-col items-end text-right">
                        <span className="text-sm font-medium">Alex Chen</span>
                        <span className="text-xs text-muted-foreground">Premium Plan</span>
                    </div>
                    <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10 text-primary">
                        <User className="h-5 w-5" />
                    </div>
                </div>
            </div>
        </header>
    );
}
