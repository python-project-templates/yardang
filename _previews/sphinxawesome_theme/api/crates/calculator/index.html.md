<a id="crate-calculator"></a>

# Crate `calculator`

Version: 0.1.0

<a id="calculator"></a>

### pub mod calculator;[[source]](code/calculator.md#rust-code-calculator)

<a id="calculator-library"></a>

## Calculator Library

A simple calculator library demonstrating Rust documentation with sphinx-rust.

This crate provides basic arithmetic operations and a calculator struct that maintains a history of operations.

<a id="example"></a>

### Example

```rust
use calculator::{Calculator, Operation};  let mut calc = Calculator::new(); let result = calc.calculate(5.0, 3.0, Operation::Add); assert_eq!(result, 8.0); 
```

<a id="id1"></a>

## Structs

| [`Calculator`](structs/calculator::Calculator.md#calculator-Calculator)                               | A calculator that performs basic arithmetic operations.         |
|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| [`ScientificCalculator`](structs/calculator::ScientificCalculator.md#calculator-ScientificCalculator) | A scientific calculator with additional mathematical functions. |

<a id="id2"></a>

## Enums

| [`CalculatorError`](enums/calculator::CalculatorError.md#calculator-CalculatorError)   | Errors that can occur during calculator operations.   |
|----------------------------------------------------------------------------------------|-------------------------------------------------------|
