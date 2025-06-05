#!/usr/bin/env bash
# wiki_local.sh "Page Title" [dump_dir]
# Extract HTML for a page from a local Wikipedia dump.
set -euo pipefail
IFS=$'\n\t'

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 \"Wikipedia Page Title\" [dump_dir]" >&2
  exit 1
fi

title="$1"
dumpdir="${2:-${WIKI_DUMP_DIR:-/mnt/d/wikidump}}"
slug="${title// /_}"
outfile="${slug}.html"

python3 /usr/local/bin/wiki_local.py "$title" --dumpdir "$dumpdir" --outfile "$outfile"

echo "→ Saved offline page for '$title' to '$outfile'"
