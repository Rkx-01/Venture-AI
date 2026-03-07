from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.utils.idea_validation import validate_startup_idea
from app.services.startup_evaluation_service import StartupEvaluationService
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


class EvaluateStartupRequest(BaseModel):
    idea_text: str


@router.get("")
async def test_evaluate_startup_reachability():
    """Diagnostic endpoint to verify connectivity."""
    return {"status": "ok", "message": "Evaluation endpoint is reachable via GET"}


@router.post("")
async def evaluate_startup_endpoint(request: EvaluateStartupRequest):
    """
    Evaluates a given startup idea and generates a comprehensive report.
    Returns structured JSON with idea summary, market insights, competitors,
    SWOT analysis, startup score, and investment recommendations.
    """
    logger.info(f"Received request to evaluate startup idea: {request.idea_text[:50]}...")
    
    # Input Validation
    if not validate_startup_idea(request.idea_text):
        logger.warning(f"Invalid startup idea rejected: {request.idea_text}")
        raise HTTPException(
            status_code=400,
            detail="Invalid input: Please enter a meaningful startup idea. Example: AI tool for helping students learn coding."
        )

    try:
        evaluator = StartupEvaluationService()
        data = await evaluator.evaluate_startup(request.idea_text)
        logger.info("Successfully completed startup evaluation.")
        # Return raw dict to avoid Pydantic strict validation issues
        return JSONResponse(content=data)
    except HTTPException:
        # Re-raise HTTP exceptions (like 503 Quota) so the global handler catch them
        raise
    except Exception as e:
        logger.error(f"Unexpected error evaluating startup: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Neural engine encountered an internal failure. System diagnosis: {str(e)}"
        )
