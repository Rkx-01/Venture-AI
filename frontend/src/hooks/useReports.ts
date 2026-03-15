import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";

export const useReports = () => {
    return useQuery({
        queryKey: ["reports"],
        queryFn: async () => {
            const response = await api.get("/reports");
            return response.data;
        },
    });
};
