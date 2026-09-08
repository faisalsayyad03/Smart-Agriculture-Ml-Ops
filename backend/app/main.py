from __future__ import annotations

import csv
import statistics
from backend.app import compat
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import importlib

from backend.app.config import API_V1_STR, BACKEND_CORS_ORIGINS, DATA_DIR, PROJECT_NAME

crop = importlib.import_module("backend.app.api.routes.crop")
fertilizer = importlib.import_module("backend.app.api.routes.fertilizer")
irrigation = importlib.import_module("backend.app.api.routes.irrigation")
price = importlib.import_module("backend.app.api.routes.price")
yield_route = importlib.import_module("backend.app.api.routes.yield")
compat.patch_serialized_models()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title=PROJECT_NAME, version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "service": PROJECT_NAME}


@app.get(f"{API_V1_STR}/health")
def api_health():
    return {"status": "ok", "service": PROJECT_NAME}


@app.get("/api/weather/current")
def weather_current(lat: float = 20.5937, lon: float = 78.9629):
    dataset_path = DATA_DIR / "irrigation_prediction.csv"
    with dataset_path.open(newline="", encoding="utf-8") as dataset_file:
        rows = list(csv.DictReader(dataset_file))
    sample = rows[:100]
    temperature = statistics.mean(float(row["Temperature_C"]) for row in sample)
    humidity = statistics.mean(float(row["Humidity"]) for row in sample)
    wind_speed = statistics.mean(float(row["Wind_Speed_kmh"]) for row in sample)
    cloud_coverage = round(min(100, humidity))
    condition = "Clear" if cloud_coverage < 35 else "Partly cloudy" if cloud_coverage < 70 else "Cloudy"
    return {
        "configured": True,
        "message": "Weather summary from the local irrigation dataset.",
        "temperature": round(temperature, 1),
        "condition": condition,
        "humidity": round(humidity, 1),
        "wind_speed": round(wind_speed, 1),
        "rain_probability": 0,
        "cloud_coverage": cloud_coverage,
        "sunrise": "Dataset summary",
        "sunset": "Dataset summary",
        "forecast": [],
        "alerts": [],
    }


app.include_router(crop.router, prefix=f"{API_V1_STR}/crop", tags=["crop"])
app.include_router(fertilizer.router, prefix=f"{API_V1_STR}/fertilizer", tags=["fertilizer"])
app.include_router(irrigation.router, prefix=f"{API_V1_STR}/irrigation", tags=["irrigation"])
app.include_router(price.router, prefix=f"{API_V1_STR}/price", tags=["price"])
app.include_router(yield_route.router, prefix=f"{API_V1_STR}/yield", tags=["yield"])
