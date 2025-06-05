# frameworks/compression.py

"""
compression.py

Utility for compressing free-form text into PICL expressions by
assigning high-frequency term aliases using Greek glyphs and marking the
start/end of the definitions block with labeled markers (--A--/--B--).
"""
import re
from collections import Counter

def compress_text_to_picl(text: str, top_n: int = 15, min_token_length: int = 3) -> str:
    """
    Compresses text into PICL by:
      1. Identifying top_n frequent tokens of length >= min_token_length
      2. Assigning each a unique Greek glyph not already in the source
      3. Building a DEFINITIONS block delimited with labeled markers
      4. Replacing occurrences in the text

    Args:
        text: Original text to compress.
        top_n: Number of high-frequency tokens to alias.
        min_token_length: Minimum token length to consider.

    Returns:
        A PICL-formatted string with definitions and compressed body,
        or the original text if no aliases are generated.
    """
    # Tokenize and filter by token length
    tokens = re.findall(r"\b\w+\b", text)
    filtered = [t.lower() for t in tokens if len(t) >= min_token_length]

    # Count frequencies and select top terms
    freq = Counter(filtered)
    most_common = [term for term, _ in freq.most_common(top_n)]

    # If there’s nothing to replace, return the original text unchanged
    if not most_common:
        return text

    # Define Greek glyph pool
    glyphs = [
        'α','β','γ','δ','ε','ζ','η','θ','ι','κ',
        'λ','μ','ν','ξ','π','ρ','σ','τ','υ','φ'
    ]
    # Detect existing Greek letters in source to avoid collisions
    existing_glyphs = set(re.findall(r"[\u0370-\u03FF]", text))
    available_glyphs = [g for g in glyphs if g not in existing_glyphs]

    # Truncate if not enough glyphs
    if len(available_glyphs) < len(most_common):
        most_common = most_common[:len(available_glyphs)]

    # Map terms → glyphs
    term_to_glyph = {term: available_glyphs[i] for i, term in enumerate(most_common)}

    # Build definitions block
    definitions = ["--A--"]
    for term, glyph in term_to_glyph.items():
        definitions.append(f"≜ {glyph} = {term}")
    definitions.append("--B--")

    # Replacement
    pattern = re.compile(r"\b(\w{%d,})\b" % min_token_length, re.IGNORECASE)
    def repl(m):
        w = m.group(1)
        return term_to_glyph.get(w.lower(), w)
    compressed = pattern.sub(repl, text)

    return "\n".join(definitions) + "\n\n" + compressed
