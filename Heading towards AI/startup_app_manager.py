import os
import sys
import platform
import subprocess
import shutil
import json
from pathlib import Path


OS = platform.system()

BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"


# -------------------- Windows --------------------

def get_windows_startup_folders():
    folders = []

    user = os.environ.get("USERPROFILE", "")
    if user:
        folders.append(Path(user) / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup")

    appdata = os.environ.get("ALLUSERSPROFILE", "")
    if appdata:
        folders.append(Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup")

    return folders


def list_windows_startup():
    entries = []

    for folder in get_windows_startup_folders():
        if not folder.is_dir():
            continue
        for f in folder.iterdir():
            if f.is_file():
                entries.append({
                    "name": f.name,
                    "path": str(f),
                    "type": "folder",
                    "source": str(folder)
                })

    # registry (HKLM + HKCU Run)
    try:
        import winreg
    except ImportError:
        return entries

    reg_paths = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKCU"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKLM"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run", "HKLM32"),
    ]

    for hive, subkey, label in reg_paths:
        try:
            with winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        entries.append({
                            "name": name,
                            "path": value,
                            "type": "registry",
                            "source": f"{label}\\{subkey}"
                        })
                        i += 1
                    except OSError:
                        break
        except FileNotFoundError:
            continue
        except PermissionError:
            continue

    return entries


def remove_windows_registry_entry(hive_label, name):
    try:
        import winreg
    except ImportError:
        return False

    hive_map = {
        "HKCU": winreg.HKEY_CURRENT_USER,
        "HKLM": winreg.HKEY_LOCAL_MACHINE,
        "HKLM32": winreg.HKEY_LOCAL_MACHINE,
    }

    subkey_map = {
        "HKCU": r"Software\Microsoft\Windows\CurrentVersion\Run",
        "HKLM": r"Software\Microsoft\Windows\CurrentVersion\Run",
        "HKLM32": r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
    }

    try:
        with winreg.OpenKey(hive_map[hive_label], subkey_map[hive_label], 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, name)
            return True
    except (FileNotFoundError, PermissionError, OSError):
        return False


# -------------------- Linux --------------------

def get_linux_autostart_dirs():
    dirs = []

    home = os.path.expanduser("~")
    dirs.append(Path(home) / ".config" / "autostart")
    dirs.append(Path("/etc/xdg/autostart"))

    return dirs


def parse_desktop_file(path):
    info = {"Name": "", "Exec": "", "Comment": "", "Hidden": "false", "Type": ""}

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            in_desktop = False
            for line in f:
                line = line.strip()
                if line.startswith("[Desktop Entry]"):
                    in_desktop = True
                    continue
                if line.startswith("[") and in_desktop:
                    break
                if not in_desktop or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip()
                if k in info:
                    info[k] = v
    except OSError:
        pass

    return info


def list_linux_startup():
    entries = []

    for d in get_linux_autostart_dirs():
        if not d.is_dir():
            continue
        for f in d.iterdir():
            if f.suffix == ".desktop" and f.is_file():
                parsed = parse_desktop_file(f)
                entries.append({
                    "name": parsed.get("Name") or f.stem,
                    "path": str(f),
                    "exec": parsed.get("Exec", ""),
                    "comment": parsed.get("Comment", ""),
                    "hidden": parsed.get("Hidden", "false").lower() == "true",
                    "source": str(d)
                })

    return entries


def toggle_linux_entry(path, enable):
    p = Path(path)
    if not p.is_file():
        return False

    try:
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()

        if enable:
            content = content.replace("Hidden=true", "Hidden=false")
        else:
            if "Hidden=true" in content:
                pass
            else:
                content = content.replace("Hidden=false", "Hidden=true")
                if "Hidden=true" not in content:
                    content += "\nHidden=true\n"

        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except OSError:
        return False


def remove_linux_entry(path):
    try:
        os.remove(path)
        return True
    except OSError:
        return False


# -------------------- macOS --------------------

def list_macos_startup():
    entries = []

    # user login items via osascript
    try:
        result = subprocess.run(
            ["osascript", "-e", 'tell application "System Events" to get the name of every login item'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            names = [n.strip() for n in result.stdout.strip().split(",") if n.strip()]
            for name in names:
                entries.append({
                    "name": name,
                    "path": "(login item)",
                    "type": "login_item",
                    "source": "System Events"
                })
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # LaunchAgents
    agents_dirs = [
        Path(os.path.expanduser("~/Library/LaunchAgents")),
        Path("/Library/LaunchAgents"),
        Path("/Library/LaunchDaemons"),
    ]

    for d in agents_dirs:
        if not d.is_dir():
            continue
        for f in d.iterdir():
            if f.suffix == ".plist" and f.is_file():
                entries.append({
                    "name": f.stem,
                    "path": str(f),
                    "type": "launch_agent",
                    "source": str(d)
                })

    return entries


def remove_macos_login_item(name):
    script = f'tell application "System Events" to delete login item "{name}"'
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


# -------------------- Cross-platform --------------------

def get_startup_entries():
    if OS == "Windows":
        return list_windows_startup()
    if OS == "Linux":
        return list_linux_startup()
    if OS == "Darwin":
        return list_macos_startup()
    return []


def display_entries(entries):
    if not entries:
        print(f"{YELLOW}No startup entries found.{RESET}")
        return

    print(f"\n{BOLD}{'IDX':<5}{'NAME':<35}{'SOURCE':<40}{'STATUS':<10}{RESET}")
    print("─" * 95)

    for i, e in enumerate(entries, 1):
        name = (e.get("name") or "")[:34]
        source = (e.get("source") or "")[:39]

        if OS == "Linux":
            status = "DISABLED" if e.get("hidden") else "ENABLED"
        elif OS == "Windows":
            status = e.get("type", "").upper()
        elif OS == "Darwin":
            status = e.get("type", "").upper()
        else:
            status = ""

        color = GREEN if status == "ENABLED" else DIM

        print(f"{i:<5}{name:<35}{source:<40}{color}{status:<10}{RESET}")


def export_entries(entries, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)
        print(f"{GREEN}Exported {len(entries)} entries to {path}{RESET}")
        return True
    except OSError as e:
        print(f"{RED}Export failed: {e}{RESET}")
        return False


def main():
    print(f"=== Startup App Manager ({OS}) ===\n")

    if OS not in ("Windows", "Linux", "Darwin"):
        print(f"{RED}Unsupported OS: {OS}{RESET}")
        return

    if OS != "Windows" and os.geteuid() != 0:
        print(f"{DIM}Note: some system-wide entries require sudo to modify.{RESET}")

    while True:
        entries = get_startup_entries()
        display_entries(entries)

        print(f"\n{BOLD}Options:{RESET}")
        print("  1. Refresh list")
        print("  2. Show details of entry")
        print("  3. Enable entry (Linux only)")
        print("  4. Disable entry (Linux only)")
        print("  5. Delete entry")
        print("  6. Export list to JSON")
        print("  7. Quit")

        choice = input("\nChoose: ").strip()

        if choice == '1':
            continue

        if choice == '2':
            try:
                idx = int(input("Entry index: ").strip()) - 1
                if 0 <= idx < len(entries):
                    e = entries[idx]
                    print(f"\n{BOLD}{CYAN}Entry Details{RESET}")
                    print("─" * 60)
                    for k, v in e.items():
                        print(f"  {k:<12}: {v}")
                else:
                    print("Invalid index.")
            except ValueError:
                print("Invalid input.")

        elif choice == '3':
            if OS != "Linux":
                print(f"{YELLOW}Only supported on Linux.{RESET}")
                continue
            try:
                idx = int(input("Entry index: ").strip()) - 1
                if 0 <= idx < len(entries):
                    e = entries[idx]
                    if e.get("source") == "/etc/xdg/autostart":
                        print(f"{YELLOW}System-wide entry, cannot modify without sudo copy.{RESET}")
                        continue
                    if toggle_linux_entry(e["path"], enable=True):
                        print(f"{GREEN}Enabled: {e['name']}{RESET}")
                    else:
                        print(f"{RED}Failed to enable.{RESET}")
            except ValueError:
                print("Invalid.")

        elif choice == '4':
            if OS != "Linux":
                print(f"{YELLOW}Only supported on Linux.{RESET}")
                continue
            try:
                idx = int(input("Entry index: ").strip()) - 1
                if 0 <= idx < len(entries):
                    e = entries[idx]
                    if toggle_linux_entry(e["path"], enable=False):
                        print(f"{GREEN}Disabled: {e['name']}{RESET}")
                    else:
                        print(f"{RED}Failed to disable.{RESET}")
            except ValueError:
                print("Invalid.")

        elif choice == '5':
            try:
                idx = int(input("Entry index to delete: ").strip()) - 1
            except ValueError:
                print("Invalid input.")
                continue

            if not (0 <= idx < len(entries)):
                print("Invalid index.")
                continue

            e = entries[idx]
            print(f"\n{YELLOW}About to delete:{RESET} {e['name']}")
            print(f"  Path: {e['path']}")
            print(f"  Source: {e['source']}")

            confirm = input("Confirm delete? (y/n): ").strip().lower()
            if confirm != 'y':
                continue

            success = False

            if OS == "Windows":
                if e.get("type") == "folder":
                    try:
                        os.remove(e["path"])
                        success = True
                    except OSError as err:
                        print(f"{RED}Failed: {err}{RESET}")
                elif e.get("type") == "registry":
                    src = e["source"].split("\\")[0]
                    if remove_windows_registry_entry(src, e["name"]):
                        success = True
                    else:
                        print(f"{RED}Failed to remove registry entry (try admin).{RESET}")

            elif OS == "Linux":
                if remove_linux_entry(e["path"]):
                    success = True
                else:
                    print(f"{RED}Failed to delete (try sudo).{RESET}")

            elif OS == "Darwin":
                if e.get("type") == "login_item":
                    if remove_macos_login_item(e["name"]):
                        success = True
                    else:
                        print(f"{RED}Failed to remove login item.{RESET}")
                elif e.get("type") == "launch_agent":
                    try:
                        os.remove(e["path"])
                        success = True
                    except OSError as err:
                        print(f"{RED}Failed: {err}{RESET}")

            if success:
                print(f"{GREEN}Deleted: {e['name']}{RESET}")

        elif choice == '6':
            path = input("Export to file (default startup_backup.json): ").strip() or "startup_backup.json"
            export_entries(entries, path)

        elif choice == '7':
            break

        else:
            print("Invalid choice.")

    print("Done.")


if __name__ == "__main__":
    main()