import os
import sys
import json
import time
import re
import argparse
import smtplib
from email.mime.text import MIMEText
from urllib.request import Request, urlopen
from datetime import datetime

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    print("Install: pip install beautifulsoup4")
    sys.exit(1)


WATCHLIST_FILE = "price_watchlist.json"
HISTORY_FILE = "price_history.json"


def fetch_html(url, timeout=20):
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    with urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="ignore")


def clean_price(text):
    if not text:
        return None

    text = text.replace(",", "").replace(" ", "")

    match = re.search(r"[\d]+(?:\.\d+)?", text)
    if not match:
        return None

    try:
        return float(match.group(0))
    except ValueError:
        return None


# ---------- Site-specific parsers ----------

def parse_amazon(html):
    soup = BeautifulSoup(html, "html.parser")

    selectors = [
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        ".a-price .a-offscreen",
        "#corePrice_feature_div .a-offscreen",
        "#price_inside_buybox",
        "span.a-price-whole",
    ]

    for sel in selectors:
        el = soup.select_one(sel)
        if el:
            price = clean_price(el.get_text())
            if price:
                return price

    # fallback: search for currency pattern
    text = soup.get_text()
    matches = re.findall(r"\$\s*([\d,]+\.\d{2})", text)
    if matches:
        prices = [clean_price(m) for m in matches[:10]]
        prices = [p for p in prices if p and p > 0]
        if prices:
            return min(prices)

    return None


def parse_ebay(html):
    soup = BeautifulSoup(html, "html.parser")

    for sel in ["#prcIsum", "#mm-saleDscPrc", ".x-price-primary", "#prcIsum_bidPrice"]:
        el = soup.select_one(sel)
        if el:
            price = clean_price(el.get_text())
            if price:
                return price

    text = soup.get_text()
    match = re.search(r"US\s*\$([\d,]+\.\d{2})", text)
    if match:
        return clean_price(match.group(1))

    return None


def parse_generic(html):
    soup = BeautifulSoup(html, "html.parser")

    # try schema.org
    for el in soup.find_all(attrs={"itemprop": "price"}):
        content = el.get("content") or el.get_text()
        price = clean_price(content)
        if price:
            return price

    # try common class/id names
    candidates = []

    for attr in ["class", "id"]:
        for el in soup.find_all(attrs={attr: re.compile(r"price", re.IGNORECASE)}):
            text = el.get_text(strip=True)
            p = clean_price(text)
            if p and p > 0:
                candidates.append(p)

    if candidates:
        return min(candidates)

    # meta tags
    for meta in soup.find_all("meta"):
        prop = (meta.get("property") or "") + " " + (meta.get("name") or "")
        if "price" in prop.lower() or "amount" in prop.lower():
            content = meta.get("content")
            p = clean_price(content)
            if p:
                return p

    return None


def detect_parser(url):
    host = url.lower()
    if "amazon." in host:
        return parse_amazon
    if "ebay." in host:
        return parse_ebay
    return parse_generic


def get_price(url):
    try:
        html = fetch_html(url)
    except Exception as e:
        return None, f"fetch failed: {e}"

    parser = detect_parser(url)

    try:
        price = parser(html)
    except Exception as e:
        return None, f"parse failed: {e}"

    if price is None:
        return None, "price not found"

    return price, None


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


# ---------- Notification ----------

def send_email_notification(smtp_host, smtp_port, user, password, to_addr, subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = user
    msg["To"] = to_addr
    msg["Subject"] = subject

    import ssl
    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, [to_addr], msg.as_string())


def try_desktop_notify(title, message):
    try:
        from plyer import notification
        notification.notify(title=title, message=message, timeout=10)
        return True
    except Exception:
        return False


