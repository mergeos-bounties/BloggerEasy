from __future__ import annotations

from pathlib import Path

import pytest

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.presets import PRESETS, apply_preset

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"

PACK = ("portfolio", "news", "personal", "docs")


def test_pack_templates_registered() -> None:
    for name in PACK:
        assert name in PRESETS, f"{name} missing from PRESETS"


@pytest.mark.parametrize("template", PACK)
def test_gen_works_for_each_pack_template(tmp_path: Path, template: str) -> None:
    out = tmp_path / f"{template}.xml"
    result = generate_from_html(SAMPLES / "minimal_blog.html", out, template=template)
    assert result["validation"]["ok"], f"{template} failed validation"
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "b:skin" in text
    assert f"Template: {template}" in text


def test_pack_templates_have_distinct_accents() -> None:
    accents = {name: PRESETS[name].get("accent") for name in PACK}
    # personal/docs bring their own accent; portfolio/news too — all distinct
    values = [a for a in accents.values() if a]
    assert len(values) == len(set(values)), f"accents not distinct: {accents}"


def test_personal_is_single_column_docs_is_two_column() -> None:
    base = {"title": "T", "colors": {}, "features": {}}
    personal = apply_preset(dict(base, features={}), "personal")
    docs = apply_preset(dict(base, features={}), "docs")
    assert personal.get("layout") != "two-column"  # single-column layout
    assert docs.get("layout") == "two-column"
    assert docs["features"].get("dense") is True
