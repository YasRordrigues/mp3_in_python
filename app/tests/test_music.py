from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_play_song():
    response = client.post("/music/play/", json={"path": "example.mp3"})
    assert response.status_code == 200
    assert "Playing" in response.json()["message"]

def test_increase_volume():
    response = client.post("/music/volume/increase/")
    assert response.status_code == 200
    assert "Volume increased" in response.json()["message"]
