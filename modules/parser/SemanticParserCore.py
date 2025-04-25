# File: modules/parser/SemanticParserCore.py

from modules.parser.symbolic_normalizer import normalize_noun
from modules.parser.symbolic_nouns import SYMBOLIC_NOUNS

from collections import Counter

class SemanticParserCore:
    def normalize(self, sentence):
        tokens = sentence.lower().split()
        parsed = []
        for word in tokens:
            base = normalize_noun(word.strip(',."'))
            key = f"N_{base.upper()}"
            entry = SYMBOLIC_NOUNS.get(key)
            if entry:
                parsed.append((word, {"Z": entry[1], "tag": None}))
            else:
                parsed.append((word, {"Z": None, "tag": None}))
        return parsed

    def display(self, parsed):
        for word, meta in parsed:
            print(f"{word:15} → Z: {meta['Z'] or '-'} | Tag: {meta['tag'] or '-'}")

    def structured(self, parsed):
        return [{"word": w, "Z": m["Z"], "tag": m["tag"]} for w, m in parsed]

    def summarize(self, parsed):
        z_counts = Counter(meta["Z"] for _, meta in parsed if meta["Z"])
        return dict(z_counts)


# Example Usage
if __name__ == "__main__":
    parser = SemanticParserCore()
    text = (
        "I am in need of a programmer, a grammarian, a statistician, "
        "a theoretical physicist, a theoretical mathematician, "
        "and a language designer in the form of elegance."
    )
    result = parser.normalize(text)
    parser.display(result)

    print("\n🧠 Structured Output:")
    print(parser.structured(result))

    print("\n📊 Z-Summary:")
    print(parser.summarize(result))
