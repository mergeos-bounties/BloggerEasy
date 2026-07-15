from __future__ import annotations

from pathlib import Path

from bloggereasy.parse.html_page import parse_html_file

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_parse_minimal_blog() -> None:
    structure = parse_html_file(SAMPLES / "minimal_blog.html")
    assert "Coastal" in structure["title"]
    assert structure["features"]["sidebar"] is True
    assert structure["layout"] == "two-column"
    assert structure["colors"]["primary"].startswith("#")
    assert len(structure["nav_links"]) >= 2


def test_parse_single_column() -> None:
    structure = parse_html_file(SAMPLES / "single_column.html")
    assert structure["features"]["sidebar"] is False
    assert structure["layout"] == "single-column"


def test_parse_expanded_layout_fixtures() -> None:
    expected = {
        "editorial_magazine.html": ("Northline Review", "two-column"),
        "creative_portfolio_grid.html": ("Mira Stone Portfolio", "single-column"),
        "docs_knowledge_base.html": ("Atlas Docs Hub", "two-column"),
    }

    for filename, (title, layout) in expected.items():
        structure = parse_html_file(SAMPLES / filename)

        assert structure["title"] == title
        assert structure["layout"] == layout
        assert structure["features"]["nav_count"] >= 3
        assert structure["features"]["footer"] is True
        assert structure["colors"]["primary"].startswith("#")


def test_parse_newsletter_signup_page_fixture() -> None:
    sample = SAMPLES / "newsletter_signup_page.html"

    assert sample.is_file()

    structure = parse_html_file(sample)

    assert structure["title"] == "Lettersmith Launch List"
    assert structure["layout"] == "single-column"
    assert structure["features"]["header"] is True
    assert structure["features"]["footer"] is True
    assert structure["features"]["nav_count"] >= 3
    assert "Join the launch list" in structure["headings"]
    assert any("weekly field notes" in paragraph for paragraph in structure["sample_paragraphs"])
