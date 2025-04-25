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
        return sentence.split()

    def resolve_token_zglyph(self, word):
        base = normalize_noun(word)
        key = f"N_{base.upper()}"
        return SYMBOLIC_NOUNS.get(key, None)

    def parse(self, sentence):
        norm = self.normalize(sentence)
        tokens = self.tokenize(norm)
        gloss = []
        for token in tokens:
            clean_token = token.strip(".,;:!?\"'()[]{}")
            _, z_value = self.resolve_token_zglyph(clean_token)
            gloss.append(z_value if z_value else f"?{clean_token}")
        return gloss

    def parse_sentence(self, sentence):
        return {
            "original": sentence,
            "normalized": self.normalize(sentence),
            "tokens": self.tokenize(self.normalize(sentence)),
            "gloss": self.parse(sentence)
        }

# Example use
if __name__ == "__main__":
    parser = SemanticParser()
    result = parser.parse_sentence("A language designer and a theoretical physicist.")
    print(result)
