from __future__ import annotations

from pathlib import Path
from typing import Iterable


def structure_from_image(path: Path, *, title: str = "My Blog") -> dict:
    """
    Build a theme structure from an image.

    With optional Pillow, extracts a simple color palette.
    Without vision deps, returns a sensible default scaffold.
    """
    colors = _default_colors()
    try:
        from PIL import Image

        img = Image.open(path).convert("RGB")
        img = img.resize((64, 64))
        pixels = list(img.getdata())
        hexes = _dominant_hexes(pixels)
        regions = {
            "header": _dominant_hexes(_region_pixels(img, 0.0, 0.25), limit=1)[0],
            "content": _dominant_hexes(_region_pixels(img, 0.25, 0.8), limit=1)[0],
            "footer": _dominant_hexes(_region_pixels(img, 0.8, 1.0), limit=1)[0],
        }
        if hexes:
            colors = {
                "primary": regions["header"],
                "secondary": hexes[1] if len(hexes) > 1 else hexes[0],
                "background": regions["content"],
                "text": "#222222",
                "palette": hexes,
                "header": regions["header"],
                "content_bg": regions["content"],
                "footer": regions["footer"],
            }
    except Exception:
        # Pillow missing or unreadable image — keep defaults
        pass

    return {
        "source": str(path),
        "title": title or path.stem.replace("_", " ").title(),
        "description": f"Theme scaffold from image {path.name}",
        "nav_links": [
            {"label": "Home", "href": "#"},
            {"label": "Posts", "href": "#"},
            {"label": "About", "href": "#"},
        ],
        "headings": [],
        "sample_paragraphs": [],
        "colors": colors,
        "fonts": {"body": "system-ui, sans-serif", "heading": "Georgia, serif"},
        "layout": "two-column",
        "features": {"header": True, "sidebar": True, "footer": True, "nav_count": 3},
        "image_regions": colors.get("header")
        and {
            "header": colors.get("header"),
            "content": colors.get("content_bg"),
            "footer": colors.get("footer"),
        },
        "from_image": True,
    }


def _default_colors() -> dict:
    return {
        "primary": "#2563eb",
        "secondary": "#0ea5e9",
        "background": "#ffffff",
        "text": "#0f172a",
        "palette": ["#2563eb", "#0ea5e9", "#ffffff", "#0f172a"],
    }


def _dominant_hexes(pixels: Iterable[tuple[int, int, int]], *, limit: int = 6) -> list[str]:
    buckets: dict[tuple[int, int, int], int] = {}
    for r, g, b in pixels:
        key = (r // 32 * 32, g // 32 * 32, b // 32 * 32)
        buckets[key] = buckets.get(key, 0) + 1
    ranked = sorted(buckets.items(), key=lambda kv: kv[1], reverse=True)
    hexes = [f"#{r:02x}{g:02x}{b:02x}" for (r, g, b), _ in ranked[:limit]]
    return hexes or _default_colors()["palette"][:limit]


def _region_pixels(img, start: float, end: float) -> list[tuple[int, int, int]]:
    width, height = img.size
    y0 = max(0, min(height - 1, int(height * start)))
    y1 = max(y0 + 1, min(height, int(height * end)))
    return [img.getpixel((x, y)) for y in range(y0, y1) for x in range(width)]
