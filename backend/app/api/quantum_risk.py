from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add parent dir to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.supabase_client import get_supabase_client

router = APIRouter()

class QuantumRiskRequest(BaseModel):
    rsa_key_size: Optional[int] = 2048
    ecc_curve: Optional[str] = "P-256"
    hash_algorithm: Optional[str] = "SHA-256"
    system_name: Optional[str] = "Unnamed System"

class QuantumRiskResponse(BaseModel):
    risk_score: int
    threat_level: str
    recommended_algorithm: str
    migration_priority: str
    rsa_analysis: dict
    ecc_analysis: dict
    hash_analysis: dict
    readiness_score: int
    recommendations: list

@router.post("/quantum-risk")
async def analyze_quantum_risk(request: QuantumRiskRequest):
    try:
        # Calculate risk based on key sizes
        rsa_risk = 0
        if request.rsa_key_size <= 1024:
            rsa_risk = 95
        elif request.rsa_key_size <= 2048:
            rsa_risk = 75
        elif request.rsa_key_size <= 3072:
            rsa_risk = 50
        elif request.rsa_key_size <= 4096:
            rsa_risk = 30
        else:
            rsa_risk = 15

        # ECC Risk
        ecc_risk = 0
        ecc_curves = {
            "P-256": 70,
            "P-384": 55,
            "P-521": 40,
            "secp256k1": 75
        }
        ecc_risk = ecc_curves.get(request.ecc_curve, 65)

        # Hash Risk
        hash_risk = 0
        hashes = {
            "SHA-1": 95,
            "SHA-256": 40,
            "SHA-384": 30,
            "SHA-512": 25,
            "SHA3-256": 20,
            "SHA3-512": 15
        }
        hash_risk = hashes.get(request.hash_algorithm, 50)

        # Calculate overall risk score
        overall_risk = int((rsa_risk + ecc_risk + hash_risk) / 3)

        # Determine threat level
        if overall_risk >= 70:
            threat_level = "Critical"
            migration_priority = "Immediate"
        elif overall_risk >= 50:
            threat_level = "High"
            migration_priority = "Urgent"
        elif overall_risk >= 30:
            threat_level = "Medium"
            migration_priority = "Scheduled"
        else:
            threat_level = "Low"
            migration_priority = "Planned"

        # Determine recommended algorithm
        if overall_risk >= 50:
            recommended = "CRYSTALS-Kyber"
        else:
            recommended = "ML-KEM-768"

        readiness_score = 100 - overall_risk

        recommendations = [
            "Upgrade RSA keys to at least 4096 bits as a temporary measure",
            "Plan migration to post-quantum key encapsulation mechanisms",
            "Implement crypto-agile architecture for future algorithm updates",
            "Conduct quarterly quantum risk assessments",
            "Deploy hybrid classical-post-quantum cryptography"
        ]

        response_data = QuantumRiskResponse(
            risk_score=overall_risk,
            threat_level=threat_level,
            recommended_algorithm=recommended,
            migration_priority=migration_priority,
            rsa_analysis={
                "key_size": request.rsa_key_size,
                "risk_level": "Critical" if rsa_risk >=70 else "High" if rsa_risk >=50 else "Medium" if rsa_risk >=30 else "Low",
                "vulnerable": rsa_risk >= 50
            },
            ecc_analysis={
                "curve": request.ecc_curve,
                "risk_level": "Critical" if ecc_risk >=70 else "High" if ecc_risk >=50 else "Medium" if ecc_risk >=30 else "Low",
                "vulnerable": ecc_risk >= 50
            },
            hash_analysis={
                "algorithm": request.hash_algorithm,
                "risk_level": "Critical" if hash_risk >=70 else "High" if hash_risk >=50 else "Medium" if hash_risk >=30 else "Low",
                "vulnerable": hash_risk >= 50
            },
            readiness_score=readiness_score,
            recommendations=recommendations
        )

        # Store in Supabase
        supabase = get_supabase_client()
        if supabase:
            try:
                supabase.table("scan_results").insert({
                    "scan_type": "quantum_risk",
                    "scan_data": response_data.model_dump(),
                    "severity": threat_level
                }).execute()
                
                # Update dashboard stats
                stats = supabase.table("dashboard_stats").select("*").order("recorded_at", desc=True).limit(1).execute()
                if stats.data:
                    current = stats.data[0]
                    supabase.table("dashboard_stats").insert({
                        "total_scans": current["total_scans"] + 1,
                        "quantum_risk_score": overall_risk,
                        "active_threats": current["active_threats"],
                        "prompt_attacks_blocked": current["prompt_attacks_blocked"],
                        "vulnerabilities_found": current["vulnerabilities_found"],
                        "compliance_score": current["compliance_score"]
                    }).execute()
            except Exception as db_error:
                print(f"Warning: Could not store in database: {db_error}")

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing quantum risk: {str(e)}")
