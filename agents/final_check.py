# === File: api/final_check.py ===

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

router = APIRouter()

class Product(BaseModel):
    id: str
    name: str
    brand: str
    price: float
    color: str

class FinalCheckRequest(BaseModel):
    recommendations: List[Product]
    selected_index: Optional[int] = None  # 1-based
    refine: Optional[bool] = False        # whether to revisit preferences

@router.post("/final-check")
def final_check(request: FinalCheckRequest) -> Dict:
    context = request.dict()
    recs = context["recommendations"]

    if not recs:
        return {"confirmed_product": None, "message": "No recommendations available."}

    if context.get("refine"):
        return {"confirmed_product": None, "message": "User chose to refine preferences."}

    selected_index = context.get("selected_index")
    if selected_index is None or not (1 <= selected_index <= len(recs)):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid selection. Choose an index between 1 and {len(recs)} or set 'refine' to true."
        )

    confirmed = recs[selected_index - 1]
    return {
        "confirmed_product": confirmed,
        "message": f"You confirmed: {confirmed['name']} (ID: {confirmed['id']})"
    }
