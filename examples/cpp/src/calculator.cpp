/**
 * @file calculator.cpp
 * @brief Implementation of the Calculator class.
 */

#include "calculator.hpp"
#include <cmath>
#include <sstream>
#include <iomanip>

namespace calc {

Calculator::Calculator() : history_() {}

Calculator::~Calculator() {}

double Calculator::add(double a, double b) {
    double result = a + b;
    recordOperation({result, Operation::ADD, "Addition"});
    return result;
}

double Calculator::subtract(double a, double b) {
    double result = a - b;
    recordOperation({result, Operation::SUBTRACT, "Subtraction"});
    return result;
}

double Calculator::multiply(double a, double b) {
    double result = a * b;
    recordOperation({result, Operation::MULTIPLY, "Multiplication"});
    return result;
}

double Calculator::divide(double a, double b) {
    if (b == 0.0) {
        throw std::invalid_argument("Division by zero is not allowed");
    }
    double result = a / b;
    recordOperation({result, Operation::DIVIDE, "Division"});
    return result;
}

std::vector<OperationResult> Calculator::getHistory() const {
    return history_;
}

void Calculator::clearHistory() {
    history_.clear();
}

size_t Calculator::getOperationCount() const {
    return history_.size();
}

void Calculator::recordOperation(const OperationResult& result) {
    if (history_.size() < MAX_HISTORY_SIZE) {
        history_.push_back(result);
    }
}

double ScientificCalculator::power(double base, double exponent) {
    return std::pow(base, exponent);
}

double ScientificCalculator::squareRoot(double value) {
    if (value < 0.0) {
        throw std::invalid_argument("Cannot calculate square root of negative number");
    }
    return std::sqrt(value);
}

std::string formatNumber(double value, int precision) {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(precision) << value;
    return oss.str();
}

} // namespace calc
