import os
import re
import urllib.request

def extract_video_id(url):
    patterns = [
        r'(?:v=)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be/)([0-9A-Za-z_-]{11})',
        r'(?:embed/)([0-9A-Za-z_-]{11})',
        r'(?:shorts/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_thumbnails(video_id):
    return {
        "maxresdefault": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        "sddefault": f"https://img.youtube.com/vi/{video_id}/sddefault.jpg",
        "hqdefault": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        "mqdefault": f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
        "default": f"https://img.youtube.com/vi/{video_id}/default.jpg",
    }

def download_thumbnail(url, filepath):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status != 200:
                return False
            data = response.read()

        if len(data) < 1000:
            return False

        with open(filepath, "wb") as f:
            f.write(data)
        return True
    except Exception:
        return False

def main():
    url = input("YouTube URL or video ID: ").strip()
    if not url:
        print("No input.")
        return

    video_id = extract_video_id(url)
    if not video_id:
        print("Could not find video ID in URL.")
        return

    print(f"\nVideo ID: {video_id}")

    out_dir = input("Output folder (blank = thumbnails): ").strip() or "thumbnails"
    os.makedirs(out_dir, exist_ok=True)

    thumbs = get_thumbnails(video_id)

    print("\nAvailable sizes:")
    keys = list(thumbs.keys())
    for i, key in enumerate(keys, 1):
        print(f"{i}. {key}")

    print("6. Download all")

    choice = input("\nChoose: ").strip()

    if choice == "6":
        selected = keys
    else:
        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(keys):
                print("Invalid choice.")
                return
            selected = [keys[idx]]
        except ValueError:
            print("Invalid choice.")
            return

    for key in selected:
        thumb_url = thumbs[key]
        filename = f"{video_id}_{key}.jpg"
        filepath = os.path.join(out_dir, filename)

        print(f"\nDownloading {key}...")
        if download_thumbnail(thumb_url, filepath):
            size = os.path.getsize(filepath)
            print(f"  Saved: {filepath} ({size // 1024} KB)")
        else:
            print(f"  Not available for this video.")

    print("\nDone.")

if __name__ == "__main__":
    main()