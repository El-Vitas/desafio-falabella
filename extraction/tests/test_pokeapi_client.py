import pytest
import requests

from extraction.constants.http import BACKOFF_MAX_SECONDS, MAX_ATTEMPTS
from extraction.errors import PokeApiRequestError
from extraction.pokeapi_client import compute_backoff_seconds, fetch_json
from extraction.tests.fakes import FakeResponse, FakeSession, detail_url

URL = detail_url(25)
PAYLOAD = {"id": 25, "name": "pikachu"}
FIXED_FRACTION = 0.5
RETRY_AFTER_SECONDS = 7


class RecordingSleep:
    def __init__(self) -> None:
        self.waits: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.waits.append(seconds)


def fetch(session: FakeSession, sleep: RecordingSleep) -> object:
    return fetch_json(session, URL, sleep=sleep, random_fraction=lambda: FIXED_FRACTION)


def test_returns_the_payload_without_waiting_when_the_first_attempt_succeeds() -> None:
    session = FakeSession({URL: [FakeResponse(200, PAYLOAD)]})
    sleep = RecordingSleep()

    payload = fetch(session, sleep)

    assert payload == PAYLOAD
    assert sleep.waits == []


def test_retries_a_server_error_and_returns_the_later_success() -> None:
    session = FakeSession({URL: [FakeResponse(503), FakeResponse(200, PAYLOAD)]})
    sleep = RecordingSleep()

    payload = fetch(session, sleep)

    assert payload == PAYLOAD
    assert len(session.requested_urls) == 2
    assert sleep.waits == [compute_backoff_seconds(1, FIXED_FRACTION)]


def test_waits_what_retry_after_says_on_429() -> None:
    throttled = FakeResponse(429, headers={"Retry-After": str(RETRY_AFTER_SECONDS)})
    session = FakeSession({URL: [throttled, FakeResponse(200, PAYLOAD)]})
    sleep = RecordingSleep()

    fetch(session, sleep)

    assert sleep.waits == [RETRY_AFTER_SECONDS]


@pytest.mark.parametrize("retry_after", ["²", "٣", "soon", "-1"])
def test_ignores_a_retry_after_that_is_not_plain_seconds(retry_after: str) -> None:
    throttled = FakeResponse(429, headers={"Retry-After": retry_after})
    session = FakeSession({URL: [throttled, FakeResponse(200, PAYLOAD)]})
    sleep = RecordingSleep()

    assert fetch(session, sleep) == PAYLOAD
    assert sleep.waits == [compute_backoff_seconds(1, FIXED_FRACTION)]


def test_fails_immediately_on_404_without_retrying() -> None:
    not_found = FakeResponse(404, {"status": 404, "message": "Not Found"})
    session = FakeSession({URL: [not_found]})
    sleep = RecordingSleep()

    with pytest.raises(PokeApiRequestError, match="HTTP 404"):
        fetch(session, sleep)

    assert len(session.requested_urls) == 1
    assert sleep.waits == []


def test_gives_up_after_the_maximum_attempts_on_repeated_timeouts() -> None:
    session = FakeSession({URL: [requests.Timeout() for _attempt in range(MAX_ATTEMPTS)]})
    sleep = RecordingSleep()

    with pytest.raises(PokeApiRequestError, match=f"Timeout after {MAX_ATTEMPTS} attempts"):
        fetch(session, sleep)

    assert len(session.requested_urls) == MAX_ATTEMPTS
    assert len(sleep.waits) == MAX_ATTEMPTS - 1


def test_fails_without_retrying_when_a_200_body_is_not_json() -> None:
    session = FakeSession({URL: [FakeResponse(200, is_valid_json=False)]})
    sleep = RecordingSleep()

    with pytest.raises(PokeApiRequestError, match="not valid JSON"):
        fetch(session, sleep)

    assert len(session.requested_urls) == 1


def test_backoff_grows_exponentially_and_never_exceeds_the_maximum() -> None:
    first_wait = compute_backoff_seconds(1, 1.0)
    second_wait = compute_backoff_seconds(2, 1.0)
    late_wait = compute_backoff_seconds(20, 1.0)

    assert second_wait == first_wait * 2
    assert late_wait == BACKOFF_MAX_SECONDS
