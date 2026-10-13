from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        antwort = client.get("/api/health")
    assert antwort.status_code == 200
    assert antwort.json() == {"status": "ok"}
