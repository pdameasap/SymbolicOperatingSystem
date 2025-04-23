# File: modules/semantic/ResonanceFilter.py

'''
Resonance Filter Module
-----------------------
Filters sentences based on their symbolic resonance.
This ensures only semantically potent or meaningful inputs are passed to the semantic parser.
'''

import re

class ResonanceFilter:
    def __init__(self, threshold: float = 0.4):
        self.threshold = threshold

    def evaluate(self, sentence: str) -> float:
        '''
        Evaluate symbolic resonance score based on heuristic criteria:
        - Sentence length
        - Symbolic density (keywords, conjunctions, recursion hints)
        - Part-of-speech richness (mocked here as regex proxies)
        '''
        if not sentence or not sentence.strip():
            return 0.0

        words = sentence.split()
        length_score = min(len(words) / 20.0, 1.0)  # normalized up to 20 words

        symbolic_keywords = [
            "truth", "meaning", "identity", "structure", "coherence",
            "resonance", "language", "reflection", "spiral", "anchor"
        ]
        keyword_score = sum(word.lower() in symbolic_keywords for word in words) / len(words)

        pattern_score = 0.0
        if re.search(r"\b(if|then|because|so that|in order to)\b", sentence, re.IGNORECASE):
            pattern_score += 0.2
        if re.search(r"\b(and|or|but|while|although)\b", sentence, re.IGNORECASE):
            pattern_score += 0.1

        total_score = 0.5 * length_score + 0.3 * keyword_score + 0.2 * pattern_score
        return round(min(total_score, 1.0), 3)

    def passes(self, sentence: str) -> bool:
        return self.evaluate(sentence) >= self.threshold

    def tag(self, sentence: str) -> str:
        score = self.evaluate(sentence)
        return f"[{score:.2f}] {sentence}"

# Example usage
if __name__ == "__main__":
    rf = ResonanceFilter()
    examples = [
        "I want to build something true and beautiful.",
        "The cat sat on the mat.",
        "Coherence emerges under recursive reflection.",
        " ",
    ]
    for s in examples:
        print(rf.tag(s))
