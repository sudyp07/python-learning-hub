import os
import sys
import re
import argparse
import html as html_module
from urllib.request import Request, urlopen
from urllib.parse import urlparse

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    print("Install: pip install beautifulsoup4")
    sys.exit(1)


BLOCK_TAGS = {
    "p", "div", "section", "article", "header", "footer", "main",
    "aside", "nav", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol",
    "li", "table", "tr", "blockquote", "pre", "hr", "br"
}

SKIP_TAGS = {"script", "style", "noscript", "iframe", "svg", "head", "meta", "link"}


def fetch_html(url, timeout=20):
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (HTMLtoText; educational)"
    })
    with urlopen(req, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="ignore")


def read_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def remove_skip_tags(soup):
    for tag in soup.find_all(SKIP_TAGS):
        tag.decompose()
    # also remove HTML comments
    for comment in soup.find_all(string=lambda text: isinstance(text, type(soup.new_string("")))):
        try:
            from bs4 import Comment
            if isinstance(comment, Comment):
                comment.extract()
        except ImportError:
            pass


def extract_text_basic(soup):
    remove_skip_tags(soup)

    # insert newlines for block elements
    for tag in soup.find_all(BLOCK_TAGS):
        tag.insert_after("\n")

    text = soup.get_text()

    # normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = "\n".join(line.strip() for line in text.splitlines())
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_with_formatting(soup):
    remove_skip_tags(soup)

    lines = []

    def walk(node, depth=0, list_stack=None):
        if list_stack is None:
            list_stack = []

        from bs4 import NavigableString, Tag

        if isinstance(node, NavigableString):
            text = str(node)
            text = html_module.unescape(text)
            text = re.sub(r"\s+", " ", text)
            if text.strip():
                lines.append(("text", text.strip(), depth, list_stack[:]))
            return

        if not isinstance(node, Tag):
            return

        name = node.name.lower()

        if name in SKIP_TAGS:
            return

        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            text = node.get_text(strip=True)
            if text:
                level = int(name[1])
                lines.append(("heading", text, level, list_stack[:]))
            return

        if name == "li":
            marker = "-"
            if list_stack and list_stack[-1] == "ol":
                # count index
                parent = node.parent
                idx = 1
                if parent:
                    for sib in parent.find_all("li", recursive=False):
                        if sib is node:
                            break
                        idx += 1
                marker = f"{idx}."

            inline = node.get_text(" ", strip=True)
            lines.append(("list", f"{marker} {inline}", depth, list_stack[:]))
            return

        if name == "blockquote":
            text = node.get_text(" ", strip=True)
            if text:
                for chunk in text.split("\n"):
                    lines.append(("quote", f"> {chunk}", depth, list_stack[:]))
            return

        if name == "pre":
            text = node.get_text()
            if text.strip():
                lines.append(("pre", text.rstrip(), depth, list_stack[:]))
            return

        if name == "hr":
            lines.append(("hr", "─" * 40, 0, []))
            return

        if name == "br":
            lines.append(("br", "", 0, []))
            return

        if name == "table":
            # extract table as text
            rows = []
            for tr in node.find_all("tr"):
                cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
                if cells:
                    rows.append(cells)
            if rows:
                # calc column widths
                col_count = max(len(r) for r in rows)
                widths = [0] * col_count
                for row in rows:
                    for i, cell in enumerate(row):
                        widths[i] = max(widths[i], len(cell))
                lines.append(("table_start", "", 0, []))
                for r_i, row in enumerate(rows):
                    padded = []
                    for i, cell in enumerate(row):
                        padded.append(cell.ljust(widths[i]))
                    lines.append(("table_row", " | ".join(padded), 0, []))
                    if r_i == 0:
                        lines.append(("table_sep",
                                      "-+-".join("-" * w for w in widths), 0, []))
                lines.append(("table_end", "", 0, []))
            return

        if name in ("ul", "ol"):
            list_stack.append(name)
            for child in node.children:
                walk(child, depth, list_stack)
            list_stack.pop()
            return

        # generic container
        has_block_child = False
        for child in node.children:
            from bs4 import Tag
            if isinstance(child, Tag) and child.name.lower() in BLOCK_TAGS:
                has_block_child = True
                break

        if has_block_child:
            for child in node.children:
                walk(child, depth, list_stack)
        else:
            text = node.get_text(" ", strip=True)
            if text:
                lines.append(("para", text, depth, list_stack[:]))

    body = soup.body if soup.body else soup

    for child in body.children:
        walk(child)

    # render to text
    output = []
    prev_type = None

    for entry in lines:
        kind, content, depth, _ = entry

        if kind == "heading":
            level = depth
            if output and output[-1] != "":
                output.append("")
            output.append(content.upper() if level == 1 else content)
            output.append("=" * len(content) if level == 1 else "-" * len(content) if level == 2 else "")
            output.append("")

        elif kind == "list":
            output.append("  " * depth + content)

        elif kind == "quote":
            output.append(content)

        elif kind == "pre":
            output.append("")
            output.append(content)
            output.append("")

        elif kind == "hr":
            output.append("")
            output.append(content)
            output.append("")

        elif kind == "table_row":
            output.append(content)

        elif kind == "table_sep":
            output.append(content)

        elif kind == "para":
            output.append(content)
            output.append("")

        elif kind == "br":
            output.append("")

    # collapse multiple blanks
    final = []
    prev_blank = False
    for line in output:
        if not line.strip():
            if not prev_blank:
                final.append("")
            prev_blank = True
        else:
            final.append(line)
            prev_blank = False

    return "\n".join(final).strip()


def extract_links(soup, base_url=None):
    links = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True)
        href = a["href"]

        if base_url and not href.startswith(("http://", "https://", "mailto:", "#")):
            from urllib.parse import urljoin
            href = urljoin(base_url, href)

        links.append({"text": text, "href": href})

    return links


