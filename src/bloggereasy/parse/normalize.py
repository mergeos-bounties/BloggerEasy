"""Normalize messy exported HTML (Figma / site exporters) before theme gen.

Design-tool and site exporters emit HTML with quirks that break or bloat theme
generation:

- ``<script>`` tags (tracking, hydration) — unsafe and useless in a Blogger theme
- Enormous inline ``<style>`` blocks and ``style="..."`` attributes — bloat
- Absolute filesystem / localhost paths in ``src``/``href`` — dead links

``normalize_export_html`` returns cleaned HTML plus a report of what changed so
callers (and tests) can assert on the transformation.
"""

from __future__ import annotations

import re

# Cap a single inline <style> block; larger blocks are truncated with a marker.
MAX_INLINE_CSS = 20_000

_SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL)
_SCRIPT_SELFCLOSE_RE = re.compile(r"<script\b[^>]*/>", re.IGNORECASE)
_STYLE_BLOCK_RE = re.compile(r"(<style\b[^>]*>)(.*?)(</style>)", re.IGNORECASE | re.DOTALL)
_STYLE_ATTR_RE = re.compile(r'\sstyle="[^"]*"', re.IGNORECASE)
# absolute file / localhost / windows paths in src/href
_ABS_PATH_RE = re.compile(
    r'((?:src|href)\s*=\s*")'
    r'(file://[^"]*|[A-Za-z]:\\[^"]*|https?://localhost[^"]*|https?://127\.0\.0\.1[^"]*)'
    r'"',
    re.IGNORECASE,
)


def normalize_export_html(html: str, *, strip_inline_style_attrs: bool = False) -> tuple[str, dict]:
    """Clean exported HTML. Returns ``(clean_html, report)``.

    - Removes all ``<script>`` tags (paired and self-closing).
    - Truncates any inline ``<style>`` block larger than ``MAX_INLINE_CSS``.
    - Rewrites absolute file/localhost paths in ``src``/``href`` to ``#``.
    - Optionally strips ``style="..."`` attributes (off by default so color
      extraction from inline styles still works).
    """
    report = {
        "scripts_removed": 0,
        "style_blocks_truncated": 0,
        "abs_paths_rewritten": 0,
        "style_attrs_removed": 0,
        "original_bytes": len(html.encode("utf-8")),
    }

    # 1. strip scripts
    html, n = _SCRIPT_RE.subn("", html)
    report["scripts_removed"] += n
    html, n = _SCRIPT_SELFCLOSE_RE.subn("", html)
    report["scripts_removed"] += n

    # 2. cap huge inline CSS
    def _cap(m: re.Match) -> str:
        open_tag, css, close_tag = m.group(1), m.group(2), m.group(3)
        if len(css) > MAX_INLINE_CSS:
            report["style_blocks_truncated"] += 1
            css = css[:MAX_INLINE_CSS] + "\n/* …truncated by BloggerEasy export adapter… */\n"
        return f"{open_tag}{css}{close_tag}"

    html = _STYLE_BLOCK_RE.sub(_cap, html)

    # 3. rewrite absolute/localhost paths
    html, n = _ABS_PATH_RE.subn(r'\1#"', html)
    report["abs_paths_rewritten"] += n

    # 4. optional: strip inline style attrs
    if strip_inline_style_attrs:
        html, n = _STYLE_ATTR_RE.subn("", html)
        report["style_attrs_removed"] += n

    report["clean_bytes"] = len(html.encode("utf-8"))
    return html, report
