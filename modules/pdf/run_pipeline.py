#!/usr/bin/env python3

# modules/pdf/run_pipeline.py

import sys
import logging
import argparse
from pathlib import Path

# Add the parent directory to sys.path to allow importing the module
parent_dir = Path(__file__).resolve().parent.parent
if parent_dir not in sys.path:
    sys.path.insert(0, str(parent_dir))

from pdf.pipeline import process_pdf_directory, get_detailed_analysis

def setup_logging(verbose=False, debug=False):
    """Configure logging based on verbosity level."""
    level = logging.WARNING
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
        
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr
    )

def main():
    """Main entry point for the PDF Z-Glyph pipeline."""
    parser = argparse.ArgumentParser(
        description="Process PDF files to identify most frequent Z-Glyphs"
    )
    parser.add_argument(
        "directory", 
        help="Directory containing PDF files to process"
    )
    parser.add_argument(
        "--sequential", 
        action="store_true", 
        help="Process files sequentially instead of in parallel"
    )
    parser.add_argument(
        "--workers", 
        type=int, 
        default=4, 
        help="Maximum number of worker threads for parallel processing"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug logging"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable info logging"
    )
    parser.add_argument(
        "--detailed", 
        action="store_true", 
        help="Perform detailed Z-Glyph analysis"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        help="Output file for detailed analysis (only used with --detailed)"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(verbose=args.verbose, debug=args.debug)
    
    # Process PDFs
    if args.detailed:
        # Perform detailed analysis
        detailed_results = get_detailed_analysis(args.directory, args.output)
        
        # Print summary to stdout
        for filename, distribution in detailed_results.items():
            if distribution:
                # Get the most frequent Z-Glyphs (could be multiple with same count)
                max_count = distribution[0][1] if distribution else 0
                top_zglyphs = ''.join([z for z, count in distribution if count == max_count])
                print(f"{filename}{top_zglyphs}")
            else:
                print(f"{filename}Z?")
    else:
        # Standard processing
        results = process_pdf_directory(
            args.directory, 
            parallel=not args.sequential, 
            max_workers=args.workers
        )
        
        # Print results sorted by filename
        for filename in sorted(results.keys()):
            print(f"{filename}{results[filename]}")

if __name__ == "__main__":
    main()
