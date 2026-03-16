from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post("", status_code=status.HTTP_410_GONE)
async def get_startup_score():
    raise HTTPException(status_code=410, detail="Use POST /api/evaluate-startup which includes a startup score.")
