import os
import re
import sys
import argparse
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode


# ---------- Rule-based checks ----------

RULES = [
    (r'\b(\w+) \1\b', "Repeated word"),
    (r'\b(teh)\b', "Likely typo: 'teh' -> 'the'"),
    (r'\b(recieve)\b', "Spelling: 'recieve' -> 'receive'"),
    (r'\b(seperate)\b', "Spelling: 'seperate' -> 'separate'"),
    (r'\b(definately)\b', "Spelling: 'definately' -> 'definitely'"),
    (r'\b(alot)\b', "Use 'a lot' (two words)"),
    (r'\b(irregardless)\b', "Use 'regardless'"),
    (r'\b(could of|would of|should of)\b', "Use 'could have/would have/should have'"),
    (r'\bi ([a-z]+ing)\b', "Possible capitalization issue at sentence start"),
    (r'\s+([,.!?;:])', "Space before punctuation"),
    (r'([,.!?;:])(?=[A-Za-z])', "Missing space after punctuation"),
    (r'  +', "Multiple consecutive spaces"),
    (r'\bi\b', "Lowercase 'i' should be 'I'"),
    (r'\bits\b(?=\s+(a|an|the|very|not|been|going))', "'its' vs 'it's'"),
    (r'\byour\b(?=\s+(going|doing|coming|welcome|right|wrong))', "'your' vs \"you're\""),
    (r'\bthier\b', "'thier' -> 'their'"),
    (r'\bwich\b', "'wich' -> 'which'"),
    (r'\b(between you and I)\b', "Should be 'between you and me'"),
    (r'\b(less \w+s)\b', "Consider 'fewer' for countable nouns"),
    (r'\b(me and \w+)\b', "Consider putting yourself last"),
    (r'"([^"]*)"\s*said', "Consider comma before 'said'"),
    (r'\bin order to\b', "Consider 'to' (more concise)"),
    (r'\bdue to the fact that\b', "Consider 'because'"),
    (r'\bat this point in time\b', "Consider 'now'"),
    (r'\bin the event that\b', "Consider 'if'"),
    (r'\bvery unique\b', "'unique' is absolute; avoid 'very'"),
]


class Issue:
    def __init__(self, start, end, message, category, suggestion="", rule=""):
        self.start = start
        self.end = end
        self.message = message
        self.category = category
        self.suggestion = suggestion
        self.rule = rule


def check_rule_based(text):
    issues = []

    for pattern, message in RULES:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            matched = m.group(0)
            suggestion = ""

            if "->" in message:
                parts = message.split("->")
                suggestion = parts[1].strip().strip("'\"")

            issues.append(Issue(m.start(), m.end(), message, "rule",
                                suggestion=suggestion, rule=pattern))

    return issues


def check_sentence_structure(text):
    issues = []

    sentences = re.split(r'(?<=[.!?])\s+', text)

    offset = 0
    for sent in sentences:
        stripped = sent.strip()

        if not stripped:
            offset += len(sent) + 1
            continue

        # very long sentence
        word_count = len(stripped.split())
        if word_count > 40:
            issues.append(Issue(
                offset, offset + len(stripped),
                f"Long sentence ({word_count} words). Consider splitting.",
                "style"
            ))

        # no ending punctuation
        if stripped and stripped[-1] not in ".!?":
            issues.append(Issue(
                offset + len(stripped) - 1, offset + len(stripped),
                "Sentence missing ending punctuation.",
                "punctuation",
                suggestion=stripped[-1] + "."
            ))

        # passive voice hint
        passive = re.search(r'\b(was|were|is|are|been|being|be)\s+\w+ed\b', stripped, re.IGNORECASE)
        if passive:
            issues.append(Issue(
                offset + passive.start(), offset + passive.end(),
                "Possible passive voice. Consider active voice.",
                "style"
            ))

        # starts with lowercase
        first_alpha = next((i for i, c in enumerate(stripped) if c.isalpha()), None)
        if first_alpha is not None and stripped[first_alpha].islower():
            issues.append(Issue(
                offset + first_alpha, offset + first_alpha + 1,
                "Sentence should start with a capital letter.",
                "capitalization",
                suggestion=stripped[first_alpha].upper()
            ))

        offset += len(sent) + 1

    return issues


def check_subject_verb(text):
    issues = []

    patterns = [
        (r'\b(he|she|it)\s+(are|were|have|do)\b', "'he/she/it' with plural verb"),
        (r'\b(they|we|you)\s+(is|was|has|does)\b', "Plural subject with singular verb"),
        (r'\b(I)\s+(is|are|was\s+not\s+are)\b', "Subject-verb mismatch with 'I'"),
        (r'\b(there)\s+(is)\s+\w+s\b', "'there is' with plural noun"),
        (r'\b(there)\s+(are)\s+a\s+\w+\b', "'there are' with singular noun"),
    ]

    for pattern, msg in patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            issues.append(Issue(m.start(), m.end(), msg, "grammar"))

    return issues