def notify(title, message, config=None):
    print(f"\n[ALERT] {title}")
    print(f"        {message}")

    if config:
        if config.get("desktop_notify"):
            try_desktop_notify(title, message)

        if config.get("email_enabled"):
            try:
                send_email_notification(
                    config["smtp_host"], config["smtp_port"],
                    config["email_user"], config["email_pass"],
                    config["email_to"],
                    f"Price Alert: {title}",
                    message
                )
                print("        (email sent)")
            except Exception as e:
                print(f"        (email failed: {e})")


# ---------- Core logic ----------

def check_item(item, history, config=None):
    url = item["url"]
    name = item.get("name", url)
    target = item.get("target_price")
    drop_pct = item.get("drop_percent")

    print(f"\nChecking: {name}")
    print(f"  URL: {url}")

    price, err = get_price(url)

    if price is None:
        print(f"  ERROR: {err}")
        return None

    print(f"  Current price: ${price:.2f}")

    entry = {
        "time": datetime.now().isoformat(),
        "price": price
    }

    history.setdefault(url, []).append(entry)

    if len(history[url]) > 100:
        history[url] = history[url][-100:]

    prices = [h["price"] for h in history[url]]

    if target and price <= target:
        notify(
            f"{name} hit target price",
            f"Current: ${price:.2f}  |  Target: ${target:.2f}\n{url}",
            config
        )

    if drop_pct and len(prices) >= 2:
        prev = prices[-2]
        if prev > 0:
            change = (price - prev) / prev * 100
            if change <= -abs(drop_pct):
                notify(
                    f"{name} dropped {abs(change):.1f}%",
                    f"Was: ${prev:.2f}  |  Now: ${price:.2f}\n{url}",
                    config
                )

    # notify on all-time low
    if len(prices) >= 2 and price < min(prices[:-1]):
        notify(
            f"{name} new lowest price",
            f"New low: ${price:.2f}\n{url}",
            config
        )

    return price


def watch_loop(interval_minutes, config=None, once=False):
    watchlist = load_json(WATCHLIST_FILE, [])
    history = load_json(HISTORY_FILE, {})

    if not watchlist:
        print("No items in watchlist. Add some first.")
        return

    print(f"\nWatching {len(watchlist)} item(s), checking every {interval_minutes} min")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            for item in watchlist:
                try:
                    check_item(item, history, config)
                except Exception as e:
                    print(f"  Failed to check: {e}")

            save_json(HISTORY_FILE, history)
            print(f"\nSaved history. Next check in {interval_minutes} minutes.")

            if once:
                break

            time.sleep(interval_minutes * 60)

    except KeyboardInterrupt:
        print("\n\nStopped by user.")
        save_json(HISTORY_FILE, history)


# ---------- CLI ----------

def add_item_interactive():
    watchlist = load_json(WATCHLIST_FILE, [])

    print("\n--- Add item ---")
    name = input("Name (label): ").strip()
    if not name:
        return

    url = input("URL: ").strip()
    if not url:
        return

    target_input = input("Target price (blank for none): ").strip()
    target = float(target_input) if target_input else None

    drop_input = input("Alert on % drop (blank for none): ").strip()
    drop = float(drop_input) if drop_input else None

    watchlist.append({
        "name": name,
        "url": url,
        "target_price": target,
        "drop_percent": drop,
        "added": datetime.now().isoformat()
    })

    save_json(WATCHLIST_FILE, watchlist)
    print(f"Added '{name}' to watchlist.")


def list_items():
    watchlist = load_json(WATCHLIST_FILE, [])
    history = load_json(HISTORY_FILE, {})

    if not watchlist:
        print("Watchlist empty.")
        return

    print(f"\n{len(watchlist)} item(s):\n")
    for i, item in enumerate(watchlist, 1):
        print(f"{i}. {item['name']}")
        print(f"   URL: {item['url']}")
        if item.get("target_price"):
            print(f"   Target: ${item['target_price']:.2f}")
        if item.get("drop_percent"):
            print(f"   Alert on drop: {item['drop_percent']}%")

        hist = history.get(item["url"], [])
        if hist:
            prices = [h["price"] for h in hist]
            print(f"   Last: ${prices[-1]:.2f}   Min: ${min(prices):.2f}   Max: ${max(prices):.2f}   Records: {len(prices)}")
        print()


