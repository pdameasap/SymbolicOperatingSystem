# File: modules/parser/SemanticParser.py

import re
from modules.parser.symbolic_nouns import SYMBOLIC_NOUNS
from modules.parser.symbolic_normalizer import normalize_noun

class SemanticParser:
    def __init__(self):
        self.symbol_map = {
            "theoretical": "Z₁₁", "physicist": "Z₁₁", "mathematician": "Z₁₃",
            "language": "Z₁₀", "designer": "Z₁₀", "programmer": "Z₁",
            "structure": "Z₁", "architecture": "Z₁", "grammarian": "Z₆",
            "expression": "Z₆", "syntax": "Z₆", "statistician": "Z₁₂",
            "change": "Z₁₂", "data": "Z₁₂", "principle": "Z₁₁",
            "physics": "Z₁₁", "abstraction": "Z₁₃", "math": "Z₁₃",
            "shape": "Z₁₀", "pattern": "Z₁₀",
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
            "dream": "Z₁₃", "hope": "Z₂", "fear": "Z₂", "memory": "Z₁₁",
            "form": "Z₁₀", "field": "Z₁₆", "signal": "Z₄",
            "anchor": "Z₈", "reflection": "Z₈", "truths": "Z₃", "harmonic": "Z₅",
            "symbol": "Z₁₀", "soul": "Z₇", "beauty": "Z₈", "presence": "Z₁₆",
            "possibility": "Z₂", "grief": "Z₂", "silence": "Z₁₄", "knowing": "Z₃",
            "patterning": "Z₁₀", "fractal": "Z₁₃", "interlock": "Z₁₀", "alignment": "Z₁₆"
        }

    def normalize(self, sentence):
        return re.sub(r'\s+', ' ', sentence.lower()).strip()

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
            base_token = token.strip(",.?!:;\"'")
            if base_token in self.symbol_map:
                gloss.append(self.symbol_map[base_token])
            else:
                z_entry = self.resolve_token_zglyph(base_token)
                gloss.append(z_entry[1] if z_entry else f"?{token}")
        return gloss

    def parse_sentence(self, sentence):
        return {
            "original": sentence,
            "normalized": self.normalize(sentence),
            "tokens": self.tokenize(self.normalize(sentence)),
            "gloss": self.parse(sentence)
        }

# Optional test
if __name__ == "__main__":
    parser = SemanticParser()
    result = parser.parse_sentence("A language designer and a theoretical physicist.")
    print(result)
