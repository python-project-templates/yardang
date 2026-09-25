import importlib.util
from pathlib import Path

from yardang import __version__
from yardang.build import generate_docs_configuration
from yardang.sphinx import setup


def test_setup_returns_extension_metadata():
    assert setup(None) == {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


def test_generated_configuration_enables_extension(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "test-project"\nversion = "1.0.0"\n')
    (tmp_path / "README.md").write_text("# Test Project\n")
    monkeypatch.chdir(tmp_path)

    with generate_docs_configuration() as conf_dir:
        conf_content = (Path(conf_dir) / "conf.py").read_text()

    assert '"yardang.sphinx"' in conf_content


def test_github_admonition_preserves_quoted_blank_lines(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "test-project"\nversion = "1.0.0"\n')
    (tmp_path / "README.md").write_text("# Test Project\n")
    monkeypatch.chdir(tmp_path)

    with generate_docs_configuration() as conf_dir:
        spec = importlib.util.spec_from_file_location("yardang_test_conf", Path(conf_dir) / "conf.py")
        conf = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(conf)

        lines = ["> [!NOTE]\n> First paragraph.\n>\n> Second paragraph."]
        conf.run_convert_github_admonitions_to_rst(None, "index.md", lines)

    assert lines == [":::{note}\n\n  First paragraph.\n\n  Second paragraph."]
