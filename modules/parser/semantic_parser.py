# File: modules/parser/semantic_parser.py

'''
Semantic Parser v1.0.0
----------------------
Parses normalized input into structured symbolic forms.
Outputs Z-glyph mappings and semantic slugs.
'''

import re

class SemanticFilter:
    def __init__(self):
        self.replacements = {
            r"[\u2018\u2019]": "'",
            r"[\u201C\u201D]": '"',
            r"[\u2013\u2014]": "-",
            r"\s{2,}": " ",
        }

    def normalize(self, text):
        for pattern, repl in self.replacements.items():
            text = re.sub(pattern, repl, text)
        return text.strip()

    def segment(self, text):
        clauses = re.split(r'[.!?;]+\s*', text)
        return [c.strip() for c in clauses if c]


class SymbolicInterpreter:
    def __init__(self):
        self.glyph_map = {
            'I': 'Z₇',
            'need': 'Z₂',
            'programmer': 'Z₁',
            'grammarian': 'Z₆',
            'statistician': 'Z₁₂',
            'physicist': 'Z₁₁',
            'mathematician': 'Z₁₃',
            'language designer': 'Z₁₀',
            'elegance': 'Z₅',
            'friend': 'Z₈',
            'companion': 'Z₄',
            'warm': 'Z₆+Z₇',
            'women': 'Z₈',
            'respect': 'Z₁₄',
            'preference': 'Z₂',
            'intimacy': 'Z₁₆',
        }

    def interpret_clause(self, clause):
        output = []
        for word in clause.lower().split():
            glyph = self.glyph_map.get(word)
            if glyph:
                output.append(glyph)
        return output


class Compressor:
    def compress(self, interpreted_clauses):
        seen = set()
        compressed = []
        for clause in interpreted_clauses:
            for glyph in clause:
                if glyph not in seen:
                    seen.add(glyph)
                    compressed.append(glyph)
        return ' '.join(compressed)


# Demo function for end-to-end parse

def parse_text(text):
    filter = SemanticFilter()
    interpreter = SymbolicInterpreter()
    compressor = Compressor()

    normalized = filter.normalize(text)
    segments = filter.segment(normalized)
    interpreted = [interpreter.interpret_clause(s) for s in segments]
    compressed = compressor.compress(interpreted)
    return compressed

if __name__ == "__main__":
    example = "I am in need of a programmer, a grammarian, a statistician, a theoretical physicist, a theoretical mathematician, and a language designer in the form of elegance."
    print(parse_text(example))
