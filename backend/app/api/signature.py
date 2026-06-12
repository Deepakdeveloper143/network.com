from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import random
from PIL import Image
import io

router = APIRouter()

class SignatureCheckResponse(BaseModel):
    match_percentage: int
    forgery_probability: int
    confidence_score: int
    tampering_detected: bool
    analysis_result: str
    details: str

@router.post("/signature/check")
async def check_signature(file: UploadFile = File(...)):
    try:
        # Read and validate the image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # Simulate signature analysis
        match_percentage = random.randint(40, 98)
        confidence_score = random.randint(60, 95)

        if match_percentage >= 85:
            forgery_probability = random.randint(0, 15)
            analysis_result = "Genuine"
            details = "Signature matches known patterns with high confidence"
        elif match_percentage >= 60:
            forgery_probability = random.randint(30, 50)
            analysis_result = "Suspicious"
            details = "Significant inconsistencies detected, further verification recommended"
        else:
            forgery_probability = random.randint(70, 95)
            analysis_result = "Forgery Detected"
            details = "Multiple discrepancies indicate potential forgery"

        tampering_detected = forgery_probability > 60

        return SignatureCheckResponse(
            match_percentage=match_percentage,
            forgery_probability=forgery_probability,
            confidence_score=confidence_score,
            tampering_detected=tampering_detected,
            analysis_result=analysis_result,
            details=details
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing signature: {str(e)}")
