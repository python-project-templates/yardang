"""Tests for llms.txt generation (sphinx-llm) in yardang."""

import os
from pathlib import Path


class TestLlmsConfiguration:
    """Tests for llms.txt configuration loading and generation."""

    def test_llms_config_loading_from_pyproject(self, tmp_path):
        """Test that llms configuration is loaded from pyproject.toml."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false

[tool.yardang.llms]
enabled = true
description = "A project for LLMs"
build-parallel = false
suffix-mode = "replace"
full-build = false
"""
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Test Project\n\nTest content.")

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            from yardang.utils import get_config

            assert get_config(section="enabled", base="tool.yardang.llms") is True
            assert get_config(section="description", base="tool.yardang.llms") == "A project for LLMs"
            assert get_config(section="build-parallel", base="tool.yardang.llms") is False
            assert get_config(section="suffix-mode", base="tool.yardang.llms") == "replace"
            assert get_config(section="full-build", base="tool.yardang.llms") is False
        finally:
            os.chdir(original_cwd)

    def test_llms_config_defaults(self, tmp_path):
        """Test that llms configuration returns None when not specified."""
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

            assert get_config(section="enabled", base="tool.yardang.llms") is None
            assert get_config(section="suffix-mode", base="tool.yardang.llms") is None
        finally:
            os.chdir(original_cwd)

    def test_generate_docs_with_llms_enabled(self, tmp_path):
        """Test that generate_docs_configuration wires in the sphinx-llm extension."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false

[tool.yardang.llms]
enabled = true
description = "A project for LLMs"
suffix-mode = "replace"
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
                conf_content = (Path(conf_dir) / "conf.py").read_text()

                assert "use_llms = True" in conf_content
                assert 'extensions.append("sphinx_llm.txt")' in conf_content
                assert "llms_txt_suffix_mode" in conf_content
                assert "replace" in conf_content
                assert "A project for LLMs" in conf_content
        finally:
            os.chdir(original_cwd)

    def test_generate_docs_llms_disabled_by_default(self, tmp_path):
        """Test that llms.txt generation is off unless explicitly enabled."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false
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
                conf_content = (Path(conf_dir) / "conf.py").read_text()

                assert "use_llms = False" in conf_content
        finally:
            os.chdir(original_cwd)
