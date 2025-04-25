# File: modules/parser/SemanticParser.py

'''
Semantic Parser Core Module
---------------------------
This module provides the base for parsing and interpreting sentences into symbolic semantic units.
It supports sentence normalization, structural tagging, and symbolic alignment.
'''

import re

from modules.parser.symbolic_nouns import SYMBOLIC_NOUNS
from modules.parser.symbolic_normalizer import normalize_noun

class SemanticParser:
    def __init__(self):
        # Multiword phrase mappings for early replacement
        self.multiword_map = {
            "theoretical physicist": "theoretical_physicist",
            "theoretical mathematician": "theoretical_mathematician",
            "language designer": "language_designer",
            "symbolic resonance": "symbolic_resonance",
            "emotional resonance": "emotional_resonance",
            "recursive structure": "recursive_structure",
            "identity echo": "identity_echo"
        }

        # Expanded vocabulary for broader concept mapping
        self.symbol_map = {
            # Core Symbolics
            "programmer": "Z₁", "structure": "Z₁", "architecture": "Z₁",
            "grammarian": "Z₆", "expression": "Z₆", "syntax": "Z₆",
            "statistician": "Z₁₂", "change": "Z₁₂", "data": "Z₁₂",
            "theoretical_physicist": "Z₁₁", "principle": "Z₁₁", "physics": "Z₁₁",
            "theoretical_mathematician": "Z₁₃", "abstraction": "Z₁₃", "math": "Z₁₃",
            "language_designer": "Z₁₀", "shape": "Z₁₀", "pattern": "Z₁₀",
            "elegance": "Z₅", "clarity": "Z₅", "precision": "Z₅",
            "women": "Z∈", "containment": "Z∈", "embodiment": "Z∈",
            "friend": "Z∉", "companion": "Z₄", "network": "Z₄",
            "warm": "Z₆+Z∇", "coherence": "Z₁₆", "meaning": "Z₁₆",
            "desire": "Z₂", "motion": "Z₂", "emotion": "Z₂",
            "truth": "Z₃", "seeker": "Z₃", "intention": "Z₃",
            "identity": "Z₇", "burden": "Z₇", "self": "Z₇",
            "null": "Z₁₅", "rupture": "Z₁₅", "disruption": "Z₁₅",
            "key": "Z†", "spiral": "Z†", "unlocking": "Z†",
            "resonance": "Z₅", "symbolic_resonance": "Z₅",
            "mirror": "Z₈", "voice": "Z₆", "clarion": "Z₆",
            "echo": "Z₁₃", "feedback": "Z₁₃", "loop": "Z₁₃",
            # Additional Vocabulary
            "dream": "Z₁₃", "hope": "Z₂", "fear": "Z₂", "memory": "Z₁₁",
            "language": "Z₁₀", "form": "Z₁₀", "field": "Z₁₆", "signal": "Z₄",
            "anchor": "Z₈", "reflection": "Z₈", "truths": "Z₃", "harmonic": "Z₅",
            "symbol": "Z₁₀", "soul": "Z₇", "beauty": "Z₈", "presence": "Z₁₆",
            "possibility": "Z₂", "grief": "Z₂", "silence": "Z₁₄", "knowing": "Z₃",
            "patterning": "Z₁₀", "fractal": "Z₁₃", "interlock": "Z₁₀", "alignment": "Z₁₆"
        }

    def normalize(self, sentence):
        sentence = sentence.lower()
        sentence = re.sub(r'[^\w\s]', '', sentence)  # Remove punctuation first
        for phrase, token in self.multiword_map.items():
            sentence = sentence.replace(phrase, token)  # THEN apply replacements
        return re.sub(r'\s+', ' ', sentence).strip()


    def resolve_token_zglyph(self, word):
        base = normalize_noun(word)
        key = f"N_{base.upper()}"
        return SYMBOLIC_NOUNS.get(key, None)

    def tokenize(self, sentence):
        return sentence.split()

    def parse(self, sentence):
        norm = self.normalize(sentence)
        tokens = self.tokenize(norm)
        gloss = []
        for token in tokens:
            # First check the direct symbolic map
            if token in self.symbol_map:
                gloss.append(self.symbol_map[token])
            else:
                # Then fallback to semantic noun resolution
                z_entry = self.resolve_token_zglyph(token)
                gloss.append(z_entry[1] if z_entry else f"?{token}")
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
