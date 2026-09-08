# JavaScript Calculator Example

This is an example JavaScript project demonstrating sphinx-js documentation with yardang.

## Features

- Basic arithmetic operations (add, subtract, multiply, divide)
- Calculator class with operation history
- Scientific calculator with trigonometric functions
- Full JSDoc documentation

## Usage

```javascript
import { Calculator, Operation, add, multiply } from 'calculator';

// Using standalone functions
const sum = add(5, 3);  // 8
const product = multiply(4, 5);  // 20

// Using the Calculator class
const calc = new Calculator();
calc.calculate(10, 5, Operation.ADD);  // 15
calc.calculate(20, 4, Operation.DIVIDE);  // 5

// View history
console.log(calc.getHistory());
```

## Documentation

Documentation is generated using JSDoc and integrated into the main yardang documentation using sphinx-js.
