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


def test_parse_travel_journal() -> None:
    structure = parse_html_file(SAMPLES / "travel_journal.html")
    assert "Travel" in structure["title"]
    assert structure["features"]["sidebar"] is True
    assert structure["layout"] == "two-column"
    assert structure["fonts"]["heading"] == "Palatino"
    assert len(structure["nav_links"]) == 4
