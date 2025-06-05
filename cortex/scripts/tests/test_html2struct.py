import importlib.util
from pathlib import Path

root = Path(__file__).resolve().parents[3]
script = root / "local/bin/html2struct.py"
spec = importlib.util.spec_from_file_location("html2struct", script)
html2struct = importlib.util.module_from_spec(spec)
spec.loader.exec_module(html2struct)


def test_process_html_file_no_links():
    result = html2struct.process_html_file("rocq/index.html")
    assert "links" not in result
    assert "link_categories" not in result
    assert "related" not in result
    assert result["title"]

