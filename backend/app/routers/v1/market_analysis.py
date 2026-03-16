from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("")
async def list_market_analyses():
    raise HTTPException(status_code=410, detail="Use POST /api/evaluate-startup which includes market insights.")


@router.post("")
async def analyze_market():
    raise HTTPException(status_code=410, detail="Use POST /api/evaluate-startup which includes market insights.")


@router.post("/trends")
async def analyze_industry_trends():
    raise HTTPException(status_code=410, detail="Use POST /api/evaluate-startup which includes market trends.")
