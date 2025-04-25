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
        result = SYMBOLIC_NOUNS.get(key)
        return result if isinstance(result, dict) else None

    def parse(self, sentence):
        norm = self.normalize(sentence)
        tokens = self.tokenize(norm)
        gloss = []
        for token in tokens:
            clean_token = token.strip(".,;:!?\"'()[]{}")
            z_entry = self.resolve_token_zglyph(clean_token)
            if z_entry:
                gloss.append({"Z": z_entry["Z"], "tag": z_entry["tag"]})
            else:
                gloss.append({"Z": None, "tag": None})
        return gloss

    def parse_sentence(self, sentence):
        return {
            "original": sentence,
            "normalized": self.normalize(sentence),
            "tokens": self.tokenize(self.normalize(sentence)),
            "gloss": self.parse(sentence)
        }
