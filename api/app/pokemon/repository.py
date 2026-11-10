from fastapi import Depends
from psycopg import Connection
from psycopg.rows import DictRow

from app.pokemon import queries
from app.pokemon.schemas import (
    PokemonDetail,
    PokemonListItem,
    PokemonPage,
    PokemonSummary,
    TypeSummary,
)
from app.shared.database import get_connection


class PokemonRepository:
    def __init__(self, connection: Connection[DictRow]) -> None:
        self._connection = connection

    def _count_pokemon(self) -> int:
        row = self._connection.execute(queries.COUNT_POKEMON).fetchone()
        return row["total"] if row is not None else 0

    def list_page(self, limit: int, offset: int) -> PokemonPage:
        rows = self._connection.execute(queries.LIST_POKEMON, {"limit": limit, "offset": offset})
        return PokemonPage(
            items=[PokemonListItem.model_validate(row) for row in rows.fetchall()],
            total=self._count_pokemon(),
            limit=limit,
            offset=offset,
        )

    def find_detail(self, pokemon_id: int) -> PokemonDetail | None:
        row = self._connection.execute(
            queries.POKEMON_DETAIL, {"pokemon_id": pokemon_id}
        ).fetchone()
        if row is None:
            return None
        return PokemonDetail.model_validate(row)

    def summary(self) -> PokemonSummary:
        totals = self._connection.execute(queries.POKEMON_TOTALS).fetchone()
        rows = self._connection.execute(queries.TYPE_SUMMARY).fetchall()
        return PokemonSummary(
            total_pokemon=totals["total_pokemon"] if totals else 0,
            pokemon_without_base_experience=(
                totals["pokemon_without_base_experience"] if totals else 0
            ),
            by_type=[TypeSummary.model_validate(row) for row in rows],
        )


def get_pokemon_repository(
    connection: Connection[DictRow] = Depends(get_connection),
) -> PokemonRepository:
    return PokemonRepository(connection)
