"""Round-trip property tests: colors fed in must land in the b:skin CDATA.

Issue #16: generate → the primary (and other) colors should still be present
in the generated theme's skin block, so a theme built from a design keeps its
palette when imported into Blogger.
"""

from __future__ import annotations

import re

import pytest

from bloggereasy.theme.builder import build_blogger_xml
from bloggereasy.theme.presets import PRESETS, apply_preset

# Hex colors unlikely to appear incidentally in the static template CSS.
SAMPLE_COLORS = [
    {"primary": "#ab12cd", "secondary": "#123456", "background": "#fdfdfd", "text": "#010203"},
    {"primary": "#ff6600", "secondary": "#0066ff", "background": "#ffffff", "text": "#222222"},
    {"primary": "#7c3aed", "secondary": "#0d9488", "background": "#f8fafc", "text": "#111111"},
]


def _skin_cdata(xml: str) -> str:
    """Return the CSS inside the b:skin CDATA block."""
    m = re.search(r"<b:skin[^>]*>\s*<!\[CDATA\[(.*?)\]\]>\s*</b:skin>", xml, re.DOTALL)
    assert m, "no b:skin CDATA block found"
    return m.group(1)


def _structure(colors: dict) -> dict:
    return {
        "title": "Round Trip",
        "colors": colors,
        "fonts": {"body": "system-ui", "heading": "Georgia"},
        "nav_links": [{"label": "Home", "href": "#"}],
        "features": {"sidebar": False},
        "layout": "single-column",
    }


@pytest.mark.parametrize("colors", SAMPLE_COLORS)
def test_primary_color_lands_in_skin_cdata(colors: dict) -> None:
    xml = build_blogger_xml(_structure(colors), template_name="simple")
    skin = _skin_cdata(xml)
    assert colors["primary"].lower() in skin.lower(), "primary color missing from skin CDATA"


@pytest.mark.parametrize("colors", SAMPLE_COLORS)
def test_core_colors_present_in_skin(colors: dict) -> None:
    xml = build_blogger_xml(_structure(colors), template_name="simple")
    skin = _skin_cdata(xml).lower()
    for role in ("primary", "secondary", "background", "text"):
        assert colors[role].lower() in skin, f"{role} color {colors[role]} missing from skin"


@pytest.mark.parametrize("template", list(PRESETS))
def test_effective_primary_survives_every_preset(template: str) -> None:
    """After apply_preset, whatever primary the preset resolves to must be in the skin."""
    base = _structure(
        {"primary": "#ab12cd", "secondary": "#123456", "background": "#fdfdfd", "text": "#010203"}
    )
    resolved = apply_preset(base, template)
    xml = build_blogger_xml(resolved, template_name=template)
    skin = _skin_cdata(xml).lower()
    effective_primary = (resolved.get("colors") or {}).get("primary", "").lower()
    assert effective_primary, "no effective primary after preset"
    assert effective_primary in skin, f"{template}: primary {effective_primary} missing from skin"
