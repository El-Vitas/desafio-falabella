from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PokemonRow:
    id: int
    name: str
    height: int
    weight: int
    base_experience: int | None
    sprite: str | None


@dataclass(frozen=True)
class TypeRow:
    id: int
    name: str


@dataclass(frozen=True)
class PokemonTypeRow:
    pokemon_id: int
    type_id: int
    slot: int


@dataclass(frozen=True)
class ParsedPokemon:
    pokemon: PokemonRow
    types: tuple[TypeRow, ...]
    pokemon_types: tuple[PokemonTypeRow, ...]


@dataclass(frozen=True)
class ExtractedData:
    pokemon: tuple[PokemonRow, ...]
    types: tuple[TypeRow, ...]
    pokemon_types: tuple[PokemonTypeRow, ...]


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    force_extract: bool


@dataclass(frozen=True)
class RetryableAttempt:
    reason: str
    retry_after_seconds: float | None
