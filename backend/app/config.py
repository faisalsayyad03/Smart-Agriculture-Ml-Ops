from __future__ import annotations

import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / "backend" / ".env")

PROJECT_NAME = os.getenv("PROJECT_NAME", "field.ly")
API_V1_STR = os.getenv("API_V1_STR", "/api")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

BACKEND_CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    if origin.strip()
]

MODEL_DIR = BASE_DIR / "backend" / "app" / "models"
DATA_DIR = BASE_DIR / "data"
