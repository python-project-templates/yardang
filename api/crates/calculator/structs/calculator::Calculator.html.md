<a id="struct-calculator-calculator"></a>

# Struct `calculator::Calculator`

<a id="calculator-Calculator"></a>

### pub struct Calculator(/\* private fields \*/);

A calculator that performs basic arithmetic operations.

The `Calculator` struct maintains a history of all operations performed, allowing users to review previous calculations.

<a id="examples"></a>

## Examples

```rust
use calculator::Calculator;  let mut calc = Calculator::new(); let sum = calc.add(10.0, 5.0); assert_eq!(sum, 15.0); 
```
