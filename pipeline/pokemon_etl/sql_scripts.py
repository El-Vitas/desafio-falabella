from collections.abc import Sequence
from pathlib import Path

from psycopg2.extensions import connection as Connection

from pokemon_etl.constants.paths import VIEWS_DIR


def view_scripts() -> list[Path]:
    return sorted(VIEWS_DIR.glob("*.sql"))


def run_sql_scripts(connection: Connection, scripts: Sequence[Path]) -> None:
    with connection, connection.cursor() as cursor:
        for script in scripts:
            cursor.execute(script.read_text(encoding="utf-8"))
