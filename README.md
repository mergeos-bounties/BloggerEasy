# BloggerEasy

**BloggerEasy** generates **usable Blogger XML themes** from:

| Input | Output |
| --- | --- |
| **Web HTML** | Layout + CSS + Blogger sections/widgets XML |
| **Design image** | Palette + layout hints → theme scaffold (vision extra) |

Import the exported XML in Blogger → **Theme → Backup/Restore → Upload**.

Built under [mergeos-bounties](https://github.com/mergeos-bounties) for MergeOS MRG bounties.

## Stack

- Python 3.11+
- CLI: `typer` + `rich`
- HTML parse: BeautifulSoup
- Blogger XML builder (sections, gadgets, skin CSS)
- Optional Pillow vision for image → palette

## Quick start

```bash
cd BloggerEasy
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
bloggereasy --help
```

## Commands (runnable)

```bash
bloggereasy version

# One-shot demo: generate XML for all bundled HTML samples
bloggereasy demo

# HTML page → Blogger theme XML (importable)
bloggereasy gen html --input data/samples/html/minimal_blog.html --out data/out/theme.xml
bloggereasy validate --file data/out/theme.xml

# Public URL → theme (stdlib urllib; respect site ToS)
bloggereasy gen url --url "https://example.com" --out data/out/from_url.xml

# Image design → palette + theme (Pillow optional)
bloggereasy gen image --input path/to/mockup.png --out data/out/from_image.xml --title "My Blog"

# Templates: simple | magazine | dark | from-image
bloggereasy gen html -i data/samples/html/dark_dev.html -t dark -o data/out/dark.xml
bloggereasy templates list
```

Import XML in Blogger: **Theme → Backup / Restore → Upload**.

## Layout

```
src/bloggereasy/
  cli.py
  parse/html_page.py     # HTML → structure model
  theme/builder.py       # structure → Blogger XML
  vision/palette.py      # image palette stub
  export/writer.py
  integrations/sdk.py
data/samples/html/
data/templates/
docs/BOUNTY.md
```

## MergeOS bounties

1. Star this repo + [mergeos](https://github.com/mergeos-bounties/mergeos)
2. Claim a `bounty` issue
3. Claim on MergeOS [issue #1](https://github.com/mergeos-bounties/mergeos/issues/1)
4. PR to **BloggerEasy** with tests/evidence
5. Credit MRG 25/50/100/200

See [docs/BOUNTY.md](docs/BOUNTY.md).

## License

MIT
