from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.parse.html_page import parse_html_file
from bloggereasy.theme.builder import build_blogger_xml
from bloggereasy.theme.validate import validate_blogger_xml

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_builder_includes_seo_head_placeholders() -> None:
    xml = build_blogger_xml(parse_html_file(SAMPLES / "minimal_blog.html"))

    assert "name='description'" in xml
    assert "property='og:site_name'" in xml
    assert "property='og:title'" in xml
    assert "property='og:description'" in xml
    assert "property='og:url'" in xml
    assert "name='twitter:card'" in xml
    assert "data:blog.metaDescription" in xml
    assert validate_blogger_xml(xml)["ok"] is True


def test_generated_theme_keeps_seo_defaults_valid(tmp_path: Path) -> None:
    out = tmp_path / "seo.xml"
    result = generate_from_html(SAMPLES / "portfolio.html", out, template="portfolio")
    xml = out.read_text(encoding="utf-8")

    assert result["validation"]["ok"] is True
    assert "content='website' property='og:type'" in xml
    assert "content='summary_large_image' name='twitter:card'" in xml
