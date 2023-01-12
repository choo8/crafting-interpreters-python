from time import time
from typing import List, Self
from types import MethodType
import expr
import stmt
from token_type import TokenType
from token import Token
from runtime_error import RuntimeError
from error_reporter import error_reporter
from environment import Environment
from lox_callable import LoxCallable
from lox_function import LoxFunction
from lox_class import LoxClass
from lox_instance import LoxInstance
from _return import Return


class Interpreter(expr.Visitor[object], stmt.Visitor[None]):
    def __init__(self):
        self.globals = Environment()
        self._environment = self.globals
        self._locals = {}

        def _arity(self) -> int:
            return 0

        def _call(self, interpreter: Self, arguments: List[object]) -> object:
            return float(time())

        def _to_string(self) -> str:
            return "<native fn>"

        clock = LoxCallable()
        clock.arity = MethodType(_arity, clock)
        clock.call = MethodType(_call, clock)
        clock.to_string = MethodType(_to_string, clock)

        self.globals.define("clock", clock)

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

    def visit_set_expr(self, _expr: expr.Set) -> object:
        _object = self._evaluate(_expr.object)

        if not isinstance(_object, LoxInstance):
            raise RuntimeError(_expr.name, "Only instances have fields.")

        value = self._evaluate(_expr.value)
        _object.set(_expr.name, value)
        return value

    def visit_this_expr(self, _expr: expr.This) -> object:
        return self._look_up_variable(_expr.keyword, _expr)

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
        return self._look_up_variable(_expr.name, _expr)

    def _look_up_variable(self, name: Token, _expr: expr.Expr) -> object:
        if _expr in self._locals:
            distance = self._locals[_expr]
            return self._environment.get_at(distance, name.lexme)
        else:
            return self.globals.get(name)

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

    def resolve(self, _expr: expr.Expr, depth: int) -> None:
        self._locals[_expr] = depth

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

    def visit_class_stmt(self, _stmt: stmt.Class) -> None:
        self._environment.define(_stmt.name.lexme, None)

        methods = {}
        for method in _stmt.methods:
            function = LoxFunction(
                method, self._environment, method.name.lexme == "init"
            )
            methods[method.name.lexme] = function

        klass = LoxClass(_stmt.name.lexme, methods)
        self._environment.assign(_stmt.name, klass)
        return None

    def visit_expression_stmt(self, _stmt: stmt.Stmt) -> None:
        self._evaluate(_stmt.expression)
        return None

    def visit_function_stmt(self, _stmt: stmt.Function) -> None:
        function = LoxFunction(_stmt, self._environment, False)
        self._environment.define(_stmt.name.lexme, function)
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

    def visit_return_stmt(self, _stmt: stmt.Return) -> None:
        value = None
        if _stmt.value is not None:
            value = self._evaluate(_stmt.value)

        raise Return(value)

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

        if _expr in self._locals:
            distance = self._locals[_expr]
            self._environment.assign_at(distance, _expr.name, value)
        else:
            self.globals.assign(_expr.name, value)

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

    def visit_call_expr(self, _expr: expr.Call) -> object:
        callee = self._evaluate(_expr.callee)

        arguments = []
        for argument in _expr.arguments:
            arguments.append(self._evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise RuntimeError(_expr.paren, "Can only call functions and classes.")

        function = callee
        if len(arguments) != function.arity():
            raise RuntimeError(
                _expr.paren,
                f"Expected {function.arity()} arguments but got {len(arguments)}.",
            )

        return function.call(self, arguments)

    def visit_get_expr(self, _expr: expr.Get) -> object:
        _object = self._evaluate(_expr.object)
        if isinstance(_object, LoxInstance):
            return _object.get(_expr.name)

        raise RuntimeError(_expr.name, "Only instances have properties.")
