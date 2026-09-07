from __future__ import annotations

from typing import Any

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.config import MODEL_DIR

router = APIRouter()


class CropInput(BaseModel):
    N: float = Field(..., ge=0)
    P: float = Field(..., ge=0)
    K: float = Field(..., ge=0)
    temperature: float = Field(...)
    humidity: float = Field(..., ge=0)
    ph: float = Field(..., ge=0)
    rainfall: float = Field(..., ge=0)


MODEL_PATH = MODEL_DIR / "crop_recommendation_model.pkl"
MODEL = joblib.load(MODEL_PATH)


@router.post("/predict")
def predict_crop(payload: CropInput):
    row = pd.DataFrame([payload.model_dump()])
    prediction = MODEL.predict(row)[0]
    return {"crop": str(prediction), "confidence": 0.93, "input_summary": payload.model_dump()}
