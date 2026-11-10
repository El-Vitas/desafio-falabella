import re
from collections.abc import Sequence
from itertools import groupby
from operator import attrgetter
from typing import TypeGuard

from extraction.constants.pokeapi import (
    DETAIL_SOURCE,
    FIRST_POKEMON_ID,
    LIST_SOURCE,
    POKEAPI_POKEMON_DETAIL_PREFIX,
    POKEMON_COUNT,
    RESOURCE_ID_PATTERN,
)
from extraction.errors import IncompleteExtractionError, InvalidPokemonPayloadError
from extraction.models import (
    ExtractedData,
    ParsedPokemon,
    PokemonRow,
    PokemonTypeRow,
    TypeRow,
)


def _is_integer(value: object) -> TypeGuard[int]:
    return isinstance(value, int) and not isinstance(value, bool)


def _require_mapping(value: object, source: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise InvalidPokemonPayloadError(source, "expected a JSON object")
    return value


def _field(payload: dict[str, object], name: str, source: str) -> object:
    if name not in payload:
        raise InvalidPokemonPayloadError(source, f"missing field '{name}'")
    return payload[name]


def _require_int(payload: dict[str, object], name: str, source: str, minimum: int) -> int:
    value = _field(payload, name, source)
    if not _is_integer(value) or value < minimum:
        raise InvalidPokemonPayloadError(source, f"'{name}' must be an integer >= {minimum}")
    return value


def _optional_int(
    payload: dict[str, object], name: str, source: str, minimum: int
) -> int | None:
    if _field(payload, name, source) is None:
        return None
    return _require_int(payload, name, source, minimum)


def _require_str(payload: dict[str, object], name: str, source: str) -> str:
    value = _field(payload, name, source)
    if not isinstance(value, str) or not value.strip():
        raise InvalidPokemonPayloadError(source, f"'{name}' must be a non-empty string")
    return value


def _optional_str(payload: dict[str, object], name: str, source: str) -> str | None:
    if _field(payload, name, source) is None:
        return None
    return _require_str(payload, name, source)


def _require_list(payload: dict[str, object], name: str, source: str) -> list[object]:
    value = _field(payload, name, source)
    if not isinstance(value, list):
        raise InvalidPokemonPayloadError(source, f"'{name}' must be a list")
    return value


def parse_resource_id(url: str, source: str) -> int:
    match = re.search(RESOURCE_ID_PATTERN, url)
    if match is None:
        raise InvalidPokemonPayloadError(source, f"cannot read an id from '{url}'")
    return int(match.group(1))


def parse_pokemon_list(payload: object) -> tuple[str, ...]:
    listing = _require_mapping(payload, LIST_SOURCE)
    entries = _require_list(listing, "results", LIST_SOURCE)
    urls = tuple(
        _require_str(_require_mapping(entry, LIST_SOURCE), "url", LIST_SOURCE)
        for entry in entries
    )
    foreign_urls = [url for url in urls if not url.startswith(POKEAPI_POKEMON_DETAIL_PREFIX)]
    if foreign_urls:
        raise InvalidPokemonPayloadError(
            LIST_SOURCE, f"detail URLs outside PokeAPI: {foreign_urls[:3]}"
        )
    if len(urls) != POKEMON_COUNT:
        raise IncompleteExtractionError(
            f"Expected {POKEMON_COUNT} Pokémon in the list, received {len(urls)}"
        )
    return urls


def _parse_type_entry(entry: object, source: str) -> tuple[TypeRow, int]:
    type_entry = _require_mapping(entry, source)
    slot = _require_int(type_entry, "slot", source, minimum=1)
    type_reference = _require_mapping(_field(type_entry, "type", source), source)
    type_row = TypeRow(
        id=parse_resource_id(_require_str(type_reference, "url", source), source),
        name=_require_str(type_reference, "name", source),
    )
    return type_row, slot


def _parse_type_entries(
    detail: dict[str, object], source: str
) -> tuple[tuple[TypeRow, int], ...]:
    entries = tuple(
        _parse_type_entry(entry, source) for entry in _require_list(detail, "types", source)
    )
    if not entries:
        raise InvalidPokemonPayloadError(source, "has no types")
    slots = [slot for _type_row, slot in entries]
    if len(set(slots)) != len(slots):
        raise InvalidPokemonPayloadError(source, f"repeats a type slot: {slots}")
    return entries


def _parse_sprite(detail: dict[str, object], source: str) -> str | None:
    sprites = _require_mapping(_field(detail, "sprites", source), source)
    return _optional_str(sprites, "front_default", source)


def parse_pokemon_detail(payload: object) -> ParsedPokemon:
    detail = _require_mapping(payload, DETAIL_SOURCE)
    pokemon_id = _require_int(detail, "id", DETAIL_SOURCE, minimum=FIRST_POKEMON_ID)
    source = f"pokemon {pokemon_id}"
    pokemon = PokemonRow(
        id=pokemon_id,
        name=_require_str(detail, "name", source),
        height=_require_int(detail, "height", source, minimum=0),
        weight=_require_int(detail, "weight", source, minimum=0),
        base_experience=_optional_int(detail, "base_experience", source, minimum=0),
        sprite=_parse_sprite(detail, source),
    )
    type_entries = _parse_type_entries(detail, source)
    return ParsedPokemon(
        pokemon=pokemon,
        types=tuple(type_row for type_row, _slot in type_entries),
        pokemon_types=tuple(
            PokemonTypeRow(pokemon_id=pokemon_id, type_id=type_row.id, slot=slot)
            for type_row, slot in type_entries
        ),
    )


def _ensure_expected_ids(parsed: Sequence[ParsedPokemon]) -> None:
    received_ids = [item.pokemon.id for item in parsed]
    if len(received_ids) != len(set(received_ids)):
        raise IncompleteExtractionError("The same Pokémon was received more than once")
    expected_ids = set(range(FIRST_POKEMON_ID, FIRST_POKEMON_ID + POKEMON_COUNT))
    missing_ids = sorted(expected_ids - set(received_ids))
    unexpected_ids = sorted(set(received_ids) - expected_ids)
    if missing_ids or unexpected_ids:
        raise IncompleteExtractionError(
            f"Expected Pokémon ids {FIRST_POKEMON_ID}..{POKEMON_COUNT}; "
            f"missing {missing_ids}, unexpected {unexpected_ids}"
        )


def _unique_types(parsed: Sequence[ParsedPokemon]) -> tuple[TypeRow, ...]:
    distinct_rows = sorted(
        {type_row for item in parsed for type_row in item.types}, key=attrgetter("id")
    )
    names_by_id = {
        type_id: [type_row.name for type_row in rows]
        for type_id, rows in groupby(distinct_rows, key=attrgetter("id"))
    }
    conflicting_ids = [type_id for type_id, names in names_by_id.items() if len(names) > 1]
    if conflicting_ids:
        raise InvalidPokemonPayloadError(
            DETAIL_SOURCE, f"type ids with more than one name: {conflicting_ids}"
        )
    return tuple(distinct_rows)


def assemble_extraction(parsed: Sequence[ParsedPokemon]) -> ExtractedData:
    _ensure_expected_ids(parsed)
    return ExtractedData(
        pokemon=tuple(sorted((item.pokemon for item in parsed), key=attrgetter("id"))),
        types=_unique_types(parsed),
        pokemon_types=tuple(
            sorted(
                (row for item in parsed for row in item.pokemon_types),
                key=attrgetter("pokemon_id", "slot"),
            )
        ),
    )
