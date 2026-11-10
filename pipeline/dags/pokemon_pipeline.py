import logging
from contextlib import closing
from datetime import timedelta

from airflow.exceptions import AirflowFailException
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import chain, dag, task
from psycopg2.extensions import connection as Connection

from pokemon_etl.config import data_dir
from pokemon_etl.constants.dag import (
    DAG_START_DATE,
    POKEMON_CONNECTION_ID,
    TASK_RETRIES,
    TASK_RETRY_DELAY_SECONDS,
)
from pokemon_etl.constants.paths import SCHEMA_SCRIPT
from pokemon_etl.loader import load_tables
from pokemon_etl.sql_scripts import run_sql_scripts, view_scripts
from pokemon_etl.validation.validator import format_issues, validate_csv_files

logger = logging.getLogger(__name__)


def _pokemon_connection() -> Connection:
    return PostgresHook(postgres_conn_id=POKEMON_CONNECTION_ID).get_conn()


@task
def validate_csv() -> dict[str, int]:
    report = validate_csv_files(data_dir())
    if report.warnings:
        logger.warning("Data quality warnings:\n%s", format_issues(report.warnings))
    if report.errors:
        raise AirflowFailException(f"Validation failed:\n{format_issues(report.errors)}")
    logger.info("Validated row counts: %s", report.row_counts)
    return report.row_counts


@task
def create_schema() -> None:
    with closing(_pokemon_connection()) as connection:
        run_sql_scripts(connection, [SCHEMA_SCRIPT])


@task
def load(expected_counts: dict[str, int]) -> dict[str, int]:
    with closing(_pokemon_connection()) as connection:
        loaded_counts = load_tables(connection, data_dir(), expected_counts)
    logger.info("Loaded row counts: %s", loaded_counts)
    return loaded_counts


@task
def build_views() -> None:
    with closing(_pokemon_connection()) as connection:
        run_sql_scripts(connection, view_scripts())


@dag(
    dag_id="pokemon_pipeline",
    schedule="@once",
    start_date=DAG_START_DATE,
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": TASK_RETRIES,
        "retry_delay": timedelta(seconds=TASK_RETRY_DELAY_SECONDS),
    },
)
def pokemon_pipeline() -> None:
    validated_counts = validate_csv()
    loaded_counts = load(validated_counts)
    chain(validated_counts, create_schema(), loaded_counts, build_views())


pokemon_pipeline()
