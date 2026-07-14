from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.parse.html_page import parse_html_file
from bloggereasy.theme.builder import build_blogger_xml
from bloggereasy.theme.validate import validate_blogger_xml

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_nav_links_generate_linklist_widget() -> None:
    structure = parse_html_file(SAMPLES / "portfolio.html")
    xml = build_blogger_xml(structure)

    assert "id='navigation'" in xml
    assert "type='LinkList'" in xml
    assert "name='link-0.name'" in xml
    assert "Portfolio" in xml or "Home" in xml
    assert validate_blogger_xml(xml)["ok"] is True


def test_generated_theme_contains_nav_widget(tmp_path: Path) -> None:
    out = tmp_path / "nav.xml"
    result = generate_from_html(SAMPLES / "minimal_blog.html", out)
    xml = out.read_text(encoding="utf-8")

    assert result["validation"]["ok"] is True
    assert "LinkList1" in xml
    assert "showaddelement='yes'" in xml
