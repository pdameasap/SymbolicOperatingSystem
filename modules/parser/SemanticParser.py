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
            clean_token = token.strip(".,;:!?\"'()[]{}")  # Strip punctuation
            z_entry = self.resolve_token_zglyph(clean_token)
            gloss.append(z_entry["Z"] if z_entry else f"?{clean_token}")
        return gloss

    def parse_sentence(self, sentence):
        tokens = self.tokenize(self.normalize(sentence))
        gloss = self.parse(sentence)
        tagged = []
        for token, gloss_item in zip(tokens, gloss):
            z_value = None
            tag_value = None
            if not gloss_item.startswith("?"):
                base = normalize_noun(token)
                key = f"N_{base.upper()}"
                entry = SYMBOLIC_NOUNS.get(key)
                if entry:
                    z_value = entry.get("Z")
                    tag_value = entry.get("tag")
            tagged.append({"word": token, "Z": z_value, "tag": tag_value})
        return {
            "original": sentence,
            "normalized": self.normalize(sentence),
            "tokens": tokens,
            "gloss": gloss,
            "tagged": tagged
        }