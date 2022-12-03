from typing import List
from token import Token
from token_type import TokenType
from error_reporter import error_reporter
from expr import Expr, Binary, Unary, Literal, Grouping


class _ParseError(RuntimeError):
    pass


class Parser:
    def __init__(self, tokens: List[Token]):
        self._tokens = tokens
        self._current = 0

    def parse(self) -> Expr:
        try:
            return self._expression()
        except _ParseError:
            return None

    def _expression(self) -> Expr:
        return self._equality()

    def _equality(self) -> Expr:
        expr = self._comparison()

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)

        return expr

    def _comparison(self) -> Expr:
        expr = self._term()

        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)

        return expr

    def _term(self) -> Expr:
        expr = self._factor()

        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)

        return expr

    def _factor(self) -> Expr:
        expr = self._unary()

        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)

        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)

        return self._primary()

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _match(self, *types: TokenType) -> bool:
        for type in types:
            if self._check(type):
                self._advance()
                return True

        return False

    def _consume(self, type: TokenType, msg: str) -> Token:
        if self._check(type):
            return self._advance()

        raise self._error(self._peek(), msg)

    def _check(self, type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]

    def _error(self, token: Token, msg: str) -> _ParseError:
        error_reporter.error(token, msg)
        return _ParseError()

    def _synchronize(self) -> None:
        self._advance()

        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return

            if self._peek().type == TokenType.CLASS:
                return
            elif self._peek().type == TokenType.FUN:
                return
            elif self._peek().type == TokenType.VAR:
                return
            elif self._peek().type == TokenType.FOR:
                return
            elif self._peek().type == TokenType.IF:
                return
            elif self._peek().type == TokenType.WHILE:
                return
            elif self._peek().type == TokenType.PRINT:
                return
            elif self._peek().type == TokenType.RETURN:
                return

            self._advance()
