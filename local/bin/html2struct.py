from bs4 import BeautifulSoup
from collections import defaultdict
import json
import re
import urllib.parse
import requests
import sys

HEADERS = {"User-Agent": "html2struct/1.0"}

BANNED_SECTIONS = {
    "(top)",
    "bibliography",
    "citations",
    "external links",
    "further reading",
    "notes",
    "other sources",
    "references",
    "see also",
    "sources"
}

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
}

PROHIBITED_TYPES = {
    "person", "organization", "disambiguation", "mainpage",
    "place", "identifier", "meta", "publisher"
}


def classify_categories(categories):
    # Return category labels for a list of categories.
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


def should_include_page(categories):
    kinds = classify_categories(categories)
    return not any(k in PROHIBITED_TYPES for k in kinds)


def fetch_page_html(title):
    slug = urllib.parse.quote(title.replace(" ", "_"))
    url = f"https://en.wikipedia.org/wiki/{slug}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.text
    return None


def process_html_text(html_text, spider_links=False, verbose=False):
    soup = BeautifulSoup(html_text, "lxml")

    title_tag = soup.find("title")
    toc = filter_toc(parse_table_of_contents(soup))
    sections = extract_sections_by_toc(soup, toc)

    result = {
        "title": title_tag.get_text(strip=True) if title_tag else None,
        "toc": renumber_sections_and_generate_toc(sections),
        "sections": sections,
    }

    if spider_links:
        links = extract_links(soup)
        cat_map = batch_get_categories(links)
        related = {}
        total = len(cat_map)
        for idx, (link_title, categories) in enumerate(cat_map.items(), start=1):
            if verbose:
                print(f"[{idx}/{total}] {link_title}", file=sys.stderr, flush=True)
            if should_include_page(categories):
                html = fetch_page_html(link_title)
                if html:
                    related[link_title] = process_html_text(html, spider_links=False, verbose=verbose)
        if related:
            result["related"] = related

    result = filter_banned_sections(result, BANNED_SECTIONS)
    return result

def extract_links(soup):
    # Return a sorted list of wiki page titles linked from the document.
    return sorted(set({
        urllib.parse.unquote(a["href"][6:].replace("_", " "))
        for a in soup.select("a[href^='/wiki/']")
        if not any(prefix in a["href"] for prefix in [
            ":", "#", "/wiki/Special:", "/wiki/Help:", "/wiki/Talk:"
        ])
    }))

def _batch_titles(titles, size=50):
    # Yield successive chunks from ``titles`` with ``size`` elements.
    for i in range(0, len(titles), size):
        yield titles[i:i + size]

def batch_get_categories(titles):
    # Fetch categories for a list of wiki titles using the API.
    if not titles:
        return {}

    url = "https://en.wikipedia.org/w/api.php"
    results = {}

    for batch in _batch_titles(titles, size=50):
        params = {
            "action": "query",
            "format": "json",
            "prop": "categories",
            "titles": "|".join(batch),
            "cllimit": "max",
            "redirects": "1",
        }

        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except (requests.RequestException, json.JSONDecodeError):
            continue

        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            title = page.get("title", "UNKNOWN")
            categories = [cat["title"] for cat in page.get("categories", [])]
            results[title] = categories

    return results

def normalize_spacing(text):
    import re
    # Remove extra space before punctuation
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    # Normalize quotes (single, double)
    text = re.sub(r'([\'"])\s*(.*?)\s*\1', r'\1\2\1', text)
    # Fix space between word and possessive 's
    text = re.sub(r"([a-zA-Z])\s*'\s*s\b", r"\1's", text)
    # Normalize parentheses spacing
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    # Collapse multiple spaces
    text = re.sub(r"\s{2,}", " ", text)
    # Ensure a single space around each em-dash
    text = re.sub(r"\s*—\s*", " — ", text)
    return text.strip()

def filter_banned_sections(result, banned_sections):
    banned_norms = {re.sub(r'\W+', '', s.lower()) for s in banned_sections}
    result["sections"] = [
        section for section in result["sections"]
        if re.sub(r'\W+', '', section["section_title"].lower()) not in banned_norms
    ]
    result["toc"] = [
        entry for entry in result["toc"]
        if re.sub(r'\W+', '', entry["text"].split(maxsplit=1)[-1].lower()) not in banned_norms
    ]
    return result

