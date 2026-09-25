import os
import sys
import argparse
import subprocess
import shutil
import tempfile


def check_ffmpeg():
    return shutil.which("ffmpeg") is not None


def check_imagemagick():
    return shutil.which("convert") is not None or shutil.which("magick") is not None


def get_video_info(path):
    """Try to get basic info via ffprobe."""
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None

    try:
        result = subprocess.run(
            [ffprobe, "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,duration,r_frame_rate,codec_name",
             "-of", "default=noprint_wrappers=1", path],
            capture_output=True, text=True, timeout=15
        )

        info = {}
        for line in result.stdout.strip().splitlines():
            if "=" in line:
                k, _, v = line.partition("=")
                info[k.strip()] = v.strip()

        return info
    except Exception:
        return None


def build_ffmpeg_palette_cmd(input_path, start, duration, fps, width, output_path,
                             loop=0, dither="sierra2_4a", stats_mode="diff"):
    """Two-pass high-quality palette generation."""

    scale = f"scale={width}:-1:flags=lanczos"

    filter_complex = (
        f"fps={fps},{scale},split[s0][s1];"
        f"[s0]palettegen=max_colors=256:stats_mode={stats_mode}[p];"
        f"[s1][p]paletteuse=dither={dither}"
    )

    cmd = ["ffmpeg", "-y"]

    if start is not None:
        cmd += ["-ss", str(start)]

    cmd += ["-i", input_path]

    if duration is not None:
        cmd += ["-t", str(duration)]

    cmd += [
        "-filter_complex", filter_complex,
        "-loop", str(loop),
        output_path
    ]

    return cmd


def build_simple_cmd(input_path, start, duration, fps, width, output_path,
                     loop=0, quality="high"):
    """Simple single-pass conversion."""

    scale = f"scale={width}:-1:flags=lanczos"

    if quality == "high":
        vf = f"fps={fps},{scale},split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
    elif quality == "medium":
        vf = f"fps={fps},{scale},split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
    else:
        vf = f"fps={fps},{scale}"

    cmd = ["ffmpeg", "-y"]

    if start is not None:
        cmd += ["-ss", str(start)]

    cmd += ["-i", input_path]

    if duration is not None:
        cmd += ["-t", str(duration)]

    cmd += [
        "-vf", vf,
        "-loop", str(loop),
        output_path
    ]

    return cmd


def convert_with_ffmpeg(input_path, output_path, start=None, duration=None,
                        fps=10, width=480, quality="high", loop=0,
                        two_pass=True, dither="sierra2_4a"):

    if not check_ffmpeg():
        raise RuntimeError("ffmpeg not found. Install ffmpeg and add it to PATH.")

    if two_pass and quality == "high":
        cmd = build_ffmpeg_palette_cmd(
            input_path, start, duration, fps, width, output_path,
            loop=loop, dither=dither
        )
    else:
        cmd = build_simple_cmd(
            input_path, start, duration, fps, width, output_path,
            loop=loop, quality=quality
        )

    print("Running:")
    print("  " + " ".join(cmd))
    print()

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        if result.returncode != 0:
            print("ffmpeg failed:")
            print(result.stderr[-2000:] if result.stderr else "(no error output)")
            return False

        if not os.path.isfile(output_path):
            print("No output file produced.")
            return False

        return True

    except subprocess.TimeoutExpired:
        print("Conversion timed out.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def convert_with_pillow(input_path, output_path, start=None, duration=None,
                        fps=10, width=480, loop=0):
    """Fallback using OpenCV + Pillow if ffmpeg not available."""
    try:
        import cv2
        from PIL import Image
    except ImportError:
        print("Install opencv-python and Pillow for fallback mode.")
        return False

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Could not open: {input_path}")
        return False

    video_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    if video_fps <= 0:
        video_fps = 30

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = total_frames / video_fps if total_frames else 0

    start_frame = int((start or 0) * video_fps)
    end_frame = total_frames
    if duration:
        end_frame = min(total_frames, int((start or 0) * video_fps + duration * video_fps))

    frame_step = max(1, int(round(video_fps / fps)))

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frames = []
    frame_idx = start_frame

    print(f"Extracting frames every {frame_step} from {start_frame} to {end_frame}...")

    while frame_idx < end_frame:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        # resize
        h, w = frame.shape[:2]
        new_w = width
        new_h = int(h * (new_w / w))
        if new_h % 2 != 0:
            new_h += 1

        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # convert BGR -> RGB
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        frames.append(pil_img)

        frame_idx += frame_step

    cap.release()

    if not frames:
        print("No frames extracted.")
        return False

    print(f"Assembling GIF with {len(frames)} frames...")

    frame_duration = int(1000 / fps)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration,
        loop=loop,
        optimize=True,
        disposal=2
    )

    return os.path.isfile(output_path)


