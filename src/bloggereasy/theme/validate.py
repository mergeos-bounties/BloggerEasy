from __future__ import annotations

from pathlib import Path


REQUIRED_SNIPPETS = (
    "xmlns:b=",
    "b:skin",
    "type='Blog'",
    "<b:section",
    "b:widget",
)


def validate_blogger_xml(xml: str) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    if not xml.strip().startswith("<?xml"):
        warnings.append("missing XML declaration")
    for snip in REQUIRED_SNIPPETS:
        if snip not in xml and snip.replace("'", '"') not in xml:
            # Blog type may use double quotes
            if snip == "type='Blog'" and ('type="Blog"' in xml or "type='Blog'" in xml):
                continue
            if snip not in xml:
                errors.append(f"missing required snippet: {snip}")
    if "Header" not in xml:
        warnings.append("no Header widget title found")
    if len(xml) < 800:
        warnings.append("theme XML is unusually small")
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
