import os
import re
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request
from urllib.parse import urlparse, unquote

def fetch_feed(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=30) as response:
        return response.read()

def clean_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = re.sub(r'\s+', " ", name).strip()
    return name[:150] if name else "episode"

def parse_feed(xml_data):
    root = ET.fromstring(xml_data)

    channel = root.find("channel")
    if channel is None:
        namespaces = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}
        channel = root

    title_el = channel.find("title")
    feed_title = title_el.text if title_el is not None and title_el.text else "podcast"

    episodes = []

    for item in channel.findall("item"):
        ep_title = item.findtext("title") or "untitled"
        pub_date = item.findtext("pubDate") or ""

        enclosure = item.find("enclosure")
        audio_url = None
        if enclosure is not None:
            audio_url = enclosure.get("url")

        if not audio_url:
            for child in item:
                tag = child.tag.split("}")[-1]
                if tag == "content" and child.get("url"):
                    audio_url = child.get("url")
                    break

        if audio_url:
            episodes.append({
                "title": ep_title,
                "date": pub_date,
                "url": audio_url
            })

    return feed_title, episodes

def download_file(url, dest_path):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as response:
        total = response.headers.get("Content-Length")
        total = int(total) if total else None

        downloaded = 0
        chunk_size = 65536

        with open(dest_path, "wb") as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)

                if total:
                    pct = downloaded * 100 / total
                    print(f"\r  {pct:.1f}% ({downloaded//1024} KB)", end="")
        print()

def guess_extension(url):
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    return ext if ext else ".mp3"

def main():
    feed_url = input("Podcast RSS feed URL: ").strip()
    if not feed_url:
        print("No URL given.")
        return

    print("Fetching feed...")
    try:
        xml_data = fetch_feed(feed_url)
    except Exception as e:
        print(f"Failed to fetch: {e}")
        return

    try:
        feed_title, episodes = parse_feed(xml_data)
    except ET.ParseError as e:
        print(f"Failed to parse feed: {e}")
        return

    print(f"\nPodcast: {feed_title}")
    print(f"Episodes found: {len(episodes)}\n")

    if not episodes:
        print("No downloadable episodes.")
        return

    for i, ep in enumerate(episodes, 1):
        print(f"{i}. {ep['title']}")
        if ep['date']:
            print(f"   {ep['date']}")

    print("\nEnter episode numbers to download (e.g. 1,3,5 or 'all')")
    choice = input("Selection: ").strip().lower()

    if choice == "all":
        selected = list(range(1, len(episodes) + 1))
    else:
        try:
            selected = [int(x.strip()) for x in choice.split(",")]
        except ValueError:
            print("Invalid selection.")
            return

    out_dir = clean_filename(feed_title)
    os.makedirs(out_dir, exist_ok=True)

    for num in selected:
        if num < 1 or num > len(episodes):
            print(f"Skipping {num} (out of range)")
            continue

        ep = episodes[num - 1]
        ext = guess_extension(ep["url"])
        filename = clean_filename(ep["title"]) + ext
        dest = os.path.join(out_dir, filename)

        if os.path.exists(dest):
            print(f"Already exists: {filename}")
            continue

        print(f"\nDownloading: {ep['title']}")
        try:
            download_file(ep["url"], dest)
            print(f"  Saved: {dest}")
        except Exception as e:
            print(f"  Failed: {e}")

    print("\nDone.")

if __name__ == "__main__":
    main()