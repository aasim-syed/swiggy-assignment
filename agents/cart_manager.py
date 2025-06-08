# === File: api/cart_manager.py ===

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter()

class Product(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None
    color: Optional[str] = None
    id: Optional[str] = None

class CartRequest(BaseModel):
    confirmed_product: Optional[Product] = None
    cart: Optional[List[Product]] = []
    auto_add_more: Optional[bool] = None  # replaces `input()`

@router.post("/cart-manager")
def cart_manager(request: CartRequest) -> Dict:
    context = request.dict()
    confirmed = context.get("confirmed_product")
    cart = context.get("cart", [])

    if confirmed:
        cart.append(confirmed)

    if context.get("auto_add_more") is None:
        raise HTTPException(status_code=400, detail="Missing 'auto_add_more' boolean flag.")

    return {
        "cart": cart,
        "add_more": context["auto_add_more"],
        "message": f"Added {confirmed['name']} to cart." if confirmed else "No product added"
    }
