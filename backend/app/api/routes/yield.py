from __future__ import annotations

import joblib
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.config import MODEL_DIR

router = APIRouter()


class YieldInput(BaseModel):
    Crop_Type: str
    Field_Size_ha: float = Field(..., ge=0)
    Planting_Date: str
    Soil_Type: str
    Fertilizer_Used: str
    Irrigation_Type: str


MODEL = joblib.load(MODEL_DIR / "random_forest_model.pkl")


@router.post("/predict")
def predict_yield(payload: YieldInput):
    record = {
        "Crop Type": payload.Crop_Type,
        "Soil Type": payload.Soil_Type,
        "Fertilizer Used": payload.Fertilizer_Used,
        "Irrigation Type": payload.Irrigation_Type,
        "Field Size (hectares)": payload.Field_Size_ha,
        "Planting_Year": pd.to_datetime(payload.Planting_Date, errors="coerce").year,
        "Planting_Month": pd.to_datetime(payload.Planting_Date, errors="coerce").month,
        "Planting_Day": pd.to_datetime(payload.Planting_Date, errors="coerce").day,
        "Planting_DayOfYear": pd.to_datetime(payload.Planting_Date, errors="coerce").dayofyear,
        "Planting_Quarter": pd.to_datetime(payload.Planting_Date, errors="coerce").quarter,
    }
    prediction = float(MODEL.predict(pd.DataFrame([record]))[0])
    return {
        "predicted_yield_t_per_ha": round(prediction, 2),
        "unit": "t/ha",
        "input_summary": record,
    }
