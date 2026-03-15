import { useMutation } from "@tanstack/react-query";
import { ideaService, AnalyzeIdeaRequest } from "../services/ideaService";
import { IdeaAnalysisResponse } from "../types/api";

export const useAnalyzeIdea = () => {
    return useMutation<IdeaAnalysisResponse, Error, AnalyzeIdeaRequest>({
        mutationFn: (data: AnalyzeIdeaRequest) => ideaService.analyzeIdea(data),
    });
};
