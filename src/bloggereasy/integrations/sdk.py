from __future__ import annotations

from pathlib import Path

from bloggereasy.export.writer import write_theme
from bloggereasy.parse.fetch import fetch_html_url, save_html
from bloggereasy.parse.html_page import parse_html_file, parse_html_string
from bloggereasy.theme.builder import build_blogger_xml
from bloggereasy.theme.presets import apply_preset
from bloggereasy.theme.validate import validate_blogger_xml
from bloggereasy.vision.palette import structure_from_image


def _build(structure: dict, out_path: Path, *, template: str = "simple", widgets: str = "default") -> dict:
    structure = apply_preset(structure, template)
    if widgets != "default":
        features = dict(structure.get("features") or {})
        features["widgets"] = widgets
        features["sidebar"] = True
        structure["features"] = features
        if structure.get("layout") == "single-column":
            structure["layout"] = "two-column"
    xml = build_blogger_xml(structure, template_name=template)
    validation = validate_blogger_xml(xml)
    path = write_theme(xml, out_path)
    return {
        "integration_version": "bloggereasy.sdk.v1",
        "structure": structure,
        "output": str(path),
        "bytes": path.stat().st_size,
        "validation": validation,
        "import_hint": "Blogger → Theme → Backup/Restore → Upload XML",
    }


def generate_from_html(
    html_path: Path,
    out_path: Path,
    *,
    template: str = "simple",
    widgets: str = "default",
) -> dict:
    structure = parse_html_file(html_path)
    result = _build(structure, out_path, template=template, widgets=widgets)
    result["mode"] = "html"
    return result


def generate_from_html_string(
    html: str,
    out_path: Path,
    *,
    template: str = "simple",
    widgets: str = "default",
) -> dict:
    structure = parse_html_string(html)
    result = _build(structure, out_path, template=template, widgets=widgets)
    result["mode"] = "html_string"
    return result


def generate_from_url(
    url: str,
    out_path: Path,
    *,
    template: str = "simple",
    cache_dir: Path | None = None,
    widgets: str = "default",
) -> dict:
    html = fetch_html_url(url)
    if cache_dir is not None:
        save_html(html, cache_dir / "fetched.html")
    structure = parse_html_string(html, source=url)
    result = _build(structure, out_path, template=template, widgets=widgets)
    result["mode"] = "url"
    result["url"] = url
    return result


def generate_from_image(
    image_path: Path,
    out_path: Path,
    *,
    title: str = "My Blog",
    template: str = "from-image",
    widgets: str = "default",
) -> dict:
    structure = structure_from_image(image_path, title=title)
    result = _build(structure, out_path, template=template, widgets=widgets)
    result["mode"] = "image"
    return result
