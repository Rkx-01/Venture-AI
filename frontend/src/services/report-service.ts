import { api } from "@/lib/api-client";

export interface StartupReport {
    id: string;
    idea_id: string;
    title: string;
    sections: {
        executive_summary: string;
        problem_solution: any;
        market_opportunity: any;
        competitor_landscape: any;
        startup_score: any;
    };
    created_at: string;
}

export const reportService = {
    generateReport: async (ideaId: string) => {
        const response = await api.post<{ report_id: string }>("/generate-report", { idea_id: ideaId });
        return response.data;
    },

    getReport: async (reportId: string) => {
        const response = await api.get<StartupReport>(`/reports/${reportId}`);
        return response.data;
    },

    downloadReportPdf: (reportId: string) =>
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/reports/${reportId}/download`,
};
