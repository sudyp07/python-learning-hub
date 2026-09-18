import os
import sys
import time
import signal
import platform

try:
    import psutil
except ImportError:
    print("Install: pip install psutil")
    sys.exit(1)


OS = platform.system()

BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"


def clear():
    os.system("cls" if OS == "Windows" else "clear")


def list_processes(sort_by="cpu", filter_str=None, limit=30):
    procs = []
    for p in psutil.process_iter(["pid", "name", "username", "cpu_percent", "memory_percent",
                                   "status", "create_time", "cmdline"]):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if filter_str:
        fs = filter_str.lower()
        procs = [p for p in procs if fs in (p.get("name") or "").lower()]

    if sort_by == "cpu":
        procs.sort(key=lambda x: x.get("cpu_percent") or 0, reverse=True)
    elif sort_by == "mem":
        procs.sort(key=lambda x: x.get("memory_percent") or 0, reverse=True)
    elif sort_by == "pid":
        procs.sort(key=lambda x: x.get("pid") or 0)
    elif sort_by == "name":
        procs.sort(key=lambda x: (x.get("name") or "").lower())

    return procs[:limit]


def display_processes(procs):
    print(f"\n{BOLD}{'IDX':<5}{'PID':<8}{'NAME':<30}{'USER':<18}{'CPU%':>7}{'MEM%':>7}{'STATUS':>10}{RESET}")
    print("─" * 90)

    for i, p in enumerate(procs, 1):
        name = (p.get("name") or "")[:29]
        user = (p.get("username") or "")[:17]
        cpu = p.get("cpu_percent") or 0
        mem = p.get("memory_percent") or 0
        status = p.get("status") or ""

        cpu_color = RED if cpu > 50 else (YELLOW if cpu > 10 else "")
        end = RESET if cpu_color else ""

        print(f"{i:<5}{p['pid']:<8}{name:<30}{user:<18}{cpu_color}{cpu:>6.1f}{end}{mem:>7.1f}{status:>10}")


def warmup_cpu():
    for p in psutil.process_iter(["cpu_percent"]):
        try:
            p.info["cpu_percent"]
        except Exception:
            pass


def get_process_details(pid):
    try:
        p = psutil.Process(pid)
        with p.oneshot():
            info = {
                "pid": p.pid,
                "name": p.name(),
                "exe": p.exe() if p.exe else "",
                "cwd": p.cwd() if p.cwd else "",
                "cmdline": " ".join(p.cmdline()) if p.cmdline() else "",
                "status": p.status(),
                "username": p.username(),
                "cpu_percent": p.cpu_percent(interval=0.1),
                "memory_percent": p.memory_percent(),
                "memory_info": p.memory_info(),
                "create_time": p.create_time(),
                "num_threads": p.num_threads(),
                "nice": p.nice() if hasattr(p, "nice") else "",
                "parent": p.ppid(),
                "children": [c.pid for c in p.children()],
            }
        return info
    except psutil.NoSuchProcess:
        return None
    except psutil.AccessDenied:
        return None


def show_details(pid):
    info = get_process_details(pid)
    if not info:
        print(f"{RED}Process {pid} not found or access denied.{RESET}")
        return

    print(f"\n{BOLD}{CYAN}Process Details (PID {pid}){RESET}")
    print("─" * 60)
    print(f"  Name:         {info['name']}")
    print(f"  PID:          {info['pid']}")
    print(f"  Parent PID:   {info['parent']}")
    print(f"  Status:       {info['status']}")
    print(f"  User:         {info['username']}")
    print(f"  CPU %:        {info['cpu_percent']:.2f}")
    print(f"  Memory %:     {info['memory_percent']:.2f}")
    print(f"  Memory (RSS): {info['memory_info'].rss / (1024*1024):.1f} MB")
    print(f"  Threads:      {info['num_threads']}")

    started = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info["create_time"]))
    print(f"  Started:      {started}")

    if info["exe"]:
        print(f"  Executable:   {info['exe']}")
    if info["cwd"]:
        print(f"  CWD:          {info['cwd']}")
    if info["cmdline"]:
        print(f"  Cmd line:     {info['cmdline'][:200]}")
    if info["children"]:
        print(f"  Children:     {info['children']}")


