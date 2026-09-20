import os
import sys
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote

try:
    import argostranslate.package
    import argostranslate.translate
    HAS_ARGOS = True
except ImportError:
    HAS_ARGOS = False


LANGUAGES = {
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "it": "Italian", "pt": "Portuguese", "ru": "Russian", "ja": "Japanese",
    "ko": "Korean", "zh": "Chinese", "ar": "Arabic", "hi": "Hindi",
    "bn": "Bengali", "nl": "Dutch", "pl": "Polish", "tr": "Turkish",
    "vi": "Vietnamese", "th": "Thai", "sv": "Swedish", "da": "Danish",
    "fi": "Finnish", "no": "Norwegian", "cs": "Czech", "el": "Greek",
    "he": "Hebrew", "uk": "Ukrainian", "ro": "Romanian", "hu": "Hungarian"
}


def translate_mymemory(text, source, target):
    url = "https://api.mymemory.translated.net/get"
    params = urlencode({"q": text, "langpair": f"{source}|{target}"})
    req = Request(f"{url}?{params}", headers={"User-Agent": "Mozilla/5.0"})

    with urlopen(req, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    if data.get("responseStatus") != 200:
        raise RuntimeError(data.get("responseDetails", "Translation failed"))

    return data["responseData"]["translatedText"]


def translate_libretranslate(text, source, target, api_key=None, endpoint="https://libretranslate.com/translate"):
    payload = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text"
    }
    if api_key:
        payload["api_key"] = api_key

    req = Request(endpoint, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0")

    with urlopen(req, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data.get("translatedText", "")


def install_argos_package(from_code, to_code):
    print(f"Installing Argos package {from_code} -> {to_code}...")
    argostranslate.package.update_package_index()
    available = argostranslate.package.get_available_packages()
    pkg = next((p for p in available if p.from_code == from_code and p.to_code == to_code), None)

    if not pkg:
        raise RuntimeError(f"No offline package for {from_code} -> {to_code}")

    argostranslate.package.install_from_path(pkg.download())
    print("Installed.")


def translate_argos(text, source, target):
    if not HAS_ARGOS:
        raise RuntimeError("argostranslate not installed")

    installed = argostranslate.translate.get_installed_languages()
    from_lang = next((l for l in installed if l.code == source), None)
    to_lang = next((l for l in installed if l.code == target), None)

    if not from_lang or not to_lang:
        install_argos_package(source, target)
        installed = argostranslate.translate.get_installed_languages()
        from_lang = next((l for l in installed if l.code == source), None)
        to_lang = next((l for l in installed if l.code == target), None)

    if not from_lang or not to_lang:
        raise RuntimeError("Language not available")

    translation = from_lang.get_translation(to_lang)
    return translation.translate(text)


def detect_language(text):
    url = "https://api.mymemory.translated.net/get"
    params = urlencode({"q": text, "langpair": "en|es"})
    req = Request(f"{url}?{params}", headers={"User-Agent": "Mozilla/5.0"})

    try:
        with urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        matches = data.get("matches", [])
        if matches:
            src = matches[0].get("source", "")
            if src:
                return src.split("-")[0].lower()
    except Exception:
        pass
    return None


def show_languages():
    print("\nSupported language codes:")
    items = sorted(LANGUAGES.items(), key=lambda x: x[1])
    for i, (code, name) in enumerate(items, 1):
        print(f"  {code:4} - {name}", end="   ")
        if i % 3 == 0:
            print()
    print()


def pick_language(prompt, default=None):
    show_languages()
    choice = input(f"{prompt}" + (f" (default {default}): " if default else ": ")).strip().lower()
    return choice or default


def main():
    print("=== Translator (API-based) ===\n")

    print("Engines:")
    print("  1. MyMemory (free, no key)")
    print("  2. LibreTranslate (may need key)")
    if HAS_ARGOS:
        print("  3. Argos Translate (offline, auto-installs packages)")

    engine = input("\nChoose (default 1): ").strip() or "1"

    if engine == "1":
        translate_fn = translate_mymemory
    elif engine == "2":
        endpoint = input("Endpoint (default https://libretranslate.com/translate): ").strip() or "https://libretranslate.com/translate"
        api_key = input("API key (blank if not required): ").strip() or None

        def translate_fn(text, source, target):
            return translate_libretranslate(text, source, target, api_key, endpoint)
    elif engine == "3" and HAS_ARGOS:
        translate_fn = translate_argos
    else:
        print("Invalid. Using MyMemory.")
        translate_fn = translate_mymemory

    while True:
        print("\n--- New Translation ---")
        text = input("Text: ").strip()
        if not text:
            continue

        source = input("Source language (blank = auto-detect, default en): ").strip().lower()
        if not source:
            if engine == "1":
                detected = detect_language(text)
                source = detected or "en"
                print(f"Detected: {source}")
            else:
                source = "en"

        target = pick_language("Target language", default="es")

        if source not in LANGUAGES:
            print(f"Unknown source: {source}")
            continue
        if target not in LANGUAGES:
            print(f"Unknown target: {target}")
            continue

        if source == target:
            print("Source and target are the same.")
            continue

        print(f"\nTranslating {source} -> {target}...")

        try:
            result = translate_fn(text, source, target)
            print(f"\nResult: {result}")
        except Exception as e:
            print(f"Error: {e}")

        again = input("\nTranslate another? (y/n): ").strip().lower()
        if again != "y":
            break

    print("Done.")


if __name__ == "__main__":
    main()