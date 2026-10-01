<a id="crate-calculator"></a>

# Crate `calculator`

<a id="calculator"></a>

### crate calculator

### Calculator Library

A simple calculator library demonstrating Rust documentation with sphinx-rust.

This crate provides basic arithmetic operations and a calculator struct that maintains a history of operations.

### Example

```rust
use calculator::{Calculator, Operation};

let mut calc = Calculator::new();
let result = calc.calculate(5.0, 3.0, Operation::Add);
assert_eq!(result, 8.0);
```

### Enums

<a id="calculator-CalculatorError"></a>

### enum CalculatorError

Errors that can occur during calculator operations.

<a id="calculator-CalculatorError-DivisionByZero"></a>

### DivisionByZero

Attempted to divide by zero.

<a id="calculator-CalculatorError-Overflow"></a>

### Overflow

The result overflowed.

### Traits implemented

<a id="calculator-CalculatorError-Display"></a>

### impl std::fmt::Display for [CalculatorError](#calculator-CalculatorError)

<a id="calculator-CalculatorError-Error"></a>

### impl std::error::Error for [CalculatorError](#calculator-CalculatorError)

<a id="calculator-Operation"></a>

### enum Operation

Enumeration of supported arithmetic operations.

<a id="calculator-Operation-Add"></a>

### Add

Addition operation (+)

<a id="calculator-Operation-Subtract"></a>

### Subtract

Subtraction operation (-)

<a id="calculator-Operation-Multiply"></a>

### Multiply

Multiplication operation (\*)

<a id="calculator-Operation-Divide"></a>

### Divide

Division operation (/)

### Traits implemented

<a id="calculator-Operation-Display"></a>

### impl std::fmt::Display for [Operation](#calculator-Operation)

### Structs and Unions

<a id="calculator-Calculator"></a>

### struct Calculator

A calculator that performs basic arithmetic operations.

The `Calculator` struct maintains a history of all operations performed, allowing users to review previous calculations.

### Examples

```rust
use calculator::Calculator;

let mut calc = Calculator::new();
let sum = calc.add(10.0, 5.0);
assert_eq!(sum, 15.0);
```

### Implementations

### impl [Calculator](#calculator-Calculator)

### Functions

<a id="calculator-Calculator-add"></a>

### fn add(&mut self, a: f64, b: f64) -> f64

Adds two numbers together.

### Arguments

* `a` - The first operand
* `b` - The second operand

### Returns

The sum of `a` and `b`.

### Examples

```rust
use calculator::Calculator;

let mut calc = Calculator::new();
assert_eq!(calc.add(2.0, 3.0), 5.0);
```

<a id="calculator-Calculator-calculate"></a>

### fn calculate(&mut self, a: f64, b: f64, op: [Operation](#calculator-Operation)) -> f64

Performs a calculation using the specified operation.

### Arguments

* `a` - The first operand
* `b` - The second operand
* `op` - The operation to perform

### Returns

The result of the operation.

### Panics

