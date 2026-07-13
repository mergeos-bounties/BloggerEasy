"""Theme pack sample: food_recipe (Fixes #27).

Verifies the food_recipe preset generates valid Blogger XML from the
self-contained HTML fixture, containing a b:skin block and a Blog widget.
"""

from __future__ import annotations

from pathlib import Path

from bloggereasy.integrations.sdk import generate_from_html
from bloggereasy.theme.presets import PRESETS
from bloggereasy.theme.validate import validate_theme_file

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples" / "html"


def test_food_recipe_preset_registered() -> None:
    assert "food_recipe" in PRESETS
    assert PRESETS["food_recipe"]["accent"] == "#d97742"


def test_food_recipe_sample_exists() -> None:
    assert (SAMPLES / "food_recipe.html").is_file()


def test_gen_html_food_recipe_produces_skin_and_blog_widget(tmp_path: Path) -> None:
    src = SAMPLES / "food_recipe.html"
    out = tmp_path / "food_recipe.xml"
    result = generate_from_html(src, out, template="food_recipe")

    assert result["validation"]["ok"], result["validation"]
    assert out.exists()

    xml = out.read_text(encoding="utf-8")
    assert "xmlns:b=" in xml
    assert "b:skin" in xml
    assert "type='Blog'" in xml or 'type="Blog"' in xml
    # food_recipe accent should be pushed into the skin
    assert "d97742" in xml
    assert "Template: food_recipe" in xml

    v = validate_theme_file(out)
    assert v["ok"] is True
