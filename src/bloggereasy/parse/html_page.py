from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup

from bloggereasy.parse.css import extract_css_skin
from bloggereasy.parse.normalize import normalize_export_html


def parse_html_file(path: Path) -> dict:
    html = path.read_text(encoding="utf-8", errors="replace")
    return parse_html_string(html, source=str(path))


def parse_html_string(html: str, source: str = "inline") -> dict:
    html, normalize_report = normalize_export_html(html)
    soup = BeautifulSoup(html, "lxml")

    title = _text(soup.title) if soup.title else ""
    if not title and soup.find("h1"):
        title = _text(soup.find("h1"))

    description = ""
    meta = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    if meta and meta.get("content"):
        description = str(meta["content"]).strip()

    nav_links = []
    for a in soup.select("nav a, header a, .nav a, .menu a")[:20]:
        label = _text(a)
        href = a.get("href") or "#"
        if label:
            nav_links.append({"label": label, "href": href})

    headings = [_text(h) for h in soup.find_all(["h1", "h2", "h3"])[:12] if _text(h)]
    paragraphs = [_text(p) for p in soup.find_all("p")[:8] if _text(p)]

    colors = _extract_colors(html)
    skin = extract_css_skin(html)
    fonts = skin["fonts"]
    has_sidebar = bool(
        soup.select_one("aside, .sidebar, #sidebar, .widget-area, [class*='sidebar']")
    )
    has_footer = bool(soup.find("footer") or soup.select_one(".footer, #footer"))
    has_header = bool(soup.find("header") or soup.select_one(".header, #header"))

    layout = "two-column" if has_sidebar else "single-column"

    return {
        "source": source,
        "title": title or "My Blog",
        "description": description,
        "nav_links": nav_links,
        "headings": headings,
        "sample_paragraphs": paragraphs,
        "colors": colors,
        "fonts": fonts,
        "skin": skin,
        "layout": layout,
        "features": {
            "header": has_header,
            "sidebar": has_sidebar,
            "footer": has_footer,
            "nav_count": len(nav_links),
        },
        "normalize": normalize_report,
    }


def _text(el) -> str:
    if el is None:
        return ""
    return " ".join(el.get_text(" ", strip=True).split())


def _extract_colors(html: str) -> dict:
    hexes = re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", html)
    # normalize 3-digit
    norm: list[str] = []
    for h in hexes:
        h = h.lower()
        if len(h) == 4:
            h = "#" + "".join(c * 2 for c in h[1:])
        if h not in norm:
            norm.append(h)
    primary = norm[0] if norm else "#1a73e8"
    secondary = norm[1] if len(norm) > 1 else "#34a853"
    background = next((c for c in norm if c in {"#ffffff", "#fff", "#fafafa", "#f5f5f5"}), "#ffffff")
    if background == "#fff":
        background = "#ffffff"
    text = next((c for c in norm if c in {"#000000", "#111111", "#222222", "#333333"}), "#222222")
    return {
        "primary": primary,
        "secondary": secondary,
        "background": background if background.startswith("#") else "#ffffff",
        "text": text,
        "palette": norm[:8],
    }


def _extract_fonts(html: str, soup: BeautifulSoup) -> dict:
    families = re.findall(r"font-family\s*:\s*([^;}{]+)", html, flags=re.I)
    cleaned = []
    for fam in families:
        first = fam.split(",")[0].strip().strip("'\"")
        if first and first.lower() not in {"inherit", "initial"} and first not in cleaned:
            cleaned.append(first)
    body_font = cleaned[0] if cleaned else "system-ui, sans-serif"
    heading_font = cleaned[1] if len(cleaned) > 1 else body_font
    return {"body": body_font, "heading": heading_font}
