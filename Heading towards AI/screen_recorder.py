import os
import sys
import time
import threading
import argparse
from datetime import datetime

try:
    import cv2
    import numpy as np
except ImportError:
    print("Install: pip install opencv-python numpy")
    sys.exit(1)

try:
    import mss
    HAS_MSS = True
except ImportError:
    print("Install: pip install mss")
    sys.exit(1)

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False


def list_monitors():
    with mss.mss() as sct:
        for i, m in enumerate(sct.monitors):
            print(f"  Monitor {i}: {m['width']}x{m['height']} at ({m['left']},{m['top']})")


def parse_region(region_str):
    if not region_str:
        return None
    try:
        x, y, w, h = [int(v.strip()) for v in region_str.split(",")]
        return {"left": x, "top": y, "width": w, "height": h}
    except (ValueError, TypeError):
        print(f"Invalid region: {region_str}")
        return None


def select_region_interactive():
    if not HAS_PYAUTOGUI:
        print("pyautogui not installed; cannot do interactive selection.")
        return None

    print("Move your mouse to the TOP-LEFT corner of the region and press Enter...")
    input()
    x1, y1 = pyautogui.position()
    print(f"Top-left: ({x1}, {y1})")

    print("Move your mouse to the BOTTOM-RIGHT corner and press Enter...")
    input()
    x2, y2 = pyautogui.position()
    print(f"Bottom-right: ({x2}, {y2})")

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    if width < 10 or height < 10:
        print("Region too small.")
        return None

    return {"left": left, "top": top, "width": width, "height": height}


def get_screen_size():
    with mss.mss() as sct:
        mon = sct.monitors[1]
        return mon["width"], mon["height"]


