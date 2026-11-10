import pytest
from fastapi.testclient import TestClient

from app.main import build_app
from app.pokemon.repository import get_pokemon_repository
from app.stats.repository import get_stats_repository
from tests.fakes import BULBASAUR, TEST_SETTINGS, FakePokemonRepository, FakeStatsRepository


def client_for(
    pokemon_repository: object | None = None, stats_repository: object | None = None
) -> TestClient:
    pokemon = pokemon_repository or FakePokemonRepository([BULBASAUR])
    stats = stats_repository or FakeStatsRepository()
    app = build_app(TEST_SETTINGS)
    app.dependency_overrides[get_pokemon_repository] = lambda: pokemon
    app.dependency_overrides[get_stats_repository] = lambda: stats
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def client() -> TestClient:
    return client_for()
