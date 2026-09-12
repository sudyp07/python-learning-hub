import os
import hashlib
from collections import defaultdict

def get_file_hash(path, chunk_size=8192):
    hasher = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, OSError):
        return None

def find_duplicates(folder):
    size_map = defaultdict(list)

    for root, dirs, files in os.walk(folder):
        for name in files:
            full_path = os.path.join(root, name)
            try:
                size = os.path.getsize(full_path)
            except OSError:
                continue
            size_map[size].append(full_path)

    duplicates = defaultdict(list)

    for size, paths in size_map.items():
        if len(paths) < 2:
            continue
        hash_map = defaultdict(list)
        for p in paths:
            h = get_file_hash(p)
            if h:
                hash_map[h].append(p)
        for h, group in hash_map.items():
            if len(group) > 1:
                duplicates[h] = group

    return duplicates

def main():
    folder = input("Enter folder path: ").strip()
    if not os.path.isdir(folder):
        print("Invalid folder.")
        return

    dups = find_duplicates(folder)

    if not dups:
        print("No duplicates found.")
        return

    total_wasted = 0
    count = 0

    for i, (h, files) in enumerate(dups.items(), 1):
        size = os.path.getsize(files[0])
        wasted = size * (len(files) - 1)
        total_wasted += wasted
        count += len(files) - 1

        print(f"\nGroup {i} ({len(files)} files, {size} bytes each):")
        for f in files:
            print(f"  {f}")

    print(f"\nTotal duplicate files: {count}")
    print(f"Space wasted: {total_wasted / (1024*1024):.2f} MB")

    choice = input("\nDelete duplicates (keep first)? y/n: ").strip().lower()
    if choice == 'y':
        removed = 0
        for files in dups.values():
            for f in files[1:]:
                try:
                    os.remove(f)
                    removed += 1
                except OSError as e:
                    print(f"Could not delete {f}: {e}")
        print(f"Deleted {removed} files.")

if __name__ == "__main__":
    main()