# === File: backend/api.py ===
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import os
import json
from agents.image_analyzer import analyze_image
from agents.user_clarifier import clarify_preferences
from agents.product_recommender import recommend_product

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
    try:
        context = {"product_type": request.product_type}
        result = clarify_preferences(context)
        return {
            "questions": result.get("questions", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend")
def recommend_endpoint(request: RecommendRequest):
    try:
        context = {
            "product_type": request.product_type,
            "preferences": request.preferences
        }
        result = recommend_product(context)
        return {
            "recommendations": result.get("recommendations", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
