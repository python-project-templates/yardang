import os.path
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader

from .utils import get_config

__all__ = ("generate_docs_configuration",)


@contextmanager
def generate_docs_configuration(
    *,
    project: str = "",
    title: str = "",
    module: str = "",
    description: str = "",
    author: str = "",
    copyright: str = "",
    version: str = "",
    theme: str = "furo",
    docs_root: str = "",
    root: str = "",
    cname: str = "",
    pages: Optional[List] = None,
    use_autoapi: Optional[bool] = None,
    custom_css: Optional[Path] = None,
    custom_js: Optional[Path] = None,
):
    if os.path.exists("conf.py"):
        # yield folder path to sphinx build
        yield os.path.curdir
    else:
        # load configuration
        default_data = os.path.split(os.getcwd())[-1]
        project = project or get_config(section="name", base="project") or default_data.replace("_", "-")
        title = title or get_config(section="title") or default_data.replace("_", "-")
        module = module or project.replace("-", "_") or default_data.replace("-", "_")
        description = description or get_config(section="name", base="description") or default_data.replace("_", " ").replace("-", " ")
        author = author or get_config(section="authors", base="project")
        if isinstance(author, list) and len(author) > 0:
            author = author[0]
        else:
            author = f"The {project} authors"
        if isinstance(author, dict):
            author = author["name"]
        copyright = copyright or author
        theme = theme or get_config(section="theme")
        version = version or get_config(section="version", base="project")
        docs_root = (
            docs_root
            or get_config(section="docs-host")
            or get_config(section="urls.Homepage", base="project")
            or get_config(section="urls.homepage", base="project")
            or get_config(section="urls.Documentation", base="project")
            or get_config(section="urls.documentation", base="project")
            or get_config(section="urls.Source", base="project")
            or get_config(section="urls.source", base="project")
            or ""
        )
        root = root or get_config(section="root")
        cname = cname or get_config(section="cname")
        pages = pages or get_config(section="pages") or []
        use_autoapi = use_autoapi or get_config(section="use-autoapi")

        custom_css = custom_css or get_config(section="custom-css") or (Path(__file__).parent / "custom.css")
        custom_js = custom_js or get_config(section="custom-js") or (Path(__file__).parent / "custom.js")

        source_dir = os.path.curdir

        configuration_args = {}
        for f in (
            # autodoc/autodoc-pydantic
            "autodoc_pydantic_model_show_config_summary",
            "autodoc_pydantic_model_show_validator_summary",
            "autodoc_pydantic_model_show_validator_members",
            "autodoc_pydantic_field_list_validators",
            "autodoc_pydantic_field_show_constraints",
            "autodoc_pydantic_model_member_order",
            "autodoc_pydantic_model_show_json",
            "autodoc_pydantic_settings_show_json",
            "autodoc_pydantic_model_show_field_summary",
            # myst/myst-nb
            "nb_execution_mode",
            "nb_execution_excludepatterns",
        ):
            default_value = {
                # autodoc/autodoc-pydantic
                "autodoc_pydantic_model_member_order": '"bysource"',
                "autodoc_pydantic_model_show_json": True,
                # myst/myst-nb
                "nb_execution_excludepatterns": [],
                "nb_execution_mode": "off",
            }.get(f, False)
            config_value = get_config(section=f"{f}")
            configuration_args[f] = default_value if config_value is None else config_value
        # create a temporary directory to store the conf.py file in
        with TemporaryDirectory() as td:
            templateEnv = Environment(loader=FileSystemLoader(searchpath=str(Path(__file__).parent.resolve())))
            # load the templatized conf.py file
            template = templateEnv.get_template("conf.py.j2").render(
                project=project,
                title=title,
                module=module,
                description=description,
                author=author,
                copyright=copyright,
                version=version,
                theme=theme,
                docs_root=docs_root,
                root=root,
                cname=cname,
                pages=pages,
                use_autoapi=use_autoapi,
                source_dir=source_dir,
                **configuration_args,
            )
            # dump to file
            template_file = Path(td) / "conf.py"
            template_file.write_text(template)

            # write custom css and customjs
            Path("docs/html/_static/styles").mkdir(parents=True, exist_ok=True)
            Path("docs/html/_static/styles/custom.css").write_text(custom_css.read_text())
            Path("docs/html/_static/js").mkdir(parents=True, exist_ok=True)
            Path("docs/html/_static/js/custom.js").write_text(custom_js.read_text())

            # append docs-specific ignores to gitignore
            if Path(".gitignore").exists():
                has_html_build_folder = False
                has_index_md = False
                with open(".gitignore", "r+") as fp:
                    for line in fp:
                        if "docs/html" in line:
                            has_html_build_folder = True
                        if "index.md" in line:
                            has_index_md = True
                    if not has_html_build_folder or not has_index_md:
                        fp.write("\n")
                        if not has_html_build_folder:
                            fp.write("docs/html\n")
                        if not has_index_md:
                            fp.write("index.md\n")
            # yield folder path to sphinx build
            yield td
