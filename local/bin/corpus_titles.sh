#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 corpus_file.txt" >&2
  exit 1
fi

file="$1"
echo "📂 Topics in $file:"

# Extract titles from within STX/ETX delimited blocks
awk '
  BEGIN { RS = "\x03"; FS = "\x02" }
  {
    for (i = 1; i <= NF; i++) {
      if ($i ~ /title≜/) {
        match($i, /title≜[^;]+/, m)
        if (m[0] != "") {
          title = m[0]
          gsub(/^title≜/, "", title)
          gsub(/filename.*$/, "", title)        # remove filename spill
          gsub(/Jump to content.*$/, "", title) # remove "Jump to content"
          gsub(/Pages for .*/, "", title)       # remove "Pages for logged out editors..."
          gsub(/[[:cntrl:]]/, "", title)        # remove control chars
          gsub(/^ +| +$/, "", title)            # trim
          if (title != "") print title
        }
      }
    }
  }
' "$file" | sort | uniq
