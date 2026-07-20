"""Multi-page site generator: coordinated home + about + contact theme set.

Builds a set of importable Blogger XML themes sharing a cohesive design system
(primary colors, fonts, layout structure) across three page types:

  - **home** — landing/blog index with hero + post summaries
  - **about** — bio/story-focused layout with profile section
  - **contact** — contact-form + social links layout

Each page gets its own validated XML file, produced from a shared structure
base so colors, fonts, and layout choices stay coordinated across the set.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from bloggereasy.export.writer import write_theme
from bloggereasy.theme.builder import build_blogger_xml
from bloggereasy.theme.models import PageStructure, structure_dict
from bloggereasy.theme.presets import apply_preset
from bloggereasy.theme.validate import validate_blogger_xml

MULTIPAGE_VERSION = "bloggereasy.multipage.v1"

PAGE_TYPES = ("home", "about", "contact")


def _merge_page_customizations(base: dict, page_type: str) -> dict:
    """Apply page-specific overrides on top of the shared base structure."""
    out = deepcopy(base)

    if page_type == "home":
        title_suffix = ""
        layout = "two-column"
        features = {
            "sidebar": True,
            "footer": True,
            "header": True,
            "widgets": "default",
        }
        nav_links = [
            {"label": "Home", "href": "/"},
            {"label": "About", "href": "/p/about.html"},
            {"label": "Contact", "href": "/p/contact.html"},
        ]
    elif page_type == "about":
        title_suffix = " — About"
        layout = "single-column"
        features = {
            "sidebar": False,
            "footer": True,
            "header": True,
            "widgets": "minimal",
        }
        nav_links = [
            {"label": "Home", "href": "/"},
            {"label": "About", "href": "/p/about.html"},
            {"label": "Contact", "href": "/p/contact.html"},
        ]
    elif page_type == "contact":
        title_suffix = " — Contact"
        layout = "single-column"
        features = {
            "sidebar": False,
            "footer": True,
            "header": True,
            "widgets": "minimal",
        }
        nav_links = [
            {"label": "Home", "href": "/"},
            {"label": "About", "href": "/p/about.html"},
            {"label": "Contact", "href": "/p/contact.html"},
        ]
    else:
        raise ValueError(f"Unknown page type: {page_type!r}. Expected one of {PAGE_TYPES}.")

    out["layout"] = layout
    existing_features = dict(out.get("features") or {})
    existing_features.update(features)
    out["features"] = existing_features
    out["nav_links"] = nav_links

    title = str(out.get("title") or "My Site")
    out["title"] = title + title_suffix

    page_descriptions = {
        "home": f"Welcome to {title} — the latest posts, updates, and insights.",
        "about": f"About {title} — our story, mission, and team.",
        "contact": f"Contact {title} — get in touch, we'd love to hear from you.",
    }
    out["description"] = page_descriptions[page_type]

    return out


def generate_multipage(
    structure: PageStructure | dict,
    out_dir: Path,
    *,
    template: str = "simple",
) -> dict:
    """Generate a coordinated multi-page theme set (home + about + contact).

    Parameters
    ----------
    structure
        Base page structure (from parsed HTML, presets, or manual dict).
        Colors/fonts/layout hints are shared across all three pages.
    out_dir
        Output directory; will be created if it doesn't exist.
    template
        BloggerEasy template name to apply to all pages (e.g. ``"simple"``,
        ``"portfolio"``, ``"corporate_blue"``).

    Returns
    -------
    dict
        Manifest containing version, pages (with paths, bytes, validation),
        shared design tokens, and an overall validation flag.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    base = structure_dict(structure)
    base = apply_preset(base, template)

    shared_tokens = {
        "colors": base.get("colors") or {},
        "fonts": base.get("fonts") or {},
        "template": template,
    }

    pages: dict[str, dict[str, Any]] = {}
    all_ok = True

    for page_type in PAGE_TYPES:
        page_structure = _merge_page_customizations(base, page_type)
        xml = build_blogger_xml(page_structure, template_name=template)
        validation = validate_blogger_xml(xml)
        filename = f"{page_type}.xml"
        file_path = write_theme(xml, out_dir / filename)

        ok = bool(validation.get("ok"))
        if not ok:
            all_ok = False

        pages[page_type] = {
            "file": filename,
            "path": str(file_path),
            "bytes": file_path.stat().st_size,
            "validation": validation,
            "title": page_structure.get("title"),
            "layout": page_structure.get("layout"),
        }

    return {
        "multipage_version": MULTIPAGE_VERSION,
        "template": template,
        "shared_design": shared_tokens,
        "pages": pages,
        "validation_ok": all_ok,
        "out_dir": str(out_dir),
    }
