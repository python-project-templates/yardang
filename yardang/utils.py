import os
from pathlib import Path

import toml

__all__ = ("get_config",)


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
