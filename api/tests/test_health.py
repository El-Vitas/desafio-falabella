from fastapi.testclient import TestClient

from app.shared.constants.http import HEALTHY_STATUS


def test_health_answers_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": HEALTHY_STATUS}


def test_unknown_route_answers_404_with_the_error_format(client: TestClient) -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_a_write_method_answers_405(client: TestClient) -> None:
    response = client.post("/items")

    assert response.status_code == 405
    assert response.json()["error"]["code"] == "method_not_allowed"
