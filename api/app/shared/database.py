from collections.abc import Iterator

from fastapi import Request
from psycopg import Connection
from psycopg.rows import DictRow, dict_row
from psycopg_pool import ConnectionPool

from app.shared.constants.database import (
    POOL_MAX_SIZE,
    POOL_MIN_SIZE,
    POOL_TIMEOUT_SECONDS,
    STATEMENT_TIMEOUT_MILLISECONDS,
)


def create_pool(database_url: str) -> ConnectionPool:
    return ConnectionPool(
        database_url,
        min_size=POOL_MIN_SIZE,
        max_size=POOL_MAX_SIZE,
        timeout=POOL_TIMEOUT_SECONDS,
        check=ConnectionPool.check_connection,
        kwargs={
            "row_factory": dict_row,
            "options": f"-c statement_timeout={STATEMENT_TIMEOUT_MILLISECONDS}",
        },
        open=False,
    )


def get_connection(request: Request) -> Iterator[Connection[DictRow]]:
    with request.app.state.pool.connection() as connection:
        yield connection
