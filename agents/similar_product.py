# === File: api/similar_products.py ===

import os
from difflib import SequenceMatcher
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

router = APIRouter()

# === Schema Definitions ===
class Product(BaseModel):
    name: str
    price: Optional[float] = 0.0
    brand: Optional[str] = ""
    color: Optional[str] = ""
    id: Optional[str] = ""
    category: Optional[str] = ""

class SimilarProductsContext(BaseModel):
    recommendations: List[Product]
    all_products: Optional[List[Product]] = None
    mock_mode: Optional[bool] = True

@router.post("/similar-products")
def find_similar_products(context: SimilarProductsContext) -> Dict[str, Any]:
    ctx = context.dict()
    recommendations = ctx["recommendations"]
    all_products = ctx.get("all_products") or recommendations
    mock_mode = ctx.get("mock_mode", True)

    if not recommendations or not all_products:
        raise HTTPException(status_code=400, detail="No products provided to compare.")

    try:
        selected_product = recommendations[0]["name"].lower()

        similar = []
        for p in all_products:
            name = p.get("name", "").lower()
            score = SequenceMatcher(None, selected_product, name).ratio()
            if selected_product in name or score > 0.6:
                similar.append(p)

        similar_top_5 = similar[:5]

        return {
            "recommendations": similar_top_5,
            "similar_products_confirmed": True if mock_mode else None,
            "selected_product": selected_product,
            "message": f"Found {len(similar_top_5)} similar product(s)."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding similar products: {str(e)}")
