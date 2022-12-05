from expr import Visitor, Expr, Literal, Grouping, Unary, Binary
from token_type import TokenType
from token import Token
from runtime_error import RuntimeError
from error_reporter import error_reporter


class Interpreter(Visitor[object]):
    def __init__(self):
        pass

    def interpret(self, expression: Expr) -> None:
        try:
            value = self._evaluate(expression)
            print(self._stringify(value))
        except RuntimeError as error:
            error_reporter.runtime_error(error)

    def visit_literal_expr(self, expr: Literal) -> object:
        return expr.value

    def visit_unary_expr(self, expr: Unary) -> object:
        right = self._evaluate(expr.right)

        if expr.operator.type == TokenType.BANG:
            return not self._is_truthy(right)
        elif expr.operator.type == TokenType.MINUS:
            return -float(right)

        # Unreachable
        return None

    def _check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return
        raise RuntimeError(operand, "Operand must be a number.")

    def _check_number_operands(
        self, operator: Token, left: object, right: object
    ) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(operator, "Operands must be numbers.")

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return self._evaluate(expr.expression)

    def _is_truthy(self, object: object) -> bool:
        if object is None:
            return False
        if isinstance(object, bool):
            return bool(object)
        return True

    def _is_equal(self, a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False

        return a == b

    def _stringify(self, object: object) -> str:
        if object is None:
            return "nil"
        if isinstance(object, float):
            text = str(object)
            if text.endswith(".0"):
                text = text[: len(text) - 2]
            return text
        return str(object)

    def _evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> object:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        if expr.operator.type == TokenType.GREATER:
            self._check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == TokenType.LESS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.type == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            return float(left) - float(right)
        elif expr.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise RuntimeError(
                expr.operator, "Operands must be two numbers or two strings."
            )
        elif expr.operator.type == TokenType.SLASH:
            return float(left) / float(right)
        elif expr.operator.type == TokenType.STAR:
            self._check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)

        # Unreachable
        return None
