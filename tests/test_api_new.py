"""Tests for new web UI endpoints: GET / and POST /gen/image."""

from __future__ import annotations

import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from bloggereasy.api.app import app

client = TestClient(app)


def test_index_returns_html() -> None:
    """GET / should serve the web UI HTML page."""
    r = client.get("/")
    assert r.status_code == 200
    assert "<!DOCTYPE html>" in r.text
    assert "BloggerEasy" in r.text
    assert "Paste HTML" in r.text or "Upload image" in r.text


def test_gen_image_endpoint() -> None:
    """POST /gen/image should accept a PNG and return Blogger XML."""
    # Create a minimal PNG in memory
    from io import BytesIO
    from PIL import Image

    img = Image.new("RGB", (200, 100), color=(80, 120, 200))
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    r = client.post(
        "/gen/image",
        files={"file": ("test.png", buf, "image/png")},
        data={"template": "from-image", "title": "Test Blog"},
    )
    assert r.status_code == 200
    xml = r.text
    assert "<?xml" in xml
    assert "b:skin" in xml or "<html" in xml


def test_gen_image_rejects_invalid_template() -> None:
    """POST /gen/image should reject unknown template."""
    from io import BytesIO
    from PIL import Image

    img = Image.new("RGB", (100, 50), color=(0, 0, 0))
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    r = client.post(
        "/gen/image",
        files={"file": ("x.png", buf, "image/png")},
        data={"template": "nonexistent"},
    )
    assert r.status_code == 400