def renumber_sections_and_generate_toc(sections):
    toc = []
    section_counter = 0

    for section in sections:
        section_counter += 1
        subsection_counter = 0
        toc_entry = {
            "text": f"{section_counter} {section['section_title']}",
            "href": section.get("href", f"#sec{section_counter}")
        }
        toc.append(toc_entry)

        new_blocks = []
        subsub_counter = 0
        for block in section["blocks"]:
            if block["type"] == "subsection_title":
                subsection_counter += 1
                subsub_counter = 0
                new_title = f"{section_counter}.{subsection_counter} {block['text']}"
                toc.append({
                    "text": new_title,
                    "href": block.get("href", f"#sec{section_counter}_{subsection_counter}")
                })
                new_blocks.append({
                    "href": block["href"],
                    "type": block["type"],
                    "text": new_title
                })
            elif block["type"] == "subsubsection_title":
                subsub_counter += 1
                full = f"{section_counter}.{subsection_counter}.{subsub_counter} {block['text']}"
                toc.append({
                    "text": full,
                    "href": block.get("href", f"#sec{section_counter}_{subsection_counter}_{subsub_counter}")
                })
                new_blocks.append({
                    "href": block["href"],
                    "type": block["type"],
                    "text": full
                })
            else:
                new_blocks.append(block)

        section["blocks"] = new_blocks

    return toc

def build_subsection_href_set(toc):
    subsection_hrefs = set()
    for entry in toc:
        text = entry["text"].strip()
        href = entry["href"].lstrip("#")
        if re.match(r"^\d+\.\d+", text):  # Has subsection-like prefix
            subsection_hrefs.add(href)
    return subsection_hrefs

def parse_table_of_contents(soup):
    toc_map = []
    toc_container = soup.find(
        lambda tag: (
            tag.name in {"nav", "div"} and
            "toc" in (tag.get("id", "") +
                      " ".join(tag.get("class", []))).lower()
        )
    )
    if toc_container:
        for li in toc_container.find_all("li"):
            anchor = li.find("a")
            if anchor:
                toc_map.append({
                    "text": anchor.get_text(strip=True),
                    "href": anchor.get("href", "")
                })
    return toc_map

def build_toc_anchor_map(toc):
    subsection_map = {}
    for entry in toc:
        text = entry["text"].strip()
        href = entry["href"]

        # Match prefix and label together: e.g. 4.3.1Physics
        match = re.match(r"^(?P<prefix>(\d+\.){1,2}\d+)(?P<label>.+)", text)
        if not match:
            continue

        prefix = match.group("prefix")
        label = match.group("label").strip()
        depth = prefix.count(".")

        if depth == 2:
            level = "subsubsection_title"
        elif depth == 1:
            level = "subsection_title"
        else:
            continue

        normalized = re.sub(r'\W+', '', label.lower())
        subsection_map[normalized] = {
            "text": label,
            "href": href,
            "level": level
        }

    return subsection_map

def extract_paragraph(p_tag):
    # Extract paragraph content with inline LaTeX math.
    for tag in p_tag.find_all(["a", "math"]):
        if tag.name == "a":
            tag.unwrap() # Replace links with their text
            continue
        tex = tag.find("annotation", encoding="application/x-tex")
        # Crawl up to the grandparent span, replace with the LaTeX
        if not tag.parent or tag.parent.name == "p":
            if tex and tex.string:
                tag.replace_with(tex.string)
            else:
                tag.decompose()
            continue
        if not tag.parent.parent or tag.parent.parent == "p":
            if tex and tex.string:
                tag.parent.replace_with(tex.string)
            else:
                tag.parent.decompose()
            continue
        if not tex or not tex.string:
            tag.parent.parent.decompose()
            continue
        tag.parent.parent.replace_with(tex.string)

    for sup in p_tag.find_all("sup", class_="reference"):
        sup.decompose() # Nuke all references/citations in the p element

    p_tag.smooth() # After messing with things, combine strings

    text = p_tag.get_text(" ", strip=True)
    if not text:
        return []

    return [{
        "type": "paragraph",
        "text": text
    }]

