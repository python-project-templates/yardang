//! # Calculator Library
//!
//! A simple calculator library demonstrating Rust documentation with sphinx-rust.
//!
//! This crate provides basic arithmetic operations and a calculator struct
//! that maintains a history of operations.
//!
//! ## Example
//!
//! ```rust
//! use calculator::{Calculator, Operation};
//!
//! let mut calc = Calculator::new();
//! let result = calc.calculate(5.0, 3.0, Operation::Add);
//! assert_eq!(result, 8.0);
//! ```

mod operations;

pub use operations::{Operation, OperationResult};

/// A calculator that performs basic arithmetic operations.
///
/// The `Calculator` struct maintains a history of all operations performed,
/// allowing users to review previous calculations.
///
/// # Examples
///
/// ```rust
/// use calculator::Calculator;
///
/// let mut calc = Calculator::new();
/// let sum = calc.add(10.0, 5.0);
/// assert_eq!(sum, 15.0);
/// ```
#[derive(Debug, Default)]
pub struct Calculator {
    /// History of operations performed
    history: Vec<OperationResult>,
}

impl Calculator {
    /// Creates a new Calculator instance with an empty history.
    ///
    /// # Returns
    ///
    /// A new `Calculator` with no operation history.
    ///
    /// # Examples
    ///
    /// ```rust
    /// use calculator::Calculator;
    ///
    /// let calc = Calculator::new();
    /// assert!(calc.history().is_empty());
    /// ```
    #[must_use]
    pub fn new() -> Self {
        Self {
            history: Vec::new(),
        }
    }

    /// Adds two numbers together.
    ///
    /// # Arguments
    ///
    /// * `a` - The first operand
    /// * `b` - The second operand
    ///
    /// # Returns
    ///
    /// The sum of `a` and `b`.
    ///
    /// # Examples
    ///
    /// ```rust
    /// use calculator::Calculator;
    ///
    /// let mut calc = Calculator::new();
    /// assert_eq!(calc.add(2.0, 3.0), 5.0);
    /// ```
    pub fn add(&mut self, a: f64, b: f64) -> f64 {
        let result = a + b;
        self.record(a, b, Operation::Add, result);
        result
    }

    /// Subtracts the second number from the first.
    ///
    /// # Arguments
    ///
    /// * `a` - The minuend
    /// * `b` - The subtrahend
    ///
    /// # Returns
    ///
    /// The difference `a - b`.
    ///
    /// # Examples
    ///
    /// ```rust
    /// use calculator::Calculator;
    ///
    /// let mut calc = Calculator::new();
    /// assert_eq!(calc.subtract(10.0, 4.0), 6.0);
    /// ```
    pub fn subtract(&mut self, a: f64, b: f64) -> f64 {
        let result = a - b;
        self.record(a, b, Operation::Subtract, result);
        result
    }

    /// Multiplies two numbers together.
    ///
    /// # Arguments
    ///
    /// * `a` - The first factor
    /// * `b` - The second factor
    ///
    /// # Returns
    ///
    /// The product of `a` and `b`.
    ///
    /// # Examples
    ///
    /// ```rust
    /// use calculator::Calculator;
    ///
    /// let mut calc = Calculator::new();
    /// assert_eq!(calc.multiply(3.0, 4.0), 12.0);
    /// ```
    pub fn multiply(&mut self, a: f64, b: f64) -> f64 {
        let result = a * b;
        self.record(a, b, Operation::Multiply, result);
        result
    }

    /// Divides the first number by the second.
    ///
    /// # Arguments
    ///
    /// * `a` - The dividend
    /// * `b` - The divisor
    ///
    /// # Returns
    ///
    /// The quotient `a / b`, or an error if `b` is zero.
    ///
    /// # Errors
    ///
    /// Returns a `DivisionByZero` error if `b` is zero.
    ///
    /// # Examples
    ///
    /// ```rust
    /// use calculator::Calculator;
    ///
    /// let mut calc = Calculator::new();
    /// assert_eq!(calc.divide(10.0, 2.0).unwrap(), 5.0);
    /// assert!(calc.divide(10.0, 0.0).is_err());
    /// ```
    pub fn divide(&mut self, a: f64, b: f64) -> Result<f64, CalculatorError> {
        if b == 0.0 {
            return Err(CalculatorError::DivisionByZero);
        }
        let result = a / b;
        self.record(a, b, Operation::Divide, result);
        Ok(result)
    }

    /// Performs a calculation using the specified operation.
    ///
    /// # Arguments
    ///
    /// * `a` - The first operand
    /// * `b` - The second operand
    /// * `op` - The operation to perform
    ///
    /// # Returns
    ///
    /// The result of the operation.
    ///
    /// # Panics
    ///
    /// Panics if dividing by zero. Use [`Calculator::divide`] for safe division.
    pub fn calculate(&mut self, a: f64, b: f64, op: Operation) -> f64 {
        match op {
            Operation::Add => self.add(a, b),
            Operation::Subtract => self.subtract(a, b),
            Operation::Multiply => self.multiply(a, b),
            Operation::Divide => self.divide(a, b).expect("Division by zero"),
        }
    }

    /// Returns a reference to the operation history.
    ///
    /// # Returns
    ///
    /// A slice containing all operations performed by this calculator.
    #[must_use]
    pub fn history(&self) -> &[OperationResult] {
        &self.history
    }

