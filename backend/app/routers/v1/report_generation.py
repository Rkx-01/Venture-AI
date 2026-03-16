from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("")
async def list_reports():
    raise HTTPException(status_code=410, detail="Use POST /api/evaluate-startup for full startup reports.")


@router.post("/generate-report")
async def generate_startup_report():
    raise HTTPException(status_code=410, detail="Use POST /api/evaluate-startup for full startup reports.")


@router.get("/reports/{report_id}/download")
async def download_report_pdf(report_id: str):
    raise HTTPException(status_code=410, detail="Report download is no longer supported via this endpoint.")
