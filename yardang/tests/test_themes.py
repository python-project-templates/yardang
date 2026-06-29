import os
from pathlib import Path
from unittest.mock import patch

import yardang.build as build_module
from yardang.build import BUNDLED_THEMES, _resolve_custom_asset, generate_docs_configuration
from yardang.cli import preview

ASSETS_DIR = Path(build_module.__file__).parent

MINIMAL_PYPROJECT = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false
"""


class TestResolveCustomAsset:
    """Theme-aware resolution of bundled and user-supplied CSS/JS."""

    def test_prefers_theme_specific_file(self):
        expected = (ASSETS_DIR / "sphinxawesome_theme.css").read_text()
        assert _resolve_custom_asset(None, "sphinxawesome_theme", "css", assets_dir=ASSETS_DIR) == expected

    def test_shibuya_theme_specific_file(self):
        expected = (ASSETS_DIR / "shibuya.css").read_text()
        assert _resolve_custom_asset(None, "shibuya", "css", assets_dir=ASSETS_DIR) == expected

    def test_falls_back_to_custom_css(self):
        expected = (ASSETS_DIR / "custom.css").read_text()
        assert _resolve_custom_asset(None, "furo", "css", assets_dir=ASSETS_DIR) == expected

    def test_falls_back_to_custom_js(self):
        expected = (ASSETS_DIR / "custom.js").read_text()
        assert _resolve_custom_asset(None, "furo", "js", assets_dir=ASSETS_DIR) == expected

    def test_user_content_takes_precedence(self):
        content = "body { color: red; }"
        assert _resolve_custom_asset(content, "shibuya", "css", assets_dir=ASSETS_DIR) == content

    def test_reads_existing_file(self, tmp_path):
        asset = tmp_path / "mine.css"
        asset.write_text("h1 { color: blue; }")
        assert _resolve_custom_asset(asset, "furo", "css", assets_dir=ASSETS_DIR) == "h1 { color: blue; }"

    def test_ignores_missing_path(self):
        expected = (ASSETS_DIR / "shibuya.css").read_text()
        assert _resolve_custom_asset("does/not/exist/custom.css", "shibuya", "css", assets_dir=ASSETS_DIR) == expected

    def test_returns_none_when_nothing_matches(self, tmp_path):
        assert _resolve_custom_asset(None, "furo", "css", assets_dir=tmp_path) is None


class TestGenerateDocsThemeAssets:
    """Theme assets flow through ``generate_docs_configuration`` into the output."""

    def _setup_project(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(MINIMAL_PYPROJECT)
        (tmp_path / "README.md").write_text("# Test Project\n")

    def test_html_output_dir_places_custom_assets(self, tmp_path):
        self._setup_project(tmp_path)
        out = tmp_path / "site"
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with generate_docs_configuration(theme="furo", html_output_dir=str(out)):
                pass
        finally:
            os.chdir(original_cwd)
        assert (out / "_static" / "styles" / "custom.css").is_file()
        assert (out / "_static" / "js" / "custom.js").is_file()

    def test_theme_specific_css_is_written(self, tmp_path):
        self._setup_project(tmp_path)
        out = tmp_path / "site"
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with generate_docs_configuration(theme="shibuya", html_output_dir=str(out)):
                pass
        finally:
            os.chdir(original_cwd)
        written = (out / "_static" / "styles" / "custom.css").read_text()
        assert written == (ASSETS_DIR / "shibuya.css").read_text()


class TestPreview:
    """The ``yardang preview`` command builds the docs once per theme."""

    def test_builds_each_installed_theme(self):
        with patch("yardang.cli.build") as mock_build, patch("yardang.cli.find_spec", return_value=object()):
            preview(themes=["furo", "shibuya"], output="out", quiet=True)
        calls = mock_build.call_args_list
        assert [call.kwargs["theme"] for call in calls] == ["furo", "shibuya"]
        assert [call.kwargs["output"] for call in calls] == [str(Path("out") / "furo"), str(Path("out") / "shibuya")]

    def test_uses_bundled_themes_by_default(self):
        with patch("yardang.cli.build") as mock_build, patch("yardang.cli.find_spec", return_value=object()):
            preview(quiet=True)
        assert [call.kwargs["theme"] for call in mock_build.call_args_list] == list(BUNDLED_THEMES)

    def test_skips_uninstalled_theme(self):
        def fake_find_spec(name):
            return object() if name == "furo" else None

        with patch("yardang.cli.build") as mock_build, patch("yardang.cli.find_spec", side_effect=fake_find_spec):
            preview(themes=["furo", "shibuya"], quiet=True)
        assert [call.kwargs["theme"] for call in mock_build.call_args_list] == ["furo"]
