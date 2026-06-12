from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import re
import sys
import os

# Add parent dir to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.supabase_client import get_supabase_client

router = APIRouter()

class PromptAnalysisRequest(BaseModel):
    prompt: str
    model_name: Optional[str] = "gpt-4"

class PromptAnalysisResponse(BaseModel):
    risk_score: int
    threat_category: str
    sanitized_prompt: str
    security_recommendation: str
    detected_attack_types: List[str]
    is_safe: bool

# Attack patterns to detect
INJECTION_PATTERNS = [
    r"ignore.*previous",
    r"disregard.*instructions",
    r"system.*prompt",
    r"act.*as",
    r"you.*are.*not",
    r"pretend.*to",
    r"forget.*everything",
    r"bypass.*security",
    r"reveal.*secret",
    r"show.*password",
    r"disclose.*information",
    r"leak.*data",
    r"output.*code",
    r"execute.*command",
    r"sudo",
    r"rm\s+-rf",
    r"drop.*table",
    r"delete.*from",
    r"select.*from"
]

JAILBREAK_PATTERNS = [
    r"dAN",
    r"do anything now",
    r"stay in character",
    r"persona",
    r"roleplay",
    r"simulate",
    r"hypothetically",
    r"in theory",
    r"for educational purposes",
    r"just suppose"
]

@router.post("/prompt-analyze")
async def analyze_prompt(request: PromptAnalysisRequest):
    try:
        prompt = request.prompt.lower()
        risk_score = 0
        detected_attacks = []
        threat_category = "Safe"

        # Check for injection attacks
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, prompt):
                risk_score += 30
                detected_attacks.append("Prompt Injection")
                break

        # Check for jailbreak attempts
        for pattern in JAILBREAK_PATTERNS:
            if re.search(pattern, prompt):
                risk_score += 25
                detected_attacks.append("Jailbreak Attempt")
                break

        # Check for data leakage attempts
        leakage_keywords = ["password", "secret", "api key", "token", "credit card", "ssn", "private key"]
        for keyword in leakage_keywords:
            if keyword in prompt:
                risk_score += 20
                detected_attacks.append("Data Leakage Attempt")
                break

        # Check for system prompt extraction
        if "system prompt" in prompt or "initial instructions" in prompt:
            risk_score += 35
            detected_attacks.append("System Prompt Extraction")

        # Check for role manipulation
        role_keywords = ["admin", "root", "superuser", "developer", "engineer"]
        for keyword in role_keywords:
            if keyword in prompt and ("act as" in prompt or "you are" in prompt):
                risk_score += 25
                detected_attacks.append("Role Manipulation")

        # Sanitize the prompt
        sanitized = request.prompt
        # Remove suspicious phrases
        sanitized = re.sub(r"ignore.*previous", "[REDACTED]", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r"disregard.*instructions", "[REDACTED]", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r"system.*prompt", "[REDACTED]", sanitized, flags=re.IGNORECASE)

        # Categorize threat
        if risk_score >= 70:
            threat_category = "Critical"
        elif risk_score >= 50:
            threat_category = "High"
        elif risk_score >= 30:
            threat_category = "Medium"
        elif risk_score > 0:
            threat_category = "Low"

        # Generate recommendation
        if risk_score == 0:
            recommendation = "Prompt appears safe. No suspicious patterns detected."
        elif risk_score < 30:
            recommendation = "Minor concerns detected. Review the prompt before proceeding."
        elif risk_score < 60:
            recommendation = "Moderate risk detected. Sanitized prompt provided. Consider blocking or rewriting."
        else:
            recommendation = "CRITICAL RISK! This prompt should be blocked immediately."

        is_safe = risk_score < 30

        response_data = PromptAnalysisResponse(
            risk_score=min(risk_score, 100),
            threat_category=threat_category,
            sanitized_prompt=sanitized,
            security_recommendation=recommendation,
            detected_attack_types=list(set(detected_attacks)),
            is_safe=is_safe
        )

        # Store in Supabase
        supabase = get_supabase_client()
        if supabase:
            try:
                supabase.table("scan_results").insert({
                    "scan_type": "prompt_analysis",
                    "scan_data": response_data.model_dump(),
                    "severity": threat_category
                }).execute()
                
                # Update dashboard stats
                stats = supabase.table("dashboard_stats").select("*").order("recorded_at", desc=True).limit(1).execute()
                if stats.data:
                    current = stats.data[0]
                    new_attacks_blocked = current["prompt_attacks_blocked"] + (0 if is_safe else 1)
                    new_active_threats = current["active_threats"] + (0 if is_safe else 1)
                    supabase.table("dashboard_stats").insert({
                        "total_scans": current["total_scans"] + 1,
                        "quantum_risk_score": current["quantum_risk_score"],
                        "active_threats": new_active_threats,
                        "prompt_attacks_blocked": new_attacks_blocked,
                        "vulnerabilities_found": current["vulnerabilities_found"],
                        "compliance_score": current["compliance_score"]
                    }).execute()
            except Exception as db_error:
                print(f"Warning: Could not store in database: {db_error}")

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing prompt: {str(e)}")
