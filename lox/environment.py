from typing import Self
from token import Token
from runtime_error import RuntimeError


class Environment:
    def __init__(self, enclosing: Self = None):
        self.enclosing = enclosing
        self._values = {}

    def get(self, name: Token) -> object:
        if name.lexme in self._values:
            return self._values[name.lexme]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise RuntimeError(name, f"Undefined variable '{name.lexme}'.")

    def assign(self, name: Token, value: object) -> None:
        if name.lexme in self._values:
            self._values[name.lexme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(name, f"Undefined variable '{name.lexme}'.")

    def define(self, name: str, value: object) -> None:
        self._values[name] = value
