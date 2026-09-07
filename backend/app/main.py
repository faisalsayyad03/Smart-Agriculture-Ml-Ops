from __future__ import annotations

import os
import json
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import importlib

from backend.app.config import API_V1_STR, BACKEND_CORS_ORIGINS, PROJECT_NAME, OPENWEATHER_API_KEY

crop = importlib.import_module("backend.app.api.routes.crop")
fertilizer = importlib.import_module("backend.app.api.routes.fertilizer")
irrigation = importlib.import_module("backend.app.api.routes.irrigation")
price = importlib.import_module("backend.app.api.routes.price")
yield_route = importlib.import_module("backend.app.api.routes.yield")


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
    if not OPENWEATHER_API_KEY:
        return JSONResponse(
            status_code=503,
            content={
                "configured": False,
                "message": "Weather service is not configured. Set OPENWEATHER_API_KEY.",
                "forecast": [],
                "alerts": [],
            },
        )
    query = urlencode({"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": "metric"})
    request = Request(f"https://api.openweathermap.org/data/2.5/weather?{query}")
    try:
        with urlopen(request, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return JSONResponse(
            status_code=502,
            content={"configured": True, "message": "Weather data is temporarily unavailable.", "detail": str(exc)},
        )

    system = payload.get("sys", {})
    return {
        "configured": True,
        "message": "Live weather from OpenWeather.",
        "temperature": round(payload.get("main", {}).get("temp", 0), 1),
        "condition": payload.get("weather", [{}])[0].get("description", "Unknown").title(),
        "humidity": payload.get("main", {}).get("humidity", 0),
        "wind_speed": round(payload.get("wind", {}).get("speed", 0) * 3.6, 1),
        "rain_probability": 0,
        "cloud_coverage": payload.get("clouds", {}).get("all", 0),
        "sunrise": _format_weather_time(system.get("sunrise")),
        "sunset": _format_weather_time(system.get("sunset")),
        "forecast": [],
        "alerts": [],
    }


def _format_weather_time(timestamp):
    if not timestamp:
        return "Unavailable"
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%H:%M UTC")


app.include_router(crop.router, prefix=f"{API_V1_STR}/crop", tags=["crop"])
app.include_router(fertilizer.router, prefix=f"{API_V1_STR}/fertilizer", tags=["fertilizer"])
app.include_router(irrigation.router, prefix=f"{API_V1_STR}/irrigation", tags=["irrigation"])
app.include_router(price.router, prefix=f"{API_V1_STR}/price", tags=["price"])
app.include_router(yield_route.router, prefix=f"{API_V1_STR}/yield", tags=["yield"])
