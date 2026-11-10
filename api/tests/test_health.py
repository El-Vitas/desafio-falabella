from fastapi.testclient import TestClient

from app.health import HEALTHY_STATUS
from app.main import app

client = TestClient(app)


def test_health_answers_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": HEALTHY_STATUS}


def test_unknown_route_answers_404_as_json() -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"
