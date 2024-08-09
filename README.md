<a href="https://github.com/python-project-templates/yardang"><img src="https://github.com/python-project-templates/yardang/blob/main/docs/logo.png?raw=true" alt="yardang" width="120"></a>

# yardang

[![Build Status](https://github.com/python-project-templates/yardang/actions/workflows/build.yml/badge.svg?branch=main&event=push)](https://github.com/python-project-templates/yardang/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/python-project-templates/yardang/branch/main/graph/badge.svg)](https://codecov.io/gh/python-project-templates/yardang)
[![License](https://img.shields.io/github/license/python-project-templates/yardang)](https://github.com/python-project-templates/yardang)
[![PyPI](https://img.shields.io/pypi/v/yardang.svg)](https://pypi.python.org/pypi/yardang)

`yardang` is a Python library for generating [Sphinx documentation](https://www.sphinx-doc.org/en/master/) easily, with minimal local configuration overhead.

[`yardang`](https://www.britannica.com/science/yardang) makes building [Sphinx](https://www.sphinx-doc.org/en/master/) easy.

## Configuration

Here is `yardang`'s own configuration, in `pyproject.toml`

```toml
[tool.yardang]
root = "docs/src/home.md"
cname = "yardang.python-templates.dev"
pages = [
    "docs/src/overview.md",
    "docs/src/installation.md",
    "docs/src/configuration.md",
]
use-autoapi = true
```

## Installation
You can install from PyPI via `pip`:

```bash
pip install yardang
```

Or from `conda-forge` via `conda`:

```bash
conda install yardang -c conda-forge
```
