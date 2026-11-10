from collections import Counter, defaultdict
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from psycopg2.extensions import connection as Connection

from pokemon_etl.loader import load_tables
from pokemon_etl.validation.validator import validate_csv_files
from tests.datasets import VALID_ROW_COUNTS, append_row, write_dataset
from tests.generated import read_csv

HIGH_LEVEL = 50
TOP_POSITIONS = 3
PERCENT_STEP = Decimal("0.01")

MONTHLY_GROWTH = (
    "SELECT month, captures, previous_captures, change_percent"
    " FROM monthly_capture_growth ORDER BY month"
)
TOP_TRAINERS = (
    "SELECT region, position, trainer_id, trainer_name, captures"
    " FROM top_trainers_by_region ORDER BY region, position, trainer_id"
)
HIGH_LEVEL_BY_TYPE = (
    "SELECT type_name, high_level_captures, total_captures, high_level_percent"
    " FROM high_level_captures_by_type ORDER BY type_name"
)


def fetch(connection: Connection, query: str) -> list[tuple]:
    with connection, connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def load_generated(connection: Connection, data_dir: Path) -> None:
    load_tables(connection, data_dir, validate_csv_files(data_dir).row_counts)


def percent(part: int, whole: int) -> Decimal | None:
    if whole == 0:
        return None
    return (Decimal(100) * part / whole).quantize(PERCENT_STEP, rounding=ROUND_HALF_UP)


def expected_monthly_growth(captures: list[dict[str, str]]) -> list[tuple]:
    counts = Counter(capture["captured_at"][:7] for capture in captures)
    months = sorted(counts)
    previous_counts = [None, *(counts[month] for month in months[:-1])]
    return [
        (
            date.fromisoformat(f"{month}-01"),
            counts[month],
            previous,
            None if previous is None else percent(counts[month] - previous, previous),
        )
        for month, previous in zip(months, previous_counts, strict=True)
    ]


def expected_top_trainers(data_dir: Path) -> list[tuple]:
    trainers = {trainer["id"]: trainer for trainer in read_csv(data_dir / "trainers.csv")}
    counts = Counter(capture["trainer_id"] for capture in read_csv(data_dir / "captures.csv"))
    counts_by_region: dict[str, list[int]] = defaultdict(list)
    for trainer_id, count in counts.items():
        counts_by_region[trainers[trainer_id]["region"]].append(count)
    ranked = (
        (
            trainers[trainer_id]["region"],
            1 + sum(other > count for other in counts_by_region[trainers[trainer_id]["region"]]),
            int(trainer_id),
            trainers[trainer_id]["name"],
            count,
        )
        for trainer_id, count in counts.items()
    )
    return sorted(row for row in ranked if row[1] <= TOP_POSITIONS)


def expected_high_level_by_type(data_dir: Path) -> list[tuple]:
    type_names = {row["id"]: row["name"] for row in read_csv(data_dir / "types.csv")}
    types_by_pokemon: dict[str, list[str]] = defaultdict(list)
    for row in read_csv(data_dir / "pokemon_types.csv"):
        types_by_pokemon[row["pokemon_id"]].append(row["type_id"])
    totals: Counter[str] = Counter()
    high_levels: Counter[str] = Counter()
    for capture in read_csv(data_dir / "captures.csv"):
        for type_id in types_by_pokemon[capture["pokemon_id"]]:
            totals[type_id] += 1
            high_levels[type_id] += int(capture["level"]) >= HIGH_LEVEL
    return sorted(
        (
            name,
            high_levels[type_id],
            totals[type_id],
            percent(high_levels[type_id], totals[type_id]),
        )
        for type_id, name in type_names.items()
    )


def test_monthly_growth_keeps_empty_months_and_leaves_undefined_changes_null(
    connection: Connection, tmp_path: Path
) -> None:
    load_tables(connection, write_dataset(tmp_path), VALID_ROW_COUNTS)

    assert fetch(connection, MONTHLY_GROWTH) == [
        (date(2025, 11, 1), 2, None, None),
        (date(2025, 12, 1), 0, 2, Decimal("-100.00")),
        (date(2026, 1, 1), 2, 0, None),
    ]


def test_top_trainers_lists_regions_without_captures_empty(
    connection: Connection, tmp_path: Path
) -> None:
    load_tables(connection, write_dataset(tmp_path), VALID_ROW_COUNTS)

    assert fetch(connection, TOP_TRAINERS) == [
        ("Johto", 1, 3, "Brock Oak", 1),
        ("Kalos", None, None, None, None),
        ("Kanto", 1, 1, "Ash Oak", 2),
        ("Kanto", 2, 2, "Misty Stone", 1),
    ]


def test_tied_trainers_share_their_position(connection: Connection, tmp_path: Path) -> None:
    extra_capture = ["5", "2", "16", "2026-01-11 10:00:00", "20", "Route 1"]
    counts = {**VALID_ROW_COUNTS, "captures": VALID_ROW_COUNTS["captures"] + 1}
    data_dir = write_dataset(tmp_path, append_row("captures.csv", extra_capture))
    load_tables(connection, data_dir, counts)

    kanto = [row for row in fetch(connection, TOP_TRAINERS) if row[0] == "Kanto"]

    assert [(row[1], row[3]) for row in kanto] == [(1, "Ash Oak"), (1, "Misty Stone")]


def test_high_level_captures_count_both_types_and_leave_empty_types_null(
    connection: Connection, tmp_path: Path
) -> None:
    load_tables(connection, write_dataset(tmp_path), VALID_ROW_COUNTS)

    assert fetch(connection, HIGH_LEVEL_BY_TYPE) == [
        ("fire", 0, 0, None),
        ("grass", 2, 3, Decimal("66.67")),
        ("normal", 0, 1, Decimal("0.00")),
        ("poison", 2, 3, Decimal("66.67")),
    ]


def test_monthly_growth_on_the_generated_data(
    connection: Connection, generated_data_dir: Path
) -> None:
    load_generated(connection, generated_data_dir)

    rows = fetch(connection, MONTHLY_GROWTH)
    changes = {row[0]: row[3] for row in rows}

    assert rows == expected_monthly_growth(read_csv(generated_data_dir / "captures.csv"))
    assert len(rows) == 12
    assert changes[date(2026, 2, 1)] == Decimal("88.81")
    assert changes[date(2026, 9, 1)] == Decimal("-41.80")


def test_top_trainers_on_the_generated_data(
    connection: Connection, generated_data_dir: Path
) -> None:
    load_generated(connection, generated_data_dir)

    rows = fetch(connection, TOP_TRAINERS)
    leaders = {row[0]: row[4] for row in rows if row[1] == 1}

    assert rows == expected_top_trainers(generated_data_dir)
    assert len(rows) == 16
    assert max(leaders.values()) == leaders["Johto"] == 1270
    assert [(row[1], row[2], row[4]) for row in rows if row[0] == "Kalos"] == [(1, 41, 54)]


def test_high_level_captures_on_the_generated_data(
    connection: Connection, generated_data_dir: Path
) -> None:
    load_generated(connection, generated_data_dir)

    captures = read_csv(generated_data_dir / "captures.csv")

    assert fetch(connection, HIGH_LEVEL_BY_TYPE) == expected_high_level_by_type(generated_data_dir)
    assert sum(int(capture["level"]) >= HIGH_LEVEL for capture in captures) == 695
