import os
import sys
import argparse

try:
    import cv2
except ImportError:
    print("Install: pip install opencv-python")
    sys.exit(1)

try:
    import pytesseract
except ImportError:
    print("Install: pip install pytesseract")
    print("Also install Tesseract OCR engine on your system:")
    print("  Windows: https://github.com/UB-Mannheim/tesseract/wiki")
    print("  Linux:   sudo apt install tesseract-ocr")
    print("  macOS:   brew install tesseract")
    sys.exit(1)


SUPPORTED_IMAGES = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp", ".gif")
SUPPORTED_PDFS = (".pdf",)


def preprocess_image(img, mode="auto"):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    if mode == "raw":
        return gray

    if mode == "thresh":
        _, out = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return out

    if mode == "denoise":
        gray = cv2.medianBlur(gray, 3)
        _, out = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return out

    if mode == "sharpen":
        kernel = cv2.getGaussianKernel(3, 0)
        blurred = cv2.GaussianBlur(gray, (0, 0), 3)
        sharpened = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)
        return sharpened

    # auto: adaptive threshold
    gray = cv2.medianBlur(gray, 3)
    out = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 31, 10)
    return out


def extract_text_from_image(path, lang="eng", psm=3, preprocess="auto", scale=1.0):
    img = cv2.imread(path)

    if img is None:
        raise ValueError(f"Could not read image: {path}")

    if scale != 1.0:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    processed = preprocess_image(img, preprocess)

    config = f"--oem 3 --psm {psm}"

    text = pytesseract.image_to_string(processed, lang=lang, config=config)
    return text, processed


def get_ocr_data(path, lang="eng", psm=3, preprocess="auto", scale=1.0):
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Could not read image: {path}")

    if scale != 1.0:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    processed = preprocess_image(img, preprocess)
    config = f"--oem 3 --psm {psm}"

    data = pytesseract.image_to_data(processed, lang=lang, config=config,
                                      output_type=pytesseract.Output.DICT)
    return data, processed


def draw_boxes(path, data, out_path, min_conf=40):
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Could not read image: {path}")

    n = len(data["text"])

    for i in range(n):
        text = data["text"][i].strip()
        if not text:
            continue

        try:
            conf = int(data["conf"][i])
        except (ValueError, TypeError):
            continue

        if conf < min_conf:
            continue

        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 200, 100), 2)

        label = f"{text} ({conf}%)"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
        cv2.rectangle(img, (x, y - th - 6), (x + tw + 4, y), (0, 200, 100), -1)
        cv2.putText(img, label, (x + 2, y - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (20, 20, 20), 1)

    cv2.imwrite(out_path, img)
    return out_path


def extract_from_pdf(pdf_path, lang="eng"):
    try:
        from pdf2image import convert_from_path
    except ImportError:
        print("Install pdf2image: pip install pdf2image")
        print("And install poppler-utils on your system.")
        return None

    pages = convert_from_path(pdf_path, dpi=200)
    results = []

    for i, page in enumerate(pages):
        arr = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        processed = preprocess_image(gray, "auto")
        text = pytesseract.image_to_string(processed, lang=lang, config="--oem 3 --psm 3")
        results.append((i + 1, text))

    return results


def save_output(text, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved: {path}")
    except OSError as e:
        print(f"Save failed: {e}")


def print_summary(text):
    lines = [l for l in text.splitlines() if l.strip()]
    words = text.split()
    print(f"\nLines: {len(lines)}")
    print(f"Words: {len(words)}")
    print(f"Chars: {len(text)}")


def interactive_mode():
    print("=== OCR Text Extractor ===\n")

    path = input("Image path: ").strip().strip('"')
    if not os.path.isfile(path):
        print("File not found.")
        return

    print("\nPreprocess modes: raw, auto, thresh, denoise, sharpen")
    mode = input("Preprocess (default auto): ").strip().lower() or "auto"
    if mode not in ("raw", "auto", "thresh", "denoise", "sharpen"):
        mode = "auto"

    print("\nPage segmentation modes (PSM):")
    print("  3  - Fully automatic (default)")
    print("  4  - Single column of text")
    print("  6  - Single uniform block of text")
    print("  7  - Single text line")
    print("  8  - Single word")
    print("  11 - Sparse text")
    print("  13 - Raw line")

    psm_input = input("PSM (default 3): ").strip() or "3"
    try:
        psm = int(psm_input)
    except ValueError:
        psm = 3

    lang = input("Language code (default 'eng'): ").strip() or "eng"

    scale_input = input("Upscale factor (default 1.0, use 1.5-2 for small text): ").strip()
    try:
        scale = float(scale_input) if scale_input else 1.0
    except ValueError:
        scale = 1.0

    print("\nProcessing...")
    try:
        text, processed = extract_text_from_image(path, lang=lang, psm=psm,
                                                   preprocess=mode, scale=scale)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("\n--- Extracted Text ---")
    print(text.strip() if text.strip() else "(no text detected)")
    print("--- End ---")

    print_summary(text)

    if input("\nShow bounding boxes overlay? (y/n): ").strip().lower() == 'y':
        try:
            data, _ = get_ocr_data(path, lang=lang, psm=psm, preprocess=mode, scale=scale)
            base, ext = os.path.splitext(path)
            out_path = f"{base}_ocr{ext}"
            draw_boxes(path, data, out_path)
            print(f"Saved overlay: {out_path}")
        except Exception as e:
            print(f"Failed: {e}")

    if input("\nSave text to file? (y/n): ").strip().lower() == 'y':
        out = input("Output path (default output.txt): ").strip() or "output.txt"
        save_output(text, out)


def main():
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="OCR Text Extractor")
        parser.add_argument("input", help="Image or PDF path")
        parser.add_argument("-o", "--output", help="Output text file")
        parser.add_argument("-l", "--lang", default="eng", help="Language code")
        parser.add_argument("-p", "--psm", type=int, default=3, help="Page segmentation mode")
        parser.add_argument("-m", "--mode", default="auto",
                            choices=["raw", "auto", "thresh", "denoise", "sharpen"],
                            help="Preprocess mode")
        parser.add_argument("-s", "--scale", type=float, default=1.0, help="Upscale factor")
        parser.add_argument("--boxes", action="store_true", help="Draw bounding boxes")
        args = parser.parse_args()

        if not os.path.isfile(args.input):
            print(f"File not found: {args.input}")
            return

        ext = os.path.splitext(args.input)[1].lower()

        if ext in SUPPORTED_PDFS:
            print("Processing PDF...")
            results = extract_from_pdf(args.input, lang=args.lang)
            if results:
                full = "\n\n".join(f"--- Page {n} ---\n{t}" for n, t in results)
                if args.output:
                    save_output(full, args.output)
                else:
                    print(full)
        else:
            print("Processing image...")
            try:
                text, _ = extract_text_from_image(
                    args.input, lang=args.lang, psm=args.psm,
                    preprocess=args.mode, scale=args.scale
                )
                if args.output:
                    save_output(text, args.output)
                else:
                    print(text)

                if args.boxes:
                    data, _ = get_ocr_data(
                        args.input, lang=args.lang, psm=args.psm,
                        preprocess=args.mode, scale=args.scale
                    )
                    base, e = os.path.splitext(args.input)
                    out_path = f"{base}_ocr{e}"
                    draw_boxes(args.input, data, out_path)
                    print(f"Saved overlay: {out_path}")

            except Exception as e:
                print(f"Error: {e}")
    else:
        interactive_mode()


if __name__ == "__main__":
    main()