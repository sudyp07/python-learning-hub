import os
import sys
import time
import argparse
from datetime import datetime

try:
    import cv2
except ImportError:
    print("Install: pip install opencv-python")
    sys.exit(1)


def make_output_dir(path="captures"):
    os.makedirs(path, exist_ok=True)
    return path


def add_overlay(frame, text_lines, color=(255, 255, 255), bg=(0, 0, 0)):
    h, w = frame.shape[:2]
    line_h = 24
    pad = 8
    max_w = 0

    for line in text_lines:
        (tw, _), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
        max_w = max(max_w, tw)

    box_w = max_w + pad * 2
    box_h = len(text_lines) * line_h + pad * 2

    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (10 + box_w, 10 + box_h), bg, -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    for i, line in enumerate(text_lines):
        y = 10 + pad + (i + 1) * line_h - 6
        cv2.putText(frame, line, (10 + pad, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1, cv2.LINE_AA)


def apply_filters(frame, mode):
    if mode == "none":
        return frame
    if mode == "gray":
        return cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    if mode == "sepia":
        kernel = __import__("numpy").array([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]
        ])
        import numpy as np
        sepia = cv2.transform(frame, kernel)
        return np.clip(sepia, 0, 255).astype(frame.dtype)
    if mode == "blur":
        return cv2.GaussianBlur(frame, (15, 15), 0)
    if mode == "edge":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    if mode == "negative":
        return cv2.bitwise_not(frame)
    return frame


