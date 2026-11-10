from pokemon_etl.constants.validation import MAX_CAPTURE_LEVEL, MIN_CAPTURE_LEVEL
from pokemon_etl.validation.checks import (
    capture_is_not_before_its_trainer,
    capture_is_not_in_the_future,
    has_distinct_fighters,
    has_positive_duration,
    winner_is_a_fighter,
)
from pokemon_etl.validation.enums import ColumnKind, Severity
from pokemon_etl.validation.models import (
    ColumnSpec,
    ForeignKeySpec,
    ReferenceCheck,
    RowCheck,
    TableSpec,
)

TYPES = TableSpec(
    name="types",
    file_name="types.csv",
    columns=(
        ColumnSpec("id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("name", ColumnKind.TEXT),
    ),
    unique_keys=(("id",), ("name",)),
)

POKEMON = TableSpec(
    name="pokemon",
    file_name="pokemon.csv",
    columns=(
        ColumnSpec("id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("name", ColumnKind.TEXT),
        ColumnSpec("height", ColumnKind.INTEGER, minimum=0),
        ColumnSpec("weight", ColumnKind.INTEGER, minimum=0),
        ColumnSpec(
            "base_experience", ColumnKind.INTEGER, minimum=0, empty_severity=Severity.WARNING
        ),
        ColumnSpec("sprite", ColumnKind.TEXT, empty_severity=Severity.WARNING),
    ),
    unique_keys=(("id",),),
)

POKEMON_TYPES = TableSpec(
    name="pokemon_types",
    file_name="pokemon_types.csv",
    columns=(
        ColumnSpec("pokemon_id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("type_id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("slot", ColumnKind.INTEGER, minimum=1),
    ),
    unique_keys=(("pokemon_id", "type_id"), ("pokemon_id", "slot")),
    foreign_keys=(
        ForeignKeySpec("pokemon_id", referenced_table="pokemon"),
        ForeignKeySpec("type_id", referenced_table="types"),
    ),
)

TRAINERS = TableSpec(
    name="trainers",
    file_name="trainers.csv",
    columns=(
        ColumnSpec("id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("name", ColumnKind.TEXT),
        ColumnSpec("region", ColumnKind.TEXT),
        ColumnSpec("created_at", ColumnKind.DATE),
    ),
    unique_keys=(("id",),),
)

CAPTURE_TRAINER = ForeignKeySpec("trainer_id", referenced_table="trainers")

CAPTURES = TableSpec(
    name="captures",
    file_name="captures.csv",
    columns=(
        ColumnSpec("id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("trainer_id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("pokemon_id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("captured_at", ColumnKind.TIMESTAMP),
        ColumnSpec(
            "level", ColumnKind.INTEGER, minimum=MIN_CAPTURE_LEVEL, maximum=MAX_CAPTURE_LEVEL
        ),
        ColumnSpec("location", ColumnKind.TEXT),
    ),
    unique_keys=(("id",),),
    foreign_keys=(
        CAPTURE_TRAINER,
        ForeignKeySpec("pokemon_id", referenced_table="pokemon"),
    ),
    row_checks=(
        RowCheck(
            "not_in_the_future", "captured_at", Severity.WARNING, capture_is_not_in_the_future
        ),
    ),
    reference_checks=(
        ReferenceCheck(
            "before_trainer_created",
            "captured_at",
            Severity.WARNING,
            CAPTURE_TRAINER,
            capture_is_not_before_its_trainer,
        ),
    ),
)

BATTLES = TableSpec(
    name="battles",
    file_name="battles.csv",
    columns=(
        ColumnSpec("id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("pokemon_a_id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("pokemon_b_id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("winner_id", ColumnKind.INTEGER, minimum=1),
        ColumnSpec("fought_at", ColumnKind.TIMESTAMP),
        ColumnSpec("duration_seconds", ColumnKind.INTEGER),
    ),
    unique_keys=(("id",),),
    foreign_keys=(
        ForeignKeySpec("pokemon_a_id", referenced_table="pokemon"),
        ForeignKeySpec("pokemon_b_id", referenced_table="pokemon"),
        ForeignKeySpec("winner_id", referenced_table="pokemon"),
    ),
    row_checks=(
        RowCheck("distinct_fighters", "pokemon_b_id", Severity.ERROR, has_distinct_fighters),
        RowCheck("winner_fought", "winner_id", Severity.ERROR, winner_is_a_fighter),
        RowCheck("positive_duration", "duration_seconds", Severity.WARNING, has_positive_duration),
    ),
)

TABLE_SPECS_IN_LOAD_ORDER = (TYPES, POKEMON, POKEMON_TYPES, TRAINERS, CAPTURES, BATTLES)
