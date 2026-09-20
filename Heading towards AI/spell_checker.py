import os
import sys
import re
import argparse

try:
    from spellchecker import SpellChecker
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

try:
    import enchant
    HAS_ENCHANT = True
except ImportError:
    HAS_ENCHANT = False


COMMON_WORDS = set()

try:
    import nltk
    from nltk.corpus import words as nltk_words
    try:
        COMMON_WORDS.update(w.lower() for w in nltk_words.words())
    except LookupError:
        nltk.download("words", quiet=True)
        COMMON_WORDS.update(w.lower() for w in nltk_words.words())
except ImportError:
    pass


WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def edit_distance(a, b, max_dist=None):
    if a == b:
        return 0
    if max_dist is not None and abs(len(a) - len(b)) > max_dist:
        return max_dist + 1

    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            curr.append(min(curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost))
        prev = curr
    return prev[-1]


class FallbackChecker:
    def __init__(self, dictionary=None):
        self.dictionary = set()

        if dictionary and os.path.isfile(dictionary):
            with open(dictionary, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    w = line.strip().lower()
                    if w:
                        self.dictionary.add(w)
        else:
            self.dictionary.update(COMMON_WORDS)

    def unknown(self, tokens):
        return [t for t in tokens if t.lower() not in self.dictionary and not t.isdigit()]

    def candidates(self, word, limit=5):
        word = word.lower()
        # generate edits
        letters = "abcdefghijklmnopqrstuvwxyz"

        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [l + r[1:] for l, r in splits if r]
        transposes = [l + r[1] + r[0] + r[2:] for l, r in splits if len(r) > 1]
        replaces = [l + c + r[1:] for l, r in splits if r for c in letters]
        inserts = [l + c + r for l, r in splits for c in letters]

        candidates = set(deletes + transposes + replaces + inserts)
        known = [c for c in candidates if c in self.dictionary]
        known.sort(key=lambda w: (edit_distance(w, word), -len(w)))
        return known[:limit]


def get_checker(language="en"):
    if HAS_LIB:
        try:
            return SpellChecker(language=language), "pyspellchecker"
        except Exception:
            pass

    if HAS_ENCHANT:
        try:
            return enchant.Dict(language), "enchant"
        except Exception:
            pass

    return FallbackChecker(), "fallback"


def check_text(text, checker, backend, ignore_case=True):
    tokens = WORD_RE.findall(text)

    if ignore_case:
        lookup_tokens = [t.lower() for t in tokens]
    else:
        lookup_tokens = tokens

    if backend == "pyspellchecker":
        unknown = checker.unknown(lookup_tokens)
    elif backend == "enchant":
        unknown = [t for t in lookup_tokens if not checker.check(t)]
    else:
        unknown = checker.unknown(lookup_tokens)

    # get suggestions
    results = {}
    for u in set(unknown):
        if backend == "pyspellchecker":
            suggestions = list(checker.candidates(u) or [])
            if not suggestions:
                suggestions = checker.correction(u)
                suggestions = [suggestions] if suggestions else []
        elif backend == "enchant":
            suggestions = checker.suggest(u)[:5]
        else:
            suggestions = checker.candidates(u, limit=5)

        results[u] = suggestions[:5]

    return tokens, results


def apply_autocorrect(text, results, only_unique=True):
    def repl(match):
        word = match.group(0)
        lower = word.lower()

        if lower not in results:
            return word

        suggestions = results[lower]
        if not suggestions:
            return word

        if only_unique and len(suggestions) > 1:
            # only replace if top suggestion is clearly best
            return word

        best = suggestions[0]

        if word[0].isupper():
            return best.capitalize()
        if word.isupper() and len(word) > 1:
            return best.upper()
        return best

    return WORD_RE.sub(repl, text)


def interactive_spellcheck(text, checker, backend):
    tokens, results = check_text(text, checker, backend)

    if not results:
        print("\nNo spelling errors found.")
        return

    print(f"\nFound {len(results)} possible misspelling(s):")
    for word, sugg in results.items():
        print(f"  {word}  ->  {', '.join(sugg) if sugg else '(no suggestions)'}")

    print("\n--- Interactive correction ---")
    print("For each misspelling, type a replacement or ENTER to keep as-is.")

    corrected = text
    for word, sugg in list(results.items()):
        print(f"\nMisspelled: '{word}'")
        if sugg:
            print(f"Suggestions: {', '.join(sugg)}")

        choice = input("Replace with: ").strip()

        if not choice:
            continue

        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        corrected = pattern.sub(choice, corrected)

    print("\n--- Corrected text ---")
    print(corrected)

    save = input("\nSave corrected text? (y/n): ").strip().lower()
    if save == "y":
        out = input("Output file (default corrected.txt): ").strip() or "corrected.txt"
        with open(out, "w", encoding="utf-8") as f:
            f.write(corrected)
        print(f"Saved: {out}")


def main():
    parser = argparse.ArgumentParser(description="Spell Checker")
    parser.add_argument("input", nargs="?", help="Text file to check")
    parser.add_argument("-l", "--lang", default="en", help="Language (default en)")
    parser.add_argument("-a", "--auto", action="store_true", help="Auto-correct with top suggestions")
    parser.add_argument("-o", "--output", help="Save corrected text")

    args = parser.parse_args()

    checker, backend = get_checker(args.lang)
    print(f"=== Spell Checker ({backend}, lang={args.lang}) ===\n")

    if args.input:
        if not os.path.isfile(args.input):
            print(f"Not found: {args.input}")
            return
        with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        print("Enter text (blank line to finish):")
        lines = []
        while True:
            line = input()
            if not line.strip():
                break
            lines.append(line)
        text = "\n".join(lines)

    if not text.strip():
        print("No text provided.")
        return

    if args.auto:
        tokens, results = check_text(text, checker, backend)
        corrected = apply_autocorrect(text, results, only_unique=False)
        print("--- Corrected ---")
        print(corrected)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(corrected)
            print(f"Saved: {args.output}")
        return

    interactive_spellcheck(text, checker, backend)


if __name__ == "__main__":
    main()