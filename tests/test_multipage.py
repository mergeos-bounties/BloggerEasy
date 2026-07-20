"""Tests for multi-page site generator (home + about + contact)."""

from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.multipage import (
    MULTIPAGE_VERSION,
    PAGE_TYPES,
    generate_multipage,
)

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def _base_structure(sample: str = "minimal_blog.html") -> dict:
    """Build a base structure from a sample HTML file."""
    result = generate_from_html(SAMPLES / sample, Path("/dev/null"), template="simple")
    return result["structure"]


def test_multipage_generates_three_pages(tmp_path: Path) -> None:
    out_dir = tmp_path / "multipage"
    manifest = generate_multipage(_base_structure(), out_dir, template="simple")

    assert manifest["multipage_version"] == MULTIPAGE_VERSION
    assert set(manifest["pages"].keys()) == set(PAGE_TYPES)

    for page_type in PAGE_TYPES:
        info = manifest["pages"][page_type]
        xml_path = Path(info["path"])
        assert xml_path.exists(), f"missing {page_type}.xml"
        text = xml_path.read_text(encoding="utf-8")
        assert "b:skin" in text or "BloggerEasy" in text
        assert info["validation"]["ok"] is True
        assert info["bytes"] > 0


def test_multipage_shares_design_tokens(tmp_path: Path) -> None:
    out_dir = tmp_path / "multipage"
    manifest = generate_multipage(_base_structure("portfolio.html"), out_dir, template="portfolio")

    shared = manifest["shared_design"]
    assert shared["template"] == "portfolio"
    assert "colors" in shared
    assert "fonts" in shared

    # All pages should pass validation, sharing the same template/design
    assert manifest["pages"]["home"]["validation"]["ok"] is True
    assert manifest["pages"]["about"]["validation"]["ok"] is True
    assert manifest["pages"]["contact"]["validation"]["ok"] is True


def test_multipage_titles_are_distinct(tmp_path: Path) -> None:
    out_dir = tmp_path / "multipage"
    base = _base_structure("portfolio.html")
    base["title"] = "My Awesome Site"
    manifest = generate_multipage(base, out_dir, template="portfolio")

    titles = {pt: manifest["pages"][pt]["title"] for pt in PAGE_TYPES}
    assert "My Awesome Site" in titles["home"]
    assert "About" in titles["about"]
    assert "Contact" in titles["contact"]
    assert titles["home"] != titles["about"]
    assert titles["home"] != titles["contact"]
    assert titles["about"] != titles["contact"]


def test_multipage_home_has_sidebar_about_contact_dont(tmp_path: Path) -> None:
    out_dir = tmp_path / "multipage"
    manifest = generate_multipage(_base_structure(), out_dir)

    assert manifest["pages"]["home"]["layout"] == "two-column"
    assert manifest["pages"]["about"]["layout"] == "single-column"
    assert manifest["pages"]["contact"]["layout"] == "single-column"


def test_multipage_nav_links_consistent(tmp_path: Path) -> None:
    out_dir = tmp_path / "multipage"
    generate_multipage(_base_structure(), out_dir)

    # All three pages should have nav links pointing to the same destinations
    home_xml = (out_dir / "home.xml").read_text(encoding="utf-8")
    about_xml = (out_dir / "about.xml").read_text(encoding="utf-8")
    contact_xml = (out_dir / "contact.xml").read_text(encoding="utf-8")

    for xml, page_type in [
        (home_xml, "home"),
        (about_xml, "about"),
        (contact_xml, "contact"),
    ]:
        assert "About" in xml, f"About nav link missing from {page_type}"
        assert "Contact" in xml, f"Contact nav link missing from {page_type}"
        assert "Home" in xml, f"Home nav link missing from {page_type}"


def test_multipage_all_xml_valid(tmp_path: Path) -> None:
    """Every generated file is valid Blogger-importable XML."""
    out_dir = tmp_path / "multipage"
    manifest = generate_multipage(_base_structure(), out_dir, template="corporate_blue")

    assert manifest["validation_ok"] is True
    for page_type in PAGE_TYPES:
        assert manifest["pages"][page_type]["validation"]["ok"] is True


def test_multipage_works_with_different_templates(tmp_path: Path) -> None:
    """Multi-page generator should work with multiple template presets."""
    for template in ("simple", "portfolio", "news", "corporate_blue"):
        out_dir = tmp_path / f"mp_{template}"
        manifest = generate_multipage(_base_structure(), out_dir, template=template)
        assert manifest["template"] == template
        assert manifest["validation_ok"] is True


def test_multipage_file_names_match_page_types(tmp_path: Path) -> None:
    out_dir = tmp_path / "multipage"
    manifest = generate_multipage(_base_structure(), out_dir)

    for page_type in PAGE_TYPES:
        info = manifest["pages"][page_type]
        assert info["file"] == f"{page_type}.xml"


def test_multipage_creates_out_dir(tmp_path: Path) -> None:
    out_dir = tmp_path / "nested" / "deep" / "multipage"
    assert not out_dir.exists()
    generate_multipage(_base_structure(), out_dir)
    assert out_dir.exists()
    assert (out_dir / "home.xml").exists()
    assert (out_dir / "about.xml").exists()
    assert (out_dir / "contact.xml").exists()
