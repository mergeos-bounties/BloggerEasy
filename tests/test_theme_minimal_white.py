"""Golden structural check for the minimal_white clean-white personal blog pack."""

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.validate import validate_theme_file

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_minimal_white_generates_skin_and_blog_widget(tmp_path: Path) -> None:
    src = SAMPLES / "minimal_white.html"
    assert src.exists(), "minimal_white.html sample missing"

    out = tmp_path / "minimal_white.xml"
    result = generate_from_html(src, out, template="personal")

    assert result["validation"]["ok"] is True
    assert result["structure"]["title"] == "Quiet Pages"
    # personal preset keeps the single-column layout suited to a minimal blog
    assert result["structure"]["layout"] != "two-column"

    xml = out.read_text(encoding="utf-8")
    assert "b:skin" in xml
    assert "type='Blog'" in xml
    assert "Template: personal" in xml

    v = validate_theme_file(out)
    assert v["ok"] is True
