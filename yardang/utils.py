import os
from pathlib import Path

import toml

__all__ = ("get_config", "get_config_flex")


def get_pyproject_toml():
    cwd = os.getcwd()
    local_path = Path(cwd) / "pyproject.toml"
    if local_path.exists():
        return toml.loads(local_path.read_text())
    raise FileNotFoundError(str(local_path))


def get_config(section="", base="tool.yardang"):
    config = get_pyproject_toml()
    sections = base.split(".") + (section.split(".") if section else [])
    for s in sections:
        config = config.get(s, None)
        if config is None:
            return None
    return config


def get_config_flex(section="", base="tool.yardang"):
    """Look up a config key, accepting both hyphens and underscores.

    Tries the hyphenated form first (TOML convention), then the
    underscored form (Sphinx convention). For example, looking up
    ``html_extra_path`` will try ``html-extra-path`` first, then
    ``html_extra_path``.
    """
    hyphen_key = section.replace("_", "-")
    underscore_key = section.replace("-", "_")

    # Prefer hyphens (TOML convention)
    result = get_config(section=hyphen_key, base=base)
    if result is not None:
        return result

    # Fall back to underscores (Sphinx convention)
    if underscore_key != hyphen_key:
        return get_config(section=underscore_key, base=base)

    return None
