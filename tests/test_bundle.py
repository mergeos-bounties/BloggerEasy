from __future__ import annotations

import json
from pathlib import Path

import pytest

from bloggereasy.integrations.bundle import BUNDLE_VERSION, generate_bundle

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_generate_bundle_from_html(tmp_path: Path) -> None:
    out_dir = tmp_path / "bundle"
    manifest = generate_bundle(str(SAMPLES / "minimal_blog.html"), out_dir, source="html")

    assert manifest["bundle_version"] == BUNDLE_VERSION
    assert manifest["source"] == "html"

    # all four bundle files exist on disk
    theme = out_dir / "theme.xml"
    preview = out_dir / "preview.html"
    guide = out_dir / "GUIDE.md"
    evidence = out_dir / "evidence.json"
    for path in (theme, preview, guide, evidence):
        assert path.exists(), f"missing {path.name}"

    # theme is a real Blogger XML
    text = theme.read_text(encoding="utf-8")
    assert "b:skin" in text or "BloggerEasy" in text

    # guide is human-readable and points at the import flow
    guide_text = guide.read_text(encoding="utf-8")
    assert "Import into Blogger" in guide_text
    assert "theme.xml" in guide_text


def test_bundle_evidence_manifest_matches_disk(tmp_path: Path) -> None:
    out_dir = tmp_path / "bundle"
    generate_bundle(str(SAMPLES / "portfolio.html"), out_dir, source="html", template="portfolio")

    evidence = json.loads((out_dir / "evidence.json").read_text(encoding="utf-8"))
    assert evidence["template"] == "portfolio"
    assert evidence["validation"]["ok"] is True

    # checksums recorded for theme/preview/guide and are non-empty hex digests
    for name in ("theme", "preview", "guide"):
        digest = evidence["checksums"][name]
        assert len(digest) == 64
        int(digest, 16)  # raises if not valid hex


def test_bundle_from_image_fallback(tmp_path: Path) -> None:
    fake = tmp_path / "design.png"
    fake.write_bytes(b"not-an-image")
    out_dir = tmp_path / "img-bundle"
    manifest = generate_bundle(str(fake), out_dir, source="image", title="Palette Blog")

    assert manifest["source"] == "image"
    assert manifest["title"] == "Palette Blog"
    assert (out_dir / "theme.xml").exists()


def test_bundle_rejects_unknown_source(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        generate_bundle("whatever", tmp_path / "x", source="bogus")
