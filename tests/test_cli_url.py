from __future__ import annotations

from typer.testing import CliRunner

from bloggereasy import cli
from bloggereasy.cli import app


runner = CliRunner()


def test_gen_html_url_fetches_public_page(monkeypatch, tmp_path) -> None:
    seen = {}

    def fake_fetch(url: str, *, timeout: float = 15.0, user_agent: str = "BloggerEasy/0.2") -> str:
        seen["url"] = url
        seen["timeout"] = timeout
        seen["user_agent"] = user_agent
        return """
        <html>
          <head><title>Fetched Blog</title></head>
          <body>
            <header><h1>Fetched Blog</h1><nav><a href="/">Home</a></nav></header>
            <p>Fetched through a mocked HTTP call.</p>
          </body>
        </html>
        """

    monkeypatch.setattr(cli, "fetch_html_url", fake_fetch)
    out = tmp_path / "fetched.xml"

    result = runner.invoke(
        app,
        [
            "gen",
            "html",
            "--url",
            "https://example.com/blog",
            "--timeout",
            "7",
            "--out",
            str(out),
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert seen == {
        "url": "https://example.com/blog",
        "timeout": 7.0,
        "user_agent": "BloggerEasy/0.2",
    }
    assert out.exists()
    assert "Fetched Blog" in out.read_text(encoding="utf-8")


def test_gen_html_requires_exactly_one_input() -> None:
    result = runner.invoke(app, ["gen", "html"])

    assert result.exit_code == 1
    assert "Provide exactly one of --input or --url" in result.stdout
