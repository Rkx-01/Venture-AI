"use client";

import * as React from "react";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { type Competitor } from "./CompetitorCard";

interface CompetitorTableProps {
    competitors: Competitor[];
}

export function CompetitorTable({ competitors }: CompetitorTableProps) {
    return (
        <div className="rounded-xl border-2 border-black overflow-hidden bg-white shadow-brutal">
            <Table>
                <TableHeader className="bg-muted/50">
                    <TableRow>
                        <TableHead className="font-bold uppercase text-[10px]">Competitor</TableHead>
                        <TableHead className="font-bold uppercase text-[10px]">Description</TableHead>
                        <TableHead className="font-bold uppercase text-[10px]">Primary Strength</TableHead>
                        <TableHead className="font-bold uppercase text-[10px]">Primary Weakness</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {competitors.map((comp) => (
                        <TableRow key={comp.id} className="hover:bg-muted/30">
                            <TableCell className="font-bold">{comp.name}</TableCell>
                            <TableCell className="text-xs max-w-xs">{comp.description}</TableCell>
                            <TableCell className="text-xs text-emerald-600 font-medium">
                                {Array.isArray(comp.strengths) ? comp.strengths.join(", ") : comp.strengths}
                            </TableCell>
                            <TableCell className="text-xs text-rose-600 font-medium">
                                {Array.isArray(comp.weaknesses) ? comp.weaknesses.join(", ") : comp.weaknesses}
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
}
