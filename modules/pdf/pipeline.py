# pdf_pipeline_modular/pipeline.py

import os
import time
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import our modules
from pdf.pdf_processor import extract_text_from_pdf
from pdf.zglyph_parser import find_most_frequent_zglyph, get_zglyph_distribution

logger = logging.getLogger(__name__)

def process_single_pdf(pdf_file: Path) -> Tuple[str, str]:
    """Process a single PDF file and return filename and Z-Glyph result."""
    logger.info(f"Processing: {pdf_file.name}")
    start_time = time.time()
    
    try:
        extracted_text = extract_text_from_pdf(pdf_file)
        if extracted_text is not None:
            logger.info(f"Parsing Z-Glyphs for {pdf_file.name}")
            most_frequent_glyph = find_most_frequent_zglyph(extracted_text)
            processing_time = time.time() - start_time
            logger.info(f"Completed {pdf_file.name} in {processing_time:.2f}s")
            return pdf_file.name, most_frequent_glyph
        else:
            logger.warning(f"Text extraction failed for {pdf_file.name}")
            return pdf_file.name, "Z?"
    except Exception as e:
        logger.error(f"Unexpected error processing {pdf_file.name}: {type(e).__name__} - {e}")
        return pdf_file.name, "Z?"

def process_pdf_directory(directory_path: str, parallel: bool = True, max_workers: int = 4) -> Dict[str, str]:
    """
    Processes all PDFs in a directory: extracts text, finds Z-Glyphs.
    
    Args:
        directory_path: Path to directory containing PDF files
        parallel: Whether to process files in parallel
        max_workers: Maximum number of worker threads for parallel processing
        
    Returns:
        Dictionary mapping filenames to their most frequent Z-Glyphs
    """
    start_time = time.time()
    pdf_dir = Path(directory_path)
    
    if not pdf_dir.is_dir():
        logger.error(f"'{directory_path}' is not a valid directory.")
        return {}

    logger.info(f"Processing PDFs in: {pdf_dir}")

    try:
        pdf_files = sorted(list(pdf_dir.glob("*.pdf")))
    except Exception as e:
        logger.error(f"Error scanning directory: {e}")
        return {}
        
    if not pdf_files:
        logger.warning(f"No PDF files found in '{directory_path}'.")
        return {}

    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    results_dict = {} # Use dict to store results for sorting by filename later
    
    if parallel and len(pdf_files) > 1:
        actual_workers = min(max_workers, len(pdf_files))
        logger.info(f"Processing {len(pdf_files)} files using {actual_workers} parallel workers")
        with ThreadPoolExecutor(max_workers=actual_workers) as executor:
            future_to_pdf = {executor.submit(process_single_pdf, pdf_file): pdf_file for pdf_file in pdf_files}
            for future in as_completed(future_to_pdf):
                pdf_file = future_to_pdf[future]
                try:
                    filename, zglyph = future.result()
                    results_dict[filename] = zglyph
                except Exception as exc:
                    logger.error(f"PDF {pdf_file.name} generated an exception: {exc}")
                    results_dict[pdf_file.name] = "Z?"
    else:
        logger.info("Processing files sequentially")
        for pdf_file in pdf_files:
            filename, zglyph = process_single_pdf(pdf_file)
            results_dict[filename] = zglyph

    # Log completion
    total_time = time.time() - start_time
    logger.info(f"--- Completed processing {len(pdf_files)} files in {total_time:.2f}s ---")
    
    return results_dict

def get_detailed_analysis(directory_path: str, output_file: str = None) -> Dict[str, List[Tuple[str, int]]]:
    """
    Perform detailed Z-Glyph analysis on all PDFs in a directory.
    
    Args:
        directory_path: Path to directory containing PDF files
        output_file: Optional file to write detailed results
        
    Returns:
        Dictionary mapping filenames to their Z-Glyph distributions
    """
    pdf_dir = Path(directory_path)
    if not pdf_dir.is_dir():
        logger.error(f"'{directory_path}' is not a valid directory.")
        return {}
        
    pdf_files = sorted(list(pdf_dir.glob("*.pdf")))
    if not pdf_files:
        logger.warning(f"No PDF files found in '{directory_path}'.")
        return {}
        
    detailed_results = {}
    
    for pdf_file in pdf_files:
        try:
            extracted_text = extract_text_from_pdf(pdf_file)
            if extracted_text is not None:
                distribution = get_zglyph_distribution(extracted_text)
                detailed_results[pdf_file.name] = distribution
            else:
                detailed_results[pdf_file.name] = []
        except Exception as e:
            logger.error(f"Error analyzing {pdf_file.name}: {e}")
            detailed_results[pdf_file.name] = []
    
    # Write to output file if specified
    if output_file:
        try:
            with open(output_file, 'w') as f:
                for filename, distribution in detailed_results.items():
                    f.write(f"=== {filename} ===\n")
                    if distribution:
                        for zglyph, count in distribution:
                            f.write(f"{zglyph}: {count}\n")
                    else:
                        f.write("No Z-Glyphs found or processing error\n")
                    f.write("\n")
            logger.info(f"Detailed analysis written to {output_file}")
        except Exception as e:
            logger.error(f"Error writing to output file: {e}")
    
    return detailed_results
