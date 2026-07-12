from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.batch import validate_theme_dir


def test_batch_validate_demo_dir(tmp_path: Path) -> None:
    src = Path("data/samples/html/portfolio.html")
    generate_from_html(src, tmp_path / "a.xml", template="portfolio")
    generate_from_html(src, tmp_path / "b.xml", template="simple")
    report = validate_theme_dir(tmp_path)
    assert report["n"] == 2
    assert report["ok"] == 2
    assert report["fail"] == 0
