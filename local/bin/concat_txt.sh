#!/bin/bash

# Usage: concat_txt.sh sourcedir outputname.txt
if [ $# -ne 2 ]; then
  echo "Usage: $0 sourcedir outputfile"
  exit 1
fi

src="$1"
outfile="$2"
# Begin with STX
printf '```' > "$outfile"
printf '%b' '\x02' >> "$outfile"

files=("$src"/*.txt*)
for f in "${files[@]}"; do
  # Read entire file into a variable
  content=$(<"$f")
  # Strip leading backticks if present
  if [[ "$content" == \`\`\`* ]]; then
    content="${content:3}"
  fi
  # Strip leading STX if present
  if [[ "${content:0:1}" == $'\x02' ]]; then
    content="${content:1}"
  fi
  # Strip trailing backticks if present
  if [[ "$content" == *\`\`\` ]]; then
    content="${content::-3}"
  fi
  # Strip trailing ETX if present
  if [[ "${content: -1}" == $'\x03' ]]; then
    content="${content:0:${#content}-1}"
  fi
  printf "%s" "$content" >> "$outfile"
  # Insert GS, filename metadata, and FS
  printf '\x1Dfilename≜%s' "$(basename "$f")" >> "$outfile"
  if [[ "$f" == "${files[-1]}" ]]; then
    printf '%b' '\x1C' >> "$outfile"
  fi
done
# Final ETX with backticks
printf '%b' '\x03' >> "$outfile"
printf '```' >> "$outfile"
