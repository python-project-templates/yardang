import os.path
import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader

from .utils import get_config

__all__ = ("generate_docs_configuration", "run_doxygen_if_needed")


def run_doxygen_if_needed(
    breathe_projects: Dict[str, str],
    *,
    force: bool = False,
    quiet: bool = False,
) -> Dict[str, bool]:
    """Run doxygen for breathe projects if needed.

    For each project in breathe_projects, checks if the XML output directory
    exists. If not, attempts to find a Doxyfile in the parent directory and
    runs doxygen to generate the XML.

    Args:
        breathe_projects: Dict mapping project names to XML output directories.
        force: If True, run doxygen even if XML directory already exists.
        quiet: If True, suppress doxygen output.

    Returns:
        Dict mapping project names to whether doxygen was run successfully.
        Returns empty dict if doxygen is not installed.

    Example:
        >>> results = run_doxygen_if_needed({"mylib": "docs/xml"})
        >>> if results.get("mylib"):
        ...     print("Doxygen ran successfully")
    """
    # Check if doxygen is available
    doxygen_path = shutil.which("doxygen")
    if not doxygen_path:
        return {}

    results = {}
    for project_name, xml_path in breathe_projects.items():
        xml_dir = Path(xml_path)

        # Check if XML already exists (unless force is True)
        if not force and xml_dir.exists() and any(xml_dir.glob("*.xml")):
            results[project_name] = True
            continue

        # Try to find Doxyfile in parent directory of XML output
        # Common patterns: xml is in same dir as Doxyfile, or xml/ subdir
        search_dirs = [
            xml_dir.parent,  # xml is a subdirectory
            xml_dir,  # xml output is in same directory as Doxyfile
        ]

        doxyfile_path = None
        for search_dir in search_dirs:
            candidate = search_dir / "Doxyfile"
            if candidate.exists():
                doxyfile_path = candidate
                break

        if not doxyfile_path:
            if not quiet:
                print(f"Warning: No Doxyfile found for project '{project_name}'")
            results[project_name] = False
            continue

        # Run doxygen
        try:
            if not quiet:
                print(f"Running doxygen for project '{project_name}'...")

            kwargs = {"cwd": doxyfile_path.parent}
            if quiet:
                kwargs["stdout"] = subprocess.DEVNULL
                kwargs["stderr"] = subprocess.DEVNULL

            result = subprocess.run([doxygen_path], **kwargs)
            results[project_name] = result.returncode == 0

            if not quiet and result.returncode == 0:
                print(f"  Generated XML documentation in {xml_dir}")
            elif not quiet:
                print(f"  Doxygen failed with return code {result.returncode}")
        except Exception as e:
            if not quiet:
                print(f"  Error running doxygen: {e}")
            results[project_name] = False

    return results


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
    autoapi_ignore: Optional[List] = None,
    custom_css: Optional[Path] = None,
    custom_js: Optional[Path] = None,
    config_base: str = "tool.yardang",
    previous_versions: Optional[bool] = False,
    adjust_arguments: Callable = None,
    adjust_template: Callable = None,
):
    """Generate Sphinx documentation configuration from pyproject.toml.

    A context manager that creates a temporary Sphinx configuration (conf.py)
    based on settings from pyproject.toml and yields the configuration directory
    path for use with sphinx-build. If a conf.py already exists in the current
    directory, it yields the current directory instead.

    Configuration is read from the ``[tool.yardang]`` section of pyproject.toml
    by default, with breathe/doxygen settings in ``[tool.yardang.breathe]``.

    Args:
        project: Project name. Falls back to ``[project].name`` or directory name.
        title: Documentation title. Falls back to ``[tool.yardang].title`` or project name.
        module: Python module name for autoapi. Falls back to project name with
            hyphens replaced by underscores.
        description: Project description for metadata.
        author: Author name. Falls back to first entry in ``[project].authors``.
        copyright: Copyright string. Falls back to author name.
        version: Version string. Falls back to ``[project].version``.
        theme: Sphinx theme name. Defaults to ``"furo"``.
        docs_root: Base URL for hosted documentation. Used for canonical URLs.
        root: Path to README or index file to use as documentation root.
        cname: Custom domain name for GitHub Pages CNAME file.
        pages: List of page paths to include in the toctree.
        use_autoapi: Whether to use sphinx-autoapi for Python API docs.
            Defaults to ``None`` (auto-detect).
        custom_css: Path to custom CSS file. Defaults to bundled custom.css.
        custom_js: Path to custom JavaScript file. Defaults to bundled custom.js.
        config_base: Base key in pyproject.toml for configuration.
            Defaults to ``"tool.yardang"``.
        previous_versions: Whether to generate previous versions documentation.
        adjust_arguments: Callback to modify template arguments before rendering.
            Receives the args dict and should return the modified dict.
        adjust_template: Callback to modify the Jinja2 template before rendering.
            Receives the template and should return the modified template.

    Yields:
        str: Path to directory containing the generated conf.py file,
            or the current directory if conf.py already exists.

    Raises:
        FileNotFoundError: If custom_css or custom_js paths don't exist.
        toml.TomlDecodeError: If pyproject.toml is malformed.

    Example:
        Basic usage with sphinx-build::

            from yardang import generate_docs_configuration

            with generate_docs_configuration() as config_dir:
                subprocess.run(["sphinx-build", "-c", config_dir, ".", "docs/html"])

        With custom arguments callback::

            def customize(args):
                args["html_theme_options"]["sidebar_hide_name"] = True
                return args

            with generate_docs_configuration(adjust_arguments=customize) as config_dir:
                # build docs...

    Note:
        Breathe/Doxygen configuration is loaded from ``[tool.yardang.breathe]``
        with the following options:

        - ``projects``: Dict mapping project names to Doxygen XML directories
        - ``default-project``: Default project for breathe directives
        - ``domain-by-extension``: Map file extensions to Sphinx domains
        - ``show-define-initializer``: Show macro initializer values (default: True)
        - ``show-enumvalue-initializer``: Show enum value initializers (default: True)
        - ``show-include``: Show #include directives (default: True)
        - ``use-project-refids``: Prefix refids with project name (default: True)
    """
    if os.path.exists("conf.py"):
        # yield folder path to sphinx build
        yield os.path.curdir
    else:
        # load configuration
        default_data = os.path.split(os.getcwd())[-1]
        project = project or get_config(section="name", base="project") or default_data.replace("_", "-")
        title = title or get_config(section="title", base=config_base) or default_data.replace("_", "-")
        module = module or get_config(section="module", base=config_base) or project.replace("-", "_") or default_data.replace("-", "_")
        description = description or get_config(section="name", base="description") or default_data.replace("_", " ").replace("-", " ")
        author = author or get_config(section="authors", base="project")
        if isinstance(author, list) and len(author) > 0:
            author = author[0]
        else:
            author = f"The {project} authors"
        if isinstance(author, dict):
            author = author["name"]
        copyright = copyright or author
        theme = theme or get_config(section="theme", base=config_base)
        version = version or get_config(section="version", base="project")
        docs_root = (
            docs_root
            or get_config(section="docs-host", base=config_base)
            or get_config(section="urls.Homepage", base="project")
            or get_config(section="urls.homepage", base="project")
            or get_config(section="urls.Documentation", base="project")
            or get_config(section="urls.documentation", base="project")
            or get_config(section="urls.Source", base="project")
            or get_config(section="urls.source", base="project")
            or ""
        )
        root = root or get_config(section="root", base=config_base)
        cname = cname or get_config(section="cname", base=config_base)
        pages = pages or get_config(section="pages", base=config_base) or []
        use_autoapi = use_autoapi or get_config(section="use-autoapi", base=config_base)
        autoapi_ignore = autoapi_ignore or get_config(section="docs.autoapi-ignore")

        custom_css = custom_css or Path(get_config(section="custom-css", base=config_base) or (Path(__file__).parent / "custom.css"))
        custom_js = custom_js or Path(get_config(section="custom-js", base=config_base) or (Path(__file__).parent / "custom.js"))

        # if custom_css and custom_js are strings and they exist as paths, read them as Paths
        # otherwise, assume the content is directly provided
        if isinstance(custom_css, str):
            custom_css_path = Path(custom_css)
            # if the path is too long, it will throw
            try:
                if custom_css_path.exists():
                    custom_css = custom_css_path.read_text()
            except OSError:
                pass
        else:
            custom_css = custom_css.read_text()
        if isinstance(custom_js, str):
            custom_js_path = Path(custom_js)
            try:
                if custom_js_path.exists():
                    custom_js = custom_js_path.read_text()
            except OSError:
                pass
        else:
            custom_js = custom_js.read_text()

        source_dir = os.path.curdir

        configuration_args = {}
        for config_option, default in {
            # sphinx generic
            "html_theme_options": {},
            "html_static_path": [],
            "html_css_files": [],
            "html_js_files": [],
            "source_suffix": [],
            "exclude_patterns": [],
            "language": "en",
            "pygments_style": "sphinx",
            # myst/myst-nb
            "myst_enable_extensions": [
                "amsmath",
                # "attrs_inline",
                "colon_fence",
                # "deflist",
                "dollarmath",
                # "fieldlist",
                # "html_admonition",
                "html_image",
                # "linkify",
                # "replacements",
                # "smartquotes",
                # "strikethrough",
                # "substitution",
                # "tasklist",
            ],
            "myst_fence_as_directive": [
                "mermaid",
                # breathe/doxygen directives
                "doxygenindex",
                "doxygenfunction",
                "doxygenstruct",
                "doxygenclass",
                "doxygennamespace",
                "doxygengroup",
                "doxygentypedef",
                "doxygenenum",
                "doxygenfile",
                "doxygendefine",
                "doxygenunion",
                "doxygenvariable",
                # sphinx-rust directives
                "rust:crate",
                "rust:module",
                "rust:struct",
                "rust:enum",
                "rust:function",
                "rust:method",
                "rust:trait",
                "rust:impl",
                "rust:type",
                "rust:const",
                "rust:static",
                "rust:macro",
                # common sphinx directives
                "toctree",
                "literalinclude",
                "include",
            ],
            "nb_execution_mode": "off",
            "nb_execution_excludepatterns": [],
            # autodoc/autodoc-pydantic
            "autodoc_pydantic_field_list_validators": None,
            "autodoc_pydantic_field_show_constraints": None,
            "autodoc_pydantic_model_member_order": "bysource",
            "autodoc_pydantic_model_show_config_summary": None,
            "autodoc_pydantic_model_show_field_summary": None,
            "autodoc_pydantic_model_show_json": True,
            "autodoc_pydantic_model_show_validator_summary": None,
            "autodoc_pydantic_model_show_validator_members": None,
            "autodoc_pydantic_settings_show_json": None,
            # sphinx-reredirects
            "redirects": {},
        }.items():
            configuration_args[config_option] = get_config(section=config_option, base=config_base) or default

        # Load breathe/doxygen configuration from tool.yardang.breathe
        breathe_config_base = f"{config_base}.breathe"
        breathe_args = {}
        for config_option, default in {
            # breathe/doxygen
            "breathe_projects": {},
            "breathe_default_project": "",
            "breathe_domain_by_extension": {"h": "cpp", "hpp": "cpp", "cpp": "cpp", "c": "c", "py": "py", "cs": "cs"},
            "breathe_domain_by_file_pattern": {},
            "breathe_projects_source": {},
            "breathe_build_directory": "",
            "breathe_default_members": (),
            "breathe_show_define_initializer": True,
            "breathe_show_enumvalue_initializer": True,
            "breathe_show_include": True,
            "breathe_implementation_filename_extensions": [".c", ".cc", ".cpp"],
            "breathe_doxygen_config_options": {},
            "breathe_doxygen_aliases": {},
            "breathe_use_project_refids": True,
            "breathe_order_parameters_first": False,
            "breathe_separate_member_pages": False,
        }.items():
            # config keys in toml use hyphens, not underscores, and no breathe_ prefix
            toml_key = config_option.replace("breathe_", "").replace("_", "-")
            breathe_args[config_option] = get_config(section=toml_key, base=breathe_config_base)
            if breathe_args[config_option] is None:
                breathe_args[config_option] = default

        # Determine if breathe should be used
        use_breathe = bool(breathe_args["breathe_projects"] or breathe_args["breathe_projects_source"] or breathe_args["breathe_default_project"])

        # Auto-run doxygen if configured and projects exist
        auto_run_doxygen = get_config(section="auto-run-doxygen", base=breathe_config_base)
        if auto_run_doxygen is None:
            auto_run_doxygen = True  # Default to True
        if use_breathe and auto_run_doxygen and breathe_args["breathe_projects"]:
            run_doxygen_if_needed(breathe_args["breathe_projects"])

        # Convert relative paths in breathe_projects to absolute paths
        # This is needed because the conf.py is generated in a temp directory
        if breathe_args["breathe_projects"]:
            breathe_args["breathe_projects"] = {
                name: str(Path(path).resolve()) if not Path(path).is_absolute() else path for name, path in breathe_args["breathe_projects"].items()
            }

        # Load sphinx-rust configuration from tool.yardang.sphinx-rust
        rust_config_base = f"{config_base}.sphinx-rust"
        rust_args = {}
        for config_option, default in {
            # sphinx-rust
            "rust_crates": [],
            "rust_doc_formats": {},
            "rust_viewcode": True,
        }.items():
            # config keys in toml use hyphens, not underscores, and no rust_ prefix
            toml_key = config_option.replace("rust_", "").replace("_", "-")
            rust_args[config_option] = get_config(section=toml_key, base=rust_config_base)
            if rust_args[config_option] is None:
                rust_args[config_option] = default

        # Determine if sphinx-rust should be used
        use_sphinx_rust = bool(rust_args["rust_crates"])

        # Convert relative paths in rust_crates to absolute paths
        if rust_args["rust_crates"]:
            rust_args["rust_crates"] = [str(Path(path).resolve()) if not Path(path).is_absolute() else path for path in rust_args["rust_crates"]]

        # create a temporary directory to store the conf.py file in
        with TemporaryDirectory() as td:
            templateEnv = Environment(loader=FileSystemLoader(searchpath=str(Path(__file__).parent.resolve())))

            args = dict(
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
                autoapi_ignore=autoapi_ignore,
                source_dir=source_dir,
                previous_versions=previous_versions,
                use_breathe=use_breathe,
                use_sphinx_rust=use_sphinx_rust,
                **breathe_args,
                **rust_args,
                **configuration_args,
            )

            # adjust arguments if a callable is provided
            if adjust_arguments:
                args = adjust_arguments(args)

            # load the templatized conf.py file
            template = templateEnv.get_template("conf.py.j2")

            # adjust the template if a callable is provided
            if adjust_template:
                template = adjust_template(template)

            # Render
            template = template.render(**args)

            # dump to file
            template_file = Path(td) / "conf.py"
            template_file.write_text(template)

            # write custom css and customjs
            Path("docs/html/_static/styles").mkdir(parents=True, exist_ok=True)
            Path("docs/html/_static/styles/custom.css").write_text(custom_css)
            Path("docs/html/_static/js").mkdir(parents=True, exist_ok=True)
            Path("docs/html/_static/js/custom.js").write_text(custom_js)

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
