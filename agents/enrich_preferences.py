# === File: api/enrich_preferences.py ===

import os, json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, Any

router = APIRouter()

# === Input schema ===
class EnrichRequest(BaseModel):
    product_type: str
    preferences: Dict[str, str]
    mock_mode: Optional[bool] = True

@router.post("/enrich-preferences")
def enrich_preferences(context: EnrichRequest) -> Dict[str, Any]:
    ctx = context.dict()
    preferences = ctx.get("preferences", {})
    product_type = ctx.get("product_type", "")
    mock_mode = ctx.get("mock_mode", True)

    if mock_mode:
        enriched = {
            "brand": "Apple",
            "color": "white",
            "price": "under ₹25000"
        }
        preferences.update({k: v for k, v in enriched.items() if k not in preferences})
        return {
            "preferences": preferences,
            "source": "mock"
        }

    try:
        # === OpenAI Path ===
        if os.getenv("OPENAI_API_KEY"):
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            prompt = f"""The user is interested in {product_type}. Their current preferences are: {preferences}.
Suggest more attributes (brand, color, etc.) in JSON only."""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.choices[0].message.content.strip()
            enriched = json.loads(content)

        # === Claude Path ===
        elif os.getenv("CLAUDE_API_KEY"):
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=512,
                messages=[{"role": "user", "content": f"The user is interested in {product_type}. Current preferences: {preferences}. Return JSON of enriched preferences."}]
            )
            enriched = json.loads(response.content[0].text.strip())

        else:
            raise Exception("No LLM API key configured.")

        preferences.update({k: v for k, v in enriched.items() if k not in preferences})

        return {
            "preferences": preferences,
            "source": "llm"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preference enrichment failed: {str(e)}")
