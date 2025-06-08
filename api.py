# === File: backend/api.py ===
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import os
import json
from agents.image_analyzer import analyze_image
from agents.user_clarifier import clarify_preferences
from agents.product_recommender import recommend_products

app = FastAPI()

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PreferencesRequest(BaseModel):
    product_type: str

class RecommendRequest(BaseModel):
    product_type: str
    preferences: dict

@app.post("/analyze-image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        context = {"image_base64": image_base64}
        result = analyze_image(context)
        return {
            "product_type": result.get("product_type"),
            "vision_description": result.get("vision_description", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clarify-preferences")
def clarify_preferences_endpoint(request: PreferencesRequest):
    context = {"product_type": request.product_type}
    result = clarify_preferences(context)
    return result  # since `result` is already a list of questions


@app.post("/recommend")
def recommend_endpoint(request: RecommendRequest):
    try:
        result = recommend_products(request)  # ✅ pass model directly
        return {
            "recommendations": result.get("recommendations", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class SummaryRequest(BaseModel):
    recommendations: list
    preferences: dict
    product_type: str

@app.post("/summarize")
def summarize_endpoint(request: SummaryRequest):
    try:
        # Build a summary prompt
        prompt = (
            f"The user was looking for a {request.product_type} with preferences: "
            f"{json.dumps(request.preferences)}.\n\n"
            f"Here are the matching products:\n"
        )
        for idx, p in enumerate(request.recommendations):
            prompt += f"{idx + 1}. {p['name']} by {p['brand']} (₹{p['price']}, Color: {p['color']})\n"

        # Simulate a summary (or later use LLM here)
        summary = (
            f"📝 Based on your preferences, we found {len(request.recommendations)} matching items. "
            "The most suitable ones are shown above based on brand, color, and budget match."
        )

        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === Feedback Endpoint ===
class FeedbackRequest(BaseModel):
    feedback: str

@app.post("/feedback")
def feedback_endpoint(request: FeedbackRequest):
    try:
        # TODO: persist feedback somewhere
        return {"message": "Thanks for your feedback!", "received": request.feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
