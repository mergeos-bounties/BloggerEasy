"""Theme pack sample: corporate_blue (Fixes #32).

Verifies the corporate_blue preset generates valid Blogger XML from the
self-contained HTML fixture, containing a b:skin block and a Blog widget.
"""

from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.presets import PRESETS
from bloggereasy.theme.validate import validate_theme_file

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_corporate_blue_preset_registered() -> None:
    assert "corporate_blue" in PRESETS
    assert PRESETS["corporate_blue"]["accent"] == "#0055aa"


def test_corporate_blue_sample_exists() -> None:
    assert (SAMPLES / "corporate_blue.html").is_file()


def test_gen_html_corporate_blue_produces_skin_and_blog_widget(tmp_path: Path) -> None:
    src = SAMPLES / "corporate_blue.html"
    out = tmp_path / "corporate_blue.xml"
    result = generate_from_html(src, out, template="corporate_blue")

    assert result["validation"]["ok"], result["validation"]
    assert out.exists()

    xml = out.read_text(encoding="utf-8")
    assert "xmlns:b=" in xml
    assert "b:skin" in xml
    assert "type='Blog'" in xml or 'type="Blog"' in xml
    # corporate_blue accent should be pushed into the skin
    assert "0055aa" in xml
    assert "Template: corporate_blue" in xml

    v = validate_theme_file(out)
    assert v["ok"] is True
