/**
 * @file calculator.hpp
 * @brief A simple calculator library demonstrating Doxygen documentation.
 *
 * This file contains the Calculator class and related utilities for
 * performing basic arithmetic operations.
 */

#ifndef CALCULATOR_HPP
#define CALCULATOR_HPP

#include <stdexcept>
#include <string>
#include <vector>

/**
 * @namespace calc
 * @brief The calculator namespace containing all calculator-related classes.
 */
namespace calc {

/**
 * @enum Operation
 * @brief Enumeration of supported arithmetic operations.
 */
enum class Operation {
    ADD,      ///< Addition operation
    SUBTRACT, ///< Subtraction operation
    MULTIPLY, ///< Multiplication operation
    DIVIDE    ///< Division operation
};

/**
 * @struct OperationResult
 * @brief Structure to hold the result of a calculation.
 */
struct OperationResult {
    double value;          ///< The calculated value
    Operation operation;   ///< The operation that was performed
    std::string description; ///< Human-readable description of the operation
};

/**
 * @class Calculator
 * @brief A class for performing basic arithmetic operations.
 *
 * The Calculator class provides methods for addition, subtraction,
 * multiplication, and division. It also maintains a history of
 * operations performed.
 *
 * @note This is a thread-safe implementation.
 *
 * Example usage:
 * @code
 * calc::Calculator calc;
 * double result = calc.add(5.0, 3.0);
 * std::cout << "Result: " << result << std::endl;
 * @endcode
 */
class Calculator {
public:
    /**
     * @brief Default constructor.
     *
     * Initializes an empty calculator with no operation history.
     */
    Calculator();

    /**
     * @brief Destructor.
     */
    virtual ~Calculator();

    /**
     * @brief Add two numbers.
     *
     * @param a The first operand.
     * @param b The second operand.
     * @return The sum of a and b.
     *
     * @see subtract()
     */
    double add(double a, double b);

    /**
     * @brief Subtract two numbers.
     *
     * @param a The minuend.
     * @param b The subtrahend.
     * @return The difference (a - b).
     *
     * @see add()
     */
    double subtract(double a, double b);

    /**
     * @brief Multiply two numbers.
     *
     * @param a The first factor.
     * @param b The second factor.
     * @return The product of a and b.
     *
     * @see divide()
     */
    double multiply(double a, double b);

    /**
     * @brief Divide two numbers.
     *
     * @param a The dividend.
     * @param b The divisor.
     * @return The quotient (a / b).
     *
     * @throws std::invalid_argument if b is zero.
     *
     * @warning Division by zero will throw an exception.
     *
     * @see multiply()
     */
    double divide(double a, double b);

    /**
     * @brief Get the history of all operations.
     *
     * @return A vector containing all operation results.
     */
    std::vector<OperationResult> getHistory() const;

    /**
     * @brief Clear the operation history.
     */
    void clearHistory();

    /**
     * @brief Get the number of operations performed.
     *
     * @return The count of operations in history.
     */
    size_t getOperationCount() const;

protected:
    /**
     * @brief Record an operation in the history.
     *
     * @param result The result to record.
     */
    void recordOperation(const OperationResult& result);

private:
    std::vector<OperationResult> history_; ///< History of operations
};

/**
 * @class ScientificCalculator
 * @brief An extended calculator with scientific functions.
 *
 * This class inherits from Calculator and adds advanced mathematical
 * operations like power and square root.
 */
class ScientificCalculator : public Calculator {
public:
    /**
     * @brief Calculate the power of a number.
     *
     * @param base The base number.
     * @param exponent The exponent.
     * @return base raised to the power of exponent.
     */
    double power(double base, double exponent);

    /**
     * @brief Calculate the square root of a number.
     *
     * @param value The number to find the square root of.
     * @return The square root of value.
     *
     * @throws std::invalid_argument if value is negative.
     */
    double squareRoot(double value);
};

/**
 * @brief A helper function to format a number as a string.
 *
 * @param value The number to format.
 * @param precision The number of decimal places.
 * @return A formatted string representation.
 */
std::string formatNumber(double value, int precision = 2);

/**
 * @def MAX_HISTORY_SIZE
 * @brief Maximum number of operations to store in history.
 */
#define MAX_HISTORY_SIZE 1000

/**
 * @typedef HistoryList
 * @brief Type alias for the operation history container.
 */
typedef std::vector<OperationResult> HistoryList;

} // namespace calc

#endif // CALCULATOR_HPP
