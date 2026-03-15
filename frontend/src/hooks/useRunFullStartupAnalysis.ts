import { useMutation } from "@tanstack/react-query";
import { useAnalysisStore } from "@/store/analysisStore";
import { ideaService } from "@/services/ideaService";
import { toast } from "sonner";

interface RunAnalysisInput {
    idea_text: string;
    industry?: string;
    startup_idea_id: number;
}

export const useRunFullStartupAnalysis = () => {
    const {
        setCurrentIdea,
        setCurrentStep,
        setIdeaAnalysis,
        resetAnalysis,
    } = useAnalysisStore();

    return useMutation({
        mutationFn: async ({ idea_text }: RunAnalysisInput) => {
            resetAnalysis();
            setCurrentIdea(idea_text);

            // ── Step 1: Idea Analysis ────────────────────────────────────────
            setCurrentStep("idea");
            const ideaResult = await ideaService.analyzeIdea(idea_text);
            setIdeaAnalysis(ideaResult);

            // Since the new service returns EVERYTHING in one pass,
            // we skip the granular market/competitor service calls.
            // We just set the final state.
            
            setCurrentStep("complete");

            return ideaResult;
        },

        onSuccess: () => {
            toast.success("Full analysis complete!", {
                description: "All analysis steps completed successfully via the unified engine.",
            });
        },

        onError: (error: unknown) => {
            useAnalysisStore.getState().setCurrentStep("error");
            const err = error as Error;
            toast.error("Analysis pipeline failed", {
                description: err?.message || "An error occurred during the analysis. Please try again.",
            });
        },
    });
};