def record_screen(output=None, fps=20, duration=None, region=None, monitor=1,
                  codec="mp4v", show_preview=True, draw_cursor=True):
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"screen_recording_{timestamp}.mp4"

    ext = os.path.splitext(output)[1].lower()

    if ext == ".avi":
        codec = "XVID"
    elif ext == ".mp4":
        codec = "mp4v"

    fourcc = cv2.VideoWriter_fourcc(*codec)

    with mss.mss() as sct:
        if region:
            bbox = region
        else:
            monitors = sct.monitors
            if monitor >= len(monitors):
                monitor = 1 if len(monitors) > 1 else 0
            bbox = monitors[monitor]

        width = bbox["width"]
        height = bbox["height"]

        # ensure even dimensions for codecs
        if width % 2 != 0:
            width -= 1
        if height % 2 != 0:
            height -= 1

        print(f"Recording region: {bbox}")
        print(f"Output: {output}")
        print(f"FPS: {fps}")
        print(f"Duration: {'unlimited' if not duration else f'{duration}s'}")
        print("Press 'q' in the preview window or Ctrl+C to stop.\n")

        writer = cv2.VideoWriter(output, fourcc, fps, (width, height))

        if not writer.isOpened():
            print("Failed to open video writer. Try a different codec or extension.")
            return

        frame_interval = 1.0 / fps
        start_time = time.time()
        frames = 0
        stop_flag = {"stop": False}

        # keyboard listener thread
        def key_listener():
            while not stop_flag["stop"]:
                if show_preview:
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("q"):
                        stop_flag["stop"] = True
                        return
                time.sleep(0.01)

        listener = threading.Thread(target=key_listener, daemon=True)
        listener.start()

        try:
            while not stop_flag["stop"]:
                loop_start = time.time()

                img = np.array(sct.grab(bbox))
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                frame = frame[:height, :width]

                if draw_cursor and HAS_PYAUTOGUI:
                    try:
                        mx, my = pyautogui.position()
                        rx = mx - bbox["left"]
                        ry = my - bbox["top"]

                        if 0 <= rx < width and 0 <= ry < height:
                            cv2.circle(frame, (rx, ry), 8, (0, 255, 255), 2)
                            cv2.circle(frame, (rx, ry), 2, (0, 255, 255), -1)
                    except Exception:
                        pass

                writer.write(frame)
                frames += 1

                if show_preview:
                    preview = cv2.resize(frame, (width // 2, height // 2))
                    elapsed = time.time() - start_time
                    cv2.putText(preview, f"REC  {elapsed:.1f}s  {frames} frames",
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 0, 255), 2)
                    cv2.putText(preview, "Press Q to stop", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.imshow("Screen Recorder", preview)

                if duration and (time.time() - start_time) >= duration:
                    print(f"Duration reached ({duration}s).")
                    break

                elapsed = time.time() - loop_start
                sleep_time = frame_interval - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            print("\nStopped by user.")

        finally:
            stop_flag["stop"] = True
            writer.release()

            if show_preview:
                cv2.destroyAllWindows()

            duration_actual = time.time() - start_time

            if os.path.isfile(output):
                size_mb = os.path.getsize(output) / (1024 * 1024)
                print(f"\nSaved: {output}")
                print(f"Frames: {frames}")
                print(f"Duration: {duration_actual:.1f}s")
                print(f"Actual FPS: {frames / duration_actual:.1f}")
                print(f"Size: {size_mb:.2f} MB")
            else:
                print("\nNo file produced.")


def main():
    parser = argparse.ArgumentParser(description="Screen Recorder")
    parser.add_argument("-o", "--output", help="Output file (.mp4 or .avi)")
    parser.add_argument("-f", "--fps", type=int, default=20, help="Frames per second")
    parser.add_argument("-t", "--time", type=int, help="Duration in seconds (blank = until stop)")
    parser.add_argument("-r", "--region", help="Region: x,y,w,h")
    parser.add_argument("-m", "--monitor", type=int, default=1, help="Monitor index")
    parser.add_argument("--no-preview", action="store_true", help="Disable preview window")
    parser.add_argument("--no-cursor", action="store_true", help="Don't draw cursor")
    parser.add_argument("--list-monitors", action="store_true", help="List monitors")

    args = parser.parse_args()

    if args.list_monitors:
        list_monitors()
        return

    if not args.output:
        print("=== Screen Recorder ===\n")
        list_monitors()

        print("\nOptions:")
        print("  1. Full screen")
        print("  2. Specific monitor")
        print("  3. Custom region")

        choice = input("\nChoose (default 1): ").strip() or "1"

        region = None
        monitor = 1

        if choice == "2":
            try:
                monitor = int(input("Monitor index: ").strip())
            except ValueError:
                monitor = 1

        elif choice == "3":
            print("\nRegion options:")
            print("  a. Enter coordinates manually")
            print("  b. Select interactively with mouse")

            sub = input("Choose (default a): ").strip().lower() or "a"

            if sub == "b":
                region = select_region_interactive()
                if not region:
                    print("Falling back to full screen.")
            else:
                coords = input("Enter region (x,y,width,height): ").strip()
                region = parse_region(coords)

        fps_input = input("FPS (default 20): ").strip()
        fps = int(fps_input) if fps_input.isdigit() else 20

        dur_input = input("Duration in seconds (blank = until stop): ").strip()
        duration = int(dur_input) if dur_input.isdigit() else None

        output = input("Output file (default auto-named .mp4): ").strip() or None

        show_preview = input("Show preview window? (y/n, default y): ").strip().lower() != "n"
        draw_cursor = input("Draw cursor indicator? (y/n, default y): ").strip().lower() != "n"

        record_screen(
            output=output,
            fps=fps,
            duration=duration,
            region=region,
            monitor=monitor,
            show_preview=show_preview,
            draw_cursor=draw_cursor
        )
        return

    region = parse_region(args.region) if args.region else None

    record_screen(
        output=args.output,
        fps=args.fps,
        duration=args.time,
        region=region,
        monitor=args.monitor,
        show_preview=not args.no_preview,
        draw_cursor=not args.no_cursor
    )


if __name__ == "__main__":
    main()