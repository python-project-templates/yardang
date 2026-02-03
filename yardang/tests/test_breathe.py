"""Tests for breathe/doxygen integration in yardang."""

import os
from pathlib import Path


class TestBreatheConfiguration:
    """Tests for breathe configuration loading and generation."""

    def test_breathe_config_loading_from_pyproject(self, tmp_path):
        """Test that breathe configuration is loaded from pyproject.toml."""
        # Create a temporary pyproject.toml with breathe config
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false

[tool.yardang.breathe]
projects = { myproject = "docs/xml" }
default-project = "myproject"
domain-by-extension = { "hpp" = "cpp", "h" = "cpp" }
show-define-initializer = true
use-project-refids = true
"""
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Test Project\n\nTest content.")

        # Change to the temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            from yardang.utils import get_config

            # Test that breathe config is loaded correctly
            breathe_projects = get_config(section="projects", base="tool.yardang.breathe")
            assert breathe_projects == {"myproject": "docs/xml"}

            breathe_default_project = get_config(section="default-project", base="tool.yardang.breathe")
            assert breathe_default_project == "myproject"

            domain_by_extension = get_config(section="domain-by-extension", base="tool.yardang.breathe")
            assert domain_by_extension == {"hpp": "cpp", "h": "cpp"}

            show_define_initializer = get_config(section="show-define-initializer", base="tool.yardang.breathe")
            assert show_define_initializer is True

            use_project_refids = get_config(section="use-project-refids", base="tool.yardang.breathe")
            assert use_project_refids is True
        finally:
            os.chdir(original_cwd)

    def test_breathe_config_defaults(self, tmp_path):
        """Test that breathe configuration has sensible defaults when not specified."""
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

            # Test that missing breathe config returns None
            breathe_projects = get_config(section="projects", base="tool.yardang.breathe")
            assert breathe_projects is None

            breathe_default_project = get_config(section="default-project", base="tool.yardang.breathe")
            assert breathe_default_project is None
        finally:
            os.chdir(original_cwd)

    def test_generate_docs_with_breathe_config(self, tmp_path):
        """Test that generate_docs_configuration includes breathe settings."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false

[tool.yardang.breathe]
projects = { mylib = "xml" }
default-project = "mylib"
domain-by-extension = { "hpp" = "cpp" }
show-include = false
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

                # Check that breathe is included in extensions
                assert "breathe" in conf_content

                # Check that breathe configuration is present
                assert "breathe_projects" in conf_content
                assert "mylib" in conf_content
                assert "breathe_default_project" in conf_content
                assert "breathe_domain_by_extension" in conf_content
        finally:
            os.chdir(original_cwd)

    def test_breathe_disabled_when_not_configured(self, tmp_path):
        """Test that breathe extension is not added when not configured."""
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
                conf_path = Path(conf_dir) / "conf.py"
                conf_content = conf_path.read_text()

                # Check that use_breathe is False
                assert "use_breathe = False" in conf_content
        finally:
            os.chdir(original_cwd)


class TestBreatheConfigOptions:
    """Tests for individual breathe configuration options."""

    def test_all_breathe_options_parsed(self, tmp_path):
        """Test that all breathe configuration options are properly parsed."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false

[tool.yardang.breathe]
projects = { lib1 = "xml1", lib2 = "xml2" }
default-project = "lib1"
domain-by-extension = { "hpp" = "cpp", "h" = "c" }
domain-by-file-pattern = { "*.hpp" = "cpp" }
build-directory = "build/doxygen"
default-members = ["members", "protected-members"]
show-define-initializer = true
show-enumvalue-initializer = true
show-include = true
implementation-filename-extensions = [".c", ".cpp", ".cxx"]
doxygen-config-options = { EXTRACT_ALL = "YES" }
doxygen-aliases = { brief = "Short description" }
use-project-refids = true
order-parameters-first = true
separate-member-pages = false
"""
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Test Project\n\nTest content.")

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            from yardang.utils import get_config

            # Test all options
            assert get_config(section="projects", base="tool.yardang.breathe") == {"lib1": "xml1", "lib2": "xml2"}
            assert get_config(section="default-project", base="tool.yardang.breathe") == "lib1"
            assert get_config(section="domain-by-extension", base="tool.yardang.breathe") == {"hpp": "cpp", "h": "c"}
            assert get_config(section="domain-by-file-pattern", base="tool.yardang.breathe") == {"*.hpp": "cpp"}
            assert get_config(section="build-directory", base="tool.yardang.breathe") == "build/doxygen"
            assert get_config(section="default-members", base="tool.yardang.breathe") == ["members", "protected-members"]
            assert get_config(section="show-define-initializer", base="tool.yardang.breathe") is True
            assert get_config(section="show-enumvalue-initializer", base="tool.yardang.breathe") is True
            assert get_config(section="show-include", base="tool.yardang.breathe") is True
            assert get_config(section="implementation-filename-extensions", base="tool.yardang.breathe") == [".c", ".cpp", ".cxx"]
            assert get_config(section="doxygen-config-options", base="tool.yardang.breathe") == {"EXTRACT_ALL": "YES"}
            assert get_config(section="doxygen-aliases", base="tool.yardang.breathe") == {"brief": "Short description"}
            assert get_config(section="use-project-refids", base="tool.yardang.breathe") is True
            assert get_config(section="order-parameters-first", base="tool.yardang.breathe") is True
            assert get_config(section="separate-member-pages", base="tool.yardang.breathe") is False
        finally:
            os.chdir(original_cwd)


