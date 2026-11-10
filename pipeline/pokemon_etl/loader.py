from collections.abc import Mapping, Sequence
from pathlib import Path

from psycopg2 import sql
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor

from pokemon_etl.constants.dag import LOAD_LOCK_TIMEOUT
from pokemon_etl.errors import LoadCountMismatchError
from pokemon_etl.validation.models import TableSpec
from pokemon_etl.validation.rules import TABLE_SPECS_IN_LOAD_ORDER


def _truncate_statement(specs: Sequence[TableSpec]) -> sql.Composed:
    tables = sql.SQL(", ").join(sql.Identifier(spec.name) for spec in specs)
    return sql.SQL("TRUNCATE {tables}").format(tables=tables)


def _copy_table(cursor: Cursor, data_dir: Path, spec: TableSpec) -> int:
    statement = sql.SQL("COPY {table} ({columns}) FROM STDIN WITH (FORMAT csv, HEADER true)").format(
        table=sql.Identifier(spec.name),
        columns=sql.SQL(", ").join(sql.Identifier(name) for name in spec.column_names),
    )
    with (data_dir / spec.file_name).open(encoding="utf-8") as csv_file:
        cursor.copy_expert(statement.as_string(cursor), csv_file)
    return cursor.rowcount


def load_tables(
    connection: Connection,
    data_dir: Path,
    expected_counts: Mapping[str, int],
    specs: Sequence[TableSpec] = TABLE_SPECS_IN_LOAD_ORDER,
) -> dict[str, int]:
    with connection, connection.cursor() as cursor:
        cursor.execute("SET LOCAL lock_timeout = %s", (LOAD_LOCK_TIMEOUT,))
        cursor.execute(_truncate_statement(specs))
        loaded_counts = {spec.name: _copy_table(cursor, data_dir, spec) for spec in specs}
        if loaded_counts != dict(expected_counts):
            raise LoadCountMismatchError(expected_counts, loaded_counts)
    return loaded_counts