def save_photo(frame, out_dir, prefix="photo"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = f"{prefix}_{timestamp}.png"
    path = os.path.join(out_dir, filename)
    cv2.imwrite(path, frame)
    return path


def capture_single(out_dir, camera=0, width=1280, height=720, delay=0,
                   filter_mode="none", prefix="photo"):
    cap = cv2.VideoCapture(camera)

    if not cap.isOpened():
        print(f"Could not open camera {camera}.")
        return None

    if width and height:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    if delay > 0:
        print(f"Countdown: {delay}s")
        for i in range(delay, 0, -1):
            print(f"  {i}...", end="\r", flush=True)
            time.sleep(1)
        print()

    # warm up camera
    for _ in range(5):
        cap.read()
        time.sleep(0.05)

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        print("Failed to capture frame.")
        return None

    frame = apply_filters(frame, filter_mode)

    path = save_photo(frame, out_dir, prefix=prefix)
    print(f"Saved: {path}")

    return path


def capture_burst(out_dir, camera=0, count=5, interval=0.5, width=1280,
                  height=720, filter_mode="none", prefix="burst"):
    cap = cv2.VideoCapture(camera)

    if not cap.isOpened():
        print(f"Could not open camera {camera}.")
        return []

    if width and height:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    for _ in range(5):
        cap.read()
        time.sleep(0.05)

    paths = []

    print(f"Taking {count} photos every {interval}s...\n")

    for i in range(count):
        ret, frame = cap.read()
        if not ret or frame is None:
            print(f"  Frame {i+1} failed.")
            continue

        frame = apply_filters(frame, filter_mode)
        path = save_photo(frame, out_dir, prefix=f"{prefix}_{i+1:02d}")
        paths.append(path)
        print(f"  [{i+1}/{count}] {os.path.basename(path)}")

        if i < count - 1:
            time.sleep(interval)

    cap.release()
    print(f"\nSaved {len(paths)} photos to {out_dir}")

    return paths


def capture_timelapse(out_dir, camera=0, count=20, interval=2.0, width=1280,
                      height=720, filter_mode="none", prefix="timelapse"):
    cap = cv2.VideoCapture(camera)

    if not cap.isOpened():
        print(f"Could not open camera {camera}.")
        return []

    if width and height:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    for _ in range(5):
        cap.read()
        time.sleep(0.05)

    paths = []
    start = time.time()

    print(f"Timelapse: {count} photos every {interval}s")
    print("Press Ctrl+C to stop early.\n")

    try:
        for i in range(count):
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            frame = apply_filters(frame, filter_mode)
            path = save_photo(frame, out_dir, prefix=f"{prefix}_{i+1:03d}")
            paths.append(path)

            elapsed = time.time() - start
            print(f"  [{i+1}/{count}] {os.path.basename(path)}   "
                  f"(elapsed: {elapsed:.0f}s)")

            if i < count - 1:
                time.sleep(interval)

    except KeyboardInterrupt:
        print("\nStopped early.")

    finally:
        cap.release()

    print(f"\nSaved {len(paths)} photos to {out_dir}")
    return paths


def interactive_preview(out_dir, camera=0, width=1280, height=720):
    cap = cv2.VideoCapture(camera)

    if not cap.isOpened():
        print(f"Could not open camera {camera}.")
        return

    if width and height:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    filters = ["none", "gray", "sepia", "blur", "edge", "negative"]
    filter_index = 0

    mirror = True
    shot_count = 0

    print("\nControls:")
    print("  SPACE - take photo")
    print("  F     - cycle filter")
    print("  M     - toggle mirror")
    print("  V     - toggle video recording (not implemented here; use screen recorder)")
    print("  Q/ESC - quit\n")

    video_writer = None
    recording = False
    rec_fps = 20.0
    rec_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Frame read failed.")
            break

        if mirror:
            frame = cv2.flip(frame, 1)

        display = apply_filters(frame, filters[filter_index])

        info = [
            f"Filter: {filters[filter_index]}",
            f"Mirror: {'on' if mirror else 'off'}",
            f"Shots this session: {shot_count}",
            "SPACE: capture  F: filter  M: mirror  Q: quit"
        ]

        add_overlay(display, info)

        if recording and video_writer is not None:
            video_writer.write(frame)
            rec_frames += 1
            cv2.circle(display, (display.shape[1] - 30, 30), 10, (0, 0, 255), -1)

        cv2.imshow("Webcam", display)

        key = cv2.waitKey(1) & 0xFF

        if key in (ord("q"), 27):
            break

        elif key == ord(" "):
            to_save = apply_filters(frame, filters[filter_index])
            path = save_photo(to_save, out_dir)
            shot_count += 1
            print(f"  Captured: {os.path.basename(path)}")

            # flash effect
            flash = display.copy()
            flash[:] = (255, 255, 255)
            cv2.addWeighted(flash, 0.6, display, 0.4, 0, display)
            cv2.imshow("Webcam", display)
            cv2.waitKey(80)

        elif key == ord("f"):
            filter_index = (filter_index + 1) % len(filters)
            print(f"Filter: {filters[filter_index]}")

        elif key == ord("m"):
            mirror = not mirror
            print(f"Mirror: {'on' if mirror else 'off'}")

        elif key == ord("r"):
            if not recording:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                vpath = os.path.join(out_dir, f"webcam_{timestamp}.mp4")
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                video_writer = cv2.VideoWriter(
                    vpath, fourcc, rec_fps,
                    (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                     int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                )
                recording = True
                rec_frames = 0
                print(f"Recording to {vpath}")
            else:
                recording = False
                if video_writer:
                    video_writer.release()
                    video_writer = None
                print(f"Recording stopped. Frames: {rec_frames}")

    if video_writer:
        video_writer.release()

    cap.release()
    cv2.destroyAllWindows()

    print(f"\nSession done. {shot_count} photos saved to {out_dir}")


def main():
    parser = argparse.ArgumentParser(description="Webcam Photo Capture")
    parser.add_argument("-m", "--mode", default="preview",
                        choices=["preview", "single", "burst", "timelapse"],
                        help="Capture mode")
    parser.add_argument("-o", "--output", default="captures",
                        help="Output directory")
    parser.add_argument("-c", "--camera", type=int, default=0, help="Camera index")
    parser.add_argument("-n", "--count", type=int, default=5, help="Photo count (burst/timelapse)")
    parser.add_argument("-i", "--interval", type=float, default=1.0,
                        help="Interval between photos (seconds)")
    parser.add_argument("-d", "--delay", type=int, default=0,
                        help="Delay before single capture (seconds)")
    parser.add_argument("-w", "--width", type=int, default=1280, help="Capture width")
    parser.add_argument("-H", "--height", type=int, default=720, help="Capture height")
    parser.add_argument("-f", "--filter", default="none",
                        choices=["none", "gray", "sepia", "blur", "edge", "negative"],
                        help="Filter to apply")

    args = parser.parse_args()

    out_dir = make_output_dir(args.output)
    print(f"Output directory: {out_dir}\n")

    if args.mode == "preview":
        interactive_preview(out_dir, camera=args.camera,
                            width=args.width, height=args.height)

    elif args.mode == "single":
        capture_single(out_dir, camera=args.camera, width=args.width,
                       height=args.height, delay=args.delay,
                       filter_mode=args.filter)

    elif args.mode == "burst":
        capture_burst(out_dir, camera=args.camera, count=args.count,
                      interval=args.interval, width=args.width,
                      height=args.height, filter_mode=args.filter)

    elif args.mode == "timelapse":
        capture_timelapse(out_dir, camera=args.camera, count=args.count,
                          interval=args.interval, width=args.width,
                          height=args.height, filter_mode=args.filter)


if __name__ == "__main__":
    main()