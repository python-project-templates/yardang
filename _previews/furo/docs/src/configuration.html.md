<a id="configuration"></a>

# Configuration

Configuration for `yardang` is driven from the `pyproject.toml`, either via standard sections like `project` or from the dedicated `tool.yardang` section. Each option below corresponds to the [Sphinx configuration](https://www.sphinx-doc.org/en/master/usage/configuration.html).

Here is `yardang`’s own configuration, in `pyproject.toml`

```toml
[tool.yardang] root = "docs/src/home.md" cname = "yardang.python-templates.dev" pages = [     "docs/src/overview.md",     "docs/src/installation.md",     "docs/src/configuration.md", ] use-autoapi = true 
```

<a id="name"></a>

## [`name`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-project)

The project name is taken from the standard section, or from the `cwd`.

```toml
[project] name = "your project name" 
```

<a id="title"></a>

## `title`

Same as `name`

<a id="module"></a>

## `module`

The module title is taken from the `name`, replacing `-` with `_`, or from the `cwd` doing the same.

<a id="description"></a>

## `description`

```toml
[project] description = "your project description" 
```

<a id="author"></a>

## [`author`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-author)

```toml
[project] authors = "your project authors" 
```

<a id="version"></a>

## [`version`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-version)

```toml
[project] version = "0.1.0" 
```

<a id="theme"></a>

## [`theme`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme)

The Sphinx HTML theme to build with. Defaults to `furo`.

```toml
[tool.yardang] theme = "furo" 
```

`yardang` ships per-theme defaults (sensible CSS tweaks, and an optional dependency) for the following themes:

- [`furo`](https://github.com/pradyunsg/furo) (the default, always installed)
- [`sphinxawesome_theme`](https://sphinxawesome.xyz/)
- [`shibuya`](https://shibuya.lepture.com/)

`furo` is always available; install the rest with `pip install yardang[themes]`. Any other installed Sphinx theme works too — you just won’t get the bundled defaults. See [Previewing themes]() below to compare them live.

<a id="custom-css-custom-js"></a>

## `custom-css` / `custom-js`

Inject a custom stylesheet or script. The value may be a path or raw content. When unset, `yardang` looks for a bundled per-theme asset named `{theme}.css` / `{theme}.js`, then falls back to the generic `custom.css` / `custom.js`. This lets each theme ship sensible defaults — for example, `sphinxawesome_theme` and `shibuya` hide the duplicate copy button.

```toml
[tool.yardang] custom-css = "docs/_static/my.css" 
```

<a id="previewing-themes"></a>

## Previewing themes

Build the docs once per theme to compare them side-by-side:

```bash
yardang preview 
```

This renders the documentation into `docs/html/_previews/<theme>/` for each bundled theme (`furo`, `sphinxawesome_theme`, `shibuya`). Themes whose package is not installed are skipped. Restrict the set with `--themes`:

```bash
yardang preview --themes furo --themes shibuya 
```

Install the optional themes with:

```bash
pip install yardang[themes] 
```

When this runs in CI before the GitHub Pages deploy (as in `yardang`’s own [`docs.yaml`](https://github.com/python-project-templates/yardang/blob/main/.github/workflows/docs.yaml)), each theme is browsable live at a suburl of the published site:

- [`/_previews/furo/`](https://yardang.python-templates.dev/_previews/furo/)
- [`/_previews/sphinxawesome_theme/`](https://yardang.python-templates.dev/_previews/sphinxawesome_theme/)
- [`/_previews/shibuya/`](https://yardang.python-templates.dev/_previews/shibuya/)

<a id="root"></a>

## `root`

The root page to use, defaults to `README.md`.

```toml
[tool.yardang] root = "docs/src/index.md" 
```

<a id="cname"></a>

## `cname`

If set, will generate a `CNAME` file for GitHub Pages custom domains.

```toml
[tool.yardang] cname = "yardang.python-templates.dev" 
```

<a id="pages"></a>

## `pages`

Pages to include in the contents tree.

```toml
[tool.yardang] pages = [     "docs/src/overview.md",     "docs/src/installation.md",     "docs/src/configuration.md", ] 
```

<a id="use-autoapi"></a>

## `use_autoapi`

Whether or not to use [Sphinx AutoAPI](https://sphinx-autoapi.readthedocs.io/en/latest/). **NOTE:** it is recommended to manually autodoc your code.

```toml
[tool.yardang] use-autoapi = true 
```

<a id="sphinx-options"></a>

## Sphinx Options

```toml
[tool.yardang] html_theme_options = {} html_static_path = [] html_css_files = [] html_js_files = [] source_suffix = [] exclude_patterns = [] language = "en" pygments_style = "sphinx" 
```

<a id="myst"></a>

## [Myst](https://myst-parser.readthedocs.io/en/latest/#)

```toml
[tool.yardang] myst_enable_extensions = ["amsmath", "colon_fence", "dollarmath", "html_image"] myst_fence_as_directive = ["mermaid"] 
```

<a id="myst-nb"></a>

## [Myst-NB](https://myst-nb.readthedocs.io/en/latest/#)

```toml
[tool.yardang] nb_execution_mode = "off" nb_execution_excludepatterns = [] 
```

Notebooks can be included with:

```raw
```{eval-rst} .. toctree::   :maxdepth: 1    ../notebooks/example ``` 
```

An example follows:

- [Example Notebook](../notebooks/example.md)

<a id="autodoc-pydantic-arguments"></a>

## [Autodoc Pydantic](https://autodoc-pydantic.readthedocs.io/en/stable/users/examples.html) arguments

[Configuration for Autodoc Pydantic](https://autodoc-pydantic.readthedocs.io/en/stable/users/configuration.html).

```toml
[tool.yardang] autodoc_pydantic_model_show_config_summary = false autodoc_pydantic_model_show_validator_summary = false autodoc_pydantic_model_show_validator_members = false autodoc_pydantic_field_list_validators = false autodoc_pydantic_field_show_constraints = false autodoc_pydantic_model_member_order = "bysource" autodoc_pydantic_model_show_json = true autodoc_pydantic_settings_show_json = false autodoc_pydantic_model_show_field_summary = false 
```

<a id="mermaid"></a>

## Mermaid

<a id="github-admonitions"></a>

## GitHub Admonitions

GitHub admonitions are automatically translated to sphinx.

#### NOTE
Note `markdown` content

#### IMPORTANT
Important content

#### WARNING
Warning content

<a id="breathe-doxygen-integration"></a>

## Breathe/Doxygen Integration

Yardang provides integration with [Breathe](https://breathe.readthedocs.io/) for documenting C/C++ code using Doxygen. To use this feature, install yardang with the breathe extra:

```bash
pip install yardang[breathe] 
```

All breathe configuration is under `[tool.yardang.breathe]`.

<a id="projects"></a>

### `projects`

A dictionary mapping project names to their Doxygen XML output directories.

```toml
[tool.yardang.breathe] projects = { myproject = "docs/doxygen/xml", another = "path/to/xml" } 
```

<a id="default-project"></a>

### `default-project`

The default project to use when no project is specified in breathe directives.

```toml
[tool.yardang.breathe] default-project = "myproject" 
```

<a id="domain-by-extension"></a>

### `domain-by-extension`

Map file extensions to Sphinx domains.

```toml
[tool.yardang.breathe] domain-by-extension = { "hpp" = "cpp", "h" = "cpp", "py" = "py" } 
```

<a id="domain-by-file-pattern"></a>

### `domain-by-file-pattern`

Map file patterns to Sphinx domains.

```toml
[tool.yardang.breathe] domain-by-file-pattern = { "*.hpp" = "cpp" } 
```

<a id="projects-source"></a>

### `projects-source`

Configure source files for automatic Doxygen XML generation.

```toml
[tool.yardang.breathe] projects-source = { auto = ["src", ["file1.hpp", "file2.hpp"]] } 
```

<a id="build-directory"></a>

### `build-directory`

The directory where Doxygen XML is built.

```toml
[tool.yardang.breathe] build-directory = "build/doxygen" 
```

<a id="default-members"></a>

### `default-members`

Default member visibility for doxygenclass directives.

```toml
[tool.yardang.breathe] default-members = ["members", "protected-members", "private-members"] 
```

<a id="show-define-initializer"></a>

### `show-define-initializer`

Show the initializer value for #define macros.

```toml
[tool.yardang.breathe] show-define-initializer = true 
```

<a id="show-enumvalue-initializer"></a>

### `show-enumvalue-initializer`

Show the initializer value for enum values.

```toml
[tool.yardang.breathe] show-enumvalue-initializer = true 
```

<a id="show-include"></a>

### `show-include`

Show the #include directive for documented entities.

```toml
[tool.yardang.breathe] show-include = true 
```

<a id="implementation-filename-extensions"></a>

### `implementation-filename-extensions`

List of file extensions considered as implementation files.

```toml
[tool.yardang.breathe] implementation-filename-extensions = [".c", ".cc", ".cpp"] 
```

<a id="doxygen-config-options"></a>

### `doxygen-config-options`

Additional Doxygen configuration options for auto-generated XML.

```toml
[tool.yardang.breathe] doxygen-config-options = { EXTRACT_ALL = "YES", QUIET = "YES" } 
```

<a id="doxygen-aliases"></a>

### `doxygen-aliases`

Doxygen aliases for custom commands.

```toml
[tool.yardang.breathe] doxygen-aliases = { "myalias" = "Custom documentation text" } 
```

<a id="use-project-refids"></a>

### `use-project-refids`

Use project-qualified reference IDs to avoid conflicts.

```toml
[tool.yardang.breathe] use-project-refids = true 
```

<a id="order-parameters-first"></a>

### `order-parameters-first`

Order function parameters before other members in documentation.

```toml
[tool.yardang.breathe] order-parameters-first = true 
```

<a id="separate-member-pages"></a>

### `separate-member-pages`

Generate separate pages for each class member.

```toml
[tool.yardang.breathe] separate-member-pages = false 
```

<a id="complete-example"></a>

### Complete Example

Here’s a complete example configuration for a C++ project:

```toml
[tool.yardang] title = "My C++ Library" root = "docs/index.md" pages = ["docs/api.md", "docs/examples.md"] use-autoapi = false  [tool.yardang.breathe] projects = { mylib = "docs/doxygen/xml" } default-project = "mylib" domain-by-extension = { "hpp" = "cpp", "cpp" = "cpp", "h" = "cpp" } show-define-initializer = true show-enumvalue-initializer = true show-include = true use-project-refids = true 
```

Then in your documentation files, you can use breathe directives:

```markdown
# API Reference  ## MyClass  \`\`\`{doxygenclass} MyNamespace::MyClass :members: :protected-members: \`\`\`  ## Functions  \`\`\`{doxygenfunction} MyNamespace::myFunction \`\`\` 
```

<a id="sphinx-rust-integration"></a>

## Sphinx-Rust Integration

Yardang provides integration with [sphinx-rust](https://sphinx-rust.readthedocs.io/) for documenting Rust code. To use this feature, install yardang with the sphinx-rust extra:

```bash
pip install yardang[sphinx-rust] 
```

All sphinx-rust configuration is under `[tool.yardang.sphinx-rust]`.

<a id="crates"></a>

### `crates`

A list of paths to Rust crates to document.

```toml
[tool.yardang.sphinx-rust] crates = [     "path/to/crate1",     "path/to/crate2", ] 
```

<a id="doc-formats"></a>

### `doc-formats`

A dictionary mapping crate names to their docstring format. Valid values are `"restructuredtext"` (default) or `"myst-nb"` (for markdown docstrings).

```toml
[tool.yardang.sphinx-rust] doc-formats = { mycrate = "myst-nb" } 
```

**Note:** When using `myst_nb` as your Sphinx parser (which yardang uses by default), use `"myst-nb"` instead of `"markdown"` for markdown docstrings.

<a id="viewcode"></a>

### `viewcode`

Enable links to the source code for documented items. Defaults to `true`.

```toml
[tool.yardang.sphinx-rust] viewcode = true 
```

<a id="id1"></a>

### Complete Example

Here’s a complete example configuration for a Rust project:

```toml
[tool.yardang] title = "My Rust Library" root = "docs/index.md" pages = ["docs/api.md", "docs/examples.md"] use-autoapi = false  [tool.yardang.sphinx-rust] crates = [     "crates/mylib",     "crates/mylib-utils", ] doc-formats = { mylib = "myst-nb", "mylib-utils" = "restructuredtext" } viewcode = true 
```

Then in your documentation files, you can use sphinx-rust directives:

```markdown
# API Reference  ## Document a Crate  \`\`\`{eval-rst} .. rust:crate:: mylib  \`\`\`  ## Document Individual Items  \`\`\`{eval-rst} .. rust:struct:: mylib::MyStruct  \`\`\`  \`\`\`{eval-rst} .. rust:enum:: mylib::MyEnum  \`\`\`  \`\`\`{eval-rst} .. rust:function:: mylib::my_function  \`\`\` 
```

<a id="sphinx-js-integration"></a>

## Sphinx-JS Integration

Yardang provides integration with [sphinx-js](https://pypi.org/project/sphinx-js/) for documenting JavaScript and TypeScript code. To use this feature, you also need JSDoc or TypeDoc installed:

```bash
# For JavaScript projects npm install jsdoc  # For TypeScript projects npm install typedoc 
```

All sphinx-js configuration is under `[tool.yardang.sphinx-js]`.

<a id="js-source-path"></a>

### `js-source-path`

A list of directories containing your JS/TS source files, relative to the project root. This is required to enable sphinx-js.

```toml
[tool.yardang.sphinx-js] js-source-path = ["src", "lib"] 
```

Or as a single path:

```toml
[tool.yardang.sphinx-js] js-source-path = "src" 
```

<a id="js-language"></a>

### `js-language`

The language of your source files. Use `"javascript"` (default) or `"typescript"`.

```toml
[tool.yardang.sphinx-js] js-language = "typescript" 
```

<a id="root-for-relative-js-paths"></a>

### `root-for-relative-js-paths`

The root directory for resolving relative JS entity paths. Required if you have multiple `js-source-path` entries.

```toml
[tool.yardang.sphinx-js] root-for-relative-js-paths = "src" 
```

<a id="jsdoc-config-path"></a>

### `jsdoc-config-path`

Path to a JSDoc configuration file.

```toml
[tool.yardang.sphinx-js] jsdoc-config-path = "jsdoc.json" 
```

<a id="jsdoc-tsconfig-path"></a>

### `jsdoc-tsconfig-path`

Path to a TypeScript configuration file (for TypeDoc).

```toml
[tool.yardang.sphinx-js] jsdoc-tsconfig-path = "tsconfig.json" 
```

<a id="ts-type-bold"></a>

### `ts-type-bold`

Make TypeScript types bold in the output. Defaults to `false`.

```toml
[tool.yardang.sphinx-js] ts-type-bold = true 
```

<a id="id2"></a>

### Complete Example

Here’s a complete example configuration for a TypeScript project:

```toml
[tool.yardang] title = "My TypeScript Library" root = "docs/index.md" pages = ["docs/api.md", "docs/examples.md"] use-autoapi = false  [tool.yardang.sphinx-js] js-language = "typescript" js-source-path = ["src"] jsdoc-tsconfig-path = "tsconfig.json" ts-type-bold = true 
```

Then in your documentation files, you can use sphinx-js directives:

```markdown
# API Reference  ## Functions  \`\`\`{js:autofunction} myFunction \`\`\`  ## Classes  \`\`\`{js:autoclass} MyClass :members: \`\`\`  ## Modules  \`\`\`{js:automodule} myModule \`\`\` 
```

<a id="github-wiki-integration"></a>

## GitHub Wiki Integration

Yardang can generate GitHub Wiki compatible markdown documentation using [sphinx-markdown-builder](https://github.com/liran-funaro/sphinx-markdown-builder). This allows you to publish your documentation to a GitHub Wiki in addition to (or instead of) a static HTML site.

To generate wiki output, use the `yardang wiki` command instead of `yardang build`.

Wiki output is configured in the `[tool.yardang.wiki]` section:

```toml
[tool.yardang.wiki] enabled = true output-dir = "docs/wiki" generate-sidebar = true generate-footer = true fix-links = true footer-docs-url = "https://your-project.dev" footer-repo-url = "https://github.com/your-org/your-project" markdown-flavor = "github" 
```

<a id="enabled"></a>

### `enabled`

Enable the markdown builder extension. Must be `true` to use `yardang wiki`. Defaults to `false`.

```toml
[tool.yardang.wiki] enabled = true 
```

<a id="output-dir"></a>

### `output-dir`

Output directory for the generated markdown files. Defaults to `"docs/wiki"`.

```toml
[tool.yardang.wiki] output-dir = "docs/wiki" 
```

<a id="generate-sidebar"></a>

### `generate-sidebar`

Generate a `_Sidebar.md` file for wiki navigation. Defaults to `true`.

```toml
[tool.yardang.wiki] generate-sidebar = true 
```

<a id="generate-footer"></a>

### `generate-footer`

Generate a `_Footer.md` file with links to docs and repo. Defaults to `true`.

```toml
[tool.yardang.wiki] generate-footer = true 
```

<a id="fix-links"></a>

### `fix-links`

Fix internal markdown links for GitHub Wiki compatibility. Defaults to `true`.

```toml
[tool.yardang.wiki] fix-links = true 
```

<a id="footer-docs-url"></a>

### `footer-docs-url`

URL to the full documentation site (for the footer).

```toml
[tool.yardang.wiki] footer-docs-url = "https://your-project.dev" 
```

<a id="footer-repo-url"></a>

### `footer-repo-url`

URL to the repository (for the footer).

```toml
[tool.yardang.wiki] footer-repo-url = "https://github.com/your-org/your-project" 
```

<a id="markdown-flavor"></a>

### `markdown-flavor`

Markdown flavor to use. Set to `"github"` for GitHub-flavored markdown. Defaults to `"github"`.

```toml
[tool.yardang.wiki] markdown-flavor = "github" 
```

<a id="markdown-anchor-sections"></a>

### `markdown-anchor-sections`

Add anchors before each section. Defaults to `true`.

```toml
[tool.yardang.wiki] markdown-anchor-sections = true 
```

<a id="markdown-anchor-signatures"></a>

### `markdown-anchor-signatures`

Add anchors before each function/class signature. Defaults to `true`.

```toml
[tool.yardang.wiki] markdown-anchor-signatures = true 
```

<a id="markdown-bullet"></a>

### `markdown-bullet`

Bullet character to use for lists. Defaults to `"-"`.

```toml
[tool.yardang.wiki] markdown-bullet = "-" 
```

<a id="id3"></a>

### Complete Example

```toml
[tool.yardang] title = "My Project" root = "docs/index.md" pages = ["docs/overview.md", "docs/api.md"]  [tool.yardang.wiki] enabled = true output-dir = "docs/wiki" generate-sidebar = true generate-footer = true footer-docs-url = "https://myproject.dev" footer-repo-url = "https://github.com/myorg/myproject" markdown-flavor = "github" 
```

<a id="usage"></a>

### Usage

Generate GitHub Wiki output:

```bash
yardang wiki 
```

The output will be in the `docs/wiki/` directory (or the configured output directory). To publish to your GitHub Wiki:

```bash
# Clone your wiki repository git clone https://github.com/YOUR-ORG/YOUR-REPO.wiki.git  # Copy the generated markdown files cp -r docs/wiki/* YOUR-REPO.wiki/  # Commit and push cd YOUR-REPO.wiki git add . git commit -m "Update wiki documentation" git push 
```

The generated wiki includes:

- `Home.md` - The main landing page (converted from index.md)
- `_Sidebar.md` - Navigation sidebar with links to all pages
- `_Footer.md` - Footer with links to documentation and repository
- All documentation pages converted to GitHub-flavored markdown
