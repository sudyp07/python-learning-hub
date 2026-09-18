import os
import sys
import csv
import json

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Install: pip install matplotlib numpy")
    sys.exit(1)


def parse_input():
    print("=== Bar Chart Generator ===\n")
    print("1. Enter data manually")
    print("2. Load from CSV")
    print("3. Load from JSON")

    choice = input("\nChoose: ").strip()

    if choice == '1':
        labels = []
        values = []

        print("\nEnter label,value pairs. Blank label to finish.")
        while True:
            label = input("Label: ").strip()
            if not label:
                break
            try:
                value = float(input(f"Value for '{label}': ").strip())
            except ValueError:
                print("Invalid number.")
                continue
            labels.append(label)
            values.append(value)

        return labels, values

    elif choice == '2':
        path = input("CSV path: ").strip().strip('"')
        if not os.path.isfile(path):
            print("Not found.")
            return None, None

        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            rows = [r for r in reader if r]

        if not rows:
            return None, None

        print("\nColumns:", rows[0])
        lbl_col = int(input("Label column index: ").strip())
        val_col = int(input("Value column index: ").strip())

        labels = []
        values = []

        for row in rows[1:]:
            if len(row) <= max(lbl_col, val_col):
                continue
            try:
                v = float(row[val_col].replace(",", "").replace("$", "").strip())
            except ValueError:
                continue
            labels.append(row[lbl_col].strip())
            values.append(v)

        return labels, values

    elif choice == '3':
        path = input("JSON path: ").strip().strip('"')
        if not os.path.isfile(path):
            print("Not found.")
            return None, None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            return list(data.keys()), list(data.values())
        elif isinstance(data, list) and data and isinstance(data[0], dict):
            print("\nSample keys:", list(data[0].keys()))
            lbl_key = input("Label key: ").strip()
            val_key = input("Value key: ").strip()
            labels = [str(item.get(lbl_key, "")) for item in data]
            values = [float(item.get(val_key, 0)) for item in data]
            return labels, values
        else:
            print("Unsupported JSON format.")
            return None, None

    return None, None


def draw_bar_chart(labels, values, title="Bar Chart", xlabel="Category", ylabel="Value",
                   color="steelblue", horizontal=False, sort=False, top_n=None,
                   show_values=True, save=None):

    if sort:
        pairs = sorted(zip(labels, values), key=lambda p: p[1], reverse=True)
        labels = [p[0] for p in pairs]
        values = [p[1] for p in pairs]

    if top_n and top_n > 0:
        labels = labels[:top_n]
        values = values[:top_n]

    fig, ax = plt.subplots(figsize=(max(8, len(labels) * 0.5), 6))

    if isinstance(color, str) and color.startswith("#"):
        colors = color
    elif isinstance(color, list):
        colors = color[:len(labels)]
        while len(colors) < len(labels):
            colors.append("steelblue")
    else:
        cmap = plt.cm.get_cmap("viridis", len(labels))
        colors = [cmap(i) for i in range(len(labels))]

    if horizontal:
        bars = ax.barh(labels, values, color=colors)
        ax.set_xlabel(ylabel)
        ax.set_ylabel(xlabel)
        if show_values:
            for bar in bars:
                w = bar.get_width()
                ax.text(w, bar.get_y() + bar.get_height() / 2,
                        f" {w:,.2f}", va='center', fontsize=9)
    else:
        bars = ax.bar(labels, values, color=colors)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if show_values:
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, h,
                        f"{h:,.2f}", ha='center', va='bottom', fontsize=9)

        plt.xticks(rotation=45, ha='right')

    ax.set_title(title)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    if save:
        plt.savefig(save, dpi=120)
        print(f"Saved: {save}")

    plt.show()


def main():
    labels, values = parse_input()

    if not labels:
        print("No data.")
        return

    print(f"\nLoaded {len(labels)} items.")

    title = input("Chart title (default 'Bar Chart'): ").strip() or "Bar Chart"
    xlabel = input("X-axis label (default 'Category'): ").strip() or "Category"
    ylabel = input("Y-axis label (default 'Value'): ").strip() or "Value"

    color_input = input("Bar color (name, #hex, or 'rainbow'): ").strip() or "steelblue"
    if color_input.lower() == "rainbow":
        color = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6", "#1abc9c"]
    else:
        color = color_input

    horizontal = input("Horizontal bars? (y/n): ").strip().lower() == 'y'
    sort_bars = input("Sort by value descending? (y/n): ").strip().lower() == 'y'

    top_input = input("Show top N only (blank = all): ").strip()
    top_n = int(top_input) if top_input.isdigit() else None

    show_values = input("Show values on bars? (y/n, default y): ").strip().lower() != 'n'

    save = input("Save PNG path (blank = don't save): ").strip() or None

    draw_bar_chart(
        labels, values,
        title=title, xlabel=xlabel, ylabel=ylabel,
        color=color, horizontal=horizontal, sort=sort_bars,
        top_n=top_n, show_values=show_values, save=save
    )


if __name__ == "__main__":
    main()