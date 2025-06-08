# === File: api/recommend_products.py ===

import os, json
from difflib import SequenceMatcher
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

router = APIRouter()

# === Models ===
class Preferences(BaseModel):
    brand: Optional[str] = "any"
    color: Optional[str] = "any"
    price_range: Optional[str] = "0-100000"
    category: Optional[str] = ""

class RecommendationRequest(BaseModel):
    preferences: Preferences
    product_type: str
    mock_mode: Optional[bool] = True
    summarize_with_llm: Optional[bool] = False

# === Helper Functions ===
def is_similar(a: str, b: str, threshold: float = 0.75) -> bool:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold

# === API Endpoint ===
@router.post("/recommend-products")
def recommend_products(payload: RecommendationRequest) -> Dict[str, Any]:
    print("payload")
    print(payload)
    preferences = payload.preferences
    product_type = payload.product_type.lower()
    summarize = payload.preferences

    brand = preferences.get("brand", "any").lower()
    color = preferences.get("color", "any").lower()
    category = preferences.get("category", "").strip().lower() or product_type

    # Price parsing
    raw_price = preferences.get("price_range", "0-100000")
    try:
        if "-" in raw_price:
            low, high = map(int, raw_price.split("-"))
            min_price, max_price = low, high
        else:
            min_price, max_price = 0, int(raw_price)
    except:
        min_price, max_price = 0, 100000

    # Load product catalog
    db_path = os.path.join(os.path.dirname(__file__), "..", "product_db", "mock_products.json")
    try:
        with open(db_path, "r") as f:
            catalog = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Product catalog not found.")

    def match(product: dict) -> bool:
        return (
            (category in product.get("category", "").lower() or is_similar(category, product.get("category", "")))
            and (brand == "any" or brand in product.get("brand", "").lower() or is_similar(brand, product.get("brand", "")))
            and (color == "any" or color in product.get("color", "").lower() or is_similar(color, product.get("color", "")))
            and (min_price <= product.get("price", 0) <= max_price)
        )

    matched = [p for p in catalog if match(p)]

    if not matched:
        return {
            "recommendations": [],
            "error": f"No matching products found for brand={brand}, color={color}, category={category}, price_range={min_price}-{max_price}"
        }

    response = {
        "recommendations": matched,
        "preferences_used": preferences
    }

    if summarize:
        try:
            summary_prompt = (
                f"I have the following product matches for a {category}:\n\n" +
                "\n".join([
                    f"{i+1}. {p['name']} (brand: {p['brand']}, color: {p['color']}, price: ₹{p['price']})"
                    for i, p in enumerate(matched)
                ]) +
                f"\n\nBased on the user's preferences (brand={brand}, color={color}, price_range={min_price}-{max_price}), which product is most appropriate? Provide a brief rationale."
            )
            if os.getenv("OPENAI_API_KEY"):
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                llm_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": summary_prompt}],
                    max_tokens=200
                )
                rationale = llm_response.choices[0].message.content.strip()
            elif os.getenv("CLAUDE_API_KEY"):
                from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
                client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
                llm_response = client.completions.create(
                    model="claude-3.7-sonnet",
                    prompt=f"{HUMAN_PROMPT}{summary_prompt}{AI_PROMPT}",
                    max_tokens_to_sample=200
                )
                rationale = llm_response["completion"].strip()
            else:
                rationale = "LLM summarization skipped: no API key found."

            response["llm_rationale"] = rationale
        except Exception as e:
            response["llm_rationale"] = f"LLM summarization failed: {str(e)}"

    return response
