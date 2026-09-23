import os
import sys
import json
import time
import argparse
import smtplib
import socket
import ssl
from email.mime.text import MIMEText
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime
from statistics import mean, median


MONITORS_FILE = "monitors.json"
LOG_FILE = "uptime_log.json"


def fetch_status(url, timeout=15, method="GET"):
    start = time.time()

    req = Request(url, headers={
        "User-Agent": "UptimeMonitor/1.0 (health check)",
        "Accept": "*/*"
    }, method=method)

    try:
        with urlopen(req, timeout=timeout) as response:
            elapsed_ms = (time.time() - start) * 1000
            body = response.read()
            return {
                "ok": True,
                "status": response.status,
                "latency_ms": elapsed_ms,
                "size": len(body),
                "error": None
            }
    except HTTPError as e:
        elapsed_ms = (time.time() - start) * 1000
        return {
            "ok": False,
            "status": e.code,
            "latency_ms": elapsed_ms,
            "size": 0,
            "error": f"HTTP {e.code}"
        }
    except URLError as e:
        elapsed_ms = (time.time() - start) * 1000
        return {
            "ok": False,
            "status": None,
            "latency_ms": elapsed_ms,
            "size": 0,
            "error": str(e.reason)
        }
    except Exception as e:
        elapsed_ms = (time.time() - start) * 1000
        return {
            "ok": False,
            "status": None,
            "latency_ms": elapsed_ms,
            "size": 0,
            "error": str(e)
        }


def check_tcp(host, port=80, timeout=10):
    start = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed_ms = (time.time() - start) * 1000
            return {
                "ok": True,
                "status": "TCP",
                "latency_ms": elapsed_ms,
                "size": 0,
                "error": None
            }
    except (socket.timeout, socket.error, OSError) as e:
        elapsed_ms = (time.time() - start) * 1000
        return {
            "ok": False,
            "status": None,
            "latency_ms": elapsed_ms,
            "size": 0,
            "error": str(e)
        }


def check_ssl_cert(hostname, port=443):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expire_str = cert.get("notAfter", "")
                try:
                    expire_dt = datetime.strptime(expire_str, "%b %d %H:%M:%S %Y %Z")
                    days_left = (expire_dt - datetime.utcnow()).days
                except ValueError:
                    days_left = None
                return {
                    "ok": True,
                    "days_left": days_left,
                    "expires": expire_str
                }
    except Exception as e:
        return {"ok": False, "days_left": None, "expires": "", "error": str(e)}


# ---------- Storage ----------

def load_json(path, default):
    if not os.path.isfile(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"Save failed ({path}): {e}")


# ---------- Notifications ----------

def desktop_notify(title, message):
    try:
        from plyer import notification
        notification.notify(title=title, message=message, timeout=10)
        return True
    except Exception:
        return False


def email_notify(config, subject, body):
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["From"] = config["email_user"]
        msg["To"] = config["email_to"]
        msg["Subject"] = subject

        context = ssl.create_default_context()

        with smtplib.SMTP(config["smtp_host"], config["smtp_port"]) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(config["email_user"], config["email_pass"])
            server.sendmail(config["email_user"], [config["email_to"]], msg.as_string())
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False


def webhook_notify(url, payload):
    try:
        data = json.dumps(payload).encode()
        req = Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        with urlopen(req, timeout=10) as response:
            return response.status < 400
    except Exception as e:
        print(f"Webhook failed: {e}")
        return False


def notify(title, message, config=None):
    print(f"\n[ALERT] {title}")
    print(f"        {message}")

    if not config:
        return

    if config.get("desktop_notify"):
        desktop_notify(title, message)

    if config.get("email_enabled"):
        email_notify(config, title, message)

    if config.get("webhook_url"):
        webhook_notify(config["webhook_url"], {"title": title, "message": message})


# ---------- Monitoring ----------

