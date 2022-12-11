import expr
import stmt
from token_type import TokenType
from token import Token
from runtime_error import RuntimeError
from error_reporter import error_reporter
from environment import Environment
from typing import List


class Interpreter(expr.Visitor[object], stmt.Visitor[None]):
    def __init__(self):
        self._environment = Environment()

    def interpret(self, statements: List[stmt.Stmt]) -> None:
        try:
            for statement in statements:
                self._execute(statement)
        except RuntimeError as error:
            error_reporter.runtime_error(error)

    def visit_literal_expr(self, _expr: expr.Literal) -> object:
        return _expr.value

    def visit_logical_expr(self, _expr: expr.Logical) -> object:
        left = self._evaluate(_expr.left)

        if _expr.operator.type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if not self._is_truthy(left):
                return left

        return self._evaluate(_expr.right)

    def visit_unary_expr(self, _expr: expr.Unary) -> object:
        right = self._evaluate(_expr.right)

        if _expr.operator.type == TokenType.BANG:
            return not self._is_truthy(right)
        elif _expr.operator.type == TokenType.MINUS:
            self._check_number_operand(_expr.operator, right)
            return -float(right)

        # Unreachable
        return None

    def visit_variable_expr(self, _expr: expr.Variable) -> object:
        return self._environment.get(_expr.name)

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

    def visit_grouping_expr(self, _expr: expr.Grouping) -> object:
        return self._evaluate(_expr.expression)

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

    def _evaluate(self, _expr: expr.Expr) -> object:
        return _expr.accept(self)

    def _execute(self, _stmt: stmt.Stmt) -> None:
        _stmt.accept(self)

    def execute_block(
        self, statements: List[stmt.Stmt], environment: Environment
    ) -> None:
        previous = self._environment
        try:
            self._environment = environment

            for statement in statements:
                self._execute(statement)
        finally:
            self._environment = previous

    def visit_block_stmt(self, _stmt: stmt.Block) -> None:
        self.execute_block(_stmt.statements, Environment(self._environment))
        return None

    def visit_expression_stmt(self, _stmt: stmt.Stmt) -> None:
        self._evaluate(_stmt.expression)
        return None

    def visit_if_stmt(self, _stmt: stmt.If) -> None:
        if self._is_truthy(self._evaluate(_stmt.condition)):
            self._execute(_stmt.then_branch)
        elif _stmt.else_branch is not None:
            self._execute(_stmt.else_branch)
        return None

    def visit_print_stmt(self, _stmt: stmt.Stmt) -> None:
        value = self._evaluate(_stmt.expression)
        print(self._stringify(value))
        return None

    def visit_var_stmt(self, _stmt: stmt.Var) -> None:
        value = None
        if _stmt.initializer is not None:
            value = self._evaluate(_stmt.initializer)

        self._environment.define(_stmt.name.lexme, value)
        return None

    def visit_while_stmt(self, _stmt: stmt.While) -> None:
        while self._is_truthy(self._evaluate(_stmt.condition)):
            self._execute(_stmt.body)
        return None

    def visit_assign_expr(self, _expr: expr.Assign) -> object:
        value = self._evaluate(_expr.value)
        self._environment.assign(_expr.name, value)
        return value

    def visit_binary_expr(self, _expr: expr.Binary) -> object:
        left = self._evaluate(_expr.left)
        right = self._evaluate(_expr.right)

        if _expr.operator.type == TokenType.GREATER:
            self._check_number_operands(_expr.operator, left, right)
            return float(left) > float(right)
        elif _expr.operator.type == TokenType.GREATER_EQUAL:
            self._check_number_operands(_expr.operator, left, right)
            return float(left) >= float(right)
        elif _expr.operator.type == TokenType.LESS:
            self._check_number_operands(_expr.operator, left, right)
            return float(left) < float(right)
        elif _expr.operator.type == TokenType.LESS_EQUAL:
            self._check_number_operands(_expr.operator, left, right)
            return float(left) <= float(right)
        elif _expr.operator.type == TokenType.MINUS:
            self._check_number_operands(_expr.operator, left, right)
            return float(left) - float(right)
        elif _expr.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise RuntimeError(
                _expr.operator, "Operands must be two numbers or two strings."
            )
        elif _expr.operator.type == TokenType.SLASH:
            return float(left) / float(right)
        elif _expr.operator.type == TokenType.STAR:
            self._check_number_operands(_expr.operator, left, right)
            return float(left) * float(right)
        elif _expr.operator.type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        elif _expr.operator.type == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)

        # Unreachable
        return None
