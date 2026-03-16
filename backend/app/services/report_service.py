from typing import Dict, Any

class ReportService:
    """
    Extracts the final report string and investment recommendation from the master evaluation JSON.
    """
    def extract_report(self, master_json: Dict[str, Any]) -> Dict[str, str]:
        return {
            "investment_recommendation": master_json.get("investment_recommendation", "No recommendation provided."),
            "report": master_json.get("report", "No final report generated.")
        }
