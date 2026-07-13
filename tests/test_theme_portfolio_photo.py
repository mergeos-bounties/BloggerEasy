"""Theme pack sample: portfolio_photo (Fixes #26).

Verifies the portfolio_photo preset generates valid Blogger XML from the
self-contained HTML fixture, containing a b:skin block and a Blog widget.
"""

from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.presets import PRESETS
from bloggereasy.theme.validate import validate_theme_file

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_portfolio_photo_preset_registered() -> None:
    assert "portfolio_photo" in PRESETS
    assert PRESETS["portfolio_photo"]["accent"] == "#c4a574"


def test_portfolio_photo_sample_exists() -> None:
    assert (SAMPLES / "portfolio_photo.html").is_file()


def test_gen_html_portfolio_photo_produces_skin_and_blog_widget(tmp_path: Path) -> None:
    src = SAMPLES / "portfolio_photo.html"
    out = tmp_path / "portfolio_photo.xml"
    result = generate_from_html(src, out, template="portfolio_photo")

    assert result["validation"]["ok"], result["validation"]
    assert out.exists()

    xml = out.read_text(encoding="utf-8")
    assert "xmlns:b=" in xml
    assert "b:skin" in xml
    assert "type='Blog'" in xml or 'type="Blog"' in xml
    # portfolio_photo accent should be pushed into the skin
    assert "c4a574" in xml
    assert "Template: portfolio_photo" in xml

    v = validate_theme_file(out)
    assert v["ok"] is True
