from __future__ import annotations

PRESETS: dict[str, dict] = {
    "simple": {"layout_hint": "auto", "dark": False},
    "magazine": {"layout_hint": "two-column", "dark": False, "dense": True},
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
}


def apply_preset(structure: dict, template: str) -> dict:
    preset = PRESETS.get(template, PRESETS["simple"])
    out = dict(structure)
    if preset.get("layout_hint") == "two-column":
        out["layout"] = "two-column"
        feats = dict(out.get("features") or {})
        feats["sidebar"] = True
        out["features"] = feats
    if preset.get("dark"):
        colors = dict(out.get("colors") or {})
        colors["background"] = "#0f172a"
        colors["text"] = "#e2e8f0"
        colors["primary"] = colors.get("primary") or "#38bdf8"
        colors["secondary"] = colors.get("secondary") or "#818cf8"
        out["colors"] = colors
    if preset.get("accent") and not preset.get("dark"):
        colors = dict(out.get("colors") or {})
        colors["primary"] = preset["accent"]
        out["colors"] = colors
    if preset.get("dense"):
        feats = dict(out.get("features") or {})
        feats["dense"] = True
        out["features"] = feats
    out["template"] = template
    return out
