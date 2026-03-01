# Calculator Library (Rust)

A simple calculator library demonstrating Rust documentation with sphinx-rust.

## Features

- Basic arithmetic operations (add, subtract, multiply, divide)
- Scientific calculator with trigonometric and logarithmic functions
- Operation history tracking
- Full Rust documentation with examples

## Usage

```rust
use calculator::{Calculator, Operation};

fn main() {
    let mut calc = Calculator::new();
    
    // Basic operations
    let sum = calc.add(5.0, 3.0);
    println!("5 + 3 = {}", sum);
    
    let product = calc.multiply(4.0, 7.0);
    println!("4 * 7 = {}", product);
    
    // View history
    for result in calc.history() {
        println!("{}", result);
    }
}
```

## Scientific Calculator

```rust
use calculator::ScientificCalculator;

fn main() {
    let mut sci = ScientificCalculator::new();
    sci.set_use_degrees(true);
    
    println!("sin(90°) = {}", sci.sin(90.0));
    println!("sqrt(16) = {}", sci.sqrt(16.0));
    println!("2^10 = {}", sci.pow(2.0, 10.0));
}
```
