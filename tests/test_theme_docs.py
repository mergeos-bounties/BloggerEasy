from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from bloggereasy.cli import app
from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.presets import PRESETS
from bloggereasy.theme.validate import validate_theme_file

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "data" / "samples" / "html"
runner = CliRunner()


def test_docs_template_generates_sidebar_article_skin(tmp_path: Path) -> None:
    out = tmp_path / "docs.xml"
    result = generate_from_html(SAMPLES / "docs_knowledge_base.html", out, template="docs")
    xml = out.read_text(encoding="utf-8")

    assert "docs" in PRESETS
    assert result["validation"]["ok"] is True
    assert result["structure"]["layout"] == "two-column"
    assert result["structure"]["features"]["sidebar"] is True
    assert result["structure"]["features"]["dense"] is True
    assert "Template: docs" in xml
    assert "b:skin" in xml
    assert "type='Blog'" in xml
    assert "id='sidebar'" in xml
    assert "<article class='post'>" in xml
    assert "#0d9488" in xml
    assert validate_theme_file(out)["ok"] is True


def test_cli_docs_template_works_offline(tmp_path: Path) -> None:
    out = tmp_path / "cli-docs.xml"
    result = runner.invoke(
        app,
        [
            "gen",
            "html",
            "--input",
            str(SAMPLES / "docs_blog.html"),
            "--template",
            "docs",
            "--out",
            str(out),
        ],
    )

    assert result.exit_code == 0, result.stdout
    xml = out.read_text(encoding="utf-8")
    assert "Template: docs" in xml
    assert "type='Blog'" in xml
    assert "id='sidebar'" in xml


def test_readme_lists_docs_template() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "| `docs` | Documentation-style sidebar + article layout |" in readme
