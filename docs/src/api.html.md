<a id="api-reference"></a>

# API Reference

<a id="python-api"></a>

## Python API

<a id="module-yardang.build"></a>

<a id="yardang-build"></a>

### yardang.build

<a id="yardang.build.generate_docs_configuration"></a>

### yardang.build.generate_docs_configuration(\*, project: str | None = None, title: str | None = None, module: str | None = None, description: str | None = None, author: str | None = None, copyright: str | None = None, version: str | None = None, theme: str | None = None, docs_root: str | None = None, root: str | None = None, cname: str | None = None, pages: List | None = None, use_autoapi: bool | None = None, autoapi_ignore: List | None = None, custom_css: Path | None = None, custom_js: Path | None = None, html_output_dir: str | None = None, config_base: str | None = None, previous_versions: bool | None = False, adjust_arguments: Callable = None, adjust_template: Callable = None)

Generate Sphinx documentation configuration from pyproject.toml.

A context manager that creates a temporary Sphinx configuration (conf.py) based on settings from pyproject.toml and yields the configuration directory path for use with sphinx-build. If a conf.py already exists in the current directory, it yields the current directory instead.

Configuration is read from the `[tool.yardang]` section of pyproject.toml by default, with breathe/doxygen settings in `[tool.yardang.breathe]`.

* **Parameters:**
  - **project** – Project name. Falls back to `[project].name` or directory name.
  - **title** – Documentation title. Falls back to `[tool.yardang].title` or project name.
  - **module** – Python module name for autoapi. Falls back to project name with hyphens replaced by underscores.
  - **description** – Project description for metadata.
  - **author** – Author name. Falls back to first entry in `[project].authors`.
  - **copyright** – Copyright string. Falls back to author name.
  - **version** – Version string. Falls back to `[project].version`.
  - **theme** – Sphinx theme name. Defaults to `"furo"`.
  - **docs_root** – Base URL for hosted documentation. Used for canonical URLs.
  - **root** – Path to README or index file to use as documentation root.
  - **cname** – Custom domain name for GitHub Pages CNAME file.
  - **pages** – List of page paths to include in the toctree.
  - **use_autoapi** – Whether to use sphinx-autoapi for Python API docs. Defaults to `None` (auto-detect).
  - **custom_css** – Path or raw content for custom CSS. When unset, falls back to a bundled per-theme `{theme}.css` then the generic `custom.css`.
  - **custom_js** – Path or raw content for custom JS. When unset, falls back to a bundled per-theme `{theme}.js` then the generic `custom.js`.
  - **html_output_dir** – Directory where Sphinx writes HTML output. Custom CSS/JS are placed under `<html_output_dir>/_static`. Defaults to `docs/html`.
  - **config_base** – Base key in pyproject.toml for configuration. Defaults to `"tool.yardang"`.
  - **previous_versions** – Whether to generate previous versions documentation.
  - **adjust_arguments** – Callback to modify template arguments before rendering. Receives the args dict and should return the modified dict.
  - **adjust_template** – Callback to modify the Jinja2 template before rendering. Receives the template and should return the modified template.
* **Yields:**
  *str* –

  Path to directory containing the generated conf.py file,
  : or the current directory if conf.py already exists.
* **Raises:**
  **toml.TomlDecodeError** – If pyproject.toml is malformed.

### Example

Basic usage with sphinx-build:

```default
from yardang import generate_docs_configuration  with generate_docs_configuration() as config_dir:     subprocess.run(["sphinx-build", "-c", config_dir, ".", "docs/html"])
```

With custom arguments callback:

```default
def customize(args):     args["html_theme_options"]["sidebar_hide_name"] = True     return args  with generate_docs_configuration(adjust_arguments=customize) as config_dir:     # build docs...
```

#### NOTE
Breathe/Doxygen configuration is loaded from `[tool.yardang.breathe]` with the following options:

- `projects`: Dict mapping project names to Doxygen XML directories
- `default-project`: Default project for breathe directives
- `domain-by-extension`: Map file extensions to Sphinx domains
- `show-define-initializer`: Show macro initializer values (default: True)
- `show-enumvalue-initializer`: Show enum value initializers (default: True)
- `show-include`: Show #include directives (default: True)
- `use-project-refids`: Prefix refids with project name (default: True)

<a id="yardang.build.generate_wiki_configuration"></a>

