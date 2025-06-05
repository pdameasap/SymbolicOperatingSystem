#!/usr/bin/env bash
set -euo pipefail

# Directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Destination directory. Override with DEST=/custom/path
DEST=${DEST:-/usr/local/bin}

install_file() {
  local src="$1"
  local dest="$DEST/$(basename "$src")"
  if [[ "${SCRIPT_DIR}/$src" == "$dest" ]]; then
    echo "Skipping $src – already up to date at $dest"
  else
    cp "${SCRIPT_DIR}/$src" "$dest"
    chmod +x "$dest"
    echo "Installed $src to $DEST"
  fi
}

files=(
  wiki_raw.sh
  detect_wiki_type.py
  corpus_titles.sh
  concat_txt.sh
  categorize_link_file.py
  wiki_corpus.sh
  html2wikilinks.py
  html2struct.py
  encode_structured.py
  encode.py
  analyze_signal.py
)

for f in "${files[@]}"; do
  install_file "$f"
done
