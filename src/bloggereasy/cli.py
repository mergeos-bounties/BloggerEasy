from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from bloggereasy import __version__
from bloggereasy.config import OUT_DIR, SAMPLES_DIR, TEMPLATES_DIR
from bloggereasy.integrations.sdk import (
    generate_from_html,
    generate_from_image,
    generate_from_url,
)
from bloggereasy.parse.html_page import parse_html_file
from bloggereasy.theme.builder import build_blogger_xml, sanitize_filename
from bloggereasy.theme.presets import PRESETS
from bloggereasy.theme.validate import validate_theme_file

app = typer.Typer(
    help="BloggerEasy — generate usable Blogger XML themes from HTML, URL, or images.",
    no_args_is_help=True,
)
gen_app = typer.Typer(help="Generate themes")
parse_app = typer.Typer(help="Parse inputs")
templates_app = typer.Typer(help="Built-in templates")
app.add_typer(gen_app, name="gen")
app.add_typer(parse_app, name="parse")
app.add_typer(templates_app, name="templates")
console = Console()


@app.command("version")
def version_cmd() -> None:
    console.print(f"BloggerEasy {__version__}")
    console.print(f"Templates: {', '.join(PRESETS)}")


@app.command("demo")
def demo_cmd(
    out_dir: Path = typer.Option(None, "--out-dir", "-o"),
) -> None:
    """Generate themes for all bundled HTML samples (runnable smoke demo)."""
    root = out_dir or (OUT_DIR / "demo")
    root.mkdir(parents=True, exist_ok=True)
    samples = sorted((SAMPLES_DIR / "html").glob("*.html")) if (SAMPLES_DIR / "html").exists() else []
    if not samples:
        console.print("[red]No samples under data/samples/html[/red]")
        raise typer.Exit(1)
    table = Table(title="Demo generations")
    table.add_column("Sample")
    table.add_column("Output")
    table.add_column("OK")
    for path in samples:
        out = root / f"{path.stem}.xml"
        result = generate_from_html(path, out, template="simple")
        ok = "yes" if result["validation"]["ok"] else "no"
        table.add_row(path.name, str(out), ok)
    console.print(table)
    console.print(f"[green]Demo complete[/green] → {root}")
    console.print("Import any XML: Blogger → Theme → Backup/Restore → Upload")


@templates_app.command("list")
def templates_list() -> None:
    table = Table(title="Templates")
    table.add_column("Name")
    table.add_column("Notes")
    for name, meta in PRESETS.items():
        table.add_row(name, str(meta))
    if TEMPLATES_DIR.exists():
        for path in sorted(TEMPLATES_DIR.glob("*.xml")):
            table.add_row(path.stem, f"file:{path.name}")
    console.print(table)


@parse_app.command("html")
def parse_html(input: Path = typer.Option(..., "--input", "-i", exists=True, dir_okay=False)) -> None:
    console.print_json(data=parse_html_file(input))


@gen_app.command("html")
def gen_html(
    input: Path = typer.Option(..., "--input", "-i", exists=True, dir_okay=False),
    out: Path | None = typer.Option(None, "--out", "-o"),
    template: str = typer.Option("simple", "--template", "-t"),
) -> None:
    out_path = out or (OUT_DIR / f"{sanitize_filename(input.stem)}.xml")
    result = generate_from_html(input, out_path, template=template)
    console.print(f"[green]Wrote[/green] {result['output']} ({result['bytes']} bytes)")
    console.print_json(
        data={
            "title": result["structure"]["title"],
            "layout": result["structure"]["layout"],
            "validation": result["validation"],
            "import_hint": result["import_hint"],
        }
    )


@gen_app.command("url")
def gen_url(
    url: str = typer.Option(..., "--url", "-u"),
    out: Path | None = typer.Option(None, "--out", "-o"),
    template: str = typer.Option("simple", "--template", "-t"),
) -> None:
    out_path = out or (OUT_DIR / "from_url.xml")
    try:
        result = generate_from_url(url, out_path, template=template, cache_dir=OUT_DIR)
    except RuntimeError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    console.print(f"[green]Wrote[/green] {result['output']}")
    console.print_json(data={"title": result["structure"]["title"], "validation": result["validation"]})


@gen_app.command("image")
def gen_image(
    input: Path = typer.Option(..., "--input", "-i", exists=True, dir_okay=False),
    out: Path | None = typer.Option(None, "--out", "-o"),
    title: str = typer.Option("My Blog", "--title"),
    template: str = typer.Option("from-image", "--template", "-t"),
) -> None:
    out_path = out or (OUT_DIR / f"{sanitize_filename(input.stem)}-image.xml")
    result = generate_from_image(input, out_path, title=title, template=template)
    console.print(f"[green]Wrote[/green] {result['output']} ({result['bytes']} bytes)")
    console.print_json(
        data={
            "title": result["structure"]["title"],
            "colors": result["structure"]["colors"],
            "validation": result["validation"],
        }
    )


@gen_app.command("preview-css")
def preview_css(input: Path = typer.Option(..., "--input", "-i", exists=True, dir_okay=False)) -> None:
    xml = build_blogger_xml(parse_html_file(input))
    start = xml.find("<![CDATA[")
    end = xml.find("]]>", start)
    if start >= 0 and end > start:
        console.print(xml[start + 9 : end].strip())
    else:
        console.print("[yellow]No skin CDATA found[/yellow]")


@app.command("validate")
def validate_cmd(file: Path = typer.Option(..., "--file", "-f", exists=True, dir_okay=False)) -> None:
    result = validate_theme_file(file)
    console.print_json(data=result)
    if not result["ok"]:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
