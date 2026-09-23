import os
import sys
import json
import csv
import argparse
from collections import OrderedDict


def flatten_dict(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k

        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            if not v:
                items.append((new_key, ""))
            elif all(isinstance(x, (str, int, float, bool, type(None))) for x in v):
                items.append((new_key, "|".join(str(x) if x is not None else "" for x in v)))
            else:
                # complex list - serialize to JSON
                items.append((new_key, json.dumps(v, ensure_ascii=False)))
        else:
            items.append((new_key, v))
    return OrderedDict(items)


def collect_fields(records, flatten=True, sep="_"):
    fields = OrderedDict()

    for rec in records:
        if not isinstance(rec, dict):
            continue

        if flatten:
            flat = flatten_dict(rec, sep=sep)
        else:
            flat = rec

        for k in flat.keys():
            if k not in fields:
                fields[k] = None

    return list(fields.keys())


def normalize_value(value, null_value=""):
    if value is None:
        return null_value

    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, (int, float)):
        return value

    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)

    return value


def load_json_records(path, records_key=None):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if records_key:
        if isinstance(data, dict) and records_key in data:
            data = data[records_key]
        else:
            raise ValueError(f"Key '{records_key}' not found in JSON")

    # already a list of dicts
    if isinstance(data, list):
        if all(isinstance(x, dict) for x in data):
            return data
        # list of scalars
        return [{"value": x} for x in data]

    # dict
    if isinstance(data, dict):
        # check if it's a dict-of-columns: {"col": [values...]}
        all_lists = all(isinstance(v, list) for v in data.values())
        if all_lists and data:
            lengths = [len(v) for v in data.values() if isinstance(v, list)]
            if lengths and len(set(lengths)) == 1:
                # transpose to list of records
                keys = list(data.keys())
                records = []
                for i in range(lengths[0]):
                    records.append(OrderedDict((k, data[k][i]) for k in keys))
                return records

        # check if dict of key -> record
        all_dicts = all(isinstance(v, dict) for v in data.values())
        if all_dicts and data:
            records = []
            for k, v in data.items():
                rec = OrderedDict()
                rec["_key"] = k
                rec.update(v)
                records.append(rec)
            return records

        # single record
        return [data]

    return [{"value": data}]


def json_to_csv(path, output=None, records_key=None, flatten=True,
                delimiter=",", flatten_sep="_", null_value="",
                sort_fields=False, field_order=None, encoding="utf-8"):

    records = load_json_records(path, records_key=records_key)

    if not records:
        print("No records found.")
        return

    # determine fields
    if field_order:
        fields = field_order
    else:
        fields = collect_fields(records, flatten=flatten, sep=flatten_sep)

    if not fields:
        print("No fields detected.")
        return

    if sort_fields and not field_order:
        fields = sorted(fields)

    # write to output
    if output:
        f = open(output, "w", encoding=encoding, newline="")
        close_after = True
    else:
        f = sys.stdout
        close_after = False

    try:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=delimiter,
                                extrasaction="ignore", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

        for rec in records:
            if flatten:
                flat = flatten_dict(rec, sep=flatten_sep)
            else:
                flat = rec

            row = OrderedDict()
            for field in fields:
                row[field] = normalize_value(flat.get(field), null_value)

            writer.writerow(row)

        if output:
            print(f"Saved: {output}")
            print(f"Records: {len(records)}")
            print(f"Fields:  {len(fields)}")

    finally:
        if close_after:
            f.close()


def batch_convert(input_dir, output_dir, pattern=".json"):
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
        dst = os.path.join(output_dir, base + ".csv")

        try:
            json_to_csv(src, output=dst)
        except Exception as e:
            print(f"  Failed {fname}: {e}")


def interactive_mode():
    print("=== JSON to CSV Converter ===\n")

    path = input("JSON file path: ").strip().strip('"')

    if not os.path.isfile(path):
        print("File not found.")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            preview = f.read(2000)

        try:
            data = json.loads(preview)
            if isinstance(data, dict):
                print(f"\nTop-level keys: {list(data.keys())[:10]}")
            elif isinstance(data, list):
                print(f"\nTop-level: array with {len(data)} items")
                if data and isinstance(data[0], dict):
                    print(f"Item keys: {list(data[0].keys())[:10]}")
        except json.JSONDecodeError:
            print("(Preview shows large file, loading full...)")
    except OSError as e:
        print(f"Could not preview: {e}")
        return

    key_input = input("\nRecords key (blank if top-level is array): ").strip()
    records_key = key_input or None

    flat_choice = input("Flatten nested objects? (y/n, default y): ").strip().lower()
    flatten = flat_choice != "n"

    sep = "_"
    if flatten:
        sep_input = input("Nested key separator (default _): ").strip()
        sep = sep_input or "_"

    delim_input = input("Delimiter (default ','): ").strip()
    delimiter = delim_input if delim_input else ","

    sort_choice = input("Sort columns alphabetically? (y/n): ").strip().lower()
    sort_fields = sort_choice == "y"

    out = input("Save to (default output.csv): ").strip() or "output.csv"

    try:
        json_to_csv(
            path, output=out,
            records_key=records_key,
            flatten=flatten,
            delimiter=delimiter,
            flatten_sep=sep,
            sort_fields=sort_fields
        )
    except Exception as e:
        print(f"Failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="JSON to CSV Converter")
    parser.add_argument("input", nargs="?", help="JSON file or directory")
    parser.add_argument("-o", "--output", help="Output CSV file")
    parser.add_argument("-k", "--key", help="Key that holds records (if nested)")
    parser.add_argument("--no-flatten", action="store_true",
                        help="Do not flatten nested objects")
    parser.add_argument("--sep", default="_", help="Nested key separator")
    parser.add_argument("-d", "--delimiter", default=",", help="CSV delimiter")
    parser.add_argument("--null", default="", help="Value for nulls")
    parser.add_argument("--sort-fields", action="store_true",
                        help="Sort columns alphabetically")
    parser.add_argument("--fields", help="Comma-separated field order")
    parser.add_argument("--batch", action="store_true",
                        help="Batch convert a directory")

    args = parser.parse_args()

    if not args.input:
        interactive_mode()
        return

    if args.batch:
        if not os.path.isdir(args.input):
            print("For batch mode, input must be a directory.")
            return
        out_dir = args.output or "csv_output"
        batch_convert(args.input, out_dir)
        return

    if not os.path.isfile(args.input):
        print(f"Not found: {args.input}")
        return

    field_order = None
    if args.fields:
        field_order = [f.strip() for f in args.fields.split(",") if f.strip()]

    json_to_csv(
        args.input,
        output=args.output,
        records_key=args.key,
        flatten=not args.no_flatten,
        delimiter=args.delimiter,
        flatten_sep=args.sep,
        null_value=args.null,
        sort_fields=args.sort_fields,
        field_order=field_order
    )


if __name__ == "__main__":
    main()