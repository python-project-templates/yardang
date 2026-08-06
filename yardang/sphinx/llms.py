from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from docutils import nodes
from sphinx.application import Sphinx
from sphinx_markdown_builder.builder import MarkdownBuilder
from sphinx_markdown_builder.translator import MarkdownTranslator

from yardang import __version__

_DOCNAMES_ATTRIBUTE = "_yardang_llms_docnames"


def _target_uri(docname: str) -> str:
    return f"{docname}.html.md"


class _LlmsMarkdownTranslator(MarkdownTranslator):
    def visit_toctree(self, node: nodes.Node) -> None:
        raise nodes.SkipNode

    def _fetch_ref_uri(self, node: nodes.Node) -> str:
        refuri = super()._fetch_ref_uri(node)
        parsed = urlsplit(refuri)
        if parsed.scheme or parsed.netloc or not parsed.path.endswith(".html"):
            return refuri
        return urlunsplit(parsed._replace(path=f"{parsed.path}.md"))


class _MarkdownRenderer:
    """Render resolved Sphinx doctrees without running a second builder."""

    name = "yardang-llms"
    format = "markdown"
    default_translator_class = _LlmsMarkdownTranslator

    def __init__(self, app: Sphinx):
        self.app = app
        self.config = app.config
        self.current_doc_name = ""

    def create_translator(self, *args):
        return self.app.registry.create_translator(self, *args)

    @staticmethod
    def get_target_uri(docname: str, typ: str | None = None) -> str:
        return _target_uri(docname)

    def render(self, docname: str, doctree: nodes.document) -> str:
        self.current_doc_name = docname
        translator = self.create_translator(doctree, self)
        doctree.walkabout(translator)
        return translator.astext()


class LlmsBuilder(MarkdownBuilder):
    """Retain an explicit builder for direct Sphinx use."""

    name = "yardang-llms"
    epilog = "The LLM-friendly documentation is in %(outdir)s."

    def init(self):
        super().init()
        self.out_suffix = ".html.md"

    def get_outdated_docs(self):
        for docname in self.env.collect_relations():
            source_mtime = self._get_source_mtime(docname)
            target_mtime = self._get_target_mtime(docname)
            if docname not in self.env.all_docs or source_mtime is None or target_mtime is None or source_mtime > target_mtime:
                yield docname

    def get_target_uri(self, docname: str, typ: str | None = None) -> str:
        return _target_uri(docname)

    def finish(self) -> None:
        docnames = list(self.env.collect_relations())
        _write_sitemap(self.app, docnames)
        _write_full_document(self.app, docnames)


def _prepare_markdown(app: Sphinx, builder) -> None:
    if builder.name == "html":
        setattr(app, _DOCNAMES_ATTRIBUTE, frozenset(app.env.collect_relations()))


def _write_markdown(app: Sphinx, doctree: nodes.document, docname: str) -> None:
    docnames = getattr(app, _DOCNAMES_ATTRIBUTE, None)
    if docnames is None:
        docnames = frozenset(app.env.collect_relations())
        setattr(app, _DOCNAMES_ATTRIBUTE, docnames)
    if app.builder.name != "html" or docname not in docnames:
        return

    renderer = _MarkdownRenderer(app)
    target = Path(app.outdir) / renderer.get_target_uri(docname)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(renderer.render(docname, doctree), encoding="utf-8")


def _build_llms(app: Sphinx, exception: Exception | None) -> None:
    if exception is not None or app.builder.name != "html":
        return

    renderer = _MarkdownRenderer(app)
    docnames = list(app.env.collect_relations())
    for docname in docnames:
        target = Path(app.outdir) / renderer.get_target_uri(docname)
        if target.is_file():
            continue
        doctree = app.env.get_and_resolve_doctree(docname, app.builder)
        if not target.is_file():
            _write_markdown(app, doctree, docname)
    _write_sitemap(app, docnames)
    _write_full_document(app, docnames)


def _write_sitemap(app: Sphinx, docnames: list[str]) -> None:
    lines = [f"# {app.config.yardang_llms_title}", ""]
    description = app.config.yardang_llms_description.strip()
    if description:
        lines.extend(f"> {line}" for line in description.splitlines())
        lines.append("")

    lines.extend(["## Pages", ""])
    for docname in docnames:
        lines.append(f"- [{_title(app, docname)}]({_target_uri(docname)}): {_description(app, docname)}")

    if app.config.yardang_llms_full_build:
        lines.extend(["", "## Full documentation", "", "- [llms-full.txt](llms-full.txt): All pages in one document."])

    (Path(app.outdir) / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_full_document(app: Sphinx, docnames: list[str]) -> None:
    full_path = Path(app.outdir) / "llms-full.txt"
    if not app.config.yardang_llms_full_build:
        full_path.unlink(missing_ok=True)
        return

    content = []
    for docname in docnames:
        uri = _target_uri(docname)
        page = (Path(app.outdir) / uri).read_text(encoding="utf-8").strip()
        content.append(f"<!-- {uri} -->\n\n{page}")
    full_path.write_text("\n\n".join(content) + "\n", encoding="utf-8")


def _title(app: Sphinx, docname: str) -> str:
    if docname == app.config.root_doc:
        return app.config.yardang_llms_title
    title = app.env.titles.get(docname)
    return title.astext() if title is not None else docname.rsplit("/", 1)[-1].replace("_", " ").title()


def _description(app: Sphinx, docname: str) -> str:
    metadata_description = app.env.metadata.get(docname, {}).get("description")
    if metadata_description:
        return _shorten(metadata_description)

    doctree = app.env.get_doctree(docname)
    for node in doctree.findall(nodes.meta):
        if node.get("name") == "description" and node.get("content"):
            return _shorten(node["content"])
    for node in doctree.findall(nodes.paragraph):
        if any(node.findall(nodes.image)):
            continue
        if text := node.astext().strip():
            return _shorten(text)
    return "Documentation page."


def _shorten(value: str, limit: int = 160) -> str:
    text = " ".join(value.split())
    return text if len(text) <= limit else f"{text[: limit - 3].rstrip()}..."


def setup(app: Sphinx) -> dict[str, object]:
    """Generate LLM-friendly files after a successful HTML build."""
    app.setup_extension("sphinx_markdown_builder")
    app.add_config_value("yardang_llms_title", "Documentation", "")
    app.add_config_value("yardang_llms_description", "", "")
    app.add_config_value("yardang_llms_full_build", True, "")
    app.add_builder(LlmsBuilder)
    app.connect("write-started", _prepare_markdown)
    app.connect("doctree-resolved", _write_markdown, priority=900)
    app.connect("build-finished", _build_llms)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
