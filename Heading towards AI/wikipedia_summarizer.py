import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.parse import quote, urlencode

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


def fetch_json(url):
    req = Request(url, headers={"User-Agent": "WikiSummarizer/1.0 (educational)"})
    with urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_html(url):
    req = Request(url, headers={"User-Agent": "WikiSummarizer/1.0 (educational)"})
    with urlopen(req, timeout=20) as response:
        return response.read().decode("utf-8", errors="ignore")


def search_wikipedia(query, limit=5, lang="en"):
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urlencode({
        "action": "opensearch",
        "search": query,
        "limit": limit,
        "namespace": 0,
        "format": "json"
    })

    data = fetch_json(url)

    if not data or len(data) < 2:
        return []

    titles = data[1]
    descriptions = data[2] if len(data) > 2 else [""] * len(titles)
    urls = data[3] if len(data) > 3 else [""] * len(titles)

    return [{"title": t, "description": d, "url": u} for t, d, u in zip(titles, descriptions, urls)]


def get_summary(title, lang="en", sentences=None):
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
    data = fetch_json(url)

    extract = data.get("extract", "")
    if not extract:
        return None

    if sentences:
        parts = extract.split(". ")
        extract = ". ".join(parts[:sentences]).rstrip(".") + "."

    return {
        "title": data.get("title", title),
        "description": data.get("description", ""),
        "extract": extract,
        "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
        "thumbnail": data.get("thumbnail", {}).get("source", ""),
        "type": data.get("type", ""),
        "coordinates": data.get("coordinates"),
    }


def get_full_article(title, lang="en"):
    if not HAS_BS4:
        raise RuntimeError("beautifulsoup4 required for full articles: pip install beautifulsoup4")

    url = f"https://{lang}.wikipedia.org/wiki/{quote(title.replace(' ', '_'))}"
    html = fetch_html(url)

    soup = BeautifulSoup(html, "html.parser")

    content = soup.find("div", {"id": "mw-content-text"})
    if not content:
        return ""

    paragraphs = content.find_all("p")
    text_parts = []

    for p in paragraphs:
        text = p.get_text().strip()
        if len(text) > 40 and not text.startswith("Coordinates"):
            text_parts.append(text)

    return "\n\n".join(text_parts)


def get_sections(title, lang="en"):
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urlencode({
        "action": "parse",
        "page": title,
        "prop": "sections",
        "format": "json"
    })

    data = fetch_json(url)

    if "parse" not in data:
        return []

    return [s["line"] for s in data["parse"]["sections"] if s["line"]]


def get_related(title, lang="en", limit=10):
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urlencode({
        "action": "query",
        "titles": title,
        "prop": "links",
        "pllimit": limit,
        "plnamespace": 0,
        "format": "json"
    })

    data = fetch_json(url)

    pages = data.get("query", {}).get("pages", {})
    links = []

    for page in pages.values():
        for link in page.get("links", []):
            links.append(link["title"])

    return links


def get_categories(title, lang="en"):
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urlencode({
        "action": "query",
        "titles": title,
        "prop": "categories",
        "cllimit": 20,
        "format": "json"
    })

    data = fetch_json(url)

    pages = data.get("query", {}).get("pages", {})
    cats = []

    for page in pages.values():
        for c in page.get("categories", []):
            name = c["title"].replace("Category:", "")
            cats.append(name)

    return cats


def print_summary(summary):
    if not summary:
        print("No summary available.")
        return

    print()
    print("=" * 70)
    print(f"  {summary['title']}")
    if summary["description"]:
        print(f"  {summary['description']}")
    print("=" * 70)

    print()
    print(summary["extract"])

    if summary["url"]:
        print()
        print(f"Read more: {summary['url']}")


