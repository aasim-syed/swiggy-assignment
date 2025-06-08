# === File: api/confirm_product_type.py ===

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter()

# === Input schema ===
class ConfirmContext(BaseModel):
    product_type: str = "unknown"
    product_type_confirmed: Optional[bool] = False
    mock_mode: Optional[bool] = True
    user_confirmation: Optional[bool] = True  # True = "yes", False = "no"
    corrected_type: Optional[str] = None      # Provided only if user disagrees

@router.post("/confirm-product")
def confirm_product_type(context: ConfirmContext) -> Dict[str, Any]:
    ctx = context.dict()

    if ctx.get("product_type_confirmed", False):
        return ctx  # Already confirmed previously

    if ctx.get("mock_mode", True):
        ctx["product_type_confirmed"] = True
        return ctx

    user_confirms = ctx.get("user_confirmation")
    if user_confirms is None:
        raise HTTPException(status_code=400, detail="Missing user confirmation.")

    if not user_confirms:
        corrected = ctx.get("corrected_type", "").strip().lower()
        if not corrected:
            raise HTTPException(status_code=400, detail="User rejected product type but did not provide a correction.")
        ctx["product_type"] = corrected

    ctx["product_type_confirmed"] = True
    return ctx
