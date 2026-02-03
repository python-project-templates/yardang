//! Operation types and results for the calculator.

/// Enumeration of supported arithmetic operations.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Operation {
    /// Addition operation (+)
    Add,
    /// Subtraction operation (-)
    Subtract,
    /// Multiplication operation (*)
    Multiply,
    /// Division operation (/)
    Divide,
}

impl std::fmt::Display for Operation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Add => write!(f, "+"),
            Self::Subtract => write!(f, "-"),
            Self::Multiply => write!(f, "*"),
            Self::Divide => write!(f, "/"),
        }
    }
}

/// The result of a calculation, including operands and the operation performed.
#[derive(Debug, Clone)]
pub struct OperationResult {
    /// The first operand
    pub operand_a: f64,
    /// The second operand
    pub operand_b: f64,
    /// The operation that was performed
    pub operation: Operation,
    /// The calculated result
    pub result: f64,
}

impl std::fmt::Display for OperationResult {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{} {} {} = {}",
            self.operand_a, self.operation, self.operand_b, self.result
        )
    }
}
