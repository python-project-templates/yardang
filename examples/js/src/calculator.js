/**
 * Calculator class for performing arithmetic operations.
 * @module calculator
 */

import { add, subtract, multiply, divide } from './operations.js';

/**
 * Enum for calculator operations.
 * @readonly
 * @enum {string}
 */
export const Operation = {
    /** Addition operation */
    ADD: 'add',
    /** Subtraction operation */
    SUBTRACT: 'subtract',
    /** Multiplication operation */
    MULTIPLY: 'multiply',
    /** Division operation */
    DIVIDE: 'divide'
};

/**
 * Represents a calculation result with metadata.
 * @typedef {Object} CalculationResult
 * @property {number} result - The result of the calculation.
 * @property {string} operation - The operation that was performed.
 * @property {number} operandA - The first operand.
 * @property {number} operandB - The second operand.
 * @property {Date} timestamp - When the calculation was performed.
 */

/**
 * A calculator that performs basic arithmetic operations and maintains history.
 * 
 * @class
 * @example
 * const calc = new Calculator();
 * const result = calc.calculate(10, 5, Operation.ADD);
 * console.log(result); // 15
 * console.log(calc.getHistory()); // [{...}]
 */
export class Calculator {
    /**
     * Creates a new Calculator instance.
     */
    constructor() {
        /**
         * The history of calculations.
         * @type {CalculationResult[]}
         * @private
         */
        this._history = [];
    }

    /**
     * Performs a calculation with the given operands and operation.
     * 
     * @param {number} a - The first operand.
     * @param {number} b - The second operand.
     * @param {Operation} operation - The operation to perform.
     * @returns {number} The result of the calculation.
     * @throws {Error} If an invalid operation is provided.
     * @example
     * const calc = new Calculator();
     * const sum = calc.calculate(5, 3, Operation.ADD); // 8
     * const diff = calc.calculate(10, 4, Operation.SUBTRACT); // 6
     */
    calculate(a, b, operation) {
        let result;
        
        switch (operation) {
            case Operation.ADD:
                result = add(a, b);
                break;
            case Operation.SUBTRACT:
                result = subtract(a, b);
                break;
            case Operation.MULTIPLY:
                result = multiply(a, b);
                break;
            case Operation.DIVIDE:
                result = divide(a, b);
                break;
            default:
                throw new Error(`Invalid operation: ${operation}`);
        }

        this._history.push({
            result,
            operation,
            operandA: a,
            operandB: b,
            timestamp: new Date()
        });

        return result;
    }

    /**
     * Returns the history of all calculations.
     * 
     * @returns {CalculationResult[]} An array of calculation results.
     * @example
     * const calc = new Calculator();
     * calc.calculate(5, 3, Operation.ADD);
     * calc.calculate(10, 2, Operation.MULTIPLY);
     * const history = calc.getHistory();
     * console.log(history.length); // 2
     */
    getHistory() {
        return [...this._history];
    }

    /**
     * Clears the calculation history.
     * 
     * @returns {void}
     * @example
     * const calc = new Calculator();
     * calc.calculate(5, 3, Operation.ADD);
     * calc.clearHistory();
     * console.log(calc.getHistory().length); // 0
     */
    clearHistory() {
        this._history = [];
    }

    /**
     * Gets the last calculation result.
     * 
     * @returns {CalculationResult|null} The last calculation result, or null if no calculations have been made.
     */
    getLastResult() {
        if (this._history.length === 0) {
            return null;
        }
        return this._history[this._history.length - 1];
    }
}

/**
 * A scientific calculator with additional mathematical functions.
 * 
 * @class
 * @extends Calculator
 * @example
 * const sci = new ScientificCalculator();
 * const result = sci.sin(Math.PI / 2);
 * console.log(result); // 1
 */
export class ScientificCalculator extends Calculator {
    /**
     * Calculates the sine of an angle in radians.
     * 
     * @param {number} radians - The angle in radians.
     * @returns {number} The sine of the angle.
     */
    sin(radians) {
        return Math.sin(radians);
    }

    /**
     * Calculates the cosine of an angle in radians.
     * 
     * @param {number} radians - The angle in radians.
     * @returns {number} The cosine of the angle.
     */
    cos(radians) {
        return Math.cos(radians);
    }

    /**
     * Calculates the tangent of an angle in radians.
     * 
     * @param {number} radians - The angle in radians.
     * @returns {number} The tangent of the angle.
     */
    tan(radians) {
        return Math.tan(radians);
    }

    /**
     * Calculates the natural logarithm of a number.
     * 
     * @param {number} n - The number.
     * @returns {number} The natural logarithm of n.
     * @throws {Error} If n is not positive.
     */
    ln(n) {
        if (n <= 0) {
            throw new Error('Cannot calculate logarithm of non-positive number');
        }
        return Math.log(n);
    }

    /**
     * Calculates the base-10 logarithm of a number.
     * 
     * @param {number} n - The number.
     * @returns {number} The base-10 logarithm of n.
     * @throws {Error} If n is not positive.
     */
    log10(n) {
        if (n <= 0) {
            throw new Error('Cannot calculate logarithm of non-positive number');
        }
        return Math.log10(n);
    }
}
