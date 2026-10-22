import ast
import os
from pathlib import Path
from unittest.mock import patch

import pytest
import toml
from sphinx.cmd.build import build_main

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


def _bundled(*names: str) -> str:
    """Expected content for a layered resolution over the named bundled assets."""
    return "\n".join((ASSETS_DIR / name).read_text().rstrip("\n") for name in names) + "\n"


class TestThemeModule:
    """Theme names map to the package that provides them."""

    def test_bundled_theme_maps_to_its_distribution(self):
        assert build_module.theme_module("fuma") == "sphinx_fuma"

    def test_other_themes_are_unchanged(self):
        assert build_module.theme_module("furo") == "furo"


class TestDocumentedThemes:
    """The theme lists in the docs are maintained by hand, so they drift."""

    @pytest.mark.parametrize("theme", BUNDLED_THEMES)
    def test_theme_has_a_preview_link(self, theme):
        docs = Path(__file__).parents[2] / "docs" / "src" / "configuration.md"
        assert f"/_previews/{theme}/" in docs.read_text()


class TestSearchIntegration:
    """Search is theme-independent, so it is wired for every first-class theme."""

    def _conf(self, tmp_path, **kwargs):
        (tmp_path / "pyproject.toml").write_text(MINIMAL_PYPROJECT)
        (tmp_path / "README.md").write_text("# Test Project\n")
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with generate_docs_configuration(html_output_dir=str(tmp_path / "site"), **kwargs) as config_dir:
                return Path(config_dir, "conf.py").read_text()
        finally:
            os.chdir(original_cwd)

    @pytest.mark.parametrize("theme", BUNDLED_THEMES)
    def test_searchlite_is_enabled_for_first_class_themes(self, tmp_path, theme):
        assert "sphinx_searchlite" in self._conf(tmp_path, theme=theme)

    def test_fuma_is_registered_as_an_extension(self, tmp_path):
        assert "sphinx_fuma" in self._conf(tmp_path, theme="fuma")


