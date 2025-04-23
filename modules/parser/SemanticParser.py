# File: modules/parser/SemanticParser.py

'''
Semantic Parser Core Module
---------------------------
This module provides the base for parsing and interpreting sentences into symbolic semantic units.
It supports sentence normalization, structural tagging, and symbolic alignment.
'''

import re

class SemanticParser:
    def __init__(self):
        # Expanded vocabulary for broader concept mapping
        self.symbol_map = {
            "programmer": "Z₁",
            "grammarian": "Z₆",
            "statistician": "Z₁₂",
            "theoretical physicist": "Z₁₁",
            "theoretical mathematician": "Z₁₃",
            "language designer": "Z₁₀",
            "elegance": "Z₅",
            "women": "Z∈",
            "friend": "Z∉",
            "companion": "Z₄",
            "warm": "Z₆+Z∇",
            "coherence": "Z₁₆",
            "desire": "Z₂",
            "truth": "Z₃",
            "identity": "Z₇",
            "expression": "Z₆",
            "change": "Z₁₂",
            "principle": "Z₁₁",
            "abstraction": "Z₁₃",
            "shape": "Z₁₀",
            "structure": "Z₁",
            "containment": "Z∈",
            "null": "Z₁₅",
            "network": "Z₄",
            "motion": "Z₂",
            "key": "Z†",
            "spiral": "Z†",
            "resonance": "Z₅",
            "mirror": "Z₈",
            "voice": "Z₆",
            "clarity": "Z₅",
            "meaning": "Z₁₆",
            "burden": "Z₇",
            "seeker": "Z₃",
            "self": "Z₇"
        }

    def normalize(self, sentence):
        # Enhanced normalization (lowercase, punctuation strip, trim extra spaces)
        cleaned = re.sub(r'[^a-z0-9\s]', '', sentence.lower())
        return re.sub(r'\s+', ' ', cleaned).strip()

    def tokenize(self, sentence):
        return sentence.split()

    def parse(self, sentence):
        norm = self.normalize(sentence)
        tokens = self.tokenize(norm)
        gloss = []
        for token in tokens:
            gloss.append(self.symbol_map.get(token, token))
        return gloss

    def parse_sentence(self, sentence):
        return {
            "original": sentence,
            "normalized": self.normalize(sentence),
            "tokens": self.tokenize(self.normalize(sentence)),
            "gloss": self.parse(sentence)
        }

# Example usage
if __name__ == "__main__":
    parser = SemanticParser()
    result = parser.parse_sentence(
        "I am in need of a programmer, a grammarian, a statistician, a theoretical physicist, "
        "a theoretical mathematician, and a language designer in the form of elegance."
    )
    print(result)
