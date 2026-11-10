import csv
import os
import tempfile
from collections.abc import Sequence
from dataclasses import asdict, fields
from pathlib import Path

from extraction.constants.files import (
    CSV_FILE_MODE,
    POKEMON_FILE_NAME,
    POKEMON_TYPES_FILE_NAME,
    SUCCESS_MARKER_FILE_NAME,
    TEMPORARY_FILE_SUFFIX,
    TYPES_FILE_NAME,
)
from extraction.models import ExtractedData, PokemonRow, PokemonTypeRow, TypeRow


def _success_marker_path(data_dir: Path) -> Path:
    return data_dir / SUCCESS_MARKER_FILE_NAME


def is_extraction_complete(data_dir: Path) -> bool:
    return _success_marker_path(data_dir).is_file()


def _write_rows(file_descriptor: int, columns: list[str], rows: Sequence[object]) -> None:
    with os.fdopen(file_descriptor, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
        csv_file.flush()
        os.fsync(csv_file.fileno())


def _write_csv_atomically(path: Path, row_type: type, rows: Sequence[object]) -> None:
    columns = [column.name for column in fields(row_type)]
    file_descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=TEMPORARY_FILE_SUFFIX
    )
    temporary_path = Path(temporary_name)
    try:
        _write_rows(file_descriptor, columns, rows)
        os.chmod(temporary_path, CSV_FILE_MODE)
        os.replace(temporary_path, path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def write_extraction(data_dir: Path, extracted: ExtractedData) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    _success_marker_path(data_dir).unlink(missing_ok=True)
    _write_csv_atomically(data_dir / POKEMON_FILE_NAME, PokemonRow, extracted.pokemon)
    _write_csv_atomically(data_dir / TYPES_FILE_NAME, TypeRow, extracted.types)
    _write_csv_atomically(
        data_dir / POKEMON_TYPES_FILE_NAME, PokemonTypeRow, extracted.pokemon_types
    )
    _success_marker_path(data_dir).touch(mode=CSV_FILE_MODE)
