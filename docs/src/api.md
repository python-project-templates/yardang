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

### Document Individual Classes

Or document specific classes with `doxygenclass`:

```doxygenclass calc::Calculator
:members:
```

```doxygenclass calc::ScientificCalculator
:members:
```

## Rust Example

This is an example of documenting Rust code using sphinx-rust integration.

### Document a Crate

Use `rust:crate` to document an entire Rust crate:

```rust:crate calculator
```

### Document Individual Items

Or document specific structs, enums, and functions:

```rust:struct calculator::Calculator
```

```rust:struct calculator::ScientificCalculator
```

```rust:enum calculator::Operation
```

```rust:enum calculator::CalculatorError
```

