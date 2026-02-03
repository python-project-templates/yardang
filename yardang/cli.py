from pathlib import Path
from subprocess import Popen
from sys import executable, stderr, stdout
from time import sleep
from typing import List, Optional

from typer import Exit, Typer

from .build import generate_docs_configuration, generate_wiki_configuration
from .utils import get_config
from .wiki import process_wiki_output


def build(
    *,
    quiet: bool = False,
    debug: bool = False,
    pdb: bool = False,
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
    pages: Optional[List[Path]] = None,
    use_autoapi: Optional[bool] = None,
    custom_css: Optional[Path] = None,
    custom_js: Optional[Path] = None,
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
        config_base=config_base,
        previous_versions=previous_versions,
    ) as file:
        build_cmd = [
            executable,
            "-m",
            "sphinx",
            ".",
            "docs/html",
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


def main():
    app = Typer()
    app.command("build")(build)
    app.command("debug")(debug)
    app.command("wiki")(wiki)
    app()


if __name__ == "__main__":
    main()
