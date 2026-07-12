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
