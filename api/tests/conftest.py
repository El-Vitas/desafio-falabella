import pytest
from fastapi.testclient import TestClient

from app.main import build_app
from app.pokemon.repository import get_pokemon_repository
from tests.fakes import BULBASAUR, TEST_SETTINGS, FakePokemonRepository


def client_for(repository: object) -> TestClient:
    app = build_app(TEST_SETTINGS)
    app.dependency_overrides[get_pokemon_repository] = lambda: repository
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def client() -> TestClient:
    return client_for(FakePokemonRepository([BULBASAUR]))
