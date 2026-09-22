import sys
import json
import argparse
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
from urllib.parse import quote
from datetime import datetime, timezone

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


FEEDS = {
    "bbc": "https://feeds.bbci.co.uk/news/rss.xml",
    "bbc-world": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "bbc-tech": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "cnn": "http://rss.cnn.com/rss/cnn_topstories.rss",
    "reuters": "https://feeds.reuters.com/reuters/topNews",
    "nytimes": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "nytimes-tech": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "wired": "https://www.wired.com/feed/rss",
    "techcrunch": "https://techcrunch.com/feed/",
    "theverge": "https://www.theverge.com/rss/index.xml",
    "arstechnica": "https://feeds.arstechnica.com/arstechnica/index",
    "hackernews": "https://hnrss.org/frontpage",
    "reddit-prog": "https://www.reddit.com/r/programming/.rss",
    "reddit-world": "https://www.reddit.com/r/worldnews/.rss",
    "google-news": "https://news.google.com/rss",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "npr": "https://feeds.npr.org/1001/rss.xml",
    "guardian-world": "https://www.theguardian.com/world/rss",
    "cnbc": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "espn": "https://www.espn.com/espn/rss/news",
}


def fetch_url(url, timeout=15):
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (NewsFetcher; educational)"
    })
    with urlopen(req, timeout=timeout) as response:
        return response.read()


def parse_rss(xml_bytes):
    items = []

    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return items

    # RSS 2.0
    for item in root.iter("item"):
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        pub_date = item.findtext("pubDate") or ""
        description = item.findtext("description") or ""
        source_el = item.find("source")
        source = source_el.text if source_el is not None else ""

        items.append({
            "title": title.strip(),
            "link": link.strip(),
            "published": pub_date.strip(),
            "description": clean_html(description)[:300],
            "source": source
        })

    # Atom
    if not items:
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            title = entry.findtext("atom:title", default="", namespaces=ns)
            link_el = entry.find("atom:link", ns)
            link = link_el.get("href") if link_el is not None else ""
            pub_date = entry.findtext("atom:updated", default="", namespaces=ns)
            summary = entry.findtext("atom:summary", default="", namespaces=ns)

            items.append({
                "title": title.strip(),
                "link": link,
                "published": pub_date,
                "description": clean_html(summary)[:300],
                "source": ""
            })

    return items


def clean_html(html):
    if not html:
        return ""
    if HAS_BS4:
        try:
            return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
        except Exception:
            pass
    import re
    return re.sub(r"<[^>]+>", "", html).strip()


def parse_date(date_str):
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f%z",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    return None


def time_ago(dt):
    if not dt:
        return ""

    now = datetime.now(timezone.utc)
    diff = now - dt
    seconds = int(diff.total_seconds())

    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{seconds // 60}m ago"
    if seconds < 86400:
        return f"{seconds // 3600}h ago"
    if seconds < 604800:
        return f"{seconds // 86400}d ago"
    return dt.strftime("%b %d, %Y")


def fetch_feed(name_or_url):
    if name_or_url in FEEDS:
        url = FEEDS[name_or_url]
        source_name = name_or_url
    else:
        url = name_or_url
        source_name = url

    try:
        xml_bytes = fetch_url(url)
        items = parse_rss(xml_bytes)
        for item in items:
            item["feed"] = source_name
        return items
    except Exception as e:
        print(f"Failed to fetch {source_name}: {e}")
        return []


def display_headlines(items, limit=15, show_desc=False, show_source=False, show_time=True):
    if not items:
        print("No headlines.")
        return

    # sort by date
    def sort_key(item):
        dt = parse_date(item["published"])
        return dt or datetime.min.replace(tzinfo=timezone.utc)

    items = sorted(items, key=sort_key, reverse=True)

    for i, item in enumerate(items[:limit], 1):
        title = item["title"]

        meta = []
        if show_source and item.get("feed"):
            meta.append(item["feed"].upper())
        if item.get("source"):
            meta.append(item["source"])
        if show_time:
            dt = parse_date(item["published"])
            if dt:
                meta.append(time_ago(dt))

        meta_str = "  ·  ".join(meta)

        print(f"{i:>2}. {title}")
        if meta_str:
            print(f"    \033[2m{meta_str}\033[0m")
        if show_desc and item.get("description"):
            print(f"    {item['description']}")
        if item.get("link"):
            print(f"    \033[94m{item['link']}\033[0m")
        print()


def search_headlines(items, keyword):
    kw = keyword.lower()
    matches = []
    for item in items:
        text = (item["title"] + " " + item.get("description", "")).lower()
        if kw in text:
            matches.append(item)
    return matches


def filter_by_keywords(items, keywords):
    result = []
    kws = [k.lower() for k in keywords]
    for item in items:
        text = (item["title"] + " " + item.get("description", "")).lower()
        if any(k in text for k in kws):
            result.append(item)
    return result


def export_json(items, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(items)} items to {path}")
    except OSError as e:
        print(f"Save failed: {e}")


def export_csv(items, path):
    import csv
    try:
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "link", "published", "description", "source", "feed"])
            writer.writeheader()
            for item in items:
                row = {k: item.get(k, "") for k in writer.fieldnames}
                writer.writerow(row)
        print(f"Saved {len(items)} items to {path}")
    except OSError as e:
        print(f"Save failed: {e}")


