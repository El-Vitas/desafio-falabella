from decimal import Decimal
from pathlib import Path

import psycopg2
import pytest
from psycopg2 import sql
from psycopg2.extensions import connection as Connection

from pokemon_etl.errors import LoadCountMismatchError
from pokemon_etl.loader import load_tables
from tests.datasets import VALID_ROW_COUNTS, append_row, write_dataset


def _count_rows(connection: Connection, table: str) -> int:
    with connection, connection.cursor() as cursor:
        cursor.execute(sql.SQL("SELECT COUNT(*) FROM {table}").format(table=sql.Identifier(table)))
        return cursor.fetchone()[0]


def table_counts(connection: Connection) -> dict[str, int]:
    return {table: _count_rows(connection, table) for table in VALID_ROW_COUNTS}


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
    write_dataset(
        broken_dir, append_row("battles.csv", ["3", "1", "2", "16", "2025-11-01 00:00:00", "60"])
    )

    with pytest.raises(psycopg2.errors.CheckViolation):
        load_tables(
            connection,
            broken_dir,
            {**VALID_ROW_COUNTS, "battles": VALID_ROW_COUNTS["battles"] + 1},
        )

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
        ("fire", 0, None),
        ("grass", 2, Decimal("103.00")),
        ("normal", 1, Decimal("50.00")),
        ("poison", 2, Decimal("103.00")),
    ]
