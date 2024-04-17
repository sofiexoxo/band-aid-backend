from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": " successful"}

def test_logout_endpoint():
    response = client.post("/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful"}

def test_get_bands_endpoint():
    response = client.get("/bands")
    assert response.status_code == 200
    assert len(response.json()) > 0