    /// Clears the operation history.
    ///
    /// # Examples
    ///
    /// ```rust
    /// use calculator::Calculator;
    ///
    /// let mut calc = Calculator::new();
    /// calc.add(1.0, 2.0);
    /// assert!(!calc.history().is_empty());
    /// calc.clear_history();
    /// assert!(calc.history().is_empty());
    /// ```
    pub fn clear_history(&mut self) {
        self.history.clear();
    }

    /// Records an operation in the history.
    fn record(&mut self, a: f64, b: f64, op: Operation, result: f64) {
        self.history.push(OperationResult {
            operand_a: a,
            operand_b: b,
            operation: op,
            result,
        });
    }
}

/// Errors that can occur during calculator operations.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CalculatorError {
    /// Attempted to divide by zero.
    DivisionByZero,
    /// The result overflowed.
    Overflow,
}

impl std::fmt::Display for CalculatorError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::DivisionByZero => write!(f, "Cannot divide by zero"),
            Self::Overflow => write!(f, "Calculation resulted in overflow"),
        }
    }
}

impl std::error::Error for CalculatorError {}

/// A scientific calculator with additional mathematical functions.
///
/// Extends the basic [`Calculator`] with trigonometric, logarithmic,
/// and other advanced mathematical operations.
#[derive(Debug, Default)]
pub struct ScientificCalculator {
    /// The underlying basic calculator
    basic: Calculator,
    /// Whether to use degrees (true) or radians (false) for trig functions
    use_degrees: bool,
}

impl ScientificCalculator {
    /// Creates a new ScientificCalculator.
    ///
    /// By default, trigonometric functions use radians.
    #[must_use]
    pub fn new() -> Self {
        Self {
            basic: Calculator::new(),
            use_degrees: false,
        }
    }

    /// Sets whether to use degrees for trigonometric functions.
    ///
    /// # Arguments
    ///
    /// * `use_degrees` - If true, trig functions expect degrees; if false, radians.
    pub fn set_use_degrees(&mut self, use_degrees: bool) {
        self.use_degrees = use_degrees;
    }

    /// Calculates the sine of an angle.
    ///
    /// # Arguments
    ///
    /// * `angle` - The angle (in degrees or radians based on settings)
    ///
    /// # Returns
    ///
    /// The sine of the angle.
    #[must_use]
    pub fn sin(&self, angle: f64) -> f64 {
        let radians = if self.use_degrees {
            angle.to_radians()
        } else {
            angle
        };
        radians.sin()
    }

    /// Calculates the cosine of an angle.
    ///
    /// # Arguments
    ///
    /// * `angle` - The angle (in degrees or radians based on settings)
    ///
    /// # Returns
    ///
    /// The cosine of the angle.
    #[must_use]
    pub fn cos(&self, angle: f64) -> f64 {
        let radians = if self.use_degrees {
            angle.to_radians()
        } else {
            angle
        };
        radians.cos()
    }

    /// Calculates the natural logarithm of a number.
    ///
    /// # Arguments
    ///
    /// * `x` - The number (must be positive)
    ///
    /// # Returns
    ///
    /// The natural logarithm of x, or an error if x <= 0.
    pub fn ln(&self, x: f64) -> Result<f64, CalculatorError> {
        if x <= 0.0 {
            return Err(CalculatorError::Overflow);
        }
        Ok(x.ln())
    }

    /// Calculates the square root of a number.
    ///
    /// # Arguments
    ///
    /// * `x` - The number (must be non-negative)
    ///
    /// # Returns
    ///
    /// The square root of x, or NaN if x is negative.
    #[must_use]
    pub fn sqrt(&self, x: f64) -> f64 {
        x.sqrt()
    }

    /// Raises a number to a power.
    ///
    /// # Arguments
    ///
    /// * `base` - The base number
    /// * `exponent` - The exponent
    ///
    /// # Returns
    ///
    /// `base` raised to the power of `exponent`.
    #[must_use]
    pub fn pow(&self, base: f64, exponent: f64) -> f64 {
        base.powf(exponent)
    }

    /// Returns a reference to the underlying basic calculator.
    #[must_use]
    pub fn basic(&self) -> &Calculator {
        &self.basic
    }

    /// Returns a mutable reference to the underlying basic calculator.
    pub fn basic_mut(&mut self) -> &mut Calculator {
        &mut self.basic
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        let mut calc = Calculator::new();
        assert_eq!(calc.add(2.0, 3.0), 5.0);
    }

    #[test]
    fn test_subtract() {
        let mut calc = Calculator::new();
        assert_eq!(calc.subtract(10.0, 4.0), 6.0);
    }

    #[test]
    fn test_multiply() {
        let mut calc = Calculator::new();
        assert_eq!(calc.multiply(3.0, 4.0), 12.0);
    }

    #[test]
    fn test_divide() {
        let mut calc = Calculator::new();
        assert_eq!(calc.divide(10.0, 2.0).unwrap(), 5.0);
    }

    #[test]
    fn test_divide_by_zero() {
        let mut calc = Calculator::new();
        assert!(calc.divide(10.0, 0.0).is_err());
    }

    #[test]
    fn test_history() {
        let mut calc = Calculator::new();
        calc.add(1.0, 2.0);
        calc.subtract(5.0, 3.0);
        assert_eq!(calc.history().len(), 2);
    }
}