Panics if dividing by zero. Use [`Calculator::divide`](#calculator-Calculator-divide) for safe division.

<a id="calculator-Calculator-clear_history"></a>

### fn clear_history(&mut self)

Clears the operation history.

### Examples

```rust
use calculator::Calculator;

let mut calc = Calculator::new();
calc.add(1.0, 2.0);
assert!(!calc.history().is_empty());
calc.clear_history();
assert!(calc.history().is_empty());
```

<a id="calculator-Calculator-divide"></a>

### fn divide(&mut self, a: f64, b: f64) -> Result<f64, [CalculatorError](#calculator-CalculatorError)>

Divides the first number by the second.

### Arguments

* `a` - The dividend
* `b` - The divisor

### Returns

The quotient `a / b`, or an error if `b` is zero.

### Errors

Returns a `DivisionByZero` error if `b` is zero.

### Examples

```rust
use calculator::Calculator;

let mut calc = Calculator::new();
assert_eq!(calc.divide(10.0, 2.0).unwrap(), 5.0);
assert!(calc.divide(10.0, 0.0).is_err());
```

<a id="calculator-Calculator-history"></a>

### fn history(&self) -> &[[OperationResult](#calculator-OperationResult)]

Returns a reference to the operation history.

### Returns

A slice containing all operations performed by this calculator.

<a id="calculator-Calculator-multiply"></a>

### fn multiply(&mut self, a: f64, b: f64) -> f64

Multiplies two numbers together.

### Arguments

* `a` - The first factor
* `b` - The second factor

### Returns

The product of `a` and `b`.

### Examples

```rust
use calculator::Calculator;

let mut calc = Calculator::new();
assert_eq!(calc.multiply(3.0, 4.0), 12.0);
```

<a id="calculator-Calculator-new"></a>

### fn new() -> Self

Creates a new Calculator instance with an empty history.

### Returns

A new `Calculator` with no operation history.

### Examples

```rust
use calculator::Calculator;

let calc = Calculator::new();
assert!(calc.history().is_empty());
```

<a id="calculator-Calculator-subtract"></a>

### fn subtract(&mut self, a: f64, b: f64) -> f64

Subtracts the second number from the first.

### Arguments

* `a` - The minuend
* `b` - The subtrahend

### Returns

The difference `a - b`.

### Examples

```rust
use calculator::Calculator;

let mut calc = Calculator::new();
assert_eq!(calc.subtract(10.0, 4.0), 6.0);
```

<a id="calculator-OperationResult"></a>

### struct OperationResult

The result of a calculation, including operands and the operation performed.

<a id="calculator-OperationResult-operand_a"></a>

### operand_a: f64

The first operand

<a id="calculator-OperationResult-operand_b"></a>

### operand_b: f64

The second operand

<a id="calculator-OperationResult-operation"></a>

### operation: [Operation](#calculator-Operation)

The operation that was performed

<a id="calculator-OperationResult-result"></a>

### result: f64

The calculated result

### Traits implemented

<a id="calculator-OperationResult-Display"></a>

### impl std::fmt::Display for [OperationResult](#calculator-OperationResult)

<a id="calculator-ScientificCalculator"></a>

### struct ScientificCalculator

A scientific calculator with additional mathematical functions.

Extends the basic [`Calculator`](../../docs/src/api.html.md#Calculator) with trigonometric, logarithmic, and other advanced mathematical operations.

### Implementations

### impl [ScientificCalculator](#calculator-ScientificCalculator)

### Functions

<a id="calculator-ScientificCalculator-basic"></a>

### fn basic(&self) -> &[Calculator](#calculator-Calculator)

Returns a reference to the underlying basic calculator.

<a id="calculator-ScientificCalculator-basic_mut"></a>

### fn basic_mut(&mut self) -> &mut [Calculator](#calculator-Calculator)

Returns a mutable reference to the underlying basic calculator.

<a id="calculator-ScientificCalculator-cos"></a>

### fn cos(&self, angle: f64) -> f64

Calculates the cosine of an angle.

### Arguments

* `angle` - The angle (in degrees or radians based on settings)

### Returns

The cosine of the angle.

<a id="calculator-ScientificCalculator-ln"></a>

### fn ln(&self, x: f64) -> Result<f64, [CalculatorError](#calculator-CalculatorError)>

Calculates the natural logarithm of a number.

### Arguments

* `x` - The number (must be positive)

### Returns

The natural logarithm of x, or an error if x <= 0.

<a id="calculator-ScientificCalculator-new"></a>

### fn new() -> Self

Creates a new ScientificCalculator.

By default, trigonometric functions use radians.

<a id="calculator-ScientificCalculator-pow"></a>

### fn pow(&self, base: f64, exponent: f64) -> f64

Raises a number to a power.

### Arguments

* `base` - The base number
* `exponent` - The exponent

### Returns

`base` raised to the power of `exponent`.

<a id="calculator-ScientificCalculator-set_use_degrees"></a>

### fn set_use_degrees(&mut self, use_degrees: bool)

Sets whether to use degrees for trigonometric functions.

### Arguments

* `use_degrees` - If true, trig functions expect degrees; if false, radians.

<a id="calculator-ScientificCalculator-sin"></a>

### fn sin(&self, angle: f64) -> f64

Calculates the sine of an angle.

### Arguments

* `angle` - The angle (in degrees or radians based on settings)

### Returns

The sine of the angle.

<a id="calculator-ScientificCalculator-sqrt"></a>

### fn sqrt(&self, x: f64) -> f64

Calculates the square root of a number.

### Arguments

* `x` - The number (must be non-negative)

### Returns

The square root of x, or NaN if x is negative.
