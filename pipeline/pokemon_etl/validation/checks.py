from datetime import datetime

from pokemon_etl.validation.models import RowValues
from pokemon_etl.validation.values import parse_date, parse_timestamp


def _fighters(battle: RowValues) -> tuple[int, int]:
    return int(battle["pokemon_a_id"]), int(battle["pokemon_b_id"])


def has_distinct_fighters(battle: RowValues) -> bool:
    first_fighter, second_fighter = _fighters(battle)
    return first_fighter != second_fighter


def winner_is_a_fighter(battle: RowValues) -> bool:
    return int(battle["winner_id"]) in _fighters(battle)


def has_positive_duration(battle: RowValues) -> bool:
    return int(battle["duration_seconds"]) > 0


def current_time() -> datetime:
    return datetime.now()


def capture_is_not_in_the_future(capture: RowValues) -> bool:
    captured_at = parse_timestamp(capture["captured_at"])
    return captured_at is not None and captured_at <= current_time()


def capture_is_not_before_its_trainer(capture: RowValues, trainer: RowValues) -> bool:
    captured_at = parse_timestamp(capture["captured_at"])
    created_at = parse_date(trainer["created_at"])
    return captured_at is not None and created_at is not None and captured_at >= created_at
