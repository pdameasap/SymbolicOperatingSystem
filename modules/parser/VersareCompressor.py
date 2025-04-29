"""
Versare Symbolic Compressor

This module implements the symbolic compression functionality for the Versare language.
It takes text input, lemmatizes it, maps words to predefined Versare nouns or dynamically
assigns new symbols, and generates compressed output with a self-bootstrapping glossary.
"""

import re
import sys
import logging
import unicodedata
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Union, Any
from collections import Counter, defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Try to import NLTK for lemmatization
try:
    import nltk
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    from nltk.corpus import wordnet
    
    # Download required NLTK data if not already present
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)
        
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger', quiet=True)
        
    NLTK_AVAILABLE = True
except ImportError:
    logger.warning("NLTK not available. Using basic lemmatization.")
    NLTK_AVAILABLE = False

# Import SymbolicOperatingSystem modules using relative imports
try:
    from .symbolic_normalizer import normalize_noun
    from .symbolic_nouns import SYMBOLIC_NOUNS
    SOS_AVAILABLE = True
except ImportError as e:
    logger.error(f"Error importing SymbolicOperatingSystem modules: {e}")
    logger.error("Ensure symbolic_normalizer.py and symbolic_nouns.py are in the same directory.")
    SOS_AVAILABLE = False


