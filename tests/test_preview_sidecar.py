from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html


def test_generate_from_html_writes_preview_sidecar(tmp_path: Path) -> None:
    out = tmp_path / "portfolio.xml"
    result = generate_from_html(Path("data/samples/html/portfolio.html"), out, template="portfolio")

    preview = Path(result["preview_output"])
    assert out.exists()
    assert preview == tmp_path / "portfolio.preview.html"
    assert preview.exists()
    assert "<!DOCTYPE html>" in preview.read_text(encoding="utf-8")
    assert result["preview_bytes"] == preview.stat().st_size
