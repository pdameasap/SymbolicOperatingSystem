#!/usr/bin/env python3
import argparse
from bs4 import BeautifulSoup
import sys
import re

CATEGORY_MAP = {
    "person": ["births", "deaths", "people", "physicists", "mathematicians", "scientists", "writers", "alchemists"],
    "place": ["cities", "countries", "geography", "republics", "states", "regions"],
    "organization": ["organizations", "institutes", "commissions", "corporations", "universities", "societies"],
    "publisher": ["publishers", "publishing", "media groups"],
    "identifier": ["identifiers", "catalogues", "authority control"],
    "disambiguation": ["disambiguation pages"],
    "mainpage": ["main page"],
}

def extract_categories(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    cat_div = soup.find("div", id="mw-normal-catlinks")
    if not cat_div:
        return []

    links = cat_div.find_all("a")
    return [link.get_text(strip=True).lower() for link in links]

def detect_types(categories):
    types = set()
    for label, patterns in CATEGORY_MAP.items():
        for cat in categories:
            if any(pat in cat for pat in patterns):
                types.add(label)
    return list(types)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to HTML file")
    parser.add_argument("--skip-types", nargs="*", default=[], help="Types to skip (e.g. person place)")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print(f"Error reading {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

    categories = extract_categories(html)
    types = detect_types(categories)

    print(",".join(types) if types else "unknown")

    for t in types:
        if t in args.skip_types:
            sys.exit(2)  # Indicate skip
    sys.exit(0)

if __name__ == "__main__":
    main()
