import expr
from token import Token
from token_type import TokenType


class AstPrinter(expr.Visitor[str]):
    def __init__(self):
        pass

    def print(self, expr: expr.Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: expr.Expr) -> str:
        return self.parenthesize(expr.operator.lexme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: expr.Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: expr.Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: expr.Unary) -> str:
        return self.parenthesize(expr.operator.lexme, expr.right)

    def parenthesize(self, name: str, *exprs: expr.Expr) -> str:
        builder = ""

        builder += f"({name}"
        for _expr in exprs:
            builder += f" {_expr.accept(self)}"
        builder += ")"

        return builder


if __name__ == "__main__":
    ast_printer = AstPrinter()
    expression = expr.Binary(
        expr.Unary(Token(TokenType.MINUS, "-", None, 1), expr.Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        expr.Grouping(expr.Literal(45.67)),
    )
    print(ast_printer.print(expression))