def trim_gif(input_path, output_path, start, end):
    """Trim a GIF using Pillow."""
    try:
        from PIL import Image, ImageSequence
    except ImportError:
        print("Install Pillow: pip install Pillow")
        return False

    try:
        with Image.open(input_path) as im:
            frames = []
            durations = []

            current_time = 0

            for frame in ImageSequence.Iterator(im):
                duration = frame.info.get("duration", 100)
                frame_end = current_time + duration

                if current_time >= start and frame_end <= end:
                    frames.append(frame.convert("RGBA").copy())
                    durations.append(duration)

                current_time = frame_end

                if current_time > end:
                    break

            if not frames:
                print("No frames in the selected range.")
                return False

            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=im.info.get("loop", 0),
                optimize=True,
                disposal=2
            )

            return True

    except Exception as e:
        print(f"Trim failed: {e}")
        return False


def speed_gif(input_path, output_path, factor):
    """Change GIF playback speed. factor > 1 = faster, < 1 = slower."""
    try:
        from PIL import Image, ImageSequence
    except ImportError:
        print("Install Pillow: pip install Pillow")
        return False

    try:
        with Image.open(input_path) as im:
            frames = []
            durations = []

            for frame in ImageSequence.Iterator(im):
                frames.append(frame.convert("RGBA").copy())
                duration = frame.info.get("duration", 100)
                durations.append(max(20, int(duration / factor)))

            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=im.info.get("loop", 0),
                optimize=True,
                disposal=2
            )

            return True

    except Exception as e:
        print(f"Speed change failed: {e}")
        return False


def extract_frames(input_path, output_dir, fps=10, width=480):
    """Extract frames as PNG images instead of GIF."""
    try:
        import cv2
    except ImportError:
        print("Install opencv-python.")
        return False

    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Could not open: {input_path}")
        return False

    video_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    if video_fps <= 0:
        video_fps = 30

    frame_step = max(1, int(round(video_fps / fps)))

    frame_idx = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_step == 0:
            h, w = frame.shape[:2]
            new_w = width
            new_h = int(h * (new_w / w))
            resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

            out_path = os.path.join(output_dir, f"frame_{saved:05d}.png")
            cv2.imwrite(out_path, resized)
            saved += 1

        frame_idx += 1

    cap.release()
    print(f"Extracted {saved} frames to {output_dir}")
    return True


