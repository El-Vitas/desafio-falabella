import csv
from pathlib import Path

from pokemon_etl.constants.paths import SUCCESS_MARKER_FILE_NAME

CsvContent = list[list[str]]

VALID_DATASET: dict[str, CsvContent] = {
    "types.csv": [
        ["id", "name"],
        ["1", "normal"],
        ["4", "poison"],
        ["10", "fire"],
        ["12", "grass"],
    ],
    "pokemon.csv": [
        ["id", "name", "height", "weight", "base_experience", "sprite"],
        ["1", "bulbasaur", "7", "69", "64", "https://sprites.example/1.png"],
        ["2", "ivysaur", "10", "130", "142", "https://sprites.example/2.png"],
        ["16", "pidgey", "3", "18", "50", "https://sprites.example/16.png"],
    ],
    "pokemon_types.csv": [
        ["pokemon_id", "type_id", "slot"],
        ["1", "12", "1"],
        ["1", "4", "2"],
        ["2", "12", "1"],
        ["2", "4", "2"],
        ["16", "1", "1"],
    ],
    "trainers.csv": [
        ["id", "name", "region", "created_at"],
        ["1", "Ash Oak", "Kanto", "2025-01-01"],
        ["2", "Misty Stone", "Kanto", "2025-01-01"],
        ["3", "Brock Oak", "Johto", "2025-01-01"],
        ["4", "Serena Elm", "Kalos", "2025-01-01"],
    ],
    "captures.csv": [
        ["id", "trainer_id", "pokemon_id", "captured_at", "level", "location"],
        ["1", "1", "1", "2025-11-03 10:00:00", "60", "Mt. Moon"],
        ["2", "1", "16", "2025-11-05 10:00:00", "10", "Mt. Moon"],
        ["3", "2", "2", "2026-01-10 10:00:00", "55", "Route 1"],
        ["4", "3", "1", "2026-01-12 10:00:00", "5", "Route 1"],
    ],
    "battles.csv": [
        ["id", "pokemon_a_id", "pokemon_b_id", "winner_id", "fought_at", "duration_seconds"],
        ["1", "1", "2", "2", "2025-11-01 00:00:00", "120"],
        ["2", "16", "1", "16", "2025-11-02 00:00:00", "200"],
    ],
}

VALID_ROW_COUNTS = {
    "types": 4,
    "pokemon": 3,
    "pokemon_types": 5,
    "trainers": 4,
    "captures": 4,
    "battles": 2,
}


def write_dataset(
    data_dir: Path,
    overrides: dict[str, CsvContent] | None = None,
    with_success_marker: bool = True,
) -> Path:
    files = {**VALID_DATASET, **(overrides or {})}
    for file_name, content in files.items():
        with (data_dir / file_name).open("w", newline="", encoding="utf-8") as csv_file:
            csv.writer(csv_file).writerows(content)
    if with_success_marker:
        (data_dir / SUCCESS_MARKER_FILE_NAME).touch()
    return data_dir


def replace_row(file_name: str, row_index: int, row: list[str]) -> dict[str, CsvContent]:
    content = [list(existing) for existing in VALID_DATASET[file_name]]
    content[row_index] = row
    return {file_name: content}


def append_row(file_name: str, row: list[str]) -> dict[str, CsvContent]:
    return {file_name: [*VALID_DATASET[file_name], row]}
