"""Tests for #74: template list with tags filter."""
from __future__ import annotations

from bloggereasy.theme.presets import PRESETS, PRESET_TAGS, tokens_for_preset


def test_preset_tags_exist_for_all_presets() -> None:
    """Every preset has a tags entry."""
    for name in PRESETS:
        assert name in PRESET_TAGS, f"Missing tags for preset '{name}'"
        assert isinstance(PRESET_TAGS[name], list)
        assert len(PRESET_TAGS[name]) > 0, f"Empty tags for preset '{name}'"


def test_tokens_for_preset_returns_tags() -> None:
    """tokens_for_preset includes tags in output."""
    result = tokens_for_preset("dark")
    assert result["template"] == "dark"
    assert "dark" in result["tags"]
    assert "blog" in result["tags"]


def test_tokens_for_preset_includes_features() -> None:
    """tokens_for_preset includes feature flags."""
    result = tokens_for_preset("magazine")
    assert result["features"]["sidebar"] is True
    assert result["features"]["magazine_left_rail"] is True
    assert result["features"]["dense"] is True


def test_tokens_for_preset_unknown_raises() -> None:
    """tokens_for_preset raises for unknown templates."""
    try:
        tokens_for_preset("nonexistent")
        assert False, "Should have raised"
    except ValueError as e:
        assert "nonexistent" in str(e)


def test_all_tags_are_valid() -> None:
    """All tag strings are clean identifiers."""
    for name, tags in PRESET_TAGS.items():
        for tag in tags:
            assert tag.isidentifier() or "-" not in tag, f"Invalid tag '{tag}' in '{name}'"
