from app.pokemon.schemas import (
    PokemonDetail,
    PokemonListItem,
    PokemonPage,
    PokemonSummary,
    PokemonType,
    TypeSummary,
)
from app.shared.config import Settings

TEST_SETTINGS = Settings(
    database_url="postgresql://unused@localhost/unused",
    cors_allowed_origins=("http://localhost:5173",),
)

BULBASAUR = PokemonDetail(
    id=1,
    name="bulbasaur",
    height=7,
    weight=69,
    base_experience=64,
    sprite="https://sprites.example/1.png",
    types=[PokemonType(id=12, name="grass", slot=1), PokemonType(id=4, name="poison", slot=2)],
)

SUMMARY = PokemonSummary(
    total_pokemon=1,
    by_type=[
        TypeSummary(type_id=12, type_name="grass", pokemon_count=1, avg_base_experience=64.0),
        TypeSummary(type_id=4, type_name="poison", pokemon_count=1, avg_base_experience=64.0),
    ],
)


class FakePokemonRepository:
    def __init__(self, details: list[PokemonDetail]) -> None:
        self._details = {detail.id: detail for detail in details}
        self.requested_pages: list[tuple[int, int]] = []

    def list_page(self, limit: int, offset: int) -> PokemonPage:
        self.requested_pages.append((limit, offset))
        ordered = sorted(self._details.values(), key=lambda detail: detail.id)
        return PokemonPage(
            items=[
                PokemonListItem(id=detail.id, name=detail.name, sprite=detail.sprite)
                for detail in ordered[offset : offset + limit]
            ],
            total=len(ordered),
            limit=limit,
            offset=offset,
        )

    def find_detail(self, pokemon_id: int) -> PokemonDetail | None:
        return self._details.get(pokemon_id)

    def summary(self) -> PokemonSummary:
        return SUMMARY


class FailingPokemonRepository:
    def __init__(self, error: Exception) -> None:
        self._error = error

    def list_page(self, limit: int, offset: int) -> PokemonPage:
        raise self._error

    def find_detail(self, pokemon_id: int) -> PokemonDetail | None:
        raise self._error

    def summary(self) -> PokemonSummary:
        raise self._error
