# conftest.py
"""Pytest configuration for SymbolicOperatingSystem."""

from sos_path import add_repo_root_to_path

# Ensure tests use the repository root for imports
add_repo_root_to_path()
