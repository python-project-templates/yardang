from pathlib import Path
from subprocess import Popen
from sys import executable, stderr, stdout
from time import sleep
from typing import List, Optional

from typer import Exit, Typer

from .build import generate_docs_configuration


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


def main():
    app = Typer()
    app.command("build")(build)
    app.command("debug")(debug)
    app()


if __name__ == "__main__":
    main()