class VersareCompressor:
    """
    Implements the Versare symbolic compression algorithm.
    """
    
    # Unicode ranges for noun allocation
    PREDEFINED_NOUN_START = 0x1D400  # Mathematical Alphanumeric Symbols
    PREDEFINED_NOUN_END = 0x1D7FF
    
    # Primary Dynamic Noun Range (BMP safe, includes general symbols, various pictographs)
    DYNAMIC_NOUN_START = 0x2000
    DYNAMIC_NOUN_END = 0xF8FF
    
    # Secondary Dynamic Noun Range (Supplementary Private Use A and B)
    SECONDARY_DYNAMIC_NOUN_START = 0xF0000
    SECONDARY_DYNAMIC_NOUN_END = 0x10FFFD
    
    def __init__(self, initial_glossary_file: Optional[str] = None, corpus_name: Optional[str] = None, debug: bool = False):
        """
        Initialize the Versare compressor.
        
        Args:
            initial_glossary_file: Optional path to a Versare file to load initial glossary from
            corpus_name: Optional name for the corpus this compressor will process
            debug: Enable debug logging
        """
        self.debug = debug
        self.corpus_name = corpus_name
        if debug:
            logger.setLevel(logging.DEBUG)
        
        # Initialize lemmatizer
        self.lemmatizer = WordNetLemmatizer() if NLTK_AVAILABLE else None
        
        # Load predefined nouns from SymbolicOperatingSystem if available
        self.predefined_nouns = {}
        self.predefined_noun_symbols = {}
        self.load_predefined_nouns()
        
        # Dictionary for dynamically allocated nouns
        self.dynamic_nouns = {}
        self.dynamic_noun_symbols = {}
        self.next_dynamic_code_point = self.DYNAMIC_NOUN_START
        
        # Z-Glyph symbols
        self.z_glyphs = {
            1: "α",    # Structure (Alpha)
            2: "∿",    # Force (Ignition)
            3: "⥀",    # Intention (Vector)
            4: "⊞",    # Network (Web)
            5: "⊗",    # Cognition (Mirror)
            6: "∞̷",    # Expression (Voice)
            7: "⧘",    # Self (Anchor)
            8: "∴",    # Containment (Vessel)
            9: "✓",    # Relation (Bridge)
            10: "⟡",   # Pattern (Echo)
            11: "ℓ",   # Stasis (Stillpoint)
            12: "∥",   # Change (Flow)
            13: "∞",   # Construction (Forge)
            14: "∅",   # Disruption (Break)
            15: "⊚",   # Null (Silence)
            16: "Ω"    # Coherence (Omega)
        }
        
        # Operators
        self.operators = {
            "define": "≜",
            "implies": "⟹",
            "maps_to": "↦",
            "evaluates": "⊢",
            "compose": "∘",
            "union": "∪",
            "intersection": "∩",
            "subset": "⊂",
            "superset": "⊃",
            "element": "∈",
            "not_element": "∉",
            "for_all": "∀",
            "exists": "∃",
            "not_exists": "∄",
            "therefore": "∴",
            "because": "∵"
        }
        
        # Load initial glossary if provided
        if initial_glossary_file:
            self.load_glossary_from_file(initial_glossary_file)
    
    def load_predefined_nouns(self) -> None:
        """
        Load predefined nouns from SymbolicOperatingSystem.
        """
        if not SOS_AVAILABLE:
            logger.warning("SymbolicOperatingSystem not available. No predefined nouns loaded.")
            return
        
        try:
            # Get nouns from SYMBOLIC_NOUNS dictionary
            code_point = self.PREDEFINED_NOUN_START
            for noun_key, noun_info in SYMBOLIC_NOUNS.items():
                # Extract the noun string (removing N_ prefix)
                if isinstance(noun_info, tuple) and len(noun_info) >= 1:
                    noun_str = noun_info[0]
                elif isinstance(noun_info, str):
                    noun_str = noun_info
                else:
                    continue
                
                # Skip if already at the end of the predefined range
                if code_point > self.PREDEFINED_NOUN_END:
                    logger.warning(f"Reached end of predefined noun range. Skipping remaining nouns.")
                    break
                
                # Assign a Unicode symbol
                symbol = chr(code_point)
                
                # Store the noun mapping
                self.predefined_nouns[noun_str.lower()] = symbol
                self.predefined_noun_symbols[symbol] = noun_str
                
                code_point += 1
            
            logger.info(f"Loaded {len(self.predefined_nouns)} predefined nouns")
        except Exception as e:
            logger.error(f"Error loading predefined nouns: {e}")
    
    def load_glossary_from_file(self, glossary_file: str) -> None:
        """
        Load glossary definitions from an existing Versare file.
        
        Args:
            glossary_file: Path to a Versare file to load glossary from
        """
        try:
            # Read the input file
            with open(glossary_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract the header
            parts = content.split("# Compressed Content\\n\\n", 1)
            if len(parts) != 2:
                logger.warning(f"Invalid Versare file format in {glossary_file}: missing header separator")
                return
            
            header = parts[0]
            
            # Parse the symbol definitions
            noun_section_started = False
            for line in header.split('\\n'):
                if "## Nouns" in line:
                    noun_section_started = True
                    continue
                
                if not noun_section_started:
                    continue
                
                if line.startswith('#') or not line.strip():
                    continue
                
                if self.operators['define'] in line:
                    parts = line.split(self.operators['define'], 1)
                    if len(parts) == 2:
                        symbol = parts[0].strip()
                        definition = parts[1].strip()
                        
                        # Skip if it's a Z-Glyph or operator
                        if any(symbol == z_symbol for z_symbol in self.z_glyphs.values()):
                            continue
                        if any(symbol == op_symbol for op_symbol in self.operators.values()):
                            continue
                        
                        # Check if it's a predefined noun
                        if definition.lower() in self.predefined_nouns:
                            # Use the predefined symbol instead
                            continue
                        
                        # Add to dynamic nouns
                        self.dynamic_nouns[definition.lower()] = symbol
                        self.dynamic_noun_symbols[symbol] = definition
                        
                        # Update next_dynamic_code_point if necessary
                        try:
                            code_point = ord(symbol)
                            if self.DYNAMIC_NOUN_START <= code_point <= self.DYNAMIC_NOUN_END:
                                self.next_dynamic_code_point = max(self.next_dynamic_code_point, code_point + 1)
                            elif self.SECONDARY_DYNAMIC_NOUN_START <= code_point <= self.SECONDARY_DYNAMIC_NOUN_END:
                                self.next_dynamic_code_point = max(self.next_dynamic_code_point, code_point + 1)
                        except (TypeError, ValueError):
                            pass
            
            logger.info(f"Loaded {len(self.dynamic_nouns)} dynamic nouns from {glossary_file}")
        except Exception as e:
            logger.error(f"Error loading glossary from file: {e}")
    
    def get_wordnet_pos(self, word: str, pos_tag: str) -> Optional[str]:
        """
        Convert POS tag to WordNet POS tag.
        
        Args:
            word: The word to get POS for
            pos_tag: The POS tag from NLTK
            
        Returns:
            WordNet POS tag or None
        """
        if not NLTK_AVAILABLE:
            return None
            
        tag_map = {
            'J': wordnet.ADJ,
            'N': wordnet.NOUN,
            'V': wordnet.VERB,
            'R': wordnet.ADV
        }
        
        return tag_map.get(pos_tag[0].upper(), None)
    
    def lemmatize_text(self, text: str) -> List[Tuple[str, str]]:
        """
        Tokenize and lemmatize text.
        
        Args:
            text: Input text to lemmatize
            
        Returns:
            List of (original_word, lemmatized_word) tuples
        """
        if not NLTK_AVAILABLE:
            # Basic tokenization and lowercase for non-NLTK fallback
            words = re.findall(r'\\b\\w+\\b', text.lower())
            return [(word, word) for word in words]
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Get POS tags
        pos_tags = nltk.pos_tag(tokens)
        
        # Lemmatize with correct POS
        lemmatized = []
        for word, pos in pos_tags:
            wordnet_pos = self.get_wordnet_pos(word, pos)
            if wordnet_pos:
                lemma = self.lemmatizer.lemmatize(word.lower(), pos=wordnet_pos)
            else:
                # Default to noun for lemmatization
                lemma = self.lemmatizer.lemmatize(word.lower(), pos=wordnet.NOUN)
            
            lemmatized.append((word, lemma))
        
        return lemmatized
    
    def get_or_create_noun_symbol(self, lemma: str) -> str:
        """
        Get the symbol for a noun, creating a new one if it doesn't exist.
        
        Args:
            lemma: Lemmatized noun
            
        Returns:
            Unicode symbol for the noun
        """
        # Check if it's a predefined noun
        if lemma.lower() in self.predefined_nouns:
            return self.predefined_nouns[lemma.lower()]
        
        # Check if it's already a dynamically allocated noun
        if lemma.lower() in self.dynamic_nouns:
            return self.dynamic_nouns[lemma.lower()]
        
        # Allocate a new symbol
        if self.next_dynamic_code_point <= self.DYNAMIC_NOUN_END:
            symbol = chr(self.next_dynamic_code_point)
            self.dynamic_nouns[lemma.lower()] = symbol
            self.dynamic_noun_symbols[symbol] = lemma
            self.next_dynamic_code_point += 1
            return symbol

        if self.DYNAMIC_NOUN_END < self.next_dynamic_code_point < self.SECONDARY_DYNAMIC_NOUN_START:
            # Jump to Secondary Dynamic Range
            self.next_dynamic_code_point = self.SECONDARY_DYNAMIC_NOUN_START

        if self.SECONDARY_DYNAMIC_NOUN_START <= self.next_dynamic_code_point <= self.SECONDARY_DYNAMIC_NOUN_END:
            symbol = chr(self.next_dynamic_code_point)
            self.dynamic_nouns[lemma.lower()] = symbol
            self.dynamic_noun_symbols[symbol] = lemma
            self.next_dynamic_code_point += 1
            return symbol

        logger.error(f"Ran out of Unicode code points for dynamic nouns. Using fallback.")
        # Fallback: use the lemma itself
        return lemma
    
    def compress_text(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Compress text using Versare symbolic language.
        
        Args:
            text: Input text to compress
            
        Returns:
            Tuple of (compressed_text, symbol_definitions)
        """
        # Lemmatize the text
        lemmatized = self.lemmatize_text(text)
        
        # Track which symbols are used
        used_symbols = set()
        
        # Compress the text
        compressed = []
        current_pos = 0
        
        for original, lemma in lemmatized:
            # Find the position of the original word in the text
            start_pos = text.find(original, current_pos)
            if start_pos > current_pos:
                # Add any non-word characters between the last word and this one
                compressed.append(text[current_pos:start_pos])
            
            # Get the symbol for this lemma
            symbol = self.get_or_create_noun_symbol(lemma)
            compressed.append(symbol)
            used_symbols.add(symbol)
            
            # Update current position
            current_pos = start_pos + len(original)
        
        # Add any remaining text
        if current_pos < len(text):
            compressed.append(text[current_pos:])
        
        # Create the compressed text
        compressed_text = ''.join(compressed)
        
        # Create the symbol definitions
        symbol_definitions = {}
        for symbol in used_symbols:
            if symbol in self.predefined_noun_symbols:
                symbol_definitions[symbol] = self.predefined_noun_symbols[symbol]
            elif symbol in self.dynamic_noun_symbols:
                symbol_definitions[symbol] = self.dynamic_noun_symbols[symbol]
        
        return compressed_text, symbol_definitions
    
    def create_bootstrap_header(self, symbol_definitions: Dict[str, str]) -> str:
        """
        Create a self-bootstrapping header with symbol definitions.
        
        Args:
            symbol_definitions: Dictionary mapping symbols to their definitions
            
        Returns:
            Header text with symbol definitions
        """
        header = "# Versare Symbolic Language Definitions\\n\\n"
        
        # Add corpus information if available
        if self.corpus_name:
            header += f"Corpus: {self.corpus_name}\\n\\n"
        
        # Add Z-Glyph definitions
        header += "## Z-Glyphs\\n\\n"
        for index, symbol in self.z_glyphs.items():
            header += f"{symbol} {self.operators['define']} Z{index}\\n"
        
        header += "\\n## Operators\\n\\n"
        for name, symbol in self.operators.items():
            header += f"{symbol} {self.operators['define']} {name}\\n"
        
        header += "\\n## Nouns\\n\\n"
        
        # First add predefined nouns that are used
        predefined_symbols = {s: d for s, d in symbol_definitions.items() if s in self.predefined_noun_symbols}
        if predefined_symbols:
            header += "### Predefined\\n\\n"
            for symbol, definition in sorted(predefined_symbols.items()):
                header += f"{symbol} {self.operators['define']} {definition}\\n"
            header += "\\n"
        
        # Then add dynamic nouns
        dynamic_symbols = {s: d for s, d in symbol_definitions.items() if s in self.dynamic_noun_symbols}
        if dynamic_symbols:
            header += "### Dynamic\\n\\n"
            for symbol, definition in sorted(dynamic_symbols.items()):
                header += f"{symbol} {self.operators['define']} {definition}\\n"
        
        header += "\\n# Compressed Content\\n\\n"
        return header
    
    def compress_file(self, input_file: str, output_file: Optional[str] = None) -> str:
        """
        Compress a text file using Versare symbolic language.
        
        Args:
            input_file: Path to input text file
            output_file: Optional path to output file
            
        Returns:
            Path to the output file
        """
        try:
            # Read the input file
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Compress the text
            compressed_text, symbol_definitions = self.compress_text(text)
            
            # Create the bootstrap header
            header = self.create_bootstrap_header(symbol_definitions)
            
            # Combine header and compressed text
            full_output = header + compressed_text
            
            # Determine output file path
            if output_file is None:
                input_path = Path(input_file)
                output_file = str(input_path.with_suffix('.versare'))
            
            # Write the output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_output)
            
            compression_ratio = len(compressed_text) / len(text) if len(text) > 0 else 0
            logger.info(f"Compressed {input_file} to {output_file}")
            logger.info(f"Original size: {len(text)} characters")
            logger.info(f"Compressed size: {len(compressed_text)} characters")
            logger.info(f"Compression ratio: {compression_ratio:.2f}")
            
            return output_file
        except Exception as e:
            logger.error(f"Error compressing file: {e}")
            raise
    
    def decompress_text(self, compressed_text: str, symbol_definitions: Dict[str, str]) -> str:
        """
        Decompress Versare symbolic text back to natural language.
        
        Args:
            compressed_text: Compressed text
            symbol_definitions: Dictionary mapping symbols to their definitions
            
        Returns:
            Decompressed text
        """
        # Create a reverse mapping for quick lookup
        reverse_mapping = {symbol: definition for symbol, definition in symbol_definitions.items()}
        
        # Replace symbols with their definitions
        decompressed = compressed_text
        for symbol, definition in reverse_mapping.items():
            decompressed = decompressed.replace(symbol, definition)
        
        return decompressed
    
    def decompress_file(self, input_file: str, output_file: Optional[str] = None) -> str:
        """
        Decompress a Versare symbolic file back to natural language.
        
        Args:
            input_file: Path to input Versare file
            output_file: Optional path to output file
            
        Returns:
            Path to the output file
        """
        try:
            # Read the input file
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract the header and compressed content
            parts = content.split("# Compressed Content\\n\\n", 1)
            if len(parts) != 2:
                raise ValueError("Invalid Versare file format: missing header separator")
            
            header, compressed_text = parts
            
            # Parse the symbol definitions
            symbol_definitions = {}
            noun_section_started = False
            
            for line in header.split('\\n'):
                if "## Nouns" in line:
                    noun_section_started = True
                    continue
                
                if not noun_section_started:
                    continue
                
                if line.startswith('#') or not line.strip():
                    continue
                
                if self.operators['define'] in line:
                    parts = line.split(self.operators['define'], 1)
                    if len(parts) == 2:
                        symbol = parts[0].strip()
                        definition = parts[1].strip()
                        symbol_definitions[symbol] = definition
            
            # Decompress the text
            decompressed_text = self.decompress_text(compressed_text, symbol_definitions)
            
            # Determine output file path
            if output_file is None:
                input_path = Path(input_file)
                output_file = str(input_path.with_suffix('.decompressed.txt'))
            
            # Write the output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(decompressed_text)
            
            logger.info(f"Decompressed {input_file} to {output_file}")
            
            return output_file
        except Exception as e:
            logger.error(f"Error decompressing file: {e}")
            raise
    
    def extract_glossary(self, versare_file: str, output_file: Optional[str] = None) -> str:
        """
        Extract just the glossary section from a Versare file.
        
        Args:
            versare_file: Path to input Versare file
            output_file: Optional path to output glossary file
            
        Returns:
            Path to the output glossary file
        """
        try:
            # Read the input file
            with open(versare_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract the header
            parts = content.split("# Compressed Content\\n\\n", 1)
            if len(parts) != 2:
                raise ValueError("Invalid Versare file format: missing header separator")
            
            header = parts[0]
            
            # Determine output file path
            if output_file is None:
                input_path = Path(versare_file)
                output_file = str(input_path.with_suffix('.glossary'))
            
            # Write the glossary file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(header)
            
            logger.info(f"Extracted glossary from {versare_file} to {output_file}")
            
            return output_file
        except Exception as e:
            logger.error(f"Error extracting glossary: {e}")
            raise
    
    def merge_glossaries(self, glossary_files: List[str], output_file: Optional[str] = None) -> str:
        """
        Merge multiple glossary files into a single comprehensive glossary.
        
        Args:
            glossary_files: List of paths to glossary files
            output_file: Optional path to output merged glossary file
            
        Returns:
            Path to the output merged glossary file
        """
        try:
            # Create a new compressor to hold the merged glossary
            merged_compressor = VersareCompressor(corpus_name=self.corpus_name, debug=self.debug)
            
            # Load each glossary file
            for glossary_file in glossary_files:
                merged_compressor.load_glossary_from_file(glossary_file)
            
            # Create a dummy symbol definitions dictionary with all dynamic nouns
            symbol_definitions = {
                symbol: definition for symbol, definition in merged_compressor.dynamic_noun_symbols.items()
            }
            
            # Create the bootstrap header
            header = merged_compressor.create_bootstrap_header(symbol_definitions)
            
            # Determine output file path
            if output_file is None:
                output_file = "merged_glossary.versare"
            
            # Write the merged glossary file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(header)
            
            logger.info(f"Merged {len(glossary_files)} glossaries into {output_file}")
            logger.info(f"Total dynamic nouns: {len(merged_compressor.dynamic_nouns)}")
            
            return output_file
        except Exception as e:
            logger.error(f"Error merging glossaries: {e}")
            raise

# Add a method to VersareCompressor to simplify saving
def compress_text_and_save(self, text: str, output_file: str):
    """
    Compress text and save directly to a file.

    Args:
        text: Input text to compress.
        output_file: Path to the output Versare file.
    """
    compressed_text, symbol_definitions = self.compress_text(text)
    header = self.create_bootstrap_header(symbol_definitions)
    full_output = header + compressed_text
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_output)
        
    compression_ratio = len(compressed_text) / len(text) if len(text) > 0 else 0
    logger.info(f"Saved compressed output to {output_file}")
    logger.debug(f"Original size: {len(text)} chars, Compressed: {len(compressed_text)} chars, Ratio: {compression_ratio:.2f}")

# Monkey-patch the method onto the class
VersareCompressor.compress_text_and_save = compress_text_and_save

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Versare Symbolic Compressor')
    parser.add_argument('input_file', help='Input file to process')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--decompress', '-d', action='store_true', help='Decompress instead of compress')
    parser.add_argument('--extract-glossary', '-g', action='store_true', help='Extract glossary from a Versare file')
    parser.add_argument('--initial-glossary', '-i', help='Path to initial glossary file to load')
    parser.add_argument('--corpus', help='Name of the corpus this file belongs to')
    parser.add_argument('--merge-glossaries', '-m', nargs='+', help='Merge multiple glossary files')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    # Handle glossary merging separately
    if args.merge_glossaries:
        compressor = VersareCompressor(corpus_name=args.corpus, debug=args.debug)
        output_file = compressor.merge_glossaries(args.merge_glossaries, args.output)
        print(f"Merged glossary saved to: {output_file}")
        return 0
    
    # Create compressor with initial glossary if specified
    compressor = VersareCompressor(
        initial_glossary_file=args.initial_glossary,
        corpus_name=args.corpus,
        debug=args.debug
    )
    
    try:
        if args.extract_glossary:
            output_file = compressor.extract_glossary(args.input_file, args.output)
            print(f"Extracted glossary saved to: {output_file}")
        elif args.decompress:
            output_file = compressor.decompress_file(args.input_file, args.output)
            print(f"Decompressed file saved to: {output_file}")
        else:
            output_file = compressor.compress_file(args.input_file, args.output)
            print(f"Compressed file saved to: {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