### yardang.build.generate_wiki_configuration(\*, project: str = '', title: str = '', module: str = '', description: str = '', author: str = '', copyright: str = '', version: str = '', theme: str = 'furo', docs_root: str = '', root: str = '', cname: str = '', pages: List | None = None, use_autoapi: bool | None = None, autoapi_ignore: List | None = None, custom_css: Path | None = None, custom_js: Path | None = None, config_base: str = 'tool.yardang', previous_versions: bool | None = False, adjust_arguments: Callable = None, adjust_template: Callable = None)

Generate Sphinx configuration for GitHub Wiki markdown output.

A context manager similar to generate_docs_configuration, but configured for building markdown output suitable for GitHub Wiki using sphinx-markdown-builder.

This adds the sphinx_markdown_builder extension and sets appropriate options for GitHub-flavored markdown output.

* **Parameters:**
  - **project** – Project name. Falls back to `[project].name` or directory name.
  - **title** – Documentation title. Falls back to `[tool.yardang].title` or project name.
  - **module** – Python module name for autoapi. Falls back to project name with hyphens replaced by underscores.
  - **description** – Project description for metadata.
  - **author** – Author name. Falls back to first entry in `[project].authors`.
  - **copyright** – Copyright string. Falls back to author name.
  - **version** – Version string. Falls back to `[project].version`.
  - **theme** – Sphinx theme name. Defaults to `"furo"`.
  - **docs_root** – Base URL for hosted documentation. Used for canonical URLs.
  - **root** – Path to README or index file to use as documentation root.
  - **cname** – Custom domain name for GitHub Pages CNAME file.
  - **pages** – List of page paths to include in the toctree.
  - **use_autoapi** – Whether to use sphinx-autoapi for Python API docs.
  - **custom_css** – Path to custom CSS file.
  - **custom_js** – Path to custom JavaScript file.
  - **config_base** – Base key in pyproject.toml for configuration.
  - **previous_versions** – Whether to generate previous versions documentation.
  - **adjust_arguments** – Callback to modify template arguments before rendering.
  - **adjust_template** – Callback to modify the Jinja2 template before rendering.
* **Yields:**
  *tuple* –

  (config_dir, wiki_args) where config_dir is the path to the directory
  : containing the generated conf.py file, and wiki_args is a dict with wiki configuration for post-processing.

<a id="yardang.build.run_doxygen_if_needed"></a>

### yardang.build.run_doxygen_if_needed(breathe_projects: Dict[str, str], \*, force: bool = False, quiet: bool = False) → Dict[str, bool]

Run doxygen for breathe projects if needed.

For each project in breathe_projects, checks if the XML output directory exists. If not, attempts to find a Doxyfile in the parent directory and runs doxygen to generate the XML.

* **Parameters:**
  - **breathe_projects** – Dict mapping project names to XML output directories.
  - **force** – If True, run doxygen even if XML directory already exists.
  - **quiet** – If True, suppress doxygen output.
* **Returns:**
  Dict mapping project names to whether doxygen was run successfully. Returns empty dict if doxygen is not installed.

### Example

```pycon
>>> results = run_doxygen_if_needed({"mylib": "docs/xml"}) >>> if results.get("mylib"): ...     print("Doxygen ran successfully")
```

<a id="module-yardang.cli"></a>

<a id="yardang-cli"></a>

### yardang.cli

<a id="yardang.cli.build"></a>

### yardang.cli.build(\*, quiet: bool = False, debug: bool = False, pdb: bool = False, project: str | None = None, title: str | None = None, module: str | None = None, description: str | None = None, author: str | None = None, copyright: str | None = None, version: str | None = None, theme: str | None = None, docs_root: str | None = None, root: str | None = None, cname: str | None = None, pages: List[Path] | None = None, use_autoapi: bool | None = None, custom_css: Path | None = None, custom_js: Path | None = None, output: str = 'docs/html', config_base: str | None = 'tool.yardang', previous_versions: bool | None = False)

<a id="yardang.cli.debug"></a>

### yardang.cli.debug()

<a id="yardang.cli.main"></a>

### yardang.cli.main()

<a id="yardang.cli.preview"></a>

### yardang.cli.preview(\*, themes: List[str] | None = None, output: str = 'docs/html/_previews', quiet: bool = False, debug: bool = False, pdb: bool = False)

Build the documentation once per theme for side-by-side comparison.

