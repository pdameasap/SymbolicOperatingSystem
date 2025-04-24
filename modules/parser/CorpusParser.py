# File: modules/parser/CorpusParser.py

from modules.parser.SemanticParserCore import SemanticParserCore
from collections import Counter

class CorpusParser:
    def __init__(self):
        self.parser = SemanticParserCore()

    def parse_lines(self, lines):
        results = []
        z_counter = Counter()

        for idx, line in enumerate(lines):
            parsed = self.parser.normalize(line)
            z_tags = [meta["Z"] for _, meta in parsed if meta["Z"]]
            z_counter.update(z_tags)

            results.append({
                "line_number": idx + 1,
                "text": line,
                "tokens": [w for w, _ in parsed],
                "glosses": self.parser.structured(parsed),
                "z_tags": sorted(set(z_tags))
            })

        return {
            "lines": results,
            "z_summary": dict(z_counter)
        }

# Example usage
if __name__ == "__main__":
    doc = [
        "I am in need of a programmer and a grammarian.",
        "A theoretical physicist would also be nice.",
        "And perhaps a language designer, too."
    ]

    cp = CorpusParser()
    parsed_doc = cp.parse_lines(doc)

    for line in parsed_doc["lines"]:
        print(f"\nLine {line['line_number']}: {line['text']}")
        print("Z-Tags:", line["z_tags"])
        for gloss in line["glosses"]:
            print(f"  {gloss['word']:12} → Z: {gloss['Z'] or '-'} | Tag: {gloss['tag'] or '-'}")

    print("\n📊 Total Z-Summary:")
    print(parsed_doc["z_summary"])
