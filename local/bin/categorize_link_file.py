import sys
import urllib.parse
import os

US = chr(0x1F)

CATEGORY_MAP = {
    "person": [
        "births", "deaths", "living people", "mathematicians",
        "alumni", "biographies", "scientists"
    ],
    "organization": [
        "organizations", "associations", "societies", "institutions",
        "publishers", "journals", "universities", "companies"
    ],
    "disambiguation": [
        "disambiguation"
    ],
    "mainpage": [
        "main page"
    ],
    "place": [
        "cities", "countries", "geography of", "places in"
    ],
    "meta": [
        "articles with", "articles needing", "pages using",
        "webarchive", "maintenance", "stub", "cs1", "short description"
    ]
    # "identifier" removed from map; handled directly
}

def load_known_people(files):
    known = set()
    for filename in files:
        full_path = os.path.expanduser(filename)
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if name:
                    known.add(name)
    return known

def categorize_categories(title, categories, known_people):
    if title in known_people:
        return ["person"]

    found = set()
    for cat in categories:
        cat_lower = cat.lower()
        if cat_lower.endswith(" (identifier)"):
            found.add("identifier")
            continue
        for label, patterns in CATEGORY_MAP.items():
            if any(pat in cat_lower for pat in patterns):
                found.add(label)

    return sorted(found) if found else ["unknown"]

def parse_links_file(filepath, known_people):
    results = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(US)
            title = urllib.parse.unquote(parts[0])
            categories = parts[1:] if len(parts) > 1 else []
            kinds = categorize_categories(title, categories, known_people)
            results.append((title, kinds))
    return results

def main():
    if len(sys.argv) != 2:
        print("Usage: python categorize_link_file.py links_<Title>.txt")
        sys.exit(1)

    filename = sys.argv[1]
    known_people = load_known_people([
        "~/wiki/pantheon.txt", "~/wiki/people.txt"
    ])
    results = parse_links_file(filename, known_people)

    for title, types in results:
        print(f"{title} -> {', '.join(types)}")

if __name__ == "__main__":
    main()
