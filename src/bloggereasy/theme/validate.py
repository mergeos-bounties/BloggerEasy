from __future__ import annotations

import re
from pathlib import Path


XHTML_NS = "http://www.w3.org/1999/xhtml"
B_NS = "http://www.google.com/2005/gml/b"
_EXTERNAL_ASSET_RE = re.compile(
    r"<(?P<tag>img|script)\b[^>]*\bsrc\s*=\s*(?P<quote>['\"])(?P<url>https?://[^'\"]+)(?P=quote)",
    flags=re.IGNORECASE,
)


def _has_namespace(xml: str, namespace: str) -> bool:
    pattern = rf"xmlns(?::[a-zA-Z0-9_-]+)?\s*=\s*(['\"]){re.escape(namespace)}\1"
    return re.search(pattern, xml, flags=re.IGNORECASE) is not None


def _external_asset_warnings(xml: str) -> list[str]:
    return [
        f"external {match.group('tag').lower()} asset URL: {match.group('url').strip()}"
        for match in _EXTERNAL_ASSET_RE.finditer(xml)
    ]


def validate_blogger_xml(xml: str) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    stripped = xml.strip()
    if not stripped.startswith("<?xml"):
        warnings.append("missing XML declaration")

    if "<html" not in stripped.lower():
        errors.append("missing <html> root element")
        return {
            "ok": False,
            "errors": errors,
            "warnings": warnings,
            "bytes": len(xml.encode("utf-8")),
        }

    if not _has_namespace(xml, XHTML_NS):
        errors.append("missing XHTML namespace on <html>")
    if not _has_namespace(xml, B_NS):
        errors.append("missing b namespace on <html>")
    if "b:skin" not in xml:
        errors.append("missing <b:skin> theme stylesheet block")
    if "<b:section" not in xml:
        errors.append("missing required <b:section> layout block")
    if not re.search(r"type\s*=\s*(['\"])Blog\1", xml, flags=re.IGNORECASE):
        errors.append("missing Blog widget")
    if not re.search(r"title\s*=\s*(['\"]).*Header.*\1", xml, flags=re.IGNORECASE | re.DOTALL):
        warnings.append("no Header widget title found")
    if len(xml) < 800:
        warnings.append("theme XML is unusually small")
    warnings.extend(_external_asset_warnings(xml))
    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "bytes": len(xml.encode("utf-8")),
    }


def validate_theme_file(path: Path) -> dict:
    xml = path.read_text(encoding="utf-8", errors="replace")
    result = validate_blogger_xml(xml)
    result["path"] = str(path)
    return result
