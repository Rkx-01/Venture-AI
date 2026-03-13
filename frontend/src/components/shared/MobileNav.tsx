"use client";

import * as React from "react";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Separator } from "@/components/ui/separator";
import Link from "next/link";

export function MobileNav() {
    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="md:hidden">
                    <Menu className="h-6 w-6" />
                    <span className="sr-only">Toggle menu</span>
                </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-[300px] sm:w-[400px]">
                <nav className="flex flex-col gap-4">
                    <Link href="/" className="text-lg font-bold">
                        Venture AI
                    </Link>
                    <Separator />
                    <Link href="/analyze" className="text-md font-medium">
                        Analyze
                    </Link>
                    <Link href="/competitors" className="text-md font-medium">
                        Competitors
                    </Link>
                    <Link href="/reports" className="text-md font-medium">
                        Reports
                    </Link>
                </nav>
            </SheetContent>
        </Sheet>
    );
}
