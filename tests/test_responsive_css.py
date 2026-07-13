from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.parse.html_page import parse_html_file
from bloggereasy.theme.builder import build_blogger_xml

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_builder_includes_mobile_responsive_css() -> None:
    xml = build_blogger_xml(parse_html_file(SAMPLES / "minimal_blog.html"))

    assert "overflow-wrap: anywhere" in xml
    assert "img, iframe, video" in xml
    assert "@media (max-width: 800px)" in xml
    assert "@media (max-width: 480px)" in xml
    assert "flex-direction: column" in xml


def test_generated_theme_keeps_responsive_css(tmp_path: Path) -> None:
    out = tmp_path / "responsive.xml"
    result = generate_from_html(SAMPLES / "portfolio.html", out, template="portfolio")
    xml = out.read_text(encoding="utf-8")

    assert result["validation"]["ok"] is True
    assert "max-width: 100%" in xml
    assert ".post { padding: 0.85rem; }" in xml
