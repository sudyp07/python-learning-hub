import os
import sys
import csv
import json
import argparse
from collections import OrderedDict


def sniff_dialect(path, sample_size=8192):
    with open(path, "r", encoding="utf-8-sig", errors="ignore") as f:
        sample = f.read(sample_size)

    try:
        dialect = csv.Sniffer().sniff(sample)
        return dialect
    except csv.Error:
        return csv.excel


def has_header(path, sample_size=8192):
    with open(path, "r", encoding="utf-8-sig", errors="ignore") as f:
        sample = f.read(sample_size)

    try:
        return csv.Sniffer().has_header(sample)
    except csv.Error:
        return True


def convert_value(value, auto_type=True):
    if not auto_type:
        return value

    if value is None:
        return None

    s = str(value).strip()

    if s == "":
        return ""

    # boolean
    low = s.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False

    if low in ("null", "none"):
        return None

    # integer
    try:
        if "." not in s and "e" not in low:
            return int(s)
    except ValueError:
        pass

    # float
    try:
        f = float(s)
        return f
    except ValueError:
        pass

    return s


def parse_field_types(values):
    """Given a list of string values, decide type for a column."""
    if not values:
        return "string"

    non_empty = [v for v in values if v is not None and str(v).strip() != ""]

    if not non_empty:
        return "string"

    all_int = True
    all_float = True
    all_bool = True
    all_null = True

    for v in non_empty:
        s = str(v).strip()
        low = s.lower()

        if low in ("null", "none"):
            continue

        all_null = False

        if low not in ("true", "false", "yes", "no"):
            all_bool = False

        try:
            if "." in s or "e" in low:
                raise ValueError
            int(s)
        except ValueError:
            all_int = False

        try:
            float(s)
        except ValueError:
            all_float = False

    if all_null:
        return "null"
    if all_bool:
        return "bool"
    if all_int:
        return "int"
    if all_float:
        return "float"
    return "string"


def coerce(value, field_type):
    if value is None:
        return None

    s = str(value).strip()

    if field_type == "int":
        try:
            return int(s)
        except ValueError:
            return None

    if field_type == "float":
        try:
            return float(s)
        except ValueError:
            return None

    if field_type == "bool":
        return s.lower() in ("true", "yes", "1")

    if field_type == "null":
        return None

    return value


def convert_csv_to_json(path, output=None, header=True, auto_type=True,
                        delimiter=None, indent=2, compact=False,
                        records=True, keep_empty=True, encoding="utf-8"):

    dialect = sniff_dialect(path)

    if delimiter:
        dialect = csv.excel
        dialect.delimiter = delimiter

    if header is None:
        header = has_header(path)

    with open(path, "r", encoding=encoding + "-sig" if encoding == "utf-8" else encoding,
              errors="ignore", newline="") as f:
        reader = csv.reader(f, dialect)

        rows = []
        for row in reader:
            if not any(cell.strip() for cell in row):
                continue
            rows.append(row)

    if not rows:
        return [] if records else {}

    if header:
        column_names = [c.strip() for c in rows[0]]
        data_rows = rows[1:]
    else:
        col_count = max(len(r) for r in rows)
        column_names = [f"col_{i + 1}" for i in range(col_count)]
        data_rows = rows

    # detect field types
    if auto_type:
        field_types = {}
        for i, col in enumerate(column_names):
            values = [r[i] if i < len(r) else None for r in data_rows]
            field_types[i] = parse_field_types(values)

    if records:
        result = []
        for row in data_rows:
            record = OrderedDict()
            for i, col in enumerate(column_names):
                val = row[i] if i < len(row) else ""

                if not keep_empty and (val is None or str(val).strip() == ""):
                    continue

                if auto_type:
                    val = coerce(val, field_types.get(i, "string"))
                record[col] = val
            result.append(record)
    else:
        # dict of column -> list of values
        result = OrderedDict()
        for i, col in enumerate(column_names):
            values = []
            for row in data_rows:
                val = row[i] if i < len(row) else ""
                if auto_type:
                    val = coerce(val, field_types.get(i, "string"))
                values.append(val)
            result[col] = values

    json_str = json.dumps(
        result,
        indent=None if compact else indent,
        ensure_ascii=False,
        default=str
    )

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"Saved: {output}")
        print(f"Records: {len(result) if records else len(column_names)}")
    else:
        print(json_str)

    return result


def batch_convert(input_dir, output_dir, pattern=".csv"):
    if not os.path.isdir(input_dir):
        print(f"Not a directory: {input_dir}")
        return

    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.lower().endswith(pattern)]

    if not files:
        print("No matching files.")
        return

    print(f"Converting {len(files)} files...\n")

    for fname in files:
        src = os.path.join(input_dir, fname)
        base = os.path.splitext(fname)[0]
        dst = os.path.join(output_dir, base + ".json")

        try:
            convert_csv_to_json(src, output=dst, header=True, auto_type=True)
        except Exception as e:
            print(f"  Failed {fname}: {e}")


def main():
    parser = argparse.ArgumentParser(description="CSV to JSON Converter")
    parser.add_argument("input", nargs="?", help="CSV file or directory")
    parser.add_argument("-o", "--output", help="Output JSON file")
    parser.add_argument("-d", "--delimiter", help="CSV delimiter (auto if not set)")
    parser.add_argument("--no-header", action="store_true", help="CSV has no header row")
    parser.add_argument("--no-type", action="store_true", help="Do not auto-detect types")
    parser.add_argument("--compact", action="store_true", help="Compact JSON output")
    parser.add_argument("--dict", action="store_true",
                        help="Output as dict of columns instead of list of records")
    parser.add_argument("--batch", action="store_true",
                        help="Batch convert directory of CSVs")
    parser.add_argument("--skip-empty", action="store_true",
                        help="Skip empty values in records")

    args = parser.parse_args()

    if not args.input:
        print("=== CSV to JSON Converter ===\n")
        path = input("CSV file path: ").strip().strip('"')

        if not os.path.isfile(path):
            print("File not found.")
            return

        print(f"\nDetected dialect: delimiter={sniff_dialect(path).delimiter!r}")
        print(f"Has header row: {has_header(path)}")

        header_choice = input("Use first row as header? (y/n, default y): ").strip().lower()
        use_header = header_choice != "n"

        type_choice = input("Auto-detect types? (y/n, default y): ").strip().lower()
        auto_type = type_choice != "n"

        dict_choice = input("Output as list of records? (y/n, default y): ").strip().lower()
        records = dict_choice != "n"

        out = input("Save to (default output.json): ").strip() or "output.json"

        try:
            convert_csv_to_json(
                path, output=out,
                header=use_header, auto_type=auto_type,
                records=records
            )
        except Exception as e:
            print(f"Failed: {e}")
        return

    if args.batch:
        if not os.path.isdir(args.input):
            print("For batch mode, input must be a directory.")
            return
        out_dir = args.output or "json_output"
        batch_convert(args.input, out_dir)
        return

    if not os.path.isfile(args.input):
        print(f"Not found: {args.input}")
        return

    header = None if args.no_header else has_header(args.input)

    convert_csv_to_json(
        args.input,
        output=args.output,
        header=header,
        auto_type=not args.no_type,
        delimiter=args.delimiter,
        compact=args.compact,
        records=not args.dict,
        keep_empty=not args.skip_empty
    )


if __name__ == "__main__":
    main()