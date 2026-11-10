import psycopg
import pytest
from fastapi.testclient import TestClient

from app.pokemon.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from tests.conftest import client_for
from tests.fakes import BULBASAUR, SUMMARY, FailingRepository, FakePokemonRepository


def test_lists_a_page_with_the_total(client: TestClient) -> None:
    response = client.get("/items")

    assert response.status_code == 200
    assert response.json() == {
        "items": [{"id": 1, "name": "bulbasaur", "sprite": BULBASAUR.sprite}],
        "total": 1,
        "limit": DEFAULT_PAGE_SIZE,
        "offset": 0,
    }


def test_an_offset_past_the_end_returns_an_empty_page(client: TestClient) -> None:
    response = client.get("/items", params={"offset": 500})

    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == 1


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 0},
        {"limit": MAX_PAGE_SIZE + 1},
        {"limit": "abc"},
        {"offset": -1},
        {"offset": "1.5"},
    ],
)
def test_invalid_pagination_answers_400(client: TestClient, params: dict[str, object]) -> None:
    response = client.get("/items", params=params)

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_request"


def test_returns_one_pokemon_with_its_types_in_slot_order(client: TestClient) -> None:
    response = client.get("/items/1")

    assert response.status_code == 200
    assert [pokemon_type["name"] for pokemon_type in response.json()["types"]] == [
        "grass",
        "poison",
    ]


def test_the_detail_links_to_its_neighbours(client: TestClient) -> None:
    response = client.get("/items/1")

    assert response.json()["previous_id"] is None
    assert response.json()["next_id"] == 2


def test_a_missing_pokemon_answers_404(client: TestClient) -> None:
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


@pytest.mark.parametrize("pokemon_id", ["abc", "0", "-5", "1.5", "99999999999999999999"])
def test_an_invalid_id_answers_400(client: TestClient, pokemon_id: str) -> None:
    response = client.get(f"/items/{pokemon_id}")

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_request"


def test_summary_is_not_taken_as_an_id(client: TestClient) -> None:
    response = client.get("/items/summary")

    assert response.status_code == 200
    assert response.json() == SUMMARY.model_dump()


def test_an_unavailable_database_answers_503() -> None:
    client = client_for(FailingRepository(psycopg.OperationalError("down")))

    response = client.get("/items")

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "database_unavailable"


def test_data_not_loaded_yet_answers_503() -> None:
    client = client_for(FailingRepository(psycopg.errors.UndefinedTable("missing")))

    response = client.get("/items/summary")

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "data_not_loaded"


def test_an_unexpected_error_answers_500_without_internal_details() -> None:
    client = client_for(FailingRepository(RuntimeError("secret internal detail")))

    response = client.get("/items/1")

    assert response.status_code == 500
    assert "secret internal detail" not in response.text


def test_the_requested_page_reaches_the_repository() -> None:
    repository = FakePokemonRepository([BULBASAUR])
    client = client_for(repository)

    client.get("/items", params={"limit": 10, "offset": 20})

    assert repository.requested_pages == [(10, 20)]
