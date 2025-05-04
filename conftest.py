# conftest.py
import sys
import os

# Ensure the repo root is on sys.path so top-level packages (frameworks/) resolve.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
