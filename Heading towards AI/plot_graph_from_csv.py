import csv
import os
import sys

try:
    import matplotlib.pyplot as plt
    import matplotlib
except ImportError:
    print("Install matplotlib: pip install matplotlib")
    sys.exit(1)


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        sample = f.read(2048)
        f.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.excel

        reader = csv.reader(f, dialect)
        rows = [row for row in reader if any(cell.strip() for cell in row)]

    if not rows:
        return [], []

    header = rows[0]
    data = rows[1:]
    return header, data


def to_float(value):
    if value is None:
        return None
    value = str(value).strip().replace(",", "").replace("$", "").replace("%", "")
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def detect_numeric_columns(header, data):
    numeric = []
    for i in range(len(header)):
        count = 0
        total = 0
        for row in data[:50]:
            if i < len(row):
                val = to_float(row[i])
                if val is not None:
                    count += 1
                total += 1
        if total > 0 and count / total > 0.7:
            numeric.append(i)
    return numeric


def pick_column(prompt, header):
    print(f"\n{prompt}")
    for i, name in enumerate(header):
        print(f"  {i}. {name}")

    while True:
        choice = input("Enter column number: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 0 <= idx < len(header):
                return idx
        print("Invalid. Try again.")


def plot_csv(path, x_col, y_cols, title=None, xlabel=None, ylabel=None,
             show_grid=True, save=None, plot_type="line"):

    header, data = read_csv(path)
    if not header:
        print("CSV empty.")
        return

    x_values = []
    y_series = {c: [] for c in y_cols}

    for row in data:
        if x_col >= len(row):
            continue

        x_raw = row[x_col].strip()
        try:
            x_val = float(x_raw.replace(",", ""))
        except ValueError:
            x_val = x_raw

        x_values.append(x_val)

        for c in y_cols:
            if c < len(row):
                y_series[c].append(to_float(row[c]))
            else:
                y_series[c].append(None)

    fig, ax = plt.subplots(figsize=(10, 6))

    for c in y_cols:
        label = header[c]
        ys = y_series[c]

        if plot_type == "line":
            xs_filtered = [x for x, y in zip(x_values, ys) if y is not None]
            ys_filtered = [y for y in ys if y is not None]
            ax.plot(xs_filtered, ys_filtered, marker='o', markersize=3, label=label)

        elif plot_type == "bar":
            xs_filtered = [str(x) for x, y in zip(x_values, ys) if y is not None]
            ys_filtered = [y for y in ys if y is not None]
            ax.bar(xs_filtered, ys_filtered, label=label)

        elif plot_type == "scatter":
            xs_filtered = [x for x, y in zip(x_values, ys) if y is not None]
            ys_filtered = [y for y in ys if y is not None]
            ax.scatter(xs_filtered, ys_filtered, label=label, s=20)

    ax.set_title(title or f"Plot of {os.path.basename(path)}")
    ax.set_xlabel(xlabel or header[x_col])
    ax.set_ylabel(ylabel or "Value")

    if show_grid:
        ax.grid(True, alpha=0.3)

    if len(y_cols) > 1 or plot_type == "bar":
        ax.legend()

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    if save:
        plt.savefig(save, dpi=100)
        print(f"Saved: {save}")

    plt.show()


def main():
    print("=== CSV Plotter ===\n")

    path = input("CSV file path: ").strip().strip('"')

    if not os.path.isfile(path):
        print("File not found.")
        return

    header, data = read_csv(path)

    if not header:
        print("No data in CSV.")
        return

    print(f"\nRows: {len(data)}")
    print(f"Columns: {header}")

    numeric_cols = detect_numeric_columns(header, data)
    print(f"Numeric columns: {[header[i] for i in numeric_cols]}")

    x_col = pick_column("Pick X-axis column:", header)

    print("\nPick Y-axis column(s). Enter comma-separated numbers.")
    for i, name in enumerate(header):
        print(f"  {i}. {name}")

    while True:
        choice = input("Y columns: ").strip()
        try:
            y_cols = [int(x.strip()) for x in choice.split(",")]
            if all(0 <= c < len(header) for c in y_cols) and y_cols:
                break
        except ValueError:
            pass
        print("Invalid.")

    print("\nPlot types: line, bar, scatter")
    plot_type = input("Choose (default line): ").strip().lower() or "line"
    if plot_type not in ("line", "bar", "scatter"):
        plot_type = "line"

    title = input("Title (blank for default): ").strip() or None
    xlabel = input("X label (blank for column name): ").strip() or None
    ylabel = input("Y label (blank for 'Value'): ").strip() or None

    save = input("Save to PNG? Enter path or leave blank: ").strip() or None

    plot_csv(path, x_col, y_cols, title, xlabel, ylabel, save=save, plot_type=plot_type)


if __name__ == "__main__":
    main()