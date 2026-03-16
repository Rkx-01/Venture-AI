from typing import Dict, Any

class MarketEntryDifficultyService:
    """
    Extracts Market Entry Difficulty data from the master evaluation JSON.
    """
    def extract_difficulty(self, master_json: Dict[str, Any]) -> Dict[str, Any]:
        difficulty = master_json.get("market_entry_difficulty", {})
        return {
            "level": difficulty.get("level", "Unknown"),
            "reasons": difficulty.get("reasons", [])
        }
