import os
import sys
import time
import platform
import threading
from datetime import datetime

try:
    import psutil
except ImportError:
    print("Install: pip install psutil")
    sys.exit(1)


OS = platform.system()

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BLUE = "\033[94m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def clear():
    os.system("cls" if OS == "Windows" else "clear")


def color_for(percent):
    if percent < 60:
        return GREEN
    if percent < 85:
        return YELLOW
    return RED


def bar(percent, width=30):
    filled = int(width * percent / 100)
    return "█" * filled + "░" * (width - filled)


def format_bytes(n):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{days}d {hours}h {minutes}m"


def get_cpu_temp():
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        for name, entries in temps.items():
            for entry in entries:
                if entry.current:
                    return entry.current
    except (AttributeError, OSError):
        return None
    return None


def get_gpu_info():
    try:
        import subprocess
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            gpus = []
            for line in result.stdout.strip().splitlines():
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 5:
                    gpus.append({
                        "name": parts[0],
                        "util": float(parts[1]),
                        "mem_used": float(parts[2]),
                        "mem_total": float(parts[3]),
                        "temp": parts[4]
                    })
            return gpus
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        pass
    return None


def get_network_rates(prev, interval):
    curr = psutil.net_io_counters()
    sent_rate = (curr.bytes_sent - prev.bytes_sent) / interval
    recv_rate = (curr.bytes_recv - prev.bytes_recv) / interval
    return curr, sent_rate, recv_rate


def get_disk_io_rates(prev, interval):
    curr = psutil.disk_io_counters()
    if curr is None:
        return None, 0, 0
    read_rate = (curr.read_bytes - prev.read_bytes) / interval
    write_rate = (curr.write_bytes - prev.write_bytes) / interval
    return curr, read_rate, write_rate


def draw_dashboard(cpu_history, mem_history, net_history):
    clear()

    cpu_percent = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage("/")

    cpu_history.append(cpu_percent)
    mem_history.append(mem.percent)

    if len(cpu_history) > 60:
        cpu_history.pop(0)
    if len(mem_history) > 60:
        mem_history.pop(0)

    print(f"{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║           SERVER RESOURCE MONITOR                            ║{RESET}")
    print(f"{BOLD}{CYAN}╚══════════════════════════════════════════════════════════════╝{RESET}")

    hostname = platform.node()
    system = f"{platform.system()} {platform.release()}"
    uptime = format_uptime(time.time() - psutil.boot_time())
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{DIM}Host:{RESET} {hostname}  {DIM}OS:{RESET} {system}")
    print(f"{DIM}Uptime:{RESET} {uptime}  {DIM}Time:{RESET} {now}")

    print(f"\n{BOLD}── CPU ──{RESET}")
    cpu_color = color_for(cpu_percent)
    cores = psutil.cpu_count(logical=True)
    phys = psutil.cpu_count(logical=False)
    freq = psutil.cpu_freq()
    freq_str = f"{freq.current:.0f} MHz" if freq else "N/A"

    print(f"  Usage:  {cpu_color}{bar(cpu_percent)}{RESET} {cpu_percent:5.1f}%")
    print(f"  Cores:  {phys} physical / {cores} logical   Freq: {freq_str}")

    per_core = psutil.cpu_percent(percpu=True)
    if cores <= 16:
        for i, p in enumerate(per_core):
            c = color_for(p)
            print(f"    Core {i:2}: {c}{bar(p, 20)}{RESET} {p:5.1f}%")

    temp = get_cpu_temp()
    if temp:
        tc = color_for(temp if temp < 100 else 100)
        print(f"  Temp:   {tc}{temp:.1f}°C{RESET}")

    load = None
    try:
        load = os.getloadavg()
    except (AttributeError, OSError):
        pass
    if load:
        print(f"  Load:   {load[0]:.2f} {load[1]:.2f} {load[2]:.2f}")

    print(f"\n{BOLD}── Memory ──{RESET}")
    mem_color = color_for(mem.percent)
    print(f"  RAM:    {mem_color}{bar(mem.percent)}{RESET} {mem.percent:5.1f}%")
    print(f"          {format_bytes(mem.used)} / {format_bytes(mem.total)}  (free: {format_bytes(mem.available)})")

    swap_color = color_for(swap.percent)
    print(f"  Swap:   {swap_color}{bar(swap.percent)}{RESET} {swap.percent:5.1f}%")
    print(f"          {format_bytes(swap.used)} / {format_bytes(swap.total)}")

    print(f"\n{BOLD}── Disk ──{RESET}")
    disk_color = color_for(disk.percent)
    print(f"  Root:   {disk_color}{bar(disk.percent)}{RESET} {disk.percent:5.1f}%")
    print(f"          {format_bytes(disk.used)} / {format_bytes(disk.total)}  (free: {format_bytes(disk.free)})")

    print(f"\n{BOLD}── Top Processes ──{RESET}")
    print(f"  {'PID':<8}{'NAME':<25}{'CPU%':>8}{'MEM%':>8}")

    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    procs.sort(key=lambda x: (x.get("cpu_percent") or 0), reverse=True)

    for p in procs[:8]:
        name = (p.get("name") or "")[:24]
        cpu = p.get("cpu_percent") or 0
        mem_p = p.get("memory_percent") or 0
        cc = color_for(cpu)
        print(f"  {p['pid']:<8}{name:<25}{cc}{cpu:>7.1f}%{RESET}{mem_p:>7.1f}%")

    if net_history:
        print(f"\n{BOLD}── Network ──{RESET}")
        last = net_history[-1] if net_history else None
        if last:
            print(f"  ↓ {last[0]}  ↑ {last[1]}")


def main():
    print("Starting server monitor...")
    time.sleep(0.5)

    interval = 1.0
    try:
        val = input("Refresh interval seconds (default 1): ").strip()
        if val:
            interval = max(0.5, float(val))
    except ValueError:
        pass

    prev_net = psutil.net_io_counters()
    prev_disk = psutil.disk_io_counters()

    cpu_history = []
    mem_history = []
    net_history = []

    # warm up cpu_percent
    psutil.cpu_percent(interval=None)
    for p in psutil.process_iter(["cpu_percent"]):
        try:
            p.info["cpu_percent"]
        except Exception:
            pass

    print("\nPress Ctrl+C to stop.\n")

    try:
        while True:
            start = time.time()

            curr_net, sent_rate, recv_rate = get_network_rates(prev_net, interval)
            prev_net = curr_net

            if prev_disk:
                curr_disk, read_rate, write_rate = get_disk_io_rates(prev_disk, interval)
                prev_disk = curr_disk

            net_history.append((
                f"{format_bytes(recv_rate)}/s",
                f"{format_bytes(sent_rate)}/s"
            ))
            if len(net_history) > 5:
                net_history.pop(0)

            draw_dashboard(cpu_history, mem_history, net_history)

            elapsed = time.time() - start
            sleep_time = max(0.1, interval - elapsed)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n\nStopped.")


if __name__ == "__main__":
    main()