def check_monitor(monitor, config=None):
    name = monitor["name"]
    url = monitor.get("url")
    monitor_type = monitor.get("type", "http")

    if monitor_type == "tcp":
        host = monitor.get("host")
        port = monitor.get("port", 80)
        print(f"Checking {name} (TCP {host}:{port})...")
        result = check_tcp(host, port)
    else:
        method = monitor.get("method", "GET")
        print(f"Checking {name} ({method} {url})...")
        result = fetch_status(url, method=method)

    result["time"] = datetime.now().isoformat()
    result["monitor"] = name

    if result["ok"]:
        print(f"  OK  status={result['status']}  latency={result['latency_ms']:.0f}ms")
    else:
        print(f"  FAIL  {result.get('error') or 'unknown'}")

    # check for failures threshold
    fails_key = f"{name}_consecutive_fails"
    monitor.setdefault("state", {})

    if result["ok"]:
        prev_fails = monitor["state"].get("consecutive_fails", 0)
        monitor["state"]["consecutive_fails"] = 0

        if prev_fails >= monitor.get("alert_after_fails", 2):
            notify(
                f"{name} is back UP",
                f"{name} ({url or monitor.get('host')}) recovered.\n"
                f"Latency: {result['latency_ms']:.0f}ms",
                config
            )
    else:
        monitor["state"]["consecutive_fails"] = monitor["state"].get("consecutive_fails", 0) + 1
        fails = monitor["state"]["consecutive_fails"]

        if fails == monitor.get("alert_after_fails", 2):
            notify(
                f"{name} is DOWN",
                f"{name} ({url or monitor.get('host')}) failed {fails} times.\n"
                f"Error: {result.get('error') or 'unknown'}",
                config
            )

    # check response time threshold
    if result["ok"] and monitor.get("max_latency_ms"):
        if result["latency_ms"] > monitor["max_latency_ms"]:
            notify(
                f"{name} is slow",
                f"Latency {result['latency_ms']:.0f}ms exceeds threshold "
                f"{monitor['max_latency_ms']}ms",
                config
            )

    # check SSL cert expiry
    if monitor.get("check_ssl") and url and url.startswith("https://"):
        from urllib.parse import urlparse
        host = urlparse(url).hostname
        if host:
            ssl_result = check_ssl_cert(host)
            if ssl_result["ok"] and ssl_result["days_left"] is not None:
                if ssl_result["days_left"] < 30:
                    notify(
                        f"{name} SSL expires soon",
                        f"Certificate expires in {ssl_result['days_left']} days "
                        f"({ssl_result['expires']})",
                        config
                    )

    return result


def log_result(log, monitor_name, result):
    log.setdefault(monitor_name, []).append(result)
    if len(log[monitor_name]) > 500:
        log[monitor_name] = log[monitor_name][-500:]


def get_stats(entries):
    if not entries:
        return None

    total = len(entries)
    ups = sum(1 for e in entries if e["ok"])
    downs = total - ups

    uptime_pct = ups / total * 100

    latencies = [e["latency_ms"] for e in entries if e["ok"]]
    avg_lat = mean(latencies) if latencies else 0
    med_lat = median(latencies) if latencies else 0
    min_lat = min(latencies) if latencies else 0
    max_lat = max(latencies) if latencies else 0

    return {
        "total": total,
        "ups": ups,
        "downs": downs,
        "uptime_pct": uptime_pct,
        "avg_latency": avg_lat,
        "median_latency": med_lat,
        "min_latency": min_lat,
        "max_latency": max_lat
    }


