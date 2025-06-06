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


def test_should_include_page_filters():
    org_cats = ['Category:Scientific organizations based in France']
    id_cats = ['Category:OCLC (identifier)']
    assert not html2struct.should_include_page(org_cats, title='CNRS')
    assert not html2struct.should_include_page(id_cats, title='OCLC (identifier)')
    assert not html2struct.should_include_page([], title='Main Page')
    assert html2struct.should_include_page(['Category:Logic'], title='Logician')
    assert html2struct.should_include_page([], title='Random Page')


def test_extract_categories_from_html():
    html_path = Path('stimuli/Mathematics.html')
    html = html_path.read_text()
    cats = html2struct.extract_categories_from_html(html)
    assert 'Mathematics' in cats
