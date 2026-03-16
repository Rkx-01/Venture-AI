from typing import Dict, Any, List

class SwotService:
    """
    Extracts the SWOT arrays from the master evaluation JSON.
    """
    def extract_swot(self, master_json: Dict[str, Any]) -> Dict[str, List[str]]:
        swot = master_json.get("swot", {})
        return {
            "strengths": swot.get("strengths", ["No strengths identified."]),
            "weaknesses": swot.get("weaknesses", ["No weaknesses identified."]),
            "opportunities": swot.get("opportunities", ["No opportunities identified."]),
            "threats": swot.get("threats", ["No threats identified."])
        }
