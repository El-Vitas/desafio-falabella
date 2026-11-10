import logging
import random
import sys
import time
from collections.abc import Callable
from functools import partial

import requests

from extraction.config import load_settings
from extraction.constants.pokeapi import (
    POKEAPI_POKEMON_LIST_URL,
    POKEMON_COUNT,
    POKEMON_LIST_LIMIT_PARAMETER,
)
from extraction.constants.process import EXIT_FAILURE, EXIT_SUCCESS, LOG_FORMAT
from extraction.csv_writer import is_extraction_complete, write_extraction
from extraction.errors import ExtractionError
from extraction.models import ExtractedData, Settings
from extraction.pokeapi_client import create_session, fetch_json
from extraction.transform import assemble_extraction, parse_pokemon_detail, parse_pokemon_list

logger = logging.getLogger("extraction")


def extract_pokemon(
    session: requests.Session,
    sleep: Callable[[float], None],
    random_fraction: Callable[[], float],
) -> ExtractedData:
    fetch = partial(fetch_json, session, sleep=sleep, random_fraction=random_fraction)
    listing = fetch(
        POKEAPI_POKEMON_LIST_URL, params={POKEMON_LIST_LIMIT_PARAMETER: POKEMON_COUNT}
    )
    parsed = [
        parse_pokemon_detail(fetch(detail_url)) for detail_url in parse_pokemon_list(listing)
    ]
    return assemble_extraction(parsed)


def report_missing_optional_fields(extracted: ExtractedData) -> None:
    without_experience = [row.id for row in extracted.pokemon if row.base_experience is None]
    without_sprite = [row.id for row in extracted.pokemon if row.sprite is None]
    if without_experience:
        logger.warning("Pokémon without base_experience, written empty: %s", without_experience)
    if without_sprite:
        logger.warning("Pokémon without a sprite, written empty: %s", without_sprite)


def run(
    settings: Settings,
    session: requests.Session,
    sleep: Callable[[float], None],
    random_fraction: Callable[[], float],
) -> int:
    if is_extraction_complete(settings.data_dir) and not settings.force_extract:
        logger.info("CSV files already present in %s, skipping the download", settings.data_dir)
        return EXIT_SUCCESS
    try:
        extracted = extract_pokemon(session, sleep, random_fraction)
        write_extraction(settings.data_dir, extracted)
    except (ExtractionError, OSError):
        logger.exception("Extraction failed; the success marker was not written")
        return EXIT_FAILURE
    report_missing_optional_fields(extracted)
    logger.info(
        "Wrote %s Pokémon, %s types and %s Pokémon types to %s",
        len(extracted.pokemon),
        len(extracted.types),
        len(extracted.pokemon_types),
        settings.data_dir,
    )
    return EXIT_SUCCESS


def main() -> int:
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    try:
        settings = load_settings()
    except ExtractionError:
        logger.exception("Invalid configuration")
        return EXIT_FAILURE
    with create_session() as session:
        return run(settings, session, time.sleep, random.random)


if __name__ == "__main__":
    sys.exit(main())
