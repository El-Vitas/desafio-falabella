import csv
import subprocess
import sys
from pathlib import Path

from pokemon_etl.constants.paths import SUCCESS_MARKER_FILE_NAME

POKEMON_COUNT = 100
TYPE_COUNT = 3
UNUSED_TYPE_ID = TYPE_COUNT + 1
SECOND_TYPE_EVERY = 5


def _write_csv(path: Path, rows: list[list[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        csv.writer(csv_file).writerows(rows)


def _first_type(pokemon_id: int) -> int:
    return pokemon_id % TYPE_COUNT + 1


def _second_type(pokemon_id: int) -> int:
    return (pokemon_id + 1) % TYPE_COUNT + 1


def _pokemon_type_rows(pokemon_id: int) -> list[list[object]]:
    first = [pokemon_id, _first_type(pokemon_id), 1]
    if pokemon_id % SECOND_TYPE_EVERY:
        return [first]
    return [first, [pokemon_id, _second_type(pokemon_id), 2]]


def _pokemon_row(pokemon_id: int) -> list[object]:
    sprite = f"https://sprites.example/{pokemon_id}.png"
    return [pokemon_id, f"pokemon-{pokemon_id}", 1, 1, pokemon_id, sprite]


def _write_pokemon_files(data_dir: Path) -> Path:
    pokemon_ids = range(1, POKEMON_COUNT + 1)
    type_rows = ([type_id, f"type-{type_id}"] for type_id in range(1, UNUSED_TYPE_ID + 1))
    pokemon_type_rows = (
        row for pokemon_id in pokemon_ids for row in _pokemon_type_rows(pokemon_id)
    )
    pokemon_csv = data_dir / "pokemon.csv"
    _write_csv(data_dir / "types.csv", [["id", "name"], *type_rows])
    _write_csv(
        data_dir / "pokemon_types.csv", [["pokemon_id", "type_id", "slot"], *pokemon_type_rows]
    )
    _write_csv(
        pokemon_csv,
        [
            ["id", "name", "height", "weight", "base_experience", "sprite"],
            *(_pokemon_row(pokemon_id) for pokemon_id in pokemon_ids),
        ],
    )
    return pokemon_csv


def _run_generator(generator_script: Path, data_dir: Path, pokemon_csv: Path) -> None:
    command = [sys.executable, str(generator_script), "--out", str(data_dir)]
    subprocess.run([*command, "--pokemon-csv", str(pokemon_csv)], check=True, capture_output=True)


def write_generated_dataset(data_dir: Path, generator_script: Path) -> Path:
    pokemon_csv = _write_pokemon_files(data_dir)
    _run_generator(generator_script, data_dir, pokemon_csv)
    (data_dir / SUCCESS_MARKER_FILE_NAME).touch()
    return data_dir


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))
