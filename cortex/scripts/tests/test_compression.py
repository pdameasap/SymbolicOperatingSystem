
# File: cortex/scripts/tests/test_compression.py

import pytest
from frameworks.compression import compress_text_to_picl

def test_simple_compression():
    text = (
        "The quick brown fox jumps over the lazy dog. "
        "The quick brown fox is quick."
    )
    picl = compress_text_to_picl(text, top_n=2, min_token_length=3)
    assert "--A--" in picl and "--B--" in picl
    assert "≜ " in picl
    assert any(g in picl for g in ['α','β','γ'])

def test_no_replacement_for_short():
    text = "A B I Z."
    picl = compress_text_to_picl(text)
    assert "--A--" not in picl
