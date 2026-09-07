# API Reference

## Python API

### yardang.build

```{eval-rst}
.. automodule:: yardang.build
   :members:
   :undoc-members:
   :show-inheritance:
```

### yardang.cli

```{eval-rst}
.. automodule:: yardang.cli
   :members:
   :undoc-members:
   :show-inheritance:
```

### yardang.utils

```{eval-rst}
.. automodule:: yardang.utils
   :members:
   :undoc-members:
   :show-inheritance:
```

## C++ Example

This is an example of documenting C++ code using breathe integration.

### Document Everything

Use `doxygenindex` to document all symbols from Doxygen XML:

```doxygenindex
```

```{toctree}
:hidden:
:maxdepth: 2

/examples/cpp/docs/api
```

### Document Individual Classes

Or document specific classes with `doxygenclass`:

```doxygenclass calc::Calculator
:members:
```

```doxygenclass calc::ScientificCalculator
:members:
```

## Rust Example

This is an example of documenting Rust code using sphinxcontrib-rust integration.

Unlike the C++ and JavaScript examples below, the Rust pages are not written by
hand. `sphinx-rustdocgen` reads each crate listed under
`[tool.yardang.sphinx-rust]` and writes a page per module into the configured
`doc-dir`, so the only thing to author is a toctree pointing at the result:

```{toctree}
:hidden:
:maxdepth: 2

/api/calculator/lib
```

## JavaScript Example

This is an example of documenting JavaScript code using sphinx-js integration.

### Document Functions

Use `js:autofunction` to document individual functions:

```{eval-rst}
.. js:autofunction:: add

```

```{eval-rst}
.. js:autofunction:: subtract

```

```{eval-rst}
.. js:autofunction:: multiply

```

```{eval-rst}
.. js:autofunction:: divide

```

### Document Classes

Use `js:autoclass` to document classes:

```{eval-rst}
.. js:autoclass:: Calculator
   :members:

```

```{eval-rst}
.. js:autoclass:: ScientificCalculator
   :members:

```

