import os
import re

def preview_rename(files, pattern, replacement, start_num=None, prefix=None, suffix=None):
    plan = []
    counter = start_num if start_num is not None else 1

    for old_name in files:
        name, ext = os.path.splitext(old_name)

        if pattern:
            new_base = re.sub(pattern, replacement, name)
        else:
            new_base = name

        if start_num is not None:
            new_base = f"{new_base}_{counter}"
            counter += 1

        if prefix:
            new_base = prefix + new_base
        if suffix:
            new_base = new_base + suffix

        plan.append((old_name, new_base + ext))

    return plan

def main():
    folder = input("Folder path: ").strip()
    if not os.path.isdir(folder):
        print("Invalid folder.")
        return

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    if not files:
        print("No files in folder.")
        return

    print(f"\n{len(files)} files found.")
    for f in files[:10]:
        print(f"  {f}")
    if len(files) > 10:
        print(f"  ... and {len(files)-10} more")

    print("\n--- Rename options ---")
    print("1. Find and replace text")
    print("2. Add prefix")
    print("3. Add suffix")
    print("4. Number files sequentially")
    print("5. Replace with regex")

    choice = input("\nChoose option: ").strip()

    pattern = replacement = prefix = suffix = None
    start_num = None

    if choice == '1':
        pattern = input("Find text: ")
        replacement = input("Replace with: ")
    elif choice == '2':
        prefix = input("Prefix: ")
    elif choice == '3':
        suffix = input("Suffix: ")
    elif choice == '4':
        base = input("Base name: ")
        pattern = ".*"
        replacement = base
        try:
            start_num = int(input("Start number: "))
        except ValueError:
            print("Invalid number.")
            return
    elif choice == '5':
        pattern = input("Regex pattern: ")
        replacement = input("Replacement: ")
    else:
        print("Invalid choice.")
        return

    plan = preview_rename(files, pattern, replacement, start_num, prefix, suffix)

    print("\n--- Preview ---")
    for old, new in plan:
        print(f"  {old}  ->  {new}")

    confirm = input("\nApply changes? y/n: ").strip().lower()
    if confirm == 'y':
        for old, new in plan:
            old_path = os.path.join(folder, old)
            new_path = os.path.join(folder, new)
            if os.path.exists(new_path):
                print(f"Skipped (exists): {new}")
                continue
            try:
                os.rename(old_path, new_path)
            except OSError as e:
                print(f"Failed {old}: {e}")
        print("Done.")

if __name__ == "__main__":
    main()