from __future__ import annotations

import joblib
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.config import MODEL_DIR

router = APIRouter()


class PriceInput(BaseModel):
    month: str
    commodity_name: str
    avg_min_price: float = Field(..., ge=0)
    avg_max_price: float = Field(..., ge=0)
    state_name: str = "India"
    district_name: str = "All"
    calculationType: str = "Monthly"
    change: float = 0


MODEL = joblib.load(MODEL_DIR / "price_prediction_model.pkl")


@router.post("/predict")
def predict_price(payload: PriceInput):
    data = payload.model_dump()
    df = pd.DataFrame([data])
    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    df["month"] = df["month"].dt.month
    prediction = float(MODEL.predict(df)[0])
    return {
        "predicted_price": round(prediction, 2),
        "currency": "INR/quintal",
        "input_summary": data,
    }
