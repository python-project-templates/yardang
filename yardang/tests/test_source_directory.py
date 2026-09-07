from pathlib import Path
from unittest.mock import patch

import pytest
from typer import Exit

from yardang.build import generate_docs_configuration
from yardang.cli import build


@pytest.fixture
def source_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text("""
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
source-dir = "docs/source"
use-autoapi = false
use-search = false
html-static-path = ["_static"]
html-extra-path = ["extra"]
cname = "docs.example.com"
""")
    source = tmp_path / "docs/source"
    source.mkdir(parents=True)
    (source / "index.rst").write_text("Test Project\n============\n\n.. include:: introduction.rst\n\n.. toctree::\n\n   guide\n")
    (source / "introduction.rst").write_text("Existing introduction.\n")
    (source / "guide.rst").write_text("Guide\n=====\n\nExisting guide.\n")
    (source / "_static").mkdir()
    (source / "_static/site.css").write_text("body { color: navy; }\n")
    (source / "extra").mkdir()
    (source / "extra/robots.txt").write_text("User-agent: *\n")
    (tmp_path / ".gitignore").write_text(".venv/\n")
    return source


def test_existing_sources_are_not_rewritten(source_project):
    original = (source_project / "index.rst").read_bytes()
    with generate_docs_configuration() as conf_dir:
        conf = (Path(conf_dir) / "conf.py").read_text()
        assert 'master_doc = "index"' in conf
        assert 'app.connect("builder-inited", run_copyreadme)' not in conf
        assert str(source_project / "_static") in conf
        assert str(source_project / "extra") in conf
    assert (source_project / "index.rst").read_bytes() == original
    assert not (source_project / "index.md").exists()
    assert not Path("index.md").exists()
    assert Path(".gitignore").read_text() == ".venv/\n"


def test_missing_root_fails_before_generating_files(source_project):
    with pytest.raises(FileNotFoundError, match="missing.rst"), generate_docs_configuration(root="missing.rst"):
        pass
    assert not Path("index.md").exists()


def test_custom_root(source_project):
    with generate_docs_configuration(root="guide.rst") as conf_dir:
        assert 'master_doc = "guide"' in (Path(conf_dir) / "conf.py").read_text()


def test_cli_source_directory_overrides_configuration(source_project):
    with patch("yardang.cli.Popen") as popen:
        popen.return_value.poll.return_value = 0
        popen.return_value.returncode = 0
        build(source_dir=str(source_project), output="site", warning_is_error=True)
    assert popen.call_args.args[0][3:5] == [str(source_project), "site"]
    assert popen.call_args.args[0][-2:] == ["-W", "--keep-going"]


@pytest.mark.parametrize("theme", ["furo", "klink"])
def test_build_existing_rst_site(source_project, theme):
    build(output="site", theme=theme, warning_is_error=True)
    assert "Existing introduction." in Path("site/index.html").read_text()
    assert "Existing guide." in Path("site/guide.html").read_text()
    assert Path("site/_static/site.css").is_file()
    assert Path("site/robots.txt").is_file()
    assert Path("site/CNAME").read_text() == "docs.example.com"
    assert not Path("index.md").exists()


def test_build_existing_markdown_root(source_project):
    (source_project / "README.md").write_text("# Existing Markdown\n\n```{toctree}\nindex\n```\n")
    build(root="README.md", output="site", warning_is_error=True)
    assert "Existing Markdown" in Path("site/README.html").read_text()
    assert not Path("index.md").exists()


def test_strict_build_fails_on_warnings(source_project):
    (source_project / "guide.rst").write_text("Guide\n=====\n\n.. toctree::\n\n   missing-page\n")
    with pytest.raises(Exit):
        build(output="site", warning_is_error=True)


def test_klink_theme_path(source_project):
    with generate_docs_configuration(theme="klink") as conf_dir:
        conf = (Path(conf_dir) / "conf.py").read_text()
        assert 'html_theme = "klink"' in conf
        assert "html_theme_path = [klink.get_html_theme_path()]" in conf
