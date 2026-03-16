from typing import Dict, Any

class MarketAnalysisService:
    """
    Extracts market insights structural data from the master evaluation JSON.
    """
    def extract_market_insights(self, master_json: Dict[str, Any]) -> Dict[str, str]:
        market_insights = master_json.get("market_insights", {})
        return {
            "tam": market_insights.get("tam_india") or market_insights.get("tam", "TAM not generated."),
            "sam": market_insights.get("sam_india") or market_insights.get("sam", "SAM not generated."),
            "som": market_insights.get("som_india") or market_insights.get("som", "SOM not generated."),
            "trends": market_insights.get("indian_market_trends") or market_insights.get("trends", "No trends generated."),
            "opportunity": market_insights.get("opportunity", "No opportunity defined.")
        }
