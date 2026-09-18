import platform
import os
import sys
import socket
import getpass
import subprocess
import shutil
from datetime import datetime, timedelta

try:
    import psutil
except ImportError:
    print("Install: pip install psutil")
    sys.exit(1)


BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
DIM = "\033[2m"
RESET = "\033[0m"


def header(title):
    width = 66
    print(f"\n{BOLD}{CYAN}┌{'─' * width}┐{RESET}")
    pad = width - len(title) - 2
    left = pad // 2
    right = pad - left
    print(f"{BOLD}{CYAN}│{' ' * left} {title} {' ' * right}│{RESET}")
    print(f"{BOLD}{CYAN}└{'─' * width}┘{RESET}")


def row(label, value, label_width=22):
    print(f"  {DIM}{label:<{label_width}}{RESET} {value}")


def format_bytes(n):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} PB"


def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{days}d {hours}h {minutes}m {secs}s"


def get_os_info():
    header("Operating System")
    row("System", platform.system())
    row("Release", platform.release())
    row("Version", platform.version())
    row("Machine", platform.machine())
    row("Processor", platform.processor())
    row("Architecture", platform.architecture()[0])
    row("Node", platform.node())

    if platform.system() == "Linux":
        try:
            with open("/etc/os-release") as f:
                data = dict(line.strip().split("=", 1) for line in f if "=" in line)
            row("Distro", data.get("PRETTY_NAME", "Unknown").strip('"'))
        except (OSError, ValueError):
            pass


def get_cpu_info():
    header("CPU")
    row("Physical cores", psutil.cpu_count(logical=False))
    row("Logical cores", psutil.cpu_count(logical=True))

    freq = psutil.cpu_freq()
    if freq:
        row("Current freq", f"{freq.current:.0f} MHz")
        row("Min freq", f"{freq.min:.0f} MHz")
        row("Max freq", f"{freq.max:.0f} MHz")

    try:
        load = os.getloadavg()
        row("Load avg (1/5/15)", f"{load[0]:.2f}  {load[1]:.2f}  {load[2]:.2f}")
    except (AttributeError, OSError):
        pass

    row("Current usage", f"{psutil.cpu_percent(interval=1)}%")

    # cache info on linux
    if platform.system() == "Linux":
        try:
            cache = psutil.cpu_stats()
            row("Context switches", f"{cache.ctx_switches:,}")
            row("Interrupts", f"{cache.interrupts:,}")
        except Exception:
            pass


def get_memory_info():
    header("Memory")
    mem = psutil.virtual_memory()
    row("Total", format_bytes(mem.total))
    row("Available", format_bytes(mem.available))
    row("Used", f"{format_bytes(mem.used)} ({mem.percent}%)")
    row("Free", format_bytes(mem.free))

    swap = psutil.swap_memory()
    print()
    row("Swap Total", format_bytes(swap.total))
    row("Swap Used", f"{format_bytes(swap.used)} ({swap.percent}%)")
    row("Swap Free", format_bytes(swap.free))


def get_disk_info():
    header("Disk")
    partitions = psutil.disk_partitions(all=False)

    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            print(f"  {BOLD}{p.device}{RESET}  [{p.fstype}]  mounted at {p.mountpoint}")
            row("  Total", format_bytes(usage.total), label_width=14)
            row("  Used", f"{format_bytes(usage.used)} ({usage.percent}%)", label_width=14)
            row("  Free", format_bytes(usage.free), label_width=14)
            print()
        except (PermissionError, OSError):
            continue

    try:
        io = psutil.disk_io_counters()
        if io:
            row("Total read", format_bytes(io.read_bytes))
            row("Total write", format_bytes(io.write_bytes))
    except Exception:
        pass


def get_network_info():
    header("Network")
    hostname = socket.gethostname()
    row("Hostname", hostname)

    try:
        row("FQDN", socket.getfqdn())
    except Exception:
        pass

    try:
        ip = socket.gethostbyname(hostname)
        row("Local IP", ip)
    except socket.gaierror:
        pass

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        row("Primary IP", s.getsockname()[0])
        s.close()
    except Exception:
        pass

    # list interfaces
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    print()
    for name, addr_list in addrs.items():
        stat = stats.get(name)
        status = "UP" if stat and stat.isup else "DOWN"
        speed = f"{stat.speed} Mbps" if stat else ""

        print(f"  {BOLD}{name}{RESET}  [{status}]  {speed}")

        for addr in addr_list:
            if addr.family == socket.AF_INET:
                row("  IPv4", addr.address, label_width=10)
            elif addr.family == socket.AF_INET6:
                row("  IPv6", addr.address.split("%")[0], label_width=10)

    try:
        io = psutil.net_io_counters()
        print()
        row("Total sent", format_bytes(io.bytes_sent))
        row("Total recv", format_bytes(io.bytes_recv))
    except Exception:
        pass


def get_user_info():
    header("User & Boot")
    try:
        row("Current user", getpass.getuser())
    except Exception:
        pass

    try:
        users = psutil.users()
        if users:
            row("Logged in", f"{len(users)} user(s)")
            for u in users:
                started = datetime.fromtimestamp(u.started).strftime("%Y-%m-%d %H:%M")
                row(f"  {u.name}", f"{u.terminal or 'local'} since {started}")
    except Exception:
        pass

    boot_time = datetime.fromtimestamp(psutil.boot_time())
    row("Boot time", boot_time.strftime("%Y-%m-%d %H:%M:%S"))
    row("Uptime", format_uptime((datetime.now() - boot_time).total_seconds()))


def get_python_info():
    header("Python")
    row("Version", sys.version.split()[0])
    row("Executable", sys.executable)
    row("Platform", sys.platform)

    try:
        import psutil as ps
        row("psutil", ps.__version__)
    except Exception:
        pass


def get_top_processes():
    header("Top 10 Processes by CPU")

    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "username"]):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # warm up
    for p in psutil.process_iter(["cpu_percent"]):
        try:
            p.info["cpu_percent"]
        except Exception:
            pass

    import time
    time.sleep(0.3)

    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "username"]):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    procs.sort(key=lambda x: x.get("cpu_percent") or 0, reverse=True)

    print(f"  {BOLD}{'PID':<8}{'NAME':<28}{'CPU%':>8}{'MEM%':>8}{RESET}")
    print(f"  {'─' * 60}")

    for p in procs[:10]:
        name = (p.get("name") or "")[:27]
        cpu = p.get("cpu_percent") or 0
        mem = p.get("memory_percent") or 0
        print(f"  {p['pid']:<8}{name:<28}{cpu:>7.1f}%{mem:>7.1f}%")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="System Info Displayer")
    parser.add_argument("--section", choices=["os", "cpu", "mem", "disk", "net", "user", "python", "top"],
                        help="Show only a specific section")
    parser.add_argument("--no-color", action="store_true", help="Disable colors")
    args = parser.parse_args()

    global BOLD, CYAN, GREEN, YELLOW, DIM, RESET
    if args.no_color:
        BOLD = CYAN = GREEN = YELLOW = DIM = RESET = ""

    print(f"\n{BOLD}System Information Report{RESET}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    sections = {
        "os": get_os_info,
        "cpu": get_cpu_info,
        "mem": get_memory_info,
        "disk": get_disk_info,
        "net": get_network_info,
        "user": get_user_info,
        "python": get_python_info,
        "top": get_top_processes,
    }

    if args.section:
        sections[args.section]()
    else:
        for name, fn in sections.items():
            try:
                fn()
            except Exception as e:
                print(f"\n  {YELLOW}[!] {name} section error: {e}{RESET}")

    print()


if __name__ == "__main__":
    main()