def extract_images(soup, base_url=None):
    images = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        alt = img.get("alt", "")

        if base_url and src and not src.startswith(("http://", "https://", "data:")):
            from urllib.parse import urljoin
            src = urljoin(base_url, src)

        images.append({"src": src, "alt": alt})

    return images


def extract_metadata(soup):
    meta = {
        "title": "",
        "description": "",
        "keywords": "",
        "author": "",
        "og_title": "",
        "og_description": "",
        "og_image": "",
    }

    if soup.title:
        meta["title"] = soup.title.get_text(strip=True)

    for m in soup.find_all("meta"):
        name = (m.get("name") or "").lower()
        prop = (m.get("property") or "").lower()
        content = m.get("content", "")

        if name == "description":
            meta["description"] = content
        elif name == "keywords":
            meta["keywords"] = content
        elif name == "author":
            meta["author"] = content
        elif prop == "og:title":
            meta["og_title"] = content
        elif prop == "og:description":
            meta["og_description"] = content
        elif prop == "og:image":
            meta["og_image"] = content

    return meta


def wrap_text(text, width=80):
    if width <= 0:
        return text

    result = []
    for line in text.splitlines():
        if len(line) <= width:
            result.append(line)
            continue

        # preserve indentation
        indent = len(line) - len(line.lstrip())
        prefix = " " * indent

        words = line.strip().split()
        current = prefix

        for word in words:
            if len(current) + len(word) + 1 > width:
                result.append(current)
                current = prefix + word
            else:
                current += (" " if current != prefix else "") + word

        if current.strip():
            result.append(current)

    return "\n".join(result)


def convert(source, is_url=False, mode="basic", width=0):
    if is_url:
        html = fetch_html(source)
        base_url = source
    else:
        html = read_file(source)
        base_url = None

    soup = BeautifulSoup(html, "html.parser")

    if mode == "basic":
        text = extract_text_basic(soup)
    elif mode == "formatted":
        text = extract_with_formatting(soup)
    elif mode == "raw":
        remove_skip_tags(soup)
        text = soup.get_text()
    else:
        text = extract_text_basic(soup)

    if width > 0:
        text = wrap_text(text, width)

    return text, soup, base_url


def main():
    parser = argparse.ArgumentParser(description="HTML to Text Converter")
    parser.add_argument("input", nargs="?", help="HTML file or URL")
    parser.add_argument("-u", "--url", action="store_true", help="Treat input as URL")
    parser.add_argument("-m", "--mode", default="basic",
                        choices=["basic", "formatted", "raw"], help="Extraction mode")
    parser.add_argument("-w", "--width", type=int, default=0, help="Wrap width (0 = no wrap)")
    parser.add_argument("-o", "--output", help="Save text to file")
    parser.add_argument("--links", action="store_true", help="Show links")
    parser.add_argument("--images", action="store_true", help="Show images")
    parser.add_argument("--meta", action="store_true", help="Show metadata")

    args = parser.parse_args()

    if not args.input:
        print("=== HTML to Text Converter ===\n")
        source = input("HTML file path (or URL if starts with http): ").strip().strip('"')
        is_url = source.startswith(("http://", "https://"))

        print("\nModes:")
        print("  1. Basic (plain text)")
        print("  2. Formatted (preserve headings, lists, tables)")
        print("  3. Raw (as-is)")

        mode_choice = input("Choose (default 2): ").strip() or "2"
        mode = {"1": "basic", "2": "formatted", "3": "raw"}.get(mode_choice, "formatted")

        width_input = input("Wrap width (blank = none): ").strip()
        width = int(width_input) if width_input.isdigit() else 0

        try:
            text, soup, base_url = convert(source, is_url=is_url, mode=mode, width=width)
        except Exception as e:
            print(f"Failed: {e}")
            return

        print("\n--- Text ---")
        print(text)

        if input("\nShow links? (y/n): ").strip().lower() == "y":
            links = extract_links(soup, base_url)
            print(f"\n{len(links)} link(s):")
            for l in links[:50]:
                print(f"  {l['text']}  ->  {l['href']}")

        if input("Show images? (y/n): ").strip().lower() == "y":
            imgs = extract_images(soup, base_url)
            print(f"\n{len(imgs)} image(s):")
            for img in imgs[:50]:
                print(f"  {img['src']}  alt='{img['alt']}'")

        if input("Show metadata? (y/n): ").strip().lower() == "y":
            meta = extract_metadata(soup)
            print("\nMetadata:")
            for k, v in meta.items():
                if v:
                    print(f"  {k}: {v}")

        if input("\nSave text to file? (y/n): ").strip().lower() == "y":
            path = input("Path (default output.txt): ").strip() or "output.txt"
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved: {path}")

        return

    is_url = args.url or args.input.startswith(("http://", "https://"))

    try:
        text, soup, base_url = convert(args.input, is_url=is_url,
                                        mode=args.mode, width=args.width)
    except Exception as e:
        print(f"Failed: {e}")
        return

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved: {args.output}")
    else:
        print(text)

    if args.links:
        links = extract_links(soup, base_url)
        print(f"\n--- Links ({len(links)}) ---")
        for l in links:
            print(f"  {l['text']}  ->  {l['href']}")

    if args.images:
        imgs = extract_images(soup, base_url)
        print(f"\n--- Images ({len(imgs)}) ---")
        for img in imgs:
            print(f"  {img['src']}  alt='{img['alt']}'")

    if args.meta:
        meta = extract_metadata(soup)
        print("\n--- Metadata ---")
        for k, v in meta.items():
            if v:
                print(f"  {k}: {v}")


if __name__ == "__main__":
    main()