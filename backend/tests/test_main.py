
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Welcome to ReceiptWise API"
    assert data["application"] == "ReceiptWise"
    assert data["version"] == "0.1.0"
    assert data["status"] == "running"


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == "ReceiptWise"
    assert "timestamp" in data
