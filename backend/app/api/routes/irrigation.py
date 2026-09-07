from __future__ import annotations

import joblib
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.config import MODEL_DIR

router = APIRouter()


class IrrigationInput(BaseModel):
    Soil_Type: str
    Soil_pH: float = Field(..., ge=0)
    Soil_Moisture: float = Field(..., ge=0)
    Organic_Carbon: float = Field(..., ge=0)
    Electrical_Conductivity: float = Field(..., ge=0)
    Temperature_C: float = Field(...)
    Humidity: float = Field(..., ge=0)
    Rainfall_mm: float = Field(..., ge=0)
    Sunlight_Hours: float = Field(..., ge=0)
    Wind_Speed_kmh: float = Field(..., ge=0)
    Crop_Type: str
    Crop_Growth_Stage: str
    Season: str
    Irrigation_Type: str
    Water_Source: str
    Field_Area_hectare: float = Field(..., ge=0)
    Mulching_Used: str
    Previous_Irrigation_mm: float = Field(..., ge=0)
    Region: str


MODEL = joblib.load(MODEL_DIR / "irrigation_model.pkl")


@router.post("/predict")
def predict_irrigation(payload: IrrigationInput):
    row = pd.DataFrame([payload.model_dump()])
    prediction = MODEL.predict(row)[0]
    return {
        "irrigation_need": str(prediction),
        "recommendation": "Monitor soil moisture and schedule a light irrigation cycle if stress continues.",
        "input_summary": payload.model_dump(),
    }
