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


def test_weather_endpoint_reports_configuration_when_key_missing():
    response = client.get("/api/weather/current")
    assert response.status_code in {200, 503}
    payload = response.json()
    assert "configured" in payload or "message" in payload
