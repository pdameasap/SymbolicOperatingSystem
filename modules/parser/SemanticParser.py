# File: modules/parser/SemanticParser.py

import re
from modules.parser.symbolic_nouns import SYMBOLIC_NOUNS
from modules.parser.symbolic_normalizer import normalize_noun

class SemanticParser:

    def normalize(self, sentence):
        # Lowercase, remove punctuation but preserve underscores
        sentence = re.sub(r'[^\w\s]', '', sentence.lower())
        print(f"[DEBUG] normalize: '{sentence}'")
        return re.sub(r'\s+', ' ', sentence).strip()

    def tokenize(self, sentence):
        tokens = sentence.split()
        cleaned_tokens = [t.strip(".,;:!?\"'()[]{}") for t in tokens]
        print(f"[DEBUG] tokenize: raw='{tokens}' cleaned='{cleaned_tokens}'")
        return cleaned_tokens

    def resolve_token_zglyph(self, word):
        base = normalize_noun(word)
        key = f"N_{base.upper()}"
        result = SYMBOLIC_NOUNS.get(key, None)
        print(f"[DEBUG] resolve_token_zglyph: word='{word}' base='{base}' key='{key}' result='{result}'")
        return result

    def parse(self, sentence):
        norm = self.normalize(sentence)
        tokens = self.tokenize(norm)
        gloss = []
        for token in tokens:
            z_entry = self.resolve_token_zglyph(token)
            gloss.append(z_entry[1] if z_entry else f"?{token}")
        print(f"[DEBUG] parse: gloss='{gloss}'")
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
        print(f"[DEBUG] parse_sentence: {result}")
        return result

# Example use
if __name__ == "__main__":
    parser = SemanticParser()
    result = parser.parse_sentence("A language designer and a theoretical physicist.")
    print(result)