class TestBreatheConfPyGeneration:
    """Tests for the generated conf.py file with breathe configuration."""

    def test_conf_py_contains_breathe_extension(self, tmp_path):
        """Test that the generated conf.py contains the breathe extension."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false

[tool.yardang.breathe]
projects = { mylib = "xml" }
default-project = "mylib"
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

                # Verify extension is added conditionally
                assert 'extensions.append("breathe")' in conf_content
        finally:
            os.chdir(original_cwd)

    def test_conf_py_contains_all_breathe_options(self, tmp_path):
        """Test that all breathe options are rendered in conf.py."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false

[tool.yardang.breathe]
projects = { mylib = "xml" }
default-project = "mylib"
domain-by-extension = { "hpp" = "cpp" }
show-define-initializer = true
use-project-refids = true
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

                # Verify all options are present
                assert "breathe_projects = " in conf_content
                # Path is resolved to absolute, so just check the key is present
                assert "'mylib':" in conf_content
                assert "breathe_default_project = " in conf_content
                assert "breathe_domain_by_extension = " in conf_content
                assert "breathe_show_define_initializer = True" in conf_content
                assert "breathe_use_project_refids = True" in conf_content
        finally:
            os.chdir(original_cwd)


class TestDoxygenAutoRun:
    """Tests for automatic doxygen detection and execution."""

    def test_run_doxygen_if_needed_no_doxygen(self, tmp_path, monkeypatch):
        """Test that run_doxygen_if_needed returns empty dict when doxygen not installed."""
        import shutil

        from yardang.build import run_doxygen_if_needed

        # Mock shutil.which to return None (doxygen not found)
        monkeypatch.setattr(shutil, "which", lambda x: None)

        result = run_doxygen_if_needed({"mylib": str(tmp_path / "xml")})
        assert result == {}

    def test_run_doxygen_if_needed_xml_exists(self, tmp_path, monkeypatch):
        """Test that doxygen is not run if XML already exists."""
        import shutil

        from yardang.build import run_doxygen_if_needed

        # Create existing XML directory with files
        xml_dir = tmp_path / "xml"
        xml_dir.mkdir()
        (xml_dir / "index.xml").write_text("<doxygen></doxygen>")

        # Mock doxygen as available
        monkeypatch.setattr(shutil, "which", lambda x: "/usr/bin/doxygen" if x == "doxygen" else None)

        result = run_doxygen_if_needed({"mylib": str(xml_dir)}, quiet=True)
        assert result == {"mylib": True}

    def test_run_doxygen_if_needed_force(self, tmp_path, monkeypatch):
        """Test that force=True runs doxygen even if XML exists."""
        import shutil
        import subprocess

        from yardang.build import run_doxygen_if_needed

        # Create existing XML directory with files
        xml_dir = tmp_path / "xml"
        xml_dir.mkdir()
        (xml_dir / "index.xml").write_text("<doxygen></doxygen>")

        # Create a Doxyfile in parent
        doxyfile = tmp_path / "Doxyfile"
        doxyfile.write_text("OUTPUT_DIRECTORY = xml\nGENERATE_XML = YES\n")

        # Mock doxygen as available
        monkeypatch.setattr(shutil, "which", lambda x: "/usr/bin/doxygen" if x == "doxygen" else None)

        # Mock subprocess.run
        run_called = []

        def mock_run(cmd, **kwargs):
            run_called.append(cmd)

            class MockResult:
                returncode = 0

            return MockResult()

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = run_doxygen_if_needed({"mylib": str(xml_dir)}, force=True, quiet=True)
        assert result == {"mylib": True}
        assert len(run_called) == 1

    def test_run_doxygen_if_needed_no_doxyfile(self, tmp_path, monkeypatch):
        """Test that warning is shown if no Doxyfile found."""
        import shutil

        from yardang.build import run_doxygen_if_needed

        # Create XML directory path but no Doxyfile
        xml_dir = tmp_path / "xml"

        # Mock doxygen as available
        monkeypatch.setattr(shutil, "which", lambda x: "/usr/bin/doxygen" if x == "doxygen" else None)

        result = run_doxygen_if_needed({"mylib": str(xml_dir)}, quiet=True)
        assert result == {"mylib": False}

    def test_run_doxygen_if_needed_runs_doxygen(self, tmp_path, monkeypatch):
        """Test that doxygen is run when XML doesn't exist but Doxyfile does."""
        import shutil
        import subprocess

        from yardang.build import run_doxygen_if_needed

        # Create Doxyfile in parent of xml dir
        xml_dir = tmp_path / "xml"
        doxyfile = tmp_path / "Doxyfile"
        doxyfile.write_text("OUTPUT_DIRECTORY = xml\nGENERATE_XML = YES\n")

        # Mock doxygen as available
        monkeypatch.setattr(shutil, "which", lambda x: "/usr/bin/doxygen" if x == "doxygen" else None)

        # Track subprocess.run calls
        run_called = []

        def mock_run(cmd, **kwargs):
            run_called.append((cmd, kwargs.get("cwd")))

            class MockResult:
                returncode = 0

            return MockResult()

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = run_doxygen_if_needed({"mylib": str(xml_dir)}, quiet=True)
        assert result == {"mylib": True}
        assert len(run_called) == 1
        assert run_called[0][1] == tmp_path  # cwd should be Doxyfile's parent

    def test_auto_run_doxygen_config_option(self, tmp_path):
        """Test that auto-run-doxygen config option is respected."""
        pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
use-autoapi = false

[tool.yardang.breathe]
projects = { mylib = "xml" }
default-project = "mylib"
auto-run-doxygen = false
"""
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)

        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Test Project")

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            from yardang.utils import get_config

            auto_run = get_config(section="auto-run-doxygen", base="tool.yardang.breathe")
            assert auto_run is False
        finally:
            os.chdir(original_cwd)
