from __future__ import annotations

import re
from typing import Any


def extract_css_skin(html: str) -> dict[str, Any]:
    css = _collect_css(html)
    fonts = _extract_fonts(css)
    spacing = _extract_spacing(css)
    buttons = _extract_button_styles(css)
    return {
        "fonts": fonts,
        "spacing": spacing,
        "buttons": buttons,
        "rule_count": css.count("{"),
    }


def _collect_css(html: str) -> str:
    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.I | re.S)
    inline_styles = re.findall(r"\sstyle=[\"']([^\"']+)[\"']", html, flags=re.I)
    return "\n".join([*style_blocks, *inline_styles])


def _extract_fonts(css: str) -> dict[str, str]:
    families = re.findall(r"font-family\s*:\s*([^;}{]+)", css, flags=re.I)
    cleaned: list[str] = []
    for family in families:
        first = family.split(",")[0].strip().strip("'\"")
        if first and first.lower() not in {"inherit", "initial"} and first not in cleaned:
            cleaned.append(first)
    body = cleaned[0] if cleaned else "system-ui, sans-serif"
    heading = cleaned[1] if len(cleaned) > 1 else body
    return {"body": body, "heading": heading}


def _extract_spacing(css: str) -> dict[str, str]:
    return {
        "section_padding": _first_css_value(css, "padding", "1rem"),
        "card_padding": _first_css_value(css, "padding", "1rem 1.25rem", selector_hint="card|post|article"),
        "gap": _first_css_value(css, "gap", "1.5rem"),
        "radius": _first_css_value(css, "border-radius", "8px"),
    }


def _extract_button_styles(css: str) -> dict[str, str]:
    block = _first_block(css, r"(?:button|\.btn|\.button|a\.button)[^{]*")
    return {
        "background": _first_css_value(block, "background(?:-color)?", "#1a73e8"),
        "color": _first_css_value(block, "color", "#ffffff"),
        "padding": _first_css_value(block, "padding", "0.55rem 0.9rem"),
        "radius": _first_css_value(block, "border-radius", "6px"),
    }


def _first_css_value(
    css: str,
    property_name: str,
    default: str,
    *,
    selector_hint: str | None = None,
) -> str:
    haystack = css
    if selector_hint:
        hinted = _first_block(css, rf"[^{{]*(?:{selector_hint})[^{{]*")
        if hinted:
            haystack = hinted
    match = re.search(rf"{property_name}\s*:\s*([^;}}{{]+)", haystack, flags=re.I)
    return match.group(1).strip() if match else default


def _first_block(css: str, selector_pattern: str) -> str:
    match = re.search(rf"{selector_pattern}\{{([^}}]+)\}}", css, flags=re.I | re.S)
    return match.group(1) if match else ""
