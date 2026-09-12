import os
import shutil

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".rb", ".go", ".rs", ".php", ".ts"],
    "Executables": [".exe", ".msi", ".apk", ".deb", ".dmg"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
}

def get_category(ext):
    ext = ext.lower()
    for cat, extensions in CATEGORIES.items():
        if ext in extensions:
            return cat
    return "Others"

def organize(folder, dry_run=False):
    moved = 0
    skipped = 0

    for item in os.listdir(folder):
        src = os.path.join(folder, item)

        if not os.path.isfile(src):
            continue

        _, ext = os.path.splitext(item)

        if not ext:
            skipped += 1
            continue

        category = get_category(ext)
        dest_dir = os.path.join(folder, category)

        if dry_run:
            print(f"  {item}  ->  {category}/")
            moved += 1
            continue

        os.makedirs(dest_dir, exist_ok=True)

        dest = os.path.join(dest_dir, item)

        if os.path.exists(dest):
            base, e = os.path.splitext(item)
            counter = 1
            while os.path.exists(dest):
                dest = os.path.join(dest_dir, f"{base}_{counter}{e}")
                counter += 1

        try:
            shutil.move(src, dest)
            moved += 1
        except (shutil.Error, OSError) as err:
            print(f"Failed to move {item}: {err}")

    return moved, skipped

def main():
    folder = input("Folder to organize: ").strip()

    if not os.path.isdir(folder):
        print("Invalid folder.")
        return

    dry = input("Preview only? (y/n): ").strip().lower() == 'y'

    if dry:
        print("\n--- Preview ---")
        moved, skipped = organize(folder, dry_run=True)
        print(f"\nWould move {moved} files ({skipped} skipped - no extension)")
        confirm = input("Proceed with actual move? y/n: ").strip().lower()
        if confirm != 'y':
            return
        dry = False

    moved, skipped = organize(folder, dry_run=dry)
    print(f"\nDone. Moved: {moved}, Skipped: {skipped}")

if __name__ == "__main__":
    main()