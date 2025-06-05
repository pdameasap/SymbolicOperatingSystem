# install.sh
#!/usr/bin/env bash
set -euo pipefail

cp wiki_raw.sh /usr/local/bin/wiki_raw.sh
chmod +x /usr/local/bin/wiki_raw.sh
echo "Installed wiki_raw.sh to /usr/local/bin"

cp detect_wiki_type.py /usr/local/bin/detect_wiki_type.py
chmod +x /usr/local/bin/detect_wiki_type.py
echo "Installed detect_wiki_type.py to /usr/local/bin"

cp corpus_titles.sh /usr/local/bin/corpus_titles.sh
chmod +x /usr/local/bin/corpus_titles.sh
echo "Installed corpus_titles.sh to /usr/local/bin"

cp concat_txt.sh /usr/local/bin/concat_txt.sh
chmod +x /usr/local/bin/concat_txt.sh
echo "Installed concat_txt.sh to /usr/local/bin"

cp categorize_link_file.py /usr/local/bin/categorize_link_file.py
chmod +x /usr/local/bin/categorize_link_file.py
echo "Installed categorize_link_file.py to /usr/local/bin"

cp wiki_corpus.sh /usr/local/bin/wiki_corpus.sh
chmod +x /usr/local/bin/wiki_corpus.sh
echo "Installed wiki_corpus.sh to /usr/local/bin"

cp html2wikilinks.py /usr/local/bin/html2wikilinks.py
chmod +x /usr/local/bin/html2wikilinks.py
echo "Installed html2wikilinks.py to /usr/local/bin"

cp html2struct.py /usr/local/bin/html2struct.py
chmod +x /usr/local/bin/html2struct.py
echo "Installed html2struct.py to /usr/local/bin"

cp encode_structured.py /usr/local/bin/encode_structured.py
chmod +x /usr/local/bin/encode_structured.py
echo "Installed encode_structured.py to /usr/local/bin"

cp encode.py /usr/local/bin/encode.py
chmod +x /usr/local/bin/encode.py
echo "Installed encode.py to /usr/local/bin"

cp analyze_signal.py /usr/local/bin/analyze_signal.py
chmod +x /usr/local/bin/analyze_signal.py
echo "Installed analyze_signal.py to /usr/local/bin"
