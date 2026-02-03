"""Tests for GitHub Wiki generation in yardang."""

import os
from pathlib import Path


class TestWikiConfiguration:
    """Tests for wiki configuration loading and generation."""

    def test_wiki_config_loading_from_pyproject(self, tmp_path):
        """Test that wiki configuration is loaded from pyproject.toml."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false

[tool.yardang.wiki]
enabled = true
output-dir = "docs/wiki"
generate-sidebar = true
generate-footer = true
fix-links = true
footer-docs-url = "https://example.com/docs"
footer-repo-url = "https://github.com/example/repo"
markdown-flavor = "github"
"""
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Test Project\n\nTest content.")

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            from yardang.utils import get_config

            # Test that wiki config is loaded correctly
            wiki_enabled = get_config(section="enabled", base="tool.yardang.wiki")
            assert wiki_enabled is True

            wiki_output_dir = get_config(section="output-dir", base="tool.yardang.wiki")
            assert wiki_output_dir == "docs/wiki"

            generate_sidebar = get_config(section="generate-sidebar", base="tool.yardang.wiki")
            assert generate_sidebar is True

            markdown_flavor = get_config(section="markdown-flavor", base="tool.yardang.wiki")
            assert markdown_flavor == "github"

            footer_docs_url = get_config(section="footer-docs-url", base="tool.yardang.wiki")
            assert footer_docs_url == "https://example.com/docs"
        finally:
            os.chdir(original_cwd)

    def test_wiki_config_defaults(self, tmp_path):
        """Test that wiki configuration has sensible defaults when not specified."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
"""
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Test Project\n\nTest content.")

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            from yardang.utils import get_config

            # Test that missing wiki config returns None
            wiki_enabled = get_config(section="enabled", base="tool.yardang.wiki")
            assert wiki_enabled is None

            wiki_output_dir = get_config(section="output-dir", base="tool.yardang.wiki")
            assert wiki_output_dir is None
        finally:
            os.chdir(original_cwd)

    def test_generate_docs_with_wiki_enabled(self, tmp_path):
        """Test that generate_docs_configuration includes wiki/markdown builder settings."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false

[tool.yardang.wiki]
enabled = true
markdown-flavor = "github"
markdown-anchor-sections = true
"""
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Test Project\n\nTest content.")

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            from yardang.build import generate_docs_configuration

            with generate_docs_configuration() as conf_dir:
                conf_path = Path(conf_dir) / "conf.py"
                conf_content = conf_path.read_text()

                # Check that use_wiki is set
                assert "use_wiki = True" in conf_content

                # Check that markdown builder config is present when wiki is enabled
                assert "markdown_flavor" in conf_content
                assert "github" in conf_content
        finally:
            os.chdir(original_cwd)


