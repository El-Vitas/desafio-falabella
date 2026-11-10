import csv
import os
import stat
from pathlib import Path

import pytest

from extraction import csv_writer
from extraction.constants.files import CSV_FILE_MODE, SUCCESS_MARKER_FILE_NAME
from extraction.csv_writer import is_extraction_complete, write_extraction
from extraction.models import ExtractedData
from extraction.tests.fakes import make_all_details
from extraction.transform import assemble_extraction, parse_pokemon_detail

REQUIRED_HEADERS = {
    "pokemon.csv": ["id", "name", "height", "weight", "base_experience", "sprite"],
    "types.csv": ["id", "name"],
    "pokemon_types.csv": ["pokemon_id", "type_id", "slot"],
}


def build_extraction() -> ExtractedData:
    details = make_all_details()
    details[0]["base_experience"] = None
    return assemble_extraction([parse_pokemon_detail(detail) for detail in details])


def read_rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8") as csv_file:
        return list(csv.reader(csv_file))


def test_writes_the_three_files_with_the_exact_required_columns(tmp_path: Path) -> None:
    write_extraction(tmp_path, build_extraction())

    for file_name, headers in REQUIRED_HEADERS.items():
        assert read_rows(tmp_path / file_name)[0] == headers
    assert is_extraction_complete(tmp_path)


def test_writes_a_missing_value_as_an_empty_cell(tmp_path: Path) -> None:
    write_extraction(tmp_path, build_extraction())

    first_pokemon = read_rows(tmp_path / "pokemon.csv")[1]
    assert first_pokemon[:5] == ["1", "pokemon-1", "7", "69", ""]


def test_leaves_files_readable_by_other_users(tmp_path: Path) -> None:
    write_extraction(tmp_path, build_extraction())

    for file_name in REQUIRED_HEADERS:
        assert stat.S_IMODE((tmp_path / file_name).stat().st_mode) == CSV_FILE_MODE


def test_a_failure_while_writing_leaves_no_marker_and_no_temporary_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_extraction(tmp_path, build_extraction())
    replaced_paths: list[str] = []

    def replace_then_fail_on_the_second_file(source: str, destination: Path) -> None:
        replaced_paths.append(source)
        if len(replaced_paths) == 2:
            raise OSError("disk full")
        os.rename(source, destination)

    monkeypatch.setattr(csv_writer.os, "replace", replace_then_fail_on_the_second_file)

    with pytest.raises(OSError, match="disk full"):
        write_extraction(tmp_path, build_extraction())

    assert not is_extraction_complete(tmp_path)
    assert not (tmp_path / SUCCESS_MARKER_FILE_NAME).exists()
    assert [path.name for path in tmp_path.iterdir() if path.name.startswith(".")] == []
