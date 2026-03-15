import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";

export const useIdeas = () => {
    return useQuery({
        queryKey: ["ideas"],
        queryFn: async () => {
            const response = await api.get("/ideas");
            return response.data;
        },
    });
};
