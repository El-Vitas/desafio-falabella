import pytest

from extraction.constants.pokeapi import POKEAPI_BASE_URL, POKEMON_COUNT
from extraction.errors import IncompleteExtractionError, InvalidPokemonPayloadError
from extraction.models import PokemonRow, PokemonTypeRow, TypeRow
from extraction.transform import (
    assemble_extraction,
    parse_pokemon_detail,
    parse_pokemon_list,
)
from extraction.models import ParsedPokemon
from extraction.tests.fakes import (
    ALL_POKEMON_IDS,
    detail_url,
    make_all_details,
    make_detail,
    make_listing,
)


def parse_all(
    type_names_by_id: dict[int, tuple[str, ...]] | None = None,
) -> list[ParsedPokemon]:
    return [parse_pokemon_detail(detail) for detail in make_all_details(type_names_by_id)]


def test_parses_a_detail_into_the_three_csv_rows() -> None:
    parsed = parse_pokemon_detail(make_detail(1, ("grass", "poison")))

    assert parsed.pokemon == PokemonRow(
        id=1,
        name="pokemon-1",
        height=7,
        weight=69,
        base_experience=64,
        sprite="https://sprites.example/1.png",
    )
    assert parsed.types == (TypeRow(id=12, name="grass"), TypeRow(id=4, name="poison"))
    assert parsed.pokemon_types == (
        PokemonTypeRow(pokemon_id=1, type_id=12, slot=1),
        PokemonTypeRow(pokemon_id=1, type_id=4, slot=2),
    )


def test_keeps_a_null_base_experience_and_a_null_sprite_as_empty() -> None:
    detail = make_detail(1)
    detail["base_experience"] = None
    detail["sprites"] = {"front_default": None}

    parsed = parse_pokemon_detail(detail)

    assert parsed.pokemon.base_experience is None
    assert parsed.pokemon.sprite is None


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [("id", True), ("id", "25"), ("id", 0), ("height", -1), ("weight", 1.5), ("name", "")],
)
def test_rejects_invalid_scalar_fields(field: str, invalid_value: object) -> None:
    detail = make_detail(1)
    detail[field] = invalid_value

    with pytest.raises(InvalidPokemonPayloadError, match=field):
        parse_pokemon_detail(detail)


def test_rejects_a_detail_without_a_required_field() -> None:
    detail = make_detail(1)
    del detail["sprites"]

    with pytest.raises(InvalidPokemonPayloadError, match="missing field 'sprites'"):
        parse_pokemon_detail(detail)


def test_rejects_a_pokemon_without_types() -> None:
    detail = make_detail(1)
    detail["types"] = []

    with pytest.raises(InvalidPokemonPayloadError, match="has no types"):
        parse_pokemon_detail(detail)


def test_rejects_a_repeated_type_slot() -> None:
    detail = make_detail(1, ("grass", "poison"))
    detail["types"][1]["slot"] = 1

    with pytest.raises(InvalidPokemonPayloadError, match="repeats a type slot"):
        parse_pokemon_detail(detail)


def test_rejects_a_type_url_without_an_id() -> None:
    detail = make_detail(1)
    detail["types"][0]["type"]["url"] = f"{POKEAPI_BASE_URL}/type/grass/"

    with pytest.raises(InvalidPokemonPayloadError, match="cannot read an id"):
        parse_pokemon_detail(detail)


def test_rejects_a_payload_that_is_not_an_object() -> None:
    with pytest.raises(InvalidPokemonPayloadError, match="expected a JSON object"):
        parse_pokemon_detail(["not", "an", "object"])


def test_reads_the_detail_urls_from_the_list() -> None:
    urls = parse_pokemon_list(make_listing(ALL_POKEMON_IDS))

    assert urls[0] == detail_url(1)
    assert len(urls) == POKEMON_COUNT


def test_refuses_to_follow_detail_urls_outside_pokeapi() -> None:
    listing = make_listing(ALL_POKEMON_IDS)
    listing["results"][0]["url"] = "http://169.254.169.254/latest/meta-data/"

    with pytest.raises(InvalidPokemonPayloadError, match="outside PokeAPI"):
        parse_pokemon_list(listing)


def test_rejects_a_list_with_fewer_pokemon_than_expected() -> None:
    with pytest.raises(IncompleteExtractionError, match=f"Expected {POKEMON_COUNT}"):
        parse_pokemon_list(make_listing(ALL_POKEMON_IDS[:-1]))


def test_assembles_sorted_rows_and_one_row_per_type() -> None:
    parsed = parse_all({1: ("grass", "poison"), 4: ("fire",)})

    extracted = assemble_extraction(list(reversed(parsed)))

    assert [row.id for row in extracted.pokemon] == list(ALL_POKEMON_IDS)
    assert extracted.types == (
        TypeRow(id=4, name="poison"),
        TypeRow(id=10, name="fire"),
        TypeRow(id=12, name="grass"),
    )
    assert extracted.pokemon_types[:2] == (
        PokemonTypeRow(pokemon_id=1, type_id=12, slot=1),
        PokemonTypeRow(pokemon_id=1, type_id=4, slot=2),
    )


def test_rejects_a_type_id_that_arrives_with_two_names() -> None:
    parsed = parse_all()
    conflicting_detail = make_detail(2)
    conflicting_detail["types"][0]["type"]["name"] = "renamed-grass"
    parsed[1] = parse_pokemon_detail(conflicting_detail)

    with pytest.raises(InvalidPokemonPayloadError, match="more than one name"):
        assemble_extraction(parsed)


def test_rejects_an_extraction_with_a_missing_pokemon() -> None:
    with pytest.raises(IncompleteExtractionError, match=r"missing \[100\]"):
        assemble_extraction(parse_all()[:-1])


def test_rejects_an_extraction_with_a_repeated_pokemon() -> None:
    parsed = parse_all()

    with pytest.raises(IncompleteExtractionError, match="more than once"):
        assemble_extraction([*parsed, parsed[0]])
