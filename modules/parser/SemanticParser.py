# File: modules/parser/SemanticParser.py

import re
from modules.parser.symbolic_nouns import SYMBOLIC_NOUNS
from modules.parser.symbolic_normalizer import normalize_noun

class SemanticParser:
    def __init__(self):
        self.symbol_map = {
            # Core Symbolics (sorted alphabetically for readability)
            "abstraction": "Z₁₃", "anchor": "Z₈", "architecture": "Z₁",
            "beauty": "Z₈", "burden": "Z₇", "change": "Z₁₂",
            "clarion": "Z₆", "clarity": "Z₅", "coherence": "Z₁₆",
            "companion": "Z₄", "containment": "Z∈", "data": "Z₁₂",
            "designer": "Z₁₀", "desire": "Z₂", "disruption": "Z₁₅",
            "dream": "Z₁₃", "echo": "Z₁₃", "elegance": "Z₅",
            "embodiment": "Z∈", "emotion": "Z₂", "expression": "Z₆",
            "fear": "Z₂", "feedback": "Z₁₃", "field": "Z₁₆",
            "form": "Z₁₀", "fractals": "Z₁₃", "friend": "Z∉",
            "grammarian": "Z₆", "grief": "Z₂", "harmonic": "Z₅",
            "hope": "Z₂", "identity": "Z₇", "important": "Z₁₆",
            "intention": "Z₃", "interlock": "Z₁₀", "key": "Z†",
            "language": "Z₁₀", "math": "Z₁₃", "mathematician": "Z₁₃",
            "meaning": "Z₁₆", "memory": "Z₁₁", "mirror": "Z₈",
            "motion": "Z₂", "network": "Z₄", "null": "Z₁₅",
            "pattern": "Z₁₀", "patterning": "Z₁₀", "physicist": "Z₁₁",
            "possibility": "Z₂", "precision": "Z₅", "presence": "Z₁₆",
            "principle": "Z₁₁", "programmer": "Z₁", "reflection": "Z₈",
            "resonance": "Z₅", "rupture": "Z₁₅", "self": "Z₇",
            "seeker": "Z₃", "shape": "Z₁₀", "signal": "Z₄",
            "silence": "Z₁₄", "soul": "Z₇", "spiral": "Z†",
            "statistician": "Z₁₂", "structure": "Z₁", "symbol": "Z₁₀",
            "symbolic_resonance": "Z₅", "syntax": "Z₆", "theoretical": "Z₁₁",
            "truth": "Z₃", "truths": "Z₃", "unlocking": "Z†",
            "voice": "Z₆", "warm": "Z₆+Z∇", "warmth": "Z₆",
            "women": "Z∈"
        }

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
            if token in self.symbol_map:
                gloss.append(self.symbol_map[token])
            else:
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

# Example use
if __name__ == "__main__":
    parser = SemanticParser()
    result = parser.parse_sentence("A language designer and a theoretical physicist.")
    print(result)
