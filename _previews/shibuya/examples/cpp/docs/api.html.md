<a id="calculator-c-api-documentation"></a>

# Calculator C++ API Documentation

This page demonstrates how to use breathe to document C++ code with yardang.

<a id="calculator-class"></a>

## Calculator Class

<a id="_CPPv4N4calc10CalculatorE"></a>

<a id="_CPPv3N4calc10CalculatorE"></a>

<a id="_CPPv2N4calc10CalculatorE"></a>

<a id="calc::Calculator"></a>

### class Calculator

A class for performing basic arithmetic operations. 

The [Calculator](#calculatorclasscalc_1_1_calculator) class provides methods for addition, subtraction, multiplication, and division. It also maintains a history of operations performed.

 Example usage: 
```default
[calc::Calculator](#calculatorclasscalc_1_1_calculator) [calc](../../../docs/src/api.md#calculatornamespacecalc); double result = [calc](../../../docs/src/api.md#calculatornamespacecalc).add(5.0, 3.0); std::cout << "Result: " << result << std::endl;
```

 #### NOTE
This is a thread-safe implementation.

Subclassed by [calc::ScientificCalculator](#calculatorclasscalc_1_1_scientific_calculator)

### Public Functions

<a id="_CPPv4N4calc10Calculator10CalculatorEv"></a>

<a id="_CPPv3N4calc10Calculator10CalculatorEv"></a>

<a id="_CPPv2N4calc10Calculator10CalculatorEv"></a>

<a id="calc::Calculator::Calculator"></a>

### Calculator()

Default constructor. 

Initializes an empty calculator with no operation history. 

<a id="_CPPv4N4calc10CalculatorD0Ev"></a>

<a id="_CPPv3N4calc10CalculatorD0Ev"></a>

<a id="_CPPv2N4calc10CalculatorD0Ev"></a>

<a id="calc::Calculator::~Calculator"></a>

### virtual ~Calculator()

Destructor. 

<a id="_CPPv4N4calc10Calculator3addEdd"></a>

<a id="_CPPv3N4calc10Calculator3addEdd"></a>

<a id="_CPPv2N4calc10Calculator3addEdd"></a>

<a id="calc::Calculator::add__double.double"></a>

### double add(double a, double b)

Add two numbers. 

#### SEE ALSO
[subtract()](#calculatorclasscalc_1_1_calculator_1a8a1a4353a488ca5a8e26e967df402b6c)

* **Parameters:**
  - **a** – The first operand. 
  - **b** – The second operand. 
* **Returns:**
  The sum of a and b.

<a id="_CPPv4N4calc10Calculator8subtractEdd"></a>

<a id="_CPPv3N4calc10Calculator8subtractEdd"></a>

<a id="_CPPv2N4calc10Calculator8subtractEdd"></a>

<a id="calc::Calculator::subtract__double.double"></a>

### double subtract(double a, double b)

Subtract two numbers. 

#### SEE ALSO
[add()](#calculatorclasscalc_1_1_calculator_1a02adca23edb571d1230a5b053a626c9a)

* **Parameters:**
  - **a** – The minuend. 
  - **b** – The subtrahend. 
* **Returns:**
  The difference (a - b).

<a id="_CPPv4N4calc10Calculator8multiplyEdd"></a>

<a id="_CPPv3N4calc10Calculator8multiplyEdd"></a>

<a id="_CPPv2N4calc10Calculator8multiplyEdd"></a>

<a id="calc::Calculator::multiply__double.double"></a>

### double multiply(double a, double b)

Multiply two numbers. 

#### SEE ALSO
[divide()](#calculatorclasscalc_1_1_calculator_1af2da2c13c4da6cffa5b1752ab581e606)

* **Parameters:**
  - **a** – The first factor. 
  - **b** – The second factor. 
* **Returns:**
  The product of a and b.

<a id="_CPPv4N4calc10Calculator6divideEdd"></a>

<a id="_CPPv3N4calc10Calculator6divideEdd"></a>

<a id="_CPPv2N4calc10Calculator6divideEdd"></a>

<a id="calc::Calculator::divide__double.double"></a>

### double divide(double a, double b)

Divide two numbers. 

#### SEE ALSO
[multiply()](#calculatorclasscalc_1_1_calculator_1a530db79a3c237b4ef5721b601e8e5ae4)

#### WARNING
Division by zero will throw an exception.

* **Parameters:**
  - **a** – The dividend. 
  - **b** – The divisor. 
* **Throws:**
   – if b is zero.
* **Returns:**
  The quotient (a / b).

<a id="_CPPv4NK4calc10Calculator10getHistoryEv"></a>

<a id="_CPPv3NK4calc10Calculator10getHistoryEv"></a>

<a id="_CPPv2NK4calc10Calculator10getHistoryEv"></a>

<a id="calc::Calculator::getHistoryC"></a>

### [std](../../../docs/src/api.md#_CPPv4St)::vector<[OperationResult](../../../docs/src/api.md#_CPPv4N4calc15OperationResultE)> getHistory() const

Get the history of all operations. 

* **Returns:**
  A vector containing all operation results. 

<a id="_CPPv4N4calc10Calculator12clearHistoryEv"></a>

<a id="_CPPv3N4calc10Calculator12clearHistoryEv"></a>

<a id="_CPPv2N4calc10Calculator12clearHistoryEv"></a>

<a id="calc::Calculator::clearHistory"></a>

### void clearHistory()

Clear the operation history. 

<a id="_CPPv4NK4calc10Calculator17getOperationCountEv"></a>

<a id="_CPPv3NK4calc10Calculator17getOperationCountEv"></a>

<a id="_CPPv2NK4calc10Calculator17getOperationCountEv"></a>

<a id="calc::Calculator::getOperationCountC"></a>

### size_t getOperationCount() const

Get the number of operations performed. 

* **Returns:**
  The count of operations in history. 

### Protected Functions

<a id="_CPPv4N4calc10Calculator15recordOperationERK15OperationResult"></a>

<a id="_CPPv3N4calc10Calculator15recordOperationERK15OperationResult"></a>

<a id="_CPPv2N4calc10Calculator15recordOperationERK15OperationResult"></a>

<a id="calc::Calculator::recordOperation__OperationResultCR"></a>

### void recordOperation(const [OperationResult](../../../docs/src/api.md#_CPPv4N4calc15OperationResultE) &result)

Record an operation in the history. 

* **Parameters:**
  **result** – The result to record. 

<a id="scientificcalculator-class"></a>

## ScientificCalculator Class

<a id="_CPPv4N4calc20ScientificCalculatorE"></a>

<a id="_CPPv3N4calc20ScientificCalculatorE"></a>

<a id="_CPPv2N4calc20ScientificCalculatorE"></a>

<a id="calc::ScientificCalculator"></a>

### class ScientificCalculator : public [calc](../../../docs/src/api.md#_CPPv44calc)::[Calculator](../../../docs/src/api.md#_CPPv4N4calc10CalculatorE)

An extended calculator with scientific functions. 

This class inherits from [Calculator](#calculatorclasscalc_1_1_calculator) and adds advanced mathematical operations like power and square root. 

### Public Functions

<a id="_CPPv4N4calc20ScientificCalculator5powerEdd"></a>

<a id="_CPPv3N4calc20ScientificCalculator5powerEdd"></a>

<a id="_CPPv2N4calc20ScientificCalculator5powerEdd"></a>

<a id="calc::ScientificCalculator::power__double.double"></a>

### double power(double base, double exponent)

Calculate the power of a number. 

* **Parameters:**
  - **base** – The base number. 
  - **exponent** – The exponent. 
* **Returns:**
  base raised to the power of exponent. 

<a id="_CPPv4N4calc20ScientificCalculator10squareRootEd"></a>

<a id="_CPPv3N4calc20ScientificCalculator10squareRootEd"></a>

<a id="_CPPv2N4calc20ScientificCalculator10squareRootEd"></a>

<a id="calc::ScientificCalculator::squareRoot__double"></a>

### double squareRoot(double value)

Calculate the square root of a number. 

* **Parameters:**
  **value** – The number to find the square root of. 
* **Throws:**
   – if value is negative. 
* **Returns:**
  The square root of value.

<a id="enumerations"></a>

## Enumerations

<a id="operation-enum"></a>

### Operation Enum

<a id="_CPPv4N4calc9OperationE"></a>

<a id="_CPPv3N4calc9OperationE"></a>

<a id="_CPPv2N4calc9OperationE"></a>

### enum class [calc](../../../docs/src/api.md#_CPPv44calc)::Operation

Enumeration of supported arithmetic operations. 

*Values:*

<a id="_CPPv4N4calc9Operation3ADDE"></a>

<a id="_CPPv3N4calc9Operation3ADDE"></a>

<a id="_CPPv2N4calc9Operation3ADDE"></a>

### enumerator ADD

Addition operation. 

<a id="_CPPv4N4calc9Operation8SUBTRACTE"></a>

<a id="_CPPv3N4calc9Operation8SUBTRACTE"></a>

<a id="_CPPv2N4calc9Operation8SUBTRACTE"></a>

### enumerator SUBTRACT

Subtraction operation. 

<a id="_CPPv4N4calc9Operation8MULTIPLYE"></a>

<a id="_CPPv3N4calc9Operation8MULTIPLYE"></a>

<a id="_CPPv2N4calc9Operation8MULTIPLYE"></a>

### enumerator MULTIPLY

Multiplication operation. 

<a id="_CPPv4N4calc9Operation6DIVIDEE"></a>

<a id="_CPPv3N4calc9Operation6DIVIDEE"></a>

<a id="_CPPv2N4calc9Operation6DIVIDEE"></a>

### enumerator DIVIDE

Division operation. 

<a id="structures"></a>

## Structures

<a id="operationresult"></a>

### OperationResult

<a id="_CPPv4N4calc15OperationResultE"></a>

<a id="_CPPv3N4calc15OperationResultE"></a>

<a id="_CPPv2N4calc15OperationResultE"></a>

<a id="calc::OperationResult"></a>

### struct OperationResult

Structure to hold the result of a calculation. 

### Public Members

<a id="_CPPv4N4calc15OperationResult5valueE"></a>

<a id="_CPPv3N4calc15OperationResult5valueE"></a>

<a id="_CPPv2N4calc15OperationResult5valueE"></a>

<a id="calc::OperationResult::value__double"></a>

### double value

The calculated value. 

<a id="_CPPv4N4calc15OperationResult9operationE"></a>

<a id="_CPPv3N4calc15OperationResult9operationE"></a>

<a id="_CPPv2N4calc15OperationResult9operationE"></a>

<a id="calc::OperationResult::operation__Operation"></a>

### [Operation](../../../docs/src/api.md#_CPPv4N4calc9OperationE) operation

The operation that was performed. 

<a id="_CPPv4N4calc15OperationResult11descriptionE"></a>

<a id="_CPPv3N4calc15OperationResult11descriptionE"></a>

<a id="_CPPv2N4calc15OperationResult11descriptionE"></a>

<a id="calc::OperationResult::description__ss"></a>

### [std](../../../docs/src/api.md#_CPPv4St)::string description

Human-readable description of the operation. 

<a id="functions"></a>

## Functions

<a id="formatnumber"></a>

### formatNumber

<a id="_CPPv4N4calc12formatNumberEdi"></a>

<a id="_CPPv3N4calc12formatNumberEdi"></a>

<a id="_CPPv2N4calc12formatNumberEdi"></a>

<a id="calc::formatNumber__double.i"></a>

### [std](../../../docs/src/api.md#_CPPv4St)::string [calc](../../../docs/src/api.md#_CPPv44calc)::formatNumber(double value, int precision = 2)

A helper function to format a number as a string. 

* **Parameters:**
  - **value** – The number to format. 
  - **precision** – The number of decimal places. 
* **Returns:**
  A formatted string representation. 

<a id="defines"></a>

## Defines

<a id="c.MAX_HISTORY_SIZE"></a>

### MAX_HISTORY_SIZE 1000

Maximum number of operations to store in history. 

<a id="type-definitions"></a>

## Type Definitions

<a id="_CPPv4N4calc11HistoryListE"></a>

<a id="_CPPv3N4calc11HistoryListE"></a>

<a id="_CPPv2N4calc11HistoryListE"></a>

<a id="calc::HistoryList"></a>

### typedef [std](../../../docs/src/api.md#_CPPv4St)::vector<[OperationResult](../../../docs/src/api.md#_CPPv4N4calc15OperationResultE)> [calc](../../../docs/src/api.md#_CPPv44calc)::HistoryList

Type alias for the operation history container.
