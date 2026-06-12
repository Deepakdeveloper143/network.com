from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.supabase_client import get_supabase_client

router = APIRouter()

class RiskAnalysisRequest(BaseModel):
    num_vulnerabilities: int
    threat_level: str
    system_name: Optional[str] = "Unnamed System"

class RiskAnalysisResponse(BaseModel):
    risk_score: int
    risk_category: str
    recommendations: List[str]
    threat_intel: dict

@router.post("/risk-analyzer")
async def analyze_risk(request: RiskAnalysisRequest):
    try:
        threat_scores = {"Low": 20, "Medium": 50, "High": 75, "Critical": 95}
        base_risk = min(100, (request.num_vulnerabilities * 5) + threat_scores[request.threat_level])
        
        if base_risk >= 80:
            category = "Critical"
        elif base_risk >= 60:
            category = "High"
        elif base_risk >= 40:
            category = "Medium"
        else:
            category = "Low"
        
        recommendations = {
            "Critical": [
                "Immediately isolate affected systems",
                "Deploy emergency patches for critical vulnerabilities",
                "Activate incident response team",
                "Monitor for active exploitation attempts"
            ],
            "High": [
                "Prioritize patching within 72 hours",
                "Implement additional monitoring",
                "Restrict access to vulnerable systems",
                "Plan mitigation strategies"
            ],
            "Medium": [
                "Schedule patches during next maintenance window",
                "Review firewall rules",
                "Update vulnerability signatures",
                "Document findings for compliance"
            ],
            "Low": [
                "Add to routine patch management cycle",
                "Monitor for changes in threat landscape",
                "Perform regular audits",
                "Maintain baseline security"
            ]
        }
        
        threat_intel = {
            "cvss_score": base_risk,
            "exploit_prediction": "High" if base_risk > 70 else "Medium" if base_risk > 40 else "Low",
            "impact_assessment": category,
            "mitigation_effort": "High" if base_risk > 60 else "Medium" if base_risk > 30 else "Low"
        }
        
        response_data = RiskAnalysisResponse(
            risk_score=base_risk,
            risk_category=category,
            recommendations=recommendations[category],
            threat_intel=threat_intel
        )
        
        # Try to store in Supabase
        supabase = get_supabase_client()
        if supabase:
            try:
                supabase.table("scan_results").insert({
                    "scan_type": "risk_analyzer",
                    "scan_data": response_data.model_dump(),
                    "severity": category
                }).execute()
                
                # Update dashboard stats
                stats = supabase.table("dashboard_stats").select("*").order("recorded_at", desc=True).limit(1).execute()
                if stats.data:
                    current = stats.data[0]
                    supabase.table("dashboard_stats").insert({
                        "total_scans": current["total_scans"] + 1,
                        "quantum_risk_score": current["quantum_risk_score"],
                        "active_threats": current["active_threats"],
                        "prompt_attacks_blocked": current["prompt_attacks_blocked"],
                        "vulnerabilities_found": current["vulnerabilities_found"] + request.num_vulnerabilities,
                        "compliance_score": current["compliance_score"]
                    }).execute()
            except Exception as db_error:
                print(f"Warning: Could not store in database: {db_error}")
        
        return response_data
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid threat level")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing risk: {str(e)}")
