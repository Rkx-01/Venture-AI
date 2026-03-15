import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";
import { MarketAnalysisResponse } from "../types/api";

export const useMarketAnalyses = () => {
    return useQuery<MarketAnalysisResponse[], Error>({
        queryKey: ["market-analyses"],
        queryFn: async () => {
            const response = await api.get<MarketAnalysisResponse[]>("/market-analysis");
            return response.data;
        },
    });
};
