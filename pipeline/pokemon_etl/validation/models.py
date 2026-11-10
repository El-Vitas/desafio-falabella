from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field

from pokemon_etl.validation.enums import ColumnKind, Severity

RowValues = Mapping[str, str]


@dataclass(frozen=True)
class ColumnSpec:
    name: str
    kind: ColumnKind
    minimum: int | None = None
    maximum: int | None = None
    empty_severity: Severity = Severity.ERROR


@dataclass(frozen=True)
class ForeignKeySpec:
    column: str
    referenced_table: str
    referenced_column: str = "id"


@dataclass(frozen=True)
class RowCheck:
    rule: str
    column: str
    severity: Severity
    is_valid: Callable[[RowValues], bool]


@dataclass(frozen=True)
class ReferenceCheck:
    rule: str
    column: str
    severity: Severity
    foreign_key: ForeignKeySpec
    is_valid: Callable[[RowValues, RowValues], bool]


@dataclass(frozen=True)
class TableSpec:
    name: str
    file_name: str
    columns: tuple[ColumnSpec, ...]
    unique_keys: tuple[tuple[str, ...], ...]
    foreign_keys: tuple[ForeignKeySpec, ...] = ()
    row_checks: tuple[RowCheck, ...] = ()
    reference_checks: tuple[ReferenceCheck, ...] = ()

    @property
    def column_names(self) -> tuple[str, ...]:
        return tuple(column.name for column in self.columns)


@dataclass(frozen=True)
class CsvRow:
    line: int
    values: RowValues


RowsByTable = Mapping[str, Sequence[CsvRow]]


@dataclass(frozen=True)
class ValueProblem:
    severity: Severity
    rule: str


@dataclass(frozen=True, order=True)
class Finding:
    severity: Severity
    column: str
    rule: str
    line: int


@dataclass(frozen=True)
class Issue:
    severity: Severity
    table: str
    rule: str
    detail: str


@dataclass(frozen=True)
class ValidationReport:
    issues: tuple[Issue, ...]
    row_counts: dict[str, int] = field(default_factory=dict)

    @property
    def errors(self) -> tuple[Issue, ...]:
        return tuple(issue for issue in self.issues if issue.severity is Severity.ERROR)

    @property
    def warnings(self) -> tuple[Issue, ...]:
        return tuple(issue for issue in self.issues if issue.severity is Severity.WARNING)
