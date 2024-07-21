from sys import executable
from pathlib import Path
from subprocess import Popen, PIPE
from typer import Typer

from .build import generate_docs_configuration, CUSTOM_CSS


def build(quiet: bool = False, debug: bool = False):
    with generate_docs_configuration() as file:
        folder = Path("docs/html/_static/styles")
        css = folder / "custom.css"
        if not css.exists():
            folder.mkdir(parents=True, exist_ok=True)
            css.write_text(CUSTOM_CSS)

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

        process = Popen(build_cmd, stdout=PIPE)
        while process.poll() is None:
            text = process.stdout.readline().decode("utf-8")
            if text and not quiet:
                print(text)
        text = process.stdout.readline().decode("utf-8")
        if text and not quiet:
            print(text)


def debug():
    build(quiet=False, debug=True)


def main():
    app = Typer()
    app.command("build")(build)
    app.command("debug")(debug)
    app()


if __name__ == "__main__":
    main()