def kill_process(pid, force=False, tree=False):
    try:
        p = psutil.Process(pid)
        name = p.name()

        if tree:
            children = p.children(recursive=True)
            for c in children:
                try:
                    c.terminate() if not force else c.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        if force:
            p.kill()
        else:
            p.terminate()

        try:
            p.wait(timeout=3)
            print(f"{GREEN}Killed PID {pid} ({name}){RESET}")
            return True
        except psutil.TimeoutExpired:
            print(f"{YELLOW}PID {pid} did not exit. Force kill? (y/n){RESET}")
            if input().strip().lower() == 'y':
                p.kill()
                print(f"{GREEN}Force killed PID {pid}{RESET}")
                return True

    except psutil.NoSuchProcess:
        print(f"{RED}PID {pid} not found.{RESET}")
    except psutil.AccessDenied:
        print(f"{RED}Access denied for PID {pid}. Try running as admin/sudo.{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    return False


def kill_by_name(name, force=False, confirm=True):
    matches = []
    for p in psutil.process_iter(["pid", "name"]):
        try:
            if p.info["name"] and p.info["name"].lower() == name.lower():
                matches.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not matches:
        print(f"{YELLOW}No process named '{name}'.{RESET}")
        return 0

    print(f"\nFound {len(matches)} process(es) named '{name}':")
    for m in matches:
        print(f"  PID {m['pid']}")

    if confirm:
        confirm_input = input(f"Kill all? (y/n): ").strip().lower()
        if confirm_input != 'y':
            print("Cancelled.")
            return 0

    killed = 0
    for m in matches:
        if kill_process(m["pid"], force=force):
            killed += 1

    return killed


def main():
    print("=== Process Killer Utility ===\n")

    if OS == "Windows":
        print(f"{DIM}Note: admin rights needed for system processes.{RESET}")
    else:
        print(f"{DIM}Note: sudo may be needed for processes owned by others.{RESET}")

    warmup_cpu()
    time.sleep(0.3)

    while True:
        print(f"\n{BOLD}Options:{RESET}")
        print("  1. List processes")
        print("  2. Kill by PID")
        print("  3. Kill by name")
        print("  4. Show process details")
        print("  5. Kill top CPU hog")
        print("  6. Search processes")
        print("  7. Quit")

        choice = input("\nChoose: ").strip()

        if choice == '1':
            clear()
            print("Sort by: cpu / mem / pid / name")
            sort_by = input("Sort (default cpu): ").strip().lower() or "cpu"
            if sort_by not in ("cpu", "mem", "pid", "name"):
                sort_by = "cpu"

            warmup_cpu()
            time.sleep(0.2)
            procs = list_processes(sort_by=sort_by)
            display_processes(procs)

        elif choice == '2':
            warmup_cpu()
            time.sleep(0.2)
            procs = list_processes()
            display_processes(procs)

            try:
                pid = int(input("\nEnter PID to kill: ").strip())
            except ValueError:
                print("Invalid PID.")
                continue

            force = input("Force kill? (y/n): ").strip().lower() == 'y'
            tree = input("Kill children too? (y/n): ").strip().lower() == 'y'

            info = get_process_details(pid)
            if info:
                print(f"\nAbout to kill: {info['name']} (PID {pid})")
                confirm = input("Confirm? (y/n): ").strip().lower()
                if confirm == 'y':
                    kill_process(pid, force=force, tree=tree)

        elif choice == '3':
            name = input("Process name to kill: ").strip()
            if not name:
                continue
            force = input("Force kill? (y/n): ").strip().lower() == 'y'
            kill_by_name(name, force=force)

        elif choice == '4':
            try:
                pid = int(input("PID: ").strip())
            except ValueError:
                print("Invalid PID.")
                continue
            show_details(pid)

        elif choice == '5':
            warmup_cpu()
            time.sleep(0.3)
            procs = list_processes(sort_by="cpu", limit=3)
            if not procs:
                print("No processes found.")
                continue

            top = procs[0]
            print(f"\nTop CPU: {top['name']} (PID {top['pid']}) at {top.get('cpu_percent', 0):.1f}%")
            confirm = input("Kill it? (y/n): ").strip().lower()
            if confirm == 'y':
                kill_process(top["pid"])

        elif choice == '6':
            filter_str = input("Search name contains: ").strip()
            if not filter_str:
                continue
            warmup_cpu()
            time.sleep(0.2)
            procs = list_processes(filter_str=filter_str, limit=50)
            if not procs:
                print("No matches.")
            else:
                display_processes(procs)

        elif choice == '7':
            break

        else:
            print("Invalid choice.")

    print("Done.")


if __name__ == "__main__":
    main()