class TestWikiPostProcessor:
    """Tests for wiki post-processing functions."""

    def test_get_page_title_from_h1(self, tmp_path):
        """Test extracting title from H1 heading."""
        from yardang.wiki import get_page_title

        md_file = tmp_path / "test.md"
        md_file.write_text("# My Page Title\n\nSome content here.")

        title = get_page_title(md_file)
        assert title == "My Page Title"

    def test_get_page_title_fallback_to_filename(self, tmp_path):
        """Test fallback to filename when no H1 heading exists."""
        from yardang.wiki import get_page_title

        md_file = tmp_path / "my-page-name.md"
        md_file.write_text("Some content without heading.")

        title = get_page_title(md_file)
        assert title == "My Page Name"

    def test_get_page_title_index_becomes_home(self, tmp_path):
        """Test that index.md gets 'Home' as title."""
        from yardang.wiki import get_page_title

        md_file = tmp_path / "index.md"
        md_file.write_text("Some content without heading.")

        title = get_page_title(md_file)
        assert title == "Home"

    def test_convert_filename_to_wiki_format(self):
        """Test filename conversion for wiki format."""
        from yardang.wiki import convert_filename_to_wiki_format

        assert convert_filename_to_wiki_format("overview.md") == "overview"
        assert convert_filename_to_wiki_format("index.md") == "Home"
        assert convert_filename_to_wiki_format("readme.md") == "Home"
        assert convert_filename_to_wiki_format("docs/src/api.md") == "api"

    def test_fix_wiki_links_basic(self):
        """Test fixing internal markdown links."""
        from yardang.wiki import fix_wiki_links

        content = "Check [the overview](overview.md) for more info."
        page_map = {"overview.md": "overview"}

        fixed = fix_wiki_links(content, page_map)
        assert "[the overview](overview)" in fixed

    def test_fix_wiki_links_with_anchors(self):
        """Test fixing links with anchors."""
        from yardang.wiki import fix_wiki_links

        content = "See [installation](installation.md#quick-start) guide."
        page_map = {"installation.md": "installation"}

        fixed = fix_wiki_links(content, page_map)
        assert "[installation](installation#quick-start)" in fixed

    def test_fix_wiki_links_preserves_external_links(self):
        """Test that external links are preserved."""
        from yardang.wiki import fix_wiki_links

        content = "Visit [GitHub](https://github.com) for more info."
        page_map = {}

        fixed = fix_wiki_links(content, page_map)
        assert "[GitHub](https://github.com)" in fixed

    def test_generate_sidebar(self, tmp_path):
        """Test sidebar generation."""
        from yardang.wiki import generate_sidebar

        # Create some test files
        (tmp_path / "Home.md").write_text("# Welcome\n\nHome page content.")
        (tmp_path / "overview.md").write_text("# Overview\n\nOverview content.")
        (tmp_path / "installation.md").write_text("# Installation\n\nInstall steps.")

        pages = ["docs/src/overview.md", "docs/src/installation.md"]
        sidebar = generate_sidebar(tmp_path, pages, project_name="My Project")

        assert "### My Project" in sidebar
        assert "[Home](Home)" in sidebar
        assert "[Overview](overview)" in sidebar
        assert "[Installation](installation)" in sidebar

        # Check file was created
        sidebar_file = tmp_path / "_Sidebar.md"
        assert sidebar_file.exists()

    def test_generate_footer(self, tmp_path):
        """Test footer generation."""
        from yardang.wiki import generate_footer

        footer = generate_footer(
            tmp_path,
            project_name="My Project",
            docs_url="https://myproject.dev",
            repo_url="https://github.com/myorg/myproject",
        )

        assert "[📚 Full Documentation](https://myproject.dev)" in footer
        assert "[💻 Repository](https://github.com/myorg/myproject)" in footer

        # Check file was created
        footer_file = tmp_path / "_Footer.md"
        assert footer_file.exists()

    def test_rename_index_to_home(self, tmp_path):
        """Test renaming index.md to Home.md."""
        from yardang.wiki import rename_index_to_home

        # Create index.md
        index_file = tmp_path / "index.md"
        index_file.write_text("# Welcome\n\nMain page content.")

        rename_index_to_home(tmp_path)

        # Check Home.md exists and index.md doesn't
        assert not index_file.exists()
        assert (tmp_path / "Home.md").exists()

    def test_flatten_directory_structure(self, tmp_path):
        """Test flattening nested directories."""
        from yardang.wiki import flatten_directory_structure

        # Create nested structure
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "page.md").write_text("# Page\n\nContent.")

        nested = tmp_path / "docs" / "api"
        nested.mkdir(parents=True)
        (nested / "reference.md").write_text("# API Reference\n\nAPI content.")

        flatten_directory_structure(tmp_path)

        # Check files are flattened
        assert (tmp_path / "subdir-page.md").exists()
        assert (tmp_path / "docs-api-reference.md").exists()

        # Check nested dirs are removed
        assert not (tmp_path / "subdir" / "page.md").exists()

    def test_process_wiki_output_full(self, tmp_path):
        """Test full wiki output processing."""
        from yardang.wiki import process_wiki_output

        # Create test markdown output structure
        (tmp_path / "index.md").write_text("# Welcome\n\nSee [overview](overview.md).")
        (tmp_path / "overview.md").write_text("# Overview\n\nOverview content.")
        (tmp_path / "api.md").write_text("# API\n\nAPI docs.")

        process_wiki_output(
            output_dir=tmp_path,
            pages=["overview.md", "api.md"],
            project_name="Test Project",
            docs_url="https://test.dev",
            repo_url="https://github.com/test/project",
        )

        # Check Home.md exists (renamed from index.md)
        assert (tmp_path / "Home.md").exists()
        assert not (tmp_path / "index.md").exists()

        # Check sidebar was generated
        assert (tmp_path / "_Sidebar.md").exists()
        sidebar = (tmp_path / "_Sidebar.md").read_text()
        assert "Test Project" in sidebar

        # Check footer was generated
        assert (tmp_path / "_Footer.md").exists()
        footer = (tmp_path / "_Footer.md").read_text()
        assert "test.dev" in footer

        # Check links were fixed in Home.md
        home_content = (tmp_path / "Home.md").read_text()
        assert "(overview)" in home_content