For each theme in `themes` (defaulting to the themes yardang bundles defaults for), the docs are rendered into `<output>/<theme>`. Themes whose Sphinx package is not installed are skipped with a warning.

<a id="yardang.cli.wiki"></a>

### yardang.cli.wiki(\*, quiet: bool = False, debug: bool = False, pdb: bool = False, project: str | None = None, title: str | None = None, module: str | None = None, description: str | None = None, author: str | None = None, copyright: str | None = None, version: str | None = None, theme: str | None = None, docs_root: str | None = None, root: str | None = None, cname: str | None = None, pages: List[Path] | None = None, use_autoapi: bool | None = None, custom_css: Path | None = None, custom_js: Path | None = None, config_base: str | None = 'tool.yardang', previous_versions: bool | None = False, output_dir: str | None = None, skip_postprocess: bool = False)

Generate GitHub Wiki compatible markdown documentation.

Builds markdown output using sphinx-markdown-builder and post-processes it to be compatible with GitHub Wiki format, including: - Flattening directory structure - Renaming index.md to Home.md - Generating \_Sidebar.md navigation - Generating \_Footer.md - Fixing internal links

<a id="module-yardang.utils"></a>

<a id="yardang-utils"></a>

### yardang.utils

<a id="yardang.utils.get_config"></a>

### yardang.utils.get_config(section='', base='tool.yardang')

<a id="yardang.utils.get_config_flex"></a>

### yardang.utils.get_config_flex(section='', base='tool.yardang')

Look up a config key, accepting both hyphens and underscores.

Tries the hyphenated form first (TOML convention), then the underscored form (Sphinx convention). For example, looking up `html_extra_path` will try `html-extra-path` first, then `html_extra_path`.

<a id="c-example"></a>

## C++ Example

This is an example of documenting C++ code using breathe integration.

<a id="document-everything"></a>

### Document Everything

Use `doxygenindex` to document all symbols from Doxygen XML:

<a id="_CPPv4N4calc10CalculatorE"></a>

<a id="_CPPv3N4calc10CalculatorE"></a>

<a id="_CPPv2N4calc10CalculatorE"></a>

<a id="calc::Calculator"></a>

### class Calculator

 *#include <[calculator.hpp](#calculatorcalculator_8hpp)>*

A class for performing basic arithmetic operations. 

The [Calculator](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator) class provides methods for addition, subtraction, multiplication, and division. It also maintains a history of operations performed.

 Example usage: 
```default
[calc::Calculator](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator) [calc](#calculatornamespacecalc); double result = [calc](#calculatornamespacecalc).add(5.0, 3.0); std::cout << "Result: " << result << std::endl;
```

 #### NOTE
This is a thread-safe implementation.

Subclassed by [calc::ScientificCalculator](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_scientific_calculator)

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
[subtract()](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator_1a8a1a4353a488ca5a8e26e967df402b6c)

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
[add()](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator_1a02adca23edb571d1230a5b053a626c9a)

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
[divide()](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator_1af2da2c13c4da6cffa5b1752ab581e606)

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
[multiply()](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator_1a530db79a3c237b4ef5721b601e8e5ae4)

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

### [std](#_CPPv4St)::vector<[OperationResult](#_CPPv4N4calc15OperationResultE)> getHistory() const

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

### void recordOperation(const [OperationResult](#_CPPv4N4calc15OperationResultE) &result)

Record an operation in the history. 

* **Parameters:**
  **result** – The result to record. 

### Private Members

<a id="_CPPv4N4calc10Calculator8history_E"></a>

<a id="_CPPv3N4calc10Calculator8history_E"></a>

<a id="_CPPv2N4calc10Calculator8history_E"></a>

<a id="calc::Calculator::history___std::vector:OperationResult:"></a>

### [std](#_CPPv4St)::vector<[OperationResult](#_CPPv4N4calc15OperationResultE)> history_

History of operations. 

<a id="_CPPv4N4calc15OperationResultE"></a>

<a id="_CPPv3N4calc15OperationResultE"></a>

<a id="_CPPv2N4calc15OperationResultE"></a>

<a id="calc::OperationResult"></a>

### struct OperationResult

 *#include <[calculator.hpp](#calculatorcalculator_8hpp)>*

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

### [Operation](#_CPPv4N4calc9OperationE) operation

The operation that was performed. 

