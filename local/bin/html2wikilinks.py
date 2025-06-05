from bs4 import BeautifulSoup, NavigableString
from collections import defaultdict
import json
import re
import urllib.parse
import requests
import sys
import os

HEADERS = {"User-Agent": "html2wikilinks/1.0"}

US = chr(0x1F)  # ASCII Unit Separator

def wiki_from_soup(soup):
    canonical = soup.find("link", rel="canonical")
    if canonical and "href" in canonical.attrs:
        url = canonical["href"]
        return urllib.parse.unquote(url.rsplit("/wiki/", 1)[-1])
    return None

# NOTE: Maybe don't use this because it had 19,000 links for Mathematics
def get_backlinks(title, limit=500):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "backlinks",
        "bltitle": title,
        "blnamespace": 0,
        "bldir": "ascending",
        "bllimit": limit,
        "format": "json"
    }

    results = []
    while True:
        response = requests.get(url, params=params).json()
        links = response["query"]["backlinks"]
        results.extend([link["title"] for link in links])

        if "continue" in response:
            params.update(response["continue"])
        else:
            break

    return results

# Example use
# titles = get_backlinks("Mathematics")
# for t in titles:
#    print(t)

def extract_links(soup):
    return sorted(set({
        urllib.parse.unquote(a["href"][6:].replace("_", " "))
        for a in soup.select("a[href^='/wiki/']")
        if not any(prefix in a["href"] for prefix in [
            ":", "#", "/wiki/Special:", "/wiki/Help:", "/wiki/Talk:"
        ])
    }))

def batch_titles(titles, size=50):
    for i in range(0, len(titles), size):
        yield titles[i:i+size]

def batch_get_categories(titles):
    url = "https://en.wikipedia.org/w/api.php"
    title_str = "|".join(titles)
    params = {
        "action": "query",
        "format": "json",
        "prop": "categories",
        "titles": title_str,
        "cllimit": "max",
        "redirects": "1"
    }

    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, json.JSONDecodeError):
        return {}

    pages = data.get("query", {}).get("pages", {})
    return {
        page.get("title", "UNKNOWN"): [
            cat["title"] for cat in page.get("categories", [])
        ]
        for page in pages.values()
    }

def canonical_filename(title):
    return urllib.parse.quote(title, safe="") + ".txt"

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python html2wikilinks.py file.html")
        exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    title = wiki_from_soup(soup)
    if not title:
        print("Error: Could not extract canonical page title.")
        exit(1)

    links = extract_links(soup)
    print(f"Found {len(links)} links from page: {title}")

    # print("LINKS: ")
    # for link in sorted(links):
    #    print(link)

    # NOTE: Maybe don't use this because it had 19,000 links for Mathematics
    # print("LINKS TO: ")
    # titles = get_backlinks(title)
    # for t in set(sorted(titles)):
    #    print(t)

    # Write output file
    title_filename = canonical_filename(title)
    output_filename = f"links_{title_filename}"
    with open(output_filename, "w", encoding="utf-8") as f_out:
        for batch in batch_titles(links, size=50):
            category_map = batch_get_categories(batch)
            for page_title, categories in category_map.items():
                line = US.join([page_title] + categories)
                f_out.write(line + "\n")

    print(f"Output written to: {output_filename}")

    # print(json.dumps(result, indent=2, ensure_ascii=False))
