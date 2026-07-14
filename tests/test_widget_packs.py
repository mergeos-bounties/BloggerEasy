from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from bloggereasy.cli import app
from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.validate import validate_theme_file

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"
runner = CliRunner()


def test_minimal_widgets_include_profile_only(tmp_path: Path) -> None:
    out = tmp_path / "minimal-widgets.xml"
    result = generate_from_html(SAMPLES / "single_column.html", out, widgets="minimal")
    xml = out.read_text(encoding="utf-8")

    assert result["validation"]["ok"] is True
    assert result["structure"]["features"]["widgets"] == "minimal"
    assert "type='Profile'" in xml
    assert "type='Label'" not in xml
    assert "type='PopularPosts'" not in xml
    assert validate_theme_file(out)["ok"] is True


def test_full_widgets_include_popular_labels_archive(tmp_path: Path) -> None:
    out = tmp_path / "full-widgets.xml"
    result = generate_from_html(SAMPLES / "single_column.html", out, widgets="full")
    xml = out.read_text(encoding="utf-8")

    assert result["validation"]["ok"] is True
    assert result["structure"]["layout"] == "two-column"
    assert "type='PopularPosts'" in xml
    assert "type='Label'" in xml
    assert "type='BlogArchive'" in xml
    assert "type='Profile'" in xml


def test_cli_widgets_full_flag(tmp_path: Path) -> None:
    out = tmp_path / "cli-full-widgets.xml"
    result = runner.invoke(
        app,
        [
            "gen",
            "html",
            "--input",
            str(SAMPLES / "single_column.html"),
            "--widgets",
            "full",
            "--out",
            str(out),
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert "type='PopularPosts'" in out.read_text(encoding="utf-8")


def test_cli_rejects_invalid_widgets_value(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        ["gen", "html", "--input", str(SAMPLES / "single_column.html"), "--widgets", "wide"],
    )

    assert result.exit_code == 1
    assert "--widgets must be one of" in result.stdout
