from lox_callable import LoxCallable
from lox_instance import LoxInstance
from lox_function import LoxFunction
from typing import List, Dict


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: Dict[str, LoxFunction]):
        self._name = name
        self._methods = methods

    def find_method(self, name: str) -> LoxFunction:
        if name in self._methods:
            return self._methods[name]

        return None

    def __str__(self) -> str:
        return self._name

    def call(self, interpreter: "Interpreter", arguments: List[object]) -> object:
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()
