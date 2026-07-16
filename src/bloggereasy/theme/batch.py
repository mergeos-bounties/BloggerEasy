"""Batch validate theme XML files under a directory."""

from __future__ import annotations

from pathlib import Path

from bloggereasy.theme.validate import validate_theme_file


def validate_theme_dir(directory: Path) -> dict:
    files = sorted(directory.glob("*.xml")) if directory.exists() else []
    rows = []
    ok_n = 0
    for path in files:
        result = validate_theme_file(path)
        ok = bool(result.get("ok"))
        if ok:
            ok_n += 1
        rows.append(
            {
                "file": path.name,
                "ok": ok,
                "issues": result.get("issues") or result.get("errors") or [],
            }
        )
    return {
        "dir": str(directory),
        "n": len(files),
        "ok": ok_n,
        "fail": len(files) - ok_n,
        "rows": rows,
    }
