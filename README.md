# crafting-interpreters-python
My Python implementation of the Lox interpreter in [part II](https://craftinginterpreters.com/a-tree-walk-interpreter.html) of [Crafting Interpreters](https://craftinginterpreters.com/).

# Design Changes
1. Implemented an "ErrorReporter" class instead of using a "hadError" variable in the "Lox" class to indicate if an error occurred. As there are components within the "Lox" class that also performs error reporting (e.g. "Scanner" class), it will be easier to interface with an "ErrorReporter" object that is initialized when the "error_reporter" module is imported.

2. Dynamically created the subclasses of "Expr" class during import of "expr.py" instead of generating "expr.py" with a script.

# Potential Improvements
1. Token implementation to contain column that contains the lexme and its length
2. Coalescing run of errors during scanning to improve user experience
3. Implement support for C-style block comments, consider allowing them to nest.