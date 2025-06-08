# === File: api/summarize_session.py ===

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, List, Any

router = APIRouter()

# === Schema Definitions ===
class Product(BaseModel):
    name: str
    price: Optional[float] = None

class SummarizeContext(BaseModel):
    product_type: str
    preferences: dict
    recommendations: list
    cart: list = []  # optional
    feedback_rating: Optional[int] = None  # ✅ Fix added here

@router.post("/summarize")
def summarize_session(context: SummarizeContext) -> Dict[str, Any]:
    ctx = context.dict()
    preferences = ctx.get("preferences", {})
    recommendations = ctx.get("recommendations", [])
    feedback = ctx.get("feedback_rating", None)

    summary = "\n🧾 Session Summary:\n"
    summary += f"Your preferences were: {preferences}\n"

    if feedback is not None:
        summary += f"Your feedback rating: {feedback}/5\n"

    if recommendations:
        summary += "Recommended products:\n"
        for rec in recommendations:
            summary += f"- {rec.get('name', 'Unknown')} (₹{rec.get('price', 'N/A')})\n"
    else:
        summary += "No matching or similar products found.\n"

    return {
        "session_summary": summary
    }
