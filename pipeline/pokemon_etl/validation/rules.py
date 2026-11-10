from pokemon_etl.validation.enums import ColumnKind, Severity
from pokemon_etl.validation.models import ColumnSpec, ForeignKeySpec, TableSpec

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

TABLE_SPECS_IN_LOAD_ORDER = (TYPES, POKEMON, POKEMON_TYPES)
