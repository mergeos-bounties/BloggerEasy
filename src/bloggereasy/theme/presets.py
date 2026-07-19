from __future__ import annotations

from bloggereasy.theme.models import PageStructure, structure_dict

PRESETS: dict[str, dict] = {
    "simple": {"layout_hint": "auto", "dark": False},
    "magazine": {"layout_hint": "three-column", "dark": False, "dense": True},
    "dark": {"layout_hint": "two-column", "dark": True},
    "from-image": {"layout_hint": "two-column", "dark": False},
    "portfolio": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": False,
        "accent": "#c4a574",
    },
    "news": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": True,
        "accent": "#b91c1c",
    },
    "personal": {
        "layout_hint": "single-column",
        "dark": False,
        "dense": False,
        "accent": "#7c3aed",
    },
    "docs": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": True,
        "accent": "#0d9488",
    },
    "landing": {
        "layout_hint": "single-column",
        "dark": False,
        "dense": False,
        "accent": "#0ea5e9",
        "landing": True,
    },
    "portfolio_photo": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": False,
        "accent": "#c4a574",
    },
    "food_recipe": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": False,
        "accent": "#d97742",
    },
    "magazine_news": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": True,
        "accent": "#b91c1c",
    },
    "corporate_blue": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": False,
        "accent": "#0055aa",
    },
    # Multi-page site templates
    "home": {
        "layout_hint": "single-column",
        "dark": False,
        "dense": False,
        "accent": "#4cc9f0",
    },
    "about": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": False,
        "accent": "#f72585",
    },
    "contact": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": True,
        "accent": "#4cc9f0",
    },
}


def apply_preset(structure: PageStructure | dict, template: str) -> dict:
    preset = PRESETS.get(template, PRESETS["simple"])
    out = structure_dict(structure)
    if preset.get("layout_hint") in {"two-column", "three-column"}:
        out["layout"] = preset["layout_hint"]
        feats = dict(out.get("features") or {})
        feats["sidebar"] = True
        if preset.get("layout_hint") == "three-column":
            feats["magazine_left_rail"] = True
        out["features"] = feats
    if preset.get("dark"):
        out = apply_dark_variant(out)
    if preset.get("accent") and not preset.get("dark"):
        colors = dict(out.get("colors") or {})
        colors["primary"] = preset["accent"]
        out["colors"] = colors
    if preset.get("dense"):
        feats = dict(out.get("features") or {})
        feats["dense"] = True
        out["features"] = feats
    if preset.get("landing"):
        feats = dict(out.get("features") or {})
        feats["landing"] = True
        feats["sidebar"] = False
        out["features"] = feats
        out["layout"] = "single-column"
    out["template"] = template
    return out


def apply_dark_variant(structure: dict) -> dict:
    out = dict(structure)
    colors = dict(out.get("colors") or {})
    colors.update(
        {
            "background": "#0f172a",
            "text": "#e2e8f0",
            "primary": colors.get("primary") or "#38bdf8",
            "secondary": colors.get("secondary") or "#818cf8",
            "surface": "#111827",
            "muted": "#1e293b",
            "border": "#334155",
            "footer": "#020617",
            "footer_text": "#cbd5e1",
        }
    )
    out["colors"] = colors
    features = dict(out.get("features") or {})
    features["dark"] = True
    out["features"] = features
    return out