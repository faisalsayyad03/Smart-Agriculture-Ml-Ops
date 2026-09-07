from __future__ import annotations

import joblib
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.config import MODEL_DIR

router = APIRouter()


class FertilizerInput(BaseModel):
    Soil_Type: str
    Soil_pH: float = Field(..., ge=0)
    Soil_Moisture: float = Field(..., ge=0)
    Organic_Carbon: float = Field(..., ge=0)
    Electrical_Conductivity: float = Field(..., ge=0)
    Nitrogen_Level: float = Field(..., ge=0)
    Phosphorus_Level: float = Field(..., ge=0)
    Potassium_Level: float = Field(..., ge=0)
    Temperature: float = Field(...)
    Humidity: float = Field(..., ge=0)
    Rainfall: float = Field(..., ge=0)
    Crop_Type: str
    Crop_Growth_Stage: str
    Season: str
    Irrigation_Type: str
    Previous_Crop: str
    Region: str
    Fertilizer_Used_Last_Season: float = Field(..., ge=0)
    Yield_Last_Season: float = Field(..., ge=0)


MODEL = joblib.load(MODEL_DIR / "fertilizer_model.pkl")


@router.post("/predict")
def predict_fertilizer(payload: FertilizerInput):
    row = pd.DataFrame([payload.model_dump()])
    prediction = MODEL.predict(row)[0]
    return {
        "fertilizer": str(prediction),
        "reasoning": "Recommendation based on soil balance, crop stage, and nutrient profile.",
        "input_summary": payload.model_dump(),
    }
