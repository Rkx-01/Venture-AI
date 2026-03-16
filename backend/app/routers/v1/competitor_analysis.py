from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post("", status_code=status.HTTP_410_GONE)
async def analyze_competitors():
    raise HTTPException(status_code=410, detail="Use POST /api/evaluate-startup for full competitor analysis.")
