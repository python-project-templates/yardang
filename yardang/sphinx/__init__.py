from yardang import __version__


def setup(_app) -> dict[str, object]:
    """Register Yardang as a Sphinx extension."""
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
