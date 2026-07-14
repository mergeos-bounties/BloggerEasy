from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from bloggereasy.cli import app
from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.validate import validate_theme_file

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"
runner = CliRunner()


def test_magazine_template_generates_three_column_xml(tmp_path: Path) -> None:
    out = tmp_path / "magazine.xml"
    result = generate_from_html(SAMPLES / "magazine.html", out, template="magazine")
    xml = out.read_text(encoding="utf-8")

    assert result["validation"]["ok"] is True
    assert result["structure"]["layout"] == "three-column"
    assert result["structure"]["features"]["magazine_left_rail"] is True
    assert "grid-template-columns: 220px 1fr 260px" in xml
    assert "id='magazine-left'" in xml
    assert "type='Blog'" in xml
    assert validate_theme_file(out)["ok"] is True


def test_cli_magazine_template_works(tmp_path: Path) -> None:
    out = tmp_path / "cli-magazine.xml"
    result = runner.invoke(
        app,
        [
            "gen",
            "html",
            "--input",
            str(SAMPLES / "magazine.html"),
            "--template",
            "magazine",
            "--out",
            str(out),
        ],
    )

    assert result.exit_code == 0, result.stdout
    xml = out.read_text(encoding="utf-8")
    assert "id='magazine-left'" in xml
    assert "type='Blog'" in xml
