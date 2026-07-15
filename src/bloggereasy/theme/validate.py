from __future__ import annotations

import re
from pathlib import Path


XHTML_NS = "http://www.w3.org/1999/xhtml"
B_NS = "http://www.google.com/2005/gml/b"


def _has_namespace(xml: str, namespace: str) -> bool:
    escaped_ns = re.escape(namespace)
    pattern = "xmlns(?::[a-zA-Z0-9_-]+)?\\s*=\\s*(['\\\"])\\b" + escaped_ns + "\\b\\1"
    return re.search(pattern, xml, flags=re.IGNORECASE) is not None


def validate_blogger_xml(xml: str, *, strict: bool = False) -> dict:
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

    # Strict mode: additional checks
    if strict:
        xml_bytes = len(xml.encode("utf-8"))
        if xml_bytes < 2000:
            errors.append("strict: theme XML below 2000 byte floor (likely incomplete)")
        if "<b:includable" not in xml:
            errors.append("strict: missing <b:includable> blocks (widget templates incomplete)")
        if "CDATA" not in xml:
            errors.append("strict: missing CDATA skin block (CSS not properly wrapped)")
        if "<head>" not in xml.lower():
            errors.append("strict: missing <head> element")
        if "viewport" not in xml.lower():
            warnings.append("strict: no viewport meta tag (responsive breakpoints may fail)")
        if "charset" not in xml.lower():
            errors.append("strict: missing charset declaration")
        if not re.search(r"<meta\b[^>]*\bog:title\b", xml, flags=re.IGNORECASE):
            warnings.append("strict: missing og:title meta tag (social sharing preview degraded)")
        if len(re.findall(r"<b:section\b", xml)) < 3:
            warnings.append("strict: fewer than 3 <b:section> blocks (layout may be sparse)")

    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "bytes": len(xml.encode("utf-8")),
        "strict": strict,
    }


def validate_theme_file(path: Path, *, strict: bool = False) -> dict:
    xml = path.read_text(encoding="utf-8", errors="replace")
    result = validate_blogger_xml(xml, strict=strict)
    result["path"] = str(path)
    return result
