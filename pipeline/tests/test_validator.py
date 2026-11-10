from pathlib import Path

import pytest

from pokemon_etl.validation.enums import Severity
from pokemon_etl.validation.validator import validate_csv_files
from tests.datasets import VALID_ROW_COUNTS, append_row, replace_row, write_dataset


def rules_with(severity: Severity, data_dir: Path) -> set[tuple[str, str]]:
    report = validate_csv_files(data_dir)
    return {(issue.table, issue.rule) for issue in report.issues if issue.severity is severity}


def test_a_valid_dataset_has_no_issues_and_reports_row_counts(tmp_path: Path) -> None:
    report = validate_csv_files(write_dataset(tmp_path))

    assert report.issues == ()
    assert report.row_counts == VALID_ROW_COUNTS


def test_fails_when_the_extraction_did_not_finish(tmp_path: Path) -> None:
    write_dataset(tmp_path, with_success_marker=False)

    assert ("all", "complete_extraction") in rules_with(Severity.ERROR, tmp_path)


def test_fails_when_a_file_is_missing(tmp_path: Path) -> None:
    write_dataset(tmp_path)
    (tmp_path / "types.csv").unlink()

    assert ("types", "file_exists") in rules_with(Severity.ERROR, tmp_path)


def test_fails_when_a_required_column_is_missing(tmp_path: Path) -> None:
    write_dataset(tmp_path, replace_row("types.csv", 0, ["id", "label"]))

    assert ("types", "columns") in rules_with(Severity.ERROR, tmp_path)


@pytest.mark.parametrize(
    ("row", "rule"),
    [
        (["abc", "bulbasaur", "7", "69", "64", "x"], "not_an_integer"),
        (["1.5", "bulbasaur", "7", "69", "64", "x"], "not_an_integer"),
        (["0", "bulbasaur", "7", "69", "64", "x"], "below_minimum_1"),
        (["1", "bulbasaur", "-7", "69", "64", "x"], "below_minimum_0"),
        (["1", "", "7", "69", "64", "x"], "empty"),
        (["1", "bulbasaur", "7", "69", "64", "x", "extra"], "field_count"),
    ],
)
def test_fails_on_an_invalid_pokemon_row(tmp_path: Path, row: list[str], rule: str) -> None:
    write_dataset(tmp_path, replace_row("pokemon.csv", 1, row))

    assert ("pokemon", rule) in rules_with(Severity.ERROR, tmp_path)


def test_an_empty_base_experience_is_only_a_warning(tmp_path: Path) -> None:
    write_dataset(tmp_path, replace_row("pokemon.csv", 1, ["1", "bulbasaur", "7", "69", "", "x"]))

    assert rules_with(Severity.ERROR, tmp_path) == set()
    assert ("pokemon", "empty") in rules_with(Severity.WARNING, tmp_path)


def test_fails_on_a_repeated_id(tmp_path: Path) -> None:
    write_dataset(tmp_path, append_row("pokemon.csv", ["1", "copy", "7", "69", "64", "x"]))

    assert ("pokemon", "unique") in rules_with(Severity.ERROR, tmp_path)


def test_fails_on_a_repeated_type_slot(tmp_path: Path) -> None:
    write_dataset(tmp_path, append_row("pokemon_types.csv", ["16", "4", "1"]))

    assert ("pokemon_types", "unique") in rules_with(Severity.ERROR, tmp_path)


@pytest.mark.parametrize("row", [["999", "12", "1"], ["16", "999", "2"]])
def test_fails_on_a_reference_to_a_missing_row(tmp_path: Path, row: list[str]) -> None:
    write_dataset(tmp_path, append_row("pokemon_types.csv", row))

    assert ("pokemon_types", "foreign_key") in rules_with(Severity.ERROR, tmp_path)
