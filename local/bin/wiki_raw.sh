#!/usr/bin/env bash
# wiki_raw.sh "Page Title"
# Downloads a Wikipedia page and saves it as an html page

set -euo pipefail
IFS=$'\n\t'

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 \"Wikipedia Page Title\"" >&2
  exit 1
fi

title="$1"
slug="${title// /_}"
url="https://en.wikipedia.org/wiki/$slug"
outfile="${slug}.html"

# Fetch HTML
html=$(curl -sSL --user-agent "wiki_raw.sh/1.0" "$url")

# Output
echo "$html" > "$outfile"

echo "→ Saved raw HTML from '$url' to '$outfile'"
