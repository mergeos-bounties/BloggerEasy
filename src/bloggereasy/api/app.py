from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from bloggereasy import __version__
from bloggereasy.integrations.sdk import (
    generate_from_html,
    generate_from_html_string,
    generate_from_image,
)
from bloggereasy.theme.presets import PRESETS
from bloggereasy.theme.preview import structure_to_preview_html

try:
    from fastapi import FastAPI, File, Form, HTTPException, UploadFile
    from fastapi.responses import HTMLResponse, Response, PlainTextResponse
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover
    raise ImportError("Install bloggereasy[api] for FastAPI support") from exc

_STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(title="BloggerEasy", version=__version__)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Web UI: paste HTML / upload image and download Blogger XML."""
    index_html = _STATIC_DIR / "index.html"
    if index_html.exists():
        return index_html.read_text(encoding="utf-8")
    return "<h1>BloggerEasy</h1><p>POST to /gen/html or /gen/image. See /docs for the API.</p>"


class HtmlGenRequest(BaseModel):
    html: str = Field(..., min_length=20)
    template: str = "simple"
    title_hint: str | None = None


@app.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "service": "bloggereasy",
        "version": __version__,
        "templates": list(PRESETS),
    }


@app.post("/gen/html")
def gen_html(req: HtmlGenRequest) -> dict:
    if req.template not in PRESETS:
        raise HTTPException(400, f"unknown template {req.template}")
    with TemporaryDirectory() as tmp:
        out = Path(tmp) / "theme.xml"
        result = generate_from_html_string(req.html, out, template=req.template)
        xml = out.read_text(encoding="utf-8")
    return {
        "ok": result["validation"]["ok"],
        "validation": result["validation"],
        "title": result["structure"].get("title"),
        "layout": result["structure"].get("layout"),
        "xml": xml,
        "import_hint": result["import_hint"],
        "preview_html": structure_to_preview_html(result["structure"]),
    }


@app.post("/gen/html/raw", response_class=PlainTextResponse)
def gen_html_raw(req: HtmlGenRequest) -> str:
    data = gen_html(req)
    if not data["ok"]:
        raise HTTPException(400, detail=data["validation"])
    return data["xml"]


@app.post("/gen/html/download")
def gen_html_download(req: HtmlGenRequest) -> Response:
    data = gen_html(req)
    if not data["ok"]:
        raise HTTPException(400, detail=data["validation"])
    filename = _download_filename(data.get("title") or "bloggereasy-theme")
    return Response(
        content=data["xml"],
        media_type="application/xml",
        headers={"Content-Disposition": f'attachment; filename="{filename}.xml"'},
    )


@app.post("/gen/html/multipart")
async def gen_html_multipart(
    file: UploadFile = File(...),
    template: str = Form("simple"),
) -> dict:
    """Upload an HTML file (multipart) and receive Blogger XML + static preview."""
    if template not in PRESETS:
        raise HTTPException(400, f"unknown template {template}")
    raw = await file.read()
    try:
        html = raw.decode("utf-8")
    except UnicodeDecodeError:
        html = raw.decode("latin-1", errors="replace")
    if len(html.strip()) < 20:
        raise HTTPException(400, "HTML too short")
    with TemporaryDirectory() as tmp:
        src = Path(tmp) / (file.filename or "upload.html")
        src.write_text(html, encoding="utf-8")
        out = Path(tmp) / "theme.xml"
        result = generate_from_html(src, out, template=template)
        xml = out.read_text(encoding="utf-8")
    return {
        "ok": result["validation"]["ok"],
        "validation": result["validation"],
        "filename": file.filename,
        "title": result["structure"].get("title"),
        "xml": xml,
        "preview_html": structure_to_preview_html(result["structure"]),
        "import_hint": result["import_hint"],
    }


@app.post("/preview/html", response_class=HTMLResponse)
def preview_html(req: HtmlGenRequest) -> str:
    if req.template not in PRESETS:
        raise HTTPException(400, f"unknown template {req.template}")
    with TemporaryDirectory() as tmp:
        out = Path(tmp) / "theme.xml"
        result = generate_from_html_string(req.html, out, template=req.template)
    return structure_to_preview_html(result["structure"])


@app.post("/gen/image", response_class=PlainTextResponse)
async def gen_image(
    file: UploadFile = File(...),
    template: str = Form("from-image"),
    title: str = Form("My Blog"),
) -> str:
    """Upload an image (PNG/JPG) and receive a Blogger XML theme inferred from the design."""
    if template not in PRESETS:
        raise HTTPException(400, f"unknown template {template}")
    with TemporaryDirectory() as tmp:
        src = Path(tmp) / (file.filename or "upload.png")
        src.write_bytes(await file.read())
        out = Path(tmp) / "theme.xml"
        generate_from_image(src, out, title=title, template=template)
        xml = out.read_text(encoding="utf-8")
    return xml


@app.post("/gen/image/download")
async def gen_image_download(
    file: UploadFile = File(...),
    template: str = Form("from-image"),
    title: str = Form("My Blog"),
) -> Response:
    xml = await gen_image(file=file, template=template, title=title)
    filename = _download_filename(title or "image-theme")
    return Response(
        content=xml,
        media_type="application/xml",
        headers={"Content-Disposition": f'attachment; filename="{filename}.xml"'},
    )


def _download_filename(title: str) -> str:
    safe = "".join(ch.lower() if ch.isalnum() else "-" for ch in title).strip("-")
    while "--" in safe:
        safe = safe.replace("--", "-")
    return safe or "bloggereasy-theme"
