"""Quality checks and a compact summary report for the sample price CSV."""
from pathlib import Path
import csv
import re


REQUIRED_COLUMNS = ("month", "item_code", "item_name", "index_value", "source")
MONTH_PATTERN = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def inspect_csv(path):
    """Return quality diagnostics for a CSV without changing the input file."""
    path = Path(path)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in headers]
        if missing_columns:
            return {
                "path": str(path), "rows": 0, "missing_columns": missing_columns,
                "missing_values": {}, "duplicate_keys": [], "invalid_months": [],
            }

        missing_values = {column: [] for column in REQUIRED_COLUMNS}
        duplicate_keys = []
        invalid_months = []
        seen_keys = {}
        row_count = 0
        for line_number, row in enumerate(reader, start=2):
            row_count += 1
            for column in REQUIRED_COLUMNS:
                value = row.get(column)
                if value is None or not value.strip():
                    missing_values[column].append(line_number)

            month = (row.get("month") or "").strip()
            if not MONTH_PATTERN.fullmatch(month):
                invalid_months.append({"line": line_number, "value": month})

            item_code = (row.get("item_code") or "").strip()
            if month and item_code:
                key = (month, item_code)
                if key in seen_keys:
                    duplicate_keys.append({
                        "month": month, "item_code": item_code,
                        "lines": [seen_keys[key], line_number],
                    })
                else:
                    seen_keys[key] = line_number

    return {
        "path": str(path), "rows": row_count, "missing_columns": [],
        "missing_values": {key: lines for key, lines in missing_values.items() if lines},
        "duplicate_keys": duplicate_keys, "invalid_months": invalid_months,
    }


def format_report(diagnostics):
    """Format diagnostics as a human-readable summary."""
    missing_count = sum(len(lines) for lines in diagnostics["missing_values"].values())
    issues = bool(
        diagnostics["missing_columns"] or missing_count
        or diagnostics["duplicate_keys"] or diagnostics["invalid_months"]
    )
    lines = [f"CSV quality report: {diagnostics['path']}", f"Rows: {diagnostics['rows']}"]
    lines.append("Missing required columns: " + (
        ", ".join(diagnostics["missing_columns"]) or "none"
    ))
    lines.append(f"Missing values: {missing_count}")
    for column, row_numbers in diagnostics["missing_values"].items():
        lines.append(f"  {column}: {len(row_numbers)} (lines {', '.join(map(str, row_numbers))})")
    lines.append(f"Duplicate month/item_code keys: {len(diagnostics['duplicate_keys'])}")
    for duplicate in diagnostics["duplicate_keys"]:
        lines.append(
            f"  {duplicate['month']} / {duplicate['item_code']}: lines "
            f"{', '.join(map(str, duplicate['lines']))}"
        )
    lines.append(f"Invalid month values: {len(diagnostics['invalid_months'])}")
    for invalid in diagnostics["invalid_months"]:
        lines.append(f"  line {invalid['line']}: {invalid['value']!r} (expected YYYY-MM)")
    lines.append("Result: " + ("FAIL" if issues else "PASS"))
    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Check sample price CSV quality.")
    parser.add_argument(
        "csv_path", nargs="?",
        default=Path(__file__).resolve().parents[1] / "data" / "sample_prices.csv",
        help="CSV to inspect (defaults to data/sample_prices.csv)",
    )
    args = parser.parse_args()
    diagnostics = inspect_csv(args.csv_path)
    print(format_report(diagnostics))
    if (diagnostics["missing_columns"] or diagnostics["missing_values"]
            or diagnostics["duplicate_keys"] or diagnostics["invalid_months"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
