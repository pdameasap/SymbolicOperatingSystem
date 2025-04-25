# File: modules/parser/SemanticParser.py

import re
from modules.parser.symbolic_nouns import SYMBOLIC_NOUNS
from modules.parser.symbolic_normalizer import normalize_noun

class SemanticParser:

    def normalize(self, sentence):
        # Lowercase, remove punctuation but preserve underscores
        sentence = re.sub(r'[^\w\s]', '', sentence.lower())
        return re.sub(r'\s+', ' ', sentence).strip()

    def tokenize(self, sentence):
        tokens = sentence.split()
        cleaned_tokens = [t.strip(".,;:!?\"'()[]{}") for t in tokens]
        return cleaned_tokens

    def resolve_token_zglyph(self, word):
        base = normalize_noun(word)
        key = f"N_{base.upper()}"
        entry = SYMBOLIC_NOUNS.get(key, None)
        return entry if isinstance(entry, dict) and "Z" in entry else None

    def parse(self, sentence):
        norm = self.normalize(sentence)
        tokens = self.tokenize(norm)
        gloss = []
        for token in tokens:
            z_entry = self.resolve_token_zglyph(token)
            gloss.append(z_entry[1] if z_entry else f"?{token}")
        return gloss

    def parse_sentence(self, sentence):
        norm = self.normalize(sentence)
        tokens = self.tokenize(norm)
        gloss = self.parse(sentence)
        result = {
            "original": sentence,
            "normalized": norm,
            "tokens": tokens,
            "gloss": gloss
        }
        return result

# Example use
if __name__ == "__main__":
    parser = SemanticParser()
    result = parser.parse_sentence("A language designer and a theoretical physicist.")
    print(result)