def run_monitor_loop(interval_seconds, config=None, once=False):
    monitors = load_json(MONITORS_FILE, [])
    log = load_json(LOG_FILE, {})

    if not monitors:
        print("No monitors configured. Add some first.")
        return

    print(f"\nMonitoring {len(monitors)} target(s) every {interval_seconds}s")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            print(f"\n{'=' * 60}")
            print(f"Check cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)

            for monitor in monitors:
                try:
                    result = check_monitor(monitor, config)
                    log_result(log, monitor["name"], result)
                except Exception as e:
                    print(f"  Exception: {e}")

            save_json(MONITORS_FILE, monitors)
            save_json(LOG_FILE, log)

            if once:
                break

            print(f"\nSleeping {interval_seconds}s...")
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\n\nStopped.")
        save_json(MONITORS_FILE, monitors)
        save_json(LOG_FILE, log)


# ---------- CLI ----------

def add_monitor_interactive():
    monitors = load_json(MONITORS_FILE, [])

    print("\n--- Add monitor ---")
    print("Types: http, tcp")

    mtype = input("Type (default http): ").strip().lower() or "http"

    if mtype not in ("http", "tcp"):
        print("Invalid type.")
        return

    name = input("Name/label: ").strip()
    if not name:
        return

    if mtype == "tcp":
        host = input("Hostname: ").strip()
        try:
            port = int(input("Port (default 80): ").strip() or "80")
        except ValueError:
            port = 80

        monitor = {
            "name": name,
            "type": "tcp",
            "host": host,
            "port": port,
            "alert_after_fails": 2,
            "state": {}
        }
    else:
        url = input("URL (include http:// or https://): ").strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        method = input("HTTP method (GET/HEAD, default GET): ").strip().upper() or "GET"

        try:
            alert_after = int(input("Alert after N consecutive fails (default 2): ").strip() or "2")
        except ValueError:
            alert_after = 2

        lat_input = input("Max latency ms (blank for none): ").strip()
        max_lat = int(lat_input) if lat_input else None

        monitor = {
            "name": name,
            "type": "http",
            "url": url,
            "method": method,
            "alert_after_fails": alert_after,
            "max_latency_ms": max_lat,
            "check_ssl": url.startswith("https://"),
            "state": {}
        }

    monitors.append(monitor)
    save_json(MONITORS_FILE, monitors)
    print(f"Added monitor: {name}")


def list_monitors():
    monitors = load_json(MONITORS_FILE, [])
    log = load_json(LOG_FILE, {})

    if not monitors:
        print("No monitors.")
        return

    print(f"\n{len(monitors)} monitor(s):\n")
    for i, m in enumerate(monitors, 1):
        print(f"{i}. {m['name']}  [{m.get('type', 'http')}]")

        if m.get("type") == "tcp":
            print(f"   TCP {m.get('host')}:{m.get('port')}")
        else:
            print(f"   {m.get('method', 'GET')} {m.get('url')}")

        if m.get("max_latency_ms"):
            print(f"   Max latency: {m['max_latency_ms']}ms")

        stats = get_stats(log.get(m["name"], []))
        if stats:
            print(f"   Uptime: {stats['uptime_pct']:.1f}%  "
                  f"({stats['ups']}/{stats['total']} checks)")
            print(f"   Avg latency: {stats['avg_latency']:.0f}ms  "
                  f"(min {stats['min_latency']:.0f} / max {stats['max_latency']:.0f})")

        print()


def remove_monitor():
    monitors = load_json(MONITORS_FILE, [])
    if not monitors:
        print("No monitors.")
        return

    list_monitors()

    try:
        idx = int(input("Remove which number? ").strip()) - 1
    except ValueError:
        return

    if 0 <= idx < len(monitors):
        removed = monitors.pop(idx)
        save_json(MONITORS_FILE, monitors)
        print(f"Removed: {removed['name']}")


def show_stats():
    monitors = load_json(MONITORS_FILE, [])
    log = load_json(LOG_FILE, {})

    if not monitors:
        print("No monitors.")
        return

    for m in monitors:
        name = m["name"]
        entries = log.get(name, [])

        print(f"\n{name}")
        print("-" * 60)

        if not entries:
            print("  No data yet.")
            continue

        stats = get_stats(entries)

        print(f"  Total checks:  {stats['total']}")
        print(f"  Successful:    {stats['ups']}")
        print(f"  Failed:        {stats['downs']}")
        print(f"  Uptime:        {stats['uptime_pct']:.2f}%")
        print(f"  Avg latency:   {stats['avg_latency']:.0f}ms")
        print(f"  Median:        {stats['median_latency']:.0f}ms")
        print(f"  Min / Max:     {stats['min_latency']:.0f}ms / {stats['max_latency']:.0f}ms")

        last = entries[-1]
        print(f"  Last check:    {last['time'][:19]}  "
              f"{'OK' if last['ok'] else 'FAIL'}  "
              f"{last['latency_ms']:.0f}ms")


def build_notify_config():
    config = {}
    config["desktop_notify"] = input("Desktop notifications? (y/n): ").strip().lower() == "y"

    config["email_enabled"] = input("Email alerts? (y/n): ").strip().lower() == "y"
    if config["email_enabled"]:
        config["smtp_host"] = input("SMTP host: ").strip()
        config["smtp_port"] = int(input("SMTP port (587): ").strip() or "587")
        config["email_user"] = input("Email user: ").strip()
        config["email_pass"] = input("Email password: ").strip()
        config["email_to"] = input("Send alerts to: ").strip()

    wh = input("Webhook URL (Slack/Discord, blank for none): ").strip()
    if wh:
        config["webhook_url"] = wh

    return config


def main():
    parser = argparse.ArgumentParser(description="Website Uptime Monitor")
    parser.add_argument("--add", action="store_true", help="Add monitor")
    parser.add_argument("--list", action="store_true", help="List monitors")
    parser.add_argument("--remove", action="store_true", help="Remove monitor")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    parser.add_argument("--run", action="store_true", help="Run monitoring loop")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--interval", type=int, default=60, help="Interval in seconds")
    parser.add_argument("--notify", action="store_true", help="Configure notifications")

    args = parser.parse_args()

    if args.add:
        add_monitor_interactive()
        return
    if args.list:
        list_monitors()
        return
    if args.remove:
        remove_monitor()
        return
    if args.stats:
        show_stats()
        return

    if args.run or args.once:
        config = build_notify_config() if args.notify else None
        run_monitor_loop(args.interval, config=config, once=args.once)
        return

    print("=== Website Uptime Monitor ===\n")

    while True:
        print("\nOptions:")
        print("  1. Add monitor")
        print("  2. List monitors")
        print("  3. Remove monitor")
        print("  4. Show stats")
        print("  5. Run one check now")
        print("  6. Start monitoring loop")
        print("  7. Quit")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            add_monitor_interactive()
        elif choice == "2":
            list_monitors()
        elif choice == "3":
            remove_monitor()
        elif choice == "4":
            show_stats()
        elif choice == "5":
            config = None
            if input("Configure notifications? (y/n): ").strip().lower() == "y":
                config = build_notify_config()
            run_monitor_loop(1, config=config, once=True)
        elif choice == "6":
            try:
                interval = int(input("Check interval seconds (default 60): ").strip() or "60")
            except ValueError:
                interval = 60
            config = None
            if input("Configure notifications? (y/n): ").strip().lower() == "y":
                config = build_notify_config()
            run_monitor_loop(interval, config=config)
        elif choice == "7":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()