# ---------- LanguageTool API ----------

def check_languagetool(text, language="en-US"):
    url = "https://api.languagetool.org/v2/check"
    data = urlencode({
        "text": text,
        "language": language
    }).encode()

    req = Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", "Mozilla/5.0")

    with urlopen(req, timeout=20) as response:
        result = json.loads(response.read().decode("utf-8"))

    issues = []
    for m in result.get("matches", []):
        start = m["offset"]
        end = start + m["length"]
        msg = m["message"]
        category = m.get("rule", {}).get("category", {}).get("name", "grammar")
        replacements = [r["value"] for r in m.get("replacements", [])][:5]
        suggestion = replacements[0] if replacements else ""

        issues.append(Issue(start, end, msg, category, suggestion=suggestion))

    return issues


# ---------- Reporting ----------

def highlight_text(text, issues):
    if not issues:
        return text

    issues_sorted = sorted(issues, key=lambda i: i.start)

    # merge overlapping
    merged = []
    for issue in issues_sorted:
        if merged and issue.start < merged[-1].end:
            continue
        merged.append(issue)

    result = []
    last = 0

    for issue in merged:
        if issue.start < last:
            continue
        result.append(text[last:issue.start])
        result.append("\033[91m")
        result.append(text[issue.start:issue.end])
        result.append("\033[0m")
        last = issue.end

    result.append(text[last:])
    return "".join(result)


def print_issues(text, issues):
    if not issues:
        print("No issues found.")
        return

    by_category = {}

    for i in issues:
        by_category.setdefault(i.category, []).append(i)

    print(f"\nTotal issues: {len(issues)}")

    for cat, items in sorted(by_category.items()):
        print(f"\n=== {cat.upper()} ({len(items)}) ===")
        for issue in items:
            snippet = text[max(0, issue.start - 20):issue.end + 20].replace("\n", " ")
            marker = " " * min(20, issue.start) + "^" * (issue.end - issue.start)

            print(f"  [{issue.start}:{issue.end}] {issue.message}")
            print(f"      {snippet}")
            print(f"      {marker}")
            if issue.suggestion:
                print(f"      Suggestion: {issue.suggestion}")


def interactive_correction(text, issues):
    if not issues:
        print("Nothing to correct.")
        return text

    sorted_issues = sorted(issues, key=lambda i: i.start, reverse=True)
    corrected = text

    print("\n--- Interactive correction ---")
    print("For each issue, type replacement or ENTER to skip.\n")

    for issue in reversed(sorted_issues):
        original = corrected[issue.start:issue.end]
        print(f"  Issue: {issue.message}")
        print(f"  Text:  '{original}'")
        if issue.suggestion:
            print(f"  Suggested: '{issue.suggestion}'")

        replacement = input("  Replace with (blank = keep): ").strip()

        if replacement:
            corrected = corrected[:issue.start] + replacement + corrected[issue.end:]

    return corrected


def main():
    parser = argparse.ArgumentParser(description="Grammar Checker")
    parser.add_argument("input", nargs="?", help="Input file")
    parser.add_argument("-l", "--lang", default="en-US", help="Language code for LanguageTool")
    parser.add_argument("--offline", action="store_true", help="Use only rule-based checks")
    parser.add_argument("-o", "--output", help="Save corrected text")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive correction mode")

    args = parser.parse_args()

    if args.input:
        if not os.path.isfile(args.input):
            print(f"Not found: {args.input}")
            return
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        print("=== Grammar Checker ===\n")
        print("Paste text (blank line to finish):")
        lines = []
        while True:
            line = input()
            if not line.strip():
                break
            lines.append(line)
        text = "\n".join(lines)

    if not text.strip():
        print("No text.")
        return

    print(f"\nAnalyzing {len(text)} characters...\n")

    issues = []

    # rule-based checks always
    issues.extend(check_rule_based(text))
    issues.extend(check_sentence_structure(text))
    issues.extend(check_subject_verb(text))

    # language tool (unless offline)
    if not args.offline:
        try:
            lt_issues = check_languagetool(text, args.lang)
            issues.extend(lt_issues)
            print(f"LanguageTool API: {len(lt_issues)} additional issues")
        except Exception as e:
            print(f"LanguageTool failed ({e}). Using rule-based only.")

    # dedupe by (start, end, message)
    seen = set()
    unique = []
    for issue in issues:
        key = (issue.start, issue.end, issue.message)
        if key in seen:
            continue
        seen.add(key)
        unique.append(issue)

    issues = unique

    print("\n--- Highlighted text ---")
    print(highlight_text(text, issues))

    print_issues(text, issues)

    if args.interactive:
        corrected = interactive_correction(text, issues)
        print("\n--- Corrected text ---")
        print(corrected)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(corrected)
            print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()