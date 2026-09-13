import os
import re
import subprocess
import sys

def check_ytdlp():
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def list_formats(url):
    result = subprocess.run(
        ["yt-dlp", "-F", url],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

def download(url, out_dir="downloads", quality="best", audio_only=False):
    os.makedirs(out_dir, exist_ok=True)

    output_template = os.path.join(out_dir, "%(title)s.%(ext)s")

    cmd = ["yt-dlp", "-o", output_template]

    if audio_only:
        cmd += ["-x", "--audio-format", "mp3"]
    else:
        if quality == "best":
            cmd += ["-f", "bestvideo+bestaudio/best", "--merge-output-format", "mp4"]
        elif quality == "worst":
            cmd += ["-f", "worst"]
        else:
            cmd += ["-f", quality]

    cmd.append(url)

    print(f"\nRunning: {' '.join(cmd)}\n")
    subprocess.run(cmd)

def download_playlist(url, out_dir="downloads", audio_only=False):
    os.makedirs(out_dir, exist_ok=True)

    output_template = os.path.join(out_dir, "%(playlist_title)s", "%(playlist_index)s - %(title)s.%(ext)s")

    cmd = ["yt-dlp", "-o", output_template]

    if audio_only:
        cmd += ["-x", "--audio-format", "mp3"]

    cmd.append(url)
    subprocess.run(cmd)

def main():
    if not check_ytdlp():
        print("yt-dlp not found.")
        print("Install it: pip install yt-dlp")
        print("Also install ffmpeg for merging/audio conversion.")
        return

    url = input("YouTube URL: ").strip()
    if not url:
        print("No URL.")
        return

    is_playlist = "playlist" in url or "list=" in url

    print("\nOptions:")
    print("1. Download best quality (video)")
    print("2. Download worst quality (small)")
    print("3. Download audio only (MP3)")
    print("4. List available formats")
    print("5. Custom format code")

    choice = input("\nChoose: ").strip()

    out_dir = input("Output folder (blank = downloads): ").strip() or "downloads"

    if choice == "1":
        if is_playlist:
            download_playlist(url, out_dir)
        else:
            download(url, out_dir, quality="best")
    elif choice == "2":
        download(url, out_dir, quality="worst")
    elif choice == "3":
        if is_playlist:
            download_playlist(url, out_dir, audio_only=True)
        else:
            download(url, out_dir, audio_only=True)
    elif choice == "4":
        list_formats(url)
    elif choice == "5":
        fmt = input("Format code (e.g. 137+140): ").strip()
        download(url, out_dir, quality=fmt)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()