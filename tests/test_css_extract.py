from __future__ import annotations

from pathlib import Path

from bloggereasy.parse.css import extract_css_skin
from bloggereasy.parse.html_page import parse_html_file, parse_html_string
from bloggereasy.theme.builder import build_blogger_xml

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_extract_css_skin_from_inline_styles() -> None:
    html = """
    <html><head><style>
      body { font-family: Inter, Arial, sans-serif; padding: 24px; gap: 18px; }
      h1 { font-family: Merriweather, serif; }
      .card { padding: 14px 18px; border-radius: 12px; }
      .btn { background: #ffcc00; color: #111111; padding: 8px 12px; border-radius: 999px; }
    </style></head><body><h1>CSS Blog</h1></body></html>
    """

    skin = extract_css_skin(html)

    assert skin["fonts"] == {"body": "Inter", "heading": "Merriweather"}
    assert skin["spacing"]["section_padding"] == "24px"
    assert skin["spacing"]["card_padding"] == "14px 18px"
    assert skin["spacing"]["gap"] == "18px"
    assert skin["spacing"]["radius"] == "12px"
    assert skin["buttons"]["background"] == "#ffcc00"
    assert skin["buttons"]["radius"] == "999px"


def test_parse_html_includes_skin_variables() -> None:
    structure = parse_html_file(SAMPLES / "product_launch.html")

    assert "skin" in structure
    assert structure["skin"]["fonts"]["body"]
    assert structure["skin"]["spacing"]["card_padding"]


def test_builder_uses_extracted_skin_variables() -> None:
    structure = parse_html_string(
        """
        <html><head><title>Styled Blog</title><style>
          body { padding: 30px; gap: 22px; }
          article.card { padding: 16px 20px; border-radius: 14px; }
          button { background: #123456; color: #ffffff; padding: 10px 16px; border-radius: 10px; }
        </style></head><body><h1>Styled Blog</h1><article class="card"><p>Body</p></article></body></html>
        """
    )
    xml = build_blogger_xml(structure)

    assert "padding: 30px" in xml
    assert "padding: 16px 20px" in xml
    assert "gap: 22px" in xml
    assert "border-radius: 14px" in xml
    assert "background: #123456" in xml
