import os
from pathlib import Path

from yardang.build import generate_docs_configuration
from yardang.cli import build, debug


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
