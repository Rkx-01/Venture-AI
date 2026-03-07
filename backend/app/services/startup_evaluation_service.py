import json
from typing import Dict, Any
from fastapi import HTTPException
from app.ai.llm_client import LLMClient
from app.utils.logger import get_logger

from app.services.idea_analysis_service import IdeaAnalysisService
from app.services.market_analysis_service import MarketAnalysisService
from app.services.competitor_analysis_service import CompetitorAnalysisService
from app.services.swot_service import SwotService
from app.services.startup_scoring_service import StartupScoringService
from app.services.report_service import ReportService
from app.services.market_entry_difficulty_service import MarketEntryDifficultyService
from app.services.competitor_search_service import search_competitors
from app.services.market_research_service import search_market_data

logger = get_logger(__name__)

class StartupEvaluationService:
    """
    Unified evaluation orchestrator. 
    It runs a single LLM prompt to generate the entire startup analysis,
    then uses granular sub-services to extract and structure the data.
    """
    def __init__(self):
        self.llm = LLMClient()
        
        # Initialize the parsing microservices
        self.idea_service = IdeaAnalysisService()
        self.market_service = MarketAnalysisService()
        self.competitor_service = CompetitorAnalysisService()
        self.swot_service = SwotService()
        self.scoring_service = StartupScoringService()
        self.report_service = ReportService()
        self.difficulty_service = MarketEntryDifficultyService()

    def _clean_json(self, text: str) -> str:
        """Cleans AI output to extract valid JSON."""
        import re
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        # Find the first { and last }
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            text = text[start:end+1]
        
        # Remove trailing commas before closing braces/brackets
        text = re.sub(r',\s*([\]}])', r'\1', text)
        return text.strip()

    async def evaluate_startup(self, idea_text: str) -> Dict[str, Any]:
        """
        Executes the monolithic AI analysis and maps it to the precise final dictionary.
        Strictly returns real AI data or raises an error.
        """
        logger.info("Executing comprehensive single-pass startup analysis...")
        
        # 1. Real-time discovery via SerpAPI
        discovered_competitors = search_competitors(idea_text)
        market_research_data = search_market_data(idea_text)

        competitor_injection = ""
        if discovered_competitors:
            competitor_injection = f"\nThese companies currently operate in this market in India: {', '.join(discovered_competitors)}. Use them when performing the competitor analysis."

        market_data_injection = ""
        if market_research_data:
            market_data_injection = "\nHere is real market research data from the Indian startup ecosystem:\n" + "\n".join([f"- {item}" for item in market_research_data]) + "\nUsing this information estimate TAM, SAM, SOM and trends."

        system_prompt = (
            "You are an experienced venture capitalist and startup analyst specializing in the Indian startup ecosystem. "
            "You provide highly detailed, realistic, and structured data analysis specifically for the Indian market."
        )

        user_prompt = f"""
        Analyze the following startup idea specifically within the Indian market context.{competitor_injection}{market_data_injection}

        Startup Idea:
        {idea_text}
        
        Provide a structured analysis including:

        1. idea_summary: Explain the concept clearly.
        2. target_users: Describe the primary customer segments in India.
        3. market_insights: Provide estimates specifically for India:
           - TAM (Total Addressable Market in India)
           - SAM (Serviceable Available Market in India)
           - SOM (Serviceable Obtainable Market in India)
           - Indian market trends and growth potential.
        4. market_entry_difficulty: Analyze how difficult it would be for a new startup to enter this market in India.
           Consider factors such as:
           - number of existing competitors
           - capital requirements
           - technology complexity
           - regulatory barriers
           - customer acquisition difficulty
           Return a difficulty rating (level) and specific reasons.
        5. competitors: List at least 5 competitors operating in India or targeting the Indian market. Include name, description, strengths, and weaknesses.
6. swot: Provide detailed strengths, weaknesses, opportunities in India, and threats in the Indian market.
7. score_breakdown: Rate the startup idea on the following factors from 1-10:
           - market_opportunity
           - competition_level (1=Very High Competition, 10=Blue Ocean/No Competition)
           - scalability
           - execution_difficulty (1=Extremely Difficult, 10=Easy to Execute)
           - innovation
8. investment_recommendation: Provide a clear investment recommendation with strategic rationale for an India-based investor.
9. report: Generate a comprehensive executive intelligence report focused on the Indian opportunity.

        Return the result STRICTLY as a JSON object using exactly this schema:
        {{
            "idea_summary": "...",
            "target_users": "...",
            "market_insights": {{
                "tam_india": "...",
                "sam_india": "...",
                "som_india": "...",
                "indian_market_trends": "..."
            }},
            "market_entry_difficulty": {{
                "level": "Low/Medium/High",
                "reasons": ["...", "...", "..."]
            }},
            "competitors": [
                {{
                    "name": "...",
                    "description": "...",
                    "strengths": "...",
                    "weaknesses": "..."
                }}
            ],
            "swot": {{
                "strengths": ["...", "..."],
                "weaknesses": ["...", "..."],
                "opportunities": ["...", "..."],
                "threats": ["...", "..."]
            }},
            "score_breakdown": {{
                "market_opportunity": 0,
                "competition_level": 0,
                "scalability": 0,
                "execution_difficulty": 0,
                "innovation": 0
            }},
            "investment_recommendation": "...",
            "report": "..."
        }}
        """

        try:
            # Enforce JSON-mode parsing from the LLM
            result_json_str = await self.llm.generate_chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.4,
                max_tokens=4500,
                # Default to True for JSON-heavy backend services
                response_format_json=True
            )
            
            try:
                master_data = json.loads(result_json_str)
            except json.JSONDecodeError:
                logger.warning("Standard JSON parse failed, attempting deep clean...")
                cleaned_json = self._clean_json(result_json_str)
                master_data = json.loads(cleaned_json)
                
            logger.info("Successfully received generated payload from AI.")
            
        except (json.JSONDecodeError, Exception) as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "rate limit" in error_msg or "429" in error_msg or "resource_exhausted" in error_msg:
                logger.error(f"AI Quota Exceeded: {e}")
                raise HTTPException(
                    status_code=503,
                    detail="AI analysis service is currently busy due to high demand (quota reached). Please try again in a few minutes."
                )
            
            logger.error(f"AI Analysis Failed: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Neural engine encountered a critical failure. System diagnosis: {str(e)}"
            )

        # Orchestrate the structured extraction via microservices
        logger.info("Extracting data slices via microservices...")
        
        idea_data = self.idea_service.extract_idea_analysis(master_data)
        market_data = self.market_service.extract_market_insights(master_data)
        competitor_data = self.competitor_service.extract_competitors(master_data)
        swot_data = self.swot_service.extract_swot(master_data)
        score_data = self.scoring_service.extract_score(master_data)
        report_data = self.report_service.extract_report(master_data)
        difficulty_data = self.difficulty_service.extract_difficulty(master_data)

        # Build and return the final clean composition matching the UI requirements
        logger.info("Pipeline extraction complete.")
        return {
            "idea_summary": idea_data["idea_summary"],
            "target_users": idea_data["target_users"],
            "market_insights": market_data,
            "market_entry_difficulty": difficulty_data,
            "competitors": competitor_data,
            "swot": swot_data,
            "startup_score": score_data["startup_score"],
            "score_breakdown": score_data.get("score_breakdown", {}),
            "investment_recommendation": report_data["investment_recommendation"],
            "report": report_data["report"]
        }
