"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import { DASHBOARD_NAV_ITEMS, SETTINGS_NAV_ITEM } from "@/lib/navigation";
import { ChevronLeft, ChevronRight, Zap } from "lucide-react";

interface SidebarProps {
    className?: string;
}

export function Sidebar({ className }: SidebarProps) {
    const [isCollapsed, setIsCollapsed] = React.useState(false);
    const pathname = usePathname();

    return (
        <motion.aside
            initial={false}
            animate={{ width: isCollapsed ? 64 : 256 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className={cn(
                "relative flex flex-col border-r bg-card h-screen z-40 shadow-sm",
                className
            )}
        >
            <div className="flex h-16 items-center px-4 overflow-hidden">
                <Link href="/" className="flex items-center gap-3 font-bold text-primary shrink-0">
                    <motion.div
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        whileTap={{ scale: 0.9 }}
                        className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-lg shadow-primary/20"
                    >
                        <Zap className="h-5 w-5 fill-current" />
                    </motion.div>
                    <AnimatePresence>
                        {!isCollapsed && (
                            <motion.span
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -10 }}
                                className="truncate text-xl font-black tracking-tight"
                            >
                                VentureAI
                            </motion.span>
                        )}
                    </AnimatePresence>
                </Link>
            </div>

            <div className="flex-1 space-y-2 px-3 py-6 overflow-y-auto overflow-x-hidden custom-scrollbar">
                {DASHBOARD_NAV_ITEMS.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link key={item.href} href={item.href}>
                            <motion.div
                                whileHover={{ x: 4 }}
                                transition={{ type: "spring", stiffness: 400, damping: 20 }}
                                className={cn(
                                    "group relative flex items-center rounded-xl px-3 py-2.5 text-sm font-semibold transition-all duration-200",
                                    isActive
                                        ? "bg-primary text-primary-foreground shadow-md shadow-primary/10"
                                        : "text-muted-foreground hover:bg-accent/50 hover:text-foreground",
                                    isCollapsed && "justify-center px-0"
                                )}
                            >
                                <item.icon className={cn("h-5 w-5 shrink-0", !isCollapsed && "mr-3")} />
                                {!isCollapsed && (
                                    <motion.span
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        className="truncate"
                                    >
                                        {item.label}
                                    </motion.span>
                                )}
                                {isActive && (
                                    <motion.div
                                        layoutId="sidebar-active"
                                        className="absolute inset-0 bg-primary rounded-xl -z-10"
                                        transition={{ type: "spring", stiffness: 350, damping: 30 }}
                                    />
                                )}
                            </motion.div>
                        </Link>
                    );
                })}
            </div>

            <div className="border-t p-3 bg-muted/5">
                <Link href={SETTINGS_NAV_ITEM.href}>
                    <motion.div
                        whileHover={{ x: 4 }}
                        className={cn(
                            "group flex items-center rounded-xl px-3 py-2.5 text-sm font-semibold transition-all duration-200",
                            pathname === SETTINGS_NAV_ITEM.href
                                ? "bg-primary text-primary-foreground shadow-md"
                                : "text-muted-foreground hover:bg-accent/50 hover:text-foreground",
                            isCollapsed && "justify-center px-0"
                        )}
                    >
                        <SETTINGS_NAV_ITEM.icon className={cn("h-5 w-5 shrink-0", !isCollapsed && "mr-3")} />
                        {!isCollapsed && <span>{SETTINGS_NAV_ITEM.label}</span>}
                    </motion.div>
                </Link>
            </div>

            <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setIsCollapsed(!isCollapsed)}
                className="absolute -right-3 top-20 flex h-7 w-7 items-center justify-center rounded-full border bg-background text-muted-foreground shadow-lg transition-colors hover:text-primary hover:border-primary/50"
            >
                {isCollapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
            </motion.button>
        </motion.aside>
    );
}
