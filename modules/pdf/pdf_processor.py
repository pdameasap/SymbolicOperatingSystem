# pdf_pipeline_modular/pdf_processor.py

import os
import logging
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    # This should ideally be handled by the main script or setup
    # but logging here provides context if run standalone
    logging.getLogger(__name__).error("pypdf library not found.")
    raise

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: Path) -> str | None:
    """Extracts text content from a PDF file using pypdf with enhanced error handling."""
    try:
        reader = PdfReader(pdf_path)
        if reader.is_encrypted:
            logger.warning(f"PDF is encrypted: {pdf_path.name}. Attempting decrypt...")
            try:
                reader.decrypt("")
            except Exception as decrypt_err:
                logger.error(f"Cannot decrypt {pdf_path.name}: {decrypt_err}")
                return None
        
        if len(reader.pages) == 0:
            logger.warning(f"PDF has no pages: {pdf_path.name}")
            return None
            
        text = ""
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception as page_err:
                # Log error but continue with other pages
                logger.warning(f"Error extracting text from page {page_num+1} in {pdf_path.name}: {type(page_err).__name__}")
                continue
                
        if not text.strip() and len(reader.pages) > 0:
            logger.warning(f"No text extracted from {pdf_path.name}. PDF may be scanned or image-based.")
            return "" # Return empty string
            
        return text
        
    except Exception as e:
        logger.error(f"Failed to extract text from {pdf_path.name} using pypdf: {type(e).__name__}")
        # Fallback: Try with poppler-utils
        try:
            if os.system("which pdftotext > /dev/null 2>&1") == 0:
                logger.info(f"Attempting fallback extraction with pdftotext for {pdf_path.name}")
                temp_txt = pdf_path.with_suffix(".txt")
                # Use proper quoting for paths
                os.system(f"pdftotext -layout \"{pdf_path}\" \"{temp_txt}\" 2>/dev/null")
                
                if temp_txt.exists():
                    with open(temp_txt, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                    temp_txt.unlink()
                    if text.strip():
                        logger.info(f"Successfully extracted text using pdftotext for {pdf_path.name}")
                        return text
            
            logger.error(f"All extraction methods failed for {pdf_path.name}")
            return None
        except Exception as fallback_err:
            logger.error(f"Fallback extraction failed for {pdf_path.name}: {fallback_err}")
            return None