<a id="_CPPv4N4calc15OperationResult11descriptionE"></a>

<a id="_CPPv3N4calc15OperationResult11descriptionE"></a>

<a id="_CPPv2N4calc15OperationResult11descriptionE"></a>

<a id="calc::OperationResult::description__ss"></a>

### [std](#_CPPv4St)::string description

Human-readable description of the operation. 

<a id="_CPPv4N4calc20ScientificCalculatorE"></a>

<a id="_CPPv3N4calc20ScientificCalculatorE"></a>

<a id="_CPPv2N4calc20ScientificCalculatorE"></a>

<a id="calc::ScientificCalculator"></a>

### class ScientificCalculator : public [calc](#_CPPv44calc)::[Calculator](#_CPPv4N4calc10CalculatorE)

 *#include <[calculator.hpp](#calculatorcalculator_8hpp)>*

An extended calculator with scientific functions. 

This class inherits from [Calculator](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator) and adds advanced mathematical operations like power and square root. 

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

<a id="_CPPv44calc"></a>

<a id="_CPPv34calc"></a>

<a id="_CPPv24calc"></a>

<a id="calc"></a>

### namespace calc

The calculator namespace containing all calculator-related classes. 

### Typedefs

<a id="_CPPv4N4calc11HistoryListE"></a>

<a id="_CPPv3N4calc11HistoryListE"></a>

<a id="_CPPv2N4calc11HistoryListE"></a>

<a id="calc::HistoryList"></a>

### typedef [std](#_CPPv4St)::vector<[OperationResult](#_CPPv4N4calc15OperationResultE)> HistoryList

Type alias for the operation history container. 

### Enums

<a id="_CPPv4N4calc9OperationE"></a>

<a id="_CPPv3N4calc9OperationE"></a>

<a id="_CPPv2N4calc9OperationE"></a>

### enum class Operation

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

### Functions

<a id="_CPPv4N4calc12formatNumberEdi"></a>

<a id="_CPPv3N4calc12formatNumberEdi"></a>

<a id="_CPPv2N4calc12formatNumberEdi"></a>

<a id="calc::formatNumber__double.i"></a>

### [std](#_CPPv4St)::string formatNumber(double value, int precision = 2)

A helper function to format a number as a string. 

* **Parameters:**
  - **value** – The number to format. 
  - **precision** – The number of decimal places. 
* **Returns:**
  A formatted string representation. 

<a id="_CPPv4St"></a>

<a id="_CPPv3St"></a>

<a id="_CPPv2St"></a>

<a id="std"></a>

### namespace std

STL namespace. 

### *file* calculator.hpp

 *#include <stdexcept>* *#include <string>* *#include <vector>*

A simple calculator library demonstrating Doxygen documentation. 

This file contains the Calculator class and related utilities for performing basic arithmetic operations. 

### Defines

<a id="c.MAX_HISTORY_SIZE"></a>

### MAX_HISTORY_SIZE 1000

Maximum number of operations to store in history. 

### *file* calculator.cpp

 *#include “[calculator.hpp](#calculatorcalculator_8hpp)”* *#include <cmath>* *#include <sstream>* *#include <iomanip>*

Implementation of the Calculator class. 

### *dir* include

### *dir* src

<a id="document-individual-classes"></a>

### Document Individual Classes

Or document specific classes with `doxygenclass`:

### class Calculator

A class for performing basic arithmetic operations. 

The [Calculator](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator) class provides methods for addition, subtraction, multiplication, and division. It also maintains a history of operations performed.

 Example usage: 
```default
[calc::Calculator](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator) [calc](#calculatornamespacecalc); double result = [calc](#calculatornamespacecalc).add(5.0, 3.0); std::cout << "Result: " << result << std::endl;
```

 #### NOTE
This is a thread-safe implementation.

Subclassed by [calc::ScientificCalculator](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_scientific_calculator)

### Public Functions

### Calculator()

Default constructor. 

Initializes an empty calculator with no operation history. 

### virtual ~Calculator()

Destructor. 

### double add(double a, double b)

Add two numbers. 

#### SEE ALSO
[subtract()](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator_1a8a1a4353a488ca5a8e26e967df402b6c)

* **Parameters:**
  - **a** – The first operand. 
  - **b** – The second operand. 
* **Returns:**
  The sum of a and b.

### double subtract(double a, double b)

