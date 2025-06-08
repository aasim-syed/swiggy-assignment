# === File: api/inventory_check.py ===

import random
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

# === Schema Definitions ===
class Product(BaseModel):
    id: str
    name: str
    brand: str
    price: float
    color: str

class InventoryContext(BaseModel):
    recommendations: List[Product]

@router.post("/inventory-check")
def inventory_check(context: InventoryContext) -> Dict[str, Any]:
    ctx = context.dict()
    recs = ctx["recommendations"]
    inventory_status = {}

    # Simulate stock availability (75% chance in-stock)
    for prod in recs:
        pid = prod.get("id")
        inventory_status[pid] = random.choice([True, True, True, False])

    # Filter recommendations based on stock
    in_stock_recs = [p for p in recs if inventory_status.get(p["id"], False)]

    result = {
        "inventory_status": inventory_status,
        "recommendations": in_stock_recs
    }

    if not in_stock_recs:
        result["error"] = "All recommended products are out of stock. Please refine preferences."

    return result
