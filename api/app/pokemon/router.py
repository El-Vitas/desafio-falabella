from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.pokemon.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.pokemon.repository import PokemonRepository, get_pokemon_repository
from app.pokemon.schemas import PokemonDetail, PokemonPage, PokemonSummary
from app.shared.constants.database import MAX_POSTGRES_INTEGER

router = APIRouter(prefix="/items", tags=["pokemon"])

Repository = Annotated[PokemonRepository, Depends(get_pokemon_repository)]


@router.get("")
def list_pokemon(
    repository: Repository,
    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,
    offset: Annotated[int, Query(ge=0, le=MAX_POSTGRES_INTEGER)] = 0,
) -> PokemonPage:
    return repository.list_page(limit=limit, offset=offset)


@router.get("/summary")
def pokemon_summary(repository: Repository) -> PokemonSummary:
    return repository.summary()


@router.get("/{pokemon_id}")
def get_pokemon(
    repository: Repository,
    pokemon_id: Annotated[int, Path(ge=1, le=MAX_POSTGRES_INTEGER)],
) -> PokemonDetail:
    detail = repository.find_detail(pokemon_id)
    if detail is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Pokémon {pokemon_id} does not exist")
    return detail
