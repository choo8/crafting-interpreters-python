from typing import List
from _return import Return
from environment import Environment
from lox_callable import LoxCallable
from stmt import Function


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment):
        self._closure = closure
        self._declaration = declaration

    def to_string(self) -> str:
        return f"fn {self._declaration.name.lexme}>"

    def arity(self) -> int:
        return len(self._declaration.params)

    def call(self, interpreter: "Interpreter", arguments: List[object]) -> object:
        environment = Environment(self._closure)
        for idx, param in enumerate(self._declaration.params):
            environment.define(param.lexme, arguments[idx])

        try:
            interpreter.execute_block(self._declaration.body, environment)
        except Return as return_value:
            return return_value.value
        return None
