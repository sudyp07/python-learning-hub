import os
import sys
import csv
import json

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Install: pip install matplotlib")
    sys.exit(1)


def load_manual():
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
        if value < 0:
            print("Negative values not allowed in pie charts.")
            continue
        labels.append(label)
        values.append(value)

    return labels, values


def load_csv(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = [r for r in reader if r]

    if not rows:
        return [], []

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
        if v < 0:
            continue
        labels.append(row[lbl_col].strip())
        values.append(v)

    return labels, values


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        labels = list(data.keys())
        values = [float(v) for v in data.values()]
    elif isinstance(data, list) and data and isinstance(data[0], dict):
        print("\nSample keys:", list(data[0].keys()))
        lbl_key = input("Label key: ").strip()
        val_key = input("Value key: ").strip()
        labels = [str(item.get(lbl_key, "")) for item in data]
        values = [float(item.get(val_key, 0)) for item in data]
    else:
        return [], []

    return labels, values


def draw_pie_chart(labels, values, title="Pie Chart", show_percent=True,
                   show_values=False, donut=False, explode_max=False,
                   min_percent=0.0, save=None, legend=True, custom_colors=None):

    # combine tiny slices into "Other"
    if min_percent > 0:
        total = sum(values)
        threshold = total * min_percent / 100
        kept_labels = []
        kept_values = []
        other_sum = 0

        for lbl, val in zip(labels, values):
            if val >= threshold:
                kept_labels.append(lbl)
                kept_values.append(val)
            else:
                other_sum += val

        if other_sum > 0:
            kept_labels.append("Other")
            kept_values.append(other_sum)

        labels, values = kept_labels, kept_values

    fig, ax = plt.subplots(figsize=(9, 7))

    colors = custom_colors if custom_colors else None

    explode = None
    if explode_max and values:
        max_idx = values.index(max(values))
        explode = [0.1 if i == max_idx else 0 for i in range(len(values))]

    def make_autopct(pct):
        if show_percent and show_values:
            return f"{pct:.1f}%\n({pct * sum(values) / 100:,.0f})"
        elif show_percent:
            return f"{pct:.1f}%"
        elif show_values:
            return f"{pct * sum(values) / 100:,.0f}"
        return ""

    wedge_props = {"edgecolor": "white", "linewidth": 1.5} if donut else {"edgecolor": "white", "linewidth": 1}

    wedges, texts, autotexts = ax.pie(
        values,
        labels=None if legend else labels,
        autopct=make_autopct,
        startangle=90,
        colors=colors,
        explode=explode,
        wedgeprops=wedge_props,
        textprops={"fontsize": 10}
    )

    if donut:
        centre_circle = plt.Circle((0, 0), 0.55, fc="white")
        ax.add_artist(centre_circle)

    if legend:
        ax.legend(
            wedges, labels,
            title="Categories",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.axis('equal')

    plt.tight_layout()

    if save:
        plt.savefig(save, dpi=120, bbox_inches='tight')
        print(f"Saved: {save}")

    plt.show()


def main():
    print("=== Pie Chart Generator ===\n")
    print("1. Manual input")
    print("2. Load from CSV")
    print("3. Load from JSON")

    choice = input("\nChoose: ").strip()

    if choice == '1':
        labels, values = load_manual()
    elif choice == '2':
        path = input("CSV path: ").strip().strip('"')
        if not os.path.isfile(path):
            print("Not found.")
            return
        labels, values = load_csv(path)
    elif choice == '3':
        path = input("JSON path: ").strip().strip('"')
        if not os.path.isfile(path):
            print("Not found.")
            return
        labels, values = load_json(path)
    else:
        print("Invalid.")
        return

    if not labels or not values:
        print("No data.")
        return

    total = sum(values)
    print(f"\nTotal items: {len(labels)}, Total value: {total:,.2f}")

    title = input("Chart title (default 'Pie Chart'): ").strip() or "Pie Chart"

    donut = input("Donut style? (y/n): ").strip().lower() == 'y'
    show_percent = input("Show percentages? (y/n, default y): ").strip().lower() != 'n'
    show_values = input("Show raw values? (y/n): ").strip().lower() == 'y'
    explode_max = input("Highlight largest slice? (y/n): ").strip().lower() == 'y'
    legend = input("Show legend? (y/n, default y): ").strip().lower() != 'n'

    min_input = input("Merge slices below X% into 'Other' (blank = none): ").strip()
    try:
        min_percent = float(min_input) if min_input else 0.0
    except ValueError:
        min_percent = 0.0

    palette_input = input("Use rainbow palette? (y/n, default y): ").strip().lower()
    if palette_input == 'n':
        custom_colors = None
    else:
        custom_colors = [
            "#e74c3c", "#3498db", "#2ecc71", "#f39c12",
            "#9b59b6", "#1abc9c", "#e67e22", "#34495e",
            "#16a085", "#c0392b", "#27ae60", "#2980b9",
            "#8e44ad", "#f1c40f", "#d35400", "#7f8c8d"
        ]

    save = input("Save PNG path (blank = don't save): ").strip() or None

    draw_pie_chart(
        labels, values,
        title=title,
        show_percent=show_percent,
        show_values=show_values,
        donut=donut,
        explode_max=explode_max,
        min_percent=min_percent,
        save=save,
        legend=legend,
        custom_colors=custom_colors
    )


if __name__ == "__main__":
    main()