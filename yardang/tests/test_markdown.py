import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace

from yardang.build import generate_docs_configuration
from yardang.markdown import rebase_relative_references


def test_rebases_markdown_and_html_references():
    content = """[Guide](./guide.md#start)
![Diagram](../img/diagram.svg?raw=1)
[reference]: ../files/example.csv "Example"
<a href="../../CHANGELOG.md">Changes</a>
<img src='../img/diagram.svg'>
<source srcset="../img/small.svg 1x, ../img/large.svg 2x">
"""

    result = rebase_relative_references(
        content,
        source=Path("docs/src/home.md"),
        destination=Path("index.md"),
    )

    assert "[Guide](docs/src/guide.md#start)" in result
    assert "![Diagram](docs/img/diagram.svg?raw=1)" in result
    assert '[reference]: docs/files/example.csv "Example"' in result
    assert '<a href="CHANGELOG.md">Changes</a>' in result
    assert "<img src='docs/img/diagram.svg'>" in result
    assert 'srcset="docs/img/small.svg 1x, docs/img/large.svg 2x"' in result


def test_leaves_non_relative_references_unchanged():
    content = """[Web](https://example.com/docs)
[Protocol relative](//cdn.example.com/image.svg)
[Root relative](/assets/image.svg)
[Anchor](#section)
[Email](mailto:docs@example.com)
<img src="data:image/svg+xml;base64,PHN2Zz4=">
"""

    assert (
        rebase_relative_references(
            content,
            source=Path("docs/src/home.md"),
            destination=Path("index.md"),
        )
        == content
    )


def test_rebases_mixed_data_and_local_srcset_candidates():
    content = """<source srcset="data:image/svg+xml,%3Csvg%3E 1x, ../img/large.svg 2x">
<source srcset="../img/small.svg 1x, data:image/svg+xml,%3Csvg%3E 2x">
"""

    result = rebase_relative_references(content, Path("docs/src/home.md"), Path("index.md"))

    assert 'srcset="data:image/svg+xml,%3Csvg%3E 1x, docs/img/large.svg 2x"' in result
    assert 'srcset="docs/img/small.svg 1x, data:image/svg+xml,%3Csvg%3E 2x"' in result


def test_rebases_descriptorless_mixed_srcset_candidates():
    content = """<source srcset="data:image/svg+xml,%3Csvg%3E, ../img/large.svg 2x">
<source srcset="../img/small.svg, data:image/svg+xml,%3Csvg%3E 2x">
"""

    result = rebase_relative_references(content, Path("docs/src/home.md"), Path("index.md"))

    assert 'srcset="data:image/svg+xml,%3Csvg%3E, docs/img/large.svg 2x"' in result
    assert 'srcset="docs/img/small.svg, data:image/svg+xml,%3Csvg%3E 2x"' in result


def test_leaves_code_examples_and_comments_unchanged():
    content = """`<img src="../img/inline.svg">`
```html
<img src="../img/fenced.svg">
```
<!-- <img src="../img/comment.svg"> -->
<img src="../img/rendered.svg">
"""

    result = rebase_relative_references(content, Path("docs/src/home.md"), Path("index.md"))

    assert '`<img src="../img/inline.svg">`' in result
    assert '<img src="../img/fenced.svg">' in result
    assert '<!-- <img src="../img/comment.svg"> -->' in result
    assert '<img src="docs/img/rendered.svg">' in result


def test_rebases_content_after_longer_closing_fences():
    content = (
        '```html\n<img src="../img/example.svg">\n````'
        '  \n<img src="../img/after-backticks.svg">\n~~~html\n'
        '<img src="../img/example.svg">\n~~~~\n<img src="../img/after-tildes.svg">\n'
    )

    result = rebase_relative_references(content, Path("docs/src/home.md"), Path("index.md"))

    assert content.splitlines()[1] in result
    assert content.splitlines()[5] in result
    assert '<img src="docs/img/after-backticks.svg">' in result
    assert '<img src="docs/img/after-tildes.svg">' in result


def test_rebases_angle_delimited_markdown_destinations():
    content = """[Guide](<guide files/start.md?view=full#intro>)
[guide]: <guide files/start.md?view=full#intro> "Guide"
"""

    result = rebase_relative_references(content, Path("docs/src/home.md"), Path("index.md"))

    assert "[Guide](<docs/src/guide files/start.md?view=full#intro>)" in result
    assert '[guide]: <docs/src/guide files/start.md?view=full#intro> "Guide"' in result


def test_rebases_exact_unquoted_html_attributes_only():
    content = """<img src=../img/rendered.svg>
<a href=./guide.md>Guide</a>
<img data-src="../img/lazy.svg">
<svg xlink:href="../img/symbol.svg"></svg>
"""

    result = rebase_relative_references(content, Path("docs/src/home.md"), Path("index.md"))

    assert "<img src=docs/img/rendered.svg>" in result
    assert "<a href=docs/src/guide.md>Guide</a>" in result
    assert '<img data-src="../img/lazy.svg">' in result
    assert '<svg xlink:href="../img/symbol.svg"></svg>' in result


def test_generated_configuration_rebases_root_references(tmp_path):
    (tmp_path / "docs" / "src").mkdir(parents=True)
    (tmp_path / "docs" / "img").mkdir()
    (tmp_path / "docs" / "img" / "diagram.svg").write_text("<svg></svg>")
    (tmp_path / "docs" / "img" / "diagram-dark.svg").write_text("<svg>dark</svg>")
    (tmp_path / "docs" / "img" / "literal.svg").write_text("<svg>literal</svg>")
    root_content = (
        '[Guide](./guide.md)\n<source srcset="data:image/svg+xml,%3Csvg%3E 1x, ../img/diagram-dark.svg 2x">\n'
        '<img src="../img/diagram.svg">\n`<img src="../img/literal.svg">`\n'
    )
    root_path = tmp_path / "docs" / "src" / "home.md"
    root_path.write_text(root_content)
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "test-project"\nversion = "1.0.0"\n\n[tool.yardang]\nroot = "docs/src/home.md"\n')

    original_cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        with generate_docs_configuration() as conf_dir:
            spec = importlib.util.spec_from_file_location("yardang_test_conf", Path(conf_dir) / "conf.py")
            assert spec is not None
            assert spec.loader is not None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.run_copyreadme(SimpleNamespace(outdir=tmp_path / "docs" / "html"))
    finally:
        os.chdir(original_cwd)

    generated = (tmp_path / "index.md").read_text()
    assert "[Guide](docs/src/guide.md)" in generated
    assert '<source srcset="data:image/svg+xml,%3Csvg%3E 1x, docs/img/diagram-dark.svg 2x">' in generated
    assert '<img src="docs/img/diagram.svg">' in generated
    assert (tmp_path / "docs" / "html" / "docs" / "img" / "diagram.svg").read_text() == "<svg></svg>"
    assert (tmp_path / "docs" / "html" / "docs" / "img" / "diagram-dark.svg").read_text() == "<svg>dark</svg>"
    assert not (tmp_path / "docs" / "html" / "docs" / "img" / "literal.svg").exists()
    assert root_path.read_text() == root_content
