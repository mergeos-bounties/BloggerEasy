import os
from bloggereasy.theme.builder import build_blogger_xml
from bloggereasy.theme.presets import PRESETS

def test_new_templates_exist():
    """Test that the new templates are defined in PRESETS."""
    expected_templates = {"home", "about", "contact"}
    for template in expected_templates:
        assert template in PRESETS, f"Template '{template}' not found in PRESETS"

def test_new_templates_generate_valid_xml(tmp_path):
    """Test that each new template generates valid Blogger XML."""
    from bloggereasy.config import SAMPLES_DIR
    from bloggereasy.integrations.sdk import generate_from_html

    # Use the existing home.html sample for all templates (it's a simple page)
    sample_path = SAMPLES_DIR / "html" / "home.html"
    assert sample_path.exists(), f"Sample file not found: {sample_path}"

    for template in ["home", "about", "contact"]:
        out_path = tmp_path / f"test_{template}.xml"
        result = generate_from_html(
            sample_path,
            out_path,
            template=template,
            widgets="default",
            dark=False,
        )
        assert result["validation"]["ok"], f"Validation failed for template {template}: {result['validation']}"
        assert out_path.exists(), f"Output file not created for template {template}"
        # Check that the file contains expected blogger XML structure
        content = out_path.read_text(encoding="utf-8")
        assert "b:skin" in content, f"No b:skin found in output for {template}"
        assert "b:section" in content, f"No b:section found in output for {template}"
        assert "Blog" in content, f"No Blog widget found in output for {template}"