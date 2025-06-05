#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 \"Wikipedia Topic Title\"" >&2
  exit 1
fi

topic="$1"
slug="${topic// /_}"
origdir="$(pwd)"
workdir="${origdir}/${slug}"
mkdir -p "$workdir"
cd "$workdir"
prohibited=("disambiguation" "identifier" "mainpage" "person" "place" "publisher" "organization")

echo "📥 Fetching main page for \"$topic\"..."
/usr/local/bin/wiki_raw.sh "$topic"

# echo "🧠 Filtering links based on section context..."
python3 /usr/local/bin/filter_links.py "${slug}.html" related.txt

echo "📡 Fetching related pages and processing..."
while read -r link; do
  # Check for slash
  if [[ "$link" == *"/"* ]]; then
    echo "⏭️ Skipping \"$link\" — contains slash"
    continue
  fi

  /usr/local/bin/wiki_raw.sh "$link" || { echo "❌ Failed: $link" >&2; continue; }
  types=$(python3 /usr/local/bin/detect_wiki_type.py --input "${link}.html")
  # Convert comma-separated types into array
  IFS=',' read -r -a detected <<< "$types"
  # Build a hash set for fast lookups
  declare -A is_prohibited
  for p in "${prohibited[@]}"; do
    is_prohibited["$p"]=1
  done
  # Check if any detected type is in the prohibited set
  for t in "${detected[@]}"; do
    if [[ -n "${is_prohibited[$t]+found}" ]]; then
      echo "🚫 Skipping \"$link\" — detected as $t"
      rm -f "${link}.html"
      continue 2  # Skip this link
    fi
  done

  python3 /usr/local/bin/encode.py "${link}.html" "${link}.txt"
  python3 /usr/local/bin/analyze_signal.py "${link}.txt"
  python3 /usr/local/bin/encode_structured.py "_${link}.txt"
  rm -f "${link}.html" "${link}.txt" "_${link}.txt"
done < related.txt

echo "⚙️ Running pipeline on main page..."
python3 /usr/local/bin/encode.py "${slug}.html" "${slug}.txt"
python3 /usr/local/bin/analyze_signal.py "${slug}.txt"
python3 /usr/local/bin/encode_structured.py "_${slug}.txt"
rm -f related.txt "${slug}.html" "${slug}.txt" "_${slug}.txt"

echo "🧬 Concatenating into final corpus..."
corpus_file="corpus_${slug}.txt"
/usr/local/bin/concat_txt.sh . "../${corpus_file}"

cd "$origdir"
rm -rf "$workdir"
echo "✅ Done: $corpus_file"
