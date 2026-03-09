from typing import List
from serpapi import GoogleSearch
from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

def search_competitors(idea_text: str) -> List[str]:
    """
    Uses SerpAPI to find real-world competitors in the Indian market.
    """
    serpapi_key = settings.SERPAPI_KEY
    if not serpapi_key:
        logger.warning("SERPAPI_KEY not found. Skipping real-time competitor search.")
        return []

    try:
        query = f"top startups in India for {idea_text}"
        logger.info(f"Searching SerpAPI for competitors: {query}")
        
        search = GoogleSearch({
            "q": query,
            "location": "India",
            "hl": "en",
            "gl": "in",
            "api_key": serpapi_key.get_secret_value()
        })
        
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        
        competitors = []
        for res in organic_results:
            title = res.get("title", "")
            # Basic heuristic: extract first word or two from title as potential company name
            # Or use snippets. For now, let's extract titles and let LLM filter.
            if title:
                competitors.append(title)
        
        # Limit to top 10 results to avoid prompt bloat
        return list(set(competitors))[:10]
        
    except Exception as e:
        logger.error(f"SerpAPI search failed: {e}")
        return []
