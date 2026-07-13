"""Tests for the Figma/export HTML adapter (issue #14).

Covers: script stripping, huge inline-CSS capping, absolute/localhost path
normalization — and that generation from a messy exported page still
produces a valid, importable theme.
"""

from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.parse.html_page import parse_html_string
from bloggereasy.parse.normalize import MAX_INLINE_CSS, normalize_export_html

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"
FIGMA_EXPORT = SAMPLES / "figma_export.html"


def test_scripts_are_stripped() -> None:
    html = FIGMA_EXPORT.read_text(encoding="utf-8")
    clean, report = normalize_export_html(html)
    assert "<script" not in clean.lower()
    assert report["scripts_removed"] == 3  # 2 paired scripts + 1 self-closing-ish async


def test_absolute_and_localhost_paths_normalized() -> None:
    html = FIGMA_EXPORT.read_text(encoding="utf-8")
    clean, report = normalize_export_html(html)
    assert "file://" not in clean
    assert "localhost" not in clean
    assert report["abs_paths_rewritten"] >= 2


def test_huge_inline_css_is_truncated() -> None:
    huge_css = "body{color:red}" * 5000  # way over MAX_INLINE_CSS
    html = f"<html><head><style>{huge_css}</style></head><body>hi</body></html>"
    clean, report = normalize_export_html(html)
    assert report["style_blocks_truncated"] == 1
    assert len(clean) < len(html)
    assert "truncated by BloggerEasy" in clean


def test_small_inline_css_is_untouched() -> None:
    html = "<html><head><style>body{color:red}</style></head><body>hi</body></html>"
    clean, report = normalize_export_html(html)
    assert report["style_blocks_truncated"] == 0
    assert "body{color:red}" in clean


def test_normalize_is_idempotent_on_clean_html() -> None:
    html = "<html><head><title>T</title></head><body><h1>Hi</h1></body></html>"
    clean, report = normalize_export_html(html)
    assert clean == html
    assert report["scripts_removed"] == 0
    assert report["abs_paths_rewritten"] == 0


def test_parse_html_string_reports_normalization() -> None:
    html = FIGMA_EXPORT.read_text(encoding="utf-8")
    structure = parse_html_string(html)
    assert structure["normalize"]["scripts_removed"] > 0
    assert structure["title"] == "Figma Export — Studio Site"


def test_generate_from_figma_export_produces_valid_theme(tmp_path: Path) -> None:
    out = tmp_path / "figma.xml"
    result = generate_from_html(FIGMA_EXPORT, out, template="simple")
    assert result["validation"]["ok"], result["validation"]
    xml = out.read_text(encoding="utf-8")
    assert "<script" not in xml.lower()
    assert "file://" not in xml
    assert "localhost" not in xml
    # primary color extracted from inline style survives into the theme
    assert "#ff6600" in xml.lower()


def test_cap_constant_is_reasonable() -> None:
    assert 1_000 < MAX_INLINE_CSS < 1_000_000
