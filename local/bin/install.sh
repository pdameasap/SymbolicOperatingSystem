# install.sh
#!/usr/bin/env bash
set -euo pipefail
cp wiki_raw.sh /usr/local/bin/wiki_raw.sh
chmod +x /usr/local/bin/wiki_raw.sh
echo "Installed wiki_raw.sh to /usr/local/bin"
