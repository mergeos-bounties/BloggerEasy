"""Theme pack sample: magazine_news (Fixes #25).

Verifies the magazine_news preset generates valid Blogger XML from the
self-contained HTML fixture, containing a b:skin block and a Blog widget.
"""

from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.presets import PRESETS
from bloggereasy.theme.validate import validate_theme_file

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_magazine_news_preset_registered() -> None:
    assert "magazine_news" in PRESETS
    assert PRESETS["magazine_news"]["accent"] == "#b91c1c"


def test_magazine_news_sample_exists() -> None:
    assert (SAMPLES / "magazine_news.html").is_file()


def test_gen_html_magazine_news_produces_skin_and_blog_widget(tmp_path: Path) -> None:
    src = SAMPLES / "magazine_news.html"
    out = tmp_path / "magazine_news.xml"
    result = generate_from_html(src, out, template="magazine_news")

    assert result["validation"]["ok"], result["validation"]
    assert out.exists()

    xml = out.read_text(encoding="utf-8")
    assert "xmlns:b=" in xml
    assert "b:skin" in xml
    assert "type='Blog'" in xml or 'type="Blog"' in xml
    # magazine_news accent should be pushed into the skin
    assert "b91c1c" in xml
    assert "Template: magazine_news" in xml

    v = validate_theme_file(out)
    assert v["ok"] is True
