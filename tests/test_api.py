from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_crop_prediction_endpoint_accepts_valid_payload():
    payload = {
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.8,
        "humidity": 82,
        "ph": 6.5,
        "rainfall": 202.9,
    }
    response = client.post("/api/crop/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "crop" in data


def test_all_prediction_endpoints_accept_website_payloads():
    payloads = {
        "fertilizer": {
            "Soil_Type": "Loamy", "Soil_pH": 6.5, "Soil_Moisture": 35,
            "Organic_Carbon": 1.2, "Electrical_Conductivity": 0.4,
            "Nitrogen_Level": 45, "Phosphorus_Level": 30, "Potassium_Level": 40,
            "Temperature": 25, "Humidity": 60, "Rainfall": 120,
            "Crop_Type": "Rice", "Crop_Growth_Stage": "Vegetative", "Season": "Kharif",
            "Irrigation_Type": "Drip", "Previous_Crop": "Wheat", "Region": "Central",
            "Fertilizer_Used_Last_Season": 40, "Yield_Last_Season": 3.2,
        },
        "irrigation": {
            "Soil_Type": "Loamy", "Soil_pH": 6.5, "Soil_Moisture": 35,
            "Organic_Carbon": 1.2, "Electrical_Conductivity": 0.4,
            "Temperature_C": 25, "Humidity": 60, "Rainfall_mm": 120,
            "Sunlight_Hours": 8, "Wind_Speed_kmh": 12, "Crop_Type": "Rice",
            "Crop_Growth_Stage": "Vegetative", "Season": "Kharif", "Irrigation_Type": "Drip",
            "Water_Source": "Canal", "Field_Area_hectare": 2, "Mulching_Used": "Yes",
            "Previous_Irrigation_mm": 25, "Region": "Central",
        },
        "price": {
            "month": "2026-09", "commodity_name": "Rice", "avg_min_price": 1800,
            "avg_max_price": 2400, "state_name": "India", "district_name": "All",
            "calculationType": "Monthly", "change": 0,
        },
        "yield": {
            "Crop_Type": "Rice", "Field_Size_ha": 2, "Planting_Date": "2026-06-15",
            "Soil_Type": "Loamy", "Fertilizer_Used": "Urea", "Irrigation_Type": "Drip",
        },
    }
    expected_keys = {
        "fertilizer": "fertilizer",
        "irrigation": "irrigation_need",
        "price": "predicted_price",
        "yield": "predicted_yield_t_per_ha",
    }
    for service, payload in payloads.items():
        response = client.post(f"/api/{service}/predict", json=payload)
        assert response.status_code == 200
        assert response.json()[expected_keys[service]] is not None


def test_weather_endpoint_uses_local_dataset():
    response = client.get("/api/weather/current")
    assert response.status_code == 200
    payload = response.json()
    assert payload["configured"] is True
    assert "local irrigation dataset" in payload["message"]


