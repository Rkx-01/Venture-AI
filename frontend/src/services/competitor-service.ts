import { api } from "@/lib/api-client";

export interface Competitor {
    name: string;
    description: string;
    strengths: string[];
    weaknesses: string[];
    target_market: string;
    market_share?: string;
    pricing?: string;
    innovation_score: number;
    dominance_score: number;
}

export interface CompetitorAnalysisResult {
    competitors: Competitor[];
    market_gaps: string[];
    strategic_recommendations: string[];
}

export const competitorService = {
    getCompetitors: async (industry: string) => {
        const response = await api.get<CompetitorAnalysisResult>(`/competitors?industry=${encodeURIComponent(industry)}`);
        return response.data;
    },

    analyzeCompetitorLandscape: async (ideaId: string) => {
        const response = await api.post<CompetitorAnalysisResult>(`/analyze-competitors/${ideaId}`);
        return response.data;
    },
};
