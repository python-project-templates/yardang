/**
 * Calculator Library
 * 
 * A simple calculator library demonstrating JavaScript documentation with sphinx-js.
 * 
 * This module provides basic arithmetic operations and a Calculator class
 * that maintains a history of operations.
 * 
 * @module calculator
 * @example
 * import { Calculator, add, subtract } from 'calculator';
 * 
 * const calc = new Calculator();
 * const result = calc.calculate(5, 3, 'add');
 * console.log(result); // 8
 */

import { Calculator } from './calculator.js';
import { add, subtract, multiply, divide } from './operations.js';

export { Calculator, add, subtract, multiply, divide };
