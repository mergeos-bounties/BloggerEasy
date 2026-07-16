from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.validate import validate_blogger_xml, validate_theme_file

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
    result = validate_blogger_xml(xml)
    assert result["ok"] is False
    assert "missing b namespace on <html>" in result["errors"]
    assert "missing Blog widget" in result["errors"]
    assert "missing required widget section(s)" not in result["errors"]


def _valid_theme_xml(body: str = "") -> str:
    filler = "x" * 900
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:b="http://www.google.com/2005/gml/b">
  <head><b:skin><![CDATA[body {{ color: #222; }}]]></b:skin></head>
  <body>
    <b:section id="header" name="Header">
      <b:widget id="Header1" title="Header" type="Header" />
    </b:section>
    <b:section id="main" name="Main">
      <b:widget id="Blog1" title="Blog" type="Blog" />
    </b:section>
    {body}
    <p>{filler}</p>
  </body>
</html>
"""


def test_validate_warns_for_external_image_and_script_assets() -> None:
    xml = _valid_theme_xml(
        """
        <img src="https://cdn.example.com/hero.png" alt="Hero" />
        <script src='http://cdn.example.com/theme.js'></script>
        """
    )

    result = validate_blogger_xml(xml)

    assert result["ok"] is True
    assert "external img asset URL: https://cdn.example.com/hero.png" in result["warnings"]
    assert "external script asset URL: http://cdn.example.com/theme.js" in result["warnings"]


def test_validate_does_not_warn_for_local_image_and_script_assets() -> None:
    xml = _valid_theme_xml(
        """
        <img src="/assets/hero.png" alt="Hero" />
        <script src="theme.js"></script>
        """
    )

    result = validate_blogger_xml(xml)

    assert result["ok"] is True
    assert not any("external" in warning for warning in result["warnings"])