def remove_item():
    watchlist = load_json(WATCHLIST_FILE, [])
    if not watchlist:
        print("Watchlist empty.")
        return

    list_items()

    try:
        idx = int(input("Remove which number? ").strip()) - 1
    except ValueError:
        return

    if 0 <= idx < len(watchlist):
        removed = watchlist.pop(idx)
        save_json(WATCHLIST_FILE, watchlist)
        print(f"Removed: {removed['name']}")


def show_history():
    history = load_json(HISTORY_FILE, {})
    watchlist = load_json(WATCHLIST_FILE, [])

    if not history:
        print("No history yet.")
        return

    name_by_url = {i["url"]: i["name"] for i in watchlist}

    for url, entries in history.items():
        name = name_by_url.get(url, url)
        print(f"\n{name}")
        print(f"  {url}")
        print(f"  Records: {len(entries)}")

        prices = [e["price"] for e in entries]
        print(f"  Min: ${min(prices):.2f}  Max: ${max(prices):.2f}  Last: ${prices[-1]:.2f}")

        print("  Recent:")
        for e in entries[-5:]:
            print(f"    {e['time'][:19]}  ${e['price']:.2f}")


def build_notify_config():
    config = {}

    config["desktop_notify"] = input("Enable desktop notifications? (y/n): ").strip().lower() == "y"
    config["email_enabled"] = input("Enable email alerts? (y/n): ").strip().lower() == "y"

    if config["email_enabled"]:
        config["smtp_host"] = input("SMTP host (e.g. smtp.gmail.com): ").strip()
        config["smtp_port"] = int(input("SMTP port (587): ").strip() or "587")
        config["email_user"] = input("Email user: ").strip()
        config["email_pass"] = input("Email password/app password: ").strip()
        config["email_to"] = input("Send alerts to: ").strip()

    return config


def main():
    parser = argparse.ArgumentParser(description="Price Drop Alert Bot")
    parser.add_argument("--add", action="store_true", help="Add item interactively")
    parser.add_argument("--list", action="store_true", help="List watchlist")
    parser.add_argument("--remove", action="store_true", help="Remove item")
    parser.add_argument("--history", action="store_true", help="Show price history")
    parser.add_argument("--run", action="store_true", help="Run monitoring loop")
    parser.add_argument("--once", action="store_true", help="Check once and exit")
    parser.add_argument("--interval", type=int, default=30, help="Check interval in minutes")
    parser.add_argument("--notify", action="store_true", help="Configure notifications")

    args = parser.parse_args()

    if args.add:
        add_item_interactive()
        return

    if args.list:
        list_items()
        return

    if args.remove:
        remove_item()
        return

    if args.history:
        show_history()
        return

    if args.run or args.once:
        config = None
        if args.notify:
            config = build_notify_config()
        watch_loop(args.interval, config=config, once=args.once)
        return

    # interactive menu
    print("=== Price Drop Alert Bot ===\n")

    while True:
        print("\nOptions:")
        print("  1. Add item")
        print("  2. List watchlist")
        print("  3. Remove item")
        print("  4. Show price history")
        print("  5. Check now (once)")
        print("  6. Start monitoring loop")
        print("  7. Quit")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            add_item_interactive()
        elif choice == "2":
            list_items()
        elif choice == "3":
            remove_item()
        elif choice == "4":
            show_history()
        elif choice == "5":
            config = None
            if input("Configure notifications? (y/n): ").strip().lower() == "y":
                config = build_notify_config()
            watch_loop(1, config=config, once=True)
        elif choice == "6":
            try:
                interval = int(input("Check interval in minutes (default 30): ").strip() or "30")
            except ValueError:
                interval = 30
            config = None
            if input("Configure notifications? (y/n): ").strip().lower() == "y":
                config = build_notify_config()
            watch_loop(interval, config=config)
        elif choice == "7":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()