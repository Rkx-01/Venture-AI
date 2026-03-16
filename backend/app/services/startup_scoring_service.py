from typing import Dict, Any

class StartupScoringService:
    """
    Deterministic weighted scoring engine for startups.
    """
    
    # Static weights as per requirement
    WEIGHTS = {
        "market_opportunity": 0.30,
        "competition_level": 0.20,
        "scalability": 0.25,
        "execution_difficulty": 0.15,
        "innovation": 0.10
    }

    def calculate_startup_score(self, scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes a final weighted score based on individual factor ratings.
        Ratings should be from 1-10.
        """
        final_score = 0.0
        
        # Ensure we use safe defaults if keys are missing
        for factor, weight in self.WEIGHTS.items():
            rating = float(scores.get(factor, 5.0))  # Default to 5.0 (neutral) if missing
            final_score += rating * weight
            
        return {
            "startup_score": round(final_score, 2),
            "score_breakdown": {
                factor: float(scores.get(factor, 0.0)) for factor in self.WEIGHTS.keys()
            }
        }

    def extract_score(self, master_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Legacy/Backup: Previously extracted raw score, now uses the deterministic calculator.
        """
        breakdown = master_json.get("score_breakdown", {})
        if not breakdown:
            # Fallback if AI didn't provide a breakdown but provided a raw score
            return {
                "startup_score": float(master_json.get("startup_score", 0.0)),
                "risk_level": master_json.get("risk_level", "Unknown"),
                "investment_potential": master_json.get("investment_potential", "Unknown")
            }
            
        return self.calculate_startup_score(breakdown)
