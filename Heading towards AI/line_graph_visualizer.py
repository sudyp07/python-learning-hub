import os
import sys
import csv
import json

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
except ImportError:
    print("Install: pip install matplotlib")
    sys.exit(1)

from datetime import datetime


def to_float(v):
    if v is None:
        return None
    v = str(v).strip().replace(",", "").replace("$", "").replace("%", "")
    if v == "":
        return None
    try:
        return float(v)
    except ValueError:
        return None


def try_parse_date(value):
    if value is None:
        return None
    value = str(value).strip()
    formats = [
        "%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y",
        "%m/%d/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S",
        "%d %b %Y", "%b %d %Y", "%B %d %Y"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def load_manual():
    print("\nEnter series name, then x,y pairs (blank series name to finish).")

    series = {}

    while True:
        name = input("Series name: ").strip()
        if not name:
            break

        xs = []
        ys = []

        print(f"  Enter x,y pairs for '{name}'. Blank x to finish series.")
        while True:
            x_in = input("  x: ").strip()
            if not x_in:
                break
            y_in = input("  y: ").strip()

            x_date = try_parse_date(x_in)
            if x_date:
                xs.append(x_date)
            else:
                xs.append(x_in)

            ys.append(to_float(y_in))

        if xs:
            series[name] = (xs, ys)

    return series


def load_csv(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = [r for r in reader if any(c.strip() for c in r)]

    if not rows:
        return {}

    header = rows[0]
    data = rows[1:]

    print("\nColumns:")
    for i, h in enumerate(header):
        print(f"  {i}. {h}")

    x_col = int(input("X column index: ").strip())
    y_cols_input = input("Y column indices (comma-separated): ").strip()
    y_cols = [int(x.strip()) for x in y_cols_input.split(",")]

    series = {}

    for yc in y_cols:
        xs = []
        ys = []
        for row in data:
            if len(row) <= max(x_col, yc):
                continue
            x_raw = row[x_col].strip()
            x_date = try_parse_date(x_raw)
            x_val = x_date if x_date else x_raw
            y_val = to_float(row[yc])
            if y_val is None:
                continue
            xs.append(x_val)
            ys.append(y_val)
        series[header[yc]] = (xs, ys)

    return series


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    series = {}

    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, list) and v and isinstance(v[0], (int, float)):
                xs = list(range(len(v)))
                ys = v
                series[k] = (xs, ys)
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                print(f"\nSeries '{k}' keys: {list(v[0].keys())}")
                xk = input("X key: ").strip()
                yk = input("Y key: ").strip()
                xs = [try_parse_date(item.get(xk)) or item.get(xk) for item in v]
                ys = [to_float(item.get(yk)) for item in v]
                series[k] = (xs, ys)
    elif isinstance(data, list) and data and isinstance(data[0], dict):
        print(f"\nKeys: {list(data[0].keys())}")
        xk = input("X key: ").strip()
        yk = input("Y key: ").strip()
        xs = [try_parse_date(item.get(xk)) or item.get(xk) for item in data]
        ys = [to_float(item.get(yk)) for item in data]
        series[yk] = (xs, ys)

    return series


def draw_line_graph(series, title="Line Graph", xlabel="X", ylabel="Y",
                    markers=True, grid=True, fill=False,
                    smooth=False, save=None, styles=None):

    fig, ax = plt.subplots(figsize=(11, 6))

    default_colors = [
        "#3498db", "#e74c3c", "#2ecc71", "#f39c12",
        "#9b59b6", "#1abc9c", "#e67e22", "#34495e",
        "#16a085", "#c0392b", "#2980b9", "#8e44ad"
    ]
    default_markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h', 'X', 'P']
    default_styles = ['-', '--', '-.', ':']

    for i, (name, (xs, ys)) in enumerate(series.items()):
        color = default_colors[i % len(default_colors)]
        marker = default_markers[i % len(default_markers)] if markers else None
        linestyle = default_styles[i % len(default_styles)]

        # filter out None y values
        filtered = [(x, y) for x, y in zip(xs, ys) if y is not None and x is not None]
        if not filtered:
            continue

        fxs, fys = zip(*filtered)

        ax.plot(
            fxs, fys,
            label=name,
            color=color,
            marker=marker,
            markersize=5,
            linestyle=linestyle,
            linewidth=2
        )

        if fill:
            ax.fill_between(fxs, fys, alpha=0.15, color=color)

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if grid:
        ax.grid(True, alpha=0.3)

    ax.legend(loc='best')

    # handle date axis
    all_x = []
    for xs, _ in series.values():
        all_x.extend([x for x in xs if isinstance(x, datetime)])
    if all_x:
        fig.autofmt_xdate(rotation=45)

    plt.tight_layout()

    if save:
        plt.savefig(save, dpi=120, bbox_inches='tight')
        print(f"Saved: {save}")

    plt.show()


def main():
    print("=== Line Graph Visualizer ===\n")
    print("1. Manual input")
    print("2. Load from CSV")
    print("3. Load from JSON")

    choice = input("\nChoose: ").strip()

    if choice == '1':
        series = load_manual()
    elif choice == '2':
        path = input("CSV path: ").strip().strip('"')
        if not os.path.isfile(path):
            print("Not found.")
            return
        series = load_csv(path)
    elif choice == '3':
        path = input("JSON path: ").strip().strip('"')
        if not os.path.isfile(path):
            print("Not found.")
            return
        series = load_json(path)
    else:
        print("Invalid.")
        return

    if not series:
        print("No data loaded.")
        return

    print(f"\nLoaded {len(series)} series:")
    for name, (xs, ys) in series.items():
        valid = sum(1 for y in ys if y is not None)
        print(f"  {name}: {valid} points")

    title = input("\nChart title (default 'Line Graph'): ").strip() or "Line Graph"
    xlabel = input("X label (default 'X'): ").strip() or "X"
    ylabel = input("Y label (default 'Y'): ").strip() or "Y"

    markers = input("Show markers? (y/n, default y): ").strip().lower() != 'n'
    grid = input("Show grid? (y/n, default y): ").strip().lower() != 'n'
    fill = input("Fill area below lines? (y/n): ").strip().lower() == 'y'

    save = input("Save PNG path (blank = don't save): ").strip() or None

    draw_line_graph(
        series,
        title=title, xlabel=xlabel, ylabel=ylabel,
        markers=markers, grid=grid, fill=fill, save=save
    )


if __name__ == "__main__":
    main()