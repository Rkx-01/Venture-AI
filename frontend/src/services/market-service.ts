import { api } from "@/lib/api-client";

export interface MarketAnalysisRequest {
    industry: string;
    target_users: string;
    solution_type: string;
}

export interface MarketAnalysisResult {
    tam: string;
    sam: string;
    som: string;
    growth_rate: string;
    reasoning: string;
}

export const marketService = {
    analyzeMarket: async (data: MarketAnalysisRequest) => {
        const response = await api.post<MarketAnalysisResult>("/analyze-market", data);
        return response.data;
    }
};
