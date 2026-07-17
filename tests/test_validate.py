from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from bloggereasy.cli import app
from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.validate import validate_blogger_xml, validate_theme_file

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"
runner = CliRunner()


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


def test_strict_validation_accepts_well_formed_theme() -> None:
    result = validate_blogger_xml(_valid_theme_xml(), strict=True)

    assert result["ok"] is True
    assert result["strict"] is True


def test_strict_validation_rejects_empty_section() -> None:
    xml = _valid_theme_xml('<b:section id="empty" name="Empty"></b:section>')

    result = validate_blogger_xml(xml, strict=True)

    assert result["ok"] is False
    assert "empty <b:section> is not allowed: empty" in result["errors"]


def test_strict_validation_rejects_malformed_xml() -> None:
    malformed = _valid_theme_xml().replace("</html>", "")

    result = validate_blogger_xml(malformed, strict=True)

    assert result["ok"] is False
    assert "strict XML parse failed" in result["errors"]


def test_validate_cli_forwards_strict_flag(tmp_path: Path) -> None:
    theme = tmp_path / "theme.xml"
    theme.write_text(_valid_theme_xml(), encoding="utf-8")

    result = runner.invoke(app, ["validate", "--file", str(theme), "--strict"])

    assert result.exit_code == 0
    assert '"strict": true' in result.stdout
