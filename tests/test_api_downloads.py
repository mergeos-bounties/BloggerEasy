from __future__ import annotations

from io import BytesIO

import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from bloggereasy.api.app import app

client = TestClient(app)


def test_gen_html_download_returns_xml_attachment() -> None:
    html = """
    <html><head><title>Download Blog</title></head>
    <body><h1>Download Blog</h1><p>XML download endpoint.</p></body></html>
    """

    response = client.post("/gen/html/download", json={"html": html, "template": "simple"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    assert response.headers["content-disposition"] == 'attachment; filename="download-blog.xml"'
    assert "<?xml" in response.text
    assert "b:skin" in response.text


def test_gen_image_download_returns_xml_attachment() -> None:
    Image = pytest.importorskip("PIL.Image")
    img = Image.new("RGB", (32, 16), color=(80, 120, 200))
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    response = client.post(
        "/gen/image/download",
        files={"file": ("mockup.png", buf, "image/png")},
        data={"template": "from-image", "title": "Image Download"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    assert response.headers["content-disposition"] == 'attachment; filename="image-download.xml"'
    assert "<?xml" in response.text
    assert "b:skin" in response.text
