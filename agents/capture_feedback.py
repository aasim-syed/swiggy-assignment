# === File: api/capture_feedback.py ===

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter()

# === Input schema ===
class FeedbackContext(BaseModel):
    feedback_rating: Optional[int] = None
    mock_mode: Optional[bool] = True

@router.post("/feedback")
def capture_feedback(context: FeedbackContext) -> Dict[str, Any]:
    mock_mode = context.mock_mode
    rating = context.feedback_rating

    if mock_mode:
        return {
            "feedback_rating": 4,
            "message": "[MOCK] Simulated feedback rating: 4"
        }

    if rating is None or not (1 <= rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be an integer between 1 and 5.")

    return {
        "feedback_rating": rating,
        "message": "Thanks for your feedback!"
    }
