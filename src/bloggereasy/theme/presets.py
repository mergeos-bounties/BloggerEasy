from __future__ import annotations

from bloggereasy.theme.models import PageStructure, structure_dict

PRESETS: dict[str, dict] = {
    "simple": {"layout_hint": "auto", "dark": False, "notes": "Clean universal starting point"},
    "magazine": {"layout_hint": "three-column", "dark": False, "dense": True, "notes": "Three-column news/magazine layout"},
    "dark": {"layout_hint": "two-column", "dark": True, "notes": "Dark mode developer/devops look"},
    "from-image": {"layout_hint": "two-column", "dark": False, "notes": "Derive palette from image"},
    "portfolio": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": False,
        "accent": "#c4a574",
        "notes": "Warm portfolio/showcase accent",
    },
    "news": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": True,
        "accent": "#b91c1c",
        "notes": "Dense news portal with red accent",
    },
    "personal": {
        "layout_hint": "single-column",
        "dark": False,
        "dense": False,
        "accent": "#7c3aed",
        "notes": "Personal blog with purple accent",
    },
    "docs": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": True,
        "accent": "#0d9488",
        "notes": "Documentation-style with teal accent",
    },
    "portfolio_photo": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": False,
        "accent": "#c4a574",
        "notes": "Photography portfolio warm accent",
    },
    "food_recipe": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": False,
        "accent": "#d97742",
        "notes": "Food blog with orange accent",
    },
    "magazine_news": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": True,
        "accent": "#b91c1c",
        "notes": "News magazine with bold red accent",
    },
    "corporate_blue": {
        "layout_hint": "two-column",
        "dark": False,
        "dense": False,
        "accent": "#0055aa",
        "notes": "Corporate blue professional style",
    },
}

PRESET_TAGS: dict[str, list[str]] = {
    "simple": ["light", "blog", "minimal"],
    "magazine": ["light", "blog", "dense", "magazine"],
    "dark": ["dark", "blog", "dev"],
    "from-image": ["light", "blog", "creative"],
    "portfolio": ["light", "portfolio", "creative"],
    "news": ["light", "blog", "dense", "news"],
    "personal": ["light", "blog", "personal"],
    "docs": ["light", "docs", "dense"],
    "portfolio_photo": ["light", "portfolio", "creative"],
    "food_recipe": ["light", "blog", "creative", "food"],
    "magazine_news": ["light", "blog", "dense", "news", "magazine"],
    "corporate_blue": ["light", "blog", "corporate"],
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


def tokens_for_preset(template: str) -> dict:
    """Extract design tokens (CSS custom properties) from a template preset."""
    if template not in PRESETS:
        available = sorted(PRESETS.keys())
        raise ValueError(f"Unknown template '{template}'. Available: {', '.join(available)}")

    preset = PRESETS[template]
    tokens: dict[str, str] = {}

    # Base colors
    tokens["--color-primary"] = preset.get("accent") or "#1a73e8"
    tokens["--color-secondary"] = "#34a853"

    if preset.get("dark"):
        tokens["--color-background"] = "#0f172a"
        tokens["--color-text"] = "#e2e8f0"
        tokens["--color-surface"] = "#111827"
        tokens["--color-muted"] = "#1e293b"
        tokens["--color-border"] = "#334155"
        tokens["--color-footer"] = "#020617"
        tokens["--color-footer-text"] = "#cbd5e1"
    else:
        tokens["--color-background"] = "#ffffff"
        tokens["--color-text"] = "#222222"
        tokens["--color-surface"] = "#ffffff"
        tokens["--color-muted"] = "#f8fafc"
        tokens["--color-border"] = "#e5e7eb"
        tokens["--color-footer"] = "#0f172a"
        tokens["--color-footer-text"] = "#e2e8f0"

    # Typography
    tokens["--font-body"] = "system-ui, sans-serif"
    tokens["--font-heading"] = "system-ui, sans-serif"

    # Layout
    layout = preset.get("layout_hint", "single-column")
    tokens["--layout"] = layout
    tokens["--layout-sidebar"] = str(layout in {"two-column", "three-column"}).lower()

    # Spacing
    if preset.get("dense"):
        tokens["--spacing-post-pad"] = "0.6rem 0.85rem"
        tokens["--spacing-content-pad"] = "0.5rem"
        tokens["--spacing-gap"] = "1rem"
    else:
        tokens["--spacing-post-pad"] = "1rem 1.25rem"
        tokens["--spacing-content-pad"] = "1rem"
        tokens["--spacing-gap"] = "1.5rem"

    tokens["--spacing-radius"] = "8px"
    tokens["--spacing-button-radius"] = "6px"

    return {
        "template": template,
        "tags": PRESET_TAGS.get(template, []),
        "dark": preset.get("dark", False),
        "dense": preset.get("dense", False),
        "features": {
            "sidebar": layout in {"two-column", "three-column"},
            "magazine_left_rail": layout == "three-column",
            "dark": preset.get("dark", False),
            "dense": preset.get("dense", False),
        },
        "tokens": tokens,
    }
