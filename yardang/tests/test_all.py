from yardang.build import generate_docs_configuration
from yardang.cli import build, debug


def test_build():
    with generate_docs_configuration() as _:
        ...


def test_cli():
    build()
    debug()
