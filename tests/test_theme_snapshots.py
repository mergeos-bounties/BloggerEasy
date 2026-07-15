"""Golden structural snapshots for dark + magazine theme skins."""

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.validate import validate_theme_file


def test_dark_and_magazine_generate_valid_xml(tmp_path: Path) -> None:
    samples = Path("data/samples/html")
    cases = [
        ("dark_dev.html", "dark"),
        ("magazine.html", "magazine"),
        ("contact_card.html", "simple"),
        ("resume_cv.html", "simple"),
        ("product_launch.html", "dark"),
        ("newsletter.html", "simple"),
        ("newsletter_signup_page.html", "simple"),
    ]
    for name, tmpl in cases:
        src = samples / name
        assert src.exists(), name
        out = tmp_path / f"{tmpl}.xml"
        result = generate_from_html(src, out, template=tmpl)
        assert result["validation"]["ok"] is True
        xml = out.read_text(encoding="utf-8")
        assert "b:skin" in xml or "skin" in xml.lower()
        assert "Blog" in xml
        # dark preset should push dark-ish background into skin
        if tmpl == "dark":
            assert "#0f172a" in xml or "0f172a" in xml
        v = validate_theme_file(out)
        assert v["ok"] is True
