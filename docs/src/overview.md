# Overview

`yardang` is a tool to configure the most common [Sphinx](https://www.sphinx-doc.org/en/master/) options directly from a `pyproject.toml`.
Sphinx relies on a `conf.py` file and Makefiles, but these usually overlap a substantial amount with information already stored in the repository (e.g. in the `pyproject.toml`).
Within an organization, these files tend to include a substantial amount of overlapping information.

## Integrations

`yardang` takes the most important parts, like theme, title, pages, etc, and extracts them directly from the `pyproject.toml`.
It creates a temporary file for the `conf.py`, and builds the project into `docs/html`.
Out of the box, it comes with support for several popular Sphinx frameworks:

- [Sphinx Design](https://sphinx-design.readthedocs.io/en/latest/)
- [Myst Markdown](https://jupyterbook.org/en/stable/content/myst.html)
- [Sphinx AutoAPI](https://sphinx-autoapi.readthedocs.io/en/latest/)
- [Autodoc Pydantic](https://autodoc-pydantic.readthedocs.io/en/stable/users/examples.html)
- [Furo Theme](https://github.com/pradyunsg/furo)

## Usage

`yardang` builds Sphinx via a CLI, which will build docs into `docs/html`:

```bash
yardang build
```

### GitHub Pages

The goal of this project is to make it as easy as possible to use Sphinx.
The following yaml should be all it takes to integrate your project with GitHub Pages, **without changing anything in your existing repository**.

```yaml
name: Docs
on:
  push:
    branches:
      - main
permissions:
  contents: write
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - run: pip install .
      - run: pip install yardang
      - run: yardang build
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          publish_branch: gh-pages
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docs/html
```
