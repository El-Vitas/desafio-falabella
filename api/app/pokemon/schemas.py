from pydantic import BaseModel


class PokemonListItem(BaseModel):
    id: int
    name: str
    sprite: str | None


class PokemonPage(BaseModel):
    items: list[PokemonListItem]
    total: int
    limit: int
    offset: int


class PokemonType(BaseModel):
    id: int
    name: str
    slot: int


class PokemonDetail(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    base_experience: int | None
    sprite: str | None
    types: list[PokemonType]
    previous_id: int | None
    next_id: int | None


class TypeSummary(BaseModel):
    type_id: int
    type_name: str
    pokemon_count: int
    avg_base_experience: float | None


class PokemonSummary(BaseModel):
    total_pokemon: int
    pokemon_without_base_experience: int
    by_type: list[TypeSummary]
