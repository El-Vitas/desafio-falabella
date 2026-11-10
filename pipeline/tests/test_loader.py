from decimal import Decimal
from pathlib import Path

import psycopg2
import pytest
from psycopg2.extensions import connection as Connection

from pokemon_etl.errors import LoadCountMismatchError
from pokemon_etl.loader import load_tables
from tests.datasets import VALID_ROW_COUNTS, append_row, write_dataset


def table_counts(connection: Connection) -> dict[str, int]:
    with connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT (SELECT COUNT(*) FROM types), (SELECT COUNT(*) FROM pokemon),"
            " (SELECT COUNT(*) FROM pokemon_types)"
        )
        types_count, pokemon_count, pokemon_types_count = cursor.fetchone()
    return {"types": types_count, "pokemon": pokemon_count, "pokemon_types": pokemon_types_count}


def test_loads_every_row(connection: Connection, tmp_path: Path) -> None:
    loaded = load_tables(connection, write_dataset(tmp_path), VALID_ROW_COUNTS)

    assert loaded == VALID_ROW_COUNTS
    assert table_counts(connection) == VALID_ROW_COUNTS


def test_loading_twice_leaves_the_same_rows(connection: Connection, tmp_path: Path) -> None:
    data_dir = write_dataset(tmp_path)

    load_tables(connection, data_dir, VALID_ROW_COUNTS)
    load_tables(connection, data_dir, VALID_ROW_COUNTS)

    assert table_counts(connection) == VALID_ROW_COUNTS


def test_a_count_mismatch_rolls_back_to_the_previous_data(
    connection: Connection, tmp_path: Path
) -> None:
    data_dir = write_dataset(tmp_path)
    load_tables(connection, data_dir, VALID_ROW_COUNTS)

    with pytest.raises(LoadCountMismatchError):
        load_tables(connection, data_dir, {**VALID_ROW_COUNTS, "pokemon": 99})

    assert table_counts(connection) == VALID_ROW_COUNTS


def test_a_failure_halfway_rolls_back_to_the_previous_data(
    connection: Connection, tmp_path: Path
) -> None:
    load_tables(connection, write_dataset(tmp_path), VALID_ROW_COUNTS)
    broken_dir = tmp_path / "broken"
    broken_dir.mkdir()
    write_dataset(broken_dir, append_row("pokemon_types.csv", ["999", "12", "1"]))

    with pytest.raises(psycopg2.errors.ForeignKeyViolation):
        load_tables(connection, broken_dir, {**VALID_ROW_COUNTS, "pokemon_types": 6})

    assert table_counts(connection) == VALID_ROW_COUNTS


def test_the_summary_view_counts_and_averages_by_type(
    connection: Connection, tmp_path: Path
) -> None:
    load_tables(connection, write_dataset(tmp_path), VALID_ROW_COUNTS)

    with connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT type_name, pokemon_count, avg_base_experience"
            " FROM pokemon_type_summary ORDER BY type_name"
        )
        rows = cursor.fetchall()

    assert rows == [
        ("grass", 2, Decimal("103.00")),
        ("normal", 1, Decimal("50.00")),
        ("poison", 2, Decimal("103.00")),
    ]
