"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Loader2 } from "lucide-react";
import { ideaService } from "@/services/ideaService";
import { cn } from "@/lib/utils";
import { useAnalysisStore } from "@/store/analysisStore";

const STEPS = [
  "Analyzing idea architecture",
  "Executing market research",
  "Discovering competitor landscape",
  "Computing startup viability score",
  "Generating final intelligence report",
];

function EvaluateContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const ideaText = searchParams.get("q");
  const setIdeaAnalysis = useAnalysisStore((state) => state.setIdeaAnalysis);
  const setCurrentIdea = useAnalysisStore((state) => state.setCurrentIdea);

  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!ideaText) {
      router.replace("/");
      return;
    }

    let isMounted = true;

    const totalSimulatedTime = 8000;
    const stepTime = totalSimulatedTime / STEPS.length;

    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < STEPS.length - 1) return prev + 1;
        clearInterval(interval);
        return prev;
      });
    }, stepTime);

    ideaService.analyzeIdea({ idea_text: ideaText })
      .then((result) => {
        if (!isMounted) return;

        try {
          setCurrentIdea(ideaText);
          setIdeaAnalysis(result);
        } catch (e) {
          console.error("Failed to save evaluation to store:", e);
        }

        setTimeout(() => {
          if (isMounted) router.push(`/result`);
        }, 2000);
      })
      .catch((err) => {
        if (!isMounted) return;
        clearInterval(interval);
        setError(err.message || "Neural engine encountered a critical failure.");
      });

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, [ideaText, router, setCurrentIdea, setIdeaAnalysis]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-[#F5F2EB] text-[#121212] p-6">
      <div className="absolute inset-0 z-0 opacity-[0.03] pointer-events-none"
        style={{ backgroundImage: 'linear-gradient(#09090B 2px, transparent 2px), linear-gradient(90deg, #09090B 2px, transparent 2px)', backgroundSize: '60px 60px' }} />

      <div className="w-full max-w-2xl border-4 border-black bg-white shadow-[8px_8px_0px_#000] p-8 relative z-10">
        <div className="border-b-4 border-black pb-6 mb-8 flex mx-4 justify-between items-end">
          <div>
            <h1 className="font-display text-4xl uppercase">Processing</h1>
            <p className="font-bold text-[#121212]/60 uppercase tracking-widest text-sm mt-2">
              System ID: {Math.floor(Math.random() * 9000) + 1000}-X
            </p>
          </div>
          <Loader2 className="h-12 w-12 text-[#FF6500] stroke-[#FF6500] animate-spin" />
        </div>

        {error ? (
          <div className="space-y-6">
            <div className="bg-[#FF6500] text-black p-6 border-4 border-black font-bold uppercase shadow-[4px_4px_0px_#09090B]">
              <div className="flex items-center gap-3 mb-2 text-xl">
                <span>⚠️ System Alert</span>
              </div>
              <div className="text-sm font-black leading-relaxed">
                {error.toLowerCase().includes("invalid input") ? (
                  "Please enter a meaningful startup idea instead of random text."
                ) : error.includes("busy") || error.includes("quota") ? (
                  "Our AI analysis service is currently busy due to high demand. Please try again in a few minutes."
                ) : (
                  error
                )}
              </div>
            </div>

            <button
              onClick={() => router.push("/")}
              className="w-full bg-[#0091B9] text-white font-bold uppercase py-4 border-4 border-black shadow-[4px_4px_0px_#000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all"
            >
              Return to Core Control
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {STEPS.map((step, index) => {
              const isActive = index === currentStep;
              const isPast = index < currentStep;

              return (
                <div
                  key={step}
                  className={cn(
                    "flex items-center gap-4 p-4 border-4 transition-all duration-300",
                    isActive ? "border-black bg-[#FFD500] translate-x-2" :
                      isPast ? "border-black/10 bg-[#F5F2EB] opacity-60" :
                        "border-transparent opacity-30 grayscale"
                  )}
                >
                  <div className={cn(
                    "h-6 w-6 flex items-center justify-center border-2 border-black",
                    isPast ? "bg-[#0091B9]" :
                      isActive ? "bg-white animate-pulse" :
                        "bg-transparent"
                  )}>
                    {isPast && <div className="h-2 w-2 bg-white" />}
                  </div>
                  <span className={cn(
                    "font-bold uppercase tracking-wide",
                    isActive ? "text-black" : "text-[#121212]"
                  )}>
                    {step}
                  </span>

                  {isActive && (
                    <span className="ml-auto text-xs font-bold animate-pulse text-black">
                      [ EXECUTING ]
                    </span>
                  )}
                  {isPast && (
                    <span className="ml-auto text-xs font-bold text-[#121212]">
                      [ DONE ]
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        )}

        <div className="mt-8 mx-4 pt-4 border-t-4 border-black flex justify-between text-xs font-bold uppercase text-[#121212]">
          <span>Engine: Integrated AI Engine</span>
          <span>Status: Analyzing</span>
        </div>
      </div>
    </div>
  );
}

export default function EvaluatePage() {
  return (
    <Suspense fallback={
      <div className="flex min-h-screen items-center justify-center bg-[#F5F2EB]">
        <Loader2 className="h-12 w-12 animate-spin text-[#FF6500]" />
      </div>
    }>
      <EvaluateContent />
    </Suspense>
  );
}
