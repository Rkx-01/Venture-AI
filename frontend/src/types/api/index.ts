

export interface MarketInsights {
    tam: string;
    sam: string;
    som: string;
    trends: string;
}

export interface CompetitorDetail {
    name: string;
    description: string;
    strengths: string;
    weaknesses: string;
}

export interface SWOTAnalysis {
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
    threats: string[];
}

export interface IdeaAnalysisResponse {
    idea_summary: string;
    target_users: string;
    market_insights: MarketInsights;
    market_entry_difficulty: {
        level: string;
        reasons: string[];
    };
    competitors: CompetitorDetail[];
    swot: SWOTAnalysis;
    startup_score: number;
    score_breakdown: {
        market_opportunity: number;
        competition_level: number;
        scalability: number;
        innovation: number;
    };
    investment_recommendation: string;
    report: string;
}

export interface MarketAnalysisResponse {
    industry: string;
    tam: string;
    sam: string;
    som: string;
    reasoning: string;
    industry_growth_rate: string;
    market_opportunity_score: number;
}

export interface Competitor {
    name: string;
    description: string;
    product_category: string;
    market_focus: string;
    strengths: string[];
    weaknesses: string[];
}

export interface CompetitorAnalysisResponse {
    competitors: Competitor[];
    summary: string;
}

export interface StartupScoreResponse {
    market_potential_score: number;
    competition_score: number;
    scalability_score: number;
    execution_risk_score: number;
    overall_startup_score: number;
    success_probability: string;
    executive_summary: string;
}

export interface ReportResponse {
    executive_summary: string;
    problem_solution_analysis: string;
    market_opportunity: string;
    competitor_landscape: string;
    startup_score_summary: string;
    markdown_report: string;
}
