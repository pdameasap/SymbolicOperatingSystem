# modules/pdf/zglyph_parser.py

import re
import sys
import logging
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Ensure SymbolicOperatingSystem root is available
sos_root = Path(__file__).resolve().parents[2]  # Go up two levels: pdf/ -> modules/ -> SymbolicOperatingSystem/
if str(sos_root) not in sys.path:
    sys.path.insert(0, str(sos_root))

# Now safe to import
try:
    from modules.parser.symbolic_normalizer import normalize_noun
    from modules.parser.symbolic_nouns import SYMBOLIC_NOUNS
except ImportError as e:
    raise ImportError(f"Failed to import SymbolicOperatingSystem components: {e}")

# --- Z-Glyph Parsing Logic ---
def parse_text_for_zglyphs(text: str) -> Dict[str, int]:
    # Parses text to count Z-Glyphs using imported components directly.
    if not text or not isinstance(text, str):
        return {}
        
    z_summary = defaultdict(int)
    lines = text.splitlines()

    for line in lines:
        try:
            if not line.strip(): 
                continue
                
            normalized_line = re.sub(r"[^\w\s_]", "", line.lower())
            normalized_line = re.sub(r"\s+", " ", normalized_line).strip()
            
            if not normalized_line: 
                continue

            tokens = normalized_line.split()
            for token in tokens:
                try:
                    base_noun = normalize_noun(token)
                    key = f"N_{base_noun.upper()}"
                    z_entry = SYMBOLIC_NOUNS.get(key)

                    if z_entry and isinstance(z_entry, dict):
                        z_glyph = z_entry.get("Z")
                        if z_glyph and not str(z_glyph).startswith("?"):
                            z_summary[z_glyph] += 1
                except Exception:
                    continue
        except Exception:
            continue

    return dict(z_summary)

# --- Z-Glyph Sorting and Analysis ---
def zglyph_sort_key(zglyph: str) -> int:
    # Custom sort key function for Z-Glyphs to handle subscript numbers correctly.
    # Extract the numeric part after Z
    if zglyph == "Z†":
        # Special case for Z†, place it at the end
        return 999
    elif zglyph == "Z∈":
        # Special case for Z∈, place it after numbers
        return 998
    
    # For regular Z₁, Z₂, etc. - extract the number
    match = re.search(r'Z[₀₁₂₃₄₅₆₇₈₉]+', zglyph)
    if match:
        # Convert subscript digits to regular digits
        subscript_map = {
            '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4',
            '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9'
        }
        num_str = zglyph[1:]  # Remove the 'Z'
        regular_num = ''.join(subscript_map.get(c, c) for c in num_str)
        try:
            return int(regular_num)
        except ValueError:
            # If conversion fails, use string sorting as fallback
            return 500  # Middle priority
    
    # Default case
    return 500  # Middle priority

def find_most_frequent_zglyph(text: str) -> str:
    # Analyzes extracted text to find the most frequent Z-Glyph(s).
    if not text:
        return "Z?"

    try:
        z_counts = parse_text_for_zglyphs(text)
    except Exception as e:
        logger.error(f"Error during Z-Glyph parsing: {e}")
        return "Z?"

    if not z_counts:
        return "Z?"

    max_count = max(z_counts.values())
    # Use custom sorting function for Z-Glyphs to handle subscript numbers correctly
    top_zs = sorted(
        [z for z, count in z_counts.items() if count == max_count],
        key=zglyph_sort_key
    )
    
    return "".join(top_zs)

# --- Utility Functions ---
def get_zglyph_counts(text: str) -> Dict[str, int]:
    # Get counts of all Z-Glyphs in the text.
    return parse_text_for_zglyphs(text)

def get_zglyph_distribution(text: str) -> List[Tuple[str, int]]:
    # Get distribution of Z-Glyphs sorted by frequency (highest first).
    counts = parse_text_for_zglyphs(text)
    if not counts:
        return []
    
    # Sort by count (descending) and then by Z-Glyph (using custom sort)
    return sorted(
        counts.items(),
        key=lambda x: (-x[1], zglyph_sort_key(x[0]))
    )
