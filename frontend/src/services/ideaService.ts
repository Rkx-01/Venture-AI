import { api } from "@/lib/api-client";
import { IdeaAnalysisResponse } from "@/types/api";

export interface AnalyzeIdeaRequest {
    idea_text: string;
    industry?: string;
}

/**
 * Service to handle communication with the backend Idea Analysis API.
 */
export const ideaService = {
    /**
     * Sends a startup idea to the backend and returns the AI-generated analysis.
     * 
     * @param data - The request payload containing the idea text.
     * @returns A promise resolving to the structured IdeaAnalysisResponse.
     */
    async analyzeIdea(data: string | AnalyzeIdeaRequest): Promise<IdeaAnalysisResponse> {
        try {
            const requestData = typeof data === "string" ? { idea_text: data } : data;
            console.log("Evaluating idea via consolidated service:", requestData.idea_text);

            // The root /evaluate-startup endpoint provides the full single-pass analysis
            const response = await api.post<IdeaAnalysisResponse>("/api/evaluate-startup", requestData);

            console.log("Analysis result received:", response.data);
            return response.data;
        } catch (error: any) {
            console.error("[ideaService] Error analyzing idea:", error);
            const errorMessage = error?.response?.data?.error || error?.response?.data?.detail || error.message || "Failed to analyze the startup idea.";
            throw new Error(errorMessage);
        }
    }
};

export const { analyzeIdea } = ideaService;
