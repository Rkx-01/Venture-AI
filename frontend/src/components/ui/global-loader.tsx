"use client";

import { useIsFetching, useIsMutating } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

export function GlobalLoader() {
    const isFetching = useIsFetching();
    const isMutating = useIsMutating();

    
    const isGlobalLoading = isFetching > 0 || isMutating > 0;

    
    const [show, setShow] = useState(false);

    useEffect(() => {
        if (isGlobalLoading) {
            setShow(true);
        } else {
            
            
            const timer = setTimeout(() => setShow(false), 500);
            return () => clearTimeout(timer);
        }
    }, [isGlobalLoading]);

    
    if (!show && !isGlobalLoading) return null;

    return (
        <div
            className="fixed inset-x-0 top-0 z-[100] h-1 pointer-events-none"
            role="progressbar"
            aria-hidden={!isGlobalLoading}
        >
            <div
                className={cn(
                    "h-full bg-primary transition-all ease-in-out",
                    
                    
                    isGlobalLoading ? "w-[80%] duration-[3000ms]" : "w-full duration-300 opacity-0"
                )}
            />
        </div>
    );
}
