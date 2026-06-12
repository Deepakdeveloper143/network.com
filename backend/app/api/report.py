from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

router = APIRouter()

class ReportRequest(BaseModel):
    report_type: str
    data: Optional[Dict] = None

class ReportResponse(BaseModel):
    report_id: str
    report_type: str
    generated_at: str
    status: str
    download_url: str
    summary: str

@router.post("/report/generate")
async def generate_report(request: ReportRequest):
    try:
        report_id = f"QS-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        summaries = {
            "risk": "Comprehensive risk assessment report covering all security domains",
            "quantum": "Quantum readiness assessment with migration recommendations",
            "vulnerability": "Vulnerability scan report with severity ratings",
            "prompt": "Prompt security analysis report",
            "executive": "Executive summary with key metrics and recommendations"
        }
        return ReportResponse(
            report_id=report_id,
            report_type=request.report_type,
            generated_at=datetime.now().isoformat(),
            status="Generated",
            download_url=f"/api/report/download/{report_id}",
            summary=summaries.get(request.report_type, "Security report generated successfully")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")
