from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.parse.html_page import parse_html_file

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_parse_vietnamese_sample() -> None:
    structure = parse_html_file(SAMPLES / "vietnamese_blog.html")

    assert structure["title"] == "Nhật ký Sài Gòn"
    assert structure["description"] == "Mẫu blog tiếng Việt cho BloggerEasy."
    assert structure["features"]["nav_count"] == 3
    assert any(link["label"] == "Ẩm thực" for link in structure["nav_links"])
    assert len(structure["sample_paragraphs"]) >= 2


def test_generate_vietnamese_sample_xml(tmp_path: Path) -> None:
    out = tmp_path / "vietnamese_blog.xml"
    result = generate_from_html(SAMPLES / "vietnamese_blog.html", out)
    xml = out.read_text(encoding="utf-8")

    assert result["validation"]["ok"] is True
    assert "Nhật ký Sài Gòn" in xml
    assert "BloggerEasy generated theme" in xml
