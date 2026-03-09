from typing import List
from serpapi import GoogleSearch
from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

def search_market_data(idea_text: str) -> List[str]:
    """
    Uses SerpAPI to find real-world market data for the Indian market.
    """
    serpapi_key = settings.SERPAPI_KEY
    if not serpapi_key:
        logger.warning("SERPAPI_KEY not found. Skipping real-time market research.")
        return []

    try:
        query = f"{idea_text} market size India TAM SAM SOM startup industry"
        logger.info(f"Searching SerpAPI for market data: {query}")
        
        search = GoogleSearch({
            "q": query,
            "location": "India",
            "hl": "en",
            "gl": "in",
            "api_key": serpapi_key.get_secret_value()
        })
        
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        
        market_insights = []
        for res in organic_results:
            title = res.get("title", "")
            snippet = res.get("snippet", "")
            if title and snippet:
                market_insights.append(f"{title}: {snippet}")
            elif title:
                market_insights.append(title)
        
        # Limit to top 5 results to keep prompt concise but informative
        return market_insights[:5]
        
    except Exception as e:
        logger.error(f"SerpAPI market research failed: {e}")
        return []
