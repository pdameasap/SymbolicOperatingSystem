# File: modules/parser/SemanticParserCore.py

'''
Semantic Parser Core
---------------------
A minimal recursive symbolic parser designed to:
- Normalize symbolic meaning from filtered input
- Annotate glosses and context per token
- Prepare output for compression, synthesis, or interpretation
'''

from modules.parser.symbolic_normalizer import normalize_noun

from collections import Counter

class SemanticParserCore:
    def __init__(self):
        self.glossary = self.load_glosses()

    def load_glosses(self):
        # For now, hardcoded symbolic glosses; can be expanded
        return {
            "programmer": {"Z": "Z₁", "tag": "structure"},
            "grammarian": {"Z": "Z₆", "tag": "expression"},
            "statistician": {"Z": "Z₁₂", "tag": "change"},
            "physicist": {"Z": "Z₁₁", "tag": "stasis"},
            "mathematician": {"Z": "Z₁₃", "tag": "abstraction"},
            "language designer": {"Z": "Z₁₀", "tag": "architecture"},
            "woman": {"Z": "Z₈", "tag": "containment"},
            "friend": {"Z": "Z₂", "tag": "relation"},
            "companion": {"Z": "Z₄", "tag": "network"},
            "warmth": {"Z": "Z₆", "tag": "expression"},
            "elegance": {"Z": "Z₅", "tag": "aesthetic cognition"},
        }

    def normalize(self, sentence):
        tokens = sentence.lower().split()
        parsed = []
        for word in tokens:
            base = normalize_noun(word.strip(',."'))
            entry = self.glossary.get(base, None)
            if entry:
                parsed.append((word, entry))
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
