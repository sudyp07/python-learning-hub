import os
import sys
import json
import time
import csv
import argparse
import re
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote, urlparse
from datetime import datetime

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    print("Install: pip install beautifulsoup4")
    sys.exit(1)


REMOTEOK_API = "https://remoteok.com/api"
ARBEITNOW_API = "https://www.arbeitnow.com/api/job-board-api"
HIMALAYAS_API = "https://himalayas.app/jobs/api"


def fetch(url, headers=None, timeout=20):
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept": "application/json, text/html;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    if headers:
        default_headers.update(headers)

    req = Request(url, headers=default_headers)
    with urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="ignore")


def fetch_json(url, headers=None):
    return json.loads(fetch(url, headers=headers))


# ---------- RemoteOK ----------

def scrape_remoteok(keyword=None, limit=50):
    try:
        data = fetch_json(REMOTEOK_API)
    except Exception as e:
        print(f"RemoteOK failed: {e}")
        return []

    jobs = []
    for item in data:
        if not isinstance(item, dict) or "position" not in item:
            continue

        title = item.get("position", "")
        company = item.get("company", "")
        tags = item.get("tags", []) or []
        location = item.get("location", "Remote") or "Remote"
        salary_min = item.get("salary_min")
        salary_max = item.get("salary_max")
        url = item.get("url") or item.get("apply_url") or ""
        date = item.get("date", "")

        if keyword:
            haystack = (title + " " + company + " " + " ".join(tags) + " " + location).lower()
            if keyword.lower() not in haystack:
                continue

        salary = ""
        if salary_min and salary_max:
            salary = f"${salary_min:,} - ${salary_max:,}"
        elif salary_min:
            salary = f"${salary_min:,}+"

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "tags": tags,
            "salary": salary,
            "url": url,
            "date": date,
            "source": "RemoteOK"
        })

        if len(jobs) >= limit:
            break

    return jobs


# ---------- Arbeitnow ----------

def scrape_arbeitnow(keyword=None, limit=50):
    try:
        data = fetch_json(ARBEITNOW_API)
    except Exception as e:
        print(f"Arbeitnow failed: {e}")
        return []

    jobs = []

    for item in data.get("data", []):
        title = item.get("title", "")
        company = item.get("company_name", "")
        location = item.get("location", "")
        remote = item.get("remote", False)
        tags = item.get("tags", []) or []
        url = item.get("url", "")
        date = item.get("created_at", 0)
        description = item.get("description", "")

        haystack = (title + " " + company + " " + location + " " + " ".join(tags)).lower()

        if keyword and keyword.lower() not in haystack:
            continue

        loc_display = location
        if remote:
            loc_display = (location + " (Remote)").strip() if location else "Remote"

        try:
            date_str = datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d")
        except (ValueError, TypeError, OSError):
            date_str = ""

        jobs.append({
            "title": title,
            "company": company,
            "location": loc_display,
            "tags": tags,
            "salary": "",
            "url": url,
            "date": date_str,
            "source": "Arbeitnow",
            "description": re.sub(r"<[^>]+>", " ", description)[:200]
        })

        if len(jobs) >= limit:
            break

    return jobs


# ---------- Himalayas ----------

def scrape_himalayas(keyword=None, limit=50):
    try:
        data = fetch_json(HIMALAYAS_API)
    except Exception as e:
        print(f"Himalayas failed: {e}")
        return []

    jobs = []

    for item in data.get("jobs", []):
        title = item.get("title", "")
        company = item.get("companyName", "") or item.get("company", "")
        location = item.get("locationRestrictions", [])
        if isinstance(location, list):
            location = ", ".join(location) if location else "Remote"
        salary_min = item.get("minSalary")
        salary_max = item.get("maxSalary")
        url = item.get("applicationLink") or item.get("guid") or ""
        date = item.get("pubDate", "")

        haystack = (title + " " + company + " " + str(location)).lower()
        if keyword and keyword.lower() not in haystack:
            continue

        salary = ""
        if salary_min and salary_max:
            salary = f"${salary_min:,} - ${salary_max:,}"

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "tags": [],
            "salary": salary,
            "url": url,
            "date": date[:10] if date else "",
            "source": "Himalayas"
        })

        if len(jobs) >= limit:
            break

    return jobs


