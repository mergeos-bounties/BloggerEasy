"""Tests for #79: validate --strict schema mode."""
from __future__ import annotations

from bloggereasy.theme.validate import validate_blogger_xml


def test_strict_mode_rejects_small_xml() -> None:
    """Strict mode flags XML below 2000 bytes."""
    tiny = '<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:b="http://www.google.com/2005/gml/b"><head></head><body></body></html>'
    result = validate_blogger_xml(tiny, strict=True)
    assert any("2000 byte floor" in e for e in result["errors"]), f"Should flag small XML: {result}"


def test_non_strict_accepts_small_xml() -> None:
    """Non-strict mode only warns about small XML size."""
    tiny = '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:b="http://www.google.com/2005/gml/b"><head></head><body></body></html>'
    result = validate_blogger_xml(tiny, strict=False)
    assert any("unusually small" in w for w in result["warnings"]), f"Should warn about small XML: {result['warnings']}"


def test_strict_mode_checks_cdata() -> None:
    """Strict mode flags missing CDATA."""
    xml = '<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:b="http://www.google.com/2005/gml/b"><head></head><body><b:section id="main"><b:widget id="Blog1" type="Blog" version="1"><b:includable id="main"></b:includable></b:widget></b:section></body></html>'
    result = validate_blogger_xml(xml, strict=True)
    assert any("CDATA" in e for e in result["errors"]), f"Should flag missing CDATA: {result}"


def test_strict_checks_preserved_in_non_strict() -> None:
    """Non-strict mode does not apply strict checks."""
    tiny = '<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:b="http://www.google.com/2005/gml/b"><head></head><body></body></html>'
    result = validate_blogger_xml(tiny, strict=False)
    # strict checks should NOT appear
    for err in result["errors"]:
        assert "strict:" not in err, f"Strict check leaked into non-strict: {err}"
