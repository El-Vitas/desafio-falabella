import csv
from collections import Counter
from collections.abc import Mapping, Sequence
from itertools import groupby
from operator import attrgetter
from pathlib import Path

from pokemon_etl.constants.paths import SUCCESS_MARKER_FILE_NAME
from pokemon_etl.constants.validation import (
    ALL_TABLES,
    EXTRA_FIELDS_KEY,
    ISSUE_SAMPLE_SIZE,
    MAX_POSTGRES_INTEGER,
)
from pokemon_etl.validation.enums import ColumnKind, Severity
from pokemon_etl.validation.models import (
    ColumnSpec,
    CsvRow,
    Finding,
    ForeignKeySpec,
    Issue,
    ReferenceCheck,
    RowsByTable,
    TableSpec,
    ValidationReport,
    ValueProblem,
)
from pokemon_etl.validation.rules import TABLE_SPECS_IN_LOAD_ORDER
from pokemon_etl.validation.values import (
    integer_value,
    is_integer,
    parse_date,
    parse_timestamp,
)


def _sample(items: Sequence[object]) -> str:
    shown = ", ".join(str(item) for item in items[:ISSUE_SAMPLE_SIZE])
    remaining = len(items) - ISSUE_SAMPLE_SIZE
    if remaining > 0:
        return f"{shown} and {remaining} more"
    return shown


def _success_marker_issues(data_dir: Path) -> list[Issue]:
    if (data_dir / SUCCESS_MARKER_FILE_NAME).is_file():
        return []
    detail = f"{SUCCESS_MARKER_FILE_NAME} is missing: the extraction did not finish"
    return [Issue(Severity.ERROR, ALL_TABLES, "complete_extraction", detail)]


def _read_rows(data_dir: Path, spec: TableSpec) -> tuple[list[CsvRow], list[Issue]]:
    path = data_dir / spec.file_name
    if not path.is_file():
        return [], [Issue(Severity.ERROR, spec.name, "file_exists", f"{spec.file_name} not found")]
    try:
        return _parse_rows(path, spec)
    except (csv.Error, UnicodeDecodeError) as error:
        detail = f"{spec.file_name} could not be read as UTF-8 CSV: {error}"
        return [], [Issue(Severity.ERROR, spec.name, "readable", detail)]


def _parse_rows(path: Path, spec: TableSpec) -> tuple[list[CsvRow], list[Issue]]:
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        header = tuple(reader.fieldnames or ())
        if header != spec.column_names:
            detail = f"expected {list(spec.column_names)}, found {list(header)}"
            return [], [Issue(Severity.ERROR, spec.name, "columns", detail)]
        rows = [CsvRow(line=reader.line_num, values=values) for values in reader]
    return rows, []


def _is_empty(column: ColumnSpec, value: str | None) -> bool:
    if value is None or value == "":
        return True
    return column.kind is ColumnKind.TEXT and not value.strip()


def _integer_problem(column: ColumnSpec, value: str) -> ValueProblem | None:
    if not is_integer(value):
        return ValueProblem(Severity.ERROR, "not_an_integer")
    number = integer_value(value)
    if number is None or abs(number) > MAX_POSTGRES_INTEGER:
        return ValueProblem(Severity.ERROR, "out_of_integer_range")
    if column.minimum is not None and number < column.minimum:
        return ValueProblem(Severity.ERROR, f"below_minimum_{column.minimum}")
    if column.maximum is not None and number > column.maximum:
        return ValueProblem(Severity.ERROR, f"above_maximum_{column.maximum}")
    return None


def _temporal_problem(column: ColumnSpec, value: str) -> ValueProblem | None:
    parsers = {ColumnKind.DATE: parse_date, ColumnKind.TIMESTAMP: parse_timestamp}
    if parsers[column.kind](value) is None:
        return ValueProblem(Severity.ERROR, f"not_a_{column.kind}")
    return None


def _column_problem(column: ColumnSpec, value: str | None) -> ValueProblem | None:
    if value is None or _is_empty(column, value):
        return ValueProblem(column.empty_severity, "empty")
    if column.kind is ColumnKind.TEXT:
        return None
    if column.kind is ColumnKind.INTEGER:
        return _integer_problem(column, value)
    return _temporal_problem(column, value)


def _has_wrong_field_count(row: CsvRow) -> bool:
    return EXTRA_FIELDS_KEY in row.values or None in row.values.values()


def _column_findings(spec: TableSpec, row: CsvRow) -> list[Finding]:
    if _has_wrong_field_count(row):
        return [Finding(Severity.ERROR, "*", "field_count", row.line)]
    return [
        Finding(problem.severity, column.name, problem.rule, row.line)
        for column in spec.columns
        if (problem := _column_problem(column, row.values[column.name])) is not None
    ]


def _row_check_findings(spec: TableSpec, clean_rows: Sequence[CsvRow]) -> list[Finding]:
    return [
        Finding(check.severity, check.column, check.rule, row.line)
        for row in clean_rows
        for check in spec.row_checks
        if not check.is_valid(row.values)
    ]


def _column_kind(spec: TableSpec, column: str) -> ColumnKind:
    return next(column_spec.kind for column_spec in spec.columns if column_spec.name == column)


def _comparable(kind: ColumnKind, raw: str | None) -> object:
    if kind is ColumnKind.INTEGER and raw is not None:
        number = integer_value(raw)
        return raw if number is None else number
    return raw


def _rows_by_key(rows: Sequence[CsvRow], column: str, kind: ColumnKind) -> dict[object, CsvRow]:
    return {_comparable(kind, row.values[column]): row for row in rows}