def interactive_mode():
    print("=== Video to GIF Converter ===\n")

    print(f"ffmpeg available: {check_ffmpeg()}")

    path = input("Video path: ").strip().strip('"')

    if not os.path.isfile(path):
        print("File not found.")
        return

    info = get_video_info(path)
    if info:
        print("\nVideo info:")
        for k, v in info.items():
            print(f"  {k}: {v}")
    else:
        print("(could not read video info)")

    print("\nOptions:")
    print("  1. Convert whole video")
    print("  2. Convert a time range")
    print("  3. Extract frames as PNGs")
    print("  4. Trim existing GIF")
    print("  5. Change GIF speed")

    choice = input("\nChoose (default 1): ").strip() or "1"

    if choice == "3":
        out_dir = input("Output directory (default frames): ").strip() or "frames"
        fps = int(input("FPS to extract (default 10): ").strip() or "10")
        width = int(input("Width (default 480): ").strip() or "480")
        extract_frames(path, out_dir, fps=fps, width=width)
        return

    if choice == "4":
        print("Trim an existing GIF")
        gif_path = input("GIF path: ").strip().strip('"')
        if not os.path.isfile(gif_path):
            print("Not found.")
            return
        start = float(input("Start time (seconds): ").strip() or "0")
        end = float(input("End time (seconds): ").strip() or "5")
        out = input("Output GIF (default trimmed.gif): ").strip() or "trimmed.gif"
        if trim_gif(gif_path, out, start, end):
            print(f"Saved: {out}")
        return

    if choice == "5":
        gif_path = input("GIF path: ").strip().strip('"')
        if not os.path.isfile(gif_path):
            print("Not found.")
            return
        factor_input = input("Speed factor (>1 faster, <1 slower, default 2): ").strip() or "2"
        factor = float(factor_input)
        out = input("Output GIF (default speed.gif): ").strip() or "speed.gif"
        if speed_gif(gif_path, out, factor):
            print(f"Saved: {out}")
        return

    start = None
    duration = None

    if choice == "2":
        start_input = input("Start time (seconds, default 0): ").strip() or "0"
        start = float(start_input)
        dur_input = input("Duration (seconds): ").strip() or "5"
        duration = float(dur_input)

    fps_input = input("FPS (default 10): ").strip() or "10"
    fps = int(fps_input)

    width_input = input("Width px (default 480): ").strip() or "480"
    width = int(width_input)

    print("\nQuality: high, medium, low")
    quality = input("Quality (default high): ").strip().lower() or "high"

    loop_input = input("Loop forever? (0=yes, -1=no, default 0): ").strip() or "0"
    loop = int(loop_input)

    default_out = os.path.splitext(os.path.basename(path))[0] + ".gif"
    out = input(f"Output GIF (default {default_out}): ").strip() or default_out

    if check_ffmpeg():
        print(f"\nConverting to {out}...")
        ok = convert_with_ffmpeg(
            path, out,
            start=start, duration=duration,
            fps=fps, width=width, quality=quality,
            loop=loop, two_pass=(quality == "high")
        )
    else:
        print("\nffmpeg not found, using Pillow fallback...")
        ok = convert_with_pillow(
            path, out,
            start=start, duration=duration,
            fps=fps, width=width, loop=loop
        )

    if ok:
        size_kb = os.path.getsize(out) / 1024
        print(f"\nSaved: {out}  ({size_kb:.1f} KB)")
    else:
        print("\nConversion failed.")


def main():
    parser = argparse.ArgumentParser(description="Video to GIF Converter")
    parser.add_argument("input", nargs="?", help="Input video file")
    parser.add_argument("-o", "--output", help="Output GIF file")
    parser.add_argument("-s", "--start", type=float, help="Start time (seconds)")
    parser.add_argument("-t", "--duration", type=float, help="Duration (seconds)")
    parser.add_argument("-f", "--fps", type=int, default=10, help="Frames per second")
    parser.add_argument("-w", "--width", type=int, default=480, help="Output width")
    parser.add_argument("-q", "--quality", default="high",
                        choices=["high", "medium", "low"])
    parser.add_argument("--loop", type=int, default=0, help="0=loop forever, -1=no loop")
    parser.add_argument("--extract-frames", action="store_true",
                        help="Extract PNG frames instead of GIF")
    parser.add_argument("--frames-dir", default="frames", help="Output dir for frames")
    parser.add_argument("--info", action="store_true", help="Show video info only")

    args = parser.parse_args()

    if not args.input:
        interactive_mode()
        return

    if not os.path.isfile(args.input):
        print(f"Not found: {args.input}")
        return

    if args.info:
        info = get_video_info(args.input)
        if info:
            for k, v in info.items():
                print(f"{k}: {v}")
        else:
            print("Could not read video info (is ffprobe installed?).")
        return

    if args.extract_frames:
        extract_frames(args.input, args.frames_dir, fps=args.fps, width=args.width)
        return

    output = args.output
    if not output:
        base = os.path.splitext(os.path.basename(args.input))[0]
        output = base + ".gif"

    if check_ffmpeg():
        ok = convert_with_ffmpeg(
            args.input, output,
            start=args.start, duration=args.duration,
            fps=args.fps, width=args.width, quality=args.quality,
            loop=args.loop, two_pass=(args.quality == "high")
        )
    else:
        print("ffmpeg not found, using Pillow fallback...")
        ok = convert_with_pillow(
            args.input, output,
            start=args.start, duration=args.duration,
            fps=args.fps, width=args.width, loop=args.loop
        )

    if ok:
        size_kb = os.path.getsize(output) / 1024
        print(f"Saved: {output}  ({size_kb:.1f} KB)")
    else:
        print("Conversion failed.")


if __name__ == "__main__":
    main()