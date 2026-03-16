from typing import Dict, Any, List

class CompetitorAnalysisService:
    """
    Extracts structured competitor arrays from the master evaluation JSON.
    """
    def extract_competitors(self, master_json: Dict[str, Any]) -> List[Dict[str, str]]:
        competitors = master_json.get("competitors", [])
        extracted = []
        for comp in competitors:
            extracted.append({
                "name": comp.get("name", "Unknown Competitor"),
                "description": comp.get("description", "No description provided."),
                "strengths": comp.get("strengths", comp.get("strength", "Unknown strengths")),
                "weaknesses": comp.get("weaknesses", comp.get("weakness", "Unknown weaknesses"))
            })
        return extracted
