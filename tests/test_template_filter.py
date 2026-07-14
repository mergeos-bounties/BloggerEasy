"""Tests for template filter."""

import json
from click.testing import CliRunner
from bloggereasy.cli import cli

def test_list_tags(tmp_path):
    templates_dir = tmp_path / "data" / "templates"
    templates_dir.mkdir(parents=True)
    (templates_dir / "minimal.json").write_text(json.dumps({"name": "Minimal", "tags": ["clean", "simple"]}))
    
    runner = CliRunner()
    result = runner.invoke(cli, ["templates", "--list-tags"], catch_exceptions=False)
    assert "clean" in result.output
    assert "simple" in result.output
