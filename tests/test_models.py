from __future__ import annotations

import pytest
from pydantic import ValidationError

from bloggereasy.theme.builder import build_blogger_xml
from bloggereasy.theme.models import PageStructure, structure_dict, validate_structure
from bloggereasy.theme.presets import apply_preset


def test_page_structure_defaults_and_coercion() -> None:
    structure = validate_structure(
        {
            "title": "",
            "nav_links": [{"label": 123, "href": None}],
            "colors": {"primary": "#123456"},
            "features": {"nav_count": "2", "sidebar": "true"},
        }
    )

    assert structure.title == "My Blog"
    assert structure.nav_links[0].label == "123"
    assert structure.nav_links[0].href == ""
    assert structure.colors.primary == "#123456"
    assert structure.features.nav_count == 2
    assert structure.features.sidebar is True


def test_builder_validates_input_and_uses_defaults() -> None:
    xml = build_blogger_xml({"title": None, "colors": {}, "features": {}})

    assert "BloggerEasy generated theme" in xml
    assert "My Blog" in xml


def test_builder_rejects_invalid_layout() -> None:
    with pytest.raises(ValidationError):
        build_blogger_xml({"layout": "grid"})


def test_apply_preset_accepts_model_and_returns_compatible_dict() -> None:
    structure = PageStructure(title="Typed Blog")
    out = apply_preset(structure, "magazine")

    assert isinstance(out, dict)
    assert out["title"] == "Typed Blog"
    assert out["layout"] == "three-column"
    assert out["features"]["sidebar"] is True
    assert out["features"]["dense"] is True


def test_structure_dict_preserves_extra_metadata() -> None:
    out = structure_dict({"title": "Meta Blog", "custom": {"source": "fixture"}})

    assert out["title"] == "Meta Blog"
    assert out["custom"] == {"source": "fixture"}
