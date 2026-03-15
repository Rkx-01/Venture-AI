import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 5 * 60 * 1000, 
            retry: 2,
            refetchOnWindowFocus: false, 
        },
        mutations: {
            onError: (error) => {
                
                if (process.env.NODE_ENV === "development") {
                    console.error("[React Query Mutation Error]", error);
                }
            },
        },
    },
});
