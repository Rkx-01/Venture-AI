import os
from serpapi import GoogleSearch
import logging

logger = logging.getLogger(__name__)

class SerpApiClient:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY", "dummy_key")

    def search_companies(self, query: str) -> list[str]:
        """
        Perform a Google search to discover competitor companies based on the given query.
        Returns a list of extracted company names or relevant search result titles.
        """
        logger.info(f"Searching SerpAPI for query: {query}")
        
        # If no real key is provided, optionally return mock data to prevent crashes
        if not self.api_key or self.api_key in ["your_serpapi_key_here", "dummy_key"]:
            logger.warning("No valid SERPAPI_KEY found. Returning mock competitor search results.")
            return ["Mock Notion AI", "Mock Motion", "Mock Clockwise", "Mock Reclaim AI"]

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": 5  # Top 5 results
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            organic_results = results.get("organic_results", [])
            companies = []
            
            for result in organic_results:
                title = result.get("title", "")
                if title:
                    # simplistic extraction: take the title up to the first dash or pipe
                    clean_title = title.split(" - ")[0].split(" | ")[0].strip()
                    if clean_title and clean_title not in companies:
                        companies.append(clean_title)
            
            return companies[:4]
            
        except Exception as e:
            logger.error(f"Failed to execute SerpAPI search: {str(e)}")
            return []

serpapi_client = SerpApiClient()