def _reference_check_findings(
    spec: TableSpec,
    check: ReferenceCheck,
    clean_rows: Sequence[CsvRow],
    clean_rows_by_table: RowsByTable,
) -> list[Finding]:
    foreign_key = check.foreign_key
    kind = _column_kind(spec, foreign_key.column)
    referenced = _rows_by_key(
        clean_rows_by_table.get(foreign_key.referenced_table, ()),
        foreign_key.referenced_column,
        kind,
    )
    return [
        Finding(check.severity, check.column, check.rule, row.line)
        for row in clean_rows
        if (referenced_row := referenced.get(_comparable(kind, row.values[foreign_key.column])))
        is not None
        and not check.is_valid(row.values, referenced_row.values)
    ]


def _grouped_issue(table: str, findings: list[Finding]) -> Issue:
    first = findings[0]
    lines = [finding.line for finding in findings]
    detail = f"{first.column}: {len(lines)} rows, lines {_sample(lines)}"
    return Issue(first.severity, table, first.rule, detail)


def _grouped_issues(table: str, findings: Sequence[Finding]) -> list[Issue]:
    return [
        _grouped_issue(table, list(group))
        for _key, group in groupby(sorted(findings), key=attrgetter("severity", "column", "rule"))
    ]


def _duplicate_issue(
    spec: TableSpec, key_columns: tuple[str, ...], rows: Sequence[CsvRow]
) -> Issue | None:
    kinds = [_column_kind(spec, column) for column in key_columns]
    counts = Counter(
        tuple(
            _comparable(kind, row.values.get(column))
            for kind, column in zip(kinds, key_columns, strict=True)
        )
        for row in rows
    )
    duplicates = sorted((key for key, count in counts.items() if count > 1), key=str)
    if not duplicates:
        return None
    detail = f"{'/'.join(key_columns)} repeated: {_sample(duplicates)}"
    return Issue(Severity.ERROR, spec.name, "unique", detail)


def _foreign_key_issue(
    spec: TableSpec,
    foreign_key: ForeignKeySpec,
    rows: Sequence[CsvRow],
    rows_by_table: RowsByTable,
) -> Issue | None:
    if foreign_key.referenced_table not in rows_by_table:
        return None
    kind = _column_kind(spec, foreign_key.column)
    referenced_values = {
        _comparable(kind, row.values.get(foreign_key.referenced_column))
        for row in rows_by_table[foreign_key.referenced_table]
    }
    missing_lines = [
        row.line
        for row in rows
        if _comparable(kind, row.values.get(foreign_key.column)) not in referenced_values
    ]
    if not missing_lines:
        return None
    detail = (
        f"{foreign_key.column} not found in {foreign_key.referenced_table}."
        f"{foreign_key.referenced_column}: {len(missing_lines)} rows, "
        f"lines {_sample(missing_lines)}"
    )
    return Issue(Severity.ERROR, spec.name, "foreign_key", detail)


def _check_findings(
    spec: TableSpec, clean_rows: Sequence[CsvRow], clean_rows_by_table: RowsByTable
) -> list[Finding]:
    return [
        *_row_check_findings(spec, clean_rows),
        *(
            finding
            for check in spec.reference_checks
            for finding in _reference_check_findings(spec, check, clean_rows, clean_rows_by_table)
        ),
    ]


def _table_issues(
    spec: TableSpec,
    rows_by_table: RowsByTable,
    findings_by_table: Mapping[str, Sequence[Finding]],
    clean_rows_by_table: RowsByTable,
) -> list[Issue]:
    rows = rows_by_table[spec.name]
    clean_rows = clean_rows_by_table[spec.name]
    findings = [
        *findings_by_table[spec.name],
        *_check_findings(spec, clean_rows, clean_rows_by_table),
    ]
    duplicate_issues = (_duplicate_issue(spec, key, rows) for key in spec.unique_keys)
    foreign_key_issues = (
        _foreign_key_issue(spec, foreign_key, clean_rows, rows_by_table)
        for foreign_key in spec.foreign_keys
    )
    return [
        *_grouped_issues(spec.name, findings),
        *(issue for issue in duplicate_issues if issue is not None),
        *(issue for issue in foreign_key_issues if issue is not None),
    ]


def _clean_rows(rows: Sequence[CsvRow], findings: Sequence[Finding]) -> list[CsvRow]:
    lines_with_findings = {finding.line for finding in findings}
    return [row for row in rows if row.line not in lines_with_findings]


def validate_csv_files(
    data_dir: Path, specs: Sequence[TableSpec] = TABLE_SPECS_IN_LOAD_ORDER
) -> ValidationReport:
    reads = {spec.name: _read_rows(data_dir, spec) for spec in specs}
    rows_by_table = {name: rows for name, (rows, read_issues) in reads.items() if not read_issues}
    readable_specs = [spec for spec in specs if spec.name in rows_by_table]
    findings_by_table = {
        spec.name: [
            finding for row in rows_by_table[spec.name] for finding in _column_findings(spec, row)
        ]
        for spec in readable_specs
    }
    clean_rows_by_table = {
        name: _clean_rows(rows, findings_by_table[name]) for name, rows in rows_by_table.items()
    }
    issues = [
        *_success_marker_issues(data_dir),
        *(issue for _rows, read_issues in reads.values() for issue in read_issues),
        *(
            issue
            for spec in readable_specs
            for issue in _table_issues(spec, rows_by_table, findings_by_table, clean_rows_by_table)
        ),
    ]
    row_counts = {name: len(rows) for name, rows in rows_by_table.items()}
    return ValidationReport(issues=tuple(issues), row_counts=row_counts)


def format_issues(issues: Sequence[Issue]) -> str:
    return "\n".join(
        f"[{issue.severity}] {issue.table} {issue.rule}: {issue.detail}" for issue in issues
    )
