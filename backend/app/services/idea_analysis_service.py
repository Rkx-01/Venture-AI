from typing import Dict, Any

class IdeaAnalysisService:
    """
    Extracts idea analysis components from the master evaluation JSON.
    """
    def extract_idea_analysis(self, master_json: Dict[str, Any]) -> Dict[str, str]:
        return {
            "idea_summary": master_json.get("idea_summary", "No summary provided."),
            "problem_statement": master_json.get("problem_statement", "No problem statement provided."),
            "target_users": master_json.get("target_users", "No target users identified."),
            "revenue_model": master_json.get("revenue_model", "No revenue model provided."),
            "industry": master_json.get("industry", "General")
        }
