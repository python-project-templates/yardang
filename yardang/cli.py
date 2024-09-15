from subprocess import Popen
from sys import executable, stderr, stdout
from time import sleep

from typer import Exit, Typer

from .build import generate_docs_configuration


def build(quiet: bool = False, debug: bool = False):
    with generate_docs_configuration() as file:
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
