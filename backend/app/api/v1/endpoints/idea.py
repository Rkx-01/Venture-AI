"""
api/v1/endpoints/idea.py
-------------------------
FastAPI router for startup idea analysis.
Exposes the IdeaAnalysisService via a REST endpoint.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from app.schemas.idea_schema import IdeaRequest
from app.services.startup_evaluation_service import StartupEvaluationService
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

evaluation_service = StartupEvaluationService()

@router.post(
    "/evaluate-startup",
    status_code=status.HTTP_200_OK,
    summary="Analyze a startup idea",
    description="Accepts a startup idea and runs a full evaluation pipeline."
)
async def analyze_idea_endpoint(request: IdeaRequest):
    """
    POST /api/v1/analyze-idea
    Receives a startup idea and returns the full evaluation result.
    """
    logger.info("Incoming request: POST /api/v1/analyze-idea | idea_length: %d", len(request.idea_text))
    
    try:
        # Business logic is encapsulated in the pipeline
        result = await evaluation_service.evaluate_idea(request.idea_text)
        
        logger.info("Successfully processed evaluation pipeline.")
        return result

    except ValueError as e:
        logger.error("Validation error in idea analysis: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except RuntimeError as e:
        logger.error("Service failure in idea analysis: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The analysis service is temporarily unavailable. Please try again later."
        )

    except Exception as e:
        logger.critical("Unexpected error in analyze_idea_endpoint: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        )
