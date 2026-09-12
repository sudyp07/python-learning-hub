import os
import sys

def format_size(bytes_val):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} PB"

def count_items(path):
    files = 0
    dirs = 0
    total_size = 0

    for root, dirnames, filenames in os.walk(path):
        dirs += len(dirnames)
        for f in filenames:
            files += 1
            try:
                total_size += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass

    return files, dirs, total_size

def print_tree(path, prefix="", show_size=True, show_hidden=False, max_depth=None, current_depth=0):
    if max_depth is not None and current_depth > max_depth:
        return

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        print(prefix + "└── [Permission Denied]")
        return

    if not show_hidden:
        entries = [e for e in entries if not e.startswith('.')]

    dirs = []
    files = []

    for entry in entries:
        full = os.path.join(path, entry)
        if os.path.isdir(full):
            dirs.append(entry)
        else:
            files.append(entry)

    items = dirs + files

    for i, entry in enumerate(items):
        full = os.path.join(path, entry)
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "

        if os.path.isdir(full):
            if show_size:
                try:
                    f_count, d_count, size = count_items(full)
                    label = f"[{f_count}f, {d_count}d, {format_size(size)}]"
                except Exception:
                    label = ""
            else:
                label = ""

            print(f"{prefix}{connector}{entry}/ {label}")
            print_tree(full, prefix + extension, show_size, show_hidden, max_depth, current_depth + 1)
        else:
            if show_size:
                try:
                    size = format_size(os.path.getsize(full))
                    print(f"{prefix}{connector}{entry} ({size})")
                except OSError:
                    print(f"{prefix}{connector}{entry}")
            else:
                print(f"{prefix}{connector}{entry}")

def main():
    path = input("Directory path (blank = current): ").strip() or "."

    if not os.path.isdir(path):
        print("Not a valid directory.")
        return

    show_hidden = input("Show hidden files? y/n: ").strip().lower() == 'y'
    show_size = input("Show sizes? y/n: ").strip().lower() == 'y'

    depth_input = input("Max depth (blank = unlimited): ").strip()
    max_depth = int(depth_input) if depth_input.isdigit() else None

    print(f"\n{os.path.abspath(path)}")

    try:
        files, dirs, total = count_items(path)
        print(f"Total: {files} files, {dirs} folders, {format_size(total)}")
    except Exception:
        pass

    print()
    print_tree(path, show_size=show_size, show_hidden=show_hidden, max_depth=max_depth)

if __name__ == "__main__":
    main()