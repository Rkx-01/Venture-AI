"use client";

import { toast as sonnerToast } from "sonner";
import { CheckCircle2, AlertCircle, Info, Loader2 } from "lucide-react";

type ToastOptions = {
    title: string;
    description?: string;
    duration?: number;
};

export const toast = {
    success: ({ title, description, duration = 4000 }: ToastOptions) => {
        return sonnerToast(title, {
            description,
            duration,
            icon: <CheckCircle2 className="h-4 w-4 text-emerald-500" />,
            className: "group border-emerald-500/20 bg-emerald-50/50 dark:bg-emerald-950/20",
        });
    },

    error: ({ title, description, duration = 6000 }: ToastOptions) => {
        return sonnerToast(title, {
            description,
            duration,
            icon: <AlertCircle className="h-4 w-4 text-destructive" />,
            className: "group border-destructive/20 bg-destructive/5 dark:bg-destructive/10",
        });
    },

    info: ({ title, description, duration = 4000 }: ToastOptions) => {
        return sonnerToast(title, {
            description,
            duration,
            icon: <Info className="h-4 w-4 text-primary" />,
        });
    },

    loading: ({ title, description }: ToastOptions) => {
        return sonnerToast(title, {
            description,
            duration: Infinity,
            icon: <Loader2 className="h-4 w-4 animate-spin text-primary" />,
        });
    },

    dismiss: (toastId?: string | number) => sonnerToast.dismiss(toastId),
};
