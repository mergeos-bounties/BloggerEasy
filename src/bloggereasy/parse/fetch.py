from __future__ import annotations

import urllib.error
import urllib.request
from pathlib import Path


def fetch_html_url(url: str, *, timeout: float = 15.0, user_agent: str = "BloggerEasy/0.2") -> str:
    """Fetch public HTML. No auth; caller must respect site ToS."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} fetching {url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"network error fetching {url}: {exc.reason}") from exc


def save_html(html: str, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path
