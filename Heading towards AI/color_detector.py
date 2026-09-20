import os
import sys
import argparse
import webcolors

try:
    import cv2
    import numpy as np
except ImportError:
    print("Install: pip install opencv-python numpy webcolors")
    sys.exit(1)


SUPPORTED = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp")


def rgb_to_name(rgb):
    r, g, b = rgb
    try:
        name = webcolors.rgb_to_name((r, g, b))
        return name
    except ValueError:
        # find closest
        min_dist = float("inf")
        closest = "unknown"
        for hex_val, name in webcolors.CSS3_HEX_TO_NAMES.items():
            cr, cg, cb = webcolors.hex_to_rgb(hex_val)
            dist = (cr - r) ** 2 + (cg - g) ** 2 + (cb - b) ** 2
            if dist < min_dist:
                min_dist = dist
                closest = name
        return closest


def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])


def rgb_to_hsv(rgb):
    arr = np.uint8([[rgb]])
    hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)[0][0]
    return int(hsv[0]), int(hsv[1]), int(hsv[2])


def get_average_color(img, x, y, radius=5):
    h, w = img.shape[:2]
    x1 = max(0, x - radius)
    y1 = max(0, y - radius)
    x2 = min(w, x + radius)
    y2 = min(h, y + radius)

    region = img[y1:y2, x1:x2]
    avg_bgr = np.mean(region, axis=(0, 1))
    avg_rgb = (int(avg_bgr[2]), int(avg_bgr[1]), int(avg_bgr[0]))
    return avg_rgb


