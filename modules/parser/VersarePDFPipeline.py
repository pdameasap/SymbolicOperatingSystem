"""
Versare PDF Processing Pipeline

This script integrates the PDF text extraction pipeline with the Versare symbolic compressor.
It processes PDFs in a specified directory, extracts their text, compresses the text using
the Versare language, and saves the output with a self-bootstrapping glossary.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Import necessary modules using relative imports
try:
    from .VersareCompressor import VersareCompressor
    from ..pdf_pipeline_modular.pdf_processor import extract_text_from_pdf
except ImportError as e:
    logger.error(f"Error importing required modules: {e}")
    logger.error("Please ensure VersareCompressor.py and pdf_pipeline_modular are in the correct locations.")
    sys.exit(1)

def run_versare_pipeline(pdf_dir: str, output_dir: str, corpus_name: Optional[str] = None, incremental_glossary: bool = False, debug: bool = False):
    """
    Run the full PDF to Versare compression pipeline.

    Args:
        pdf_dir: Directory containing PDF files.
        output_dir: Directory to save compressed Versare files.
        corpus_name: Optional name for the corpus.
        incremental_glossary: Whether to use incremental glossary building.
        debug: Enable debug logging.
    """
    if debug:
        logger.setLevel(logging.DEBUG)

    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 1. Extract text from PDFs
    logger.info(f"Starting PDF text extraction from: {pdf_dir}")
    
    pdf_files = sorted(list(Path(pdf_dir).glob("*.pdf")))
    if not pdf_files:
        logger.error(f"No PDF files found in {pdf_dir}")
        return

    logger.info(f"Found {len(pdf_files)} PDF files to process.")

    # 2. Initialize Versare Compressor
    initial_glossary_file = None
    compressor = None # Initialize outside the loop if not incremental

    # 3. Process each PDF
    for i, pdf_path in enumerate(pdf_files):
        logger.info(f"Processing PDF {i+1}/{len(pdf_files)}: {pdf_path.name}")
        
        try:
            # Extract text from PDF using the existing pdf_processor module
            text_content = extract_text_from_pdf(str(pdf_path))
            if not text_content or text_content.strip() == "":
                logger.warning(f"No text content extracted from {pdf_path.name}")
                text_content = f"[Empty content from {pdf_path.name}]"
            logger.debug(f"Extracted text: {text_content[:100]}...")
        except Exception as e:
            logger.error(f"Failed to extract text from {pdf_path.name}: {e}")
            continue

        # Initialize or update compressor for incremental glossary
        if incremental_glossary:
            compressor = VersareCompressor(
                initial_glossary_file=initial_glossary_file,
                corpus_name=corpus_name,
                debug=debug
            )
        elif compressor is None: # Initialize once if not incremental
             compressor = VersareCompressor(
                corpus_name=corpus_name,
                debug=debug
            )

        # Define output file path
        output_filename = pdf_path.stem + ".versare"
        output_filepath = Path(output_dir) / output_filename

        # Compress the text
        try:
            logger.info(f"Compressing text to {output_filepath}")
            compressor.compress_text_and_save(text_content, str(output_filepath))
            
            # Update initial glossary for the next iteration if incremental
            if incremental_glossary:
                initial_glossary_file = str(output_filepath)
                logger.debug(f"Using {output_filepath} as initial glossary for next file.")

        except Exception as e:
            logger.error(f"Failed to compress {pdf_path.name}: {e}")
            continue

    logger.info("Versare PDF pipeline finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Versare PDF Compression Pipeline')
    parser.add_argument('pdf_dir', help='Directory containing PDF files')
    parser.add_argument('--output-dir', '-o', default='./versare_output', help='Directory to save compressed Versare files')
    parser.add_argument('--corpus', help='Name of the corpus')
    parser.add_argument('--incremental', action='store_true', help='Build glossary incrementally across files')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    run_versare_pipeline(
        pdf_dir=args.pdf_dir,
        output_dir=args.output_dir,
        corpus_name=args.corpus,
        incremental_glossary=args.incremental,
        debug=args.debug
    )