Subtract two numbers. 

#### SEE ALSO
[add()](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator_1a02adca23edb571d1230a5b053a626c9a)

* **Parameters:**
  - **a** – The minuend. 
  - **b** – The subtrahend. 
* **Returns:**
  The difference (a - b).

### double multiply(double a, double b)

Multiply two numbers. 

#### SEE ALSO
[divide()](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator_1af2da2c13c4da6cffa5b1752ab581e606)

* **Parameters:**
  - **a** – The first factor. 
  - **b** – The second factor. 
* **Returns:**
  The product of a and b.

### double divide(double a, double b)

Divide two numbers. 

#### SEE ALSO
[multiply()](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator_1a530db79a3c237b4ef5721b601e8e5ae4)

#### WARNING
Division by zero will throw an exception.

* **Parameters:**
  - **a** – The dividend. 
  - **b** – The divisor. 
* **Throws:**
   – if b is zero.
* **Returns:**
  The quotient (a / b).

### [std](#_CPPv4St)::vector<[OperationResult](#_CPPv4N4calc15OperationResultE)> getHistory() const

Get the history of all operations. 

* **Returns:**
  A vector containing all operation results. 

### void clearHistory()

Clear the operation history. 

### size_t getOperationCount() const

Get the number of operations performed. 

* **Returns:**
  The count of operations in history. 

### class ScientificCalculator : public [calc](#_CPPv44calc)::[Calculator](#_CPPv4N4calc10CalculatorE)

An extended calculator with scientific functions. 

