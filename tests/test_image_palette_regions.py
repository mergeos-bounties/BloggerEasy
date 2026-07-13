from __future__ import annotations

from pathlib import Path

import pytest

from bloggereasy.vision.palette import structure_from_image


def test_structure_from_image_extracts_region_hints(tmp_path: Path) -> None:
    Image = pytest.importorskip("PIL.Image")
    img = Image.new("RGB", (8, 8), "#ffffff")
    for y in range(0, 2):
        for x in range(8):
            img.putpixel((x, y), (200, 40, 40))
    for y in range(2, 6):
        for x in range(8):
            img.putpixel((x, y), (240, 240, 240))
    for y in range(6, 8):
        for x in range(8):
            img.putpixel((x, y), (20, 40, 80))
    path = tmp_path / "mockup.png"
    img.save(path)

    structure = structure_from_image(path, title="Regional Blog")

    assert structure["title"] == "Regional Blog"
    assert structure["colors"]["primary"] == "#c02020"
    assert structure["colors"]["background"] == "#e0e0e0"
    assert structure["colors"]["footer"] == "#002040"
    assert structure["image_regions"] == {
        "header": "#c02020",
        "content": "#e0e0e0",
        "footer": "#002040",
    }


def test_structure_from_bad_image_keeps_default_palette(tmp_path: Path) -> None:
    path = tmp_path / "bad.png"
    path.write_bytes(b"not an image")

    structure = structure_from_image(path, title="Fallback Blog")

    assert structure["title"] == "Fallback Blog"
    assert structure["colors"]["primary"] == "#2563eb"
    assert structure["from_image"] is True
