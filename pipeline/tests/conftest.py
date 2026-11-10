import os
from collections.abc import Iterator
from pathlib import Path

import psycopg2
import pytest
from psycopg2.extensions import connection as Connection

from pokemon_etl.constants.paths import SCHEMA_SCRIPT
from pokemon_etl.sql_scripts import run_sql_scripts, view_scripts
from tests.generated import write_generated_dataset

TEST_DATABASE_URL_VARIABLE = "TEST_DATABASE_URL"
GENERATOR_SCRIPT_VARIABLE = "GENERATOR_SCRIPT"
RESET_STATEMENT = (
    "DROP VIEW IF EXISTS pokemon_type_summary, monthly_capture_growth,"
    " top_trainers_by_region, high_level_captures_by_type;"
    "DROP TABLE IF EXISTS battles, captures, trainers, pokemon_types, pokemon, types CASCADE;"
)


def _required_setting(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.skip(f"{name} is not set")
    return value


@pytest.fixture
def connection() -> Iterator[Connection]:
    database_connection = psycopg2.connect(_required_setting(TEST_DATABASE_URL_VARIABLE))
    with database_connection, database_connection.cursor() as cursor:
        cursor.execute(RESET_STATEMENT)
    run_sql_scripts(database_connection, [SCHEMA_SCRIPT, *view_scripts()])
    yield database_connection
    database_connection.close()


@pytest.fixture(scope="session")
def generated_data_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    generator_script = Path(_required_setting(GENERATOR_SCRIPT_VARIABLE))
    return write_generated_dataset(tmp_path_factory.mktemp("generated"), generator_script)
