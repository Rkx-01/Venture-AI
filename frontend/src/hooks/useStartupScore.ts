import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";

export const useStartupScore = () => {
    return useQuery({
        queryKey: ["startup-score"],
        queryFn: async () => {
            const response = await api.get("/startup-score");
            return response.data;
        },
    });
};
