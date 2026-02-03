/**
 * Basic arithmetic operations.
 * @module operations
 */

/**
 * Adds two numbers together.
 * 
 * @param {number} a - The first number.
 * @param {number} b - The second number.
 * @returns {number} The sum of a and b.
 * @example
 * const result = add(5, 3);
 * console.log(result); // 8
 */
export function add(a, b) {
    return a + b;
}

/**
 * Subtracts the second number from the first.
 * 
 * @param {number} a - The number to subtract from.
 * @param {number} b - The number to subtract.
 * @returns {number} The difference of a and b.
 * @example
 * const result = subtract(10, 4);
 * console.log(result); // 6
 */
export function subtract(a, b) {
    return a - b;
}

/**
 * Multiplies two numbers together.
 * 
 * @param {number} a - The first number.
 * @param {number} b - The second number.
 * @returns {number} The product of a and b.
 * @example
 * const result = multiply(4, 5);
 * console.log(result); // 20
 */
export function multiply(a, b) {
    return a * b;
}

/**
 * Divides the first number by the second.
 * 
 * @param {number} a - The dividend.
 * @param {number} b - The divisor.
 * @returns {number} The quotient of a divided by b.
 * @throws {Error} If b is zero.
 * @example
 * const result = divide(20, 4);
 * console.log(result); // 5
 */
export function divide(a, b) {
    if (b === 0) {
        throw new Error('Division by zero');
    }
    return a / b;
}

/**
 * Calculates the power of a number.
 * 
 * @param {number} base - The base number.
 * @param {number} exponent - The exponent.
 * @returns {number} The result of base raised to the power of exponent.
 * @example
 * const result = power(2, 3);
 * console.log(result); // 8
 */
export function power(base, exponent) {
    return Math.pow(base, exponent);
}

/**
 * Calculates the square root of a number.
 * 
 * @param {number} n - The number to calculate the square root of.
 * @returns {number} The square root of n.
 * @throws {Error} If n is negative.
 * @example
 * const result = sqrt(16);
 * console.log(result); // 4
 */
export function sqrt(n) {
    if (n < 0) {
        throw new Error('Cannot calculate square root of negative number');
    }
    return Math.sqrt(n);
}