def draw_color_info(img, x, y, rgb, name):
    h, w = img.shape[:2]

    box_w = 260
    box_h = 130
    bx = x + 20
    by = y + 20

    if bx + box_w > w:
        bx = x - box_w - 20
    if by + box_h > h:
        by = y - box_h - 20

    bx = max(0, bx)
    by = max(0, by)

    overlay = img.copy()
    cv2.rectangle(overlay, (bx, by), (bx + box_w, by + box_h), (25, 25, 25), -1)
    cv2.addWeighted(overlay, 0.85, img, 0.15, 0, img)

    cv2.rectangle(img, (bx, by), (bx + box_w, by + box_h), (200, 200, 200), 1)

    color_swatch = np.zeros((60, 60, 3), dtype=np.uint8)
    color_swatch[:] = (rgb[2], rgb[1], rgb[0])
    img[by + 15:by + 75, bx + 15:bx + 75] = color_swatch
    cv2.rectangle(img, (bx + 15, by + 75), (bx + 75, by + 75), (200, 200, 200), 1)
    cv2.rectangle(img, (bx + 15, by + 15), (bx + 75, by + 75), (200, 200, 200), 1)

    hex_str = rgb_to_hex(rgb)
    hsv = rgb_to_hsv(rgb)

    tx = bx + 90
    cv2.putText(img, name.upper(), (tx, by + 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(img, f"RGB: {rgb[0]}, {rgb[1]}, {rgb[2]}", (tx, by + 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
    cv2.putText(img, f"HEX: {hex_str}", (tx, by + 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
    cv2.putText(img, f"HSV: {hsv[0]}, {hsv[1]}, {hsv[2]}", (tx, by + 95),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)


def pick_color_interactive(path):
    img = cv2.imread(path)
    if img is None:
        print(f"Could not read: {path}")
        return

    display = img.copy()
    h, w = display.shape[:2]

    max_w = 1200
    max_h = 800
    scale = 1.0

    if w > max_w or h > max_h:
        scale = min(max_w / w, max_h / h)
        display = cv2.resize(display, None, fx=scale, fy=scale)

    print("\nClick on the image to pick a color.")
    print("Press 'S' to save, 'R' to reset, 'Q' or ESC to quit.")

    picked = []

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            orig_x = int(x / scale)
            orig_y = int(y / scale)

            rgb = get_average_color(img, orig_x, orig_y, radius=4)
            name = rgb_to_name(rgb)

            picked.append({
                "x": orig_x,
                "y": orig_y,
                "rgb": rgb,
                "hex": rgb_to_hex(rgb),
                "name": name
            })

            cv2.circle(display, (x, y), 8, (0, 0, 0), 2)
            cv2.circle(display, (x, y), 8, (255, 255, 255), 1)
            cv2.circle(display, (x, y), 3, (rgb[2], rgb[1], rgb[0]), -1)

            draw_color_info(display, x, y, rgb, name)

            print(f"Picked at ({orig_x}, {orig_y}): "
                  f"RGB {rgb}  HEX {rgb_to_hex(rgb)}  Name: {name}")

    cv2.namedWindow("Color Detector", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Color Detector", on_mouse)

    while True:
        cv2.imshow("Color Detector", display)
        key = cv2.waitKey(20) & 0xFF

        if key in (ord('q'), 27):
            break
        elif key == ord('r'):
            display = img.copy()
            if scale != 1.0:
                display = cv2.resize(display, None, fx=scale, fy=scale)
            picked = []
            print("Reset.")
        elif key == ord('s'):
            if picked:
                out = "picked_colors.txt"
                with open(out, "w", encoding="utf-8") as f:
                    for i, p in enumerate(picked, 1):
                        f.write(f"{i}. ({p['x']},{p['y']})  "
                                f"RGB{p['rgb']}  {p['hex']}  {p['name']}\n")
                print(f"Saved {len(picked)} colors to {out}")
            else:
                print("Nothing to save.")

    cv2.destroyAllWindows()


def dominant_colors(path, k=5, show=True, save=None):
    img = cv2.imread(path)
    if img is None:
        print(f"Could not read: {path}")
        return

    # resize for speed
    h, w = img.shape[:2]
    scale = 200 / max(h, w)
    small = cv2.resize(img, None, fx=scale, fy=scale)

    data = small.reshape((-1, 3)).astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

    centers = np.uint8(centers)
    counts = np.bincount(labels.flatten(), minlength=k)

    order = np.argsort(counts)[::-1]

    print(f"\nTop {k} dominant colors:")
    result = []

    for i in order:
        bgr = centers[i]
        rgb = (int(bgr[2]), int(bgr[1]), int(bgr[0]))
        hex_str = rgb_to_hex(rgb)
        name = rgb_to_name(rgb)
        pct = 100 * counts[i] / counts.sum()

        print(f"  {name:<20} RGB{rgb}  {hex_str}  {pct:.1f}%")
        result.append((rgb, hex_str, name, pct))

    if show:
        swatch_h = 100
        swatch_w = 800
        canvas = np.zeros((swatch_h, swatch_w, 3), dtype=np.uint8)

        x = 0
        for rgb, hex_str, name, pct in result:
            seg_w = int(swatch_w * pct / 100)
            canvas[:, x:x + seg_w] = (rgb[2], rgb[1], rgb[0])
            x += seg_w

        canvas = cv2.resize(canvas, (800, 200), interpolation=cv2.INTER_NEAREST)

        for i, (rgb, hex_str, name, pct) in enumerate(result):
            y = 30 + i * 30
            cv2.rectangle(canvas, (10, y - 18), (35, y + 4), (rgb[2], rgb[1], rgb[0]), -1)
            cv2.rectangle(canvas, (10, y - 18), (35, y + 4), (255, 255, 255), 1)
            cv2.putText(canvas, f"{name}  {hex_str}  {pct:.1f}%",
                        (45, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Dominant Colors", canvas)

        if save:
            cv2.imwrite(save, canvas)
            print(f"Saved palette: {save}")

        print("\nPress any key in the window to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return result


def analyze_single_pixel(path, x, y):
    img = cv2.imread(path)
    if img is None:
        print(f"Could not read: {path}")
        return

    h, w = img.shape[:2]
    if not (0 <= x < w and 0 <= y < h):
        print(f"Coordinates out of range (image is {w}x{h})")
        return

    rgb = get_average_color(img, x, y, radius=2)
    hex_str = rgb_to_hex(rgb)
    name = rgb_to_name(rgb)
    hsv = rgb_to_hsv(rgb)

    print(f"\nPixel ({x}, {y}):")
    print(f"  RGB:  {rgb}")
    print(f"  HEX:  {hex_str}")
    print(f"  HSV:  {hsv}")
    print(f"  Name: {name}")


def main():
    parser = argparse.ArgumentParser(description="Color Detector from Image")
    parser.add_argument("input", nargs="?", help="Image path")
    parser.add_argument("--pixel", nargs=2, type=int, metavar=("X", "Y"),
                        help="Get color at specific pixel")
    parser.add_argument("--dominant", type=int, metavar="K",
                        help="Show K dominant colors")
    parser.add_argument("--save-palette", help="Save dominant color palette to file")
    parser.add_argument("--no-show", action="store_true", help="Don't display windows")

    args = parser.parse_args()

    if not args.input:
        print("=== Color Detector ===\n")
        path = input("Image path: ").strip().strip('"')
    else:
        path = args.input

    if not os.path.isfile(path):
        print("File not found.")
        return

    if args.pixel:
        analyze_single_pixel(path, args.pixel[0], args.pixel[1])
    elif args.dominant:
        dominant_colors(path, k=args.dominant, show=not args.no_show,
                        save=args.save_palette)
    else:
        print("\n1. Interactive picker")
        print("2. Dominant colors")
        print("3. Single pixel analysis")

        choice = input("\nChoose: ").strip()

        if choice == '1':
            pick_color_interactive(path)
        elif choice == '2':
            try:
                k = int(input("Number of colors (default 5): ").strip() or "5")
            except ValueError:
                k = 5
            save = input("Save palette PNG path (blank to skip): ").strip() or None
            dominant_colors(path, k=k, show=True, save=save)
        elif choice == '3':
            try:
                x = int(input("X coordinate: ").strip())
                y = int(input("Y coordinate: ").strip())
                analyze_single_pixel(path, x, y)
            except ValueError:
                print("Invalid coordinates.")
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()