def save_summary(summary, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {summary['title']}\n\n")
            if summary["description"]:
                f.write(f"*{summary['description']}*\n\n")
            f.write(summary["extract"])
            f.write(f"\n\nSource: {summary['url']}\n")
        print(f"Saved: {path}")
    except OSError as e:
        print(f"Save failed: {e}")


def interactive_mode(lang="en"):
    print("=== Wikipedia Summarizer ===\n")

    query = input("Search: ").strip()
    if not query:
        return

    try:
        results = search_wikipedia(query, lang=lang)
    except Exception as e:
        print(f"Search failed: {e}")
        return

    if not results:
        print("No results.")
        return

    print("\nResults:")
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r['title']}")
        if r["description"]:
            print(f"     {r['description']}")

    try:
        idx = int(input("\nPick a number: ").strip()) - 1
    except ValueError:
        print("Invalid.")
        return

    if not (0 <= idx < len(results)):
        print("Out of range.")
        return

    title = results[idx]["title"]
    print(f"\nFetching summary for '{title}'...")

    try:
        summary = get_summary(title, lang=lang)
        print_summary(summary)
    except Exception as e:
        print(f"Failed: {e}")
        return

    print("\nOptions: 1) Full article  2) Sections  3) Related  4) Categories  5) Save  6) Nothing")

    choice = input("Choose: ").strip()

    if choice == '1':
        try:
            text = get_full_article(title, lang=lang)
            print("\n--- Full Article ---\n")
            print(text[:5000])
            if len(text) > 5000:
                print(f"\n... ({len(text) - 5000} more characters)")
        except Exception as e:
            print(f"Failed: {e}")

    elif choice == '2':
        try:
            sections = get_sections(title, lang=lang)
            print("\nSections:")
            for s in sections:
                print(f"  - {s}")
        except Exception as e:
            print(f"Failed: {e}")

    elif choice == '3':
        try:
            related = get_related(title, lang=lang)
            print("\nRelated topics:")
            for r in related:
                print(f"  - {r}")
        except Exception as e:
            print(f"Failed: {e}")

    elif choice == '4':
        try:
            cats = get_categories(title, lang=lang)
            print("\nCategories:")
            for c in cats:
                print(f"  - {c}")
        except Exception as e:
            print(f"Failed: {e}")

    elif choice == '5':
        path = input("Save to (default summary.md): ").strip() or "summary.md"
        save_summary(summary, path)


def main():
    parser = argparse.ArgumentParser(description="Wikipedia Summarizer")
    parser.add_argument("query", nargs="?", help="Topic to search")
    parser.add_argument("-l", "--lang", default="en", help="Language code")
    parser.add_argument("-s", "--sentences", type=int, help="Limit summary to N sentences")
    parser.add_argument("-o", "--output", help="Save summary to file")
    parser.add_argument("--full", action="store_true", help="Get full article text")
    parser.add_argument("--sections", action="store_true", help="List sections")
    parser.add_argument("--related", action="store_true", help="Show related topics")
    parser.add_argument("--categories", action="store_true", help="Show categories")
    parser.add_argument("--search", action="store_true", help="Search only, list results")

    args = parser.parse_args()

    if not args.query:
        interactive_mode(lang=args.lang)
        return

    try:
        if args.search:
            results = search_wikipedia(args.query, lang=args.lang)
            if not results:
                print("No results.")
                return
            for i, r in enumerate(results, 1):
                print(f"{i}. {r['title']}")
                if r["description"]:
                    print(f"   {r['description']}")
            return

        if args.full:
            text = get_full_article(args.query, lang=args.lang)
            print(text)
            return

        if args.sections:
            sections = get_sections(args.query, lang=args.lang)
            for s in sections:
                print(f"  - {s}")
            return

        if args.related:
            related = get_related(args.query, lang=args.lang)
            for r in related:
                print(f"  - {r}")
            return

        if args.categories:
            cats = get_categories(args.query, lang=args.lang)
            for c in cats:
                print(f"  - {c}")
            return

        summary = get_summary(args.query, lang=args.lang, sentences=args.sentences)

        if not summary:
            print(f"No summary found for '{args.query}'. Try --search.")
            return

        print_summary(summary)

        if args.output:
            save_summary(summary, args.output)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()