def extract_sections_by_toc(soup, toc_map):
    content_root = soup.select_one("main") or soup.body
    if not content_root:
        return []

    # Map: normalized label → metadata (text, href, level)
    subsection_map = {}
    for entry in toc_map:
        text = entry["text"].strip()
        href = entry["href"]
        match = re.match(r"^(?P<prefix>(\d+\.){1,2}\d+)(?P<label>.+)", text)
        if not match:
            continue

        prefix = match.group("prefix")
        label = match.group("label").strip()
        depth = prefix.count(".")

        if depth == 2:
            level = "subsubsection_title"
        elif depth == 1:
            level = "subsection_title"
        else:
            continue

        subsection_map[href.lstrip("#")] = {
            "text": label,
            "href": href,
            "level": level
        }

    toc_ids = {
        entry["href"].lstrip("#"): re.sub(r'\W+', '', entry["text"].lower().strip())
        for entry in toc_map
    }

    sections = []
    current_title = None
    current_blocks = []
    current_href = None

    def add_section():
        nonlocal current_title, current_blocks, current_href
        if current_title and current_blocks:
            sections.append({
                **({"href": current_href} if current_href else {}),
                "section_title": current_title,
                "blocks": current_blocks.copy()
            })
            current_blocks.clear()

    for tag in content_root.find_all(
        ["h2", "h3", "h4", "p", "ul", "ol"]
    ):
        if tag.name in {"h2", "h3", "h4"}:
            raw_title = tag.get_text(strip=True)
            clean_title = re.sub(r'^\d+(\.\d+)*[\.\)]?\s*', '', raw_title).strip()
            norm_title = re.sub(r'\W+', '', clean_title.lower())

            if norm_title in BANNED_SECTIONS:
                continue

            anchor = tag.get("id", "").strip()

            # Match against subsection_map using id/href
            if anchor in subsection_map:
                sub = subsection_map[anchor]
                current_blocks.append({
                    "type": sub["level"],
                    "text": sub["text"],
                    "href": sub["href"]
                })
                continue

            # Otherwise fall back to normal section matching
            id_match = anchor and re.sub(r'\W+', '', anchor.lower()) in toc_ids
            fuzzy_match = any(
                toc_val in norm_title or norm_title in toc_val
                for toc_val in toc_ids.values()
            )

            if id_match or fuzzy_match:
                add_section()
                current_title = clean_title
                current_href = None
                for entry in toc_map:
                    toc_norm = re.sub(r'\W+', '', entry["text"].lower().strip())
                    if toc_norm in norm_title or norm_title in toc_norm:
                        current_href = entry["href"]
                        break

        elif tag.name == "p" and current_title:
            blocks = extract_paragraph(tag)
            for b in blocks:
                if b["type"] == "paragraph":
                    b["text"] = re.sub(r"\[\s*[a-zA-Z0-9]+\s*\]", "", b["text"])
                    b["text"] = normalize_spacing(b["text"])
                current_blocks.append(b)

        elif tag.name in {"ul", "ol"} and current_title:
            for sup in tag.find_all("sup", class_="reference"):
                sup.decompose() # Nuke all references/citations in the list
            raw_items = [
                re.sub(r"\s+", " ", li.get_text(" ", strip=True))
                for li in tag.find_all("li")
            ]
            seen = set()
            items = []
            for item in raw_items:
                item = normalize_spacing(item)
                if item not in seen:
                    seen.add(item)
                    items.append(item)
            current_blocks.append({
                "type": "list",
                "items": items
            })

    add_section()
    return sections

def filter_toc(toc):
    def clean(text):
        return re.sub(r'\W+', '', text.lower().strip())
    return [entry for entry in toc if clean(
        entry["text"].split(maxsplit=1)[-1]
    ) not in BANNED_SECTIONS]

def process_html_file(filepath, spider_links=False, verbose=False):
    '''Parse an HTML file into structured JSON.

    Parameters
    ----------
    filepath : str
        Path to the HTML file.
    spider_links : bool, optional
        If true, fetch linked Wikipedia pages (excluding common
        undesirable types) and include them under the ``related``
        key in the returned structure.
    '''

    with open(filepath, "r", encoding="utf-8") as f:
        html_text = f.read()

    return process_html_text(html_text, spider_links=spider_links, verbose=verbose)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert Wikipedia HTML to structured JSON")
    parser.add_argument("html_file", help="Path to the HTML file")
    parser.add_argument("--spider-links", action="store_true",
                        help="Fetch and process linked pages as well")
    parser.add_argument("--show-progress", action="store_true",
                        help="Print progress messages to stderr")
    args = parser.parse_args()

    result = process_html_file(
        args.html_file,
        spider_links=args.spider_links,
        verbose=args.show_progress,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