This class inherits from [Calculator](../../examples/cpp/docs/api.md#calculatorclasscalc_1_1_calculator) and adds advanced mathematical operations like power and square root. 

### Public Functions

### double power(double base, double exponent)

Calculate the power of a number. 

* **Parameters:**
  - **base** – The base number. 
  - **exponent** – The exponent. 
* **Returns:**
  base raised to the power of exponent. 

### double squareRoot(double value)

Calculate the square root of a number. 

* **Parameters:**
  **value** – The number to find the square root of. 
* **Throws:**
   – if value is negative. 
* **Returns:**
  The square root of value.

<a id="rust-example"></a>

## Rust Example

This is an example of documenting Rust code using sphinx-rust integration.

<a id="document-a-crate"></a>

### Document a Crate

Use `rust:crate` to document an entire Rust crate:

Version: 0.1.0

<a id="calculator"></a>

### pub mod calculator;[[source]](../../api/crates/calculator/code/calculator.md#rust-code-calculator)

<a id="calculator-library"></a>

#### Calculator Library

A simple calculator library demonstrating Rust documentation with sphinx-rust.

This crate provides basic arithmetic operations and a calculator struct that maintains a history of operations.

<a id="example"></a>

##### Example

```rust
use calculator::{Calculator, Operation};  let mut calc = Calculator::new(); let result = calc.calculate(5.0, 3.0, Operation::Add); assert_eq!(result, 8.0); 
```

<a id="id1"></a>

#### Structs

| [`Calculator`](../../api/crates/calculator/structs/calculator::Calculator.md#calculator-Calculator)                               | A calculator that performs basic arithmetic operations.         |
|-----------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| [`ScientificCalculator`](../../api/crates/calculator/structs/calculator::ScientificCalculator.md#calculator-ScientificCalculator) | A scientific calculator with additional mathematical functions. |

<a id="id2"></a>

#### Enums

| [`CalculatorError`](../../api/crates/calculator/enums/calculator::CalculatorError.md#calculator-CalculatorError)   | Errors that can occur during calculator operations.   |
|--------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|

<a id="document-individual-items"></a>

### Document Individual Items

Or document specific structs, enums, and functions:

<a id="calculator-Calculator"></a>

### pub struct Calculator(/\* private fields \*/);

A calculator that performs basic arithmetic operations.

The `Calculator` struct maintains a history of all operations performed, allowing users to review previous calculations.

<a id="examples"></a>

#### Examples

```rust
use calculator::Calculator;  let mut calc = Calculator::new(); let sum = calc.add(10.0, 5.0); assert_eq!(sum, 15.0); 
```

<a id="calculator-ScientificCalculator"></a>

### pub struct ScientificCalculator(/\* private fields \*/);

A scientific calculator with additional mathematical functions.

Extends the basic [`Calculator`] with trigonometric, logarithmic, and other advanced mathematical operations.

<a id="calculator-CalculatorError"></a>

### pub struct CalculatorError {    DivisionByZero(...),    Overflow(...),}

Errors that can occur during calculator operations.

#### Variants

* **DivisionByZero:**
  Attempted to divide by zero.
* **Overflow:**
  The result overflowed.

<a id="javascript-example"></a>

## JavaScript Example

This is an example of documenting JavaScript code using sphinx-js integration.

<a id="document-functions"></a>

### Document Functions

Use `js:autofunction` to document individual functions:

<a id="add"></a>

### *static* add(a, b)

Adds two numbers together.

* **Arguments:**
  - **a** (**number**) – The first number.
  - **b** (**number**) – The second number.
* **Returns:**
  **number** – The sum of a and b.

<a id="subtract"></a>

### *static* subtract(a, b)

Subtracts the second number from the first.

* **Arguments:**
  - **a** (**number**) – The number to subtract from.
  - **b** (**number**) – The number to subtract.
* **Returns:**
  **number** – The difference of a and b.

<a id="multiply"></a>

### *static* multiply(a, b)

Multiplies two numbers together.

* **Arguments:**
  - **a** (**number**) – The first number.
  - **b** (**number**) – The second number.
* **Returns:**
  **number** – The product of a and b.

<a id="divide"></a>

### *static* divide(a, b)

Divides the first number by the second.

* **Arguments:**
  - **a** (**number**) – The dividend.
  - **b** (**number**) – The divisor.
* **Throws:**
  **Error** – If b is zero.
* **Returns:**
  **number** – The quotient of a divided by b.

<a id="document-classes"></a>

### Document Classes

Use `js:autoclass` to document classes:

<a id="Calculator"></a>

### *class* Calculator()

A calculator that performs basic arithmetic operations and maintains history.

Creates a new Calculator instance.

<a id="Calculator.calculate"></a>

### Calculator.calculate(a, b, operation)

Performs a calculation with the given operands and operation.

* **Arguments:**
  - **a** (**number**) – The first operand.
  - **b** (**number**) – The second operand.
  - **operation** (**Operation**) – The operation to perform.
* **Throws:**
  **Error** – If an invalid operation is provided.
* **Returns:**
  **number** – The result of the calculation.

<a id="Calculator.clearHistory"></a>

### Calculator.clearHistory()

Clears the calculation history.

* **Returns:**
  **void**

<a id="Calculator.getHistory"></a>

### Calculator.getHistory()

Returns the history of all calculations.

* **Returns:**
  **Array.<CalculationResult>** – An array of calculation results.

<a id="Calculator.getLastResult"></a>

### Calculator.getLastResult()

Gets the last calculation result.

* **Returns:**
  **CalculationResult|null** – The last calculation result, or null if no calculations have been made.

<a id="ScientificCalculator"></a>

### *class* ScientificCalculator()

A scientific calculator with additional mathematical functions.

<a id="ScientificCalculator.cos"></a>

### ScientificCalculator.cos(radians)

Calculates the cosine of an angle in radians.

* **Arguments:**
  - **radians** (**number**) – The angle in radians.
* **Returns:**
  **number** – The cosine of the angle.

<a id="ScientificCalculator.ln"></a>

### ScientificCalculator.ln(n)

Calculates the natural logarithm of a number.

* **Arguments:**
  - **n** (**number**) – The number.
* **Throws:**
  **Error** – If n is not positive.
* **Returns:**
  **number** – The natural logarithm of n.

<a id="ScientificCalculator.log10"></a>

### ScientificCalculator.log10(n)

Calculates the base-10 logarithm of a number.

* **Arguments:**
  - **n** (**number**) – The number.
* **Throws:**
  **Error** – If n is not positive.
* **Returns:**
  **number** – The base-10 logarithm of n.

<a id="ScientificCalculator.sin"></a>

### ScientificCalculator.sin(radians)

Calculates the sine of an angle in radians.

* **Arguments:**
  - **radians** (**number**) – The angle in radians.
* **Returns:**
  **number** – The sine of the angle.

<a id="ScientificCalculator.tan"></a>

### ScientificCalculator.tan(radians)

Calculates the tangent of an angle in radians.

* **Arguments:**
  - **radians** (**number**) – The angle in radians.
* **Returns:**
  **number** – The tangent of the angle.
