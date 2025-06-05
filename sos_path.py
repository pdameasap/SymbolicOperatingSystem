from __future__ import annotations
import sys
from pathlib import Path

def add_repo_root_to_path() -> Path:
    """Ensure the repository root is first on sys.path.

    Returns the detected repository root path.
    """
    repo_root = Path(__file__).resolve().parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    return repo_root

