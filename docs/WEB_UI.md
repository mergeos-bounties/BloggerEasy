# BloggerEasy Web UI

**Paste HTML / Upload Image → Download Blogger XML Theme**

A modern web interface for converting HTML designs and images into valid Blogger XML themes, ready for import into Blogger.com.

## Features

- **Paste HTML** — Directly paste an HTML document (blog design, landing page, etc.) and convert to Blogger theme XML
- **Upload Image** — Upload a screenshot or design image; the system infers a theme structure from the visual layout
- **Template Presets** — Choose from bundled templates: `simple`, `magazine`, `portfolio`, `from-image`, `dark`, `news`
- **Live Preview** — See a static HTML preview of how your theme will render
- **One-Click Download** — Export the generated XML file directly to your machine
- **Validation Feedback** — Real-time validation warnings and success status

## Getting Started

### Run the Web Server

```bash
# Install extras (FastAPI + Uvicorn)
pip install -e ".[api]"

# Start the server
uvicorn bloggereasy.api.app:app --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 in your browser.

### Step 1: Source

Choose your input mode:
- **Paste HTML** — Paste a full HTML document (minimum 20 characters)
- **Upload Image** — Select a PNG/JPG of a website design

Select a template from the dropdown. The `from-image` template is automatically used when uploading images.

### Step 2: Generate

Click the **"Generate Blogger XML ⬇"** button. The system will:
1. Parse and validate your input
2. Build a Blogger-compatible XML structure
3. Extract metadata (title, layout type)
4. Generate a static HTML preview

### Step 3: Review & Download

- **XML Output** — The generated Blogger theme XML appears in the result panel
- **Preview** — Expand "Preview HTML" to see how your theme will render
- **Status** — Green text = valid and ready. Yellow/Red = warnings or errors (usually safe to proceed)
- **Download** — Click "Download theme.xml" to save the file

## Import into Blogger

1. Go to **Blogger.com → Settings → Theme**
2. Click **"Edit HTML"**
3. Replace all content with your downloaded `theme.xml`
4. Click **"Update"**

Your custom theme is now live.

## API Endpoints

All endpoints are also available programmatically:

| Endpoint | Method | Input | Output |
|----------|--------|-------|--------|
| `/` | GET | — | HTML web UI |
| `/gen/html` | POST | JSON: `{html, template, title_hint}` | JSON: `{ok, xml, preview_html, ...}` |
| `/gen/html/raw` | POST | JSON: `{html, template}` | Plain XML text |
| `/gen/html/multipart` | POST | Multipart: file, template | JSON: `{ok, xml, ...}` |
| `/gen/image` | POST | Multipart: file (image), template, title | Plain XML text |
| `/preview/html` | POST | JSON: `{html, template}` | HTML preview (embedded) |
| `/health` | GET | — | JSON: `{ok, service, version, templates}` |
| `/docs` | GET | — | Swagger API docs (interactive) |

## Examples

### Paste HTML (cURL)

```bash
curl -X POST http://localhost:8000/gen/html \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><head><title>My Blog</title></head><body><h1>Welcome</h1></body></html>",
    "template": "simple"
  }' \
  | jq '.xml' > theme.xml
```

### Upload Image (cURL)

```bash
curl -X POST http://localhost:8000/gen/image \
  -F "file=@design.png" \
  -F "template=from-image" \
  -F "title=My Blog" \
  > theme.xml
```

### Python SDK

```python
from pathlib import Path
from bloggereasy.integrations.sdk import generate_from_html, generate_from_image

# From HTML file
result = generate_from_html(
    html_path=Path("design.html"),
    out_path=Path("theme.xml"),
    template="simple"
)
print(f"Valid: {result['validation']['ok']}")

# From image
result = generate_from_image(
    image_path=Path("mockup.png"),
    out_path=Path("theme.xml"),
    template="from-image"
)
```

## Screenshots

### Homepage (Paste HTML Mode)

![Web UI Homepage](web-homepage.png)

### After Generation

![Web UI with Result](web-result.png)

### API Docs

![Swagger Docs](web-api-docs.png)

## Templates

- **simple** — Clean, minimal blog design
- **magazine** — Multi-column layout for news/magazine sites
- **portfolio** — Gallery + sidebar layout for portfolios
- **dark** — Dark theme variant
- **news** — News site template
- **from-image** — Auto-inferred template from image upload

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "HTML too short" | Ensure your HTML is at least 20 characters |
| "Unknown template" | Use one of: simple, magazine, portfolio, dark, news, from-image |
| XML validation warnings | Usually safe to ignore; XML will still import into Blogger |
| Image upload fails | Try PNG/JPG format; ensure file is a valid image |
| Port 8000 already in use | Use `--port 9000` or kill the existing process |

## Development

The web UI is built with:
- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla HTML/CSS/JavaScript (no build step)
- **Templates:** Jinja2-style generation from HTML/images
- **Architecture:** REST API + static HTML interface

See [API reference](../README.md) for more details on the theme generation engine.

---

**Version:** 0.3.7  
**License:** MIT  
**Repository:** https://github.com/mergeos-bounties/BloggerEasy