class TestDefaultTheme:
    """An unconfigured build uses the bundled default theme."""

    def test_unconfigured_theme_is_fuma(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(MINIMAL_PYPROJECT)
        (tmp_path / "README.md").write_text("# Test Project\n")
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with generate_docs_configuration(html_output_dir=str(tmp_path / "site")) as config_dir:
                conf = Path(config_dir, "conf.py").read_text()
        finally:
            os.chdir(original_cwd)
        assert 'html_theme = "fuma"' in conf
        assert "sphinx_fuma" in conf


class TestProjectLinks:
    @pytest.fixture
    def project(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "README.md").write_text("# Test Project\n")
        return toml.loads(MINIMAL_PYPROJECT)

    def _options(self, project, **kwargs):
        Path("pyproject.toml").write_text(toml.dumps(project))
        with generate_docs_configuration(**kwargs) as config_dir:
            conf = Path(config_dir, "conf.py").read_text()
        line = next(line for line in conf.splitlines() if line.startswith("html_theme_options = "))
        return ast.literal_eval(line.split(" = ", 1)[1])

    @pytest.mark.parametrize(
        ("urls", "expected"),
        [
            ({}, {}),
            ({"Homepage": "https://example.com"}, {}),
            ({"Repository": "https://gitlab.com/owner/repo"}, {}),
            ({"Homepage": "https://owner.github.io/repo"}, {}),
            ({"Repository": "https://github.com.evil.test/owner/repo"}, {}),
            ({"Repository": "https://github.com/owner"}, {}),
            ({"Repository": "ftp://github.com/owner/repo"}, {}),
            ({"Repository": "https://github.com/owner/repo"}, {"github_url": "https://github.com/owner/repo"}),
            ({"Homepage": "https://github.com/owner/repo/"}, {"github_url": "https://github.com/owner/repo"}),
            ({"Source Code": "https://github.com/owner/repo.git"}, {"github_url": "https://github.com/owner/repo"}),
            ({"Bug Tracker": "https://github.com/owner/repo/issues?q=open#top"}, {"github_url": "https://github.com/owner/repo"}),
            (
                {"Homepage": "https://github.com/owner/home", "rEpOsItOrY": "https://github.com/owner/repo"},
                {"github_url": "https://github.com/owner/repo"},
            ),
            (
                {"Homepage": "https://github.com/owner/home", "Source": "https://github.com/owner/repo"},
                {"github_url": "https://github.com/owner/repo"},
            ),
            (
                {"Repository": "https://example.com/repo", "Homepage": "https://github.com/owner/repo"},
                {"github_url": "https://github.com/owner/repo"},
            ),
        ],
    )
    def test_infers_github_repository(self, project, urls, expected):
        project["project"]["urls"] = urls
        assert self._options(project).get("github_url") == expected.get("github_url")

    @pytest.mark.parametrize(
        ("urls", "expected"),
        [
            ({}, []),
            ({"Homepage": "https://example.com"}, [{"title": "Home", "url": "https://example.com"}]),
            ({"Documentation": "https://docs.example.com"}, [{"title": "Docs", "url": "https://docs.example.com"}]),
            ({"Docs": "https://docs.example.com"}, [{"title": "Docs", "url": "https://docs.example.com"}]),
            (
                {"hOmEpAgE": "https://example.com", "dOcUmEnTaTiOn": "https://docs.example.com/guide"},
                [{"title": "Home", "url": "https://example.com"}, {"title": "Docs", "url": "https://docs.example.com/guide"}],
            ),
            (
                {"Docs": "https://old.example.com", "Documentation": "https://docs.example.com"},
                [{"title": "Docs", "url": "https://docs.example.com"}],
            ),
            (
                {"Homepage": "https://example.com/", "Documentation": "https://example.com"},
                [{"title": "Home", "url": "https://example.com/"}],
            ),
            ({"Homepage": "https://github.com/owner/repo/"}, []),
        ],
    )
    def test_infers_home_and_docs_links(self, project, urls, expected):
        project["project"]["urls"] = urls
        assert self._options(project).get("nav_links", []) == expected

    @pytest.mark.parametrize("nav_links", [[], [{"title": "Blog", "url": "https://example.com/blog"}], "Blog|https://example.com/blog"])
    @pytest.mark.parametrize("option_key", ["html_theme_options", "html-theme-options"])
    def test_explicit_navigation_takes_precedence(self, project, nav_links, option_key):
        project["project"]["urls"] = {
            "Repository": "https://github.com/owner/repo",
            "Homepage": "https://example.com",
            "Documentation": "https://docs.example.com",
        }
        project["tool"]["yardang"][option_key] = {"nav_links": nav_links}
        assert self._options(project) == {"nav_links": nav_links, "github_url": "https://github.com/owner/repo"}

    @pytest.mark.parametrize("github_url", ["https://github.com/other/repo", ""])
    @pytest.mark.parametrize("option_key", ["html_theme_options", "html-theme-options"])
    def test_explicit_options_take_precedence(self, project, github_url, option_key):
        project["project"]["urls"] = {"Repository": "https://github.com/owner/repo", "Homepage": "https://example.com"}
        options = {"github_url": github_url, "toc_style": "clerk"}
        project["tool"]["yardang"][option_key] = options
        assert self._options(project) == {**options, "nav_links": [{"title": "Home", "url": "https://example.com"}]}

    @pytest.mark.parametrize("theme", [theme for theme in BUNDLED_THEMES if theme != "fuma"])
    def test_other_themes_do_not_receive_project_links(self, project, theme):
        project["project"]["urls"] = {
            "Repository": "https://github.com/owner/repo",
            "Homepage": "https://example.com",
            "Documentation": "https://docs.example.com",
        }
        assert self._options(project, theme=theme) == {}

    def test_custom_config_base_and_existing_options(self, project):
        project["project"]["urls"] = {"Repository": "https://github.com/owner/repo", "Documentation": "https://docs.example.com"}
        project["tool"]["custom"] = project["tool"].pop("yardang")
        project["tool"]["custom"]["html-theme-options"] = {"toc_style": "clerk"}
        assert self._options(project, config_base="tool.custom") == {
            "toc_style": "clerk",
            "github_url": "https://github.com/owner/repo",
            "nav_links": [{"title": "Docs", "url": "https://docs.example.com"}],
        }

    def test_inferred_urls_render_project_links(self, project, tmp_path):
        project["project"]["urls"] = {
            "Repository": "https://github.com/owner/repo",
            "Homepage": "https://example.com",
            "Documentation": "https://docs.example.com",
        }
        self._options(project)
        output = tmp_path / "html"
        with generate_docs_configuration(html_output_dir=str(output)) as config_dir:
            result = build_main(["-q", "-b", "html", "-c", str(config_dir), ".", str(output)])
        assert result == 0
        html = (output / "index.html").read_text()
        assert "<title>Test Project" in html
        assert 'href="https://github.com/owner/repo"' in html
        assert 'href="https://github.com/owner/repo/edit/HEAD/index.md"' in html
        assert html.count('href="https://example.com" target="_blank" rel="noopener">Home</a>') == 2
        assert html.count('href="https://docs.example.com" target="_blank" rel="noopener">Docs</a>') == 2


class TestResolveCustomAsset:
    """Layered resolution of bundled and user-supplied CSS/JS."""

    def test_generic_defaults_apply_to_every_theme(self):
        assert _resolve_custom_asset(None, "klink", "css", assets_dir=ASSETS_DIR) == _bundled("custom.css")

    def test_theme_rules_are_appended_after_generic_defaults(self):
        resolved = _resolve_custom_asset(None, "shibuya", "css", assets_dir=ASSETS_DIR)
        assert resolved == _bundled("custom.css", "shibuya.css")
        assert resolved.index("prefers-color-scheme") < resolved.index("button.copybtn")

    def test_furo_rules_are_appended_after_generic_defaults(self):
        assert _resolve_custom_asset(None, "furo", "css", assets_dir=ASSETS_DIR) == _bundled("custom.css", "furo.css")

    def test_generic_js_is_used_when_theme_ships_no_js(self):
        assert _resolve_custom_asset(None, "furo", "js", assets_dir=ASSETS_DIR) == _bundled("custom.js")

    def test_user_content_takes_precedence(self):
        content = "body { color: red; }"
        assert _resolve_custom_asset(content, "shibuya", "css", assets_dir=ASSETS_DIR) == content

    def test_reads_existing_file(self, tmp_path):
        asset = tmp_path / "mine.css"
        asset.write_text("h1 { color: blue; }")
        assert _resolve_custom_asset(asset, "furo", "css", assets_dir=ASSETS_DIR) == "h1 { color: blue; }"

    def test_ignores_missing_path(self):
        expected = _bundled("custom.css", "shibuya.css")
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
        assert written == _bundled("custom.css", "shibuya.css")

    def test_default_theme_keeps_generic_defaults(self, tmp_path):
        self._setup_project(tmp_path)
        out = tmp_path / "site"
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with generate_docs_configuration(html_output_dir=str(out)):
                pass
        finally:
            os.chdir(original_cwd)
        written = (out / "_static" / "styles" / "custom.css").read_text()
        assert written == _bundled("custom.css", "fuma.css")
        assert "mermaid" in written


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