# ---------- Hacker News Who's Hiring ----------

def scrape_hn_hiring(keyword=None, limit=50):
    try:
        item = fetch_json("https://hacker-news.firebaseio.com/v0/maxitem.json")
    except Exception:
        return []

    # Find latest "Who is hiring" thread
    def search_threads():
        try:
            top = fetch_json("https://hacker-news.firebaseio.com/v0/topstories.json")
        except Exception:
            return None

        for story_id in top[:500]:
            try:
                story = fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
                title = (story.get("title") or "").lower()
                if "who is hiring" in title or "who's hiring" in title:
                    return story
            except Exception:
                continue
        return None

    story = search_threads()
    if not story:
        print("No recent 'Who is hiring' thread.")
        return []

    kids = story.get("kids", []) or []
    jobs = []

    for cid in kids[:limit * 2]:
        try:
            comment = fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{cid}.json")
        except Exception:
            continue

        text = comment.get("text") or ""
        plain = re.sub(r"<[^>]+>", " ", text)
        plain = plain.replace("&#x27;", "'").replace("&quot;", '"').replace("&amp;", "&")
        plain = re.sub(r"\s+", " ", plain).strip()

        if not plain:
            continue

        first_line = plain.split("|")[0].strip()[:120]

        if keyword and keyword.lower() not in plain.lower():
            continue

        jobs.append({
            "title": first_line,
            "company": "",
            "location": "",
            "tags": [],
            "salary": "",
            "url": f"https://news.ycombinator.com/item?id={cid}",
            "date": datetime.fromtimestamp(comment.get("time", 0)).strftime("%Y-%m-%d"),
            "source": "HN Who's Hiring",
            "description": plain[:200]
        })

        if len(jobs) >= limit:
            break

    return jobs


# ---------- Filtering ----------

def filter_jobs(jobs, keywords=None, exclude=None, location=None, min_salary=None):
    result = jobs

    if keywords:
        kw_list = [k.lower() for k in keywords]
        result = [
            j for j in result
            if any(
                k in (j.get("title", "") + " " + j.get("company", "") + " " + " ".join(j.get("tags", []))).lower()
                for k in kw_list
            )
        ]

    if exclude:
        ex_list = [e.lower() for e in exclude]
        result = [
            j for j in result
            if not any(
                e in (j.get("title", "") + " " + j.get("description", "")).lower()
                for e in ex_list
            )
        ]

    if location:
        loc = location.lower()
        result = [j for j in result if loc in (j.get("location", "") or "").lower()]

    if min_salary:
        def parse_sal(s):
            nums = re.findall(r"\d[\d,]*", s or "")
            if not nums:
                return 0
            return int(nums[0].replace(",", ""))
        result = [j for j in result if parse_sal(j.get("salary", "")) >= min_salary]

    return result


def dedupe_jobs(jobs):
    seen = set()
    result = []
    for j in jobs:
        key = (j.get("title", "").lower().strip(), j.get("company", "").lower().strip())
        if key in seen:
            continue
        seen.add(key)
        result.append(j)
    return result


# ---------- Output ----------

def display_jobs(jobs, limit=30):
    if not jobs:
        print("No jobs found.")
        return

    for i, j in enumerate(jobs[:limit], 1):
        print(f"\n{i}. {j['title']}")
        if j.get("company"):
            print(f"   Company:  {j['company']}")
        if j.get("location"):
            print(f"   Location: {j['location']}")
        if j.get("salary"):
            print(f"   Salary:   {j['salary']}")
        if j.get("tags"):
            print(f"   Tags:     {', '.join(j['tags'][:8])}")
        if j.get("date"):
            print(f"   Posted:   {j['date']}")
        print(f"   Source:   {j['source']}")
        if j.get("description"):
            print(f"   {j['description'][:180]}...")
        print(f"   URL:      {j['url']}")

    if len(jobs) > limit:
        print(f"\n... and {len(jobs) - limit} more.")


def save_json(jobs, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(jobs)} jobs to {path}")
    except OSError as e:
        print(f"Save failed: {e}")


