import psycopg
import pytest
from fastapi.testclient import TestClient

from tests.conftest import client_for
from tests.fakes import LEVEL_CLASSIFICATION, MONTHLY_GROWTH, TOP_TRAINERS, FailingRepository

STATS_PATHS = (
    "/queries/monthly-growth",
    "/queries/top-trainers",
    "/queries/level-classification",
)


def test_monthly_growth_leaves_the_first_change_null(client: TestClient) -> None:
    response = client.get("/queries/monthly-growth")

    assert response.status_code == 200
    assert response.json() == MONTHLY_GROWTH.model_dump(mode="json")
    assert response.json()["months"][0] == {
        "month": "2025-11-01",
        "captures": 233,
        "previous_captures": None,
        "change_percent": None,
    }


def test_top_trainers_keeps_ties_and_empty_regions(client: TestClient) -> None:
    response = client.get("/queries/top-trainers")

    assert response.status_code == 200
    assert response.json() == TOP_TRAINERS.model_dump()


def test_level_classification_returns_a_null_percent_for_types_without_captures(
    client: TestClient,
) -> None:
    response = client.get("/queries/level-classification")

    assert response.status_code == 200
    assert response.json() == LEVEL_CLASSIFICATION.model_dump()


@pytest.mark.parametrize("path", STATS_PATHS)
def test_views_not_built_yet_answer_503(path: str) -> None:
    client = client_for(stats_repository=FailingRepository(psycopg.errors.UndefinedTable("view")))

    response = client.get(path)

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "data_not_loaded"


@pytest.mark.parametrize("path", STATS_PATHS)
def test_an_unavailable_database_answers_503(path: str) -> None:
    client = client_for(stats_repository=FailingRepository(psycopg.OperationalError("down")))

    response = client.get(path)

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "database_unavailable"


def test_an_unknown_query_answers_404(client: TestClient) -> None:
    response = client.get("/queries/unknown")

    assert response.status_code == 404
