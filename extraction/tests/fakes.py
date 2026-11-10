import requests

from extraction.constants.pokeapi import (
    FIRST_POKEMON_ID,
    POKEAPI_BASE_URL,
    POKEAPI_POKEMON_LIST_URL,
    POKEMON_COUNT,
)

TYPE_IDS_BY_NAME = {"grass": 12, "poison": 4, "fire": 10, "electric": 13}
DEFAULT_TYPE_NAMES = ("grass",)
ALL_POKEMON_IDS = range(FIRST_POKEMON_ID, FIRST_POKEMON_ID + POKEMON_COUNT)


class FakeResponse:
    def __init__(
        self,
        status_code: int,
        payload: object = None,
        headers: dict[str, str] | None = None,
        is_valid_json: bool = True,
    ) -> None:
        self.status_code = status_code
        self.headers = headers or {}
        self._payload = payload
        self._is_valid_json = is_valid_json

    def json(self) -> object:
        if not self._is_valid_json:
            raise requests.JSONDecodeError("Expecting value", "<html>", 0)
        return self._payload


class FakeSession:
    def __init__(self, outcomes_by_url: dict[str, list[FakeResponse | Exception]]) -> None:
        self._outcomes_by_url = outcomes_by_url
        self.requested_urls: list[str] = []

    def respond_to(self, url: str, outcomes: list[FakeResponse | Exception]) -> None:
        self._outcomes_by_url[url] = outcomes

    def get(self, url: str, params: object = None, timeout: object = None) -> FakeResponse:
        self.requested_urls.append(url)
        outcome = self._outcomes_by_url[url].pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def detail_url(pokemon_id: int) -> str:
    return f"{POKEAPI_POKEMON_LIST_URL}/{pokemon_id}/"


def type_url(type_name: str) -> str:
    return f"{POKEAPI_BASE_URL}/type/{TYPE_IDS_BY_NAME[type_name]}/"


def make_detail(
    pokemon_id: int, type_names: tuple[str, ...] = DEFAULT_TYPE_NAMES
) -> dict[str, object]:
    return {
        "id": pokemon_id,
        "name": f"pokemon-{pokemon_id}",
        "height": 7,
        "weight": 69,
        "base_experience": 64,
        "sprites": {"front_default": f"https://sprites.example/{pokemon_id}.png"},
        "types": [
            {"slot": slot, "type": {"name": type_name, "url": type_url(type_name)}}
            for slot, type_name in enumerate(type_names, start=1)
        ],
    }


def make_all_details(
    type_names_by_id: dict[int, tuple[str, ...]] | None = None,
) -> list[dict[str, object]]:
    overrides = type_names_by_id or {}
    return [
        make_detail(pokemon_id, overrides.get(pokemon_id, DEFAULT_TYPE_NAMES))
        for pokemon_id in ALL_POKEMON_IDS
    ]


def make_listing(pokemon_ids: range) -> dict[str, object]:
    return {
        "count": len(pokemon_ids),
        "results": [
            {"name": f"pokemon-{pokemon_id}", "url": detail_url(pokemon_id)}
            for pokemon_id in pokemon_ids
        ],
    }
