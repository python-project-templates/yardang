from importlib.util import find_spec
from pathlib import Path
from subprocess import Popen
from sys import executable, stderr, stdout
from time import sleep
from typing import List, Optional

from typer import Exit, Typer

from .build import BUNDLED_THEMES, generate_docs_configuration, generate_wiki_configuration
from .utils import get_config
from .wiki import process_wiki_output


def build(
    *,
    quiet: bool = False,
    debug: bool = False,
    pdb: bool = False,
    project: Optional[str] = None,
    title: Optional[str] = None,
    module: Optional[str] = None,
    description: Optional[str] = None,
    author: Optional[str] = None,
    copyright: Optional[str] = None,
    version: Optional[str] = None,
    theme: Optional[str] = None,
    docs_root: Optional[str] = None,
    root: Optional[str] = None,
    cname: Optional[str] = None,
    pages: Optional[List[Path]] = None,
    use_autoapi: Optional[bool] = None,
    custom_css: Optional[Path] = None,
    custom_js: Optional[Path] = None,
    output: str = "docs/html",
    config_base: Optional[str] = "tool.yardang",
    previous_versions: Optional[bool] = False,
):
    with generate_docs_configuration(
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
        custom_css=custom_css,
        custom_js=custom_js,
        html_output_dir=output,
        config_base=config_base,
        previous_versions=previous_versions,
    ) as file:
        build_cmd = [
            executable,
            "-m",
            "sphinx",
            ".",
            output,
            "-c",
            file,
        ]

        if debug:
            print(" ".join(build_cmd))
        if quiet:
            process = Popen(build_cmd)
        else:
            process = Popen(build_cmd, stderr=stderr, stdout=stdout)
        while process.poll() is None:
            sleep(0.1)
        if process.returncode != 0:
            if pdb:
                import pdb

                pdb.set_trace()
            raise Exit(process.returncode)


def debug():
    build(quiet=False, debug=True)


def wiki(
    *,
    quiet: bool = False,
    debug: bool = False,
    pdb: bool = False,
    project: Optional[str] = None,
    title: Optional[str] = None,
    module: Optional[str] = None,
    description: Optional[str] = None,
    author: Optional[str] = None,
    copyright: Optional[str] = None,
    version: Optional[str] = None,
    theme: Optional[str] = None,
    docs_root: Optional[str] = None,
    root: Optional[str] = None,
    cname: Optional[str] = None,
    pages: Optional[List[Path]] = None,
    use_autoapi: Optional[bool] = None,
    custom_css: Optional[Path] = None,
    custom_js: Optional[Path] = None,
    config_base: Optional[str] = "tool.yardang",
    previous_versions: Optional[bool] = False,
    output_dir: Optional[str] = None,
    skip_postprocess: bool = False,
):
    """Generate GitHub Wiki compatible markdown documentation.

    Builds markdown output using sphinx-markdown-builder and post-processes
    it to be compatible with GitHub Wiki format, including:
    - Flattening directory structure
    - Renaming index.md to Home.md
    - Generating _Sidebar.md navigation
    - Generating _Footer.md
    - Fixing internal links
    """
    # Get project name for wiki sidebar
    project_name = project or get_config(section="name", base="project") or Path.cwd().name

    # Get pages from config if not provided
    pages_list = pages or get_config(section="pages", base=config_base) or []
    if isinstance(pages_list, list):
        pages_list = [str(p) for p in pages_list]

    with generate_wiki_configuration(
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
        custom_css=custom_css,
        custom_js=custom_js,
        config_base=config_base,
        previous_versions=previous_versions,
    ) as (config_dir, wiki_args):
        # Determine output directory
        wiki_output_dir = output_dir or wiki_args.get("wiki_output_dir", "docs/wiki")

        # Build markdown using sphinx-markdown-builder
        build_cmd = [
            executable,
            "-m",
            "sphinx",
            "-b",
            "markdown",
            ".",
            wiki_output_dir,
            "-c",
            config_dir,
        ]

        if debug:
            print(" ".join(build_cmd))
        if quiet:
            process = Popen(build_cmd)
        else:
            process = Popen(build_cmd, stderr=stderr, stdout=stdout)
        while process.poll() is None:
            sleep(0.1)
        if process.returncode != 0:
            if pdb:
                import pdb

                pdb.set_trace()
            raise Exit(process.returncode)

        # Post-process for GitHub Wiki compatibility
        if not skip_postprocess:
            if not quiet:
                print("\nPost-processing markdown for GitHub Wiki...")

            process_wiki_output(
                output_dir=Path(wiki_output_dir),
                pages=pages_list,
                project_name=project_name,
                docs_url=wiki_args.get("wiki_footer_docs_url", ""),
                repo_url=wiki_args.get("wiki_footer_repo_url", ""),
                generate_sidebar_file=wiki_args.get("wiki_generate_sidebar", True),
                generate_footer_file=wiki_args.get("wiki_generate_footer", True),
                fix_links=wiki_args.get("wiki_fix_links", True),
            )

            if not quiet:
                print(f"GitHub Wiki output generated in: {wiki_output_dir}")
                print("\nTo use with GitHub Wiki:")
                print("  1. Clone your wiki: git clone https://github.com/YOUR/REPO.wiki.git")
                print(f"  2. Copy contents of {wiki_output_dir}/ to the wiki repo")
                print("  3. Commit and push to publish")


def preview(
    *,
    themes: Optional[List[str]] = None,
    output: str = "docs/html/_previews",
    quiet: bool = False,
    debug: bool = False,
    pdb: bool = False,
):
    """Build the documentation once per theme for side-by-side comparison.

    For each theme in ``themes`` (defaulting to the themes yardang bundles
    defaults for), the docs are rendered into ``<output>/<theme>``. Themes whose
    Sphinx package is not installed are skipped with a warning.
    """
    themes = themes or list(BUNDLED_THEMES)
    built = []
    failed = []
    for theme in themes:
        if find_spec(theme) is None:
            print(f"Skipping theme '{theme}': install it to include it in previews", file=stderr)
            continue
        theme_output = str(Path(output) / theme)
        if not quiet:
            print(f"Building preview for theme '{theme}' -> {theme_output}")
        try:
            build(theme=theme, output=theme_output, quiet=quiet, debug=debug, pdb=pdb)
        except Exit as exc:
            failed.append(theme)
            print(f"Failed to build preview for theme '{theme}' (exit {exc.exit_code})", file=stderr)
            continue
        built.append((theme, theme_output))
    if built:
        print("\nTheme previews generated:")
        for theme, theme_output in built:
            print(f"  {theme}: {theme_output}/index.html")
    if failed:
        raise Exit(1)


def main():
    app = Typer()
    app.command("build")(build)
    app.command("debug")(debug)
    app.command("preview")(preview)
    app.command("wiki")(wiki)
    app()


if __name__ == "__main__":
    main()
