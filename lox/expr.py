from typing import Generic, TypeVar


R = TypeVar("R")


class Expr:
    def __init__(self):
        pass


class Visitor(Generic[R]):
    def __init__(self):
        pass


subclasses = {
    "Binary": {"left": "Expr", "operator": "int", "right": "Expr"},
    "Grouping": {"expression": "Expr"},
    "Literal": {"value": "object"},
    "Unary": {"operator": "int", "right": "Expr"},
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
