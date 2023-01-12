import expr
import stmt
from token import Token
from interpreter import Interpreter
from error_reporter import error_reporter
from enum import Enum
from typing import List, overload
from functools import singledispatchmethod


class FunctionType(Enum):
    NONE = 1
    FUNCTION = 2
    INTIALIZER = 3
    METHOD = 4


class ClassType(Enum):
    NONE = 1
    CLASS = 2


class Resolver(expr.Visitor[None], stmt.Visitor[None]):
    def __init__(self, interpreter: Interpreter):
        self._interpreter = interpreter
        self._scopes = []
        self._current_function = FunctionType.NONE
        self._current_class = ClassType.NONE

    @singledispatchmethod
    def _overloaded_resolve(self, arg) -> None:
        return NotImplemented

    @_overloaded_resolve.register
    def _(self, statements: list) -> None:
        for statement in statements:
            self._overloaded_resolve(statement)

    @_overloaded_resolve.register
    def _(self, _stmt: stmt.Stmt) -> None:
        _stmt.accept(self)

    @_overloaded_resolve.register
    def _(self, _expr: expr.Expr) -> None:
        _expr.accept(self)

    @overload
    def _resolve(self, statements: List[stmt.Stmt]) -> None:
        ...

    @overload
    def _resolve(self, _stmt: stmt.Stmt) -> None:
        ...

    @overload
    def _resolve(self, _expr: expr.Expr) -> None:
        ...

    def _resolve(self, *args, **kwargs) -> None:
        return self._overloaded_resolve(*args, **kwargs)

    def _resolve_function(self, function: stmt.Function, type: FunctionType) -> None:
        enclosing_function = self._current_function
        self._current_function = type

        self._begin_scope()
        for param in function.params:
            self._declare(param)
            self._define(param)
        self._resolve(function.body)
        self._end_scope()
        self._current_function = enclosing_function

    def _begin_scope(self) -> None:
        self._scopes.append({})

    def _end_scope(self) -> None:
        self._scopes.pop()

    def _declare(self, name: Token) -> None:
        if len(self._scopes) == 0:
            return

        if name.lexme in self._scopes[-1]:
            error_reporter.error(
                name, "Already a variable with this name in this scope."
            )

        self._scopes[-1][name.lexme] = False

    def _define(self, name: Token) -> None:
        if len(self._scopes) == 0:
            return
        self._scopes[-1][name.lexme] = True

    def _resolve_local(self, _expr: expr.Expr, name: Token) -> None:
        for idx in range(len(self._scopes) - 1, -1, -1):
            if name.lexme in self._scopes[idx]:
                self._interpreter.resolve(_expr, len(self._scopes) - 1 - idx)
                return

    def visit_block_stmt(self, _stmt: stmt.Block) -> None:
        self._begin_scope()
        self._resolve(_stmt.statements)
        self._end_scope()
        return None

    def visit_expression_stmt(self, _stmt: stmt.Expression) -> None:
        self._resolve(_stmt.expression)
        return None

    def visit_class_stmt(self, _stmt: stmt.Class) -> None:
        enclosing_class = self._current_class
        self._current_class = ClassType.CLASS

        self._declare(_stmt.name)
        self._define(_stmt.name)

        self._begin_scope()
        self._scopes[-1]["this"] = True

        for method in _stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.lexme == "init":
                declaration = FunctionType.INTIALIZER

            self._resolve_function(method, declaration)

        self._end_scope()

        self._current_class = enclosing_class
        return None

    def visit_if_stmt(self, _stmt: stmt.If) -> None:
        self._resolve(_stmt.condition)
        self._resolve(_stmt.then_branch)
        if _stmt.else_branch is not None:
            self._resolve(_stmt.else_branch)
        return None

    def visit_print_stmt(self, _stmt: stmt.Print) -> None:
        self._resolve(_stmt.expression)
        return None

    def visit_return_stmt(self, _stmt: stmt.Return) -> None:
        if self._current_function == FunctionType.NONE:
            error_reporter.error(_stmt.keyword, "Can't return from top-level code.")

        if _stmt.value is not None:
            if self._current_function == FunctionType.INTIALIZER:
                error_reporter.error(
                    _stmt.keyword, "Can't return a value from an initializer."
                )

            self._resolve(_stmt.value)

        return None

    def visit_function_stmt(self, _stmt: stmt.Function) -> None:
        self._declare(_stmt.name)
        self._define(_stmt.name)

        self._resolve_function(_stmt, FunctionType.FUNCTION)
        return None

    def visit_var_stmt(self, _stmt: stmt.Var) -> None:
        self._declare(_stmt.name)
        if _stmt.initializer is not None:
            self._resolve(_stmt.initializer)
        self._define(_stmt.name)
        return None

    def visit_while_stmt(self, _stmt: stmt.While) -> None:
        self._resolve(_stmt.condition)
        self._resolve(_stmt.body)
        return None

    def visit_assign_expr(self, _expr: expr.Assign) -> None:
        self._resolve(_expr.value)
        self._resolve_local(_expr, _expr.name)
        return None

    def visit_binary_expr(self, _expr: expr.Binary) -> None:
        self._resolve(_expr.left)
        self._resolve(_expr.right)
        return None

    def visit_call_expr(self, _expr: expr.Call) -> None:
        self._resolve(_expr.callee)

        for argument in _expr.arguments:
            self._resolve(argument)

        return None

    def visit_get_expr(self, _expr: expr.Get) -> None:
        self._resolve(_expr.object)
        return None

    def visit_grouping_expr(self, _expr: expr.Grouping) -> None:
        self._resolve(_expr.expression)
        return None

    def visit_literal_expr(self, _expr: expr.Literal) -> None:
        return None

    def visit_logical_expr(self, _expr: expr.Logical) -> None:
        self._resolve(_expr.left)
        self._resolve(_expr.right)
        return None

    def visit_set_expr(self, _expr: expr.Set) -> None:
        self._resolve(_expr.value)
        self._resolve(_expr.object)
        return None

    def visit_this_expr(self, _expr: expr.This) -> None:
        if self._current_class == ClassType.NONE:
            error_reporter.error(_expr.keyword, "Can't use 'this' outside of a class.")
            return None

        self._resolve_local(_expr, _expr.keyword)
        return None

    def visit_unary_expr(self, _expr: expr.Unary) -> None:
        self._resolve(_expr.right)
        return None

    def visit_variable_expr(self, _expr: expr.Variable) -> None:
        if (
            len(self._scopes) > 0
            and _expr.name.lexme in self._scopes[-1]
            and not self._scopes[-1][_expr.name.lexme]
        ):
            error_reporter.error(
                _expr.name, "Can't read local variable in its own initializer."
            )

        self._resolve_local(_expr, _expr.name)
        return None
