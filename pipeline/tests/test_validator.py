from datetime import datetime
from pathlib import Path

import pytest

from pokemon_etl.validation import checks
from pokemon_etl.validation.enums import Severity
from pokemon_etl.validation.validator import validate_csv_files
from tests.datasets import VALID_ROW_COUNTS, append_row, replace_row, write_dataset

AFTER_THE_GENERATED_CAPTURES = datetime(2030, 1, 1)


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


def test_ids_are_compared_by_value_like_the_database(tmp_path: Path) -> None:
    write_dataset(tmp_path, append_row("pokemon.csv", ["01", "copy", "7", "69", "64", "x"]))

    assert ("pokemon", "unique") in rules_with(Severity.ERROR, tmp_path)


def test_a_reference_written_with_leading_zeros_finds_its_row(tmp_path: Path) -> None:
    write_dataset(tmp_path, append_row("pokemon_types.csv", ["016", "4", "2"]))

    assert ("pokemon_types", "foreign_key") not in rules_with(Severity.ERROR, tmp_path)


@pytest.mark.parametrize(
    ("value", "rule"),
    [("٣", "not_an_integer"), ("9" * 5000, "out_of_integer_range"), (" ", "not_an_integer")],
)
def test_rejects_integers_postgres_would_reject(tmp_path: Path, value: str, rule: str) -> None:
    write_dataset(
        tmp_path, replace_row("pokemon.csv", 1, ["1", "bulbasaur", "7", "69", value, "x"])
    )

    assert ("pokemon", rule) in rules_with(Severity.ERROR, tmp_path)


def test_an_unreadable_file_is_an_error_instead_of_a_crash(tmp_path: Path) -> None:
    write_dataset(tmp_path)
    (tmp_path / "types.csv").write_bytes(b"id,name\n1,\xff\xfe\n")

    assert ("types", "readable") in rules_with(Severity.ERROR, tmp_path)


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


@pytest.mark.parametrize(
    ("row", "rule"),
    [
        (["1", "1", "1", "2025-11-03 10:00:00", "0", "Mt. Moon"], "below_minimum_1"),
        (["1", "1", "1", "2025-11-03 10:00:00", "101", "Mt. Moon"], "above_maximum_100"),
        (["1", "1", "1", "2025-13-03 10:00:00", "60", "Mt. Moon"], "not_a_timestamp"),
        (["1", "1", "1", "2025-11-03", "60", "Mt. Moon"], "not_a_timestamp"),
        (["1", "1", "1", "", "60", "Mt. Moon"], "empty"),
        (
            ["99999999999", "1", "1", "2025-11-03 10:00:00", "60", "Mt. Moon"],
            "out_of_integer_range",
        ),
    ],
)
def test_fails_on_an_invalid_capture_row(tmp_path: Path, row: list[str], rule: str) -> None:
    write_dataset(tmp_path, replace_row("captures.csv", 1, row))

    assert ("captures", rule) in rules_with(Severity.ERROR, tmp_path)


def test_fails_on_an_invalid_trainer_date(tmp_path: Path) -> None:
    write_dataset(tmp_path, replace_row("trainers.csv", 1, ["1", "Ash Oak", "Kanto", "yesterday"]))

    assert ("trainers", "not_a_date") in rules_with(Severity.ERROR, tmp_path)


@pytest.mark.parametrize(
    "row",
    [
        ["5", "99", "1", "2025-11-03 10:00:00", "60", "Mt. Moon"],
        ["5", "1", "99", "2025-11-03 10:00:00", "60", "Mt. Moon"],
    ],
)
def test_fails_on_a_capture_of_a_missing_trainer_or_pokemon(
    tmp_path: Path, row: list[str]
) -> None:
    write_dataset(tmp_path, append_row("captures.csv", row))

    assert ("captures", "foreign_key") in rules_with(Severity.ERROR, tmp_path)


@pytest.mark.parametrize(
    ("row", "rule"),
    [
        (["3", "1", "1", "1", "2025-11-01 00:00:00", "120"], "distinct_fighters"),
        (["3", "1", "2", "16", "2025-11-01 00:00:00", "120"], "winner_fought"),
        (["3", "1", "2", "999", "2025-11-01 00:00:00", "120"], "foreign_key"),
    ],
)
def test_fails_on_an_impossible_battle(tmp_path: Path, row: list[str], rule: str) -> None:
    write_dataset(tmp_path, append_row("battles.csv", row))

    assert ("battles", rule) in rules_with(Severity.ERROR, tmp_path)


@pytest.mark.parametrize("duration", ["0", "-20"])
def test_a_non_positive_duration_is_only_a_warning(tmp_path: Path, duration: str) -> None:
    write_dataset(
        tmp_path, append_row("battles.csv", ["3", "1", "2", "2", "2025-11-01 00:00:00", duration])
    )

    assert rules_with(Severity.ERROR, tmp_path) == set()
    assert ("battles", "positive_duration") in rules_with(Severity.WARNING, tmp_path)


@pytest.mark.parametrize(
    ("captured_at", "rule"),
    [
        ("2999-01-01 00:00:00", "not_in_the_future"),
        ("2024-12-31 23:59:59", "before_trainer_created"),
    ],
)
def test_a_capture_with_an_odd_date_is_only_a_warning(
    tmp_path: Path, captured_at: str, rule: str
) -> None:
    write_dataset(
        tmp_path, append_row("captures.csv", ["5", "1", "1", captured_at, "60", "Mt. Moon"])
    )

    assert rules_with(Severity.ERROR, tmp_path) == set()
    assert ("captures", rule) in rules_with(Severity.WARNING, tmp_path)


def test_an_invalid_value_does_not_also_trigger_the_row_checks(tmp_path: Path) -> None:
    write_dataset(
        tmp_path, append_row("battles.csv", ["3", "1", "1", "abc", "2025-11-01 00:00:00", "-5"])
    )

    assert rules_with(Severity.ERROR, tmp_path) == {("battles", "not_an_integer")}
    assert rules_with(Severity.WARNING, tmp_path) == set()


def test_the_generated_dataset_only_warns_about_five_battles(
    generated_data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(checks, "current_time", lambda: AFTER_THE_GENERATED_CAPTURES)

    report = validate_csv_files(generated_data_dir)

    assert report.errors == ()
    assert [(issue.table, issue.rule) for issue in report.warnings] == [
        ("battles", "positive_duration")
    ]
    assert report.warnings[0].detail == (
        "duration_seconds: 5 rows, lines 172, 232, 291, 1279, 1814"
    )
