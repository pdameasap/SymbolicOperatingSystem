# File: modules/parser/SemanticParserCore.py

'''
Semantic Parser Core
---------------------
A minimal recursive symbolic parser designed to:
- Normalize symbolic meaning from filtered input
- Annotate glosses and context per token
- Prepare output for compression, synthesis, or interpretation
'''

class SemanticParser:
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
            entry = self.glossary.get(word.strip(',.'), None)
            if entry:
                parsed.append((word, entry))
            else:
                parsed.append((word, {"Z": None, "tag": None}))
        return parsed

    def display(self, parsed):
        for word, meta in parsed:
            print(f"{word:15} → Z: {meta['Z'] or '-'} | Tag: {meta['tag'] or '-'}")


# Example Usage
if __name__ == "__main__":
    parser = SemanticParser()
    text = "I am in need of a programmer, a grammarian, a statistician, a theoretical physicist, a theoretical mathematician, and a language designer in the form of elegance."
    result = parser.normalize(text)
    parser.display(result)
