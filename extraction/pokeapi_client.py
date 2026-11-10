import logging
from collections.abc import Callable, Mapping

import requests

from extraction.constants.http import (
    BACKOFF_BASE_SECONDS,
    BACKOFF_MAX_SECONDS,
    CONNECT_TIMEOUT_SECONDS,
    HTTP_OK,
    MAX_ATTEMPTS,
    READ_TIMEOUT_SECONDS,
    RETRY_AFTER_HEADER,
    RETRYABLE_STATUS_CODES,
    USER_AGENT,
)
from extraction.errors import PokeApiRequestError
from extraction.models import RetryableAttempt

logger = logging.getLogger(__name__)


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    return session


def compute_backoff_seconds(attempt: int, random_fraction: float) -> float:
    ceiling = min(BACKOFF_MAX_SECONDS, BACKOFF_BASE_SECONDS * 2 ** (attempt - 1))
    return ceiling * random_fraction


def _retry_after_seconds(response: requests.Response) -> float | None:
    raw_value = response.headers.get(RETRY_AFTER_HEADER, "").strip()
    if not (raw_value.isascii() and raw_value.isdigit()):
        return None
    return min(float(raw_value), BACKOFF_MAX_SECONDS)


def _decode_json(response: requests.Response, url: str) -> object:
    try:
        return response.json()
    except ValueError as error:
        raise PokeApiRequestError(url, "response body is not valid JSON") from error


def _attempt_request(
    session: requests.Session, url: str, params: Mapping[str, int] | None
) -> object | RetryableAttempt:
    try:
        response = session.get(
            url, params=params, timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS)
        )
    except (
        requests.ConnectionError,
        requests.Timeout,
        requests.exceptions.ChunkedEncodingError,
    ) as error:
        return RetryableAttempt(reason=type(error).__name__, retry_after_seconds=None)
    if response.status_code in RETRYABLE_STATUS_CODES:
        return RetryableAttempt(
            reason=f"HTTP {response.status_code}",
            retry_after_seconds=_retry_after_seconds(response),
        )
    if response.status_code != HTTP_OK:
        raise PokeApiRequestError(url, f"HTTP {response.status_code}")
    return _decode_json(response, url)


def _seconds_before_retry(
    attempt: int, failure: RetryableAttempt, random_fraction: Callable[[], float]
) -> float:
    if failure.retry_after_seconds is not None:
        return failure.retry_after_seconds
    return compute_backoff_seconds(attempt, random_fraction())


def fetch_json(
    session: requests.Session,
    url: str,
    *,
    sleep: Callable[[float], None],
    random_fraction: Callable[[], float],
    params: Mapping[str, int] | None = None,
) -> object:
    failure = RetryableAttempt(reason="no attempt was made", retry_after_seconds=None)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        outcome = _attempt_request(session, url, params)
        if not isinstance(outcome, RetryableAttempt):
            return outcome
        failure = outcome
        logger.warning(
            "Attempt %s/%s for %s failed: %s", attempt, MAX_ATTEMPTS, url, failure.reason
        )
        if attempt < MAX_ATTEMPTS:
            sleep(_seconds_before_retry(attempt, failure, random_fraction))
    raise PokeApiRequestError(url, f"{failure.reason} after {MAX_ATTEMPTS} attempts")
