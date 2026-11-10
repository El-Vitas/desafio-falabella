import os
from collections.abc import Iterator

import psycopg2
import pytest
from psycopg2.extensions import connection as Connection

from pokemon_etl.constants.paths import SCHEMA_SCRIPT
from pokemon_etl.sql_scripts import run_sql_scripts, view_scripts

TEST_DATABASE_URL_VARIABLE = "TEST_DATABASE_URL"
RESET_STATEMENT = (
    "DROP VIEW IF EXISTS pokemon_type_summary;"
    "DROP TABLE IF EXISTS pokemon_types, pokemon, types CASCADE;"
)


@pytest.fixture
def connection() -> Iterator[Connection]:
    database_url = os.environ.get(TEST_DATABASE_URL_VARIABLE)
    if not database_url:
        pytest.skip(f"{TEST_DATABASE_URL_VARIABLE} is not set")
    database_connection = psycopg2.connect(database_url)
    with database_connection, database_connection.cursor() as cursor:
        cursor.execute(RESET_STATEMENT)
    run_sql_scripts(database_connection, [SCHEMA_SCRIPT, *view_scripts()])
    yield database_connection
    database_connection.close()
