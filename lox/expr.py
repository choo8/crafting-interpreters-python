from typing import Generic, TypeVar, List
from token import Token


R = TypeVar("R")


class Expr:
    def __init__(self):
        pass


class Visitor(Generic[R]):
    def __init__(self):
        pass


subclasses = {
    "Assign": {"name": "Token", "value": "Expr"},
    "Binary": {"left": "Expr", "operator": "int", "right": "Expr"},
    "Call": {"callee": "Expr", "paren": "Token", "arguments": "List[Expr]"},
    "Get": {"object": "Expr", "name": "Token"},
    "Grouping": {"expression": "Expr"},
    "Literal": {"value": "object"},
    "Logical": {"left": "Expr", "operator": "Token", "right": "Expr"},
    "Set": {"object": "Expr", "name": "Token", "value": "Expr"},
    "This": {"keyword": "Token"},
    "Unary": {"operator": "Token", "right": "Expr"},
    "Variable": {"name": "Token"},
}

for name, attributes in subclasses.items():
    # Initialize the class
    args = ""
    instance_init = ""
    for arg, arg_type in attributes.items():
        args += f", {arg}: {arg_type}"

    subclass_str = ""
    subclass_str += f"class {name}(Expr):\n"
    subclass_str += f"    def __init__(self{args}):\n"

    for arg in attributes:
        subclass_str += f"        self.{arg} = {arg}\n"

    subclass_str += "\n"
    subclass_str += "    def accept(self, visitor: Visitor[R]) -> R:\n"
    subclass_str += f"        return visitor.visit_{name.lower()}_expr(self)\n"

    # Exposes the class when module is imported
    exec(subclass_str, globals())
