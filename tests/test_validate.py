from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.validate import validate_theme_file

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_validate_generated(tmp_path: Path) -> None:
    out = tmp_path / "t.xml"
    generate_from_html(SAMPLES / "minimal_blog.html", out)
    result = validate_theme_file(out)
    assert result["ok"] is True


def test_validate_reports_clear_errors_for_missing_blogger_bits() -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head></head>
  <body>
    <b:skin>body{}</b:skin>
    <b:section id="main" name="Main"></b:section>
  </body>
</html>
"""
    from bloggereasy.theme.validate import validate_blogger_xml

    result = validate_blogger_xml(xml)
    assert result["ok"] is False
    assert "missing b namespace on <html>" in result["errors"]
    assert "missing Blog widget" in result["errors"]
    assert "missing required widget section(s)" not in result["errors"]
