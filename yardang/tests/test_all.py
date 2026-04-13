import os
from pathlib import Path

from yardang.build import generate_docs_configuration
from yardang.cli import build, debug
from yardang.utils import get_config_flex


def test_build():
    with generate_docs_configuration() as _:
        ...


def test_cli():
    build()
    debug()


class TestUseAutoapi:
    """Tests for use_autoapi parameter handling."""

    def test_use_autoapi_false_not_overridden_by_config(self, tmp_path):
        """Test that explicitly passing use_autoapi=False is not overridden by config."""
        # Create a pyproject.toml with use-autoapi = true
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = true
"""
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Test Project\n\nTest content.")

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Explicitly pass use_autoapi=False - this should NOT be overridden by config
            with generate_docs_configuration(use_autoapi=False) as conf_dir:
                conf_path = Path(conf_dir) / "conf.py"
                conf_content = conf_path.read_text()

                # Verify that use_autoapi is False, not True from config
                assert "use_autoapi = False" in conf_content
        finally:
            os.chdir(original_cwd)

    def test_use_autoapi_none_falls_back_to_config(self, tmp_path):
        """Test that use_autoapi=None (default) falls back to config value."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = true
"""
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Test Project\n\nTest content.")

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Don't pass use_autoapi - should fall back to config value (True)
            with generate_docs_configuration() as conf_dir:
                conf_path = Path(conf_dir) / "conf.py"
                conf_content = conf_path.read_text()

                # Verify that use_autoapi is True from config
                assert "use_autoapi = True" in conf_content
        finally:
            os.chdir(original_cwd)


class TestGetConfigFlex:
    """Tests for get_config_flex accepting both hyphens and underscores."""

    def test_hyphen_key_found(self, tmp_path):
        """Test that hyphenated keys are found."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
html-extra-path = ["docs/extra"]
"""
        (tmp_path / "pyproject.toml").write_text(pyproject_content)
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = get_config_flex(section="html-extra-path", base="tool.yardang")
            assert result == ["docs/extra"]
        finally:
            os.chdir(original_cwd)

    def test_underscore_key_found(self, tmp_path):
        """Test that underscored keys are found."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
html_extra_path = ["docs/extra"]
"""
        (tmp_path / "pyproject.toml").write_text(pyproject_content)
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = get_config_flex(section="html_extra_path", base="tool.yardang")
            assert result == ["docs/extra"]
        finally:
            os.chdir(original_cwd)

    def test_hyphen_key_searched_when_underscore_queried(self, tmp_path):
        """Test that querying with underscores finds hyphenated keys."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
html-extra-path = ["docs/extra"]
"""
        (tmp_path / "pyproject.toml").write_text(pyproject_content)
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            # Query with underscores, but TOML uses hyphens
            result = get_config_flex(section="html_extra_path", base="tool.yardang")
            assert result == ["docs/extra"]
        finally:
            os.chdir(original_cwd)

    def test_underscore_key_searched_when_hyphen_queried(self, tmp_path):
        """Test that querying with hyphens finds underscored keys."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
html_extra_path = ["docs/extra"]
"""
        (tmp_path / "pyproject.toml").write_text(pyproject_content)
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            # Query with hyphens, but TOML uses underscores
            result = get_config_flex(section="html-extra-path", base="tool.yardang")
            assert result == ["docs/extra"]
        finally:
            os.chdir(original_cwd)

    def test_hyphen_takes_precedence(self, tmp_path):
        """Test that hyphenated key takes precedence when both exist."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
html-extra-path = ["from-hyphens"]
html_extra_path = ["from-underscores"]
"""
        (tmp_path / "pyproject.toml").write_text(pyproject_content)
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = get_config_flex(section="html_extra_path", base="tool.yardang")
            assert result == ["from-hyphens"]
        finally:
            os.chdir(original_cwd)

    def test_missing_key_returns_none(self, tmp_path):
        """Test that missing keys return None."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test"
"""
        (tmp_path / "pyproject.toml").write_text(pyproject_content)
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = get_config_flex(section="html_extra_path", base="tool.yardang")
            assert result is None
        finally:
            os.chdir(original_cwd)


class TestHtmlExtraPath:
    """Tests for html_extra_path in generated conf.py."""

    def test_html_extra_path_with_hyphens(self, tmp_path):
        """Test that html-extra-path (hyphens) is picked up in generated conf.py."""
        extra_dir = tmp_path / "docs" / "extra"
        extra_dir.mkdir(parents=True)
        (extra_dir / "page.html").write_text("<html><body>test</body></html>")

        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false
html-extra-path = ["docs/extra"]
"""
        (tmp_path / "pyproject.toml").write_text(pyproject_content)
        (tmp_path / "README.md").write_text("# Test\n\nContent.")

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with generate_docs_configuration() as conf_dir:
                conf_content = (Path(conf_dir) / "conf.py").read_text()
                assert "html_extra_path" in conf_content
                assert "docs/extra" in conf_content or "docs\\\\extra" in conf_content or str(extra_dir) in conf_content
        finally:
            os.chdir(original_cwd)

    def test_html_extra_path_with_underscores(self, tmp_path):
        """Test that html_extra_path (underscores) is also accepted."""
        extra_dir = tmp_path / "docs" / "extra"
        extra_dir.mkdir(parents=True)
        (extra_dir / "page.html").write_text("<html><body>test</body></html>")

        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false
html_extra_path = ["docs/extra"]
"""
        (tmp_path / "pyproject.toml").write_text(pyproject_content)
        (tmp_path / "README.md").write_text("# Test\n\nContent.")

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with generate_docs_configuration() as conf_dir:
                conf_content = (Path(conf_dir) / "conf.py").read_text()
                assert "html_extra_path" in conf_content
                assert "docs/extra" in conf_content or "docs\\\\extra" in conf_content or str(extra_dir) in conf_content
        finally:
            os.chdir(original_cwd)
