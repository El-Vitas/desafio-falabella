from pathlib import Path

from extraction.constants.pokeapi import POKEAPI_POKEMON_LIST_URL, POKEMON_COUNT
from extraction.constants.process import EXIT_FAILURE, EXIT_SUCCESS
from extraction.csv_writer import is_extraction_complete
from extraction.main import run
from extraction.models import Settings
from extraction.tests.fakes import (
    ALL_POKEMON_IDS,
    FakeResponse,
    FakeSession,
    detail_url,
    make_all_details,
    make_listing,
)


def healthy_api() -> FakeSession:
    outcomes = {
        detail_url(detail["id"]): [FakeResponse(200, detail)] for detail in make_all_details()
    }
    outcomes[POKEAPI_POKEMON_LIST_URL] = [FakeResponse(200, make_listing(ALL_POKEMON_IDS))]
    return FakeSession(outcomes)


def run_with(session: FakeSession, data_dir: Path, force_extract: bool = False) -> int:
    settings = Settings(data_dir=data_dir, force_extract=force_extract)
    return run(settings, session, sleep=lambda _seconds: None, random_fraction=lambda: 0.0)


def test_downloads_and_writes_the_csv_files(tmp_path: Path) -> None:
    session = healthy_api()

    exit_code = run_with(session, tmp_path)

    assert exit_code == EXIT_SUCCESS
    assert is_extraction_complete(tmp_path)
    assert len(session.requested_urls) == POKEMON_COUNT + 1


def test_skips_the_download_when_a_complete_extraction_exists(tmp_path: Path) -> None:
    run_with(healthy_api(), tmp_path)
    second_session = healthy_api()

    exit_code = run_with(second_session, tmp_path)

    assert exit_code == EXIT_SUCCESS
    assert second_session.requested_urls == []


def test_downloads_again_when_forced(tmp_path: Path) -> None:
    run_with(healthy_api(), tmp_path)
    second_session = healthy_api()

    run_with(second_session, tmp_path, force_extract=True)

    assert len(second_session.requested_urls) == POKEMON_COUNT + 1


def test_fails_without_writing_when_one_pokemon_cannot_be_downloaded(tmp_path: Path) -> None:
    session = healthy_api()
    session.respond_to(detail_url(57), [FakeResponse(404)])

    exit_code = run_with(session, tmp_path)

    assert exit_code == EXIT_FAILURE
    assert not is_extraction_complete(tmp_path)
    assert list(tmp_path.iterdir()) == []
