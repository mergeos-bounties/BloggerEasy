from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from bloggereasy.cli import app
from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.builder import build_blogger_xml
from bloggereasy.theme.presets import apply_dark_variant

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"
runner = CliRunner()


def test_apply_dark_variant_sets_skin_colors() -> None:
    structure = apply_dark_variant({"title": "Dark Blog", "colors": {"primary": "#ffcc00"}})
    xml = build_blogger_xml(structure)

    assert structure["features"]["dark"] is True
    assert "background: #0f172a" in xml
    assert "color: #e2e8f0" in xml
    assert "background: #111827" in xml
    assert "border: 1px solid #334155" in xml


def test_sdk_dark_flag_writes_dark_theme(tmp_path: Path) -> None:
    out = tmp_path / "dark.xml"
    result = generate_from_html(SAMPLES / "minimal_blog.html", out, dark=True)

    assert result["validation"]["ok"] is True
    assert result["structure"]["features"]["dark"] is True
    assert "#0f172a" in out.read_text(encoding="utf-8")


def test_cli_gen_html_dark_flag(tmp_path: Path) -> None:
    out = tmp_path / "dark-cli.xml"
    result = runner.invoke(
        app,
        [
            "gen",
            "html",
            "--input",
            str(SAMPLES / "minimal_blog.html"),
            "--dark",
            "--out",
            str(out),
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert out.exists()
    assert "#0f172a" in out.read_text(encoding="utf-8")
