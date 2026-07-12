from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html, generate_from_image

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_generate_from_html(tmp_path: Path) -> None:
    out = tmp_path / "out.xml"
    result = generate_from_html(SAMPLES / "minimal_blog.html", out)
    assert result["integration_version"] == "bloggereasy.sdk.v1"
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "BloggerEasy" in text or "b:skin" in text


def test_generate_from_image_without_pillow(tmp_path: Path) -> None:
    # even a non-image path name: structure_from_image falls back if open fails
    fake = tmp_path / "design.png"
    fake.write_bytes(b"not-an-image")
    out = tmp_path / "img-theme.xml"
    result = generate_from_image(fake, out, title="Palette Blog")
    assert result["mode"] == "image"
    assert out.exists()
    assert result["structure"]["title"] == "Palette Blog"


def test_generate_from_html_travel_journal(tmp_path: Path) -> None:
    out = tmp_path / "travel_journal.xml"
    result = generate_from_html(SAMPLES / "travel_journal.html", out)
    assert result["integration_version"] == "bloggereasy.sdk.v1"
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "b:skin" in text
    assert "Blog1" in text or "Blog" in text
