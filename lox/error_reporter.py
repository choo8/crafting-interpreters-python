import sys
from functools import singledispatchmethod
from token import Token
from token_type import TokenType


class ErrorReporter:
    def __init__(self):
        self.had_error = False

    @singledispatchmethod
    def error(self, arg, msg: str) -> None:
        pass

    @error.register
    def _(self, line: int, msg: str) -> None:
        self.report(line, "", msg)

    def report(self, line: int, where: str, msg: str) -> None:
        print(f"[line {line}] Error{where}: {msg}", file=sys.stderr)
        self.had_error = True

    @error.register
    def _(self, token: Token, msg: str) -> None:
        if token.type == TokenType.EOF:
            self.report(token.line, " at end", msg)
        else:
            self.report(token.line, f" at '{token.lexme}'", msg)

error_reporter = ErrorReporter()
