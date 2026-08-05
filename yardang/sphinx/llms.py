from pathlib import Path

from docutils import nodes
from sphinx_markdown_builder.builder import MarkdownBuilder

from yardang import __version__


class LlmsBuilder(MarkdownBuilder):
    """Build LLM-friendly Markdown and index files."""

    name = "yardang-llms"
    epilog = "The LLM-friendly documentation is in %(outdir)s."

    def init(self):
        super().init()
        self.out_suffix = ".html.md"

    def get_outdated_docs(self):
        for docname in self._ordered_docnames():
            source_mtime = self._get_source_mtime(docname)
            target_mtime = self._get_target_mtime(docname)
            if docname not in self.env.all_docs or source_mtime is None or target_mtime is None or source_mtime > target_mtime:
                yield docname

    def get_target_uri(self, docname: str, typ: str | None = None):
        return f"{docname}{self.out_suffix}"

    def finish(self):
        docnames = self._ordered_docnames()
        self._write_sitemap(docnames)

        full_path = Path(self.outdir) / "llms-full.txt"
        if self.config.yardang_llms_full_build:
            content = []
            for docname in docnames:
                target = Path(self.outdir) / self.get_target_uri(docname)
                content.append(f"<!-- {self.get_target_uri(docname)} -->\n\n{target.read_text(encoding='utf-8').strip()}")
            full_path.write_text("\n\n".join(content) + "\n", encoding="utf-8")
        else:
            full_path.unlink(missing_ok=True)

    def _ordered_docnames(self) -> list[str]:
        return list(self.env.collect_relations())

    def _write_sitemap(self, docnames: list[str]) -> None:
        lines = [f"# {self.config.yardang_llms_title}", ""]
        description = self.config.yardang_llms_description.strip()
        if description:
            lines.extend(f"> {line}" for line in description.splitlines())
            lines.append("")

        lines.extend(["## Pages", ""])
        for docname in docnames:
            lines.append(f"- [{self._title(docname)}]({self.get_target_uri(docname)}): {self._description(docname)}")

        if self.config.yardang_llms_full_build:
            lines.extend(["", "## Full documentation", "", "- [llms-full.txt](llms-full.txt): All pages in one document."])

        (Path(self.outdir) / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _title(self, docname: str) -> str:
        if docname == self.config.root_doc:
            return self.config.yardang_llms_title
        title = self.env.titles.get(docname)
        return title.astext() if title is not None else docname.rsplit("/", 1)[-1].replace("_", " ").title()

    def _description(self, docname: str) -> str:
        metadata_description = self.env.metadata.get(docname, {}).get("description")
        if metadata_description:
            return self._shorten(metadata_description)

        doctree = self.env.get_doctree(docname)
        for node in doctree.findall(nodes.meta):
            if node.get("name") == "description" and node.get("content"):
                return self._shorten(node["content"])
        for node in doctree.findall(nodes.paragraph):
            if any(node.findall(nodes.image)):
                continue
            if text := node.astext().strip():
                return self._shorten(text)
        return "Documentation page."

    @staticmethod
    def _shorten(value: str, limit: int = 160) -> str:
        text = " ".join(value.split())
        return text if len(text) <= limit else f"{text[: limit - 3].rstrip()}..."


def setup(app) -> dict[str, object]:
    """Register Yardang's LLM-friendly Markdown builder."""
    app.setup_extension("sphinx_markdown_builder")
    app.add_config_value("yardang_llms_title", "Documentation", "")
    app.add_config_value("yardang_llms_description", "", "")
    app.add_config_value("yardang_llms_full_build", True, "")
    app.add_builder(LlmsBuilder)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
