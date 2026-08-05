import re
from pathlib import Path

from yardang.build import generate_docs_configuration
from yardang.cli import build


def _write_project(tmp_path: Path, *, full_build: bool = True) -> None:
    (tmp_path / "pyproject.toml").write_text(
        f"""
[project]
name = "test-project"
version = "1.0.0"

[tool.yardang]
title = "Test Project"
root = "README.md"
pages = ["guide.md"]
use-autoapi = false

[tool.yardang.llms]
enabled = true
description = "A project for LLMs"
full-build = {str(full_build).lower()}
"""
    )
    (tmp_path / "README.md").write_text("# Test Project\n\nProject overview.\n")
    (tmp_path / "guide.md").write_text("# Guide\n\nGuide summary for language models.\n")
    (tmp_path / "orphan.md").write_text("# Orphan\n\nThis page is not in the toctree.\n")


def test_generated_configuration_enables_yardang_llms(tmp_path, monkeypatch):
    _write_project(tmp_path)
    monkeypatch.chdir(tmp_path)

    with generate_docs_configuration() as conf_dir:
        conf_content = (Path(conf_dir) / "conf.py").read_text()

    assert "use_llms = True" in conf_content
    assert 'extensions.append("yardang.sphinx.llms")' in conf_content
    assert 'yardang_llms_description = """A project for LLMs"""' in conf_content
    assert "yardang_llms_full_build = True" in conf_content
    assert "sphinx_llm" not in conf_content
    assert not (tmp_path / "conf.py").exists()


def test_build_generates_llms_outputs(tmp_path, monkeypatch):
    _write_project(tmp_path)
    monkeypatch.chdir(tmp_path)
    output = tmp_path / "html"

    build(quiet=True, output=str(output))

    assert (output / "index.html").is_file()
    assert (output / "guide.html").is_file()
    assert (output / "index.html.md").is_file()
    assert (output / "guide.html.md").is_file()
    assert not (output / "orphan.html.md").exists()
    assert (output / "llms-full.txt").is_file()

    sitemap = (output / "llms.txt").read_text()
    assert sitemap.startswith("# Test Project\n\n> A project for LLMs\n")
    assert "- [Test Project](index.html.md): Project overview." in sitemap
    assert "- [Guide](guide.html.md): Guide summary for language models." in sitemap
    assert "Orphan" not in sitemap
    assert "[llms-full.txt](llms-full.txt)" in sitemap

    for target in re.findall(r"\]\(([^)]+)\)", sitemap):
        assert (output / target).is_file()


def test_full_build_can_be_disabled(tmp_path, monkeypatch):
    _write_project(tmp_path)
    monkeypatch.chdir(tmp_path)
    output = tmp_path / "html"

    build(quiet=True, output=str(output))
    assert (output / "llms-full.txt").is_file()

    _write_project(tmp_path, full_build=False)
    build(quiet=True, output=str(output))

    assert (output / "llms.txt").is_file()
    assert not (output / "llms-full.txt").exists()
    assert "llms-full.txt" not in (output / "llms.txt").read_text()


def test_llms_generation_is_disabled_by_default(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "test-project"\nversion = "1.0.0"\n\n[tool.yardang]\nuse-autoapi = false\n')
    (tmp_path / "README.md").write_text("# Test Project\n")
    monkeypatch.chdir(tmp_path)
    output = tmp_path / "html"

    build(quiet=True, output=str(output))

    assert (output / "index.html").is_file()
    assert not (output / "llms.txt").exists()