def list_feeds():
    print("\nAvailable feeds:")
    for name in sorted(FEEDS.keys()):
        print(f"  {name}")
    print()


def interactive_mode():
    print("=== News Headline Fetcher ===\n")
    list_feeds()

    choice = input("Feed name (or full URL): ").strip()

    if not choice:
        print("Nothing selected.")
        return

    print(f"\nFetching {choice}...")
    items = fetch_feed(choice)

    if not items:
        return

    print(f"Got {len(items)} items.\n")

    try:
        limit = int(input("Show how many? (default 15): ").strip() or "15")
    except ValueError:
        limit = 15

    show_desc = input("Show descriptions? (y/n): ").strip().lower() == "y"
    show_source = input("Show source name? (y/n): ").strip().lower() == "y"
    show_time = input("Show relative time? (y/n, default y): ").strip().lower() != "n"

    print()
    display_headlines(items, limit=limit, show_desc=show_desc,
                      show_source=show_source, show_time=show_time)

    search = input("\nSearch keyword (blank to skip): ").strip()
    if search:
        results = search_headlines(items, search)
        print(f"\n{len(results)} matches:\n")
        display_headlines(results, limit=50, show_desc=True, show_source=True)

    save = input("\nSave results? (json/csv/none): ").strip().lower()
    if save == "json":
        path = input("Path (default news.json): ").strip() or "news.json"
        export_json(items, path)
    elif save == "csv":
        path = input("Path (default news.csv): ").strip() or "news.csv"
        export_csv(items, path)


def main():
    parser = argparse.ArgumentParser(description="News Headline Fetcher")
    parser.add_argument("feed", nargs="?", help="Feed name or URL")
    parser.add_argument("-n", "--limit", type=int, default=15, help="Number of headlines")
    parser.add_argument("-d", "--desc", action="store_true", help="Show descriptions")
    parser.add_argument("-s", "--source", action="store_true", help="Show source")
    parser.add_argument("-k", "--keyword", help="Filter by keyword")
    parser.add_argument("-o", "--output", help="Save results (ends in .json or .csv)")
    parser.add_argument("--list", action="store_true", help="List available feeds")
    parser.add_argument("--all", action="store_true", help="Fetch from all feeds")

    args = parser.parse_args()

    if args.list:
        list_feeds()
        return

    if not args.feed and not args.all:
        interactive_mode()
        return

    if args.all:
        all_items = []
        for name in FEEDS.keys():
            print(f"Fetching {name}...")
            items = fetch_feed(name)
            all_items.extend(items)
            if args.keyword:
                pass
        items = all_items
    else:
        items = fetch_feed(args.feed)

    if args.keyword:
        items = search_headlines(items, args.keyword)

    display_headlines(items, limit=args.limit, show_desc=args.desc,
                      show_source=args.source or args.all)

    if args.output:
        if args.output.endswith(".csv"):
            export_csv(items, args.output)
        else:
            export_json(items, args.output)


if __name__ == "__main__":
    main()