#!/usr/bin/env python3
# Extract HTML for a Wikipedia page from a local multistream dump.
import argparse
import bz2
import os
import sys
import io
import subprocess
import tempfile
import xml.etree.ElementTree as ET

def cygpath_to_windows(path):
    # Convert a Cygwin /cygdrive/c/... path to C:\\...
    if path.startswith("/cygdrive/"):
        drive_letter = path[10]
        rest = path[11:]
        win_rest = rest.replace('/', '\\')
        return f"{drive_letter.upper()}:\\{win_rest}"
    return path

def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("title", help="Page title")
    p.add_argument("--dumpdir", default=os.environ.get("WIKI_DUMP_DIR", "/cygdrive/d/wiki"), help="Directory containing dump and index")
    p.add_argument("--outfile", help="Output HTML file", required=False)
    return p.parse_args()


def find_offsets(index_path, title):
    offset = None
    next_offset = None
    with bz2.open(index_path, "rt") as idx:
        lines = idx.readlines()
    for line in lines:
        off, _, name = line.rstrip().split(":", 2)
        if name == title:
            offset = int(off)
            break
    if offset is None:
        return None, None
    for line in lines:
        off = int(line.split(":", 1)[0])
        if off > offset:
            next_offset = off
            break
    return offset, next_offset


def extract_page_text(dump_path, offset, length, title):
    with open(dump_path, "rb") as f:
        f.seek(offset)
        chunk = f.read(length)
    xml_data = bz2.decompress(chunk)
    # The extracted chunk from the multistream dump is not a complete XML
    # document on its own.  It usually contains several consecutive ``<page>``
    # elements without a single root element which causes ``xml.etree`` to
    # raise ``ParseError`` ("junk after document element").  To allow parsing
    # these fragments we wrap the decompressed data in a dummy root element.
    wrapped = b"<root>" + xml_data + b"</root>"
    for event, elem in ET.iterparse(io.BytesIO(wrapped), events=("end",)):
        if elem.tag == "page":
            t = elem.find("title")
            if t is not None and t.text == title:
                rev = elem.find("revision")
                text_elem = rev.find("text") if rev is not None else None
                return text_elem.text if text_elem is not None else ""
            elem.clear()
    return None


def page_to_html(wikitext):
    # Use system temp dir that works across Windows + Cygwin
    with tempfile.NamedTemporaryFile("w", delete=False, dir="/cygdrive/c/Users/pdame/AppData/Local/Temp") as src:
        src.write(wikitext or "")
        temp_path = src.name  # Save the file path while it's still open

    html_path = temp_path + ".html"

    # Convert to Windows-native path format
    win_temp_path = cygpath_to_windows(temp_path)
    win_html_path = cygpath_to_windows(html_path)

    subprocess.run(["pandoc", "-f", "mediawiki", "-t", "html", win_temp_path, "-o", win_html_path], check=True)
    with open(html_path, "r") as f:
        html = f.read()
    os.remove(src.name)
    os.remove(html_path)
    return html


def main():
    args = parse_args()
    dump_path = os.path.join(args.dumpdir, "enwiki-latest-pages-articles-multistream.xml.bz2")
    index_path = os.path.join(args.dumpdir, "enwiki-latest-pages-articles-multistream-index.txt.bz2")
    if not os.path.exists(dump_path) or not os.path.exists(index_path):
        sys.exit(f"Dump or index not found in {args.dumpdir}")
    offset, next_offset = find_offsets(index_path, args.title)
    if offset is None:
        sys.exit(f"Page not found in index: {args.title}")
    if next_offset is None:
        next_offset = os.path.getsize(dump_path)
    length = next_offset - offset
    text = extract_page_text(dump_path, offset, length, args.title)
    if text is None:
        sys.exit(f"Page not found in dump chunk: {args.title}")
    html = page_to_html(text)
    if args.outfile:
        with open(args.outfile, "w") as out:
            out.write(html)
    else:
        sys.stdout.write(html)

if __name__ == "__main__":
    main()
