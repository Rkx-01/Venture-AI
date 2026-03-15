import { create } from "zustand";
import { devtools } from "zustand/middleware";
import type {
    IdeaAnalysisResponse,
    MarketAnalysisResponse,
    CompetitorAnalysisResponse,
    StartupScoreResponse,
    ReportResponse,
} from "@/types/api";

// ------------------------------------------------
// State shape
// ------------------------------------------------

export type AnalysisStep =
    | "idle"
    | "idea"
    | "market"
    | "competitors"
    | "score"
    | "report"
    | "complete"
    | "error";

interface AnalysisState {
    // The raw idea text entered by the user
    currentIdea: string | null;

    // Active pipeline step for progress UI
    currentStep: AnalysisStep;

    // Results from each analysis step
    ideaAnalysis: IdeaAnalysisResponse | null;
    marketAnalysis: MarketAnalysisResponse | null;
    competitorAnalysis: CompetitorAnalysisResponse | null;
    startupScore: StartupScoreResponse | null;
    report: ReportResponse | null;

    // ------------------------------------------------
    // Actions
    // ------------------------------------------------
    setCurrentIdea: (idea: string) => void;
    setCurrentStep: (step: AnalysisStep) => void;
    setIdeaAnalysis: (data: IdeaAnalysisResponse) => void;
    setMarketAnalysis: (data: MarketAnalysisResponse) => void;
    setCompetitorAnalysis: (data: CompetitorAnalysisResponse) => void;
    setStartupScore: (data: StartupScoreResponse) => void;
    setReport: (data: ReportResponse) => void;

    /** Clears all analysis state to reset for a new idea submission */
    resetAnalysis: () => void;
}

const initialState = {
    currentIdea: null,
    currentStep: "idle" as AnalysisStep,
    ideaAnalysis: null,
    marketAnalysis: null,
    competitorAnalysis: null,
    startupScore: null,
    report: null,
};

export const useAnalysisStore = create<AnalysisState>()(
    devtools(
        (set) => ({
            ...initialState,

            setCurrentIdea: (idea) => set({ currentIdea: idea }, false, "setCurrentIdea"),

            setCurrentStep: (step) => set({ currentStep: step }, false, "setCurrentStep"),

            setIdeaAnalysis: (data) => set({ ideaAnalysis: data }, false, "setIdeaAnalysis"),

            setMarketAnalysis: (data) => set({ marketAnalysis: data }, false, "setMarketAnalysis"),

            setCompetitorAnalysis: (data) =>
                set({ competitorAnalysis: data }, false, "setCompetitorAnalysis"),

            setStartupScore: (data) => set({ startupScore: data }, false, "setStartupScore"),

            setReport: (data) => set({ report: data }, false, "setReport"),

            resetAnalysis: () => set(initialState, false, "resetAnalysis"),
        }),
        { name: "AnalysisStore" }
    )
);