def save_csv(jobs, path):
    if not jobs:
        return
    fields = ["title", "company", "location", "salary", "tags", "date", "source", "url", "description"]
    try:
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            for j in jobs:
                row = dict(j)
                row["tags"] = ", ".join(row.get("tags", []))
                writer.writerow(row)
        print(f"Saved {len(jobs)} jobs to {path}")
    except OSError as e:
        print(f"Save failed: {e}")


# ---------- Main ----------

SOURCES = {
    "remoteok": scrape_remoteok,
    "arbeitnow": scrape_arbeitnow,
    "himalayas": scrape_himalayas,
    "hn": scrape_hn_hiring,
}


def interactive_mode():
    print("=== Job Scraper ===\n")

    print("Sources:")
    for i, name in enumerate(SOURCES.keys(), 1):
        print(f"  {i}. {name}")
    print("  a. All sources")

    choice = input("\nChoose (default a): ").strip().lower() or "a"

    if choice == "a":
        sources = list(SOURCES.keys())
    elif choice.isdigit() and 1 <= int(choice) <= len(SOURCES):
        sources = [list(SOURCES.keys())[int(choice) - 1]]
    else:
        print("Invalid.")
        return

    keyword = input("Keyword (blank for all): ").strip() or None
    exclude = input("Exclude keywords (comma-separated): ").strip()
    exclude_list = [x.strip() for x in exclude.split(",") if x.strip()] if exclude else None

    location = input("Location filter (blank for none): ").strip() or None

    min_sal_input = input("Min salary (blank for none): ").strip()
    min_salary = None
    if min_sal_input:
        try:
            min_salary = int(min_sal_input)
        except ValueError:
            pass

    all_jobs = []
    for src in sources:
        print(f"\nFetching from {src}...")
        try:
            jobs = SOURCES[src](keyword=keyword, limit=50)
            print(f"  Got {len(jobs)} jobs.")
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"  Failed: {e}")

    all_jobs = filter_jobs(all_jobs, keywords=None, exclude=exclude_list,
                            location=location, min_salary=min_salary)
    all_jobs = dedupe_jobs(all_jobs)

    print(f"\nTotal after filtering: {len(all_jobs)}")

    try:
        limit = int(input("Show how many? (default 20): ").strip() or "20")
    except ValueError:
        limit = 20

    display_jobs(all_jobs, limit=limit)

    save = input("\nSave results? (json/csv/none): ").strip().lower()
    if save == "json":
        path = input("Path (default jobs.json): ").strip() or "jobs.json"
        save_json(all_jobs, path)
    elif save == "csv":
        path = input("Path (default jobs.csv): ").strip() or "jobs.csv"
        save_csv(all_jobs, path)


def main():
    parser = argparse.ArgumentParser(description="Job Scraper")
    parser.add_argument("-s", "--source", choices=list(SOURCES.keys()) + ["all"], default="all")
    parser.add_argument("-k", "--keyword", help="Search keyword")
    parser.add_argument("-x", "--exclude", help="Exclude keywords (comma-separated)")
    parser.add_argument("-l", "--location", help="Location filter")
    parser.add_argument("--min-salary", type=int, help="Minimum salary")
    parser.add_argument("-n", "--limit", type=int, default=20, help="Number to display")
    parser.add_argument("-o", "--output", help="Save results (.json or .csv)")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        interactive_mode()
        return

    if args.source == "all":
        sources = list(SOURCES.keys())
    else:
        sources = [args.source]

    exclude_list = None
    if args.exclude:
        exclude_list = [x.strip() for x in args.exclude.split(",") if x.strip()]

    all_jobs = []
    for src in sources:
        print(f"Fetching from {src}...")
        try:
            jobs = SOURCES[src](keyword=args.keyword, limit=50)
            print(f"  {len(jobs)} jobs")
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"  Failed: {e}")

    all_jobs = filter_jobs(all_jobs, exclude=exclude_list,
                            location=args.location, min_salary=args.min_salary)
    all_jobs = dedupe_jobs(all_jobs)

    print(f"\nTotal: {len(all_jobs)} jobs\n")
    display_jobs(all_jobs, limit=args.limit)

    if args.output:
        if args.output.endswith(".csv"):
            save_csv(all_jobs, args.output)
        else:
            save_json(all_jobs, args.output)


if __name__ == "__main__":
    main()