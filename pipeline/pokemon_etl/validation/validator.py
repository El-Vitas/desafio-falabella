import csv
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from itertools import groupby
from operator import attrgetter
from pathlib import Path

from pokemon_etl.constants.paths import SUCCESS_MARKER_FILE_NAME
from pokemon_etl.constants.validation import (
    ALL_TABLES,
    EXTRA_FIELDS_KEY,
    INTEGER_PATTERN,
    ISSUE_SAMPLE_SIZE,
)
from pokemon_etl.validation.enums import ColumnKind, Severity
from pokemon_etl.validation.models import (
    ColumnSpec,
    CsvRow,
    Finding,
    ForeignKeySpec,
    Issue,
    TableSpec,
    ValidationReport,
    ValueProblem,
)
from pokemon_etl.validation.rules import TABLE_SPECS_IN_LOAD_ORDER


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
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        header = tuple(reader.fieldnames or ())
        if header != spec.column_names:
            detail = f"expected {list(spec.column_names)}, found {list(header)}"
            return [], [Issue(Severity.ERROR, spec.name, "columns", detail)]
        rows = [CsvRow(line=reader.line_num, values=values) for values in reader]
    return rows, []


def _is_empty(value: str | None) -> bool:
    return value is None or not value.strip()


def _column_problem(column: ColumnSpec, value: str | None) -> ValueProblem | None:
    if _is_empty(value):
        return ValueProblem(column.empty_severity, "empty")
    if column.kind is not ColumnKind.INTEGER:
        return None
    if not re.fullmatch(INTEGER_PATTERN, value.strip()):
        return ValueProblem(Severity.ERROR, "not_an_integer")
    if column.minimum is not None and int(value) < column.minimum:
        return ValueProblem(Severity.ERROR, f"below_minimum_{column.minimum}")
    return None


def _has_wrong_field_count(row: CsvRow) -> bool:
    return EXTRA_FIELDS_KEY in row.values or None in row.values.values()


def _row_findings(spec: TableSpec, row: CsvRow) -> list[Finding]:
    if _has_wrong_field_count(row):
        return [Finding(Severity.ERROR, "*", "field_count", row.line)]
    return [
        Finding(problem.severity, column.name, problem.rule, row.line)
        for column in spec.columns
        if (problem := _column_problem(column, row.values[column.name])) is not None
    ]


def _grouped_issue(table: str, findings: list[Finding]) -> Issue:
    first = findings[0]
    lines = [finding.line for finding in findings]
    detail = f"{first.column}: {len(lines)} rows, lines {_sample(lines)}"
    return Issue(first.severity, table, first.rule, detail)


def _value_issues(spec: TableSpec, rows: Sequence[CsvRow]) -> list[Issue]:
    findings = sorted(finding for row in rows for finding in _row_findings(spec, row))
    return [
        _grouped_issue(spec.name, list(group))
        for _key, group in groupby(findings, key=attrgetter("severity", "column", "rule"))
    ]


def _duplicate_issue(
    spec: TableSpec, key_columns: tuple[str, ...], rows: Sequence[CsvRow]
) -> Issue | None:
    counts = Counter(tuple(row.values.get(column) for column in key_columns) for row in rows)
    duplicates = sorted((key for key, count in counts.items() if count > 1), key=str)
    if not duplicates:
        return None
    detail = f"{'/'.join(key_columns)} repeated: {_sample(duplicates)}"
    return Issue(Severity.ERROR, spec.name, "unique", detail)


def _foreign_key_issue(
    spec: TableSpec,
    foreign_key: ForeignKeySpec,
    rows: Sequence[CsvRow],
    rows_by_table: Mapping[str, Sequence[CsvRow]],
) -> Issue | None:
    if foreign_key.referenced_table not in rows_by_table:
        return None
    referenced_values = {
        row.values.get(foreign_key.referenced_column)
        for row in rows_by_table[foreign_key.referenced_table]
    }
    missing_lines = [
        row.line for row in rows if row.values.get(foreign_key.column) not in referenced_values
    ]
    if not missing_lines:
        return None
    detail = (
        f"{foreign_key.column} not found in {foreign_key.referenced_table}."
        f"{foreign_key.referenced_column}: {len(missing_lines)} rows, "
        f"lines {_sample(missing_lines)}"
    )
    return Issue(Severity.ERROR, spec.name, "foreign_key", detail)


def _table_issues(spec: TableSpec, rows_by_table: Mapping[str, Sequence[CsvRow]]) -> list[Issue]:
    rows = rows_by_table[spec.name]
    duplicate_issues = (_duplicate_issue(spec, key, rows) for key in spec.unique_keys)
    foreign_key_issues = (
        _foreign_key_issue(spec, foreign_key, rows, rows_by_table)
        for foreign_key in spec.foreign_keys
    )
    return [
        *_value_issues(spec, rows),
        *(issue for issue in duplicate_issues if issue is not None),
        *(issue for issue in foreign_key_issues if issue is not None),
    ]


def validate_csv_files(
    data_dir: Path, specs: Sequence[TableSpec] = TABLE_SPECS_IN_LOAD_ORDER
) -> ValidationReport:
    reads = {spec.name: _read_rows(data_dir, spec) for spec in specs}
    rows_by_table = {name: rows for name, (rows, read_issues) in reads.items() if not read_issues}
    issues = [
        *_success_marker_issues(data_dir),
        *(issue for _rows, read_issues in reads.values() for issue in read_issues),
        *(
            issue
            for spec in specs
            if spec.name in rows_by_table
            for issue in _table_issues(spec, rows_by_table)
        ),
    ]
    row_counts = {name: len(rows) for name, rows in rows_by_table.items()}
    return ValidationReport(issues=tuple(issues), row_counts=row_counts)


def format_issues(issues: Sequence[Issue]) -> str:
    return "\n".join(
        f"[{issue.severity}] {issue.table} {issue.rule}: {issue.detail}" for issue in issues
    )
