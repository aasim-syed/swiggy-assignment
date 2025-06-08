# === File: api/clarify_preferences.py ===

import os
from difflib import get_close_matches
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Tuple, Dict, Optional

router = APIRouter()

# === Mock Schema (same as original) ===
mock_questions_schema = {
    "sneakers": [
        ("What brand of sneakers are you interested in?", "brand"),
        ("What is your preferred color?", "color"),
        ("What is your price range? (e.g., 0-5000)", "price_range"),
        ("What size do you wear?", "size"),
        ("Do you prefer any material (e.g., mesh, leather)?", "material"),
    ],
    "electronics": [
        ("Which electronics brand do you prefer?", "brand"),
        ("What category (e.g., phone, laptop, headphones) are you looking for?", "category"),
        ("What is your budget range? (e.g., 0-20000)", "price_range"),
        ("Any color preference for the device?", "color"),
    ],
    "books": [
        ("What genre of books are you interested in?", "genre"),
        ("Do you prefer paperback or hardcover?", "format"),
        ("Any specific author or title in mind?", "author_or_title"),
        ("What's your budget? (e.g., 0-500)", "price_range"),
        ("Do you prefer new releases or classics?", "preference"),
    ],
    "default": [
        ("What brand of product are you interested in?", "brand"),
        ("What is your preferred color?", "color"),
        ("What is your price range? (e.g., 0-10000)", "price_range"),
        ("Do you have a preferred size?", "size"),
        ("Any material or feature preferences?", "features"),
    ],
}

# === Input Model ===
class ClarifyRequest(BaseModel):
    product_type: str
    mock_mode: Optional[bool] = True

# === Output Model ===
class Question(BaseModel):
    question_text: str
    key: str

@router.post("/clarify-preferences", response_model=List[Question])
def clarify_preferences(input_data: ClarifyRequest):
    product_type = input_data.get("product_type", "").strip().lower()
    mock_mode = input_data.get("mock_mode", True)


    # 1. Fuzzy-match schema
    schema_key = product_type if product_type in mock_questions_schema else None
    if not schema_key:
        close = get_close_matches(product_type, mock_questions_schema.keys(), n=1, cutoff=0.6)
        schema_key = close[0] if close else "default"

    questions = []

    # 2. Try LLM if available and not in mock mode
    llm_key = os.getenv("OPENAI_API_KEY") or os.getenv("CLAUDE_API_KEY")
    if not mock_mode and llm_key:
        try:
            prompt = (
                f"You are an AI shopping assistant. The user wants a {schema_key}. "
                "Generate 5 clear questions to clarify their preferences, focusing on brand, color, "
                "size (if relevant), material (if relevant), and price range."
            )

            if os.getenv("OPENAI_API_KEY"):
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                )
                llm_output = response.choices[0].message.content.strip()
            else:
                from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
                client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
                llm_output = client.completions.create(
                    model="claude-3.7-sonnet",
                    prompt=f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}",
                    max_tokens_to_sample=200
                )["completion"].strip()

            for line in llm_output.split("\n"):
                line = line.strip()
                if not line:
                    continue
                key_guess = guess_key(line)
                questions.append(Question(question_text=line, key=key_guess))

            return questions

        except Exception:
            # Fallback to mock
            pass

    # 3. Fallback to mock schema
    mock_schema = mock_questions_schema[schema_key]
    return [Question(question_text=q, key=k) for q, k in mock_schema]

# === Utility for key inference ===
def guess_key(text: str) -> str:
    text = text.lower()
    if "brand" in text:
        return "brand"
    if "color" in text:
        return "color"
    if "price" in text or "budget" in text:
        return "price_range"
    if "size" in text:
        return "size"
    if "genre" in text:
        return "genre"
    if "author" in text:
        return "author_or_title"
    if "material" in text:
        return "material"
    if "category" in text:
        return "category"
    return "other"
